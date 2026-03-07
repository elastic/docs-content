---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Data Encryption via OpenSSL Utility" prebuilt detection rule.'
---

# Suspicious Data Encryption via OpenSSL Utility

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Data Encryption via OpenSSL Utility

OpenSSL is a widely-used command-line tool for secure data encryption and decryption. Adversaries may exploit OpenSSL to encrypt files rapidly across systems, aiming to disrupt data availability or demand ransom. The detection rule identifies suspicious OpenSSL usage by monitoring rapid file encryption activities, focusing on specific command patterns and excluding benign operations, thus highlighting potential malicious behavior.

### Possible investigation steps

- Review the process execution details on the host identified by host.id to confirm the presence of the openssl command and its associated arguments, ensuring they match the suspicious pattern specified in the query.
- Examine the user.name associated with the process to determine if the activity aligns with expected behavior for that user or if it indicates potential unauthorized access.
- Investigate the parent process identified by process.parent.entity_id to understand the context in which the openssl command was executed, checking for any unusual or unexpected parent processes.
- Check for any recent file modifications or creations on the host that coincide with the time window of the alert to assess the impact of the encryption activity.
- Look for additional related alerts or logs from the same host or user within a similar timeframe to identify any patterns or further suspicious activities that could indicate a broader attack.

### False positive analysis

- Legitimate batch encryption operations by system administrators or automated scripts may trigger the rule. To handle this, identify and whitelist specific scripts or user accounts that perform regular encryption tasks.
- Backup processes that use OpenSSL for encrypting data before storage can be mistaken for malicious activity. Exclude known backup processes by specifying their parent process names or paths.
- Developers or security teams testing encryption functionalities might inadvertently match the rule's criteria. Create exceptions for development environments or specific user accounts involved in testing.
- Automated data transfer services that encrypt files for secure transmission could be flagged. Identify these services and exclude their associated processes or user accounts from the rule.
- Regularly review and update the exclusion list to ensure it reflects current operational practices and does not inadvertently allow malicious activities.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further spread of the encryption activity and potential lateral movement by the adversary.
- Terminate any suspicious OpenSSL processes identified on the host to halt ongoing encryption activities.
- Conduct a forensic analysis of the affected host to identify the scope of the encryption, including which files were encrypted and any potential data exfiltration.
- Restore encrypted files from the most recent clean backup to ensure data availability and integrity, ensuring that the backup is free from any malicious alterations.
- Change all credentials and keys that may have been exposed or used on the affected host to prevent unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are compromised.
- Implement enhanced monitoring and logging for OpenSSL usage across the network to detect and respond to similar threats more effectively in the future.
