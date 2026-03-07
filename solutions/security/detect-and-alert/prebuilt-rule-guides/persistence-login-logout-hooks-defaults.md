---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Persistence via Login or Logout Hook" prebuilt detection rule.'
---

# Persistence via Login or Logout Hook

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Persistence via Login or Logout Hook

In macOS environments, login and logout hooks are scripts executed automatically during user login or logout, often used for system management tasks. Adversaries exploit this by inserting malicious scripts to maintain persistence. The detection rule identifies suspicious use of the `defaults` command to set these hooks, excluding known legitimate scripts, thus highlighting potential unauthorized persistence attempts.

### Possible investigation steps

- Review the process execution details to confirm the use of the "defaults" command with "write" arguments targeting "LoginHook" or "LogoutHook".
- Check the process execution history for the user account associated with the alert to identify any unusual or unauthorized activity.
- Investigate the source and content of the script specified in the "defaults" command to determine if it contains malicious or unauthorized code.
- Cross-reference the script path against known legitimate scripts to ensure it is not mistakenly flagged.
- Analyze recent system changes or installations that might have introduced the suspicious script or process.
- Review system logs around the time of the alert for any additional indicators of compromise or related suspicious activity.

### False positive analysis

- Known false positives include legitimate scripts used by system management tools like JAMF, which are often set as login or logout hooks.
- To handle these, users can create exceptions for known legitimate scripts by adding their paths to the exclusion list in the detection rule.
- Regularly review and update the exclusion list to ensure it includes all authorized scripts used in your environment.
- Monitor for any changes in the behavior of these scripts to ensure they remain non-threatening and authorized.
- Collaborate with IT and security teams to identify any new legitimate scripts that should be excluded from detection.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential lateral movement or data exfiltration by the adversary.
- Terminate any suspicious processes associated with the unauthorized login or logout hooks to halt any ongoing malicious activity.
- Remove the unauthorized login or logout hooks by using the `defaults delete` command to ensure the persistence mechanism is dismantled.
- Conduct a thorough review of system logs and recent changes to identify any additional unauthorized modifications or indicators of compromise.
- Restore any affected system files or configurations from a known good backup to ensure system integrity and functionality.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems are affected.
- Implement enhanced monitoring and alerting for similar unauthorized use of the `defaults` command to improve detection and response capabilities.
