---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Outbound Scheduled Task Activity via PowerShell" prebuilt detection rule.'
---

# Outbound Scheduled Task Activity via PowerShell

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Outbound Scheduled Task Activity via PowerShell

PowerShell, a powerful scripting language in Windows, can automate tasks via the Task Scheduler. Adversaries exploit this by creating scheduled tasks to execute malicious scripts, facilitating lateral movement or remote discovery. The detection rule identifies suspicious PowerShell activity by monitoring for the Task Scheduler DLL load and subsequent outbound RPC connections, signaling potential misuse.

### Possible investigation steps

- Review the alert details to identify the specific host.id and process.entity_id associated with the suspicious activity.
- Examine the process execution history on the affected host to determine if the PowerShell process (powershell.exe, pwsh.exe, or powershell_ise.exe) has executed any unexpected or unauthorized scripts.
- Check the network logs for the host to identify any unusual or unauthorized outbound RPC connections, particularly those targeting port 135, and verify if the destination addresses are legitimate and expected.
- Investigate the context of the taskschd.dll library load by reviewing recent scheduled tasks on the host to identify any newly created or modified tasks that could be linked to the alert.
- Correlate the alert with other security events or logs from the same host or network segment to identify any patterns or additional indicators of compromise that may suggest lateral movement or remote discovery attempts.

### False positive analysis

- Legitimate administrative tasks using PowerShell may trigger the rule if they involve loading the Task Scheduler DLL and making RPC connections. To manage this, identify and whitelist specific scripts or processes that are known to perform these actions regularly.
- Automated system maintenance or monitoring tools might also load the Task Scheduler DLL and establish RPC connections. Review these tools and exclude their process IDs or hashes from the detection rule to prevent false alerts.
- Software updates or installations that use PowerShell scripts could mimic the behavior detected by the rule. Monitor update schedules and temporarily disable the rule during these periods if necessary, or create exceptions for known update processes.
- Developers or IT staff using PowerShell for legitimate remote management tasks may inadvertently trigger the rule. Implement user-based exceptions for trusted personnel or restrict the rule to non-administrative accounts to reduce false positives.

### Response and remediation

- Isolate the affected host immediately from the network to prevent further lateral movement or data exfiltration.
- Terminate the suspicious PowerShell process identified in the alert to stop any ongoing malicious activity.
- Conduct a forensic analysis of the affected system to identify any additional malicious scheduled tasks or scripts and remove them.
- Review and clean up any unauthorized scheduled tasks created on the system to ensure no persistence mechanisms remain.
- Reset credentials for any accounts that were used or potentially compromised during the incident to prevent unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the scope of the attack.
- Implement enhanced monitoring for similar PowerShell and scheduled task activities across the network to detect and respond to future threats promptly.
