---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Attempt to Disable Syslog Service" prebuilt detection rule.'
---

# Attempt to Disable Syslog Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Attempt to Disable Syslog Service

Syslog is a critical component in Linux environments, responsible for logging system events and activities. Adversaries may target syslog to disable logging, thereby evading detection and obscuring their malicious actions. The detection rule identifies attempts to stop or disable syslog services by monitoring specific process actions and arguments, flagging suspicious commands that could indicate an attempt to impair logging defenses.

### Possible investigation steps

- Review the process details to identify the user account associated with the command execution, focusing on the process.name and process.args fields to determine if the action was legitimate or suspicious.
- Check the system's recent login history and user activity to identify any unauthorized access attempts or anomalies around the time the syslog service was targeted.
- Investigate the parent process of the flagged command to understand the context of its execution and determine if it was initiated by a legitimate application or script.
- Examine other logs and alerts from the same host around the time of the event to identify any correlated suspicious activities or patterns that might indicate a broader attack.
- Assess the system for any signs of compromise, such as unexpected changes in configuration files, unauthorized software installations, or unusual network connections, to determine if the attempt to disable syslog is part of a larger attack.

### False positive analysis

- Routine maintenance activities may trigger this rule, such as scheduled service restarts or system updates. To manage this, create exceptions for known maintenance windows or specific administrative accounts performing these tasks.
- Automated scripts or configuration management tools like Ansible or Puppet might stop or disable syslog services as part of their operations. Identify these scripts and whitelist their execution paths or associated user accounts.
- Testing environments often simulate service disruptions, including syslog, for resilience testing. Exclude these environments from the rule or adjust the rule to ignore specific test-related processes.
- Some legitimate software installations or updates may require stopping syslog services temporarily. Monitor installation logs and exclude these processes if they are verified as non-threatening.
- In environments with multiple syslog implementations, ensure that the rule is not overly broad by refining the process arguments to match only the specific syslog services in use.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and potential lateral movement by the adversary.
- Terminate any suspicious processes identified in the alert, specifically those attempting to stop or disable syslog services, to restore normal logging functionality.
- Restart the syslog service on the affected system to ensure that logging is re-enabled and operational, using commands like `systemctl start syslog` or `service syslog start`.
- Conduct a thorough review of recent logs, if available, to identify any additional suspicious activities or indicators of compromise that may have occurred prior to the syslog service being disabled.
- Escalate the incident to the security operations team for further investigation and to determine if the attack is part of a larger campaign or if other systems are affected.
- Implement additional monitoring on the affected system and similar systems to detect any further attempts to disable logging services, using enhanced logging and alerting mechanisms.
- Review and update access controls and permissions to ensure that only authorized personnel have the ability to modify or stop critical services like syslog, reducing the risk of future incidents.
