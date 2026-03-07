---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Spike in Bytes Sent to an External Device via Airdrop" prebuilt detection rule.'
---

# Spike in Bytes Sent to an External Device via Airdrop

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Bytes Sent to an External Device via Airdrop

Airdrop facilitates seamless file sharing between Apple devices, leveraging Bluetooth and Wi-Fi. While convenient, adversaries can exploit it for unauthorized data exfiltration by transferring large volumes of sensitive data. The detection rule employs machine learning to identify anomalies in data transfer patterns, flagging unusual spikes in bytes sent as potential exfiltration attempts, thus aiding in early threat detection.

### Possible investigation steps

- Review the alert details to identify the specific device and user involved in the data transfer. Check for any known associations with previous incidents or suspicious activities.
- Analyze the volume of data transferred and compare it to typical usage patterns for the device and user. Determine if the spike is significantly higher than usual.
- Investigate the time and context of the data transfer. Correlate with other logs or alerts to identify any concurrent suspicious activities or anomalies.
- Check the destination device's details to verify if it is a recognized and authorized device within the organization. Investigate any unknown or unauthorized devices.
- Contact the user associated with the alert to verify the legitimacy of the data transfer. Gather information on the nature of the files transferred and the purpose of the transfer.
- Review any recent changes in the user's access privileges or roles that might explain the increased data transfer activity.

### False positive analysis

- Regular large file transfers for legitimate business purposes, such as media companies transferring video files, can trigger false positives. Users can create exceptions for specific devices or user accounts known to perform these tasks regularly.
- Software updates or backups that involve transferring large amounts of data to external devices may be misidentified as exfiltration attempts. Users should whitelist these activities by identifying the associated processes or applications.
- Educational institutions or creative teams often share large files for collaborative projects. Establishing a baseline for expected data transfer volumes and excluding these from alerts can reduce false positives.
- Devices used for testing or development purposes might frequently send large data volumes. Users can exclude these devices from monitoring by adding them to an exception list.
- Personal use of Airdrop for transferring large media files, such as photos or videos, can be mistaken for suspicious activity. Users can mitigate this by setting thresholds that account for typical personal use patterns.

### Response and remediation

- Immediately isolate the affected device from the network to prevent further data exfiltration.
- Verify the identity and permissions of the user associated with the anomalous Airdrop activity to ensure they are authorized to transfer data.
- Conduct a forensic analysis of the device to identify any unauthorized applications or processes that may have facilitated the data transfer.
- Review and revoke any unnecessary permissions or access rights for the user or device involved in the incident.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if the activity is part of a larger threat campaign.
- Implement additional monitoring on the affected device and similar devices to detect any further anomalous Airdrop activities.
- Update security policies and controls to restrict Airdrop usage to only trusted devices and networks, reducing the risk of future unauthorized data transfers.
