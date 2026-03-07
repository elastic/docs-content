---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Active Directory Group Modification by SYSTEM" prebuilt detection rule.'
---

# Active Directory Group Modification by SYSTEM

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Active Directory Group Modification by SYSTEM

Active Directory (AD) is a critical component in Windows environments, managing user and group permissions. SYSTEM, a high-privilege account, can modify AD groups, which attackers exploit to gain unauthorized access. By monitoring specific event logs for SYSTEM-initiated group changes, the detection rule identifies potential privilege escalation, signaling an attacker may have compromised a domain controller.

### Possible investigation steps

- Review the event log entry with event code 4728 to confirm the SYSTEM account (S-1-5-18) initiated the group modification.
- Identify the specific Active Directory group that was modified and determine if it is a sensitive or high-privilege group.
- Check for any recent changes or anomalies in the domain controller's security logs that might indicate SYSTEM privilege escalation.
- Investigate the timeline of events leading up to the group modification to identify any suspicious activities or patterns.
- Correlate this event with other security alerts or logs to assess if there is a broader attack pattern or campaign.
- Verify if there are any known vulnerabilities or misconfigurations in the domain controller that could have been exploited to gain SYSTEM privileges.

### False positive analysis

- Routine administrative tasks performed by automated scripts or scheduled tasks may trigger this rule. Review and document these tasks, then create exceptions for known benign scripts to prevent unnecessary alerts.
- System maintenance activities, such as software updates or system reconfigurations, might involve legitimate group modifications by SYSTEM. Coordinate with IT teams to identify and whitelist these activities.
- Certain security tools or monitoring solutions may perform group modifications as part of their normal operation. Verify these tools' actions and exclude them from triggering alerts if they are confirmed to be safe.
- In environments with custom applications that require SYSTEM-level access for group management, ensure these applications are documented and their actions are excluded from detection to avoid false positives.
- Regularly review and update the list of exceptions to ensure they remain relevant and do not inadvertently allow malicious activities to go undetected.

### Response and remediation

- Immediately isolate the affected domain controller from the network to prevent further unauthorized access or lateral movement by the attacker.
- Revoke any unauthorized group memberships added by the SYSTEM account to prevent privilege escalation and unauthorized access.
- Conduct a thorough review of recent changes in Active Directory, focusing on group modifications and user account activities, to identify any other potential unauthorized changes.
- Reset passwords for all accounts that were added to groups by the SYSTEM account to mitigate the risk of compromised credentials being used.
- Apply security patches and updates to the domain controller to address any vulnerabilities that may have been exploited to gain SYSTEM privileges.
- Monitor for any further suspicious activities or attempts to modify Active Directory groups, using enhanced logging and alerting mechanisms.
- Escalate the incident to the security operations center (SOC) or incident response team for a comprehensive investigation and to determine the full scope of the breach.
