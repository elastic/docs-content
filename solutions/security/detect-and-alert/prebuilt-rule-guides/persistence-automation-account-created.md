---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Azure Automation Account Created" prebuilt detection rule.
---

# Azure Automation Account Created

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Azure Automation Account Created

Azure Automation accounts facilitate the automation of management tasks and orchestration across cloud environments, enhancing operational efficiency. However, adversaries may exploit these accounts to establish persistence by automating malicious activities. The detection rule monitors the creation of these accounts by analyzing specific Azure activity logs, focusing on successful operations, to identify potential unauthorized or suspicious account creations.

### Possible investigation steps

- Review the Azure activity logs to confirm the creation of the Automation account by checking for the operation name "MICROSOFT.AUTOMATION/AUTOMATIONACCOUNTS/WRITE" and ensure the event outcome is marked as Success.
- Identify the user or service principal that initiated the creation of the Automation account by examining the associated user identity information in the activity logs.
- Investigate the context of the Automation account creation by reviewing recent activities performed by the identified user or service principal to determine if there are any other suspicious or unauthorized actions.
- Check the configuration and permissions of the newly created Automation account to ensure it does not have excessive privileges that could be exploited for persistence or lateral movement.
- Correlate the Automation account creation event with other security alerts or logs to identify any patterns or indicators of compromise that may suggest malicious intent.

### False positive analysis

- Routine administrative tasks may trigger the rule when legitimate users create Azure Automation accounts for operational purposes. To manage this, maintain a list of authorized personnel and their expected activities, and cross-reference alerts with this list.
- Automated deployment scripts or infrastructure-as-code tools might create automation accounts as part of their normal operation. Identify these scripts and exclude their associated activities from triggering alerts by using specific identifiers or tags.
- Scheduled maintenance or updates by cloud service providers could result in the creation of automation accounts. Verify the timing and context of the account creation against known maintenance schedules and exclude these from alerts if they match.
- Development and testing environments often involve frequent creation and deletion of resources, including automation accounts. Implement separate monitoring rules or environments for these non-production areas to reduce noise in alerts.

### Response and remediation

- Immediately review the Azure activity logs to confirm the creation of the Automation account and identify the user or service principal responsible for the action.
- Disable the newly created Azure Automation account to prevent any potential malicious automation tasks from executing.
- Conduct a thorough investigation of the user or service principal that created the account to determine if their credentials have been compromised or if they have acted maliciously.
- Reset credentials and enforce multi-factor authentication for the identified user or service principal to prevent unauthorized access.
- Review and adjust Azure role-based access control (RBAC) policies to ensure that only authorized personnel have the ability to create Automation accounts.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems or accounts have been compromised.
- Implement enhanced monitoring and alerting for future Automation account creations to quickly detect and respond to similar threats.

## Setup

The Azure Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
