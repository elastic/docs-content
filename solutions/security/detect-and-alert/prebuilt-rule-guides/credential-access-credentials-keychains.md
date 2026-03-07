---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Keychain CommandLine Interaction via Unsigned or Untrusted Process" prebuilt detection rule.'
---

# Keychain CommandLine Interaction via Unsigned or Untrusted Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Keychain CommandLine Interaction via Unsigned or Untrusted Process

macOS keychains securely store user credentials, such as passwords and certificates, essential for system and application authentication. Adversaries may target these directories to extract sensitive information, potentially compromising user accounts and system integrity. The detection rule identifies suspicious access attempts by monitoring process activities related to keychain directories, excluding known legitimate processes and actions, thus highlighting potential unauthorized access attempts.

### Possible investigation steps

- Review the process details that triggered the alert, focusing on the process.args field to identify the specific keychain directory accessed and the nature of the access attempt.
- Examine the process.parent.executable and process.executable fields to determine the origin of the process and assess whether it is a known or potentially malicious application.
- Investigate the process.Ext.effective_parent.executable field to trace the parent process chain and identify any unusual or unauthorized parent processes that may have initiated the access.
- Check for any recent changes or installations on the system that could explain the access attempt, such as new software or updates that might interact with keychain directories.
- Correlate the alert with other security events or logs from the same host to identify any patterns or additional suspicious activities that could indicate a broader compromise.

### False positive analysis

- Processes related to legitimate security applications like Microsoft Defender, JumpCloud Agent, and Rapid7 IR Agent may trigger false positives. Users can mitigate this by ensuring these applications are included in the exclusion list for process executables and effective parent executables.
- Routine administrative tasks involving keychain management, such as setting keychain settings or importing certificates, might be flagged. To handle this, users should add these specific actions to the exclusion list for process arguments.
- Applications like OpenVPN Connect and JAMF management tools that interact with keychain directories for legitimate purposes can cause false alerts. Users should verify these applications are part of the exclusion list for parent executables to prevent unnecessary alerts.
- Regular system maintenance or updates that involve keychain access might be misinterpreted as suspicious. Users should monitor these activities and adjust the exclusion criteria as needed to accommodate known maintenance processes.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule that are attempting to access keychain directories without legitimate reasons.
- Conduct a thorough review of the system's keychain access logs to identify any unauthorized access or modifications to keychain files.
- Change all passwords and credentials stored in the keychain on the affected system to prevent potential misuse of compromised credentials.
- Restore the system from a known good backup if unauthorized access has led to system integrity issues or data corruption.
- Implement additional monitoring on the affected system to detect any further unauthorized access attempts, focusing on the keychain directories and related processes.
- Escalate the incident to the security operations team for further investigation and to determine if the threat is part of a larger attack campaign.
