#!/usr/bin/env python3
import os, json, torch
from ThreatMoe import ThreatMoE

# config
ckpt = "models/demo_ckpt.pth"
device = "cpu"
infile = "SampleTest.txt"
tele_out = "results/baseline_output_trained.jsonl"

# instantiate model
mo = ThreatMoE(device=device)

# load checkpoint if present and shapes match
if os.path.exists(ckpt):
    sd = torch.load(ckpt, map_location='cpu')
    if "gating" in sd:
        try:
            mo.gating.load_state_dict(sd["gating"])
            print("Loaded gating from", ckpt)
        except Exception as e:
            print("Failed to load gating:", e)
    for i,e in enumerate(getattr(mo, "experts", [])):
        key = f"expert_{i}"
        if key in sd:
            try:
                e.load_state_dict(sd[key])
                print("Loaded", key, "from", ckpt)
            except Exception as e:
                print("Failed to load", key, ":", e)

# run the same pipeline for each sample in infile and write telemetry
os.makedirs(os.path.dirname(tele_out) or ".", exist_ok=True)
with open(infile, "r", encoding="utf-8") as f, open(tele_out, "a", encoding="utf-8") as out:
    for line in f:
        line=line.strip()
        if not line: continue
        try:
            j=json.loads(line)
            raw = j.get("raw") or j.get("text") or line
        except:
            raw = line
        rec = mo.run_single({"raw": raw})
        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        out.flush()
print("Wrote telemetry to", tele_out)
