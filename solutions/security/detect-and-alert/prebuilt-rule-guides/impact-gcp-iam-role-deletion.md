---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "GCP IAM Role Deletion" prebuilt detection rule.
---

# GCP IAM Role Deletion

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating GCP IAM Role Deletion

Google Cloud Platform's IAM roles define permissions for actions on resources, crucial for managing access. Adversaries might delete roles to disrupt legitimate user access, hindering operations. The detection rule monitors audit logs for successful role deletions, signaling potential unauthorized access removal, thus aiding in identifying and mitigating such security threats.

### Possible investigation steps

- Review the audit logs for the specific event.action:google.iam.admin.v*.DeleteRole to identify the exact role that was deleted and the associated project or resource.
- Identify the user or service account responsible for the deletion by examining the actor information in the audit logs.
- Check the event.timestamp to determine when the role deletion occurred and correlate it with any other suspicious activities around the same time.
- Investigate the event.outcome:success to confirm that the role deletion was completed successfully and assess the potential impact on access and operations.
- Analyze the context of the deletion by reviewing recent changes or activities in the project or organization to understand if the deletion was part of a legitimate change or an unauthorized action.
- Contact the user or team responsible for the project to verify if the role deletion was intentional and authorized, and gather additional context if needed.

### False positive analysis

- Routine administrative actions may trigger alerts when roles are deleted as part of regular maintenance or restructuring. To manage this, create exceptions for known administrative accounts or scheduled maintenance windows.
- Automated scripts or tools that manage IAM roles might cause false positives if they delete roles as part of their operation. Identify these scripts and exclude their actions from triggering alerts by using specific service accounts or tags.
- Deletion of temporary or test roles used in development environments can be mistaken for malicious activity. Implement filters to exclude actions within designated development projects or environments.
- Changes in organizational structure or policy might necessitate role deletions, which could be misinterpreted as threats. Document and communicate these changes to the security team to adjust monitoring rules accordingly.
- Third-party integrations or services that manage IAM roles could inadvertently cause false positives. Ensure these services are properly documented and their actions are whitelisted if deemed non-threatening.

### Response and remediation

- Immediately revoke any active sessions and credentials associated with the deleted IAM role to prevent unauthorized access.
- Restore the deleted IAM role from a backup or recreate it with the same permissions to ensure legitimate users regain access.
- Conduct a thorough review of recent IAM activity logs to identify any unauthorized changes or suspicious activities related to IAM roles.
- Notify the security team and relevant stakeholders about the incident for awareness and further investigation.
- Implement additional monitoring on IAM role changes to detect and alert on any future unauthorized deletions promptly.
- Review and tighten IAM role permissions to ensure the principle of least privilege is enforced, reducing the risk of similar incidents.
- Consider enabling additional security features such as multi-factor authentication (MFA) for accounts with permissions to modify IAM roles.

## Setup

The GCP Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
