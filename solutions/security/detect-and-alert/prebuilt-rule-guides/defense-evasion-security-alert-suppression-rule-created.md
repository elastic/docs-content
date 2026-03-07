---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Azure Diagnostic Settings Alert Suppression Rule Created or Modified" prebuilt detection rule.'
---

# Azure Diagnostic Settings Alert Suppression Rule Created or Modified

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Azure Diagnostic Settings Alert Suppression Rule Created or Modified

Azure Alert Suppression Rules are used to manage alert noise by filtering out known false positives. However, adversaries can exploit these rules to hide malicious activities by suppressing legitimate security alerts. The detection rule monitors Azure activity logs for successful operations related to suppression rule changes, helping identify potential misuse that could lead to defense evasion and reduced security visibility.

### Possible investigation steps

- Review the Azure activity logs to identify the specific suppression rule that was created or modified by filtering logs with the operation name "MICROSOFT.SECURITY/ALERTSSUPPRESSIONRULES/WRITE" and ensuring the event outcome is "success".
- Determine the identity of the user or service principal that performed the operation by examining the associated user or service account details in the activity logs.
- Investigate the context and justification for the creation or modification of the suppression rule by checking any related change management records or communications.
- Assess the impact of the suppression rule on security visibility by identifying which alerts are being suppressed and evaluating whether these alerts are critical for detecting potential threats.
- Cross-reference the suppression rule changes with recent security incidents or alerts to determine if there is any correlation or if the rule could have been used to hide malicious activity.
- Verify the legitimacy of the suppression rule by consulting with relevant stakeholders, such as security operations or cloud management teams, to confirm if the change was authorized and aligns with security policies.

### False positive analysis

- Routine maintenance activities by IT staff may trigger alerts when legitimate suppression rules are created or modified. To manage this, establish a baseline of expected changes and create exceptions for known maintenance periods or personnel.
- Automated processes or scripts that regularly update suppression rules for operational efficiency can generate false positives. Identify these processes and exclude their activity from alerting by using specific identifiers or tags associated with the automation.
- Changes made by trusted third-party security services that integrate with Azure might be flagged. Verify the legitimacy of these services and whitelist their operations to prevent unnecessary alerts.
- Frequent updates to suppression rules due to evolving security policies can lead to false positives. Document these policy changes and adjust the alerting criteria to accommodate expected modifications.
- Temporary suppression rules created during incident response to manage alert noise can be mistaken for malicious activity. Ensure these rules are documented and time-bound, and exclude them from alerting during the response period.

### Response and remediation

- Immediately review the Azure activity logs to confirm the creation or modification of the suppression rule and identify the user or service account responsible for the change.
- Temporarily disable the suspicious suppression rule to restore visibility into potential security alerts that may have been suppressed.
- Conduct a thorough investigation of recent alerts that were suppressed by the rule to determine if any malicious activities were overlooked.
- If malicious activity is confirmed, initiate incident response procedures to contain and remediate the threat, including isolating affected resources and accounts.
- Escalate the incident to the security operations team for further analysis and to assess the potential impact on the organization's security posture.
- Implement additional monitoring and alerting for changes to suppression rules to ensure any future modifications are promptly detected and reviewed.
- Review and update access controls and permissions for creating or modifying suppression rules to ensure only authorized personnel can make such changes.

## Setup

The Azure Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
