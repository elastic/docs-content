---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Remote Scheduled Task Creation via RPC" prebuilt detection rule.
---

# Remote Scheduled Task Creation via RPC

## Triage and analysis

### Remote Scheduled Task Creation via RPC

[Scheduled tasks](https://docs.microsoft.com/en-us/windows/win32/taskschd/about-the-task-scheduler) are a great mechanism for persistence and program execution. These features can be used remotely for a variety of legitimate reasons, but at the same time used by malware and adversaries. When investigating scheduled tasks that were set up remotely, one of the first steps should be to determine the original intent behind the configuration and to verify if the activity is tied to benign behavior such as software installation or any kind of network administrator work. One objective for these alerts is to understand the configured action within the scheduled task. This is captured within the registry event data for this rule and can be base64 decoded to view the value.

#### Possible investigation steps

- Review the TaskContent value to investigate the task configured action.
- Validate if the activity is not related to planned patches, updates, network administrator activity, or legitimate software installations.
- Further examination should include review of host-based artifacts and network logs from around when the scheduled task was created, on both the source and target machines.

### False positive analysis

- There is a high possibility of benign activity tied to the creation of remote scheduled tasks as it is a general feature within Windows and used for legitimate purposes for a wide range of activity. Any kind of context should be found to further understand the source of the activity and determine the intent based on the scheduled task's contents.

### Related rules

- Service Command Lateral Movement - d61cbcf8-1bc1-4cff-85ba-e7b21c5beedc
- Remotely Started Services via RPC - aa9a274d-6b53-424d-ac5e-cb8ca4251650
- Remote Scheduled Task Creation - 954ee7c8-5437-49ae-b2d6-2960883898e9

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Remove scheduled task and any other related artifacts.
- Review privileged account management and user account management settings. Consider implementing group policy object (GPO) policies to further restrict activity, or configuring settings that only allow administrators to create remote scheduled tasks.

