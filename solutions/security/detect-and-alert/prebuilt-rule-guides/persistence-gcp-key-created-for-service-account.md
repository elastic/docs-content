---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "GCP Service Account Key Creation" prebuilt detection rule.'
---

# GCP Service Account Key Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating GCP Service Account Key Creation

In GCP, service accounts are crucial for applications to authenticate and interact with Google services securely. They use cryptographic keys for API access, which, if mismanaged, can be exploited by adversaries to gain unauthorized access. The detection rule monitors audit logs for new key creations, flagging potential misuse by identifying successful key generation events, thus helping to mitigate risks associated with unauthorized access.

### Possible investigation steps

- Review the audit logs for the specific event.action: google.iam.admin.v*.CreateServiceAccountKey to identify the service account involved in the key creation.
- Check the event.dataset:gcp.audit logs to determine the user or process that initiated the key creation and verify if it aligns with expected behavior or scheduled tasks.
- Investigate the permissions and roles assigned to the service account to assess the potential impact of the new key being used maliciously.
- Examine the event.outcome:success logs to confirm the successful creation of the key and cross-reference with any recent changes or deployments that might justify the key creation.
- Contact the owner or responsible team for the service account to verify if the key creation was authorized and necessary for their operations.
- Review any recent alerts or incidents related to the service account to identify patterns or repeated unauthorized activities.

### False positive analysis

- Routine key rotations by automated processes can trigger alerts. To manage this, identify and whitelist these processes by their service account names or associated metadata.
- Development and testing environments often generate new keys frequently. Exclude these environments from alerts by using environment-specific tags or labels.
- Scheduled maintenance activities by cloud administrators may involve key creation. Document these activities and create exceptions based on the timing and user accounts involved.
- Third-party integrations that require periodic key updates can cause false positives. Maintain a list of trusted third-party services and exclude their key creation events from alerts.
- Internal tools or scripts that programmatically create keys for operational purposes should be reviewed and, if deemed safe, added to an exception list based on their execution context.

### Response and remediation

- Immediately revoke the newly created service account key to prevent unauthorized access. This can be done through the GCP Console or using the gcloud command-line tool.
- Conduct a thorough review of the service account's permissions to ensure they are aligned with the principle of least privilege. Remove any unnecessary permissions that could be exploited.
- Investigate the source of the key creation event by reviewing audit logs to identify the user or process responsible for the action. Determine if the action was authorized or if it indicates a potential compromise.
- If unauthorized access is suspected, rotate all keys associated with the affected service account and any other potentially compromised accounts to mitigate further risk.
- Implement additional monitoring and alerting for unusual service account activities, such as unexpected key creations or permission changes, to enhance detection of similar threats in the future.
- Escalate the incident to the security team for further investigation and to determine if additional containment or remediation actions are necessary, including notifying affected stakeholders if a breach is confirmed.

## Setup

The GCP Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
