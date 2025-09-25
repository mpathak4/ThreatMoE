# ThreatIntel Expert for CyberMoE / ThreatMoE

Purpose
The ThreatIntel Expert is a domain specialist designed to ingest, normalize, enrich, correlate, and score Indicators of Compromise (IOCs), TTPs, and threat metadata from external feeds and analyst reports. It integrates into the CyberMoE architecture as a sparsely-invoked expert inside ThreatMoE, providing explainable evidence and structured enrichment that fuses with other experts (Network, Endpoint, Malware, Identity, Cloud, Vulnerability, OT) to produce robust detection and response signals.

Key capabilities
- Ingest: OTX, MISP, STIX/TAXII, CVE/NVD, commercial and custom IOC feeds.
- Normalize: canonical IOC schema (ip, cidr, fqdn, url, hash, cve, cpe, asn), provenance, timestamps.
- Enrich: passive DNS, WHOIS, certificate transparency, vulnerability metadata, OSINT.
- Correlate: cross-feed IOC linking, actor attribution heuristics, campaign stitching and timelines.
- Score & Prioritize: risk_score, confidence, recommended_action (block/investigate/monitor), asset exposure mapping.
- Explain: per-IOC evidence, provenance, top contributing features and per-expert explainability payloads.
- Interoperate: implements ThreatMoE expert API (state_dict load/save, run_single(event) → telemetry record).

Quick start
- Use run_with_ckpt.py to load a locally trained checkpoint and generate telemetry.
- See Requirements.md (repo contains a minimal Requirements.md; extend for production pins).
- For development, use ThreatMoE.Encoder as the canonical featurizer/encoder for expert training.

Repository layout (partial)
- ThreatMoE.py — demo runner and expert interface used in the repository.
- run_with_ckpt.py — wrapper to instantiate ThreatMoE, load checkpoint, and emit telemetry.
- models/demo_ckpt.pth — recommended location for gating/expert checkpoints.
- data/, results/ — sample data and telemetry outputs.
- docs/ (proposed) — ARCHITECTURE.md, THREAT_MODEL.md, EXPERT_MODULES.md, DEV_GUIDE.md.

Next actions
- Add/extend the docs in this repo (use the provided heredocs).
- Build an evaluation set and reproducible training script using ThreatMoE.Encoder.
