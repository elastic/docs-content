---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "New GitHub Self Hosted Action Runner" prebuilt detection rule.
---

# New GitHub Self Hosted Action Runner

## Triage and analysis

### Investigating New GitHub Self Hosted Action Runner

Adversaries who gain the ability to modify or trigger workflows in a linked GitHub repository can execute arbitrary commands on the runner host.

### Possible investigation steps

- Validate the user is authoried to perform this change
- Review the purpose of the self-hosted action runner and what actions will be executed.
- Verify if there is any adjascent  sensitive file access or collection.
- Correlate with other alerts and investiguate if this activity is related to a supply chain attack.

### False positive analysis

- Authorized github self-hosted actions runner.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized command execution and potential lateral movement.
- Terminate any suspicious child processes that were initiated by the Github actions runner.
- Conduct a thorough review of the affected system's logs and configurations to identify any unauthorized changes or additional indicators of compromise.
- Restore the system from a known good backup if any unauthorized changes or malicious activities are confirmed.
- Implement application whitelisting to prevent unauthorized execution.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on the broader network.
