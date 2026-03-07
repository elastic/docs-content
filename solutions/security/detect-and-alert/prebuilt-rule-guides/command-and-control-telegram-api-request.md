---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Linux Telegram API Request" prebuilt detection rule.
---

# Linux Telegram API Request

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Linux Telegram API Request

Telegram's API allows applications to interact with its messaging platform, often used for legitimate automation and communication tasks. However, adversaries may exploit this by using commands like `curl` or `wget` to communicate with Telegram's API for command and control purposes. The detection rule identifies such suspicious activity by monitoring for these commands accessing the Telegram API, indicating potential misuse.

### Possible investigation steps

- Review the process details to confirm the execution of the curl or wget command with the api.telegram.org domain in the command line, as indicated by the process.command_line field.
- Investigate the user account associated with the process to determine if the activity aligns with expected behavior or if the account may be compromised.
- Check the network activity logs to identify any additional connections to api.telegram.org or other suspicious domains, which may indicate further command and control communication.
- Analyze the parent process of the detected curl or wget command to understand how the process was initiated and if it was triggered by another suspicious activity.
- Examine the system for any other indicators of compromise, such as unusual file modifications or additional unauthorized processes, to assess the scope of potential malicious activity.

### False positive analysis

- Legitimate automation scripts or applications may use curl or wget to interact with Telegram's API for non-malicious purposes. Review the context and purpose of these scripts to determine if they are authorized.
- System administrators or developers might use curl or wget for testing or maintenance tasks involving Telegram's API. Verify if these activities are part of routine operations and consider excluding them if they are deemed safe.
- Monitoring tools or integrations that rely on Telegram for notifications could trigger this rule. Identify these tools and add exceptions for their known processes to prevent unnecessary alerts.
- If a specific user or service account frequently triggers this rule due to legitimate use, consider creating an exception for that account to reduce noise while maintaining security oversight.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further communication with the Telegram API and potential data exfiltration.
- Terminate any suspicious processes identified as using curl or wget to interact with api.telegram.org to halt ongoing malicious activities.
- Conduct a thorough review of the affected system's process logs and network connections to identify any additional indicators of compromise or related malicious activity.
- Remove any unauthorized scripts or binaries that may have been used to automate the interaction with the Telegram API.
- Reset credentials and review access permissions for any accounts that were active on the affected system to prevent unauthorized access.
- Update and patch the affected system to the latest security standards to mitigate vulnerabilities that could be exploited in similar attacks.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.

