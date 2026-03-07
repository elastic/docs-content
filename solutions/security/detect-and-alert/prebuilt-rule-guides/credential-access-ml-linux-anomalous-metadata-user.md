---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Linux User Calling the Metadata Service" prebuilt detection rule.'
---

# Unusual Linux User Calling the Metadata Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Linux User Calling the Metadata Service

Cloud platforms provide a metadata service that allows instances to access configuration data, including credentials. Adversaries may exploit this by using unusual Linux users to query the service, aiming to extract sensitive information. The detection rule leverages machine learning to identify anomalous access patterns, focusing on credential access tactics, thus alerting analysts to potential threats.

### Possible investigation steps

- Review the alert details to identify the specific Linux user account that accessed the metadata service and the timestamp of the activity.
- Check the user's login history and recent activity on the system to determine if the access pattern is consistent with their normal behavior or if it appears suspicious.
- Investigate the source IP address and geolocation associated with the metadata service access to identify any anomalies or unexpected locations.
- Examine system logs and audit trails for any additional unauthorized or unusual access attempts around the same time frame.
- Verify if the user account has legitimate reasons to access the metadata service, such as running specific applications or scripts that require metadata information.
- Assess whether there have been any recent changes to user permissions or roles that could explain the access, and ensure that these changes were authorized.
- If suspicious activity is confirmed, consider isolating the affected instance and user account to prevent further unauthorized access while conducting a deeper investigation.

### False positive analysis

- Routine administrative scripts may access the metadata service for legitimate configuration purposes. To handle this, identify and whitelist these scripts to prevent unnecessary alerts.
- Automated backup or monitoring tools might query the metadata service as part of their normal operations. Exclude these tools by adding them to an exception list based on their user accounts or process identifiers.
- Scheduled tasks or cron jobs that require metadata access for updates or maintenance can trigger false positives. Review and document these tasks, then configure the rule to ignore these specific access patterns.
- Development or testing environments often simulate metadata service access to mimic production scenarios. Ensure these environments are recognized and excluded from the rule to avoid false alerts.
- Temporary user accounts created for specific projects or tasks may access the metadata service. Regularly audit these accounts and adjust the rule to exclude them if their access is deemed non-threatening.

### Response and remediation

- Immediately isolate the affected Linux instance from the network to prevent further unauthorized access or data exfiltration.
- Revoke any credentials or tokens that may have been exposed or accessed through the metadata service to prevent misuse.
- Conduct a thorough review of the instance's user accounts and permissions, removing any unauthorized or suspicious accounts and tightening access controls.
- Analyze system logs and metadata service access logs to identify the source and scope of the breach, focusing on the unusual user activity.
- Restore the affected instance from a known good backup if any unauthorized changes or malware are detected.
- Implement additional monitoring and alerting for metadata service access, particularly for unusual user accounts, to detect similar threats in the future.
- Escalate the incident to the security operations team for further investigation and to determine if additional instances or services are affected.
