---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Successful SSH Authentication from Unusual SSH Public Key" prebuilt detection rule.
---

# Successful SSH Authentication from Unusual SSH Public Key

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Successful SSH Authentication from Unusual SSH Public Key

SSH public key authentication is a secure method for accessing Linux systems, relying on cryptographic keys rather than passwords. Adversaries may exploit this by using stolen or unauthorized keys to gain access. The detection rule identifies successful logins using new public keys, unseen in the past 10 days, signaling potential unauthorized access attempts. This helps in early detection of suspicious activities, aligning with threat tactics like Initial Access.

### Possible investigation steps

- Review the specific SSH login event details, focusing on the event.category, event.action, and event.outcome fields to confirm the successful authentication via public key.
- Identify the source IP address and user account associated with the login event to determine if they are known or expected.
- Check the system.auth.ssh.method field to ensure the authentication method was indeed public key and not another method.
- Investigate the history of the public key used for authentication by searching logs for any previous occurrences or related activities within the last 10 days.
- Correlate the event with other security logs or alerts from the same host or user to identify any patterns or additional suspicious activities.
- Assess the risk by considering the context of the login, such as the time of access, the location of the source IP, and any recent changes in user behavior or system configurations.
- If unauthorized access is suspected, initiate incident response procedures, including revoking the public key, notifying affected parties, and conducting a thorough security review of the system.

### False positive analysis

- Frequent logins from known automation scripts or services using rotating SSH keys can trigger false positives. To manage this, identify these services and add their public keys to an exception list.
- Developers or system administrators who regularly update their SSH keys for security reasons may cause alerts. Maintain a record of authorized personnel and their key update schedules to exclude these events.
- Temporary access granted to third-party vendors or contractors might appear as unusual activity. Ensure that any temporary access is documented and keys are added to an exception list during the access period.
- Test environments where SSH keys are frequently generated and used for various testing purposes can lead to false positives. Implement a separate monitoring policy for test environments to reduce noise in production alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Revoke the unauthorized SSH public key from the system's authorized_keys file to block further access using that key.
- Conduct a thorough review of recent login activities and system logs to identify any additional unauthorized access or suspicious activities that may have occurred.
- Change passwords and regenerate SSH keys for all legitimate users on the affected system to ensure no compromised credentials remain in use.
- Notify the security team and relevant stakeholders about the incident for awareness and further investigation.
- Implement additional monitoring on the affected system and related network segments to detect any further suspicious activities or attempts to regain access.
- Review and update access control policies and SSH key management practices to prevent similar incidents in the future, ensuring that only authorized keys are allowed and regularly audited.

