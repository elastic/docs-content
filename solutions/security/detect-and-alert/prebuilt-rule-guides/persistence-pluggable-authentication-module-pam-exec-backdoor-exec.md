---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Backdoor Execution Through PAM_EXEC" prebuilt detection rule.'
---

# Potential Backdoor Execution Through PAM_EXEC

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Backdoor Execution Through PAM_EXEC

PAM (Pluggable Authentication Module) is a critical framework in Linux systems for user authentication. Adversaries may exploit PAM by inserting malicious modules that execute backdoor scripts during user logins, ensuring persistent access. The detection rule identifies this threat by monitoring SSH session changes followed by unusual child processes, often indicative of backdoor execution, especially when these processes originate from suspicious directories or use scripting languages.

### Possible investigation steps

- Review the process entity ID associated with the alert to identify the specific SSH session and its related activities.
- Examine the parent process details, specifically focusing on the SSH or SSHD process, to determine the source and legitimacy of the login attempt.
- Investigate the child process that was started, paying close attention to its name and executable path, especially if it matches patterns like scripting languages (e.g., perl, python) or suspicious directories (e.g., /tmp, /var/tmp).
- Check the process arguments count and content to understand the command or script being executed, which may provide insights into the potential backdoor's functionality.
- Correlate the event timestamp with user login records and system logs to identify any unusual login patterns or unauthorized access attempts.
- Assess the risk and impact by determining if the process has made any unauthorized changes to the system or if it has established any persistent mechanisms.
- If a backdoor is confirmed, initiate containment measures such as terminating the malicious process, removing the unauthorized PAM module, and conducting a full system audit to prevent further exploitation.

### False positive analysis

- Legitimate administrative scripts executed via SSH may trigger the rule if they use scripting languages like Perl, Python, or PHP. To handle this, identify and whitelist known administrative scripts and their execution paths.
- Automated backup or maintenance processes that run from directories like /var/backups or /var/log can be mistaken for malicious activity. Exclude these processes by specifying their exact paths and names in the exception list.
- Development or testing environments where scripts are frequently executed from temporary directories such as /tmp or /dev/shm may cause false positives. Implement exceptions for these environments by defining specific user accounts or process names that are known to be safe.
- Custom monitoring or logging tools that spawn child processes from SSH sessions might be flagged. Review these tools and add them to the exclusion list if they are verified as non-threatening.
- Regular user activities involving the use of scripting languages for legitimate purposes can be misinterpreted. Educate users on best practices and adjust the rule to exclude common benign scripts used in daily operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, especially those originating from unusual directories or using scripting languages.
- Conduct a thorough review of PAM configuration files and modules to identify and remove any unauthorized or malicious entries.
- Reset credentials for all users on the affected system, prioritizing those with elevated privileges, to mitigate potential credential compromise.
- Restore the system from a known good backup if malicious modifications are confirmed, ensuring that the backup is free from tampering.
- Implement enhanced monitoring on the affected system and similar environments to detect any recurrence of the threat, focusing on SSH session changes and unusual child processes.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on other systems within the network.
