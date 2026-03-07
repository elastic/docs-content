---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Persistence via WMI Event Subscription" prebuilt detection rule.
---

# Persistence via WMI Event Subscription

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Persistence via WMI Event Subscription

Windows Management Instrumentation (WMI) is a powerful framework for managing data and operations on Windows systems. Adversaries exploit WMI by creating event subscriptions that trigger malicious code execution, ensuring persistence. The detection rule identifies suspicious use of `wmic.exe` to create event consumers, signaling potential abuse of WMI for persistence by monitoring specific process activities and arguments.

### Possible investigation steps

- Review the process execution details for `wmic.exe` to confirm the presence of suspicious arguments such as "create", "ActiveScriptEventConsumer", or "CommandLineEventConsumer" that indicate potential WMI event subscription abuse.
- Examine the parent process of `wmic.exe` to determine how it was launched and assess whether this aligns with expected behavior or if it suggests malicious activity.
- Investigate the user account associated with the `wmic.exe` process to determine if it has the necessary privileges to create WMI event subscriptions and whether the account activity is consistent with normal operations.
- Check for any recent changes or additions to WMI event filters, consumers, or bindings on the affected system to identify unauthorized modifications that could indicate persistence mechanisms.
- Correlate the alert with other security events or logs from data sources like Microsoft Defender for Endpoint or Sysmon to gather additional context and identify any related suspicious activities or patterns.

### False positive analysis

- Legitimate administrative tasks using wmic.exe may trigger the rule, such as system monitoring or configuration changes. To handle this, identify and document routine administrative scripts and exclude them from triggering alerts.
- Software installations or updates that use WMI for legitimate event subscriptions can be mistaken for malicious activity. Maintain a list of trusted software and their expected behaviors to create exceptions in the detection rule.
- Automated system management tools that rely on WMI for event handling might cause false positives. Review and whitelist these tools by verifying their source and purpose to prevent unnecessary alerts.
- Security software or monitoring solutions that utilize WMI for legitimate purposes can be flagged. Collaborate with IT and security teams to identify these tools and adjust the rule to exclude their known benign activities.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes related to `wmic.exe` that are identified as creating event consumers, specifically those involving "ActiveScriptEventConsumer" or "CommandLineEventConsumer".
- Remove any unauthorized WMI event subscriptions by using tools like `wevtutil` or PowerShell scripts to list and delete suspicious event filters, consumers, and bindings.
- Conduct a thorough review of the system's WMI repository to ensure no other malicious or unauthorized configurations exist.
- Restore the system from a known good backup if the integrity of the system is compromised and cannot be assured through manual remediation.
- Update and patch the system to the latest security standards to mitigate any vulnerabilities that may have been exploited.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
