---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Enable Host Network Discovery via Netsh" prebuilt detection rule.
---

# Enable Host Network Discovery via Netsh

## Triage and analysis

### Investigating Enable Host Network Discovery via Netsh

The Windows Defender Firewall is a native component that provides host-based, two-way network traffic filtering for a device and blocks unauthorized network traffic flowing into or out of the local device.

Attackers can enable Network Discovery on the Windows firewall to find other systems present in the same network. Systems with this setting enabled will communicate with other systems using broadcast messages, which can be used to identify targets for lateral movement. This rule looks for the setup of this setting using the netsh utility.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Inspect the host for suspicious or abnormal behavior in the alert timeframe.

### False positive analysis

- This mechanism can be used legitimately. Analysts can dismiss the alert if the Administrator is aware of the activity and there are justifications for this configuration.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Disable Network Discovery:
    - Using netsh: `netsh advfirewall firewall set rule group="Network Discovery" new enable=No`
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Review the privileges assigned to the involved users to ensure that the least privilege principle is being followed.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

