---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Sudo Hijacking" prebuilt detection rule.
---

# Potential Sudo Hijacking

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Sudo Hijacking

Sudo is a critical utility in Linux environments, allowing users to execute commands with elevated privileges. Adversaries may exploit this by replacing the sudo binary with a malicious version to capture passwords or maintain persistence. The detection rule identifies suspicious creation or renaming of the sudo binary, excluding legitimate package management processes, to flag potential hijacking attempts.

### Possible investigation steps

- Review the file creation or rename event details to confirm the file path is either /usr/bin/sudo or /bin/sudo, as these are critical locations for the sudo binary.
- Check the process executable that triggered the event to ensure it is not part of the legitimate package management processes listed in the query, such as /bin/dpkg or /usr/bin/yum.
- Investigate the user account associated with the event to determine if the activity aligns with their typical behavior or if it appears suspicious.
- Examine the system logs around the time of the event for any unusual activity or errors that might indicate tampering or unauthorized access.
- Verify the integrity of the current sudo binary by comparing its hash with a known good version to detect any unauthorized modifications.
- Assess the system for any additional signs of compromise, such as unexpected network connections or new user accounts, which may indicate broader malicious activity.

### False positive analysis

- Package management processes can trigger false positives when legitimate updates or installations occur. To handle this, ensure that processes like dpkg, rpm, yum, and apt are included in the exclusion list as they are common package managers.
- Custom scripts or automation tools that modify the sudo binary for legitimate reasons may cause alerts. Review these scripts and consider adding their paths to the exclusion list if they are verified as safe.
- Temporary files or directories used during legitimate software installations or updates, such as those in /var/lib/dpkg or /tmp, can lead to false positives. Exclude these paths if they are part of a known and safe process.
- Development or testing environments where sudo binaries are frequently modified for testing purposes might trigger alerts. In such cases, consider excluding these environments from monitoring or adding specific exclusions for known safe modifications.
- Ensure that any process or executable that is known to interact with the sudo binary in a non-malicious way is added to the exclusion list to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the attacker.
- Verify the integrity of the sudo binary by comparing its hash with a known good version from a trusted source. If compromised, replace it with the legitimate binary.
- Conduct a thorough review of system logs and the process execution history to identify any unauthorized changes or suspicious activities related to the sudo binary.
- Reset passwords for all user accounts on the affected system, especially those with elevated privileges, to mitigate potential credential theft.
- Implement additional monitoring on the affected system and similar environments to detect any further attempts to modify critical binaries or escalate privileges.
- Escalate the incident to the security operations team for a comprehensive investigation and to determine if other systems may be affected.
- Review and update access controls and permissions to ensure that only authorized personnel can modify critical system binaries.
