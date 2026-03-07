---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "At Job Created or Modified" prebuilt detection rule.'
---

# At Job Created or Modified

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating At Job Created or Modified

The 'at' command in Linux schedules tasks for future execution, aiding system admins in automating routine jobs. However, attackers can exploit this for persistence, privilege escalation, or executing unauthorized commands. The detection rule identifies suspicious 'at' job creations or modifications by monitoring specific file paths and excluding benign processes, helping to flag potential malicious activities.

### Possible investigation steps

- Review the file path of the created or modified 'at' job to confirm it is within the monitored directory: /var/spool/cron/atjobs/*. Determine if the file path is expected or unusual for the system's typical operations.
- Identify the process that triggered the alert by examining the process.executable field. Check if the process is known and expected in the context of the system's normal operations.
- Investigate the user account associated with the process that created or modified the 'at' job. Determine if the account has legitimate reasons to schedule tasks or if it might be compromised.
- Check the contents of the 'at' job file to understand the commands or scripts scheduled for execution. Look for any suspicious or unauthorized commands that could indicate malicious intent.
- Correlate the event with other recent alerts or logs from the same host to identify any patterns or additional indicators of compromise, such as privilege escalation attempts or unauthorized access.
- Verify if there are any known vulnerabilities or exploits associated with the processes or commands involved in the alert, which could provide further context on the potential threat.

### False positive analysis

- System package managers like dpkg, rpm, and yum can trigger false positives when they create or modify at jobs during software installations or updates. To manage this, ensure these processes are included in the exclusion list within the detection rule.
- Automated system management tools such as Puppet and Chef may also create or modify at jobs as part of their routine operations. Add these tools to the exclusion list to prevent unnecessary alerts.
- Temporary files with extensions like swp or dpkg-remove can be mistakenly flagged. Exclude these file extensions from the rule to reduce false positives.
- Processes running from directories like /nix/store or /snap can be benign and should be considered for exclusion if they are part of regular system operations.
- If the process executable is null, it might indicate a benign system process that lacks a defined executable path. Consider reviewing these cases to determine if they are legitimate and adjust the rule accordingly.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or execution of malicious tasks.
- Terminate any suspicious processes associated with the creation or modification of 'at' jobs that are not part of the excluded benign processes.
- Review and remove any unauthorized 'at' jobs found in the /var/spool/cron/atjobs/ directory to eliminate persistence mechanisms.
- Conduct a thorough examination of the system for additional indicators of compromise, such as unauthorized user accounts or unexpected network connections.
- Restore the system from a known good backup if malicious activity is confirmed and cannot be fully remediated.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for 'at' job activities to detect similar threats in the future, ensuring that alerts are promptly reviewed and acted upon.
