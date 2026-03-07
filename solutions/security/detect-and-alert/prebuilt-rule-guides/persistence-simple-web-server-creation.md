---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Simple HTTP Web Server Creation" prebuilt detection rule.
---

# Simple HTTP Web Server Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Simple HTTP Web Server Creation

Simple HTTP web servers, often created using PHP or Python, are lightweight and easy to deploy, making them ideal for quick file sharing or testing. However, adversaries exploit this simplicity to establish persistence on compromised Linux systems. By deploying a web server, they can upload malicious payloads, such as reverse shells, to maintain remote access. The detection rule identifies suspicious server creation by monitoring process executions that match specific patterns, such as PHP or Python commands indicative of server setup, thereby alerting analysts to potential threats.

### Possible investigation steps

- Review the process execution details to confirm the presence of PHP or Python commands with arguments matching the patterns specified in the query, such as PHP with the "-S" argument or Python with "--cgi" or "CGIHTTPServer".
- Identify the user account under which the suspicious process was executed to determine if it aligns with expected behavior or if it indicates potential compromise.
- Examine the network activity associated with the process to identify any unusual connections or data transfers that could suggest malicious intent or data exfiltration.
- Check the file system for any newly created or modified files in the web server's root directory that could contain malicious payloads, such as reverse shells.
- Investigate the parent process of the suspicious server creation to understand how the process was initiated and whether it was triggered by another potentially malicious activity.
- Correlate the alert with other security events or logs from the same host to identify any additional indicators of compromise or related suspicious activities.

### False positive analysis

- Development and testing environments often use simple HTTP servers for legitimate purposes such as serving static files or testing web applications. To manage this, create exceptions for known development directories or user accounts frequently involved in these activities.
- Automated scripts or cron jobs may start simple HTTP servers for routine tasks like file distribution or internal data sharing. Identify these scripts and exclude their execution paths or associated user accounts from triggering alerts.
- Educational or training sessions might involve setting up simple HTTP servers as part of learning exercises. Exclude specific IP ranges or user groups associated with training environments to prevent false positives.
- System administrators might use simple HTTP servers for quick troubleshooting or system maintenance tasks. Document these activities and create exceptions based on the administrator's user accounts or specific server names.
- Continuous integration and deployment pipelines may temporarily start HTTP servers during build or deployment processes. Identify these pipelines and exclude their associated processes or execution contexts from the detection rule.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious PHP or Python processes identified by the detection rule to halt the operation of the unauthorized web server.
- Conduct a thorough examination of the web server's root directory to identify and remove any malicious payloads, such as reverse shells or unauthorized scripts.
- Review system logs and network traffic to identify any additional indicators of compromise or lateral movement attempts by the adversary.
- Restore the system from a known good backup if any critical system files or configurations have been altered by the adversary.
- Implement stricter access controls and monitoring on the affected system to prevent similar unauthorized server setups in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are compromised.
