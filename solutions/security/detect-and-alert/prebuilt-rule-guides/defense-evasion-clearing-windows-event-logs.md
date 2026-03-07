---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Clearing Windows Event Logs" prebuilt detection rule.'
---

# Clearing Windows Event Logs

## Triage and analysis

### Investigating Clearing Windows Event Logs

Windows event logs are a fundamental data source for security monitoring, forensics, and incident response. Adversaries can tamper, clear, and delete this data to break SIEM detections, cover their tracks, and slow down incident response.

This rule looks for the execution of the `wevtutil.exe` utility or the `Clear-EventLog` cmdlet to clear event logs.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
  - Verify if any other anti-forensics behaviors were observed.
- Investigate the event logs prior to the action for suspicious behaviors that an attacker may be trying to cover up.

### False positive analysis

- This mechanism can be used legitimately. Analysts can dismiss the alert if the administrator is aware of the activity and there are justifications for this action.
- Analyze whether the cleared event log is pertinent to security and general monitoring. Administrators can clear non-relevant event logs using this mechanism. If this activity is expected and noisy in your environment, consider adding exceptions — preferably with a combination of user and command line conditions.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
  - This activity is potentially done after the adversary achieves its objectives on the host. Ensure that previous actions, if any, are investigated accordingly with their response playbooks.
- Isolate the involved host to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
