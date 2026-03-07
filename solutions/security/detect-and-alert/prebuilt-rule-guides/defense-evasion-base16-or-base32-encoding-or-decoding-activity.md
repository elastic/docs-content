---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Base16 or Base32 Encoding/Decoding Activity" prebuilt detection rule.
---

# Base16 or Base32 Encoding/Decoding Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Base16 or Base32 Encoding/Decoding Activity

Base16 and Base32 are encoding schemes used to convert binary data into text, facilitating data transmission and storage. Adversaries exploit these encodings to obfuscate malicious payloads, evading detection by security systems. The detection rule identifies suspicious encoding/decoding activities on Linux systems by monitoring specific processes and actions, excluding benign uses like help or version checks.

### Possible investigation steps

- Review the process name and arguments to confirm if the activity is related to encoding/decoding using base16 or base32, ensuring it is not a benign use case like help or version checks.
- Examine the user account associated with the process to determine if the activity aligns with their typical behavior or if it appears suspicious.
- Check the parent process of the encoding/decoding activity to identify if it was initiated by a legitimate application or a potentially malicious script or program.
- Investigate the timing and frequency of the encoding/decoding events to assess if they coincide with other suspicious activities or known attack patterns.
- Correlate the event with network activity logs to see if there is any data exfiltration attempt or communication with known malicious IP addresses or domains.
- Look into any recent changes or anomalies in the system that might indicate a compromise, such as unauthorized file modifications or new user accounts.

### False positive analysis

- Routine administrative tasks may trigger the rule if administrators use base16 or base32 commands for legitimate data encoding or decoding. To manage this, create exceptions for specific user accounts or scripts known to perform these tasks regularly.
- Automated backup or data transfer processes might use base16 or base32 encoding as part of their operations. Identify these processes and exclude them by specifying their unique process arguments or execution paths.
- Development and testing environments often involve encoding and decoding operations for debugging or data manipulation. Exclude these environments by filtering based on hostnames or IP addresses associated with non-production systems.
- Security tools or scripts that perform regular encoding checks for data integrity or compliance purposes can also trigger false positives. Whitelist these tools by their process names or execution contexts to prevent unnecessary alerts.
- Educational or research activities involving encoding techniques may inadvertently match the rule criteria. Consider excluding known educational user groups or specific research project identifiers to reduce false positives.

### Response and remediation

- Isolate the affected system from the network to prevent potential lateral movement or data exfiltration by the adversary.
- Terminate any suspicious processes identified by the detection rule, specifically those involving base16 or base32 encoding/decoding without benign arguments.
- Conduct a thorough review of recent system logs and process execution history to identify any additional suspicious activities or related processes.
- Remove any malicious files or payloads that have been identified as part of the encoding/decoding activity.
- Restore any affected files or systems from known good backups to ensure system integrity and data accuracy.
- Update and patch the affected system to close any vulnerabilities that may have been exploited by the adversary.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
