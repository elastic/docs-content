---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Microsoft Exchange Server UM Spawning Suspicious Processes" prebuilt detection rule.'
---

# Microsoft Exchange Server UM Spawning Suspicious Processes

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Microsoft Exchange Server UM Spawning Suspicious Processes

Microsoft Exchange Server's Unified Messaging (UM) integrates voice messaging with email, allowing users to access voicemails via their inbox. Adversaries exploit vulnerabilities like CVE-2021-26857 to execute unauthorized processes, potentially leading to system compromise. The detection rule identifies unusual processes initiated by UM services, excluding known legitimate executables, to flag potential exploitation attempts.

### Possible investigation steps

- Review the alert details to confirm the process parent name is either "UMService.exe" or "UMWorkerProcess.exe" and verify the process executable path is not among the known legitimate paths listed in the exclusion criteria.
- Gather additional context by checking the process command line arguments and the user account under which the suspicious process was executed to identify any anomalies or unauthorized access.
- Investigate the historical activity of the host by reviewing recent logs for any other unusual or unauthorized processes, especially those related to the Microsoft Exchange Server.
- Check for any recent patches or updates applied to the Microsoft Exchange Server to ensure that vulnerabilities like CVE-2021-26857 have been addressed.
- Correlate the alert with other security tools and data sources such as Microsoft Defender for Endpoint or Sysmon to identify any related suspicious activities or indicators of compromise.
- Assess the network activity from the host to detect any potential lateral movement or data exfiltration attempts that might be associated with the suspicious process.

### False positive analysis

- Legitimate UM service updates or patches may trigger the rule. Regularly update the list of known legitimate executables to include new or updated UM service files.
- Custom scripts or monitoring tools that interact with UM services might be flagged. Identify these scripts and add their executables to the exclusion list if they are verified as safe.
- Non-standard installation paths for Exchange Server can cause false positives. Ensure that all legitimate installation paths are included in the exclusion list to prevent unnecessary alerts.
- Administrative tasks performed by IT staff using command-line tools may be misidentified. Document these tasks and consider excluding the associated executables if they are part of routine maintenance.
- Third-party integrations with Exchange Server that spawn processes could be flagged. Verify these integrations and exclude their executables if they are deemed secure and necessary for business operations.

### Response and remediation

- Isolate the affected Microsoft Exchange Server from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified as being spawned by the UM service that are not part of the known legitimate executables list.
- Apply the latest security patches and updates to the Microsoft Exchange Server to address CVE-2021-26857 and any other known vulnerabilities.
- Conduct a thorough review of the server's security logs and network traffic to identify any additional indicators of compromise or unauthorized access attempts.
- Restore the server from a known good backup taken before the suspicious activity was detected, ensuring that the backup is free from compromise.
- Implement enhanced monitoring and alerting for any future suspicious processes spawned by the UM service, using the detection rule as a baseline.
- Escalate the incident to the organization's security operations center (SOC) or incident response team for further investigation and to determine if additional systems may be affected.
