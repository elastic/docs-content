---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Linux User Account Credential Modification" prebuilt detection rule.'
---

# Linux User Account Credential Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Linux User Account Credential Modification

In Linux environments, user account credentials are crucial for system access and management. Adversaries may exploit command-line utilities to modify credentials, often using scripts to automate this process post-infection. The detection rule identifies suspicious use of shell commands that echo passwords into the passwd utility, a technique indicative of unauthorized credential changes, by monitoring specific command patterns and excluding benign processes.

### Possible investigation steps

- Review the process command line to confirm the presence of the suspicious pattern "*echo*passwd*" and assess if it aligns with known malicious activity.
- Identify the user account associated with the process to determine if it is a legitimate user or potentially compromised.
- Examine the parent process details, including the command line and executable path, to understand the context of how the suspicious process was initiated.
- Check for any recent changes to user accounts on the system, focusing on password modifications or new account creations around the time of the alert.
- Investigate the system for any additional signs of compromise, such as unexpected network connections or other suspicious processes running concurrently.
- Correlate the event with other security alerts or logs to identify if this activity is part of a broader attack pattern or campaign.

### False positive analysis

- Automated build processes may trigger this rule if they use shell scripts that include echoing passwords for testing or configuration purposes. To handle this, exclude processes with parent command lines or executables related to build tools like make.
- System administration scripts that automate user account management might use similar command patterns. Review these scripts and exclude them by specifying their parent process or executable paths.
- Custom user scripts for password management could inadvertently match the rule's criteria. Identify these scripts and add exceptions based on their unique command line or parent process attributes.
- Some legitimate software installations might use echo and passwd in their setup scripts. Monitor installation logs and exclude known safe installation processes by their parent command line or executable.

### Response and remediation

- Immediately isolate the affected Linux system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule, particularly those involving the echo command being used with the passwd utility.
- Change the passwords of any user accounts that may have been compromised, ensuring the use of strong, unique passwords.
- Review and audit recent user account changes and access logs to identify any unauthorized modifications or access attempts.
- Restore any affected user accounts to their previous state using backups or system snapshots, if available.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement additional monitoring and alerting for similar command patterns to enhance detection and prevent recurrence of this threat.
