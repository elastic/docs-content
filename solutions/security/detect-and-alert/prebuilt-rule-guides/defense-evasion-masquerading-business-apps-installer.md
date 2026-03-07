---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Masquerading as Business App Installer" prebuilt detection rule.
---

# Potential Masquerading as Business App Installer

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Masquerading as Business App Installer

Business applications are integral to productivity, often downloaded and installed by users. Adversaries exploit this by creating malicious executables with names mimicking legitimate apps, tricking users into installing them. The detection rule identifies such threats by checking for unsigned executables in download directories, ensuring they don't masquerade as trusted applications.

### Possible investigation steps

- Review the process name and executable path to confirm if it matches any known legitimate business application names listed in the rule, such as Slack, WebEx, or Teams, and verify if it was executed from a typical download directory.
- Check the process code signature status and subject name to determine if the executable is unsigned or signed by an untrusted entity, which could indicate a masquerading attempt.
- Investigate the source of the download by examining browser history, email attachments, or any recent file transfers to identify potential phishing attempts or malicious download sources.
- Analyze the process execution context, including parent processes and command-line arguments, to understand how the executable was launched and if it aligns with typical user behavior.
- Look for any network connections initiated by the process to identify suspicious outbound traffic or connections to known malicious IP addresses or domains.
- Cross-reference the executable's hash with threat intelligence databases to check for known malware signatures or previous reports of malicious activity.
- If the executable is determined to be suspicious, isolate the affected system and perform a full malware scan to prevent further compromise.

### False positive analysis

- Unsigned executables from legitimate developers may trigger alerts if they are not properly signed or if the signature is not recognized. Users can create exceptions for specific executables by verifying the developer's authenticity and adding them to a trusted list.
- Custom or in-house developed applications that mimic business app names but are unsigned can cause false positives. Organizations should ensure these applications are signed with a trusted certificate or add them to an exclusion list after verifying their safety.
- Software updates or beta versions of legitimate applications might not have updated signatures, leading to false positives. Users should verify the source of the update and, if legitimate, temporarily exclude these versions from the rule.
- Applications installed in non-standard directories that match the naming patterns but are legitimate can be excluded by specifying trusted paths or directories in the rule configuration.
- Third-party tools or utilities that integrate with business applications and use similar naming conventions might be flagged. Users should verify these tools and, if safe, add them to an exception list to prevent future alerts.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of the potential threat and to contain any malicious activity.
- Terminate the suspicious process identified by the alert to stop any ongoing malicious actions.
- Quarantine the executable file flagged by the detection rule to prevent execution and further analysis.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or remnants.
- Review and analyze the process execution logs and any related network activity to understand the scope of the intrusion and identify any other potentially compromised systems.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement application whitelisting to prevent unauthorized executables from running, ensuring only trusted and signed applications are allowed to execute.
