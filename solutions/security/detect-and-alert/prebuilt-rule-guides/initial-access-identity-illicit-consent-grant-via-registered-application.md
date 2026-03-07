---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "M365 Identity OAuth Illicit Consent Grant by Rare Client and User" prebuilt detection rule.
---

# M365 Identity OAuth Illicit Consent Grant by Rare Client and User

## Triage and analysis

### Investigating M365 Identity OAuth Illicit Consent Grant by Rare Client and User

Adversaries may register a malicious application in Microsoft Entra ID and trick users into granting excessive permissions via OAuth consent. These apps can access sensitive Microsoft 365 data—such as mail, profiles, and files—on behalf of the user once consent is granted. This activity is often initiated through spearphishing campaigns that direct the user to a pre-crafted OAuth consent URL.

This rule identifies a new consent grant to an application using Microsoft 365 audit logs. Additionally, this is a New Terms rule that will only trigger if the user and client ID have not been seen doing this activity in the last 14 days.

#### Possible investigation steps

- **Review the app in Entra ID**:
  - Go to **Enterprise Applications** in the Azure portal.
  - Search for the `AppId` or name from `o365.audit.ObjectId`.
  - Review granted API permissions and whether admin consent was required.
  - Check the `Publisher` and `Verified` status.

- **Assess the user who granted consent**:
  - Investigate `o365.audit.UserId` (e.g., `terrance.dejesus@...`) for signs of phishing or account compromise.
  - Check if the user was targeted in recent phishing simulations or campaigns.
  - Review the user’s sign-in logs for suspicious geolocation, IP, or device changes.

- **Determine scope and risk**:
  - Use the `ConsentContext_IsAdminConsent` and `ConsentContext_OnBehalfOfAll` flags to assess privilege level.
  - If `offline_access` or `Mail.Read` was granted, consider potential data exposure.
  - Cross-reference affected `Target` objects with known business-critical assets or data owners.

- **Correlate additional telemetry**:
  - Review logs from Defender for Cloud Apps (MCAS), Microsoft Purview, or other DLP tooling for unusual access patterns.
  - Search for `AppId` across your tenant to determine how widely it's used.

### False positive analysis

- Not all consent grants are malicious. Verify if the app is business-approved, listed in your app catalog, or commonly used by users in that role or department.
- Consent reasons like `WindowsAzureActiveDirectoryIntegratedApp` could relate to integrated services, though these still require verification.

### Response and remediation

- **If the app is confirmed malicious**:
  - Revoke OAuth consent using the [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/api/oauth2permissiongrant-delete).
  - Remove any related service principals from Entra ID.
  - Block the app via the Conditional Access "Grant" control or Defender for Cloud Apps policies.
  - Revoke refresh tokens and require reauthentication for affected users.
  - Notify end-users and IT of the potential exposure.
  - Activate your phishing or OAuth abuse response playbook.

- **Prevent future misuse**:
  - Enable the [Admin consent workflow](https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/configure-admin-consent-workflow) to restrict user-granted consent.
  - Audit and reduce overprivileged applications in your environment.
  - Consider using Defender for Cloud Apps OAuth app governance.


