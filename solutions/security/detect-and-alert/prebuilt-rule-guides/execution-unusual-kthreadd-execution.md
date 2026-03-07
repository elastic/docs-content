---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Execution from Kernel Thread (kthreadd) Parent" prebuilt detection rule.
---

# Unusual Execution from Kernel Thread (kthreadd) Parent

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Execution from Kernel Thread (kthreadd) Parent

The kernel thread (kthreadd) is a fundamental component in Linux systems responsible for managing kernel-level processes. Adversaries may exploit kthreadd to execute payloads from kernel space, thereby evading detection due to its trusted status. The detection rule identifies suspicious child processes initiated by kthreadd, focusing on unusual executable paths and command lines indicative of malicious activity, while filtering out known benign processes.

### Possible investigation steps

- Review the alert details to identify the specific child process name and executable path that triggered the rule. Focus on paths like /dev/shm, /tmp, /var/tmp, and /var/www, which are commonly used for storing temporary or potentially malicious files.
- Examine the command line arguments associated with the suspicious process. Look for indicators of compromise such as references to sensitive files or directories like /etc/shadow, /etc/sudoers, or ~/.ssh, as well as suspicious commands like base64 or cron.
- Check the parent process details to confirm it is indeed kthreadd. Investigate any unusual behavior or anomalies in the parent process that might suggest exploitation or manipulation.
- Investigate the network activity of the host to identify any connections to suspicious IP addresses or domains, especially if the command line includes references to /dev/tcp or other network-related paths.
- Analyze the system logs and historical data to determine if similar alerts have been triggered in the past, which might indicate a persistent threat or repeated exploitation attempts.
- Assess the risk and impact of the detected activity by correlating it with other security events or alerts on the host, considering the medium severity and risk score of 47 associated with this rule.

### False positive analysis

- Legitimate system maintenance tasks may trigger this rule, such as automated scripts running from temporary directories. Users can create exceptions for specific scripts or processes that are verified as safe.
- Development or testing environments often use temporary directories for executing scripts. Exclude known development tools or scripts from these environments to reduce noise.
- Some monitoring or backup tools might use command lines or executables that match the rule's criteria. Identify these tools and add them to the exclusion list to prevent false alerts.
- Custom administrative scripts that perform routine checks or updates might inadvertently match the rule. Review these scripts and exclude them if they are part of regular operations.
- If certain processes are consistently flagged but are known to be benign, consider adjusting the rule to exclude these specific processes or command lines to improve detection accuracy.

### Response and remediation

- Isolate the affected host immediately to prevent further malicious activity and lateral movement within the network.
- Terminate any suspicious processes identified as child processes of kthreadd that match the alert criteria, ensuring to log the process details for further analysis.
- Conduct a thorough review of the file paths and command lines flagged in the alert to identify any unauthorized or malicious files or scripts. Remove or quarantine these files as necessary.
- Check for unauthorized modifications in critical system files and directories such as /etc/init.d, /etc/ssh, and /root/.ssh. Restore any altered files from a known good backup.
- Escalate the incident to the security operations team for a deeper forensic investigation to determine the root cause and entry point of the threat.
- Implement additional monitoring on the affected host and similar systems to detect any recurrence of the threat, focusing on the specific indicators identified in the alert.
- Update and patch the affected system to the latest security standards to mitigate vulnerabilities that may have been exploited by the adversary.

