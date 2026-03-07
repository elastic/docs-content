---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Privilege Escalation via GDB CAP_SYS_PTRACE" prebuilt detection rule.'
---

# Privilege Escalation via GDB CAP_SYS_PTRACE

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Privilege Escalation via GDB CAP_SYS_PTRACE

The CAP_SYS_PTRACE capability in Linux allows processes to trace and control other processes, a feature primarily used for debugging. Adversaries can exploit this by using GDB with this capability to inject code into processes running as root, thereby escalating privileges. The detection rule identifies such abuse by monitoring sequences where GDB is executed with CAP_SYS_PTRACE, followed by a process running as root, indicating potential privilege escalation.

### Possible investigation steps

- Review the alert details to identify the specific host and process entity ID where the GDB execution with CAP_SYS_PTRACE was detected.
- Examine the process tree on the affected host to determine the parent process of GDB and any child processes it may have spawned, focusing on any processes running as root.
- Check the user account associated with the GDB execution to verify if it is a legitimate user and assess if there are any indications of compromise or misuse.
- Investigate the timeline of events around the alert to identify any preceding or subsequent suspicious activities, such as unauthorized access attempts or changes in user privileges.
- Analyze system logs and audit records for any signs of unauthorized access or privilege escalation attempts, particularly focusing on the time window specified by the maxspan of 1 minute in the query.
- Correlate the findings with other security alerts or incidents on the same host to determine if this event is part of a larger attack campaign.

### False positive analysis

- Development environments where GDB is frequently used for legitimate debugging purposes may trigger false positives. To mitigate this, consider excluding specific user accounts or processes that are known to use GDB regularly for debugging.
- Automated testing systems that utilize GDB for testing applications with elevated privileges might be flagged. Implement exceptions for these systems by identifying and excluding their specific process names or user IDs.
- Security tools or monitoring solutions that use GDB with CAP_SYS_PTRACE for legitimate monitoring or analysis tasks can cause false alerts. Review and whitelist these tools by their process names or associated user accounts.
- System administrators or developers who have legitimate reasons to use GDB with elevated capabilities should be identified, and their activities should be excluded from the rule to prevent unnecessary alerts.
- Scheduled maintenance scripts that involve GDB for system diagnostics or performance tuning may be misinterpreted as malicious. Exclude these scripts by their execution schedule or specific identifiers.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious processes identified as running with elevated privileges, especially those involving GDB with CAP_SYS_PTRACE.
- Revoke CAP_SYS_PTRACE capability from non-essential users and processes to limit potential abuse.
- Conduct a thorough review of user accounts and permissions on the affected system to ensure no unauthorized privilege escalations have occurred.
- Restore the affected system from a known good backup if any unauthorized changes or code injections are detected.
- Monitor the affected and related systems for any signs of persistence mechanisms or further malicious activity.
- Report the incident to the appropriate internal security team or authority for further investigation and potential escalation if necessary.
