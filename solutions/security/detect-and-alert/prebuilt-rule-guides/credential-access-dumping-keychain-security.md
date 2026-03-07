---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Dumping of Keychain Content via Security Command" prebuilt detection rule.
---

# Dumping of Keychain Content via Security Command

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Dumping of Keychain Content via Security Command

Keychains in macOS securely store user credentials, including passwords and certificates. Adversaries exploit this by using commands to extract keychain data, aiming to access sensitive information. The detection rule identifies suspicious activity by monitoring processes that initiate keychain dumps, specifically looking for command-line arguments associated with this malicious behavior, thus alerting analysts to potential credential theft attempts.

### Possible investigation steps

- Review the process details to identify the parent process and determine if the keychain dump was initiated by a legitimate application or user.
- Examine the user account associated with the process to verify if the activity aligns with their typical behavior or if the account may be compromised.
- Check the timestamp of the event to correlate with any other suspicious activities or anomalies on the system around the same time.
- Investigate the command-line arguments used in the process to confirm if they match known patterns of malicious keychain dumping attempts.
- Analyze any network connections or data transfers initiated by the process to identify potential exfiltration of the dumped keychain data.
- Look for additional alerts or logs from the same host or user to assess if this is part of a broader attack campaign.

### False positive analysis

- Legitimate administrative tasks or system maintenance activities may trigger the rule if they involve keychain access. Users should review the context of the process initiation to determine if it aligns with routine administrative operations.
- Security or IT tools that perform regular audits or backups of keychain data might be flagged. Users can create exceptions for these tools by identifying their specific process names or paths and excluding them from the rule.
- Developers or advanced users testing applications that require keychain access might inadvertently trigger the rule. Users should document these activities and consider temporary exclusions during development phases.
- Automated scripts or workflows that interact with keychain data for legitimate purposes could be mistaken for malicious activity. Users should ensure these scripts are well-documented and consider adding them to an allowlist if they are frequently used.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, specifically those involving the "dump-keychain" command, to halt ongoing credential theft attempts.
- Conduct a thorough review of the system's keychain access logs to identify any unauthorized access or export of credentials and determine the scope of the compromise.
- Change all credentials stored in the keychain, including passwords for Wi-Fi, websites, and any other services, to mitigate the risk of unauthorized access using stolen credentials.
- Restore the system from a known good backup if any unauthorized changes or malware are detected, ensuring that the backup predates the compromise.
- Escalate the incident to the security operations team for further investigation and to assess whether additional systems may be affected.
- Implement enhanced monitoring and alerting for similar suspicious activities, focusing on keychain access and command-line arguments related to credential dumping, to prevent future incidents.
