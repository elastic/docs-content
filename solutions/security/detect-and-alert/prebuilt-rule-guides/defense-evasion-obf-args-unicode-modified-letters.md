---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Command Obfuscation via Unicode Modifier Letters" prebuilt detection rule.
---

# Command Obfuscation via Unicode Modifier Letters

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Command Obfuscation via Unicode Modifier Letters

Adversaries sometimes replace ASCII characters with visually similar Unicode modifier letters or combining marks to evade simple string-based detections.

### Possible investigation steps

- Review the process execution details (command_line, parent, code signature, hash).
- Analyze the full execution process tree to identify the root cause.
- Check the creation of any persistence using scheduled tasks, Run key, services, shortcuts or startup folders.
- Cross-reference with other logs or alerts to identify any related incidents or patterns of activity that might indicate a larger threat campaign.

### False positive analysis

- Legitimate internationalized applications and installers use Unicode (e.g., localized product names, non-Latin scripts).
- Dev tools or fonts may create commands with combining marks (rare) — check installer/tool provenance.
- Command lines that include user input, file names, or paths with non-ASCII characters (e.g., user folders) can trigger the rule.

### Response and remediation

- Isolate the host if there are signs of active compromise (outbound C2, credential theft, lateral movement).
- Terminate the suspicious process and any direct descendants after collecting forensic evidence (memory, artifacts).
- Collect EDR snapshots, full disk image or targeted file copies, registry hives, and network logs for investigation.
- Remove any persistence entries (scheduled task, startup, services) tied to the activity.
- Qurantine and submit samples to malware analysis; if confirmed malicious, remove and restore from known good backups.
- Block and update indicators related to this activity (hashes, exact normalized command patterns, codepoint sequences, IPs/domains).
- Run global hutning queries for same Unicode patterns, normalized variants, and identical parent/child process chains.

