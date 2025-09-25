# Threat Model — MoE-specific risks and mitigations

Scope
Focuses on risks introduced by model composition (gating + experts) and the ThreatIntel Expert’s exposure from external feeds and enrichment pipelines.

Adversary capabilities
- Publish or inject poisoned IOCs in public or shared feeds.
- Probe public interfaces to infer model internals (black-box extraction).
- Influence retraining via mislabeled feedback or data contamination.
- Access telemetry or enrichment outputs (insider or downstream compromise).

Attack enumeration, detection signals, and containment

1) Gating manipulation
- Description: crafted inputs cause the gating net to route to a weak or compromised expert.
- Detection signals: abrupt shifts in gating distribution for specific input classes; rising gating entropy; repeated unusual top-k selections.
- Containment: validate gating pivots with threshold checks; fall back to majority experts; require analyst review for extreme pivots.
- Remediation: quarantine inputs, run offline analysis, retract suspect checkpoint and retrain.

2) Expert poisoning (supply-chain feed poisoning)
- Description: poisoned feed items bias an expert during training or incremental updates.
- Detection signals: sudden parameter drift between checkpoints; increased loss on golden held-out set; anomalous per-expert prediction distributions.
- Containment: enforce feed provenance policies; staged retraining with canary evaluation; block untrusted feeds.
- Remediation: revert to prior checkpoints, run influence analysis to find poisoned samples, adopt robust training strategies.

3) Extraction via fusion probes
- Description: repeated, crafted queries used to infer model behavior or reconstruct training data.
- Detection signals: high-rate probing, low-entropy outputs for diverse inputs, repeated near-identical responses to crafted sequences.
- Containment: authentication + rate-limiting; randomized response noise for unauthenticated users; reduce fidelity of returned enrichment for public endpoints.
- Remediation: throttle clients, rotate models, tighten access control.

4) Membership inference and data leakage
- Description: adversary infers presence of rare IOCs or sensitive records via enrichment responses.
- Detection signals: repeated requests for unique IOCs, correlated external observations tying outputs back to internal data.
- Containment: redact or aggregate sensitive enrichment fields; expose only aggregated evidence to low-privilege contexts.
- Remediation: purge logs, rotate credentials, increase redaction and token gating.

5) Backdoors and hidden triggers
- Description: adversary embeds triggers in data that cause specific expert behavior when activated.
- Detection signals: targeted triggers produce extreme outputs, activation clustering across test cases.
- Containment: routine canary/backdoor tests; hold model updates behind canary acceptance gates.
- Remediation: retrain from clean data, apply targeted pruning and adversarial filtering.

Monitoring & detection
- Maintain per-feed provenance metrics and ingestion signatures.
- Monitor gating/expert distribution drift and checkpoint parameter delta metrics.
- Canary test every proposed checkpoint on golden datasets prior to promotion.
- Produce alerts on abnormal gating entropy, per-expert output drift, and large parameter deltas.

Policies & controls
- Signed feed ingestion and provenance attestations where possible.
- RBAC for feed configuration and enrichment API keys.
- Staged retraining, canary testing, and audit logging for every model change.
