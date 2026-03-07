---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "M365 SharePoint Search for Sensitive Content" prebuilt detection rule.'
---

# M365 SharePoint Search for Sensitive Content

## Triage and Analysis

### Investigating M365 SharePoint Search for Sensitive Content

This rule detects search queries in SharePoint or OneDrive that contain sensitive terms. The Microsoft 365 Unified Audit Log captures the actual search query text in the `SearchQueryText` field, allowing detection of reconnaissance activity targeting credentials, financial data, PII, legal documents, or infrastructure information.

#### Possible Investigation Steps

- Identify who performed the search and determine if this user has a legitimate business need to search for this type of content.
- Review the exact search terms used. Multiple sensitive terms in one query are more suspicious.
- Determine if the search was via browser, automation tool (PnP PowerShell), or API.
- Review the source IP and correlate with the user's typical access patterns.
- Look for subsequent file download or access events from the same user/session within minutes of the search.
- Determine if the user is a member of roles that would legitimately search for sensitive content (HR, Finance, Legal, Security, Compliance).
- Check Azure AD sign-in logs for authentication anomalies (device code flow, unusual location).

### Response and Remediation

- If unauthorized search activity is confirmed, immediately review what files were accessed or downloaded following the search.
- Revoke the user's session tokens and require reauthentication with MFA.
- If the account was compromised, reset credentials and investigate the compromise vector.
- Review Data Loss Prevention (DLP) policies to ensure sensitive content is properly protected.
- Consider implementing sensitivity labels and access restrictions on high-value content.
