---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "GCP Pub/Sub Subscription Deletion" prebuilt detection rule.'
---

# GCP Pub/Sub Subscription Deletion

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating GCP Pub/Sub Subscription Deletion

Google Cloud Pub/Sub is a messaging service that enables asynchronous communication between event producers and consumers. Subscriptions in Pub/Sub are crucial for message delivery to applications. Adversaries may delete subscriptions to disrupt communication, evade detection, or impair defenses. The detection rule monitors audit logs for successful subscription deletions, flagging potential defense evasion activities.

### Possible investigation steps

- Review the audit logs for the specific event.action: google.pubsub.v*.Subscriber.DeleteSubscription to identify the user or service account responsible for the deletion.
- Check the event.dataset:gcp.audit logs for any preceding or subsequent actions by the same user or service account to determine if there is a pattern of suspicious activity.
- Investigate the context of the deleted subscription by examining the associated project and any related resources to understand the potential impact on the application or service.
- Verify if the deletion aligns with any recent changes or maintenance activities within the organization to rule out legitimate actions.
- Assess the permissions and roles assigned to the user or service account to ensure they are appropriate and not overly permissive, which could indicate a security risk.
- Consult with the relevant application or service owners to confirm whether the subscription deletion was authorized and necessary.

### False positive analysis

- Routine maintenance activities by administrators may lead to subscription deletions that are not malicious. To manage this, create exceptions for known maintenance windows or specific admin accounts.
- Automated scripts or tools used for managing Pub/Sub resources might delete subscriptions as part of their normal operation. Identify these scripts and exclude their actions from triggering alerts by using service account identifiers.
- Development and testing environments often involve frequent creation and deletion of subscriptions. Exclude these environments from alerts by filtering based on project IDs or environment tags.
- Subscription deletions as part of a resource cleanup process can be non-threatening. Document and exclude these processes by identifying patterns in the audit logs, such as specific user agents or IP addresses associated with cleanup operations.

### Response and remediation

- Immediately verify the legitimacy of the subscription deletion by contacting the responsible team or individual to confirm if the action was authorized.
- If unauthorized, revoke access for the user or service account involved in the deletion to prevent further unauthorized actions.
- Restore the deleted subscription from backup or recreate it if necessary, ensuring that message delivery to the application is resumed.
- Conduct a thorough review of audit logs to identify any other suspicious activities or patterns that may indicate further compromise.
- Implement additional access controls and monitoring for Pub/Sub resources to prevent unauthorized deletions in the future.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems or data were affected.
- Update incident response plans and playbooks to include specific procedures for handling Pub/Sub subscription deletions and similar threats.

## Setup

The GCP Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
