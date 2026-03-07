---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID MFA TOTP Brute Force Attempted" prebuilt detection rule.
---

# Entra ID MFA TOTP Brute Force Attempted

## Triage and analysis

### Investigating Entra ID MFA TOTP Brute Force Attempted

This rule detects brute force attempts against Azure Entra multi-factor authentication (MFA) Time-based One-Time Password (TOTP) verification codes. It identifies high-frequency failed TOTP code attempts for a single user in a short time-span with a high number of distinct session IDs. Adversaries may programmatically attempt to brute-force TOTP codes by generating several sessions and attempting to guess the correct code.

#### Possible Investigation Steps:

    - Check the source addresses associated with the failed TOTP attempts.
    - Determine if the source IP address is consistent with the user’s typical login locations.
    - Look for unusual geographic patterns or anomalous IP addresses (e.g., proxies, VPNs, or locations outside the user’s normal activity).
    - Review the error code associated with the failed attempts. This can help identify if the failures are due to incorrect TOTP codes or other issues.
    - Verify that that auth metho reported is `OAth` as it indicates the use of TOTP codes.
    - Pivot into signin logs for the target user and check if auth via TOTP was successful which would indicate a successful brute force attempt.
    - Review conditional access policies applied to the user or group as reported by the sign-in logs.
    - Analyze the client application ID and display name to determine if the attempts are coming from a legitimate application or a potentially malicious script.
        - Adversaries may use legitimate FOCI applications to bypass security controls or make login attempts appear legitimate.
    - Review the resource ID access is being attempted against such as MyApps, Microsoft Graph, or other resources. This can help identify if the attempts are targeting specific applications or services.
    - The correlation IDs or session IDs can be used to trace the authentication attempts across different logs or systems. Note that for this specific behavior, unique session ID count is high and could be challenging to correlate.

#### False Positive Analysis:

    - Verify if the failed attempts could result from the user’s unfamiliarity with TOTP codes or issues with device synchronization.
    - Check if the user recently switched MFA methods or devices, which could explain multiple failures.
    - Determine if this is whitebox testing or a developer testing MFA integration.

#### Response and Remediation:

    - If proven malicious, lock the affected account temporarily to prevent further unauthorized attempts.
    - Notify the user of suspicious activity and validate their access to the account.
    - Reset passwords and MFA settings for the affected user to prevent unauthorized access while communicating with the user.
    - Ensure conditional access policies are configured to monitor and restrict anomalous login behavior.
    - Consider a different MFA method or additional security controls to prevent future bypass attempts.
    - Implement additional monitoring to track high-frequency authentication failures across the environment.
    - Audit historical logs for similar patterns involving other accounts to identify broader threats.
    - Provide guidance on the secure use of MFA and the importance of recognizing and reporting suspicious activity.

