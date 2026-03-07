---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "A scheduled task was created" prebuilt detection rule.
---

# A scheduled task was created

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating A scheduled task was created

Scheduled tasks in Windows automate routine tasks, enhancing efficiency. However, adversaries exploit this feature to maintain persistence, move laterally, or escalate privileges by creating malicious tasks. The detection rule identifies suspicious task creation by filtering out benign tasks and those initiated by system accounts, focusing on potential threats. This approach helps security analysts pinpoint unauthorized task creation indicative of malicious activity.

### Possible investigation steps

- Review the user account associated with the task creation to determine if it is a known and authorized user, ensuring it is not a system account by checking that the username does not end with a dollar sign.
- Examine the task name and path in the event data to identify if it matches any known benign tasks or if it appears suspicious or unfamiliar.
- Investigate the origin of the task creation by checking the source IP address or hostname, if available, to determine if it aligns with expected network activity.
- Check the task's scheduled actions and triggers to understand what the task is designed to execute and when, looking for any potentially harmful or unexpected actions.
- Correlate the task creation event with other security events or logs around the same time to identify any related suspicious activities or anomalies.

### False positive analysis

- Scheduled tasks created by system accounts or computer accounts are often benign. These can be excluded by filtering out user names ending with a dollar sign, which typically represent system accounts.
- Tasks associated with common software updates or maintenance, such as those from Hewlett-Packard or Microsoft Visual Studio, are generally non-threatening. These can be excluded by specifying their full task names in the exclusion list.
- OneDrive update tasks are frequently triggered and are usually safe. Exclude these by using patterns that match their task names, such as those starting with "OneDrive Standalone Update Task".
- Regularly review and update the exclusion list to include any new benign tasks that are identified over time, ensuring that the rule remains effective without generating unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the adversary.
- Terminate any suspicious scheduled tasks identified by the alert to halt any ongoing malicious activity.
- Conduct a thorough review of the system's scheduled tasks to identify and remove any other unauthorized or suspicious tasks.
- Restore the system from a known good backup if any malicious activity has been confirmed and has potentially compromised system integrity.
- Update and patch the system to the latest security standards to close any vulnerabilities that may have been exploited.
- Monitor the system and network for any signs of re-infection or further unauthorized scheduled task creation.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
