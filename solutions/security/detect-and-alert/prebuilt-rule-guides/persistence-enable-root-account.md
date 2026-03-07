---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Attempt to Enable the Root Account" prebuilt detection rule.
---

# Attempt to Enable the Root Account

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Attempt to Enable the Root Account

In macOS environments, the root account is typically disabled to enhance security. However, adversaries may attempt to enable it using the `dsenableroot` command to gain persistent, elevated access. The detection rule identifies such attempts by monitoring process events for the execution of `dsenableroot` without the disable flag, indicating potential misuse for persistence.

### Possible investigation steps

- Review the process event logs to confirm the execution of the dsenableroot command without the disable flag, as indicated by the absence of process.args:"-d".
- Identify the user account associated with the process event to determine if the action was initiated by a legitimate user or a potential adversary.
- Check for any recent changes in user account permissions or configurations that might indicate unauthorized access or privilege escalation.
- Investigate any other suspicious activities or process executions around the same time as the dsenableroot command to identify potential lateral movement or further persistence mechanisms.
- Correlate the event with other security alerts or logs from the same host to assess if this is part of a broader attack campaign.

### False positive analysis

- System administrators may legitimately enable the root account for maintenance or troubleshooting. To handle this, create exceptions for known administrator accounts or specific maintenance windows.
- Automated scripts or management tools might use the dsenableroot command as part of their operations. Identify these tools and exclude their process signatures from triggering alerts.
- Educational or testing environments may require enabling the root account for instructional purposes. Implement exclusions for these environments by tagging relevant systems or user accounts.
- Ensure that any exclusion rules are regularly reviewed and updated to reflect changes in administrative practices or tool usage to maintain security integrity.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent any potential lateral movement by the adversary.
- Terminate any unauthorized processes associated with the `dsenableroot` command to halt further misuse of elevated privileges.
- Review system logs and user activity to identify any unauthorized changes or access that occurred after the root account was enabled.
- Reset the root account password and disable the root account to prevent further unauthorized access.
- Conduct a thorough scan of the system for any additional signs of compromise or persistence mechanisms that may have been installed.
- Notify the security team and relevant stakeholders about the incident for awareness and further investigation.
- Implement additional monitoring and alerting for any future attempts to enable the root account, ensuring rapid detection and response.
