---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Privilege Escalation via PKEXEC" prebuilt detection rule.
---

# Potential Privilege Escalation via PKEXEC

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Privilege Escalation via PKEXEC

Polkit's pkexec is a command-line utility that allows an authorized user to execute commands as another user, typically root, in Linux environments. Adversaries exploit vulnerabilities like CVE-2021-4034 by injecting unsecure environment variables, enabling unauthorized privilege escalation. The detection rule identifies suspicious file paths indicative of such exploitation attempts, focusing on environment variable manipulation to preemptively flag potential threats.

### Possible investigation steps

- Review the alert details to confirm the presence of the file path pattern "/*GCONV_PATH*" on a Linux host, as this is indicative of the potential exploitation attempt.
- Examine the process execution history on the affected host to identify any instances of pkexec being executed around the time of the alert. Look for unusual or unauthorized command executions.
- Check the environment variables set during the pkexec execution to identify any suspicious or unauthorized modifications that could indicate an exploitation attempt.
- Investigate the user account associated with the alert to determine if it has a history of privilege escalation attempts or other suspicious activities.
- Analyze system logs and security events for any additional indicators of compromise or related suspicious activities that occurred before or after the alert.
- Assess the patch status of the affected system to determine if it is vulnerable to CVE-2021-4034 and ensure that appropriate security updates have been applied.

### False positive analysis

- Routine administrative tasks involving pkexec may trigger alerts if they involve environment variable manipulation. Review the context of the command execution to determine if it aligns with expected administrative behavior.
- Custom scripts or applications that legitimately use environment variables in their execution paths might be flagged. Identify these scripts and consider adding them to an exception list if they are verified as non-threatening.
- Automated system management tools that modify environment variables for legitimate purposes could cause false positives. Monitor these tools and exclude their known safe operations from the detection rule.
- Development environments where developers frequently test applications with varying environment variables might generate alerts. Establish a baseline of normal activity and exclude these patterns if they are consistent and verified as safe.
- Scheduled tasks or cron jobs that involve environment variable changes should be reviewed. If they are part of regular system maintenance, document and exclude them from triggering alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further exploitation or lateral movement by the attacker.
- Terminate any suspicious processes associated with pkexec or unauthorized privilege escalation attempts to halt ongoing exploitation.
- Conduct a thorough review of system logs and file access records to identify any unauthorized changes or access patterns, focusing on the presence of GCONV_PATH in file paths.
- Revert any unauthorized changes made by the attacker, such as modifications to critical system files or configurations, to restore system integrity.
- Apply the latest security patches and updates to the polkit package to address CVE-2021-4034 and prevent future exploitation.
- Implement enhanced monitoring and alerting for similar privilege escalation attempts, ensuring that any future attempts are detected and responded to promptly.
- Report the incident to relevant internal security teams and, if necessary, escalate to external authorities or cybersecurity partners for further investigation and support.
