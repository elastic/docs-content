---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Windows Sandbox with Sensitive Configuration" prebuilt detection rule.'
---

# Windows Sandbox with Sensitive Configuration

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Windows Sandbox with Sensitive Configuration

Windows Sandbox is a lightweight virtual environment designed to safely run untrusted applications. It isolates processes from the host system, preventing permanent changes. However, adversaries can exploit this by configuring the sandbox to access host resources, enabling network connections, or executing commands at startup. The detection rule identifies such misuse by monitoring specific process activities and configurations indicative of potential abuse, such as unauthorized file system access or network enablement, helping analysts spot and mitigate threats effectively.

### Possible investigation steps

- Review the process details for "wsb.exe" or "WindowsSandboxClient.exe" to confirm the start of a new container and check for any unusual command-line arguments that match the query criteria, such as "<Networking>Enable</Networking>" or "<NetworkingEnabled>true>".
- Investigate any file system access attempts by the sandbox, particularly focusing on write access to the host file system indicated by "<HostFolder>C:\<ReadOnly>false". Determine if any unauthorized or suspicious files have been modified or created.
- Examine network activity associated with the sandbox process to identify any unexpected or unauthorized connections, especially if "<NetworkingEnabled>true>" is present in the command line.
- Check for any logon commands executed by the sandbox process using "<LogonCommand>" in the command line to identify potential persistence mechanisms or automated tasks that could indicate malicious intent.
- Correlate the sandbox activity with other security alerts or logs from data sources like Elastic Endgame, Sysmon, or Microsoft Defender for Endpoint to gather additional context and identify any related suspicious activities.

### False positive analysis

- Legitimate software installations or updates may configure the Windows Sandbox to enable network connections or access host resources. Users can create exceptions for known software update processes to prevent unnecessary alerts.
- Developers and IT administrators might use Windows Sandbox for testing purposes, which could involve enabling network connections or accessing host files. Establishing a list of approved users or processes that frequently perform these actions can help reduce false positives.
- Automated scripts or tools that configure the sandbox for legitimate purposes, such as testing or development, may trigger the rule. Identifying and excluding these scripts from monitoring can minimize false alerts.
- Security tools or system management software might use sandbox features for legitimate operations. Users should verify and whitelist these tools to avoid misidentification as threats.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, specifically those related to Windows Sandbox misuse, such as "wsb.exe" or "WindowsSandboxClient.exe".
- Conduct a thorough review of the system's file system and network logs to identify any unauthorized access or data transfers that may have occurred.
- Remove any unauthorized configurations or scripts found within the Windows Sandbox environment that enable network connections or host file system access.
- Restore the system to a known good state using backups or system restore points, ensuring that any malicious changes are reversed.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and alerting for similar suspicious activities, focusing on process creation and command-line parameters related to Windows Sandbox configurations.
