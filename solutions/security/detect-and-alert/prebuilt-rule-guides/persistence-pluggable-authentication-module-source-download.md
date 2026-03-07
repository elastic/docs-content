---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Pluggable Authentication Module (PAM) Source Download" prebuilt detection rule.'
---

# Pluggable Authentication Module (PAM) Source Download

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Pluggable Authentication Module (PAM) Source Download

Pluggable Authentication Modules (PAM) are integral to Linux systems, managing authentication tasks. Adversaries may exploit PAM by downloading its source code to insert backdoors, compromising authentication. The detection rule identifies suspicious downloads of PAM source files using tools like `curl` or `wget`, flagging potential threats to system integrity and user credentials.

### Possible investigation steps

- Review the process details to confirm the use of `curl` or `wget` for downloading the PAM source file, focusing on the `process.name` and `process.args` fields to verify the URL pattern matches the suspicious download.
- Check the user account associated with the process execution to determine if the activity was initiated by a legitimate user or a potential adversary.
- Investigate the system's command history and logs to identify any preceding or subsequent commands that might indicate further malicious activity or attempts to compile and install the downloaded PAM source.
- Examine network logs for any unusual outbound connections or data exfiltration attempts following the download, which could suggest further compromise.
- Assess the integrity of existing PAM modules on the system to ensure no unauthorized modifications or backdoors have been introduced.
- Correlate this event with other alerts or anomalies on the same host to identify patterns or a broader attack campaign.

### False positive analysis

- Legitimate system administrators or developers may download PAM source files for testing or development purposes. To handle this, create exceptions for known user accounts or IP addresses that regularly perform such downloads.
- Automated scripts or configuration management tools might use `curl` or `wget` to download PAM source files as part of routine updates or system setups. Identify these scripts and whitelist their activities to prevent false positives.
- Security researchers or auditors may download PAM source files to conduct security assessments. Establish a process to verify and approve these activities, allowing exceptions for recognized research teams or individuals.
- Educational institutions or training environments might download PAM source files for instructional purposes. Implement a policy to exclude these environments from triggering alerts, ensuring they are recognized as non-threatening.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any active `curl` or `wget` processes identified in the alert to stop the download of potentially malicious PAM source files.
- Conduct a thorough review of PAM configuration files and shared object files on the affected system to identify and remove any unauthorized modifications or backdoors.
- Restore the affected system from a known good backup if unauthorized changes to PAM files are detected and cannot be easily reversed.
- Implement stricter access controls and monitoring on systems handling PAM configurations to prevent unauthorized downloads or modifications in the future.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
- Update detection mechanisms to monitor for similar download attempts and unauthorized modifications to critical authentication components.
