---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Azure Compute VM Command Executed" prebuilt detection rule.'
---

# Azure Compute VM Command Executed

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Azure Compute VM Command Executed

Azure Virtual Machines (VMs) allow users to run applications and services in the cloud. While roles like Virtual Machine Contributor can manage VMs, they typically can't access them directly. However, commands can be executed remotely via PowerShell, running as System. Adversaries may exploit this to execute unauthorized commands. The detection rule monitors Azure activity logs for command execution events, flagging successful operations to identify potential misuse.

### Possible investigation steps

- Review the Azure activity logs to identify the specific user or service principal that initiated the command execution event, focusing on the operation_name "MICROSOFT.COMPUTE/VIRTUALMACHINES/RUNCOMMAND/ACTION".
- Check the event.outcome field to confirm the success of the command execution and gather details about the command executed.
- Investigate the role and permissions of the user or service principal involved to determine if they have legitimate reasons to execute commands on the VM.
- Analyze the context of the command execution, including the time and frequency of the events, to identify any unusual patterns or anomalies.
- Correlate the command execution event with other logs or alerts from the same time period to identify any related suspicious activities or potential lateral movement.
- If unauthorized access is suspected, review the VM's security settings and access controls to identify and mitigate any vulnerabilities or misconfigurations.

### False positive analysis

- Routine maintenance tasks executed by IT administrators can trigger the rule. To manage this, create exceptions for known maintenance scripts or scheduled tasks that are regularly executed.
- Automated deployment processes that use PowerShell scripts to configure or update VMs may be flagged. Identify these processes and exclude them from the rule to prevent unnecessary alerts.
- Security tools or monitoring solutions that perform regular checks on VMs might execute commands that are benign. Whitelist these tools by identifying their specific command patterns and excluding them from detection.
- Development and testing environments often involve frequent command executions for testing purposes. Consider excluding these environments from the rule or setting up a separate monitoring policy with adjusted thresholds.
- Ensure that any exclusion or exception is documented and reviewed periodically to maintain security posture and adapt to any changes in the environment or processes.

### Response and remediation

- Immediately isolate the affected virtual machine from the network to prevent further unauthorized command execution and potential lateral movement.
- Review the Azure activity logs to identify the source of the command execution and determine if it was authorized or part of a larger attack pattern.
- Revoke any unnecessary permissions from users or roles that have the ability to execute commands on virtual machines, focusing on those with Virtual Machine Contributor roles.
- Conduct a thorough investigation of the executed commands to assess any changes or impacts on the system, and restore the VM to a known good state if necessary.
- Implement additional monitoring and alerting for similar command execution activities, ensuring that any future unauthorized attempts are detected promptly.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems or data may have been compromised.
- Review and update access control policies and role assignments to ensure that only necessary permissions are granted, reducing the risk of similar incidents in the future.

## Setup

The Azure Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
