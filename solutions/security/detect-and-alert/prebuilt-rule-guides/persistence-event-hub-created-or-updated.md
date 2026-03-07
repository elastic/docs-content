---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Azure Event Hub Authorization Rule Created or Updated" prebuilt detection rule.'
---

# Azure Event Hub Authorization Rule Created or Updated

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Azure Event Hub Authorization Rule Created or Updated

Azure Event Hub Authorization Rules manage access to Event Hubs via cryptographic keys, akin to administrative credentials. Adversaries may exploit these rules to gain unauthorized access or escalate privileges, potentially exfiltrating data. The detection rule monitors for the creation or modification of these rules, flagging successful operations to identify potential misuse or unauthorized changes.

### Possible investigation steps

- Review the Azure activity logs to identify the user or service principal associated with the operation by examining the `azure.activitylogs.operation_name` and `event.outcome` fields.
- Check the timestamp of the event to determine when the authorization rule was created or updated, and correlate this with any other suspicious activities around the same time.
- Investigate the specific Event Hub namespace affected by the rule change to understand its role and importance within the organization.
- Verify if the `RootManageSharedAccessKey` or any other high-privilege authorization rule was involved, as these carry significant risk if misused.
- Assess the necessity and legitimacy of the rule change by contacting the user or team responsible for the Event Hub namespace to confirm if the change was authorized and aligns with operational needs.
- Examine any subsequent access patterns or data transfers from the affected Event Hub to detect potential data exfiltration or misuse following the rule change.

### False positive analysis

- Routine administrative updates to authorization rules by IT staff can trigger alerts. To manage this, create exceptions for known administrative accounts or scheduled maintenance windows.
- Automated scripts or deployment tools that update authorization rules as part of regular operations may cause false positives. Identify these scripts and exclude their activity from alerts by filtering based on their service principal or user identity.
- Changes made by trusted third-party services integrated with Azure Event Hub might be flagged. Verify these services and exclude their operations by adding them to an allowlist.
- Frequent updates during development or testing phases can lead to false positives. Consider setting up separate monitoring profiles for development environments to reduce noise.
- Legitimate changes made by users with appropriate permissions might be misinterpreted as threats. Regularly review and update the list of authorized users to ensure only necessary personnel have access, and exclude their actions from alerts.

### Response and remediation

- Immediately revoke or rotate the cryptographic keys associated with the affected Event Hub Authorization Rule to prevent unauthorized access.
- Review the Azure Activity Logs to identify any unauthorized access or data exfiltration attempts that may have occurred using the compromised authorization rule.
- Implement conditional access policies to restrict access to Event Hub Authorization Rules based on user roles and network locations.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems or data have been compromised.
- Conduct a security review of all Event Hub Authorization Rules to ensure that only necessary permissions are granted and that the RootManageSharedAccessKey is not used in applications.
- Enhance monitoring and alerting for changes to authorization rules by integrating with a Security Information and Event Management (SIEM) system to detect similar threats in the future.

## Setup

The Azure Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
