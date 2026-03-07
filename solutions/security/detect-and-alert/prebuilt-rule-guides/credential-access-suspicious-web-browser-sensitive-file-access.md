---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Web Browser Sensitive File Access" prebuilt detection rule.'
---

# Suspicious Web Browser Sensitive File Access

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Web Browser Sensitive File Access

Web browsers store sensitive data like cookies and login credentials in specific files. Adversaries exploit this by accessing these files using untrusted or unsigned processes, potentially stealing credentials. The detection rule identifies such unauthorized access on macOS by monitoring file access events, focusing on untrusted processes or scripts, and excluding known safe executables, thus flagging potential credential theft attempts.

### Possible investigation steps

- Review the process executable path and name to determine if it is a known legitimate application or script, focusing on those not signed by trusted entities or identified as osascript.
- Check the process code signature details to verify if the process is unsigned or untrusted, which could indicate malicious activity.
- Investigate the user account associated with the process to determine if there is any unusual or unauthorized activity, such as unexpected logins or privilege escalations.
- Examine the file access event details, including the specific sensitive file accessed (e.g., cookies.sqlite, logins.json), to assess the potential impact on credential security.
- Correlate the event with other security alerts or logs from the same host or user to identify any patterns or additional suspicious activities that might indicate a broader compromise.
- Verify if the process executable path matches any known safe paths, such as the excluded path for the Elastic Endpoint, to rule out false positives.

### False positive analysis

- Access by legitimate applications: Some legitimate applications may access browser files for valid reasons, such as backup or synchronization tools. Users can create exceptions for these applications by adding their code signatures to the exclusion list.
- Developer or testing scripts: Developers might use scripts like osascript for testing purposes, which could trigger the rule. To manage this, users can whitelist specific scripts or processes used in development environments.
- Security software interactions: Security tools might access browser files as part of their scanning or monitoring activities. Users should verify the legitimacy of these tools and add them to the exclusion list if they are trusted.
- System maintenance tasks: Automated system maintenance tasks might access browser files. Users can identify these tasks and exclude them if they are part of routine system operations and deemed safe.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any untrusted or unsigned processes identified in the alert, especially those accessing sensitive browser files.
- Conduct a thorough review of the affected system's recent activity logs to identify any additional suspicious behavior or potential lateral movement.
- Change all potentially compromised credentials, focusing on those stored in the affected web browsers, and enforce multi-factor authentication where possible.
- Restore any altered or deleted sensitive files from a known good backup to ensure data integrity.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Update endpoint protection and monitoring tools to enhance detection capabilities for similar unauthorized access attempts in the future.
