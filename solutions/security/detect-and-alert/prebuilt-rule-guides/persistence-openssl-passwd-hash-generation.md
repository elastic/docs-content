---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "OpenSSL Password Hash Generation" prebuilt detection rule.
---

# OpenSSL Password Hash Generation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating OpenSSL Password Hash Generation

OpenSSL is a robust cryptographic toolkit used for secure communications and data protection, including generating password hashes. Adversaries may exploit OpenSSL to create hashes for unauthorized user accounts or modify existing ones, aiding in persistent access to Linux systems. The detection rule identifies suspicious OpenSSL executions by monitoring specific process actions and arguments, flagging potential misuse for further investigation.

### Possible investigation steps

- Review the process execution details to confirm the presence of the "openssl" command with the "passwd" argument, as this indicates an attempt to generate a password hash.
- Identify the user account associated with the process execution to determine if the action was performed by a legitimate user or a potential adversary.
- Check the system logs and user activity around the time of the alert to identify any suspicious behavior or unauthorized access attempts.
- Investigate any recent changes to user accounts on the system, focusing on new account creations or password modifications that coincide with the alert.
- Correlate the alert with other security events or alerts from the same host to identify patterns or additional indicators of compromise.
- Assess the risk and impact of the detected activity by considering the context of the system and its role within the organization, as well as any potential data exposure or system access implications.

### False positive analysis

- Routine administrative tasks may trigger the rule when system administrators use OpenSSL to generate password hashes for legitimate user account management. To handle this, create exceptions for specific administrator accounts or processes that are known to perform these tasks regularly.
- Automated scripts for user account provisioning or maintenance that utilize OpenSSL for password hashing can also cause false positives. Identify these scripts and exclude their execution paths or associated user accounts from the rule.
- Security tools or compliance checks that periodically verify password strength or integrity using OpenSSL might be flagged. Review these tools and whitelist their operations to prevent unnecessary alerts.
- Development environments where OpenSSL is used for testing password hashing functions can generate alerts. Exclude these environments or specific test accounts from monitoring to reduce noise.
- Scheduled tasks or cron jobs that involve OpenSSL for password management purposes should be identified and excluded if they are part of regular system operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious OpenSSL processes identified by the detection rule to halt ongoing unauthorized password hash generation.
- Conduct a thorough review of user accounts on the affected system to identify any unauthorized accounts or changes to existing accounts, and revert any unauthorized modifications.
- Change passwords for all user accounts on the affected system, especially those with elevated privileges, to ensure that any compromised credentials are no longer valid.
- Implement additional monitoring on the affected system to detect any further unauthorized use of OpenSSL or similar tools, focusing on process execution and command-line arguments.
- Escalate the incident to the security operations team for a comprehensive investigation to determine the root cause and scope of the breach, and to assess potential impacts on other systems.
- Review and update access controls and authentication mechanisms to enhance security and prevent similar incidents in the future, ensuring that only authorized users can perform sensitive operations.
