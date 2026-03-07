---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Windows User Calling the Metadata Service" prebuilt detection rule.'
---

# Unusual Windows User Calling the Metadata Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Windows User Calling the Metadata Service

Cloud platforms provide a metadata service that allows instances to access configuration data, including credentials. Adversaries may exploit this by using compromised Windows accounts to query the service, aiming to harvest sensitive information. The detection rule leverages machine learning to identify atypical access patterns by Windows users, flagging potential credential access attempts.

### Possible investigation steps

- Review the alert details to identify the specific Windows user account involved in the unusual access to the metadata service.
- Check the timestamp of the access attempt to correlate with any known scheduled tasks or legitimate user activities.
- Investigate the source IP address and device from which the metadata service was accessed to determine if it aligns with expected user behavior or known assets.
- Examine recent login and access logs for the identified user account to detect any other suspicious activities or anomalies.
- Assess whether there have been any recent changes to the user's permissions or roles that could explain the access attempt.
- Look for any other alerts or incidents involving the same user account or device to identify potential patterns of malicious behavior.
- Consult with the user or their manager to verify if the access was legitimate or if the account may have been compromised.

### False positive analysis

- Routine administrative tasks by IT personnel may trigger alerts. Review access logs to confirm legitimate administrative actions and consider whitelisting specific user accounts or IP addresses.
- Automated scripts or scheduled tasks that query the metadata service for configuration updates can be mistaken for suspicious activity. Identify these scripts and exclude them from the rule by adding them to an exception list.
- Cloud management tools that regularly access the metadata service for monitoring or configuration purposes might be flagged. Verify these tools and create exceptions for their known access patterns.
- Instances where legitimate software updates or patch management processes access the metadata service should be reviewed. Document these processes and exclude them from triggering alerts.
- Temporary access by third-party vendors or consultants may appear unusual. Ensure their access is documented and create temporary exceptions during their engagement period.

### Response and remediation

- Immediately isolate the affected Windows system from the network to prevent further unauthorized access to the metadata service.
- Revoke any potentially compromised credentials identified during the investigation and issue new credentials to affected users.
- Conduct a thorough review of access logs to identify any unauthorized data access or exfiltration attempts from the metadata service.
- Implement additional monitoring on the affected system and similar systems to detect any further anomalous access attempts.
- Escalate the incident to the security operations center (SOC) for a deeper investigation into potential lateral movement or other compromised systems.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Review and enhance access controls and permissions for the metadata service to ensure only authorized users can access sensitive information.
