# Developer Guide

Local development
- Use .venv virtualenv (Python 3.10+) and install dependencies from requirements.txt.
- For training and encoding, use ThreatMoE.Encoder to guarantee consistent embeddings between training and runtime.

Running with a checkpoint
- Use run_with_ckpt.py to instantiate ThreatMoE, load models/demo_ckpt.pth (keys: "gating", "expert_0", ...), and emit telemetry to results/baseline_output_trained.jsonl.

Checkpoint format (required)
- Single PyTorch file with keys:
  - "gating" → state_dict for gating net
  - "expert_0", "expert_1", ... → state_dict for each expert
- Save with:
  torch.save({"gating": gating.state_dict(), "expert_0": expert0.state_dict(), ...}, ckpt_path)

Training recommendations
- Use ThreatMoE.Encoder in training scripts so embedding dims match runtime encoder.
- Deterministic behaviour: set torch.manual_seed(42) and deterministic data shuffling in experiments.
- Staged retraining: run local evaluation on golden canary dataset before promoting checkpoints.

Testing and CI
- Golden dataset tests: per-expert expected behaviors and gating distribution baselines.
- Parameter-delta checks: compute max_abs_diff vs prior checkpoint and alert if large.
- Canary evaluation: run proposed checkpoint on golden dataset and compare metrics before deployment.

Operational checklist before deploying a checkpoint
1. Verify checkpoint loads cleanly into ThreatMoE instance (max_abs_diff near 0).
2. Run canary eval and confirm metrics pass thresholds.
3. Verify gating/expert distribution drift is within acceptable bounds.
4. Sign and record deployment artifact with provenance metadata.

Contributing
- Use small, focused PRs that include tests for gating/expert behavior and update this DEV_GUIDE when interfaces change.
