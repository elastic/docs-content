---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Linux Credential Dumping via Proc Filesystem" prebuilt detection rule.
---

# Potential Linux Credential Dumping via Proc Filesystem

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Linux Credential Dumping via Proc Filesystem

The /proc filesystem in Linux provides a window into the system's processes, offering details like memory usage and command-line arguments. Adversaries exploit this by using tools like mimipenguin to extract plaintext credentials from memory, leveraging vulnerabilities such as CVE-2018-20781. The detection rule identifies suspicious sequences involving the 'ps' and 'strings' commands, which are indicative of attempts to access and parse sensitive data from the /proc filesystem.

### Possible investigation steps

- Review the alert details to identify the specific host.id where the suspicious activity was detected, focusing on the processes involved.
- Examine the process execution history on the affected host to confirm the presence of the 'ps' and 'strings' commands executed in sequence, as indicated by the query.
- Investigate the command-line arguments used with the 'ps' and 'strings' commands to determine if they match the suspicious patterns specified in the query, such as '-eo pid command' and '/tmp/*'.
- Check for any recent modifications or suspicious files in the /tmp directory on the affected host, as this is a common location for temporary files used in attacks.
- Analyze the system logs and any available network traffic data to identify potential lateral movement or data exfiltration attempts following the credential dumping activity.
- Assess the system for any signs of compromise or additional malicious activity, such as unauthorized user accounts or unexpected network connections.
- Consider isolating the affected host from the network to prevent further credential exposure and initiate a comprehensive forensic analysis to understand the full scope of the incident.

### False positive analysis

- System administrators or monitoring tools may use the 'ps' and 'strings' commands for legitimate system diagnostics and performance monitoring. To mitigate this, create exceptions for known administrative scripts or tools that regularly execute these commands.
- Automated scripts for system health checks might trigger the rule if they use 'ps' and 'strings' to gather process information. Identify and whitelist these scripts by their specific command patterns or execution paths.
- Security tools that perform regular scans or audits might mimic the behavior detected by the rule. Review and exclude these tools by their process names or execution context to prevent false alerts.
- Developers or testers running debugging sessions may inadvertently trigger the rule when analyzing process memory. Establish a process to temporarily disable the rule or exclude specific user accounts during known testing periods.
- Custom monitoring solutions that log process details for analysis could match the rule's criteria. Document and exclude these solutions by their unique execution characteristics or host identifiers.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further credential exposure and potential lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule, specifically those involving the 'ps' and 'strings' commands with the specified arguments.
- Conduct a thorough review of the affected system's process memory and logs to identify any additional unauthorized access or data exfiltration attempts.
- Change passwords for all user accounts on the affected system, prioritizing those with elevated privileges, to mitigate the risk of credential misuse.
- Apply patches and updates to address CVE-2018-20781 and any other known vulnerabilities on the affected system to prevent future exploitation.
- Enhance monitoring and logging on the affected host and similar systems to detect any recurrence of the exploit or similar suspicious activities.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on the broader network.
