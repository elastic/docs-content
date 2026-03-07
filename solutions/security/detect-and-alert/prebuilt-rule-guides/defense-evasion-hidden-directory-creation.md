---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Hidden Directory Creation via Unusual Parent" prebuilt detection rule.
---

# Hidden Directory Creation via Unusual Parent

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Hidden Directory Creation via Unusual Parent

In Linux environments, hidden directories, often prefixed with a dot, are typically used for configuration files but can be exploited by attackers to conceal malicious activities. Adversaries may create these directories using unexpected parent processes in sensitive locations. The detection rule identifies such anomalies by monitoring directory creation commands executed by unusual parent executables, focusing on specific directories and excluding known benign patterns.

### Possible investigation steps

- Review the process.parent.executable field to identify the parent process that initiated the directory creation and assess its legitimacy based on its typical behavior and location.
- Examine the process.args field to understand the specific arguments used with the mkdir command, focusing on the directory path and any patterns that may indicate malicious intent.
- Check the process.command_line field for any unusual or suspicious command-line patterns that might suggest an attempt to evade detection.
- Investigate the context of the parent process by reviewing recent activities or logs associated with it, especially if it originates from sensitive directories like /dev/shm, /tmp, or /var/tmp.
- Correlate the alert with other security events or logs from the same host to identify any related suspicious activities or patterns that could indicate a broader attack or compromise.
- Consult threat intelligence sources or databases to determine if the parent executable or directory path has been associated with known malicious activities or threat actors.

### False positive analysis

- Temporary directories used by legitimate applications can trigger false positives. Exclude known benign parent executables like those in "/tmp/newroot/*" or "/run/containerd/*" to reduce noise.
- Automated build processes may create hidden directories during software compilation. Add exceptions for parent executables such as "/var/tmp/buildah*" or "/tmp/python-build.*" to prevent unnecessary alerts.
- Development tools and scripts might create hidden directories for caching or temporary storage. Consider excluding parent executables like "/tmp/pear/temp/*" or "/tmp/cliphist-wofi-img" if they are part of regular development activities.
- Ensure that the command line patterns like "mkdir -p ." or "mkdir ./*" are excluded, as these are common in scripts and do not typically indicate malicious intent.
- Regularly review and update the list of excluded patterns and parent executables to align with changes in the environment and reduce false positives effectively.

### Response and remediation

- Isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes associated with the unusual parent executable identified in the alert to halt potential malicious operations.
- Conduct a thorough review of the hidden directory and its contents to identify and remove any malicious files or tools.
- Restore any affected files or configurations from a known good backup to ensure system integrity.
- Implement stricter access controls and monitoring on sensitive directories to prevent unauthorized directory creation.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are compromised.
- Update and enhance endpoint detection and response (EDR) solutions to improve detection capabilities for similar threats in the future.
