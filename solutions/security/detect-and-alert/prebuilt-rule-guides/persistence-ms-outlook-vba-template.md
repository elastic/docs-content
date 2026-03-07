---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Persistence via Microsoft Outlook VBA" prebuilt detection rule.'
---

# Persistence via Microsoft Outlook VBA

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Persistence via Microsoft Outlook VBA

Microsoft Outlook supports VBA scripting to automate tasks, which can be exploited by adversaries to maintain persistence. Attackers may install malicious VBA templates in the Outlook environment, triggering scripts upon application startup. The detection rule identifies suspicious activity by monitoring for unauthorized modifications to the VBAProject.OTM file, a common target for such persistence techniques, leveraging various data sources to flag potential threats.

### Possible investigation steps

- Review the alert details to confirm the file path matches the pattern "C:\\Users\\*\\AppData\\Roaming\\Microsoft\\Outlook\\VbaProject.OTM" and ensure the event type is not "deletion".
- Check the modification timestamp of the VbaProject.OTM file to determine when the unauthorized change occurred.
- Identify the user account associated with the file path to understand which user profile was potentially compromised.
- Investigate recent login activities and processes executed by the identified user to detect any anomalies or unauthorized access.
- Examine the contents of the VbaProject.OTM file for any suspicious or unfamiliar VBA scripts that could indicate malicious intent.
- Correlate the findings with other data sources such as Sysmon, Microsoft Defender for Endpoint, or SentinelOne to gather additional context or related events.
- Assess the risk and impact of the detected activity and determine if further containment or remediation actions are necessary.

### False positive analysis

- Routine updates or legitimate changes to the Outlook environment can trigger alerts. Users should verify if recent software updates or administrative changes align with the detected activity.
- Custom scripts or macros developed by IT departments for legitimate automation tasks may be flagged. Establish a whitelist of known and approved VBA scripts to prevent unnecessary alerts.
- User-initiated actions such as importing or exporting Outlook settings might modify the VbaProject.OTM file. Educate users on the implications of these actions and consider excluding these specific user actions from triggering alerts.
- Security software or backup solutions that interact with Outlook files could cause false positives. Identify and exclude these processes if they are known to be safe and necessary for operations.
- Regularly review and update the exclusion list to ensure it reflects current organizational needs and does not inadvertently allow malicious activity.

### Response and remediation

- Isolate the affected endpoint from the network to prevent further spread of the malicious VBA script and to contain the threat.
- Terminate any suspicious Outlook processes on the affected machine to stop the execution of potentially harmful scripts.
- Remove the unauthorized or malicious VbaProject.OTM file from the affected user's Outlook directory to eliminate the persistence mechanism.
- Restore the VbaProject.OTM file from a known good backup if available, ensuring that it is free from any unauthorized modifications.
- Conduct a full antivirus and antimalware scan on the affected endpoint using tools like Microsoft Defender for Endpoint to identify and remove any additional threats.
- Review and update endpoint security policies to restrict unauthorized modifications to Outlook VBA files, leveraging application whitelisting or similar controls.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on other systems within the network.
