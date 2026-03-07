---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Azure Kubernetes Services (AKS) Kubernetes Events Deleted" prebuilt detection rule.'
---

# Azure Kubernetes Services (AKS) Kubernetes Events Deleted

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Azure Kubernetes Services (AKS) Kubernetes Events Deleted

Azure Kubernetes Service (AKS) manages containerized applications using Kubernetes, which logs events like state changes. These logs are crucial for monitoring and troubleshooting. Adversaries may delete these logs to hide their tracks, impairing defenses. The detection rule identifies such deletions by monitoring specific Azure activity logs, flagging successful deletion operations to alert security teams of potential evasion tactics.

### Possible investigation steps

- Review the Azure activity logs to confirm the deletion event by checking for the operation name "MICROSOFT.KUBERNETES/CONNECTEDCLUSTERS/EVENTS.K8S.IO/EVENTS/DELETE" and ensure the event outcome is marked as "Success".
- Identify the user or service principal responsible for the deletion by examining the associated identity information in the activity logs.
- Investigate the timeline of events leading up to and following the deletion to identify any suspicious activities or patterns, such as unauthorized access attempts or configuration changes.
- Check for any other related alerts or anomalies in the Azure environment that might indicate a broader attack or compromise.
- Assess the impact of the deleted events by determining which Kubernetes resources or operations were affected and if any critical logs were lost.
- Review access controls and permissions for the user or service principal involved to ensure they align with the principle of least privilege and adjust if necessary.
- Consider implementing additional monitoring or alerting for similar deletion activities to enhance detection and response capabilities.

### False positive analysis

- Routine maintenance activities by authorized personnel may trigger deletion events. To manage this, create exceptions for known maintenance windows or specific user accounts responsible for these tasks.
- Automated scripts or tools used for log rotation or cleanup might delete events as part of their normal operation. Identify these scripts and exclude their activity from triggering alerts by whitelisting their associated service accounts or IP addresses.
- Misconfigured applications or services that inadvertently delete logs can cause false positives. Review application configurations and adjust them to prevent unnecessary deletions, and exclude these applications from alerts if they are verified as non-threatening.
- Test environments often generate log deletions during setup or teardown processes. Exclude these environments from monitoring or create specific rules that differentiate between production and test environments to avoid unnecessary alerts.

### Response and remediation

- Immediately isolate the affected Azure Kubernetes cluster to prevent further unauthorized access or tampering with logs.
- Conduct a thorough review of recent activity logs and access permissions for the affected cluster to identify any unauthorized access or privilege escalation.
- Restore deleted Kubernetes events from backups or snapshots if available, to ensure continuity in monitoring and auditing.
- Implement stricter access controls and audit logging for Kubernetes event deletion operations to prevent unauthorized deletions in the future.
- Notify the security operations team and relevant stakeholders about the incident for awareness and further investigation.
- Escalate the incident to the incident response team if there is evidence of broader compromise or if the deletion is part of a larger attack campaign.
- Review and update incident response plans to incorporate lessons learned from this event, ensuring quicker detection and response to similar threats in the future.

## Setup

The Azure Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
