---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Installer Package Spawns Network Event" prebuilt detection rule.'
---

# Suspicious Installer Package Spawns Network Event

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Installer Package Spawns Network Event

MacOS installer packages, often with a .pkg extension, are used to distribute software. Adversaries exploit this by embedding scripts to execute additional commands or download malicious payloads. The detection rule identifies suspicious behavior by monitoring for installer packages spawning shell processes followed by network activity, indicating potential malicious activity.

### Possible investigation steps

- Review the process details to identify the parent process name and entity ID, focusing on processes like "installer" or "package_script_service" that initiated the suspicious activity.
- Examine the child process that was spawned, such as "bash", "sh", or "python", to determine the commands executed and assess if they align with typical installation behavior or appear malicious.
- Investigate the network activity associated with the suspicious process, particularly looking at processes like "curl" or "wget", to identify any external connections made and the destination IP addresses or domains.
- Check the timestamp and sequence of events to confirm if the network activity closely followed the process execution, indicating a potential download or data exfiltration attempt.
- Analyze any downloaded files or payloads for malicious content using threat intelligence tools or sandbox environments to determine their intent and potential impact.
- Correlate the findings with known threat actor tactics or campaigns, leveraging threat intelligence sources to assess if the activity matches any known patterns or indicators of compromise.

### False positive analysis

- Legitimate software installations may trigger this rule if they use scripts to configure network settings or download updates. Users can create exceptions for known safe software by whitelisting specific installer package names or hashes.
- System administrators often use scripts to automate software deployment and updates, which might involve network activity. To reduce false positives, exclude processes initiated by trusted administrative tools or scripts.
- Development environments on macOS might execute scripts that connect to the internet for dependencies or updates. Users can mitigate this by excluding processes associated with known development tools or environments.
- Some security tools or monitoring software may use scripts to perform network checks or updates. Identify and exclude these processes if they are verified as non-threatening.
- Frequent updates from trusted software vendors might trigger this rule. Users should maintain an updated list of trusted vendors and exclude their processes from triggering alerts.

### Response and remediation

- Isolate the affected MacOS system from the network immediately to prevent further malicious activity or data exfiltration.
- Terminate any suspicious processes identified in the alert, such as those initiated by the installer package, to halt ongoing malicious actions.
- Conduct a thorough review of the installed applications and remove any unauthorized or suspicious software, especially those with a .pkg extension.
- Restore the system from a known good backup if available, ensuring that the backup predates the installation of the malicious package.
- Update and patch the MacOS system and all installed applications to the latest versions to mitigate vulnerabilities that could be exploited by similar threats.
- Monitor network traffic for any signs of command and control communication or data exfiltration attempts, using the indicators identified in the alert.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
