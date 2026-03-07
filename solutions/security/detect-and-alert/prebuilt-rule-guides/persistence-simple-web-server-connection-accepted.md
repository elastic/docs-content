---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Simple HTTP Web Server Connection" prebuilt detection rule.
---

# Simple HTTP Web Server Connection

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Simple HTTP Web Server Connection

Simple HTTP servers in Python and PHP are often used for development and testing, providing a quick way to serve web content. However, attackers can exploit these servers to maintain access on compromised Linux systems by deploying backdoors or executing commands remotely. The detection rule identifies suspicious server activity by monitoring for specific process patterns and command-line arguments indicative of these lightweight servers, flagging potential misuse for further investigation.

### Possible investigation steps

- Review the process details, including the process name and command line arguments, to confirm if the server was started using Python or PHP, as indicated by the query fields.
- Check the network connection details associated with the event, such as the source and destination IP addresses and ports, to identify any suspicious or unexpected connections.
- Investigate the user account under which the process was initiated to determine if it aligns with expected behavior or if it indicates potential unauthorized access.
- Examine the system logs and any related events around the time of the alert to identify any additional suspicious activities or anomalies.
- Assess the server's web root directory for any unauthorized files or scripts that could indicate a backdoor or malicious payload.
- Correlate this event with other alerts or indicators of compromise on the system to evaluate if this is part of a larger attack campaign.

### False positive analysis

- Development and testing environments may frequently trigger this rule when developers use Python or PHP's built-in HTTP servers for legitimate purposes. To manage this, consider excluding specific user accounts or IP addresses associated with development activities from the rule.
- Automated scripts or cron jobs that start simple HTTP servers for routine tasks can also generate false positives. Identify these scripts and add their process names or command-line patterns to an exception list.
- Educational or training environments where students are learning web development might cause alerts. In such cases, exclude the network segments or user groups associated with these activities.
- Internal tools or services that rely on lightweight HTTP servers for functionality might be flagged. Review these tools and whitelist their specific process names or command-line arguments to prevent unnecessary alerts.
- Temporary testing servers spun up for short-term projects can be mistaken for malicious activity. Document these instances and apply temporary exceptions during the project duration.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious Python or PHP processes identified by the detection rule to stop the potential backdoor or unauthorized server activity.
- Conduct a thorough review of the system's file system, focusing on the web root directory, to identify and remove any unauthorized scripts or payloads that may have been uploaded.
- Change all credentials associated with the compromised system, including SSH keys and passwords, to prevent attackers from regaining access.
- Restore the system from a known good backup if any unauthorized changes or persistent threats are detected that cannot be easily remediated.
- Implement network monitoring to detect any future unauthorized HTTP server activity, focusing on unusual process patterns and command-line arguments.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
