---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID Sharepoint or OneDrive Accessed by Unusual Client" prebuilt detection rule.'
---

# Entra ID Sharepoint or OneDrive Accessed by Unusual Client

## Triage and analysis

### Investigating Entra ID Sharepoint or OneDrive Accessed by Unusual Client

This rule identifies when an application accesses SharePoint Online or OneDrive for Business for the first time in the tenant. This is a critical signal for detecting successful OAuth phishing campaigns, where adversaries trick users into granting consent to malicious applications. Once consent is granted, the malicious app can persistently access file storage without further user interaction. This detection also catches illicit consent grants, compromised third-party applications, or custom malicious apps registered by adversaries.

### Possible Investigation Steps:

- Identify the Application: Review `azure.signinlogs.properties.app_id` and `azure.signinlogs.properties.app_display_name` to determine which application accessed SharePoint. Cross-reference with known legitimate applications in your environment.
- Check Application Registration: Search Entra ID app registrations for the app ID. Determine if it's a first-party Microsoft app, known third-party integration, or suspicious/unknown application.
- Review Consent History: Investigate when and how consent was granted. Check `azure.auditlogs` for recent `Consent to application` events matching this app ID. Identify which user granted consent and whether it was admin or user consent.
- Analyze Permissions Granted: Review the OAuth scopes and permissions granted to the application. Look for overly broad permissions (e.g., `Files.ReadWrite.All`, `Sites.ReadWrite.All`) that exceed business requirements.
- Correlate with User Activity: Check if the user who granted consent recently received phishing emails, clicked suspicious links, or reported potential phishing attempts.
- Inspect Source IP and Location: Review `source.ip` and `source.geo.*` fields. Determine if the sign-in originated from expected locations or suspicious infrastructure (VPNs, data centers, anonymizers).
- Review Application Publisher: Check if the application is verified by Microsoft or has a suspicious/generic publisher name. Unverified applications with generic names (e.g., "File Viewer", "Document Manager") are common in phishing.
- Check for Data Access: Review subsequent SharePoint audit logs to see what files/sites the application accessed after gaining consent.
- Conditional Access Evaluation: Review `azure.signinlogs.properties.applied_conditional_access_policies` to determine if any security controls were bypassed or if the application should have been blocked.

### False Positive Analysis

- New Legitimate Integrations: Newly deployed third-party SaaS applications (e.g., document management, collaboration tools) that integrate with SharePoint will trigger this detection during initial setup. Validate with IT/procurement teams.
- Microsoft First-Party Applications: This rule excludes common Microsoft first-party apps (Office 365 SharePoint Online, OneDrive SyncEngine, OneDrive iOS App, Microsoft Office, SharePoint Web Client Extensibility, Microsoft Teams, Office 365 Exchange Online, and other Microsoft-owned app IDs). However, new Microsoft applications or features may still appear. Cross-reference unfamiliar app IDs against Microsoft's first-party app list.
- Development/Testing: Developers testing OAuth flows or building internal applications may generate alerts in development or staging environments.
- Organizational Changes: Mergers, acquisitions, or tenant migrations may introduce legitimate applications from partner organizations accessing SharePoint for the first time.

### Response and Remediation

- Immediate Actions if Malicious:
  - Revoke consent for the malicious application immediately via Entra ID > Enterprise Applications
  - Revoke all active sessions and refresh tokens for affected users
  - Disable the application's service principal to prevent further access
  - Review and remediate any data accessed by the application using SharePoint audit logs
- User Notification: Contact users who granted consent to inform them of the phishing attempt and provide security awareness training on identifying malicious OAuth consent requests
- Conditional Access Hardening: Implement or strengthen Conditional Access policies to:
  - Require admin consent for high-risk permissions (Files.ReadWrite.All, Sites.ReadWrite.All)
  - Block unverified publishers from accessing sensitive resources
  - Enforce device compliance and MFA for application access
- Tenant-Wide Review: Audit all application consents across the tenant to identify other potentially malicious applications that may have gained access through similar campaigns
- Monitor for Campaign Patterns: Check if the same malicious application targeted multiple users, indicating an organized phishing campaign. Coordinate with email security teams to identify and block phishing emails used in the campaign.
