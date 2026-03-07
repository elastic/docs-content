---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Escalation via Vulnerable MSI Repair" prebuilt detection rule.'
---

# Potential Escalation via Vulnerable MSI Repair

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Escalation via Vulnerable MSI Repair

Windows Installer (MSI) is a service used for software installation and maintenance. Adversaries exploit vulnerabilities in MSI repair functions to gain elevated privileges. This detection rule identifies suspicious activity by monitoring browser processes accessing Microsoft Help pages, followed by elevated process creation, indicating potential privilege escalation attempts.

### Possible investigation steps

- Review the alert details to identify the specific browser process that accessed the Microsoft Help page, noting the process name and command line details.
- Check the user domain associated with the process to confirm if it matches "NT AUTHORITY", "AUTORITE NT", or "AUTORIDADE NT", which may indicate a system-level account was used.
- Investigate the parent process of the browser to determine if it was expected or if it shows signs of compromise or unusual behavior.
- Examine the timeline of events to see if an elevated process was spawned shortly after the browser accessed the Microsoft Help page, indicating potential exploitation.
- Correlate the event with other security logs or alerts from data sources like Elastic Endgame, Sysmon, or Microsoft Defender for Endpoint to gather additional context or evidence of malicious activity.
- Assess the risk and impact of the elevated process by identifying its actions and any changes made to the system, such as modifications to critical files or registry keys.

### False positive analysis

- Legitimate software updates or installations may trigger the rule if they involve browser-based help documentation. To manage this, identify and whitelist known software update processes that frequently access Microsoft Help pages.
- Automated scripts or administrative tools that use browsers to access Microsoft Help for legitimate purposes can cause false positives. Exclude these scripts or tools by specifying their unique command-line patterns or process names.
- User-initiated troubleshooting or help-seeking behavior that involves accessing Microsoft Help pages might be misinterpreted as suspicious. Educate users on safe browsing practices and consider excluding specific user accounts or domains that are known to frequently engage in such activities.
- Security tools or monitoring solutions that simulate browser activity for testing purposes may inadvertently trigger the rule. Identify these tools and create exceptions based on their process names or command-line arguments to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further exploitation or lateral movement by the adversary.
- Terminate any suspicious elevated processes that were spawned following the browser's navigation to the Microsoft Help page to halt potential privilege escalation activities.
- Conduct a thorough review of the affected system's event logs and process creation history to identify any unauthorized changes or additional indicators of compromise.
- Apply the latest security patches and updates to the Windows Installer service and any other vulnerable components to mitigate the exploited vulnerability.
- Restore the affected system from a known good backup if unauthorized changes or persistent threats are detected that cannot be easily remediated.
- Monitor the network for any signs of similar exploitation attempts or related suspicious activities, using enhanced detection rules and threat intelligence feeds.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to ensure comprehensive remediation and recovery efforts.
