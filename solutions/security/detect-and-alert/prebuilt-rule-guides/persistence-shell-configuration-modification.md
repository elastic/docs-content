---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Shell Configuration Creation" prebuilt detection rule.
---

# Shell Configuration Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Shell Configuration Creation

Shell configuration files in Unix-like systems are crucial for setting up user environments by defining variables, aliases, and startup scripts. Adversaries exploit these files to execute malicious code persistently. The detection rule identifies suspicious creation or modification of these files, excluding benign processes, to flag potential threats, aligning with tactics like persistence and event-triggered execution.

### Possible investigation steps

- Review the specific file path involved in the alert to determine if it is a system-wide or user-specific shell configuration file, as listed in the query.
- Identify the process executable that triggered the alert and verify if it is part of the excluded benign processes. If not, investigate the process's origin and purpose.
- Check the creation timestamp of the file to correlate with any known user activities or scheduled tasks that might explain the change.
- Examine the contents of the newly created shell configuration file for any suspicious or unauthorized entries, such as unexpected scripts or commands.
- Investigate the user account associated with the file creation to determine if the activity aligns with their typical behavior or if the account may have been compromised.
- Cross-reference the alert with other security logs or alerts to identify any related suspicious activities or patterns that could indicate a broader attack campaign.

### False positive analysis

- System package managers like dpkg, rpm, and yum often modify shell configuration files during software installations or updates. To handle these, exclude processes with executables such as /bin/dpkg or /usr/bin/rpm from triggering alerts.
- Automated system management tools like Puppet and Chef may alter shell configuration files as part of their routine operations. Exclude these processes by adding exceptions for executables like /opt/puppetlabs/puppet/bin/puppet or /usr/bin/chef-client.
- User account management activities, such as adding new users, can lead to shell configuration file modifications. Exclude processes like /usr/sbin/adduser or /sbin/useradd to prevent false positives in these scenarios.
- Temporary files created by text editors (e.g., .swp files) during editing sessions can trigger alerts. Exclude file extensions such as swp, swpx, and swx to avoid these false positives.
- Virtualization and containerization tools like Docker and Podman may modify shell configuration files as part of their operations. Exclude executables like /usr/bin/dockerd or /usr/bin/podman to manage these cases.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Review the modified or newly created shell configuration files to identify and remove any unauthorized or malicious code.
- Restore the affected shell configuration files from a known good backup to ensure the system's environment is clean and secure.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malware or persistence mechanisms.
- Monitor the system and network for any signs of re-infection or related suspicious activity, focusing on the indicators of compromise (IOCs) associated with the Kaiji malware family.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
- Implement additional monitoring and alerting for changes to shell configuration files to enhance detection of similar threats in the future.
