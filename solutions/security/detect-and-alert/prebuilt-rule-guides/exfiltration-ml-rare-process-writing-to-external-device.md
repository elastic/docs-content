---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Process Writing Data to an External Device" prebuilt detection rule.'
---

# Unusual Process Writing Data to an External Device

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Process Writing Data to an External Device

In modern environments, processes may write data to external devices for legitimate reasons, such as backups or data transfers. However, adversaries can exploit this by using seemingly harmless processes to exfiltrate sensitive data. The detection rule leverages machine learning to identify rare processes engaging in such activities, flagging potential exfiltration attempts by analyzing deviations from typical behavior patterns.

### Possible investigation steps

- Review the process name and path to determine if it is commonly associated with legitimate activities or known software.
- Check the user account associated with the process to verify if it has the necessary permissions and if the activity aligns with the user's typical behavior.
- Analyze the external device's details, such as its type and connection history, to assess if it is a recognized and authorized device within the organization.
- Investigate the volume and type of data being written to the external device to identify any sensitive or unusual data transfers.
- Correlate the process activity with other security events or logs to identify any concurrent suspicious activities or anomalies.
- Consult with the user or department associated with the process to confirm if the data transfer was authorized and necessary.

### False positive analysis

- Backup processes may trigger alerts when writing data to external devices. Users should identify and whitelist legitimate backup applications to prevent false positives.
- Data transfer applications used for legitimate business purposes can be flagged. Regularly review and approve these applications to ensure they are not mistakenly identified as threats.
- Software updates or installations that involve writing data to external devices might be detected. Establish a list of known update processes and exclude them from triggering alerts.
- IT maintenance activities, such as system diagnostics or hardware testing, can cause false positives. Document and exclude these routine processes to avoid unnecessary alerts.
- User-initiated file transfers for legitimate reasons, such as moving large datasets for analysis, should be monitored and approved to prevent misclassification.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further data exfiltration and contain the threat.
- Identify and terminate the suspicious process writing data to the external device to stop any ongoing exfiltration activities.
- Conduct a forensic analysis of the affected system to determine the scope of the data exfiltration, including what data was accessed or transferred.
- Review and revoke any compromised credentials or access permissions associated with the affected process to prevent unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement additional monitoring on the affected system and similar environments to detect any recurrence of the threat or related suspicious activities.
- Update security policies and controls to prevent similar exfiltration attempts, such as restricting process permissions to write to external devices and enhancing endpoint protection measures.
