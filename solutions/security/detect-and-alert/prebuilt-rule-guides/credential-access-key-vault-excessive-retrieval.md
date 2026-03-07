---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Azure Key Vault Excessive Secret or Key Retrieved" prebuilt detection rule.
---

# Azure Key Vault Excessive Secret or Key Retrieved

## Triage and analysis

### Investigating Azure Key Vault Excessive Secret or Key Retrieved

Azure Key Vault is a cloud service that safeguards encryption keys and secrets like certificates, connection strings, and passwords. It is crucial for managing sensitive data in Azure environments. Unauthorized modifications to Key Vaults can lead to data breaches or service disruptions. This rule detects excessive secret or key retrieval operations from Azure Key Vault, which may indicate potential abuse or unauthorized access attempts.

### Possible investigation steps
- Review the `azure.platformlogs.identity.claim.upn` field to identify the user principal making the retrieval requests. This can help determine if the activity is legitimate or suspicious.
- Check the `azure.platformlogs.identity.claim.appid` or `azure.platformlogs.identity.claim.appid_display_name` to identify the application or service making the requests. If the application is not recognized or authorized, it may indicate a potential security incident. It is plausible that the application is a FOCI compliant application, which are commonly abused by adversaries to evade security controls or conditional access policies.
- Analyze the `azure.platformlogs.resource.name` field to determine which Key Vault is being accessed. This can help assess the impact of the retrieval operations and whether they target sensitive resources.
- Review the `event.action` field to confirm the specific actions being performed, such as `KeyGet`, `SecretGet`, or `CertificateGet`. These actions indicate retrieval of keys, secrets, or certificates from the Key Vault.
- Check the `source.ip` or `source.geo.*` fields to identify the source of the retrieval requests. Look for unusual or unexpected IP addresses, especially those associated with known malicious activity or geographic locations that do not align with the user's typical behavior.
- Use the `time_window` field to analyze the frequency of retrieval operations. If multiple retrievals occur within a short time frame (e.g., within a few minutes), it may indicate excessive or suspicious activity.
- Correlate the retrieval operations with other security events or alerts in the environment to identify any patterns or related incidents.
- Triage the user with Entra ID sign-in logs to gather more context about their authentication behavior and any potential anomalies.

### False positive analysis
- Routine administrative tasks or automated scripts may trigger excessive retrievals, especially in environments where Key Vaults are heavily utilized for application configurations or secrets management. If this is expected behavior, consider adjusting the rule or adding exceptions for specific applications or user principals.
- Legitimate applications or services may perform frequent retrievals of keys or secrets for operational purposes, such as configuration updates or secret rotation. If this is expected behavior, consider adjusting the rule or adding exceptions for specific applications or user principals.
- Security teams may perform periodic audits or assessments that involve retrieving keys or secrets from Key Vaults. If this is expected behavior, consider adjusting the rule or adding exceptions for specific user principals or applications.
- Some applications may require frequent access to keys or secrets for normal operation, leading to high retrieval counts. If this is expected behavior, consider adjusting the rule or adding exceptions for specific applications or user principals.

### Response and remediation
- Investigate the user principal making the excessive retrieval requests to determine if they are authorized to access the Key Vault and its contents. If the user is not authorized, take appropriate actions to block their access and prevent further unauthorized retrievals.
- Review the application or service making the requests to ensure it is legitimate and authorized to access the Key Vault. If the application is unauthorized or suspicious, consider blocking it and revoking its permissions to access the Key Vault.
- Assess the impact of the excessive retrieval operations on the Key Vault and its contents. Determine if any sensitive data was accessed or compromised during the retrievals.
- Implement additional monitoring and alerting for the Key Vault to detect any further suspicious activity or unauthorized access attempts.
- Consider implementing stricter access controls or policies for Key Vaults to limit excessive retrievals and ensure that only authorized users and applications can access sensitive keys and secrets.
- Educate users and administrators about the risks associated with excessive retrievals from Key Vaults and encourage them to follow best practices for managing keys and secrets in Azure environments.

