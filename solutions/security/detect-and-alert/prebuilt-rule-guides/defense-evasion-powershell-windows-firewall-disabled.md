---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Windows Firewall Disabled via PowerShell" prebuilt detection rule.
---

# Windows Firewall Disabled via PowerShell

## Triage and analysis

### Investigating Windows Firewall Disabled via PowerShell

Windows Defender Firewall is a native component that provides host-based, two-way network traffic filtering for a device and blocks unauthorized network traffic flowing into or out of the local device.

Attackers can disable the Windows firewall or its rules to enable lateral movement and command and control activity.

This rule identifies patterns related to disabling the Windows firewall or its rules using the `Set-NetFirewallProfile` PowerShell cmdlet.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Inspect the host for suspicious or abnormal behavior in the alert timeframe.

### False positive analysis

- This mechanism can be used legitimately. Check whether the user is an administrator and is legitimately performing troubleshooting.
- In case of an allowed benign true positive (B-TP), assess adding rules to allow needed traffic and re-enable the firewall.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Re-enable the firewall with its desired configurations.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Review the privileges assigned to the involved users to ensure that the least privilege principle is being followed.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

