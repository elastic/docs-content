---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Enumeration via Active Directory Web Service" prebuilt detection rule.
---

# Potential Enumeration via Active Directory Web Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Enumeration via Active Directory Web Service

Active Directory Web Service (ADWS) facilitates querying Active Directory (AD) over a network, providing a web-based interface for directory services. Adversaries may exploit ADWS to enumerate network resources and user accounts, gaining insights into the environment. The detection rule identifies suspicious activity by monitoring processes that load AD-related modules and establish network connections to the ADWS port, indicating potential unauthorized enumeration attempts.

### Possible investigation steps

- Review the process entity ID to identify the specific process that triggered the alert and gather details such as the process name, executable path, and user context.
- Examine the user ID associated with the process to determine if it belongs to a legitimate user or service account, and verify if the user has a history of accessing Active Directory resources.
- Investigate the network connection details, focusing on the destination IP address and port 9389, to identify the target server and assess if it is a legitimate Active Directory Web Service endpoint.
- Check for any recent changes or unusual activity on the host machine, such as new software installations or configuration changes, that could explain the loading of Active Directory-related modules.
- Correlate the alert with other security events or logs from the same timeframe to identify any patterns or additional suspicious activities that might indicate a broader attack or reconnaissance effort.

### False positive analysis

- Legitimate administrative tools or scripts may load Active Directory-related modules and connect to the ADWS port. To handle this, create exceptions for known administrative processes that regularly perform these actions.
- Scheduled tasks or automated scripts running under service accounts might trigger the rule. Identify these tasks and exclude their associated user IDs or process paths from the detection rule.
- Security or monitoring software that queries Active Directory for legitimate purposes can cause false positives. Review and whitelist these applications by adding their executable paths to the exclusion list.
- Development or testing environments where developers frequently interact with Active Directory services may generate alerts. Consider excluding specific user IDs or process paths associated with these environments to reduce noise.
- Ensure that any exceptions or exclusions are regularly reviewed and updated to reflect changes in the environment or administrative practices.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified in the alert that are loading Active Directory-related modules and making network connections to the ADWS port.
- Conduct a thorough review of the affected system's user accounts and permissions to identify any unauthorized changes or access.
- Reset credentials for any accounts that were potentially compromised or used in the suspicious activity.
- Implement network segmentation to limit access to the ADWS port (9389) to only trusted systems and users.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Update and enhance monitoring rules to detect similar enumeration attempts in the future, focusing on unusual process behavior and network connections to critical services.
