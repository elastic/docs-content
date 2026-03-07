---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious SeIncreaseBasePriorityPrivilege Use" prebuilt detection rule.
---

# Suspicious SeIncreaseBasePriorityPrivilege Use

## Triage and analysis

### Investigating Suspicious SeIncreaseBasePriorityPrivilege Use

SeIncreaseBasePriorityPrivilege allows to increase the priority of processes running on the system so that the CPU scheduler allows them to pre-empt other lower priority processes when the higher priority process has something to do.

### Possible investigation steps

- Review the process.executable reputation and it's execution chain.
- Investiguate if the SubjectUserName is expected to perform this action.
- Correlate the event with other security alerts or logs to identify any patterns or additional suspicious activities that might suggest a broader attack campaign.
- Check the agent health status and verify if there is any tampering with endpoint security processes.

### False positive analysis

- Administrative tasks involving legitimate CPU scheduling priority changes.

### Response and remediation

- Immediately isolate the affected machine from the network to prevent further unauthorized access or lateral movement within the domain.
- Terminate the processes involved in the execution chain.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to ensure comprehensive remediation efforts are undertaken.
