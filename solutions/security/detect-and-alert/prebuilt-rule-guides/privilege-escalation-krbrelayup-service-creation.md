---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Service Creation via Local Kerberos Authentication" prebuilt detection rule.
---

# Service Creation via Local Kerberos Authentication

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Service Creation via Local Kerberos Authentication

Kerberos is a network authentication protocol designed to provide strong authentication for client/server applications. In Windows environments, it is often used for secure identity verification. Adversaries may exploit Kerberos by relaying authentication tickets locally to escalate privileges, potentially creating services with elevated rights. The detection rule identifies suspicious local logons using Kerberos, followed by service creation, indicating possible misuse. By monitoring specific logon events and service installations, it helps detect unauthorized privilege escalation attempts.

### Possible investigation steps

- Review the event logs for the specific LogonId identified in the alert to gather details about the logon session, including the user account involved and the time of the logon event.
- Examine the source IP address and port from the logon event to confirm it matches the localhost (127.0.0.1 or ::1) and determine if this aligns with expected behavior for the user or system.
- Investigate the service creation event (event ID 4697) associated with the same LogonId to identify the service name, executable path, and any related command-line arguments to assess if it is legitimate or potentially malicious.
- Check for any recent changes or anomalies in the system or user account, such as modifications to user privileges, group memberships, or recent software installations, that could indicate unauthorized activity.
- Correlate the findings with other security alerts or logs from the same timeframe to identify any patterns or additional indicators of compromise that may suggest a broader attack or compromise.

### False positive analysis

- Routine administrative tasks may trigger the rule if administrators frequently log in locally using Kerberos and create services as part of their duties. To manage this, create exceptions for known administrative accounts or specific service creation activities that are part of regular maintenance.
- Automated scripts or software updates that use Kerberos authentication and subsequently install or update services can also generate false positives. Identify these scripts or update processes and exclude their associated logon IDs from the rule.
- Security software or monitoring tools that perform regular checks and use Kerberos for authentication might inadvertently trigger the rule. Review the behavior of these tools and whitelist their activities if they are verified as non-threatening.
- In environments where localhost is used for testing or development purposes, developers might log in using Kerberos and create services. Consider excluding specific development machines or user accounts from the rule to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or privilege escalation.
- Terminate any suspicious services created during the incident to halt potential malicious activities.
- Conduct a thorough review of the affected system's event logs, focusing on the specific LogonId and service creation events to identify the scope of the compromise.
- Reset the credentials of the compromised user account and any other accounts that may have been accessed using the relayed Kerberos tickets.
- Apply patches and updates to the affected system and any other systems in the network to address known vulnerabilities that could be exploited in similar attacks.
- Implement network segmentation to limit the ability of attackers to move laterally within the network, reducing the risk of privilege escalation.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to ensure comprehensive remediation efforts are undertaken.
