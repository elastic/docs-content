---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Execution via GitHub Actions Runner" prebuilt detection rule.
---

# Execution via GitHub Actions Runner

## Triage and analysis

### Investigating Execution via GitHub Actions Runner

Adversaries who gain the ability to modify or trigger workflows in a linked GitHub repository can execute arbitrary commands on the runner host.

### Possible investigation steps

- Review the execution details like process.command_line and if it's expected or not.
- Examine associated network and file activities and if there is any ingress tool transfer activity.
- Verify if there is adjascent any sensitive file access or collection.
- Correlate with other alerts and investiguate if this activity is related to a supply chain attack.

### False positive analysis

- Authorized github workflow actions.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized command execution and potential lateral movement.
- Terminate any suspicious child processes that were initiated by the Github actions runner.
- Conduct a thorough review of the affected system's logs and configurations to identify any unauthorized changes or additional indicators of compromise.
- Restore the system from a known good backup if any unauthorized changes or malicious activities are confirmed.
- Implement application whitelisting to prevent unauthorized execution.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on the broader network.
