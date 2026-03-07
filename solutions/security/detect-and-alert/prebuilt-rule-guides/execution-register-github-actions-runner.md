---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Remote GitHub Actions Runner Registration" prebuilt detection rule.'
---

# Remote GitHub Actions Runner Registration

## Triage and analysis

### Investigating Remote GitHub Actions Runner Registration

Unexpected or unauthorized Github actions runner registration may indicate adversarial activity aimed at establishing remote code execution via malicious GitHub workflows.

### Possible investigation steps

- Review the remote repository details and reputation.
- Examine the remote repository for any suspicious workflows run commands in the `.github/workflows` folder.
- Examine the execution context like process tree, associated network and file activities.
- Verify if there is adjascent any sensitive file access or collection.
- Correlate with other alerts and investiguate if this activity is related to a supply chain attack.

### False positive analysis

- Authorized configuration changes.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized command execution and potential lateral movement.
- Terminate any suspicious child processes that were initiated by the registered Github actions runner.
- Conduct a thorough review of the affected system's logs and configurations to identify any unauthorized changes or additional indicators of compromise.
- Restore the system from a known good backup if any unauthorized changes or malicious activities are confirmed.
- Implement application whitelisting to prevent unauthorized execution.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on the broader network.
