---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Sudo Activity" prebuilt detection rule.
---

# Unusual Sudo Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Sudo Activity

Sudo is a command in Unix-like systems that allows permitted users to execute commands as a superuser, providing necessary privileges for administrative tasks. Adversaries may exploit this by using compromised credentials to gain elevated access, potentially bypassing security controls. The 'Unusual Sudo Activity' detection rule leverages machine learning to identify deviations from normal sudo usage patterns, flagging potential privilege escalation attempts for further investigation.

### Possible investigation steps

- Review the user account associated with the unusual sudo activity to determine if it aligns with known administrative roles or if it is typically associated with non-privileged tasks.
- Check the timestamp of the sudo activity to see if it coincides with any known maintenance windows or reported troubleshooting activities.
- Analyze the command executed with sudo to assess whether it is a common administrative command or if it appears suspicious or unnecessary for the user's role.
- Investigate the source IP address or hostname from which the sudo command was executed to verify if it is a recognized and authorized device.
- Look into recent login activity for the user account to identify any unusual access patterns or locations that could indicate compromised credentials.
- Cross-reference the alert with any other security events or logs around the same time to identify potential indicators of compromise or related malicious activity.

### False positive analysis

- Administrative troubleshooting activities can trigger false positives. Regularly review and document legitimate administrative tasks that require sudo access to differentiate them from potential threats.
- Developers or IT staff performing routine maintenance may cause alerts. Create exceptions for known maintenance windows or specific user accounts that frequently require elevated privileges.
- Automated scripts or scheduled tasks using sudo might be flagged. Identify and whitelist these scripts or tasks if they are verified as safe and necessary for operations.
- New employees or role changes can lead to unusual sudo activity. Update user roles and permissions promptly to reflect their current responsibilities and reduce unnecessary alerts.
- Temporary access granted for specific projects can appear suspicious. Ensure that temporary access is well-documented and set to expire automatically to prevent lingering false positives.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Revoke or reset the compromised credentials to prevent further misuse and ensure that the affected user account is secured.
- Conduct a thorough review of recent sudo logs and system activity to identify any unauthorized changes or actions taken by the adversary.
- Restore any altered or deleted files from backups, ensuring that the system is returned to its last known good state.
- Apply any necessary security patches or updates to the affected system to close vulnerabilities that may have been exploited.
- Enhance monitoring and logging for sudo activities across all systems to detect similar anomalies in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
