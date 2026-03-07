---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Browser Child Process" prebuilt detection rule.
---

# Suspicious Browser Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Browser Child Process

Web browsers are integral to user interaction with the internet, often serving as gateways for adversaries to exploit vulnerabilities. Attackers may execute malicious scripts or commands by spawning child processes from browsers, leveraging scripting languages or command-line tools. The detection rule identifies unusual child processes initiated by browsers on macOS, filtering out known benign activities to highlight potential threats, thus aiding in early threat detection and response.

### Possible investigation steps

- Review the process command line to understand the context of the execution and identify any potentially malicious scripts or commands.
- Check the parent process name to confirm it is one of the specified browsers (e.g., Google Chrome, Safari) and verify if the browser was expected to be running at the time of the alert.
- Investigate the user account associated with the process to determine if the activity aligns with their typical behavior or if the account may have been compromised.
- Examine the network activity around the time of the alert to identify any suspicious connections or data transfers that may indicate further malicious activity.
- Look for any related alerts or logs that might provide additional context or evidence of a broader attack or compromise.
- Assess the risk and impact of the detected activity by considering the severity and risk score provided, and determine if immediate response actions are necessary.

### False positive analysis

- Legitimate software updates or installations may trigger the rule if they use shell scripts or command-line tools. Users can create exceptions for known update paths, such as those related to Microsoft AutoUpdate or Google Chrome installations, to prevent these from being flagged.
- Development or testing activities involving scripting languages like Python or shell scripts may be mistakenly identified as threats. Users should consider excluding specific development directories or command patterns that are frequently used in their workflows.
- Automated scripts or tools that interact with web browsers for legitimate purposes, such as web scraping or data collection, might be detected. Users can whitelist these processes by specifying their command-line arguments or paths to avoid false positives.
- System administration tasks that involve remote management or configuration changes via command-line tools could be misinterpreted as suspicious. Users should identify and exclude these routine administrative commands to reduce unnecessary alerts.
- Browser extensions or plugins that execute scripts for enhanced functionality might trigger the rule. Users should review and whitelist trusted extensions that are known to execute benign scripts.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further malicious activity or lateral movement by the adversary.
- Terminate the suspicious child process identified in the alert to halt any ongoing malicious execution.
- Conduct a thorough review of the browser's recent activity and history to identify any potentially malicious websites or downloads that may have triggered the alert.
- Remove any malicious files or scripts that were executed by the suspicious child process to prevent further exploitation.
- Apply the latest security patches and updates to the affected browser and macOS system to mitigate known vulnerabilities that could be exploited.
- Monitor the system for any signs of persistence mechanisms or additional suspicious activity, ensuring that no backdoors or unauthorized access points remain.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected, ensuring a coordinated response.
