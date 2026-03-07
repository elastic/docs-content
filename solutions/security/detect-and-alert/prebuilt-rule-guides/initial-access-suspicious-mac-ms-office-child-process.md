---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious macOS MS Office Child Process" prebuilt detection rule.'
---

# Suspicious macOS MS Office Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious macOS MS Office Child Process

Microsoft Office applications on macOS can be exploited by adversaries to execute malicious child processes, often through malicious macros or document exploits. These child processes may include scripting languages or utilities that can be leveraged for unauthorized actions. The detection rule identifies such suspicious activity by monitoring for unexpected child processes spawned by Office apps, while filtering out known benign behaviors and false positives, thus helping to pinpoint potential threats.

### Possible investigation steps

- Review the parent process name and executable path to confirm if the Office application is legitimate and expected on the host.
- Examine the child process name and command line arguments to identify any potentially malicious or unexpected behavior, such as the use of scripting languages or network utilities like curl or nscurl.
- Check the process arguments for any indicators of compromise or suspicious patterns that are not filtered out by the rule, such as unexpected network connections or file modifications.
- Investigate the effective parent executable path to ensure it is not associated with known benign applications or services that are excluded by the rule.
- Correlate the alert with any recent phishing attempts or suspicious email activity that might have led to the execution of malicious macros or document exploits.
- Analyze the host's recent activity and system logs to identify any other anomalies or related alerts that could provide additional context or evidence of compromise.

### False positive analysis

- Product version discovery commands can trigger false positives. Exclude processes with arguments like "ProductVersion" and "ProductBuildVersion" to reduce noise.
- Office error reporting may cause alerts. Exclude paths related to Microsoft Error Reporting to prevent unnecessary alerts.
- Network setup and management tools such as "/usr/sbin/networksetup" can be benign. Exclude these executables if they are part of regular system operations.
- Third-party applications like ToDesk and JumpCloud Agent might be flagged. Exclude their executables if they are verified as safe and part of normal operations.
- Zotero integration can cause false positives with shell processes. Exclude specific command lines involving "CFFIXED_USER_HOME/.zoteroIntegrationPipe" to avoid these alerts.

### Response and remediation

- Immediately isolate the affected macOS device from the network to prevent further malicious activity or lateral movement.
- Terminate any suspicious child processes identified by the alert, such as those involving scripting languages or utilities like curl, bash, or osascript.
- Conduct a thorough review of the parent Microsoft Office application and associated documents to identify and remove any malicious macros or document exploits.
- Restore the affected system from a known good backup if malicious activity has compromised system integrity or data.
- Update all Microsoft Office applications to the latest version to patch any known vulnerabilities that could be exploited by similar threats.
- Implement application whitelisting to restrict the execution of unauthorized scripts and utilities, reducing the risk of exploitation through Office applications.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
