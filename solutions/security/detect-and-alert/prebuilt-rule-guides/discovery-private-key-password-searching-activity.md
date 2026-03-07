---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Private Key Searching Activity" prebuilt detection rule.
---

# Private Key Searching Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Private Key Searching Activity

In Linux environments, private keys are crucial for secure communications and authentication. Adversaries may exploit this by searching for private keys to gain unauthorized access or escalate privileges. The detection rule identifies suspicious use of the 'find' command targeting key files in sensitive directories, signaling potential malicious intent. This proactive monitoring helps mitigate risks associated with unauthorized key access.

### Possible investigation steps

- Review the process details to confirm the 'find' command was executed with parameters targeting private key files, as indicated by the command line containing patterns like "*id_dsa*", "*id_rsa*", etc., and directories such as "/home/", "/etc/ssh", or "/root/".
- Identify the user account associated with the process to determine if the activity aligns with expected behavior for that user or if it suggests potential compromise.
- Check the process's parent process to understand the context in which the 'find' command was executed, which may provide insights into whether this was part of a legitimate script or an unauthorized action.
- Investigate any recent login activity or changes in user privileges for the account involved to assess if there has been any unauthorized access or privilege escalation.
- Examine system logs and other security alerts around the time of the event to identify any correlated suspicious activities or anomalies that might indicate a broader attack campaign.

### False positive analysis

- System administrators or automated scripts may use the 'find' command to locate private keys for legitimate maintenance tasks. To handle this, create exceptions for known administrative accounts or scripts that regularly perform these actions.
- Backup processes might search for private keys as part of routine data protection activities. Identify and exclude these processes by specifying their unique command-line patterns or process IDs.
- Security audits or compliance checks often involve scanning for private keys to ensure proper security measures are in place. Exclude these activities by recognizing the specific tools or scripts used during audits.
- Developers or DevOps teams may search for private keys during application deployment or configuration. Establish a list of trusted users or processes involved in these operations and exclude them from triggering alerts.
- Automated configuration management tools like Ansible or Puppet might search for keys as part of their operations. Identify these tools and exclude their specific command-line patterns to prevent false positives.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, particularly those involving the 'find' command searching for private keys.
- Conduct a thorough review of access logs and process execution history to identify any unauthorized access or privilege escalation attempts.
- Change all potentially compromised private keys and associated credentials, ensuring new keys are securely generated and stored.
- Implement stricter access controls and permissions on directories containing private keys to limit exposure to unauthorized users.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Enhance monitoring and alerting for similar activities by ensuring that detection rules are tuned to capture variations of the 'find' command targeting sensitive files.
