---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "New USB Storage Device Mounted" prebuilt detection rule.'
---

# New USB Storage Device Mounted

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating New USB Storage Device Mounted

Removable devices, like USB drives, are common in Windows environments for data transfer. Adversaries exploit these to introduce malware or exfiltrate data, leveraging their plug-and-play nature. The detection rule monitors registry changes for new device names, signaling potential unauthorized access. By focusing on first-time-seen devices, it helps identify suspicious activities linked to data exfiltration or initial access attempts.

This detection uses Elastic Defend device control events, Device control helps protect your Windows and Mac endpoints from data loss, malware, and unauthorized access by managing which devices can connect to your computers. Specifically, it restricts which external USB storage devices can connect to hosts that have Elastic Defend installed.


### Possible investigation steps

- Review the device mount event details to confirm the presence of a new device by checking the device.serial_number.
- Check for any subsequent file access or transfer events involving the new device to assess potential data exfiltration.
- Investigate the device's history by searching for any previous connections to other systems within the network to determine if it has been used elsewhere.
- Analyze any related alerts or logs for additional context or suspicious activities linked to the device.

### False positive analysis

- Frequent use of company-issued USB drives for legitimate data transfer can trigger alerts. Maintain a list of approved devices and create exceptions for these in the monitoring system.
- Software updates or installations via USB drives may be flagged. Identify and whitelist known update devices or processes to prevent unnecessary alerts.
- IT department activities involving USB devices for maintenance or troubleshooting can appear suspicious. Coordinate with IT to log and exclude these routine operations from triggering alerts.
- Devices used for regular backups might be detected as new. Ensure backup devices are registered and excluded from the rule to avoid false positives.
- Personal USB devices used by employees for non-work-related purposes can cause alerts. Implement a policy for registering personal devices and exclude them if deemed non-threatening.

### Response and remediation

- Immediately isolate the affected host from the network to prevent potential data exfiltration or further spread of malware.
- Block the device by serial number using the relevant Elastic Defend Device Control policy.
- Conduct a thorough scan of the isolated host using updated antivirus and anti-malware tools to identify and remove any malicious software introduced via the removable device.
- If malicious activity is confirmed, collect and preserve relevant logs and evidence for further forensic analysis and potential legal action.
- Notify the security team and relevant stakeholders about the incident, providing details of the device and any identified threats.
- Implement a temporary block on the use of removable devices across the network until the threat is fully contained and remediated.
- Enhance monitoring and detection capabilities by updating security tools and rules to better identify similar threats in the future, focusing on registry changes and device connections.
