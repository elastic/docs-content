---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Linux System Information Discovery Activity" prebuilt detection rule.
---

# Unusual Linux System Information Discovery Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Linux System Information Discovery Activity

In Linux environments, system information discovery involves commands that reveal details about system configuration and software versions. While typically used for legitimate troubleshooting, adversaries exploit this to gather intelligence for further attacks, such as privilege escalation. The detection rule leverages machine learning to identify atypical usage patterns, flagging potential misuse by compromised accounts.

### Possible investigation steps

- Review the alert details to identify the specific user account and the command executed that triggered the alert. Focus on any unusual or unexpected user context.
- Check the user's activity history to determine if this type of command execution is typical for the user or if it deviates from their normal behavior.
- Investigate the source IP address and hostname associated with the alert to verify if they are consistent with the user's usual access patterns or if they indicate potential unauthorized access.
- Examine system logs for any additional suspicious activities or anomalies around the time of the alert, such as failed login attempts or other unusual commands executed.
- Assess whether the command executed could be part of a legitimate troubleshooting process or if it aligns with known tactics for privilege escalation or persistence.
- If the account is suspected to be compromised, consider resetting the user's credentials and conducting a broader investigation into potential lateral movement or data exfiltration activities.

### False positive analysis

- Routine administrative tasks by system administrators may trigger alerts. To manage this, create exceptions for known admin accounts performing regular maintenance.
- Automated scripts for system monitoring or inventory management can be flagged. Identify and whitelist these scripts to prevent unnecessary alerts.
- Scheduled jobs or cron tasks that gather system information for legitimate purposes might be detected. Review and exclude these tasks from the rule to reduce false positives.
- Development or testing environments where frequent system information queries are normal can cause alerts. Consider excluding these environments from monitoring or adjusting the sensitivity of the rule for these contexts.
- Security tools that perform regular system scans may be misidentified. Ensure these tools are recognized and excluded from triggering the rule.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified as part of the unusual system information discovery activity.
- Review and reset credentials for the potentially compromised account to prevent further misuse.
- Conduct a thorough examination of system logs and command history to identify any additional malicious activities or indicators of compromise.
- Apply security patches and updates to the affected system to mitigate any known vulnerabilities that could be exploited for privilege escalation.
- Implement enhanced monitoring on the affected system and similar environments to detect any recurrence of unusual system information discovery activities.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
