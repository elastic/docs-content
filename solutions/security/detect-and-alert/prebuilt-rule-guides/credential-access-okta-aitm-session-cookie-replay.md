---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Okta AiTM Session Cookie Replay" prebuilt detection rule.'
---

# Okta AiTM Session Cookie Replay

## Triage and analysis

### Investigating Okta AiTM Session Cookie Replay

Adversary-in-the-Middle (AiTM) attacks use reverse proxies to intercept authentication flows, capturing session cookies after victims complete MFA. Attackers then replay these cookies from their own infrastructure to hijack authenticated sessions. This rule detects the post-capture phase by identifying sessions used from anomalous contexts.

This is an ES|QL aggregation-based rule. Pivot into raw events using the root session ID for full investigation context.

### Possible investigation steps

- Review the collected IP addresses from the alert to identify all IPs that accessed this session. Investigate geographic locations and ASN ownership for each IP.
- Examine the user agent values for non-browser user agents like `python-requests`, `curl`, or `Headless` browsers that indicate programmatic access.
- Check Okta's risk assessment fields. HIGH risk with reasons like "Anomalous Device" or "Anomalous Location" strengthens AiTM suspicion.
- Correlate the session start timestamp with the first replay attempt timestamp to understand the attack timeline.
- Query raw Okta events for the session ID to see all activity within this session, including accessed applications.
- Review proxy detection fields to determine if attacker requests originated from VPN/proxy infrastructure.
- Check the user's recent password reset or MFA enrollment events, as these may indicate account compromise leading to the AiTM attack.
- Contact the user to verify if they received phishing emails with links to suspicious login pages around the session start time.

### False positive analysis

- Legitimate VPN usage may cause IP address changes within a session. Check if both IPs belong to known corporate VPN ranges or the user's typical locations.
- Users traveling may show geographic IP changes. Correlate with travel schedules or expense reports if available.
- Browser extensions or security tools may modify user agents. Verify the user agent patterns match known tools in the environment.
- API integrations using user context may trigger non-browser UA detection. Exclude known service accounts.

### Response and remediation

- Immediately terminate all active sessions for the affected user via Okta Admin Console.
- Reset the user's password and require MFA re-enrollment to invalidate any captured credentials.
- Review and revoke any OAuth tokens or API keys associated with the user.
- Check Okta System Log for applications accessed during the suspicious session and assess data exposure.
- If downstream applications were accessed, coordinate with application owners to review access logs and potential data exfiltration.
- Block the attacker IP addresses at the network perimeter and add to threat intelligence feeds.
- Implement Okta sign-on policies that challenge or block sessions with HIGH risk scores or proxy detection.
- Consider enabling Okta ThreatInsight to automatically block known malicious IPs.
- Review email security logs for phishing attempts targeting the user around the session start time.
- Escalate to incident response if sensitive applications (AWS, Salesforce, email) were accessed from the attacker IP.
