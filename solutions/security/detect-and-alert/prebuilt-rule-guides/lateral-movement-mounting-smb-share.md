---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Attempt to Mount SMB Share via Command Line" prebuilt detection rule.
---

# Attempt to Mount SMB Share via Command Line

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Attempt to Mount SMB Share via Command Line

SMB (Server Message Block) is a protocol used for network file sharing, allowing applications to read and write to files and request services from server programs in a computer network. Adversaries exploit SMB to move laterally within a network by accessing shared resources using valid credentials. The detection rule identifies suspicious command-line activities on macOS, such as using built-in commands to mount SMB shares, which may indicate unauthorized access attempts. It filters out benign processes, like those from Google Drive, to reduce false positives, focusing on potential threats.

### Possible investigation steps

- Review the process details to confirm the execution of commands like "mount_smbfs", "open", "mount", or "osascript" with arguments indicating an attempt to mount an SMB share.
- Check the user account associated with the process to determine if it is a valid and authorized user for accessing SMB shares.
- Investigate the source and destination IP addresses involved in the SMB connection attempt to identify if they are known and trusted within the network.
- Examine the parent process of the suspicious activity to understand the context and origin of the command execution, ensuring it is not a benign process like Google Drive.
- Look for any other related alerts or logs that might indicate lateral movement or unauthorized access attempts within the network.
- Assess the risk and impact of the activity by correlating it with other security events or incidents involving the same user or system.

### False positive analysis

- Google Drive operations can trigger this rule due to its use of SMB for file synchronization. To manage this, exclude processes originating from the Google Drive application by using the provided exception for its executable path.
- Legitimate user activities involving manual mounting of SMB shares for accessing network resources may be flagged. To handle this, identify and whitelist specific user accounts or devices that regularly perform these actions as part of their normal workflow.
- Automated backup solutions that utilize SMB for network storage access might be detected. Review and exclude these processes by identifying their specific command-line patterns or parent processes.
- Development or testing environments where SMB shares are frequently mounted for application testing can cause alerts. Implement exceptions for these environments by specifying known IP addresses or hostnames associated with the test servers.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further lateral movement by the adversary.
- Verify the credentials used in the SMB mount attempt to determine if they have been compromised. Reset passwords and revoke access if necessary.
- Conduct a thorough review of recent login activities and access logs on the affected system and any connected SMB shares to identify unauthorized access or data exfiltration.
- Remove any unauthorized SMB mounts and ensure that no persistent connections remain active.
- Update and patch the macOS system and any related software to mitigate known vulnerabilities that could be exploited for lateral movement.
- Enhance monitoring and logging on the network to detect future unauthorized SMB mount attempts, focusing on the specific command-line patterns identified in the alert.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on the broader network infrastructure.
