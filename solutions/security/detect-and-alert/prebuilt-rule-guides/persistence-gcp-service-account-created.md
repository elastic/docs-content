---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "GCP Service Account Creation" prebuilt detection rule.'
---

# GCP Service Account Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating GCP Service Account Creation

In GCP, service accounts enable applications and VMs to interact with APIs securely. While essential for automation, they can be exploited if improperly managed. Adversaries might create service accounts to gain persistent access without detection. The detection rule monitors audit logs for successful service account creations, flagging potential unauthorized activities for further investigation.

### Possible investigation steps

- Review the audit logs for the specific event.action:google.iam.admin.v*.CreateServiceAccount to identify the time and source of the service account creation.
- Check the identity of the user or service that initiated the service account creation to determine if it aligns with expected administrative activities.
- Investigate the permissions and roles assigned to the newly created service account to assess if they are excessive or unusual for its intended purpose.
- Correlate the service account creation event with other recent activities in the environment to identify any suspicious patterns or anomalies.
- Verify if the service account is being used by any unauthorized applications or VMs by reviewing recent API calls and access logs associated with the account.

### False positive analysis

- Routine service account creation by automated deployment tools or scripts can trigger false positives. Identify and document these tools, then create exceptions in the monitoring system to exclude these known activities.
- Service accounts created by trusted internal teams for legitimate projects may also be flagged. Establish a process for these teams to notify security personnel of planned service account creations, allowing for pre-approval and exclusion from alerts.
- Scheduled maintenance or updates that involve creating temporary service accounts can result in false positives. Coordinate with IT operations to understand their schedules and adjust monitoring rules to accommodate these activities.
- Third-party integrations that require service accounts might be mistakenly flagged. Maintain an inventory of authorized third-party services and their associated service accounts to quickly verify and exclude these from alerts.

### Response and remediation

- Immediately disable the newly created service account to prevent any unauthorized access or actions.
- Review the IAM policy and permissions associated with the service account to ensure no excessive privileges were granted.
- Conduct a thorough audit of recent activities performed by the service account to identify any suspicious or unauthorized actions.
- Notify the security team and relevant stakeholders about the potential security incident for further investigation and coordination.
- Implement additional monitoring and alerting for service account creations to detect similar activities in the future.
- If malicious activity is confirmed, follow incident response procedures to contain and remediate any impact, including revoking access and conducting a security review of affected resources.
- Document the incident and response actions taken to improve future detection and response capabilities.

## Setup

The GCP Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
