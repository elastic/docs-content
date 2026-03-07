---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "SystemKey Access via Command Line" prebuilt detection rule.
---

# SystemKey Access via Command Line

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating SystemKey Access via Command Line

macOS keychains securely store user credentials, including passwords and certificates. Adversaries may exploit command-line access to extract keychain data, gaining unauthorized credentials. The detection rule identifies suspicious process activities targeting SystemKey paths, excluding legitimate security processes, to flag potential credential theft attempts.

### Possible investigation steps

- Review the process details to identify the executable that attempted to access the SystemKey paths, focusing on the process.args field to confirm the presence of "/private/var/db/SystemKey" or "/var/db/SystemKey".
- Investigate the parent process using process.Ext.effective_parent.executable to determine if the process chain is suspicious or if it might be a legitimate process that was not excluded by the rule.
- Check the timestamp of the event to correlate with other system activities or user actions that might explain the access attempt.
- Analyze the user account associated with the process to determine if it aligns with expected behavior or if it might indicate a compromised account.
- Review recent system logs and security alerts for any other unusual activities or patterns that might suggest a broader compromise or targeted attack.
- If possible, conduct a forensic analysis of the system to identify any unauthorized changes or additional indicators of compromise related to credential theft.

### False positive analysis

- Security software updates or scans may trigger the rule by accessing SystemKey paths. Users can create exceptions for known security applications that frequently access these paths, ensuring they are not flagged as threats.
- System maintenance scripts or backup processes might access SystemKey paths as part of routine operations. Identify these processes and add them to an exclusion list to prevent false alerts.
- Administrative tools used by IT departments for legitimate credential management could be mistakenly flagged. Verify these tools and configure the rule to exclude them from detection.
- Custom scripts developed for internal use that interact with keychain data should be reviewed and, if deemed safe, added to the list of exceptions to avoid unnecessary alerts.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule that are accessing the SystemKey paths, ensuring no further credential extraction occurs.
- Conduct a thorough review of the system's keychain access logs to identify any unauthorized access attempts and determine the scope of the compromise.
- Change all credentials stored in the keychain that may have been accessed, including Wi-Fi passwords, website credentials, and any other sensitive information.
- Restore the system from a known good backup if unauthorized changes or persistent threats are detected, ensuring the system is free from compromise.
- Implement additional monitoring on the affected system and similar endpoints to detect any further attempts to access keychain data, using enhanced logging and alerting mechanisms.
- Escalate the incident to the security operations team for further investigation and to assess the need for broader organizational response measures, such as notifying affected users or stakeholders.
