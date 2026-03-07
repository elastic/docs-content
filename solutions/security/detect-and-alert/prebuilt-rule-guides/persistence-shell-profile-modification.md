---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Bash Shell Profile Modification" prebuilt detection rule.
---

# Bash Shell Profile Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Bash Shell Profile Modification

Bash shell profiles, such as `.bash_profile` and `.bashrc`, are scripts that configure user environments upon login. Adversaries exploit these by inserting malicious commands to ensure persistence, executing harmful scripts whenever a user initiates a shell session. The detection rule identifies unauthorized modifications by monitoring file changes and filtering out benign processes, focusing on unusual executables and paths to flag potential threats.

### Possible investigation steps

- Review the alert details to identify the specific file path that was modified, focusing on paths like /home/*/.bash_profile or /home/*/.bashrc.
- Examine the process name and executable that triggered the alert to determine if it is an unusual or unauthorized process, as specified in the query.
- Check the modification timestamp of the affected file to correlate with any known user activity or scheduled tasks.
- Investigate the contents of the modified Bash shell profile file to identify any suspicious or unexpected commands or scripts.
- Cross-reference the user account associated with the modified file to determine if the activity aligns with their typical behavior or if the account may be compromised.
- Look for any related alerts or logs around the same timeframe that might indicate a broader attack or persistence mechanism.

### False positive analysis

- Frequent use of text editors like vim or nano may trigger alerts when users legitimately modify their shell profiles. To mitigate this, consider excluding these processes from the detection rule if they are commonly used in your environment.
- Automated system updates or configuration management tools like dnf or yum might modify shell profiles as part of their operations. Exclude these processes if they are verified as part of routine maintenance.
- Development tools such as git or platform-python may alter shell profiles during setup or updates. If these tools are regularly used, add them to the exclusion list to prevent false positives.
- User-specific applications located in directories like /Applications or /usr/local may be flagged if they modify shell profiles. Verify these applications and exclude their paths if they are trusted and frequently used.
- Consider excluding specific user directories from monitoring if they are known to contain benign scripts that modify shell profiles, ensuring these exclusions are well-documented and reviewed regularly.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes identified in the alert that are not part of the allowed list, such as unauthorized executables modifying shell profiles.
- Restore the modified shell profile files (.bash_profile, .bashrc) from a known good backup to remove any malicious entries.
- Conduct a thorough review of user accounts and permissions on the affected system to ensure no unauthorized access or privilege escalation has occurred.
- Implement file integrity monitoring on critical shell profile files to detect and alert on future unauthorized changes.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Review and update endpoint protection policies to enhance detection capabilities for similar persistence techniques, leveraging MITRE ATT&CK framework references for T1546.
