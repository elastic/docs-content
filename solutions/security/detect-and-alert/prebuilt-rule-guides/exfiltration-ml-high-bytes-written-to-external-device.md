---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Bytes Sent to an External Device" prebuilt detection rule.
---

# Spike in Bytes Sent to an External Device

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Bytes Sent to an External Device

The detection rule leverages machine learning to identify anomalies in data transfer patterns to external devices, which typically follow predictable trends. Adversaries may exploit this by transferring large volumes of data to external media for exfiltration. The rule detects deviations from normal behavior, flagging potential illicit data transfers for further investigation.

### Possible investigation steps

- Review the alert details to identify the specific external device involved and the volume of data transferred.
- Correlate the time of the anomaly with user activity logs to determine if the data transfer aligns with any known or authorized user actions.
- Check historical data transfer patterns for the involved device to assess whether the detected spike is truly anomalous or part of a legitimate operational change.
- Investigate the user account associated with the data transfer for any signs of compromise or unusual behavior, such as recent password changes or failed login attempts.
- Examine the content and type of data transferred, if possible, to assess the sensitivity and potential impact of the data exfiltration.
- Cross-reference the device and user activity with other security alerts or incidents to identify any related suspicious activities or patterns.

### False positive analysis

- Regular backups to external devices can trigger false positives. Users should identify and exclude backup operations from the rule's scope by specifying known backup software or devices.
- Software updates or installations that involve large data transfers to external media may be misclassified. Users can create exceptions for these activities by defining specific update processes or installation paths.
- Data archiving processes that periodically transfer large volumes of data to external storage can be mistaken for exfiltration. Users should whitelist these scheduled archiving tasks by recognizing the associated patterns or schedules.
- Media content creation or editing, such as video production, often involves significant data transfers. Users can exclude these activities by identifying and excluding the relevant applications or file types.
- Temporary data transfers for legitimate business purposes, like transferring project files to a client, can be flagged. Users should document and exclude these known business processes by specifying the involved devices or file types.

### Response and remediation

- Immediately isolate the affected device from the network to prevent further data exfiltration.
- Conduct a forensic analysis of the device to identify the source and scope of the data transfer, focusing on the files transferred and any associated processes or applications.
- Review and revoke any unnecessary permissions or access rights that may have facilitated the data transfer to the external device.
- Notify the security operations center (SOC) and relevant stakeholders about the incident for awareness and potential escalation.
- Implement additional monitoring on similar devices and network segments to detect any further anomalous data transfer activities.
- Update and enforce data transfer policies to restrict unauthorized use of external devices, ensuring compliance with organizational security standards.
- Consider deploying endpoint detection and response (EDR) solutions to enhance visibility and control over data movements to external devices.
