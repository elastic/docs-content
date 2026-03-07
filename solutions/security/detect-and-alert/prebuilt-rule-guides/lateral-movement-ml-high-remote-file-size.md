---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Remote File Size" prebuilt detection rule.
---

# Unusual Remote File Size

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Remote File Size
Machine learning models in security environments analyze file transfer patterns to identify anomalies, such as unusually large files shared remotely. Adversaries exploit this by aggregating data into large files to avoid detection during lateral movement. The 'Unusual Remote File Size' rule leverages ML to flag these anomalies, aiding in early detection of potential data exfiltration activities.

### Possible investigation steps

- Review the alert details to identify the specific remote host and file size involved in the anomaly.
- Check the historical file transfer patterns of the identified remote host to determine if this large file size is truly unusual.
- Investigate the contents and purpose of the large file, if accessible, to assess whether it contains sensitive or valuable information.
- Analyze network logs to trace the origin and destination of the file transfer, looking for any unauthorized or suspicious connections.
- Correlate the event with other security alerts or logs to identify any concurrent suspicious activities that might indicate lateral movement or data exfiltration.
- Verify the user account associated with the file transfer to ensure it has not been compromised or misused.

### False positive analysis

- Large file transfers related to legitimate business operations, such as backups or data migrations, can trigger false positives. Users should identify and whitelist these routine activities to prevent unnecessary alerts.
- Software updates or patches distributed across the network may also appear as unusually large file transfers. Establishing a baseline for expected file sizes during these updates can help in distinguishing them from potential threats.
- Remote file sharing services used for collaboration might generate alerts if large files are shared frequently. Monitoring and excluding these services from the rule can reduce false positives.
- Automated data processing tasks that involve transferring large datasets between systems should be documented and excluded from the rule to avoid false alarms.
- Regularly review and update the list of known safe hosts and services that are permitted to transfer large files, ensuring that only legitimate activities are excluded from detection.

### Response and remediation

- Isolate the affected host immediately to prevent further lateral movement and potential data exfiltration. Disconnect it from the network to contain the threat.
- Conduct a thorough analysis of the large file transfer to determine its contents and origin. Verify if sensitive data was included and assess the potential impact.
- Review and terminate any unauthorized remote sessions or connections identified during the investigation to prevent further exploitation.
- Reset credentials and review access permissions for the affected host and any associated accounts to mitigate the risk of compromised credentials being used for further attacks.
- Implement network segmentation to limit the ability of attackers to move laterally within the network, reducing the risk of similar incidents in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to ensure comprehensive remediation actions are taken.
- Enhance monitoring and logging for unusual file transfer activities and remote access attempts to improve early detection of similar threats in the future.
