---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Windows Defender Disabled via Registry Modification" prebuilt detection rule.
---

# Windows Defender Disabled via Registry Modification

## Triage and analysis

### Investigating Windows Defender Disabled via Registry Modification

Microsoft Windows Defender is an antivirus product built into Microsoft Windows, which makes it popular across multiple environments. Disabling it is a common step in threat actor playbooks.

This rule monitors the registry for configurations that disable Windows Defender or the start of its service.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Validate the activity is not related to planned patches, updates, network administrator activity, or legitimate software installations.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Check if this operation was approved and performed according to the organization's change management policy.

### False positive analysis

- This mechanism can be used legitimately. Analysts can dismiss the alert if the administrator is aware of the activity, the configuration is justified (for example, it is being used to deploy other security solutions or troubleshooting), and no other suspicious activity has been observed.

### Related rules

- Disabling Windows Defender Security Settings via PowerShell - c8cccb06-faf2-4cd5-886e-2c9636cfcb87
- Microsoft Windows Defender Tampering - fe794edd-487f-4a90-b285-3ee54f2af2d3

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Re-enable Windows Defender and restore the service configurations to automatic start.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Review the privileges assigned to the user to ensure that the least privilege principle is being followed.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

