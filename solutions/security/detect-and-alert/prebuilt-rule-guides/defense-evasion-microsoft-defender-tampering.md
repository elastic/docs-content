---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Microsoft Windows Defender Tampering" prebuilt detection rule.'
---

# Microsoft Windows Defender Tampering

## Triage and analysis

### Investigating Microsoft Windows Defender Tampering

Microsoft Windows Defender is an antivirus product built into Microsoft Windows, which makes it popular across multiple environments. Disabling it is a common step in threat actor playbooks.

This rule monitors the registry for modifications that disable Windows Defender features.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Validate the activity is not related to planned patches, updates, network administrator activity, or legitimate software installations.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Examine which features have been disabled, and check if this operation is done under change management and approved according to the organization's policy.

### False positive analysis

- This mechanism can be used legitimately. Analysts can dismiss the alert if the administrator is aware of the activity, the configuration is justified (for example, it is being used to deploy other security solutions or troubleshooting), and no other suspicious activity has been observed.

### Related rules

- Windows Defender Disabled via Registry Modification - 2ffa1f1e-b6db-47fa-994b-1512743847eb
- Disabling Windows Defender Security Settings via PowerShell - c8cccb06-faf2-4cd5-886e-2c9636cfcb87

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Take actions to restore the appropriate Windows Defender antivirus configurations.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Review the privileges assigned to the user to ensure that the least privilege principle is being followed.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
