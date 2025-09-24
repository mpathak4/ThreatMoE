#!/usr/bin/env python3
"""
ThreatMoe.py - demo runner with real components (transformers + torch)

This demo is small, deterministic, and safe for local use:
- Embedding: distilbert-base-uncased (from transformers) or fallback to simple hashing if offline
- Gating: tiny MLP (PyTorch)
- Experts: small linear classifiers (PyTorch) that produce logits
- Fusion: average expert probabilities -> final probability
- Emits JSON lines to stdout (one JSON per event) and optionally to data/cybermoe_telemetry.jsonl

Notes:
- For production replace random-initialized models with trained weights.
- Use GPU by setting CYBERMOE_DEVICE=cuda if available.
"""
import os
import json
import time
import argparse
from typing import List, Dict, Any

# Try imports
USE_TRANSFORMERS = True
USE_TORCH = True
try:
    import torch
    import torch.nn as nn
except Exception:
    USE_TORCH = False
try:
    from transformers import AutoTokenizer, AutoModel
except Exception:
    USE_TRANSFORMERS = False

# Config
BACKBONE = os.environ.get("CYBERMOE_BACKBONE", "distilbert-base-uncased")
DEVICE = os.environ.get("CYBERMOE_DEVICE", "cpu")
TELE_PATH = os.environ.get("CYBERMOE_TELE", "data/cybermoe_telemetry.jsonl")

# Utilities
def emit_jsonl(path: str, record: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    line = json.dumps(record, ensure_ascii=False)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
        f.flush()
        try:
            import os as _os; _os.fsync(f.fileno())
        except Exception:
            pass

# Encoder: use transformers if available, otherwise a safe hash-based fallback
class Encoder:
    def __init__(self, backbone=BACKBONE, device="cpu"):
        self.device = device
        if USE_TRANSFORMERS:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(backbone)
                self.model = AutoModel.from_pretrained(backbone).to(device)
                self.model.eval()
                self.dim = self.model.config.hidden_size if hasattr(self.model.config, "hidden_size") else 768
            except Exception:
                # fallback
                self._fallback = True
                self.dim = 128
            else:
                self._fallback = False
        else:
            self._fallback = True
            self.dim = 128

    def encode(self, text: str):
        if not text:
            text = ""
        if not self._fallback and USE_TRANSFORMERS:
            with torch.no_grad():
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding="longest")
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                out = self.model(**inputs, output_hidden_states=False, return_dict=True)
                # mean-pool last hidden state
                hidden = out.last_hidden_state
                emb = hidden.mean(dim=1).squeeze(0).cpu().numpy().tolist()
                return emb
        # fallback: deterministic hash-based vector
        h = [float((hash(text + str(i)) % 1000) / 1000.0) for i in range(self.dim)]
        return h

# Tiny gating MLP
if USE_TORCH:
    class GatingNet(nn.Module):
        def __init__(self, in_dim: int, hidden: int = 64, num_experts: int = 3):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(in_dim, hidden),
                nn.ReLU(),
                nn.Linear(hidden, num_experts)
            )
        def forward(self, x):
            return self.net(x)
else:
    GatingNet = None

# Tiny expert classifier (linear)
if USE_TORCH:
    class ExpertNet(nn.Module):
        def __init__(self, in_dim: int, hidden: int = 32, num_classes: int = 2):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(in_dim, hidden),
                nn.ReLU(),
                nn.Linear(hidden, num_classes)
            )
        def forward(self, x):
            return self.net(x)
else:
    ExpertNet = None

# Demo pipeline container
class ThreatMoE:
    def __init__(self, device="cpu", num_experts=3):
        self.device = device
        self.encoder = Encoder(device=device)
        self.num_experts = num_experts
        self.dim = self.encoder.dim
        # init gating and experts with deterministic seeds for reproducibility
        if USE_TORCH:
            torch.manual_seed(42)
            self.gating = GatingNet(self.dim, hidden=64, num_experts=num_experts).to(device)
            self.experts = [ExpertNet(self.dim, hidden=32, num_classes=2).to(device) for _ in range(num_experts)]
            # small weight scaling so outputs are in a stable range
            for p in self.gating.parameters():
                p.data.mul_(0.1)
            for e in self.experts:
                for p in e.parameters():
                    p.data.mul_(0.1)
        else:
            self.gating = None
            self.experts = []

    def run_single(self, event: Dict[str, Any]) -> Dict[str, Any]:
        text = event.get("raw") or event.get("text") or ""
        emb = self.encoder.encode(text)
        ts = int(time.time() * 1000)

        # compute gating probs
        if USE_TORCH:
            x = torch.tensor(emb, dtype=torch.float32, device=self.device).unsqueeze(0)
            with torch.no_grad():
                logits = self.gating(x).squeeze(0)          # shape: (num_experts,)
                gating_probs = torch.softmax(logits, dim=0).cpu().numpy().tolist()
                topk_idx = sorted(range(len(gating_probs)), key=lambda i: gating_probs[i], reverse=True)[:2]
        else:
            # fallback uniform gating
            gating_probs = [1.0/self.num_experts]*self.num_experts
            topk_idx = list(range(min(2, self.num_experts)))

        # call experts (only top-k)
        expert_logits = {}
        expert_probs = {}
        for i in topk_idx:
            if USE_TORCH:
                x = torch.tensor(emb, dtype=torch.float32, device=self.device).unsqueeze(0)
                with torch.no_grad():
                    logit = self.experts[i](x).squeeze(0).cpu().numpy().tolist()
                expert_logits[i] = logit
                # softmax
                import math
                exps = [math.exp(v) for v in logit]
                ssum = sum(exps) or 1.0
                expert_probs[i] = [v/ssum for v in exps]
            else:
                # fallback deterministic stub
                expert_logits[i] = [0.1*i, 0.2*i+0.05]
                ssum = sum(expert_logits[i]) or 1.0
                expert_probs[i] = [v/ssum for v in expert_logits[i]]

        # fusion: weighted average of expert_probs using gating weights normalized over topk
        topk_weights = [gating_probs[i] for i in topk_idx]
        wsum = sum(topk_weights) or 1.0
        fused = [0.0, 0.0]
        for idx, w in zip(topk_idx, topk_weights):
            probs = expert_probs.get(idx, [0.0, 0.0])
            fused[0] += (w/wsum) * probs[0]
            fused[1] += (w/wsum) * probs[1]
        predicted_label = int(fused[1] > fused[0])
        predicted_prob = float(fused[1])

        out = {
            "event_id": event.get("event_id"),
            "ts_ms": ts,
            "raw": text,
            "embedding_len": len(emb),
            "gating": gating_probs,
            "topk_idx": topk_idx,
            "expert_logits": expert_logits,
            "expert_probs": expert_probs,
            "predicted_label": predicted_label,
            "predicted_prob": predicted_prob,
        }
        return out

# CLI
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", default="SampleTest.txt", help="Input file (one JSON per line or plain lines)")
    parser.add_argument("--telemetry", "-t", default=TELE_PATH, help="Telemetry JSONL path (appended)")
    parser.add_argument("--device", "-d", default=DEVICE, help="Device (cpu or cuda)")
    args = parser.parse_args()

    os.environ["CYBERMOE_DEVICE"] = args.device
    mo = ThreatMoE(device=args.device)

    with open(args.input, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except Exception:
                ev = {"event_id": f"line-{int(time.time()*1000)}", "raw": line}
            res = mo.run_single(ev)
            print(json.dumps(res, ensure_ascii=False))
            # also append to telemetry
            try:
                emit_jsonl(args.telemetry, res)
            except Exception:
                pass

if __name__ == "__main__":
    main()
