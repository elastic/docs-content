---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "M365 OneDrive/SharePoint Excessive File Downloads" prebuilt detection rule.
---

# M365 OneDrive/SharePoint Excessive File Downloads

## Triage and Analysis

### Investigating M365 OneDrive/SharePoint Excessive File Downloads

This rule detects an excessive number of files downloaded from OneDrive using OAuth authentication. Threat actors may use OAuth phishing attacks, such as **Device Code Authentication phishing**, to obtain valid access tokens and perform unauthorized data exfiltration. This method allows adversaries to bypass traditional authentication mechanisms, making it a stealthy and effective technique.

This rule leverages ESQL aggregations which limit the field values available in the alert document. To investigate further, it is recommended to identify the original documents ingested.

#### Possible Investigation Steps

- Review the user ID field to identify the user who performed the downloads. Check if this user typically downloads large amounts of data from OneDrive.
- Correlate user ID with Entra Sign-In logs to verify the authentication method used and determine if it was expected for this user.
- Review the authentication method used. If OAuth authentication was used, investigate whether it was expected for this user.
- Identify the client application used for authentication. Determine if it is a legitimate enterprise-approved app or an unauthorized third-party application.
- Check the number of unique files downloaded. If a user downloads a high volume of unique files in a short period, it may indicate data exfiltration.
- Analyze the file types and directories accessed to determine if sensitive or confidential data was involved.
- Investigate the source IP address and geolocation of the download activity. If it originates from an unusual or anonymized location, further scrutiny is needed.
- Review other recent activities from the same user, such as file access, sharing, or permission changes, that may indicate further compromise.
- Check for signs of session persistence using OAuth. If Azure sign-in logs are correlated where `authentication_protocol` or `originalTransferMethod` field shows `deviceCode`, the session was established through device code authentication.
- Look for multiple authentication attempts from different devices or locations within a short timeframe, which could indicate unauthorized access.
- Investigate if other OAuth-related anomalies exist, such as consent grants for unfamiliar applications or unexpected refresh token activity.
- Review the `file.directory` value from the original documents to identify the specific folders or paths where the files were downloaded.
- Examine if the downloaded files are from Sharepoint or OneDrive by checking the `event.code` field.
- Review the incoming token type to determine how authentication occurred. If the `token.id` field is populated, it indicates that OAuth authentication was used, which may suggest an OAuth phishing attack.

### False Positive Analysis

- Verify if the user regularly downloads large batches of files as part of their job function.
- Determine if the downloads were triggered by an authorized automated process, such as a data backup or synchronization tool.
- Confirm if the detected OAuth application is approved for enterprise use and aligns with expected usage patterns.

### Response and Remediation

- If unauthorized activity is confirmed, revoke the OAuth token used and terminate active OneDrive sessions.
- Reset the affected user's password and require reauthentication to prevent continued unauthorized access.
- Restrict OAuth app permissions and enforce conditional access policies to limit authentication to trusted devices and applications.
- Monitor for additional signs of compromise, such as unusual email forwarding rules, external sharing of OneDrive files, or privilege escalation attempts.
- Educate users on OAuth phishing risks and encourage the use of **Microsoft Defender for Office 365 Safe Links** to mitigate credential-based attacks.
- Enable continuous monitoring for OAuth authentication anomalies using **Microsoft Entra ID sign-in logs** and security tools.

