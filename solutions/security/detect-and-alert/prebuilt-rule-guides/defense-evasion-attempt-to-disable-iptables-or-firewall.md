---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Attempt to Disable IPTables or Firewall" prebuilt detection rule.
---

# Attempt to Disable IPTables or Firewall

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Attempt to Disable IPTables or Firewall

Firewalls like IPTables on Linux systems are crucial for controlling network traffic and protecting against unauthorized access. Adversaries may attempt to disable these firewalls to bypass security measures and facilitate malicious activities. The detection rule identifies suspicious processes that attempt to disable or stop firewall services, such as using commands to flush IPTables rules or halt firewall services, indicating potential defense evasion tactics.

### Possible investigation steps

- Review the process details, including process.name and process.args, to confirm if the command was intended to disable or stop firewall services.
- Check the process.parent.args to understand the context in which the suspicious process was executed, especially if it was triggered by a parent process with arguments like "force-stop".
- Investigate the user account associated with the process execution to determine if it was an authorized user or potentially compromised.
- Examine the host's recent activity logs for any other suspicious behavior or anomalies around the time of the alert, focusing on event.type "start" and event.action "exec" or "exec_event".
- Assess the network traffic logs to identify any unusual inbound or outbound connections that might have occurred after the firewall was disabled or stopped.
- Correlate this event with other alerts or incidents involving the same host or user to identify potential patterns or coordinated attack attempts.

### False positive analysis

- Routine system maintenance or updates may trigger the rule when legitimate processes like systemctl or service are used to stop or restart firewall services. To manage this, create exceptions for known maintenance scripts or scheduled tasks that perform these actions.
- Network troubleshooting activities often involve temporarily disabling firewalls to diagnose connectivity issues. Users can exclude specific user accounts or IP addresses associated with network administrators from triggering the rule during these activities.
- Automated deployment scripts that configure or reconfigure firewall settings might match the rule's criteria. Identify and whitelist these scripts by their process names or execution paths to prevent false positives.
- Security software updates or installations may require temporary firewall adjustments, which could be flagged by the rule. Consider excluding processes associated with trusted security software vendors during update windows.
- Development or testing environments often have different security requirements, leading to frequent firewall changes. Implement environment-specific exceptions to avoid false positives in these contexts.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or potential lateral movement by the adversary.
- Terminate any suspicious processes identified in the alert, such as those attempting to disable or stop firewall services, to halt ongoing malicious activities.
- Review and restore the firewall configurations to their last known good state to ensure that network traffic is properly controlled and unauthorized access is blocked.
- Conduct a thorough examination of the affected system for any signs of compromise or additional malicious activity, focusing on logs and system changes around the time of the alert.
- Escalate the incident to the security operations team for further analysis and to determine if the threat is part of a larger attack campaign.
- Implement additional monitoring and alerting for similar activities across the network to detect and respond to future attempts to disable firewall services promptly.
- Review and update firewall policies and configurations to enhance security measures and prevent similar defense evasion tactics in the future.
