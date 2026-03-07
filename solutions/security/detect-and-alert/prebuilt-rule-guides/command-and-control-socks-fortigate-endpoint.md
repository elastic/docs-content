---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "FortiGate SOCKS Traffic from an Unusual Process" prebuilt detection rule.'
---

# FortiGate SOCKS Traffic from an Unusual Process

## Triage and analysis

### Investigating FortiGate SOCKS Traffic from an Unusual Process

### Possible investigation steps

- Review the process details like command_line, privileges, global relevance and reputation.
- Review the parent process execution details like command_line, global relevance and reputation.
- Examine all network connection details performed by the process during last 48h.
- Examine all localhost network connections performed by the same process to verify if there is any port forwarding with another process on the same machine.
- Correlate the alert with other security events or logs to identify any patterns or additional indicators of compromise related to the same process or network activity.

### False positive analysis

- Browser proxy extensions and Add-ons.
- Development and deployment tools.
- Third party trusted tools using SOCKS for network communication.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate the suspicious processes and all associated children and parents.
- Conduct a thorough review of the system's configuration files to identify unauthorized changes.
- Reset credentials for any accounts associated with the source machine.
- Implement network-level controls to block traffic via SOCKS unless authorized.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
