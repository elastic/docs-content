---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "GCP Pub/Sub Topic Deletion" prebuilt detection rule.
---

# GCP Pub/Sub Topic Deletion

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating GCP Pub/Sub Topic Deletion

Google Cloud Platform's Pub/Sub service facilitates asynchronous messaging, allowing applications to communicate by publishing messages to topics. Deleting a topic can disrupt this communication, potentially as a tactic for defense evasion. Adversaries might exploit this by deleting topics to impair defenses or hide their tracks. The detection rule monitors audit logs for successful topic deletions, flagging potential misuse for further investigation.

### Possible investigation steps

- Review the audit logs for the specific event.action: google.pubsub.v*.Publisher.DeleteTopic to identify the exact time and user or service account responsible for the deletion.
- Investigate the event.dataset:gcp.audit logs around the same timeframe to identify any related activities or anomalies that might indicate malicious intent or unauthorized access.
- Check the event.outcome:success to confirm the deletion was completed successfully and correlate it with any reported service disruptions or issues in the affected applications.
- Assess the permissions and roles of the user or service account involved in the deletion to determine if they had legitimate access and reasons for performing this action.
- Contact the user or team responsible for the deletion to verify if the action was intentional and authorized, and gather any additional context or justification for the deletion.
- Review any recent changes in IAM policies or configurations that might have inadvertently allowed unauthorized topic deletions.

### False positive analysis

- Routine maintenance or updates by administrators can lead to legitimate topic deletions. To manage this, create exceptions for known maintenance periods or specific admin accounts.
- Automated scripts or tools that manage Pub/Sub topics might delete topics as part of their normal operation. Identify these scripts and exclude their actions from triggering alerts by using service account identifiers.
- Development and testing environments often involve frequent topic creation and deletion. Exclude these environments from monitoring by filtering based on project IDs or environment tags.
- Scheduled clean-up jobs that remove unused or temporary topics can trigger false positives. Document these jobs and adjust the detection rule to ignore deletions occurring during their execution times.
- Changes in project requirements or architecture might necessitate topic deletions. Ensure that such changes are communicated and documented, allowing for temporary exceptions during the transition period.

### Response and remediation

- Immediately assess the impact of the topic deletion by identifying affected services and applications that rely on the deleted topic for message flow.
- Restore the deleted topic from backup if available, or recreate the topic with the same configuration to resume normal operations.
- Notify relevant stakeholders, including application owners and security teams, about the incident and potential service disruptions.
- Review access logs and permissions to identify unauthorized access or privilege escalation that may have led to the topic deletion.
- Implement stricter access controls and permissions for Pub/Sub topics to prevent unauthorized deletions in the future.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if the deletion is part of a larger attack pattern.
- Enhance monitoring and alerting for Pub/Sub topic deletions to ensure rapid detection and response to similar incidents in the future.

## Setup

The GCP Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
