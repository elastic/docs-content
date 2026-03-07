---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Execution via FileFix Phishing Attack" prebuilt detection rule.'
---

# Potential Execution via FileFix Phishing Attack

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Execution via FileFix Phishing Attack

### Possible investigation steps

- Review the process command line and arguments to identify any malicious intent.
- Review web activity preceeding the alert to identify the initial vector.
- Investigate any files, network or child process events from the suspected process.
- Correlate the event with other security alerts or logs from the same host or user to identify patterns or additional indicators of compromise.
- Assess the risk and impact of the detected activity by considering the context of the environment, such as the presence of sensitive data or critical systems that might be affected.

### False positive analysis

- Legitimate administrative scripts containing the suspicious keywords such as CAPTCHA.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further spread or communication with potential command and control servers.
- Terminate any suspicious processes identified by the detection rule to halt ongoing malicious activities.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malicious payloads or scripts.
- Review and clean up any unauthorized changes to system configurations or scheduled tasks that may have been altered by the malicious PowerShell activity.
- Restore any affected files or system components from known good backups to ensure system integrity and functionality.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are compromised.
- Implement additional monitoring and logging for PowerShell activities across the network to enhance detection of similar threats in the future.
