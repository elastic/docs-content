---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Root Network Connection via GDB CAP_SYS_PTRACE" prebuilt detection rule.
---

# Root Network Connection via GDB CAP_SYS_PTRACE

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Root Network Connection via GDB CAP_SYS_PTRACE

GDB, a debugger, can be granted the CAP_SYS_PTRACE capability, allowing it to trace and control processes, a feature often exploited by attackers. By injecting code into root processes, adversaries can execute malicious payloads, such as reverse shells. The detection rule identifies suspicious sequences where GDB is used with this capability, followed by a root-initiated network connection, signaling potential privilege escalation or command and control activities.

### Possible investigation steps

- Review the process execution details to confirm the presence of GDB with CAP_SYS_PTRACE capability by examining the process name, capabilities, and user ID fields in the alert.
- Investigate the network connection attempt by analyzing the process name and user ID fields to determine if the connection was initiated by a root process.
- Check the timeline of events to ensure the sequence of GDB execution followed by a network connection attempt occurred within the specified maxspan of 30 seconds.
- Identify the destination IP address and port of the network connection to assess if it is known for malicious activity or associated with command and control servers.
- Examine the host system for any signs of compromise or unauthorized changes, focusing on processes and files that may have been affected by the potential privilege escalation.
- Correlate the alert with other security events or logs from the same host to identify any additional suspicious activities or patterns that may indicate a broader attack.

### False positive analysis

- Development environments may trigger this rule when developers use GDB with CAP_SYS_PTRACE for legitimate debugging purposes. To mitigate, create exceptions for specific user IDs or processes known to be involved in development activities.
- Automated testing frameworks that utilize GDB for testing applications with root privileges can cause false positives. Identify and exclude these processes or testing environments from the rule.
- System maintenance scripts that require debugging of root processes might inadvertently match the rule criteria. Review and whitelist these scripts or the specific time frames they run to prevent unnecessary alerts.
- Security tools that perform legitimate process tracing as part of their monitoring activities could be mistaken for malicious behavior. Ensure these tools are recognized and excluded from the detection rule.
- Custom administrative scripts that use GDB for process management under root privileges should be documented and excluded to avoid false alarms.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further malicious activity and potential lateral movement.
- Terminate any suspicious processes associated with GDB that have been granted the CAP_SYS_PTRACE capability, especially those initiated by non-root users.
- Conduct a thorough review of the affected system's logs to identify any unauthorized changes or additional malicious activities that may have occurred.
- Reset credentials and review permissions for any accounts that may have been compromised, particularly those with elevated privileges.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Implement network monitoring to detect and block any further unauthorized outbound connections from root processes.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
