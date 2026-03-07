---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Outbound Network Connection via Unsigned Binary" prebuilt detection rule.'
---

# Suspicious Outbound Network Connection via Unsigned Binary

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Outbound Network Connection via Unsigned Binary

Unsigned or untrusted binaries making outbound network connections to raw IP addresses on non-standard ports is a significant indicator of malware activity. Legitimate macOS applications are typically code-signed by Apple or identified developers, while malware often lacks valid signatures. This detection rule identifies this suspicious combination of unsigned binaries with network activity to detect potential command and control communication or data exfiltration attempts.

### Possible investigation steps

- Review the process.executable and process.hash fields to identify the unsigned binary and search for its hash in threat intelligence databases and malware repositories.
- Examine the process.code_signature fields to understand why the binary is untrusted, including whether it lacks a signature entirely or has an invalid or revoked certificate.
- Analyze the destination.ip and destination.port fields to identify the remote endpoint and research it in threat intelligence sources for known malicious infrastructure.
- Investigate the process.parent.executable and process.command_line to understand how the unsigned binary was launched and trace the execution chain to the initial access vector.
- Review file.creation and file.modification events to determine when and how the unsigned binary was placed on the system.
- Check for persistence mechanisms that may have been created by or for the unsigned binary, such as LaunchAgents, LaunchDaemons, or cron jobs.
- Correlate with other network events from the same host to identify patterns of C2 communication or additional indicators of compromise.

### False positive analysis

- Custom internal tools developed in-house may be unsigned and require network access for legitimate business purposes. Verify with development teams and consider adding specific exclusions.
- Development builds and testing environments may use unsigned binaries during the software development lifecycle. Document these activities and create targeted exceptions.
- Open-source utilities compiled locally may not have code signatures. Evaluate these on a case-by-case basis and add to exclusion lists if verified safe.
- Homebrew and other package manager binaries are already excluded but verify that legitimate tools from these sources are not being flagged.

### Response and remediation

- Immediately terminate the unsigned process and block the destination IP address at network perimeters and endpoint firewalls.
- Quarantine the unsigned binary for forensic analysis and malware reverse engineering.
- Conduct a comprehensive scan of the affected system to identify additional malware components, persistence mechanisms, or lateral movement indicators.
- Investigate how the unsigned binary was delivered to the system and remediate the initial access vector.
- Review other systems in the environment for the same binary hash or similar indicators of compromise.
- Implement application allowlisting policies to prevent unauthorized unsigned binaries from executing.
- Escalate to the incident response team for further investigation if the binary is confirmed malicious.
