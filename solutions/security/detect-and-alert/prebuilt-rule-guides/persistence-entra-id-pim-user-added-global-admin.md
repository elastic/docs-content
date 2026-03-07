---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID Global Administrator Role Assigned (PIM User)" prebuilt detection rule.
---

# Entra ID Global Administrator Role Assigned (PIM User)

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Entra ID Global Administrator Role Assigned (PIM User)

Azure AD's Global Administrator role grants extensive access, allowing users to modify any administrative setting. Privileged Identity Management (PIM) helps manage and monitor such access. Adversaries may exploit this by adding themselves or others to this role, gaining persistent control. The detection rule identifies suspicious role additions by monitoring specific audit logs, focusing on successful role assignments to PIM users, thus helping to flag potential unauthorized access attempts.

### Possible investigation steps

- Review the Azure audit logs to confirm the details of the role addition event, focusing on the event.dataset:azure.auditlogs and azure.auditlogs.properties.category:RoleManagement fields.
- Identify the user account that was added to the Global Administrator role by examining the azure.auditlogs.properties.target_resources.*.display_name field.
- Check the event.outcome field to ensure the role addition was successful and not a failed attempt.
- Investigate the user account's recent activities and login history to determine if there are any anomalies or signs of compromise.
- Verify if the role addition aligns with any recent administrative changes or requests within the organization to rule out legitimate actions.
- Assess the potential impact of the role addition by reviewing the permissions and access levels granted to the user.
- If suspicious activity is confirmed, initiate a response plan to remove unauthorized access and secure the affected accounts.

### False positive analysis

- Routine administrative tasks may trigger alerts when legitimate IT staff are assigned the Global Administrator role for maintenance or updates. To manage this, create exceptions for known IT personnel or scheduled maintenance windows.
- Automated scripts or tools used for role assignments can cause false positives if they frequently add users to the Global Administrator role. Consider excluding these automated processes from monitoring or adjusting the detection rule to account for their activity.
- Temporary project-based role assignments might be flagged as suspicious. Implement a process to document and pre-approve such assignments, allowing for their exclusion from alerts.
- Training or onboarding sessions where new administrators are temporarily granted elevated access can result in false positives. Establish a protocol to notify the monitoring team of these events in advance, so they can be excluded from the detection rule.

### Response and remediation

- Immediately revoke the Global Administrator role from any unauthorized PIM user identified in the alert to prevent further unauthorized access.
- Conduct a thorough review of recent changes made by the affected account to identify any unauthorized modifications or suspicious activities.
- Reset the credentials of the compromised account and enforce multi-factor authentication (MFA) to secure the account against further unauthorized access.
- Notify the security team and relevant stakeholders about the incident for awareness and further investigation.
- Implement additional monitoring on the affected account and related systems to detect any further suspicious activities.
- Review and update access policies and role assignments in Azure AD to ensure that only necessary personnel have elevated privileges.
- Document the incident and response actions taken for future reference and to improve incident response procedures.

## Setup

The Azure Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
