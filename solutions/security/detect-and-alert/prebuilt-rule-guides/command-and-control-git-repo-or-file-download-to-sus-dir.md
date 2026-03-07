---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Git Repository or File Download to Suspicious Directory" prebuilt detection rule.'
---

# Git Repository or File Download to Suspicious Directory

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Git Repository or File Download to Suspicious Directory

Git, wget, and curl are essential tools for managing and transferring files in Linux environments. Adversaries exploit these tools to download malicious payloads into temporary directories like /tmp, /var/tmp, or /dev/shm, which are often overlooked. The detection rule identifies this behavior by monitoring for git clone commands or GitHub downloads followed by file creation in these directories, signaling potential threats.

### Possible investigation steps

- Review the process details, including process.entity_id and process.name, to confirm the execution of git, wget, or curl commands and verify if they align with expected usage patterns.
- Examine the process.command_line field to identify the specific GitHub URL or repository being accessed, and assess whether it is known or potentially malicious.
- Check the file creation event details, focusing on the file.path to determine the exact location and nature of the files created in /tmp, /var/tmp, or /dev/shm directories.
- Investigate the host.id and host.os.type to gather additional context about the affected system, including its role and any recent changes or anomalies.
- Correlate the timing of the process start and file creation events to understand the sequence of actions and identify any potential patterns or anomalies.
- Consult threat intelligence sources to determine if the accessed GitHub repository or downloaded files are associated with known threats or malicious activity.

### False positive analysis

- Development activities may trigger this rule when developers clone repositories or download files from GitHub into temporary directories for testing purposes. To manage this, create exceptions for specific user accounts or processes that are known to perform legitimate development tasks.
- Automated scripts or cron jobs that regularly update or download files from GitHub into temporary directories can also cause false positives. Identify these scripts and exclude their process IDs or command patterns from the rule.
- System maintenance tasks that involve downloading updates or patches into temporary directories might be flagged. Coordinate with system administrators to identify these tasks and whitelist the associated processes or directories.
- Security tools or monitoring solutions that download threat intelligence feeds or other data into temporary directories could be mistakenly identified. Verify these tools and exclude their activities from the rule to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system to prevent further potential malicious activity and lateral movement within the network.
- Terminate any suspicious processes related to git, wget, or curl that are actively running and associated with the creation of files in the /tmp, /var/tmp, or /dev/shm directories.
- Conduct a thorough examination of the files created in these directories to identify and remove any malicious payloads or tools.
- Restore any compromised files or systems from clean backups to ensure the integrity of the affected system.
- Implement network monitoring to detect and block any unauthorized outbound connections to suspicious domains, particularly those related to GitHub or other code repositories.
- Escalate the incident to the security operations center (SOC) for further analysis and to determine if additional systems may be affected.
- Update endpoint protection and intrusion detection systems to enhance detection capabilities for similar threats, focusing on the specific indicators of compromise identified in this alert.
