---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "LLM-Based Attack Chain Triage by Host" prebuilt detection rule.'
---

# LLM-Based Attack Chain Triage by Host

## Triage and analysis

### Investigating LLM-Based Attack Chain Triage by Host

Start by reviewing the `Esql.summary` field which contains the LLM's assessment of why these alerts were flagged. The
`Esql.confidence` score (0.7-1.0) indicates the LLM's certainty, scores above 0.9 warrant immediate attention. Focus
on validating the specific indicators mentioned in the summary, such as suspicious domains, download-and-execute 
patterns, unusual process chains, suspicious file operations, DNS queries to malicious domains, or registry modifications.

### Possible investigation steps

- Examine `Esql.process_command_line_values` for suspicious patterns such as encoded commands, download-and-execute sequences,
  or reconnaissance tools.
- Check `Esql.process_parent_command_line_values` to understand process lineage and identify unusual parent-child relationships.
- Review `Esql.file_path_values` for suspicious file drops, DLL side-loading attempts, or persistence mechanisms.
- Analyze `Esql.dns_question_name_values` for connections to suspicious or known-malicious domains.
- Inspect `Esql.registry_path_values` and `Esql.registry_data_strings_values` for persistence or configuration changes.
- Query the alerts index for `host.id` to retrieve the full details of each correlated alert.
- Check if the affected user (`Esql.user_name_values`) has legitimate access and whether the activity aligns with their role.

### False positive analysis

- Security testing frameworks indicate threat emulation testing.
- Software package managers (Homebrew, apt, yum, pip) may trigger discovery alerts during normal updates.
- System initialization or cloud instance bootstrapping (EC2 user-data, cloud-init) may trigger account creation alerts.
- Adversaries aware of LLM-based analysis may attempt to inject testing-related keywords (e.g., Nessus, SCCM references)
  in command lines to influence the model toward FP verdicts. Validate suspicious content regardless of testing indicators.

### Response and remediation

- For high-confidence TP verdicts (>0.9), consider immediate host isolation to contain potential compromise.
- Extract IOCs from command lines (domains, IPs, file hashes, paths) and search across the environment.
- Terminate suspicious processes and remove any dropped files or persistence mechanisms.
- If the attack chain shows lateral movement indicators, expand investigation to connected hosts.
