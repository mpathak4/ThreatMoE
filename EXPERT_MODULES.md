# Expert Modules — Reference

Network Expert
- Domain: NetFlow, pcap, network metadata
- Tasks: anomaly detection, protocol fingerprinting, lateral movement detection
- Outputs: flow_scores, suspect_sessions, top_contributing_flows

Endpoint Expert
- Domain: EDR events, process telemetry
- Tasks: process anomaly detection, persistence & autorun discovery, credential misuse detection
- Outputs: process_alerts, suspicious_binaries, remediation_suggested

Malware Expert
- Domain: binary samples, static/dynamic traces
- Tasks: family classification, unpacking feature extraction, YARA matches
- Outputs: family_label, behavioral_tags, associated_IOCs

Email/Phishing Expert
- Domain: headers, body text, URLs, attachments
- Tasks: phishing detection, URL reputation scoring, attachment analysis
- Outputs: phish_score, url_reputation, verdict, matched_signatures

Vulnerability Expert
- Domain: CVE feeds, package metadata, SBOMs
- Tasks: vulnerability risk scoring, exploit likelihood estimation, patch prioritization
- Outputs: vuln_score, remediation_priority, affected_assets

ThreatIntel Expert
- Domain: IOC feeds, reports, TTP mappings
- Tasks: normalization, enrichment, actor attribution, IOC correlation
- Outputs: enrichment_blob, actor_score, correlation_cluster, recommended_action

Identity Expert
- Domain: AD, SSO logs, session telemetry
- Tasks: anomalous access detection, suspicious privilege escalations
- Outputs: identity_risk_score, session_flags, recommended_review

Cloud Expert
- Domain: CloudTrail, Kubernetes events, container telemetry
- Tasks: misconfiguration detection, lateral cloud movement detection
- Outputs: cloud_risk, suspicious_api_calls, remediation_steps

Infra/OT Expert
- Domain: ICS/PLC telemetry, command logs
- Tasks: command anomaly detection, safety impact scoring
- Outputs: safety_score, command_anomaly_flags, emergency_actions
