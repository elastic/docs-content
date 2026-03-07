---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Execution via Electron Child Process Node.js Module" prebuilt detection rule.
---

# Execution via Electron Child Process Node.js Module

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Execution via Electron Child Process Node.js Module

Electron applications, built on Node.js, can execute child processes using the `child_process` module, inheriting parent process permissions. Adversaries exploit this to execute unauthorized commands, bypassing security controls. The detection rule identifies suspicious process starts on macOS, focusing on command-line arguments indicative of such abuse, aiding in threat detection and mitigation.

### Possible investigation steps

- Review the process arguments captured in the alert to confirm the presence of suspicious patterns, such as the use of "-e" and the inclusion of "require('child_process')".
- Identify the parent Electron application process to determine if it is a legitimate application or potentially malicious.
- Check the user account associated with the process to assess if it has elevated privileges that could be exploited.
- Investigate the command executed by the child process to understand its purpose and potential impact on the system.
- Correlate the alert with other security events or logs from the same host to identify any related suspicious activities or patterns.
- Examine the network activity of the host around the time of the alert to detect any unauthorized data exfiltration or communication with known malicious IPs.

### False positive analysis

- Legitimate Electron applications may use the child_process module for valid operations, such as launching helper scripts or tools. Users should identify and whitelist these known applications to prevent unnecessary alerts.
- Development environments often execute scripts using child_process during testing or debugging. Exclude processes originating from development directories or environments to reduce false positives.
- Automated build or deployment tools running on macOS might invoke child processes as part of their workflow. Recognize and exclude these tools by their process names or paths.
- Some Electron-based applications might use command-line arguments that match the detection pattern for legitimate reasons. Review and adjust the detection rule to exclude these specific argument patterns when associated with trusted applications.
- Regularly review and update the exclusion list to accommodate new legitimate use cases as they arise, ensuring that the detection rule remains effective without generating excessive false positives.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized command execution and potential lateral movement.
- Terminate any suspicious child processes identified as being spawned by the Electron application to halt any ongoing malicious activity.
- Conduct a thorough review of the Electron application's code and configuration to identify and remove any unauthorized or malicious scripts or modules, particularly those involving the `child_process` module.
- Revoke and reset any credentials or tokens that may have been exposed or compromised due to the unauthorized execution, ensuring that new credentials are distributed securely.
- Apply security patches and updates to the Electron application and underlying Node.js environment to mitigate any known vulnerabilities that could be exploited in a similar manner.
- Enhance monitoring and logging on the affected system and similar environments to detect any future attempts to exploit the `child_process` module, focusing on command-line arguments and process creation events.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems or data have been impacted, ensuring a comprehensive response to the threat.
