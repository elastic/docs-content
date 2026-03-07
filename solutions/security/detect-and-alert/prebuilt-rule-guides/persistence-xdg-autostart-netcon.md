---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Network Connections Initiated Through XDG Autostart Entry" prebuilt detection rule.
---

# Network Connections Initiated Through XDG Autostart Entry

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Network Connections Initiated Through XDG Autostart Entry

XDG Autostart entries are used in GNOME and XFCE Linux environments to automatically execute scripts or applications upon user login, facilitating user convenience. However, adversaries can exploit this feature to maintain persistence by modifying these entries to initiate unauthorized network connections. The detection rule identifies such malicious activity by monitoring processes linked to XDG autostart and subsequent suspicious network connections, excluding known benign processes and internal IP ranges.

### Possible investigation steps

- Review the process details from the alert, focusing on the process.entity_id and process.executable fields to identify the specific application or script that was executed through the XDG autostart entry.
- Examine the parent process information, particularly the process.parent.executable field, to confirm if the process was initiated by a legitimate session manager like /usr/bin/xfce4-session.
- Investigate the network connection details, paying attention to the destination.ip field to determine if the connection was attempted to an external or suspicious IP address not covered by the internal IP ranges specified in the query.
- Check the process.args field for any unusual or unexpected command-line arguments that might indicate malicious intent or unauthorized modifications to the autostart entry.
- Correlate the alert with other security events or logs from the same host.id to identify any additional suspicious activities or patterns that might suggest a broader compromise or persistence mechanism.
- Validate the legitimacy of the process.executable by comparing it against known benign applications listed in the query, such as /usr/lib64/firefox/firefox, to rule out false positives.

### False positive analysis

- Network connections from legitimate applications like Firefox or FortiClient may trigger false positives. To handle this, add these applications to the exclusion list in the detection rule.
- Internal network traffic within known safe IP ranges can be mistakenly flagged. Ensure these IP ranges are included in the exclusion criteria to prevent unnecessary alerts.
- Custom scripts or applications that are part of the user's normal login process might be misidentified. Review and whitelist these processes if they are verified as non-threatening.
- Regular updates or maintenance tasks that initiate network connections during login can cause false alerts. Identify these tasks and adjust the rule to exclude them if they are part of routine operations.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized network connections and potential lateral movement.
- Terminate any suspicious processes identified as being initiated through XDG autostart entries to halt any ongoing malicious activity.
- Review and remove any unauthorized or suspicious XDG autostart entries to eliminate persistence mechanisms established by the attacker.
- Conduct a thorough scan of the affected system for additional indicators of compromise, such as unauthorized user accounts or modified system files, to ensure comprehensive remediation.
- Restore any altered system configurations or files from a known good backup to ensure system integrity and functionality.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems may be affected.
- Implement enhanced monitoring and logging for XDG autostart entries and network connections to detect similar threats in the future and improve overall security posture.
