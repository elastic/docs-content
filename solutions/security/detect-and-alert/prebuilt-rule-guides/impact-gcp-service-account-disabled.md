---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "GCP Service Account Disabled" prebuilt detection rule.
---

# GCP Service Account Disabled

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating GCP Service Account Disabled

In Google Cloud Platform, service accounts are crucial for applications and VMs to perform authorized actions without user intervention. Adversaries may disable these accounts to disrupt services, impacting business operations. The detection rule identifies successful disablement actions in audit logs, signaling potential malicious activity by correlating specific event actions and outcomes, thus enabling timely investigation and response.

### Possible investigation steps

- Review the audit logs for the specific event.action:google.iam.admin.v*.DisableServiceAccount to identify the exact time and source of the disablement action.
- Identify the user or service account that performed the disablement by examining the actor information in the audit logs.
- Check for any recent changes or unusual activities associated with the disabled service account, such as modifications to permissions or roles.
- Investigate any related events or actions in the audit logs around the same timeframe to identify potential patterns or additional suspicious activities.
- Assess the impact of the disabled service account on business operations by determining which applications or services were using the account.
- Contact relevant stakeholders or application owners to verify if the disablement was authorized or if it was an unexpected action.

### False positive analysis

- Routine maintenance activities by administrators may involve disabling service accounts temporarily. To manage this, create exceptions for known maintenance periods or specific administrator actions.
- Automated scripts or tools used for testing or deployment might disable service accounts as part of their process. Identify these scripts and exclude their actions from triggering alerts by using specific identifiers or tags.
- Organizational policy changes or restructuring might lead to intentional service account disablement. Document these changes and update the detection rule to recognize these legitimate actions.
- Service accounts associated with deprecated or retired applications may be disabled as part of cleanup efforts. Maintain an updated list of such applications and exclude related disablement actions from alerts.

### Response and remediation

- Immediately isolate the affected service account by revoking its permissions to prevent further unauthorized actions.
- Review the audit logs to identify any other suspicious activities associated with the disabled service account and assess the potential impact on business operations.
- Re-enable the service account if it is determined to be legitimate and necessary for business functions, ensuring that it is secured with appropriate permissions and monitoring.
- Notify the security team and relevant stakeholders about the incident for awareness and further investigation.
- Implement additional monitoring and alerting for similar disablement actions on service accounts to detect and respond to future incidents promptly.
- Conduct a root cause analysis to understand how the service account was disabled and address any security gaps or misconfigurations that allowed the incident to occur.
- Consider implementing additional security measures such as multi-factor authentication and least privilege access to enhance the protection of service accounts.

## Setup

The GCP Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
