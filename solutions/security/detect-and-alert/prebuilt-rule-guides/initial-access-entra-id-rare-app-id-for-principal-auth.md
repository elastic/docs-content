---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID User Sign-in with Unusual Client" prebuilt detection rule.'
---

# Entra ID User Sign-in with Unusual Client

## Triage and analysis

### Investigating Entra ID User Sign-in with Unusual Client

This rule identifies rare Azure Entra apps IDs requesting authentication on-behalf-of a principal user. An adversary with stolen credentials may specify an Azure-managed app ID to authenticate on-behalf-of a user. This is a rare event and may indicate an attempt to bypass conditional access policies (CAP) and multi-factor authentication (MFA) requirements. The app ID specified may not be commonly used by the user based on their historical sign-in activity.

### Possible investigation steps

- Identify the source IP address from which the failed login attempts originated by reviewing `source.ip`. Determine if the IP is associated with known malicious activity using threat intelligence sources or if it belongs to a corporate VPN, proxy, or automation process.
- Analyze affected user accounts by reviewing `azure.signinlogs.properties.user_principal_name` to determine if they belong to privileged roles or high-value users. Look for patterns indicating multiple failed attempts across different users, which could suggest a password spraying attempt.
- Examine the authentication method used in `azure.signinlogs.properties.authentication_details` to identify which authentication protocols were attempted and why they failed. Legacy authentication methods may be more susceptible to brute-force attacks.
- Review the authentication error codes found in `azure.signinlogs.properties.status.error_code` to understand why the login attempts failed. Common errors include `50126` for invalid credentials, `50053` for account lockouts, `50055` for expired passwords, and `50056` for users without a password.
- Correlate failed logins with other sign-in activity by looking at `event.outcome`. Identify if there were any successful logins from the same user shortly after multiple failures or if there are different geolocations or device fingerprints associated with the same account.
- Review `azure.signinlogs.properties.app_id` to identify which applications were initiating the authentication attempts. Determine if these applications are Microsoft-owned, third-party, or custom applications and if they are authorized to access the resources.
- Check for any conditional access policies that may have been triggered by the failed login attempts by reviewing `azure.signinlogs.properties.authentication_requirement`. This can help identify if the failed attempts were due to policy enforcement or misconfiguration.

## False positive analysis

- Automated scripts or applications using non-interactive authentication may trigger this detection, particularly if they rely on legacy authentication protocols recorded in `azure.signinlogs.properties.authentication_protocol`.
- Corporate proxies or VPNs may cause multiple users to authenticate from the same IP, appearing as repeated failed attempts under `source.ip`.
- User account lockouts from forgotten passwords or misconfigured applications may show multiple authentication failures in `azure.signinlogs.properties.status.error_code`.
- Exclude known trusted IPs, such as corporate infrastructure, from alerts by filtering `source.ip`.
- Exclude known custom applications from `azure.signinlogs.properties.app_id` that are authorized to use non-interactive authentication.
- Ignore principals with a history of failed logins due to legitimate reasons, such as expired passwords or account lockouts, by filtering `azure.signinlogs.properties.user_principal_name`.
- Correlate sign-in failures with password reset events or normal user behavior before triggering an alert.

## Response and remediation

- Block the source IP address in `source.ip` if determined to be malicious.
- Reset passwords for all affected user accounts listed in `azure.signinlogs.properties.user_principal_name` and enforce stronger password policies.
- Ensure basic authentication is disabled for all applications using legacy authentication protocols listed in `azure.signinlogs.properties.authentication_protocol`.
- Enable multi-factor authentication (MFA) for impacted accounts to mitigate credential-based attacks.
- Review conditional access policies to ensure they are correctly configured to block unauthorized access attempts recorded in `azure.signinlogs.properties.authentication_requirement`.
- Review Conditional Access policies to enforce risk-based authentication and block unauthorized access attempts recorded in `azure.signinlogs.properties.authentication_requirement`.
- Implement a zero-trust security model by enforcing least privilege access and continuous authentication.
- Regularly review and update conditional access policies to ensure they are effective against evolving threats.
- Restrict the use of legacy authentication protocols by disabling authentication methods listed in `azure.signinlogs.properties.client_app_used`.
- Regularly audit authentication logs in `azure.signinlogs` to detect abnormal login behavior and ensure early detection of potential attacks.
- Regularly rotate client credentials and secrets for applications using non-interactive authentication to reduce the risk of credential theft.
