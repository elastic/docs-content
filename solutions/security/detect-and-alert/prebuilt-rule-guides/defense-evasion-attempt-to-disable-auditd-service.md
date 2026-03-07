---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Attempt to Disable Auditd Service" prebuilt detection rule.'
---

# Attempt to Disable Auditd Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Attempt to Disable Auditd Service

Auditd is a critical Linux service responsible for system auditing and logging, capturing security-relevant events. Adversaries may target this service to evade detection by disabling it, thus preventing the logging of their activities. The detection rule identifies suspicious processes attempting to stop or disable Auditd, such as using commands like `service stop` or `systemctl disable`, signaling potential defense evasion tactics.

### Possible investigation steps

- Review the process details to identify the user account associated with the suspicious command execution, focusing on the process fields such as process.name and process.args.
- Check the system logs for any preceding or subsequent suspicious activities around the time of the alert, particularly looking for other defense evasion tactics or unauthorized access attempts.
- Investigate the command history of the user identified to determine if there are any other unauthorized or suspicious commands executed.
- Verify the current status of the Auditd service on the affected host to ensure it is running and properly configured.
- Correlate the alert with any other security events or alerts from the same host or user to identify potential patterns or broader attack campaigns.

### False positive analysis

- System administrators may intentionally stop or disable the Auditd service during maintenance or troubleshooting. To handle this, create exceptions for known maintenance windows or specific administrator accounts.
- Automated scripts or configuration management tools might stop or disable Auditd as part of routine system updates or deployments. Identify these scripts and whitelist their activities to prevent false alerts.
- Some Linux distributions or custom setups might have alternative methods for managing services that could trigger this rule. Review and adjust the detection criteria to align with the specific service management practices of your environment.
- In environments where Auditd is not used or is replaced by another logging service, the rule might trigger unnecessarily. Consider disabling the rule or adjusting its scope in such cases.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and potential lateral movement by the adversary.
- Terminate any suspicious processes identified in the alert that are attempting to disable the Auditd service to stop the adversary's actions.
- Re-enable and restart the Auditd service on the affected system to ensure that auditing and logging are resumed, capturing any further suspicious activities.
- Conduct a thorough review of the system logs and audit records to identify any unauthorized changes or additional indicators of compromise that may have occurred prior to the alert.
- Apply any necessary security patches or updates to the affected system to address vulnerabilities that may have been exploited by the adversary.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected.
- Implement enhanced monitoring and alerting for similar activities across the network to detect and respond to future attempts to disable critical security services.
