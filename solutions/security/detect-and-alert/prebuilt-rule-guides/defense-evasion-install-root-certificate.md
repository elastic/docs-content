---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Attempt to Install Root Certificate" prebuilt detection rule.
---

# Attempt to Install Root Certificate

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Attempt to Install Root Certificate

Root certificates are pivotal in establishing trust within public key infrastructures, enabling secure communications by verifying the authenticity of digital certificates. Adversaries exploit this by installing unauthorized root certificates on compromised macOS systems, thereby bypassing security warnings and facilitating covert command and control communications. The detection rule identifies such activities by monitoring specific process executions related to certificate management, excluding known legitimate applications, thus highlighting potential malicious attempts to subvert trust controls.

### Possible investigation steps

- Review the process execution details to confirm the presence of the "security" process with the "add-trusted-cert" argument, as this indicates an attempt to add a root certificate.
- Check the parent process of the suspicious activity to ensure it is not one of the known legitimate applications, such as Bitdefender, as specified in the exclusion list.
- Investigate the user account associated with the process execution to determine if it is a legitimate user or potentially compromised.
- Examine recent system logs and network activity for any signs of unauthorized access or communication with known malicious command and control servers.
- Assess the system for any other indicators of compromise or unusual behavior that may suggest further malicious activity beyond the root certificate installation attempt.

### False positive analysis

- Security software installations or updates may trigger the rule as they often involve legitimate root certificate installations. Users can handle this by adding exceptions for known security software paths, such as Bitdefender, to prevent unnecessary alerts.
- System administrators performing routine maintenance or updates might install root certificates as part of their tasks. To mitigate this, create exceptions for processes executed by trusted admin accounts or during scheduled maintenance windows.
- Some enterprise applications may require the installation of root certificates for internal communications. Identify these applications and exclude their processes from the rule to avoid false positives.
- Development environments on macOS systems might involve testing with self-signed certificates, which could trigger the rule. Developers can be instructed to use designated test environments or have their processes excluded during development phases.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized communications and potential data exfiltration.
- Revoke any unauthorized root certificates installed on the system by accessing the Keychain Access application and removing the suspicious certificates from the System Roots keychain.
- Conduct a thorough review of system logs and process execution history to identify any additional unauthorized changes or suspicious activities that may have occurred alongside the root certificate installation.
- Restore the system to a known good state using backups or system snapshots taken prior to the compromise, ensuring that any malicious changes are reverted.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if other systems in the network may be affected.
- Implement enhanced monitoring and alerting for similar activities by refining detection capabilities to include additional indicators of compromise (IOCs) related to unauthorized certificate installations.
- Review and update security policies and configurations to prevent unauthorized certificate installations, such as enforcing stricter access controls and requiring administrative approval for certificate management actions.
