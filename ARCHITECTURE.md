$(sed -n '1,200p' <<'TXT'
Architecture overview
- Data plane: external feeds -> ingestion -> normalizer -> enrichment -> store
- Model plane: ThreatMoE gating + experts; ThreatIntel Expert as one expert
- Control plane: orchestration, audit, retraining pipelines
TXT
)
