---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "GCP Pub/Sub Subscription Creation" prebuilt detection rule.'
---

# GCP Pub/Sub Subscription Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating GCP Pub/Sub Subscription Creation

Google Cloud Pub/Sub is a messaging service that enables asynchronous communication between applications by decoupling event producers and consumers. Adversaries might exploit this by creating unauthorized subscriptions to intercept or exfiltrate sensitive data streams. The detection rule monitors audit logs for successful subscription creation events, helping identify potential misuse by flagging unexpected or suspicious activity.

### Possible investigation steps

- Review the audit log entry associated with the alert to identify the user or service account responsible for the subscription creation by examining the `event.dataset` and `event.action` fields.
- Verify the legitimacy of the subscription by checking the associated project and topic details to ensure they align with expected configurations and business needs.
- Investigate the history of the user or service account involved in the subscription creation to identify any unusual or unauthorized activities, focusing on recent changes or access patterns.
- Assess the permissions and roles assigned to the user or service account to determine if they have the necessary privileges for subscription creation and whether these permissions are appropriate.
- Consult with relevant stakeholders or application owners to confirm whether the subscription creation was authorized and necessary for operational purposes.

### False positive analysis

- Routine subscription creation by automated deployment tools or scripts can trigger false positives. Identify and whitelist these tools by excluding their service accounts from the detection rule.
- Development and testing environments often create and delete subscriptions frequently. Exclude these environments by filtering out specific project IDs associated with non-production use.
- Scheduled maintenance or updates might involve creating new subscriptions temporarily. Coordinate with the operations team to understand regular maintenance schedules and adjust the rule to ignore these activities during known maintenance windows.
- Internal monitoring or logging services that create subscriptions for legitimate data collection purposes can be excluded by identifying their specific patterns or naming conventions and adding them to an exception list.

### Response and remediation

- Immediately review the audit logs to confirm the unauthorized subscription creation and identify the source, including the user or service account responsible for the action.
- Revoke access for the identified user or service account to prevent further unauthorized actions. Ensure that the principle of least privilege is enforced.
- Delete the unauthorized subscription to stop any potential data interception or exfiltration.
- Conduct a thorough review of all existing subscriptions to ensure no other unauthorized subscriptions exist.
- Notify the security team and relevant stakeholders about the incident for awareness and further investigation.
- Implement additional monitoring and alerting for subscription creation events to detect similar activities in the future.
- If applicable, report the incident to Google Cloud support for further assistance and to understand if there are any broader implications or vulnerabilities.

## Setup

The GCP Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
