# Architecture Overview

High-level design
- Data plane: ingestion adapters → normalizer → enrichment pipelines → feature/vector store.
- Model plane: ThreatMoE gating network + specialist experts (Network, Endpoint, Malware, Email/Phish, Vulnerability, ThreatIntel, Identity, Cloud, OT). Each expert exposes run_single(event) and state_dict for checkpointing.
- Control plane: orchestration, retraining pipelines, canary testing, and deployment gates.
- Storage: immutable telemetry logs, versioned checkpoints, artifact provenance and audit trails.

ThreatIntel Expert role
- Input: event with raw text or IOC fields.
- Featurizer: uses ThreatMoE.Encoder (text embedding + structured IOC features).
- Expert head: classifier/regressor that outputs expert_logits, expert_probs, and an evidence/enrichment blob.
- Output: telemetry JSONL containing per-expert explainability and enrichment.

Sparse routing and fusion
- Gate receives the event embedding and selects a small subset of experts (top-k) based on gating logits.
- Selected experts produce per-expert probabilities and evidence; fusion layer aggregates (weighted) probabilities to produce the final label and confidence.
- Explainability: fused output includes per-expert contributions and the top evidence items.

Operational building blocks
- Ingest adapters: connectors for OTX, MISP, TAXII, CVE/NVD, vendor APIs, and custom feeds.
- Normalizer: canonical IOC schema with provenance and TTL.
- Enrichment: caching layer + enrichment workers for passive DNS, WHOIS, CT logs, vulnerability metadata.
- Vector store: lightweight embedding-based similarity for correlation/clustering.
- Checkpoint store: versioned model artifacts (gating + experts) with signatures and deployment metadata.

Security & operational controls
- Rate limits and caching for enrichment; signed ingestion for high-trust feeds.
- RBAC for feed management; audit logs for ingestion/enrichment/model operations.
- Canary evaluation: require golden dataset pass before checkpoint promotion.
