$(sed -n '1,200p' <<'TXT'
Developer workflow (quick)
- Use run_with_ckpt.py locally to load checkpoints and produce telemetry.
- Training: import ThreatMoE.Encoder and expert heads; save checkpoints with gating and expert_i keys.
TXT
)
