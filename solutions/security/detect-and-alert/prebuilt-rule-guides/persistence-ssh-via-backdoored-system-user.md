---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Login via System User" prebuilt detection rule.
---

# Unusual Login via System User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Login via System User

In Linux environments, system users typically have restricted login capabilities to prevent unauthorized access. These accounts, often set with `nologin`, are not meant for interactive sessions. Adversaries may exploit these accounts by altering their configurations to enable SSH access, thus bypassing standard security measures. The detection rule identifies successful logins by these uncommon system users, flagging potential unauthorized access attempts for further investigation.

### Possible investigation steps

- Review the login event details to identify the specific system user account involved in the successful login, focusing on the user.name field.
- Check the system logs for any recent changes to the user account's configuration, particularly modifications that might have enabled SSH access for accounts typically set with nologin.
- Investigate the source IP address associated with the login event to determine if it is known or suspicious, and assess whether it aligns with expected access patterns.
- Examine the timeline of events leading up to and following the login to identify any unusual activities or patterns that could indicate malicious behavior.
- Verify if there are any other successful login attempts from the same source IP or involving other system user accounts, which could suggest a broader compromise.
- Consult with system administrators to confirm whether any legitimate changes were made to the system user account's login capabilities and document any authorized modifications.

### False positive analysis

- System maintenance tasks may require temporary login access for system users. Verify if the login corresponds with scheduled maintenance and consider excluding these events during known maintenance windows.
- Automated scripts or services might use system accounts for legitimate purposes. Identify these scripts and whitelist their associated activities to prevent false alerts.
- Some system users might be configured for specific applications that require login capabilities. Review application requirements and exclude these users if their access is deemed necessary and secure.
- In environments with custom configurations, certain system users might be intentionally modified for operational needs. Document these changes and adjust the detection rule to exclude these known modifications.
- Regularly review and update the list of system users in the detection rule to ensure it reflects the current environment and operational requirements, minimizing unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any active sessions associated with the unusual system user accounts identified in the alert to disrupt ongoing unauthorized access.
- Review and revert any unauthorized changes to the system user accounts, such as modifications to the shell configuration that enabled login capabilities.
- Conduct a thorough audit of the system for any additional unauthorized changes or backdoors, focusing on SSH configurations and user account settings.
- Reset passwords and update authentication mechanisms for all system user accounts to prevent further exploitation.
- Implement additional monitoring and alerting for any future login attempts by system users, ensuring rapid detection and response to similar threats.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
