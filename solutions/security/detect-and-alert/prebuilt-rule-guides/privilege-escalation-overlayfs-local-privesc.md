---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Privilege Escalation via OverlayFS" prebuilt detection rule.
---

# Potential Privilege Escalation via OverlayFS

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Privilege Escalation via OverlayFS

OverlayFS is a union filesystem used in Linux environments to overlay one filesystem on top of another, allowing for efficient file management and updates. Adversaries exploit vulnerabilities in Ubuntu's OverlayFS modifications to execute crafted executables that escalate privileges to root. The detection rule identifies suspicious sequences involving the 'unshare' command with specific arguments and subsequent UID changes to root, indicating potential exploitation attempts.

### Possible investigation steps

- Review the alert details to confirm the presence of the 'unshare' command with the specific arguments '-r', '-rm', 'm', and '*cap_setuid*' as indicated in the query. This will help verify if the command execution aligns with the known exploitation pattern.
- Check the process tree and parent process information using the process.parent.entity_id to understand the context in which the 'unshare' command was executed. This can provide insights into whether the command was part of a legitimate operation or a potential attack.
- Investigate the user account associated with the process execution (user.id != "0") to determine if the account has a history of suspicious activity or if it has been compromised.
- Examine the host.id and host.os.type fields to identify the specific Linux host involved and assess its vulnerability status regarding CVE-2023-2640 and CVE-2023-32629. This can help determine if the host is susceptible to the exploitation attempt.
- Analyze any subsequent UID changes to root (user.id == "0") to confirm if the privilege escalation was successful and identify any unauthorized access or actions taken by the elevated process.
- Review system logs and other security alerts around the time of the event to identify any additional indicators of compromise or related suspicious activities that might corroborate the exploitation attempt.

### False positive analysis

- Legitimate administrative tasks using the 'unshare' command with similar arguments may trigger the rule. Review the context of the command execution and verify if it aligns with routine system maintenance or configuration changes.
- Automated scripts or system management tools that utilize 'unshare' for containerization or namespace isolation might cause false positives. Identify these scripts and consider excluding their specific process names or paths from the rule.
- Development environments where developers frequently test applications with elevated privileges could inadvertently match the rule criteria. Implement user-based exceptions for known developer accounts to reduce noise.
- Security tools or monitoring solutions that simulate privilege escalation scenarios for testing purposes may be flagged. Whitelist these tools by their process hash or signature to prevent unnecessary alerts.
- Custom applications that require temporary privilege elevation for legitimate operations should be reviewed. If deemed safe, add these applications to an exception list based on their unique identifiers.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further exploitation or lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule, particularly those involving the 'unshare' command with the specified arguments.
- Conduct a thorough review of user accounts and privileges on the affected system to ensure no unauthorized changes have been made, especially focusing on accounts with root access.
- Apply the latest security patches and updates to the affected system, specifically addressing CVE-2023-2640 and CVE-2023-32629, to mitigate the vulnerability in OverlayFS.
- Monitor for any further attempts to exploit the vulnerability by setting up alerts for similar sequences of commands and UID changes.
- Escalate the incident to the security operations team for a detailed forensic analysis to understand the scope and impact of the exploitation attempt.
- Implement additional security measures, such as enhanced logging and monitoring, to detect and respond to privilege escalation attempts more effectively in the future.
