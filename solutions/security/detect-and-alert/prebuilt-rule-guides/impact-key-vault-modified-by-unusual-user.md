---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Azure Key Vault Modified" prebuilt detection rule.
---

# Azure Key Vault Modified

## Triage and analysis

### Investigating Azure Key Vault Modified

Azure Key Vault is a cloud service that safeguards encryption keys and secrets like certificates, connection strings, and passwords. It is crucial for managing sensitive data in Azure environments. Unauthorized modifications to Key Vaults can lead to data breaches or service disruptions. This rule detects modifications to Key Vaults, which may indicate potential security incidents or misconfigurations.

### Possible investigation steps
- Review the `azure.activitylogs.operation_name` field to identify the specific operation performed on the Key Vault. Common operations include `Microsoft.KeyVault/vaults/write` for modifications and `Microsoft.KeyVault/vaults/delete` for deletions.
- Check the `event.outcome` field to confirm the success of the operation. A successful outcome indicates that the modification or deletion was completed.
- Investigate the `azure.activitylogs.identity.principal_id` or `azure.activitylogs.identity.principal_name` fields to determine the user or service principal that performed the operation. This can help identify whether the action was authorized or potentially malicious.
- Analyze the `azure.activitylogs.resource_id` field to identify the specific Key Vault that was modified. This can help assess the impact of the change and whether it affects critical resources or applications.
- Cross-reference the time of the modification with other security events or alerts in the environment to identify any patterns or related activities that may indicate a coordinated attack or misconfiguration.
- Consult with relevant stakeholders or system owners to verify if the modification was planned or expected, and gather additional context if necessary.

### False positive analysis
- Routine maintenance activities by administrators can trigger alerts when they modify or delete Key Vaults. To manage this, create exceptions for known maintenance windows or specific administrator accounts.
- Automated scripts or tools used for Key Vault management might perform frequent updates or deletions, leading to false positives. Identify these scripts and exclude their operations from triggering alerts by using specific identifiers or tags.
- Changes made by authorized third-party services or integrations that manage Key Vault configurations can also result in false positives. Review and whitelist these services to prevent unnecessary alerts.
- Regular updates or deployments in a development or testing environment may cause alerts. Consider excluding these environments from monitoring or adjusting the rule to focus on production environments only.
- Temporary changes for troubleshooting or testing purposes might be flagged. Document these activities and use temporary exceptions to avoid false positives during these periods.

### Response and remediation
- Immediately isolate the affected Key Vault to prevent further unauthorized access or changes.
- Review the Azure activity logs to identify the specific operations performed on the Key Vault and their outcomes.
- Collaborate with security teams to assess the impact of the modifications and determine if any sensitive data was compromised.
- If unauthorized changes are confirmed, initiate incident response procedures, including notifying affected parties and conducting a thorough investigation.
- Implement additional monitoring and alerting for the affected Key Vault to detect any further suspicious activity.

