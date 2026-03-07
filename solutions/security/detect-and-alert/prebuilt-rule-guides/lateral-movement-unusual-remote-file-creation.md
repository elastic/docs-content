---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Remote File Creation" prebuilt detection rule.'
---

# Unusual Remote File Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Remote File Creation

Remote file creation tools like SCP, FTP, and SFTP are essential for transferring files across networks, often used in legitimate administrative tasks. However, adversaries can exploit these services to move laterally within a network, creating files in unauthorized locations. The detection rule identifies suspicious file creation activities by monitoring specific processes and excluding typical paths, thus highlighting potential lateral movement attempts by attackers.

### Possible investigation steps

- Review the alert details to identify the specific process name (e.g., scp, ftp, sftp) involved in the file creation event.
- Examine the file path where the file was created to determine if it is an unusual or unauthorized location, considering the exclusion of typical paths like /dev/ptmx, /run/*, or /var/run/*.
- Check the user account associated with the process to verify if it is a legitimate user or if there are signs of compromised credentials.
- Investigate the source and destination IP addresses involved in the file transfer to identify any suspicious or unexpected network connections.
- Analyze recent activity on the host to identify any other unusual or unauthorized actions that may indicate lateral movement or further compromise.
- Correlate this event with other alerts or logs to determine if it is part of a broader attack pattern or campaign within the network.

### False positive analysis

- Administrative file transfers: Legitimate administrative tasks often involve transferring files using SCP, FTP, or SFTP. To manage this, create exceptions for known administrative accounts or specific IP addresses that regularly perform these tasks.
- Automated backup processes: Scheduled backups may use tools like rsync or sftp-server to create files remotely. Identify and exclude these processes by specifying the paths or scripts involved in the backup operations.
- System updates and patches: Some system updates might involve remote file creation in non-standard directories. Monitor update schedules and exclude these activities by correlating them with known update events.
- Development and testing environments: Developers may use remote file transfer services to deploy or test applications. Establish a baseline of typical development activities and exclude these from alerts by defining specific user accounts or project directories.
- Third-party integrations: Some third-party applications might require remote file creation as part of their functionality. Document these integrations and exclude their associated processes or file paths from triggering alerts.

### Response and remediation

- Isolate the affected host immediately to prevent further lateral movement within the network. This can be done by removing the host from the network or applying network segmentation controls.
- Terminate any suspicious processes identified in the alert, such as scp, ftp, sftp, vsftpd, sftp-server, or sync, to stop unauthorized file transfers.
- Conduct a thorough review of the file paths and files created to determine if any sensitive data has been compromised or if any malicious files have been introduced.
- Restore any unauthorized or malicious file changes from known good backups to ensure system integrity.
- Update and patch the affected systems to close any vulnerabilities that may have been exploited by the attacker.
- Implement stricter access controls and authentication mechanisms for remote file transfer services to prevent unauthorized use.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems have been compromised.
