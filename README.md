$(sed -n '1,200p' <<'TXT'
# ThreatIntel Expert for CyberMoE / ThreatMoE

Purpose
ThreatIntel Expert is a specialist module designed to ingest, normalize, enrich, correlate, and score Indicators of Compromise (IOCs), TTPs, and threat metadata from external feeds and reports. It integrates into the CyberMoE platform as a domain expert that can be sparsely invoked by ThreatMoE’s gating layer, and whose outputs are fused with other experts (Network, Endpoint, Malware, Identity, Cloud, Vulnerability, OT) for efficient, explainable detection and response.

[See repository docs for full details: ARCHITECTURE.md, THREAT_MODEL.md, EXPERT_MODULES.md, DEV_GUIDE.md]
TXT
)
