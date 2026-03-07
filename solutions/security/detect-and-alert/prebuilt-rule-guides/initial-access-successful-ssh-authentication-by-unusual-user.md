---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Successful SSH Authentication from Unusual User" prebuilt detection rule.'
---

# Successful SSH Authentication from Unusual User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Successful SSH Authentication from Unusual User

SSH (Secure Shell) is a protocol used to securely access and manage Linux systems. Adversaries may exploit valid user accounts to gain unauthorized access, bypassing traditional security measures. The detection rule identifies unusual SSH logins by flagging users who haven't logged in for over 10 days, indicating potential misuse of credentials. This proactive approach helps in early detection of unauthorized access attempts.

### Possible investigation steps

- Review the specific user account involved in the alert to determine if the login is expected or authorized, considering the user's typical login patterns and responsibilities.
- Check the source IP address of the SSH login to see if it is recognized or associated with previous legitimate access, or if it appears unusual or suspicious.
- Analyze the timing of the login event to see if it coincides with any known maintenance windows or scheduled activities that could explain the access.
- Investigate any recent changes to the user's account, such as password resets or modifications to permissions, that could indicate potential compromise.
- Correlate the SSH login event with other logs or alerts from the same timeframe to identify any additional suspicious activities or patterns that could suggest a broader security incident.

### False positive analysis

- Users returning from extended leave or vacation may trigger the rule. To manage this, create exceptions for users with known absence periods.
- System administrators or service accounts that log in infrequently for maintenance tasks can be excluded by identifying and documenting these accounts.
- Automated scripts or processes that authenticate sporadically might be flagged. Review and whitelist these processes if they are legitimate and necessary for operations.
- Temporary contractors or consultants with limited access periods may cause alerts. Ensure their access is documented and create exceptions for their accounts during their engagement period.
- Accounts used for testing or development purposes that are not regularly active can be excluded by maintaining a list of such accounts and updating it as needed.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the attacker.
- Terminate the active SSH session associated with the unusual login to cut off the attacker's access.
- Reset the password for the compromised user account and any other accounts that may have been accessed using the same credentials.
- Conduct a thorough review of the affected system's logs and configurations to identify any unauthorized changes or additional compromised accounts.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems or accounts have been affected.
- Implement multi-factor authentication (MFA) for SSH access to enhance security and prevent similar unauthorized access attempts in the future.
- Update and enhance monitoring rules to detect similar unusual login patterns, ensuring early detection of potential threats.
