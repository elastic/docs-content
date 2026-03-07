---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Azure Diagnostic Settings Deleted" prebuilt detection rule.
---

# Azure Diagnostic Settings Deleted

## Triage and analysis

### Investigating Azure Diagnostic Settings Deleted

Azure Diagnostic Settings are crucial for monitoring and logging platform activities, sending data to various destinations for analysis. Adversaries may delete these settings to hinder detection and analysis of their activities, effectively evading defenses. The detection rule identifies such deletions by monitoring specific Azure activity logs for successful deletion operations, flagging potential defense evasion attempts.

### Possible investigation steps

- Identify the user or service principal responsible for the deletion by examining the associated user identity or service principal ID in the activity logs.
- If this is a service principal, determine which application is associated with it and examine credential use with authentication sources to identify potential compromise.
- Examine the resource group and subscription context to understand the scope of the deletion and whether it affects critical resources.
- Check the timestamp of the deletion event to determine when the diagnostic settings were removed and correlate this with other security events or alerts around the same time.
- Investigate the affected resources by identifying which diagnostic settings were deleted and assess the potential impact on monitoring and logging capabilities.
- Review any recent changes or activities performed by the identified user or service principal to determine if there are other suspicious actions that might indicate malicious intent.
- Assess the current security posture by ensuring that diagnostic settings are reconfigured and that logging and monitoring are restored to maintain visibility into platform activities.

### False positive analysis

- Examine the service principal or user account involved in the deletion to determine if it is part of an automated process or legitimate administrative activity.
- Automated scripts or tools used for managing Azure resources might delete diagnostic settings as part of their operation. Review and whitelist these scripts if they are verified as non-threatening.
- Changes in organizational policy or compliance requirements could lead to legitimate deletions. Confirm with relevant teams if such policy changes are in effect.
- Test environments often undergo frequent configuration changes, including the deletion of diagnostic settings. Consider excluding these environments from the rule or adjusting the rule to account for their unique behavior.
- Ensure that any third-party integrations or services with access to Azure resources are reviewed, as they might inadvertently delete diagnostic settings during their operations.

### Response and remediation

- Immediately isolate affected Azure resources to prevent further unauthorized changes or deletions. This may involve temporarily restricting access to the affected subscriptions or resource groups.
- Review the Azure activity logs to identify the source of the deletion request, including the user account, service principal and IP address involved. This will help determine if the action was authorized or malicious.
- Recreate the deleted diagnostic settings as soon as possible to restore logging and monitoring capabilities. Ensure that logs are being sent to secure and appropriate destinations.
- Conduct a thorough investigation of the user account or service principal involved in the deletion. If the account is compromised, reset credentials, and review permissions to ensure they are appropriate and follow the principle of least privilege.
- Escalate the incident to the security operations team for further analysis and to determine if additional resources or expertise are needed to address the threat.
- Implement additional monitoring and alerting for similar deletion activities to ensure rapid detection and response to future attempts.
- Review and update access controls and policies related to diagnostic settings to prevent unauthorized deletions, ensuring that only trusted and necessary personnel have the ability to modify these settings.

