---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suricata and Elastic Defend Network Correlation" prebuilt detection rule.
---

# Suricata and Elastic Defend Network Correlation

## Triage and analysis

### Investigating Suricata and Elastic Defend Network Correlation

### Possible investigation steps

- Investigate in the Timeline feature the two events matching this correlation (Suricata and Elastic Defend).
- Review the process details like command_line, privileges, global relevance and reputation.
- Assess the destination.ip reputation and global relevance.
- Review the parent process execution details like command_line, global relevance and reputation.
- Examine all network connection details performed by the process during last 48h.
- Correlate the alert with other security events or logs to identify any patterns or additional indicators of compromise related to the same process or network activity.

### False positive analysis

- Trusted system or third party processes performing network activity that looks like beaconing.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate the suspicious processes and all associated children and parents.
- Implement network-level controls to block traffic to the destination.ip.
- Conduct a thorough review of the system's configuration files to identify unauthorized changes.
- Reset credentials for any accounts associated with the source machine.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.

