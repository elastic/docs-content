---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Privacy Control Bypass via Localhost Secure Copy" prebuilt detection rule.
---

# Potential Privacy Control Bypass via Localhost Secure Copy

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Privacy Control Bypass via Localhost Secure Copy

Secure Copy Protocol (SCP) is used for secure file transfers over SSH. On macOS, SSH daemon inclusion in the Full Disk Access list can be exploited to bypass privacy controls. Adversaries may misuse SCP to locally copy files, evading security measures. The detection rule identifies such activity by monitoring SCP commands targeting localhost, excluding benign uses like Vagrant, to flag potential privacy control bypass attempts.

### Possible investigation steps

- Review the process details to confirm the presence of SCP commands targeting localhost or 127.0.0.1, as indicated by the process.command_line field.
- Check the process.args field for the presence of "StrictHostKeyChecking=no" to verify if the SCP command was executed with potentially insecure settings.
- Investigate the user account associated with the SCP command to determine if it is a legitimate user or potentially compromised.
- Examine the timing and frequency of the SCP command execution to identify any unusual patterns or repeated attempts that may indicate malicious activity.
- Cross-reference the alert with other security logs or alerts to identify any related suspicious activities or anomalies around the same timeframe.
- Assess the system for any unauthorized changes or access to sensitive files that may have occurred as a result of the SCP command execution.

### False positive analysis

- Vagrant usage can trigger false positives due to its legitimate use of SCP for local file transfers. To mitigate this, ensure that Vagrant-related SCP commands are excluded by refining the detection rule to ignore processes with arguments containing "vagrant@*127.0.0.1*".
- Development and testing environments may frequently use SCP to localhost for legitimate purposes. Consider creating exceptions for known development tools or scripts that regularly perform these actions to reduce noise.
- Automated backup solutions might use SCP to copy files locally as part of their routine operations. Identify and whitelist these processes to prevent them from being flagged as potential threats.
- System administrators may use SCP for local file management tasks. Establish a list of trusted administrator accounts or specific command patterns that can be safely excluded from triggering alerts.
- Continuous integration and deployment pipelines might involve SCP commands to localhost. Review and exclude these processes if they are part of a controlled and secure workflow.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious SCP processes identified in the alert to halt ongoing unauthorized file transfers.
- Conduct a thorough review of the system's Full Disk Access list to identify and remove any unauthorized applications, including the SSH daemon if it was added without proper authorization.
- Analyze the system's SSH configuration and logs to identify any unauthorized changes or access patterns, and revert any suspicious modifications.
- Reset credentials for any accounts that may have been compromised, focusing on those with SSH access, and enforce the use of strong, unique passwords.
- Implement network monitoring to detect and alert on any future SCP commands targeting localhost, especially those bypassing host key checks.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on sensitive data, ensuring compliance with organizational incident response protocols.
