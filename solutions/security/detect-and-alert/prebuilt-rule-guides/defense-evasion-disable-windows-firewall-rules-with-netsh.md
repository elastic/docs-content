---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Disable Windows Firewall Rules via Netsh" prebuilt detection rule.'
---

# Disable Windows Firewall Rules via Netsh

## Triage and analysis

### Investigating Disable Windows Firewall Rules via Netsh

The Windows Defender Firewall is a native component which provides host-based, two-way network traffic filtering for a device, and blocks unauthorized network traffic flowing into or out of the local device.

Attackers can disable the Windows firewall or its rules to enable lateral movement and command and control activity.

This rule identifies patterns related to disabling the Windows firewall or its rules using the `netsh.exe` utility.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the user to check if they are aware of the operation.
- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate other alerts associated with the user/host during the past 48 hours.

### False positive analysis

- This mechanism can be used legitimately. Check whether the user is an administrator and is legitimately performing troubleshooting.
- In case of an allowed benign true positive (B-TP), assess adding rules to allow needed traffic and re-enable the firewall.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Review the privileges assigned to the involved users to ensure that the least privilege principle is being followed.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
