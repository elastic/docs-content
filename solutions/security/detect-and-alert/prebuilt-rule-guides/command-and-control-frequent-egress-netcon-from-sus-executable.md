---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "High Number of Egress Network Connections from Unusual Executable" prebuilt detection rule.'
---

# High Number of Egress Network Connections from Unusual Executable

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating High Number of Egress Network Connections from Unusual Executable

In Linux environments, executables can initiate network connections for legitimate purposes. However, adversaries exploit this by deploying malware in temporary directories to establish command and control (C2) channels. The detection rule identifies unusual executables making numerous outbound connections, excluding trusted IP ranges and known benign paths, to flag potential threats.

### Possible investigation steps

- Review the process.executable field to identify the specific executable making the connections and determine if it is known or expected in the environment.
- Examine the destination.ip field to identify the external IP addresses the executable is attempting to connect to and check if they are known malicious or suspicious.
- Check the host.os.type and agent.id fields to identify the specific host and agent involved, and gather additional context about the system's role and recent activity.
- Analyze the @timestamp field to correlate the timing of the connections with other events or activities on the network or host.
- Cross-reference the identified executable and IP addresses with threat intelligence sources to determine if they are associated with known threats or campaigns.
- If the executable is determined to be malicious or suspicious, isolate the affected host and perform a deeper forensic analysis to identify any additional indicators of compromise or lateral movement.

### False positive analysis

- Executables in temporary directories used by legitimate applications or scripts can trigger alerts. Review the process name and executable path to determine if they are associated with known applications or scripts.
- Automated scripts or cron jobs that perform network operations might be flagged. Identify these scripts and consider excluding their paths from the rule if they are verified as non-malicious.
- Development or testing environments often use temporary directories for network operations. If these environments are known and trusted, add their specific paths to the exclusion list.
- Backup or synchronization tools that use temporary directories for data transfer can generate numerous connections. Verify these tools and exclude their paths if they are confirmed to be safe.
- Security tools or monitoring agents that operate in temporary directories might be mistakenly flagged. Confirm their legitimacy and exclude their paths to prevent false positives.

### Response and remediation

- Isolate the affected host immediately from the network to prevent further potential malicious communication and lateral movement.
- Terminate the suspicious process identified by the alert to stop any ongoing malicious activity.
- Conduct a forensic analysis of the affected system to identify any additional indicators of compromise (IOCs) and assess the extent of the infection.
- Remove any malicious executables or files found in temporary directories such as /tmp, /var/tmp, or /dev/shm to eliminate the threat.
- Patch and update the affected system to the latest security standards to close any vulnerabilities that may have been exploited.
- Monitor network traffic for any unusual outbound connections from other systems to detect potential spread or similar threats.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to ensure comprehensive remediation.
