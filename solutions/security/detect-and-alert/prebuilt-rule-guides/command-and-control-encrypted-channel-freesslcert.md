---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Connection to Commonly Abused Free SSL Certificate Providers" prebuilt detection rule.
---

# Connection to Commonly Abused Free SSL Certificate Providers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Connection to Commonly Abused Free SSL Certificate Providers

Free SSL certificates, like those from Let's Encrypt, enable secure web traffic encryption. Adversaries exploit these to mask malicious command and control (C2) communications. The detection rule identifies unusual Windows processes accessing domains with such certificates, excluding common false positives, to flag potential misuse of encrypted channels for C2 activities.

### Possible investigation steps

- Review the process executable path to confirm if it is a native Windows process and assess the legitimacy of its network activity. Focus on paths like "C:\Windows\System32\*.exe" and "C:\Windows\SysWOW64\*.exe".
- Investigate the specific domain accessed by the process, such as those ending in "*.letsencrypt.org" or "*.sslforfree.com", to determine if it is associated with known malicious activity or if it is a legitimate service.
- Check the process name against the list of excluded false positives, ensuring it is not "svchost.exe", "MicrosoftEdge*.exe", or "msedge.exe", which are common and typically benign.
- Analyze the network traffic associated with the process to identify any unusual patterns or anomalies that could indicate command and control activity.
- Correlate the alert with other security events or logs from the same host to identify any additional indicators of compromise or related suspicious activities.

### False positive analysis

- Windows system processes like svchost.exe and MicrosoftEdge.exe are common false positives due to their legitimate network activities. These can be excluded from the detection rule to reduce noise.
- Regularly update the list of excluded processes to include any new system processes that are verified to have legitimate reasons for accessing domains with free SSL certificates.
- Monitor and analyze network traffic patterns to identify any additional processes that consistently generate false positives, and consider adding them to the exclusion list if they are deemed non-threatening.
- Use process whitelisting to allow known safe applications that frequently access these domains, ensuring they do not trigger alerts unnecessarily.
- Implement a review process to periodically reassess the exclusion list, ensuring it remains relevant and does not inadvertently allow malicious activities to go undetected.

### Response and remediation

- Isolate the affected system from the network to prevent further malicious communication and potential lateral movement.
- Terminate any suspicious processes identified in the alert that are not typically associated with network activity, such as those running from unusual paths or with unexpected network connections.
- Conduct a thorough review of the system's recent activity logs to identify any unauthorized changes or additional indicators of compromise.
- Remove any malicious files or executables found on the system, ensuring that all remnants of the threat are eradicated.
- Restore the system from a known good backup if any critical system files or configurations have been altered.
- Update and patch the system to the latest security standards to close any vulnerabilities that may have been exploited.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
