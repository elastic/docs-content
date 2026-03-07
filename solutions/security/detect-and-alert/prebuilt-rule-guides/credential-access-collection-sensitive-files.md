---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Sensitive Files Compression" prebuilt detection rule.
---

# Sensitive Files Compression

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Sensitive Files Compression

Compression utilities like zip, tar, and gzip are essential for efficiently managing and transferring files. However, adversaries can exploit these tools to compress and exfiltrate sensitive data, such as SSH keys and configuration files. The detection rule identifies suspicious compression activities by monitoring process executions involving these utilities and targeting known sensitive file paths, thereby flagging potential data collection and credential access attempts.

### Possible investigation steps

- Review the process execution details to identify the user account associated with the compression activity, focusing on the process.name and process.args fields.
- Examine the command line arguments (process.args) to determine which specific sensitive files were targeted for compression.
- Check the event.timestamp to establish a timeline and correlate with other potentially suspicious activities on the host.
- Investigate the host's recent login history and user activity to identify any unauthorized access attempts or anomalies.
- Analyze network logs for any outbound connections from the host around the time of the event to detect potential data exfiltration attempts.
- Assess the integrity and permissions of the sensitive files involved to determine if they have been altered or accessed inappropriately.

### False positive analysis

- Routine system backups or administrative tasks may trigger the rule if they involve compressing sensitive files for legitimate purposes. Users can create exceptions for known backup scripts or administrative processes by excluding specific process names or command-line arguments associated with these tasks.
- Developers or system administrators might compress configuration files during development or deployment processes. To handle this, users can whitelist specific user accounts or directories commonly used for development activities, ensuring these actions are not flagged as suspicious.
- Automated scripts or cron jobs that regularly archive logs or configuration files could be mistakenly identified as threats. Users should review and exclude these scheduled tasks by identifying their unique process identifiers or execution patterns.
- Security tools or monitoring solutions that periodically compress and transfer logs for analysis might be misinterpreted as malicious. Users can exclude these tools by specifying their process names or paths in the detection rule exceptions.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further data exfiltration and unauthorized access.
- Terminate any suspicious processes identified by the detection rule to halt ongoing compression and potential data exfiltration activities.
- Conduct a thorough review of the compressed files and their contents to assess the extent of sensitive data exposure and determine if any data has been exfiltrated.
- Change all credentials associated with the compromised files, such as SSH keys and AWS credentials, to prevent unauthorized access using stolen credentials.
- Restore any altered or deleted configuration files from a known good backup to ensure system integrity and functionality.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for compression utilities and sensitive file access to detect and respond to similar threats more effectively in the future.
