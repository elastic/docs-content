---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "First Time Seen Commonly Abused Remote Access Tool Execution" prebuilt detection rule.
---

# First Time Seen Commonly Abused Remote Access Tool Execution

## Triage and analysis

### Investigating First Time Seen Commonly Abused Remote Access Tool Execution

Remote access software is a class of tools commonly used by IT departments to provide support by connecting securely to users' computers. Remote access is an ever-growing market where new companies constantly offer new ways of quickly accessing remote systems.

At the same pace as IT departments adopt these tools, the attackers also adopt them as part of their workflow to connect into an interactive session, maintain access with legitimate software as a persistence mechanism, drop malicious software, etc.

This rule detects when a remote access tool is seen in the environment for the first time in the last 15 days, enabling analysts to investigate and enforce the correct usage of such tools.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Check if the execution of the remote access tool is approved by the organization's IT department.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Contact the account owner and confirm whether they are aware of this activity.
  - If the tool is not approved for use in the organization, the employee could have been tricked into installing it and providing access to a malicious third party. Investigate whether this third party could be attempting to scam the end-user or gain access to the environment through social engineering.
- Investigate any abnormal behavior by the subject process, such as network connections, registry or file modifications, and any spawned child processes.

### False positive analysis

- If an authorized support person or administrator used the tool to conduct legitimate support or remote access, consider reinforcing that only tooling approved by the IT policy should be used. The analyst can dismiss the alert if no other suspicious behavior is observed involving the host or users.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Run a full scan using the antimalware tool in place. This scan can reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- If an unauthorized third party did the access via social engineering, consider improvements to the security awareness program.
- Enforce that only tooling approved by the IT policy should be used for remote access purposes and only by authorized staff.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

