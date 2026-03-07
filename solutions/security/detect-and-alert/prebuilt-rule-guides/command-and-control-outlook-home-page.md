---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Outlook Home Page Registry Modification" prebuilt detection rule.'
---

# Outlook Home Page Registry Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Outlook Home Page Registry Modification

The Outlook Home Page feature allows users to set a webpage as the default view for folders, leveraging registry keys to store URL configurations. Adversaries exploit this by modifying these keys to redirect to malicious sites, enabling command and control or persistence. The detection rule identifies suspicious registry changes, focusing on URL entries within specific paths, flagging potential misuse for further investigation.

### Possible investigation steps

- Review the registry path and value to confirm the presence of a suspicious URL entry in the specified registry paths, such as "HKCU\\*\\SOFTWARE\\Microsoft\\Office\\*\\Outlook\\Webview\\Inbox\\URL".
- Investigate the URL found in the registry data strings to determine if it is known to be malicious or associated with suspicious activity.
- Check the modification history of the registry key to identify when the change occurred and which user or process made the modification.
- Correlate the registry modification event with other security events on the host, such as network connections or process executions, to identify potential malicious activity.
- Assess the affected system for signs of compromise, including unusual network traffic or unauthorized access attempts, to determine the scope of the incident.
- Consult threat intelligence sources to see if the URL or related indicators are associated with known threat actors or campaigns.

### False positive analysis

- Legitimate software updates or installations may modify the registry keys associated with Outlook's Home Page feature. Users can create exceptions for known software update processes to prevent unnecessary alerts.
- Custom scripts or administrative tools used by IT departments to configure Outlook settings across multiple machines might trigger this rule. Identifying and excluding these trusted scripts or tools can reduce false positives.
- Some third-party Outlook add-ins or plugins may alter the registry keys for legitimate purposes. Users should verify the legitimacy of these add-ins and whitelist them if they are deemed safe.
- Automated backup or recovery solutions that restore Outlook settings might cause registry changes. Users can exclude these processes if they are part of a regular and secure backup routine.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further communication with potentially malicious sites.
- Use endpoint detection and response (EDR) tools to terminate any suspicious processes associated with the modified registry keys.
- Restore the modified registry keys to their default values to remove the malicious URL configuration.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any additional threats.
- Review and analyze network logs to identify any outbound connections to suspicious domains or IP addresses, and block these at the firewall.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if other systems are affected.
- Implement additional monitoring on the affected system and similar endpoints to detect any recurrence of the threat, focusing on registry changes and network activity.
