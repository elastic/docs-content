---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Attempt to Disable Gatekeeper" prebuilt detection rule.
---

# Attempt to Disable Gatekeeper

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Attempt to Disable Gatekeeper

Gatekeeper is a macOS security feature that ensures only trusted software runs by verifying app signatures. Adversaries may attempt to disable it to execute unauthorized code, bypassing security checks. The detection rule identifies such attempts by monitoring process events for specific commands used to disable Gatekeeper, flagging potential defense evasion activities.

### Possible investigation steps

- Review the process event details to confirm the presence of the command `spctl --master-disable` in the `process.args` field, which indicates an attempt to disable Gatekeeper.
- Identify the user account associated with the process event to determine if the action was initiated by a legitimate user or an unauthorized actor.
- Check the `event.category` and `event.type` fields to ensure the event is categorized as a process start, which aligns with the rule's detection criteria.
- Investigate the parent process of the flagged event to understand the context in which the Gatekeeper disabling attempt was made, looking for any suspicious or unexpected parent processes.
- Examine recent process events on the same host to identify any subsequent or preceding suspicious activities that might indicate a broader attack or compromise.
- Review system logs and other security alerts on the host for additional indicators of compromise or related malicious activities.
- Assess the risk and impact of the event by considering the host's role, the sensitivity of data it handles, and any potential exposure resulting from the attempted Gatekeeper disablement.

### False positive analysis

- System administrators or IT personnel may intentionally disable Gatekeeper for legitimate software installations or troubleshooting. To manage this, create exceptions for known administrative accounts or specific maintenance windows.
- Some legitimate applications may require Gatekeeper to be disabled temporarily for installation. Identify these applications and whitelist their installation processes to prevent false alerts.
- Development environments on macOS might disable Gatekeeper to test unsigned applications. Consider excluding processes initiated by development tools or specific user accounts associated with development activities.
- Automated scripts or management tools that configure macOS settings might trigger this rule. Review and adjust these scripts to ensure they are recognized as non-threatening, or exclude them from monitoring if they are verified as safe.

### Response and remediation

- Immediately isolate the affected macOS device from the network to prevent potential lateral movement or further execution of unauthorized code.
- Terminate any suspicious processes associated with the attempt to disable Gatekeeper, specifically those involving the 'spctl --master-disable' command.
- Conduct a thorough review of recent system changes and installed applications on the affected device to identify and remove any unauthorized or malicious software.
- Restore Gatekeeper settings to their default state to ensure that only trusted software can be executed on the device.
- Escalate the incident to the security operations team for further analysis and to determine if additional devices or systems may be affected.
- Implement additional monitoring on the affected device and similar systems to detect any further attempts to disable Gatekeeper or other security features.
- Review and update endpoint security policies to enhance protection against similar threats, ensuring that all macOS devices are configured to prevent unauthorized changes to security settings.
