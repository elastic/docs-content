---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Admin Group Account Addition" prebuilt detection rule.
---

# Potential Admin Group Account Addition

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Admin Group Account Addition

In macOS environments, tools like `dscl` and `dseditgroup` manage user group memberships, including admin groups. Adversaries may exploit these tools to escalate privileges by adding accounts to admin groups, gaining unauthorized access. The detection rule identifies such attempts by monitoring process activities related to these tools, excluding legitimate management services, to flag potential privilege escalation.

### Possible investigation steps

- Review the process details to confirm the use of `dscl` or `dseditgroup` with arguments indicating an attempt to add an account to the admin group, such as "/Groups/admin" and "-a" or "-append".
- Check the process's parent executable path to ensure it is not one of the legitimate management services excluded in the query, such as JamfDaemon, JamfManagementService, jumpcloud-agent, or Addigy go-agent.
- Investigate the user account associated with the process to determine if it has a history of legitimate administrative actions or if it appears suspicious.
- Examine recent login events and user activity on the host to identify any unusual patterns or unauthorized access attempts.
- Correlate the alert with other security events or logs from the same host to identify any related suspicious activities or potential indicators of compromise.
- Assess the risk and impact of the account addition by determining if the account has been successfully added to the admin group and if any unauthorized changes have been made.

### False positive analysis

- Legitimate management services like JAMF and JumpCloud may trigger false positives when they manage user group memberships. These services are already excluded in the rule, but ensure any additional management tools used in your environment are similarly excluded.
- Automated scripts or maintenance tasks that require temporary admin access might be flagged. Review these scripts and consider adding them to the exclusion list if they are verified as safe.
- System updates or software installations that modify group memberships could be misidentified. Monitor these activities and adjust the rule to exclude known update processes if they are consistently flagged.
- User-initiated actions that are part of normal IT operations, such as adding a new admin for legitimate purposes, may appear as false positives. Ensure that such actions are documented and communicated to avoid unnecessary alerts.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or privilege escalation.
- Review the process execution logs to confirm unauthorized use of `dscl` or `dseditgroup` for adding accounts to the admin group, ensuring the activity is not part of legitimate administrative tasks.
- Remove any unauthorized accounts from the admin group to restore proper access controls and prevent further misuse of elevated privileges.
- Conduct a thorough review of all admin group memberships on the affected system to ensure no other unauthorized accounts have been added.
- Reset passwords for any accounts that were added to the admin group without authorization to prevent further unauthorized access.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and alerting for similar activities across the network to detect and respond to future privilege escalation attempts promptly.
