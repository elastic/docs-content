---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Access to a Sensitive LDAP Attribute" prebuilt detection rule.'
---

# Access to a Sensitive LDAP Attribute

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Access to a Sensitive LDAP Attribute

LDAP (Lightweight Directory Access Protocol) is crucial for accessing and managing directory information in Active Directory environments. Adversaries may exploit LDAP to access sensitive attributes like passwords and decryption keys, facilitating credential theft or privilege escalation. The detection rule identifies unauthorized access attempts by monitoring specific event codes and attribute identifiers, excluding benign activities to reduce noise, thus highlighting potential security threats.

### Possible investigation steps

- Review the event logs for event code 4662 to identify the specific user or process attempting to access the sensitive LDAP attributes.
- Check the winlog.event_data.SubjectUserSid to determine the identity of the user or service account involved in the access attempt, excluding the well-known SID S-1-5-18 (Local System).
- Analyze the winlog.event_data.Properties field to confirm which sensitive attribute was accessed, such as unixUserPassword, ms-PKI-AccountCredentials, or msPKI-CredentialRoamingTokens.
- Investigate the context of the access attempt by correlating the event with other logs or alerts around the same timestamp to identify any suspicious patterns or activities.
- Verify the legitimacy of the access by checking if the user or process has a valid reason or permission to access the sensitive attributes, considering the organization's access control policies.
- Assess the potential impact of the access attempt on the organization's security posture, focusing on credential theft or privilege escalation risks.
- Document findings and, if necessary, escalate the incident to the appropriate security team for further action or remediation.

### False positive analysis

- Access by legitimate administrative accounts: Regular access by system administrators to sensitive LDAP attributes can trigger alerts. To manage this, create exceptions for known administrative accounts by excluding their SIDs from the detection rule.
- Scheduled system processes: Automated tasks or system processes that require access to certain LDAP attributes may cause false positives. Identify these processes and exclude their specific event codes or AccessMasks if they are consistently benign.
- Service accounts: Service accounts that perform routine directory operations might access sensitive attributes as part of their normal function. Exclude these accounts by adding their SIDs to the exception list to prevent unnecessary alerts.
- Monitoring tools: Security or monitoring tools that scan directory attributes for compliance or auditing purposes can generate false positives. Whitelist these tools by excluding their event sources or specific actions from the detection criteria.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Conduct a thorough review of the access logs to identify any unauthorized users or systems that accessed the sensitive LDAP attributes.
- Reset passwords and revoke any potentially compromised credentials associated with the affected accounts, focusing on those with access to sensitive attributes.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the scope of the breach.
- Implement additional monitoring on the affected systems and accounts to detect any further suspicious activities or attempts to access sensitive LDAP attributes.
- Review and update access controls and permissions for sensitive LDAP attributes to ensure they are restricted to only necessary personnel.
- Conduct a post-incident analysis to identify any gaps in security controls and update policies or procedures to prevent similar incidents in the future.
