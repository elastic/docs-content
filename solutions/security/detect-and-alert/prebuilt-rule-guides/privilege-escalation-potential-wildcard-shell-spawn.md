---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Shell via Wildcard Injection Detected" prebuilt detection rule.
---

# Potential Shell via Wildcard Injection Detected

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Shell via Wildcard Injection Detected

Wildcard injection exploits vulnerabilities in Linux command-line utilities by manipulating wildcard characters to execute unauthorized commands. Adversaries leverage this to escalate privileges or execute arbitrary code. The detection rule identifies suspicious use of vulnerable binaries like `tar`, `rsync`, and `zip` followed by shell execution, indicating potential exploitation attempts.

### Possible investigation steps

- Review the process details to identify the specific command executed, focusing on the process name and arguments, especially those involving `tar`, `rsync`, or `zip` with suspicious flags like `--checkpoint=*`, `-e*`, or `--unzip-command`.
- Examine the parent process information to determine if a shell process (e.g., `bash`, `sh`, `zsh`) was spawned, indicating potential exploitation.
- Check the process execution path to ensure it does not match the exclusion pattern `/tmp/newroot/*`, which might indicate a benign operation.
- Investigate the host's recent activity logs to identify any other suspicious or related events that might indicate a broader attack or compromise.
- Correlate the alert with any other security events or alerts from the same host to assess if this is part of a larger attack pattern or campaign.
- Assess the user account associated with the process execution to determine if it has the necessary privileges and if the activity aligns with expected behavior for that account.

### False positive analysis

- Legitimate use of tar, rsync, or zip with wildcard-related flags in automated scripts or backup processes can trigger false positives. Review the context of these processes and consider excluding specific scripts or directories from monitoring if they are verified as safe.
- System administrators or maintenance scripts may use shell commands following tar, rsync, or zip for legitimate purposes. Identify these routine operations and create exceptions for known safe parent processes or specific command patterns.
- Development environments or testing scenarios might involve intentional use of wildcard characters for testing purposes. Exclude these environments from the rule or adjust the rule to ignore specific user accounts or process paths associated with development activities.
- Scheduled tasks or cron jobs that involve the use of these binaries with wildcard flags can be mistaken for malicious activity. Verify the legitimacy of these tasks and exclude them based on their schedule or specific command line arguments.
- Security tools or monitoring solutions that simulate attacks for testing or validation purposes might trigger this rule. Ensure these tools are recognized and excluded from monitoring to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious processes identified in the alert, particularly those involving the execution of shell commands following the use of `tar`, `rsync`, or `zip`.
- Conduct a thorough review of the affected system's logs to identify any additional indicators of compromise or unauthorized access attempts.
- Restore the affected system from a known good backup if any unauthorized changes or malicious activities are confirmed.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Implement file integrity monitoring on critical systems to detect unauthorized changes to system binaries or configuration files.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
