---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Modification of Boot Configuration" prebuilt detection rule.'
---

# Modification of Boot Configuration

## Triage and analysis

### Investigating Modification of Boot Configuration

Boot entry parameters, or boot parameters, are optional, system-specific settings that represent configuration options. These are stored in a boot configuration data (BCD) store, and administrators can use utilities like `bcdedit.exe` to configure these.

This rule identifies the usage of `bcdedit.exe` to:

- Disable Windows Error Recovery (recoveryenabled).
- Ignore errors if there is a failed boot, failed shutdown, or failed checkpoint (bootstatuspolicy ignoreallfailures).

These are common steps in destructive attacks by adversaries leveraging ransomware.

#### Possible investigation steps

- Investigate the script execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Assess whether this behavior is prevalent in the environment by looking for similar occurrences across hosts.
- Check if any files on the host machine have been encrypted.

### False positive analysis

- The usage of these options is not inherently malicious. Administrators can modify these configurations to force a machine to boot for troubleshooting or data recovery purposes.

### Related rules

- Deleting Backup Catalogs with Wbadmin - 581add16-df76-42bb-af8e-c979bfb39a59

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Consider isolating the involved host to prevent destructive behavior, which is commonly associated with this activity.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- If any other destructive action was identified on the host, it is recommended to prioritize the investigation and look for ransomware preparation and execution activities.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
