---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Git Hook Egress Network Connection" prebuilt detection rule.
---

# Git Hook Egress Network Connection

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Git Hook Egress Network Connection

Git hooks are scripts that automate tasks during Git operations like commits or pushes. Adversaries can exploit these hooks to execute unauthorized commands, maintain persistence, or initiate network connections for data exfiltration. The detection rule identifies suspicious network activities by monitoring script executions from Git hooks and subsequent egress connections to non-local IPs, flagging potential misuse.

### Possible investigation steps

- Review the process execution details to identify the specific Git hook script that triggered the alert. Check the process.args field for the exact script path within the .git/hooks directory.
- Investigate the parent process details to confirm the legitimacy of the Git operation. Verify the process.parent.name is "git" and assess whether the Git activity aligns with expected user or system behavior.
- Analyze the destination IP address involved in the network connection attempt. Use the destination.ip field to determine if the IP is known, trusted, or associated with any malicious activity.
- Check for any additional network connections from the same host around the time of the alert to identify potential patterns or additional suspicious activity.
- Correlate the alert with any recent changes in the repository or system that might explain the execution of the Git hook, such as recent commits or updates.
- Review user activity logs to determine if the Git operation was performed by an authorized user and if their actions align with their typical behavior.
- If suspicious activity is confirmed, isolate the affected system to prevent further unauthorized access or data exfiltration and initiate a deeper forensic analysis.

### False positive analysis

- Legitimate automated scripts or CI/CD pipelines may trigger Git hooks to perform network operations. Review the source and purpose of these scripts and consider excluding them if they are verified as non-threatening.
- Development environments often use Git hooks for tasks like fetching dependencies or updating remote services. Identify these common operations and create exceptions for known safe IP addresses or domains.
- Internal tools or services that rely on Git hooks for communication with other internal systems might be flagged. Ensure these tools are documented and whitelist their network activities if they are deemed secure.
- Frequent updates or deployments that involve Git hooks could lead to repeated alerts. Monitor the frequency and context of these alerts to determine if they are part of regular operations and adjust the rule to reduce noise.
- Consider the context of the network connection, such as the destination IP or domain. If the destination is a known and trusted entity, it may be appropriate to exclude it from triggering alerts.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized egress connections and potential data exfiltration.
- Terminate any suspicious processes identified as originating from Git hooks, particularly those executing shell scripts like bash, dash, or zsh.
- Conduct a thorough review of the .git/hooks directory on the affected system to identify and remove any unauthorized or malicious scripts.
- Reset credentials and access tokens associated with the affected Git repository to prevent further unauthorized access.
- Restore any modified or deleted files from a known good backup to ensure system integrity.
- Implement network monitoring to detect and block any future unauthorized egress connections from Git hooks or similar scripts.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems or repositories.
