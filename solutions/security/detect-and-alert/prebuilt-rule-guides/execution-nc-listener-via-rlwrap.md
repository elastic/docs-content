---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Netcat Listener Established via rlwrap" prebuilt detection rule.
---

# Netcat Listener Established via rlwrap

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Netcat Listener Established via rlwrap

Netcat, a versatile networking tool, can establish connections for data transfer or remote shell access. When combined with rlwrap, which enhances command-line input, it can create a more stable reverse shell environment. Adversaries exploit this to maintain persistent access. The detection rule identifies such misuse by monitoring rlwrap's execution with netcat-related arguments, signaling potential unauthorized activity.

### Possible investigation steps

- Review the process execution details to confirm the presence of rlwrap with netcat-related arguments by examining the process.name and process.args fields.
- Check the process start time and correlate it with any known scheduled tasks or user activity to determine if the execution was expected or authorized.
- Investigate the source IP address and port used in the netcat connection to identify potential external connections or data exfiltration attempts.
- Analyze the user account associated with the process execution to verify if the account has a history of similar activities or if it has been compromised.
- Examine any related network traffic logs to identify unusual patterns or connections that coincide with the alert, focusing on the host where the process was executed.
- Look for any additional processes spawned by the netcat listener to detect further malicious activity or persistence mechanisms.

### False positive analysis

- Development and testing environments may frequently use rlwrap with netcat for legitimate purposes, such as testing network applications or scripts. To manage this, create exceptions for specific user accounts or IP addresses known to be involved in development activities.
- System administrators might use rlwrap with netcat for troubleshooting or network diagnostics. Identify and exclude these activities by setting up rules that recognize the specific command patterns or user roles associated with administrative tasks.
- Automated scripts or cron jobs that utilize rlwrap and netcat for routine maintenance or monitoring can trigger false positives. Review and whitelist these scripts by their unique process identifiers or command structures to prevent unnecessary alerts.
- Educational or training environments where rlwrap and netcat are used for learning purposes can generate alerts. Implement exceptions based on the environment's network segment or user group to reduce noise from these benign activities.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or data exfiltration.
- Terminate the rlwrap and netcat processes on the affected host to disrupt the reverse shell connection.
- Conduct a forensic analysis of the affected system to identify any additional malicious activities or persistence mechanisms.
- Review and secure any compromised accounts or credentials that may have been used or accessed during the incident.
- Apply security patches and updates to the affected system to mitigate any exploited vulnerabilities.
- Enhance monitoring and logging on the affected host and network to detect similar activities in the future.
- Report the incident to the appropriate internal security team or external authorities if required, following organizational protocols.
