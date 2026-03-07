---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "M365 Identity Login from Impossible Travel Location" prebuilt detection rule.
---

# M365 Identity Login from Impossible Travel Location

## Triage and analysis

### Investigating M365 Identity Login from Impossible Travel Location

Microsoft 365's cloud-based services enable global access, but this can be exploited by adversaries logging in from disparate locations within short intervals, indicating potential account compromise. The detection rule identifies such anomalies by analyzing login events for rapid geographic shifts, flagging suspicious activity that may suggest unauthorized access attempts.

### Possible investigation steps

- Review the user associated with these sign-ins to determine if the login attempt was legitimate or if further investigation is needed.
- Analyze the geographic locations of the logins to identify any patterns or anomalies that may indicate malicious activity.
- Review the ISP information for the login attempts to identify any unusual or suspicious providers.
- Review the authorization request type to understand the context of the login attempts and whether they align with the user's typical behavior.
- Analyze the client application used for the login attempts to determine if it is consistent with the user's normal usage patterns (Teams, Office, etc.)
- Analyze the user-agent associated with the login attempts to identify any unusual or suspicious patterns. These could also indicate mobile and endpoint logins causing false-positives.

### False positive analysis

- Users traveling or using VPNs may trigger this alert. Verify with the user if they were traveling or using a VPN at the time of the login attempt.
- Mobile access may also result in false positives, as users may log in from various locations while on the go.

### Response and remediation

- Investigate the login attempt further by checking for any additional context or related events that may provide insight into the user's behavior.
- If the login attempt is deemed suspicious, consider implementing additional security measures, such as requiring multi-factor authentication (MFA) for logins from unusual locations.
- Educate users about the risks of accessing corporate resources from unfamiliar locations and the importance of using secure connections (e.g., VPNs) when doing so.
- Monitor for any subsequent login attempts from the same location or IP address to identify potential patterns of malicious activity.
- Consider adding exceptions to this rule for the user or source application ID if the login attempts are determined to be legitimate and not a security concern.

