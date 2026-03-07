---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Windows Service Installed via an Unusual Client" prebuilt detection rule.
---

# Windows Service Installed via an Unusual Client

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Windows Service Installed via an Unusual Client

Windows services are crucial for running background processes with elevated privileges. Adversaries exploit this by creating services to escalate privileges from administrator to SYSTEM. The detection rule identifies anomalies by flagging service installations initiated by atypical processes, excluding known legitimate services. This helps in spotting potential privilege escalation attempts by monitoring unusual client activity.

### Possible investigation steps

- Review the event logs to identify the specific client process that initiated the service installation by examining the winlog.event_data.ClientProcessId and winlog.event_data.ParentProcessId fields.
- Investigate the parent process associated with the unusual client process to determine if it is a known legitimate application or potentially malicious.
- Check the winlog.event_data.ServiceFileName to verify the path and name of the service file, ensuring it is not a known legitimate service excluded in the query.
- Analyze the timeline of events around the service installation to identify any preceding suspicious activities or related alerts that might indicate a broader attack.
- Conduct a reputation check on the client process and service file using threat intelligence sources to assess if they are associated with known malicious activities.
- Examine the system for any additional indicators of compromise, such as unexpected network connections or changes to critical system files, that may suggest privilege escalation or lateral movement attempts.

### False positive analysis

- Legitimate software installations or updates may trigger the rule if they create services using unusual client processes. To manage this, identify and whitelist these processes in the detection rule to prevent unnecessary alerts.
- System management tools like Veeam and PDQ Inventory are already excluded, but other similar tools might not be. Regularly review and update the exclusion list to include any additional legitimate tools used in your environment.
- Custom scripts or administrative tools that create services for maintenance or monitoring purposes can also cause false positives. Document these scripts and consider adding them to the exclusion list if they are verified as safe.
- Temporary or one-time service installations for troubleshooting or testing can be mistaken for threats. Ensure that such activities are logged and communicated to the security team to avoid confusion and unnecessary alerts.
- Changes in system configurations or updates to existing software might alter the behavior of legitimate processes, causing them to be flagged. Regularly review and adjust the detection rule to accommodate these changes while maintaining security integrity.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate the suspicious service and any associated processes identified by the alert to stop potential privilege escalation or malicious activity.
- Conduct a thorough review of the service's configuration and associated files to identify any unauthorized changes or malicious code.
- Restore any altered or compromised system files from a known good backup to ensure system integrity.
- Change all administrator and SYSTEM account passwords on the affected system and any connected systems to prevent further unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the scope of the breach.
- Implement additional monitoring and logging on the affected system and similar environments to detect any recurrence of the threat or related suspicious activities.
