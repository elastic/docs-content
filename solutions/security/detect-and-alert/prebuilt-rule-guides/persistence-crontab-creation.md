---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious CronTab Creation or Modification" prebuilt detection rule.
---

# Suspicious CronTab Creation or Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious CronTab Creation or Modification

Cron is a time-based job scheduler in Unix-like operating systems, including macOS, used to automate repetitive tasks. Adversaries may exploit cron to maintain persistence by scheduling malicious scripts or commands. The detection rule identifies unusual crontab modifications by non-standard processes, flagging potential misuse by threat actors seeking to establish persistence.

### Possible investigation steps

- Review the process name and executable path that triggered the alert to determine if it is a known legitimate application or a potentially malicious one.
- Examine the file path "/private/var/at/tabs/*" to identify any recent changes or additions to crontab entries that could indicate unauthorized scheduling of tasks.
- Investigate the user account associated with the process to determine if it has a history of legitimate crontab modifications or if it might be compromised.
- Check for any related alerts or logs around the same timeframe that might indicate additional suspicious activity or corroborate the use of cron for persistence.
- Analyze the command or script scheduled in the crontab entry to assess its purpose and potential impact on the system, looking for signs of malicious intent.

### False positive analysis

- System maintenance scripts or legitimate administrative tools may modify crontabs using non-standard processes. Review the process name and executable path to determine if the activity is part of routine maintenance.
- Development or testing environments might use scripts or automation tools that modify crontabs for legitimate purposes. Identify and document these processes to create exceptions in the detection rule.
- Some third-party applications may use cron jobs for updates or scheduled tasks. Verify the legitimacy of these applications and consider excluding their processes if they are known and trusted.
- User-initiated scripts that automate personal tasks could trigger this rule. Educate users on the implications of using cron for personal automation and establish a process for approving such scripts.
- Regularly review and update the list of excluded processes to ensure that only verified and non-threatening activities are exempt from detection.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential lateral movement or further execution of malicious tasks.
- Terminate any suspicious processes identified as modifying the crontab, especially those not typically associated with crontab modifications, such as python or osascript.
- Review and remove any unauthorized or suspicious entries in the crontab file located at /private/var/at/tabs/* to eliminate persistence mechanisms established by the threat actor.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malware or malicious scripts.
- Restore the system from a known good backup if the integrity of the system is in question and ensure all security patches and updates are applied.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for crontab modifications and related processes to detect and respond to similar threats in the future.
