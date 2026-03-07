---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Sudoers File Activity" prebuilt detection rule.
---

# Sudoers File Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Sudoers File Activity

The sudoers file is crucial in Unix-like systems, defining user permissions for executing commands with elevated privileges. Adversaries may exploit this by altering the file to gain unauthorized access or escalate privileges. The detection rule identifies suspicious changes to the sudoers file, excluding legitimate processes, to flag potential privilege escalation attempts.

### Possible investigation steps

- Review the alert details to identify the specific file path that triggered the alert, focusing on /etc/sudoers* or /private/etc/sudoers*.
- Examine the process information associated with the change event, particularly the process.name and process.executable fields, to determine if the modification was made by a suspicious or unauthorized process.
- Check the user account associated with the process that made the change to the sudoers file to assess if the account has a legitimate reason to modify the file.
- Investigate recent login activity and user behavior for the account involved in the modification to identify any anomalies or signs of compromise.
- Review system logs around the time of the alert to gather additional context on what other activities occurred on the system, which might indicate a broader attack or compromise.
- Assess the current state of the sudoers file to identify any unauthorized or suspicious entries that could indicate privilege escalation attempts.

### False positive analysis

- System updates and package installations can trigger changes to the sudoers file. Exclude processes like dpkg, yum, dnf, and platform-python from triggering alerts as they are commonly involved in legitimate updates.
- Configuration management tools such as Puppet and Chef may modify the sudoers file as part of their normal operations. Exclude process executables like /opt/chef/embedded/bin/ruby and /opt/puppetlabs/puppet/bin/ruby to prevent false positives.
- Docker daemon processes might interact with the sudoers file during container operations. Exclude /usr/bin/dockerd to avoid unnecessary alerts related to Docker activities.
- Regularly review and update the exclusion list to ensure it reflects the current environment and operational tools, minimizing false positives while maintaining security vigilance.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or privilege escalation.
- Review the recent changes to the sudoers file to identify unauthorized modifications and revert them to the last known good configuration.
- Conduct a thorough examination of system logs to identify any unauthorized access or actions performed using elevated privileges, focusing on the time frame of the detected change.
- Reset passwords and review access permissions for all users with sudo privileges to ensure no unauthorized accounts have been added or existing accounts have been compromised.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems have been affected.
- Implement additional monitoring on the affected system and similar systems to detect any further attempts to modify the sudoers file or other privilege escalation activities.
- Review and update security policies and configurations to prevent similar incidents, ensuring that only authorized processes can modify the sudoers file.
