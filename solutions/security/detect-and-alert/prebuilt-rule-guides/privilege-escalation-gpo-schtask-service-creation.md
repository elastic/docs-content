---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Creation or Modification of a new GPO Scheduled Task or Service" prebuilt detection rule.
---

# Creation or Modification of a new GPO Scheduled Task or Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Creation or Modification of a new GPO Scheduled Task or Service

Group Policy Objects (GPOs) are crucial for centralized management in Windows environments, allowing administrators to configure settings across domain-joined machines. Adversaries with domain admin rights can exploit GPOs to create or modify scheduled tasks or services, deploying malicious payloads network-wide. The detection rule identifies such activities by monitoring specific file changes in GPO paths, excluding legitimate system processes, thus highlighting potential abuse for privilege escalation or persistence.

### Possible investigation steps

- Review the file path and name to confirm if the changes were made to "ScheduledTasks.xml" or "Services.xml" within the specified GPO paths, as these are indicative of potential unauthorized modifications.
- Check the process that initiated the file change, ensuring it is not "C:\\Windows\\System32\\dfsrs.exe", which is excluded as a legitimate system process.
- Investigate the user account associated with the file modification event to determine if it has domain admin rights and assess if the activity aligns with their typical behavior or role.
- Examine recent changes in the GPO settings to identify any new or altered scheduled tasks or services that could be used for malicious purposes.
- Correlate the event with other security logs or alerts from data sources like Elastic Endgame, Sysmon, or Microsoft Defender for Endpoint to identify any related suspicious activities or patterns.
- Assess the impact by identifying which domain-joined machines are affected by the GPO changes and determine if any unauthorized tasks or services have been executed.

### False positive analysis

- Legitimate administrative changes to GPOs can trigger alerts. Regularly review and document scheduled administrative tasks to differentiate between expected and unexpected changes.
- Automated system management tools may modify GPO scheduled tasks or services as part of routine operations. Identify these tools and create exceptions for their processes to reduce noise.
- Updates or patches from Microsoft or other trusted vendors might alter GPO settings. Monitor update schedules and correlate changes with known update activities to verify legitimacy.
- Internal IT scripts or processes that manage GPOs for configuration consistency can cause false positives. Ensure these scripts are well-documented and consider excluding their specific actions from monitoring.
- Temporary changes made by IT staff for troubleshooting or testing purposes can be mistaken for malicious activity. Implement a change management process to log and approve such activities, allowing for easy exclusion from alerts.

### Response and remediation

- Immediately isolate affected systems from the network to prevent further spread of any malicious payloads deployed via the modified GPO scheduled tasks or services.
- Revoke domain admin privileges from any accounts that are suspected of being compromised to prevent further unauthorized modifications to GPOs.
- Conduct a thorough review of the modified ScheduledTasks.xml and Services.xml files to identify any unauthorized or malicious entries, and revert them to their previous legitimate state.
- Utilize endpoint detection and response (EDR) tools to scan for and remove any malicious payloads that may have been executed on domain-joined machines as a result of the GPO modifications.
- Notify the security operations center (SOC) and escalate the incident to the incident response team for further investigation and to determine the scope of the compromise.
- Implement additional monitoring on GPO paths and domain admin activities to detect any further unauthorized changes or suspicious behavior.
- Review and strengthen access controls and auditing policies for GPO management to prevent unauthorized modifications in the future.
