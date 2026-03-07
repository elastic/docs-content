---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Discovery Signal Alert with Unusual Process Executable" prebuilt detection rule.'
---

# Unusual Discovery Signal Alert with Unusual Process Executable

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Discovery Signal Alert with Unusual Process Executable

In Windows environments, discovery activities often involve querying system information, which adversaries exploit to gather intelligence for further attacks. They may use uncommon processes to evade detection. This detection rule identifies anomalies by flagging signals with rare host, user, and process combinations, indicating potential misuse of discovery tactics.

### Possible investigation steps

- Review the alert details to identify the specific host.id, user.id, and process.executable involved in the alert to understand the context of the unusual activity.
- Check the historical activity of the identified host.id and user.id to determine if this combination has been seen before and assess if the behavior is truly anomalous.
- Investigate the process.executable to verify its legitimacy, including checking its file path, digital signature, and any known associations with legitimate or malicious software.
- Correlate the alert with other security events or logs from the same host or user to identify any additional suspicious activities or patterns that may indicate a broader threat.
- Consult threat intelligence sources to determine if the process.executable or any related indicators are associated with known threat actors or campaigns.
- Assess the potential impact and risk of the activity by considering the host's role within the network and the user's access level to sensitive data or systems.

### False positive analysis

- Routine administrative tasks may trigger alerts if they involve uncommon processes. Identify these tasks and create exceptions for known benign activities to prevent unnecessary alerts.
- Software updates or installations can generate unusual process executions. Monitor and document these events, and exclude them from alerts if they are verified as legitimate.
- Custom scripts or tools used by IT staff for system management might be flagged. Review these scripts and whitelist them if they are part of regular operations.
- Automated processes or scheduled tasks that run under specific user accounts may appear suspicious. Verify these tasks and exclude them if they are part of normal system behavior.
- Third-party security or monitoring tools might use unique processes for legitimate discovery activities. Validate these tools and add them to the exception list to avoid false positives.

### Response and remediation

- Isolate the affected host immediately to prevent further lateral movement or data exfiltration. Disconnect it from the network while maintaining power to preserve volatile data for forensic analysis.
- Terminate the unusual process executable identified in the alert to halt any ongoing malicious activity. Use task management tools or scripts to ensure the process is stopped.
- Conduct a thorough review of the user account associated with the alert. Reset the account credentials and enforce multi-factor authentication to prevent unauthorized access.
- Analyze the process executable and its origin. Check for any associated files or scripts that may have been dropped on the system and remove them.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the threat is part of a larger attack campaign.
- Implement additional monitoring on the affected host and user account to detect any further suspicious activities. Use enhanced logging and alerting to capture detailed information.
- Review and update endpoint protection policies to block similar unusual processes in the future, ensuring that the security tools are configured to detect and respond to such anomalies.
