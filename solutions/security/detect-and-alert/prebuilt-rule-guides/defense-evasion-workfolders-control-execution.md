---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Signed Proxy Execution via MS Work Folders" prebuilt detection rule.'
---

# Signed Proxy Execution via MS Work Folders

## Triage and analysis

### Investigating Signed Proxy Execution via MS Work Folders

Work Folders is a role service for file servers running Windows Server that provides a consistent way for users to access their work files from their PCs and devices. This allows users to store work files and access them from anywhere. When called, Work Folders will automatically execute any Portable Executable (PE) named control.exe as an argument before accessing the synced share.

Using Work Folders to execute a masqueraded control.exe could allow an adversary to bypass application controls and increase privileges.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
    - Examine the location of the WorkFolders.exe binary to determine if it was copied to the location of the control.exe binary. It resides in the System32 directory by default.
- Trace the activity related to the control.exe binary to identify any continuing intrusion activity on the host.
- Review the control.exe binary executed with Work Folders to determine maliciousness such as additional host activity or network traffic.
- Determine if control.exe was synced to sync share, indicating potential lateral movement.
- Review how control.exe was originally delivered on the host, such as emailed, downloaded from the web, or written to
disk from a separate binary.

### False positive analysis

- Windows Work Folders are used legitimately by end users and administrators for file sharing and syncing but not in the instance where a suspicious control.exe is passed as an argument.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Review the Work Folders synced share to determine if the control.exe was shared and if so remove it.
- If no lateral movement was identified during investigation, take the affected host offline if possible and remove the control.exe binary as well as any additional artifacts identified during investigation.
- Review integrating Windows Information Protection (WIP) to enforce data protection by encrypting the data on PCs using Work Folders.
- Confirm with the user whether this was expected or not, and reset their password.
