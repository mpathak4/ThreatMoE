# ThreatMoE

ThreatMoE is a starter skeleton for an AI-driven real-time SOC threat-intelligence and anomaly detection platform.

Quick demo:
1. Put one JSON event per line in SampleTest.txt (see sample below).
2. Run: `python3 ThreatMoe.py`
3. Output: one JSON line per processed event with gating, expert logits, and predicted label.

Project layout:
- ThreatMoe.py    - demo entrypoint
- SampleTest.txt  - sample events
- Requirements.md  - dependencies and setup notes
