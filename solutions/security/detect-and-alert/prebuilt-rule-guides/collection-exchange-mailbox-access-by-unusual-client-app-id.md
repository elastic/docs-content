---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "M365 Exchange Mailbox Accessed by Unusual Client" prebuilt detection rule.
---

# M365 Exchange Mailbox Accessed by Unusual Client

## Triage and Analysis

### Investigating M365 Exchange Mailbox Accessed by Unusual Client

This rule detects when a user accesses their mailbox using a client application that is not typically used by the user, which may indicate potential compromise or unauthorized access attempts. Adversaries may use custom or third-party applications to access mailboxes, bypassing standard security controls. First-party Microsoft applications are also abused after OAuth tokens are compromised, allowing adversaries to access mailboxes without raising suspicion.

### Possible investigation steps
- Review the `o365.audit.UserId` field to identify the user associated with the mailbox access.
- Check the `o365.audit.ClientAppId` field to determine which client application was used for the mailbox access. Look for unusual or unexpected applications or determine which first-party Microsoft applications are being abused.
- Review `o365.audit.ClientInfoString` to gather additional information about the client application used for the mailbox access.
- Examine `o365.audit.Folders.Path` to identify the specific mailbox folders accessed by the client application. This can help determine if sensitive information was accessed or if the access was legitimate.
- Ensure that `o365.audit.MailboxOwnerUPN` matches the `o365.audit.UserId` to confirm that the mailbox accessed belongs to the user identified in the `o365.audit.UserId` field.
- Review geolocation information to identify the location from which the mailbox access occurred. Look for any anomalies or unexpected locations that may indicate suspicious activity.
- Examine `o365.audit.Folders.FolderItems.Id` to identify the specific items accessed within the mailbox folders. This can help determine if sensitive information was accessed or if the access was legitimate.

### False positive analysis
- Legitimate users may access their mailboxes using new or different client applications, such as when switching to a new email client or using a mobile application. If this is expected behavior, consider adjusting the rule or adding exceptions for specific users or client applications.
- Users may access their mailboxes using custom or third-party applications that are authorized by the organization, such as CRM or ERP systems. If this is expected behavior, consider adjusting the rule or adding exceptions for specific applications.

### Response and remediation
- If the mailbox access is confirmed to be suspicious or unauthorized, take immediate action to revoke the access token and prevent further access.
- Disable the user account temporarily to prevent any potential compromise or unauthorized access.
- Examine the sensitivity of the mailbox data accessed and determine if any sensitive information was compromised.
- Rotate the user's credentials and enforce multi-factor authentication (MFA) to prevent further unauthorized access.
- Review the conditional access policies in place to ensure they are sufficient to prevent unauthorized access to sensitive resources.

