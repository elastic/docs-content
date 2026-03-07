---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Credential Manipulation - Detected - Elastic Endgame" prebuilt detection rule.
---

# Credential Manipulation - Detected - Elastic Endgame

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Credential Manipulation - Detected - Elastic Endgame

Elastic Endgame is a security solution that monitors and detects suspicious activities, such as credential manipulation, which adversaries exploit to escalate privileges by altering access tokens. This detection rule identifies such threats by analyzing alerts for token manipulation events, leveraging its high-risk score and severity to prioritize investigation. The rule aligns with MITRE ATT&CK's framework, focusing on privilege escalation tactics.

### Possible investigation steps

- Review the alert details to confirm the presence of event.kind:alert and event.module:endgame, ensuring the alert is relevant to Elastic Endgame's detection capabilities.
- Examine the event.action and endgame.event_subtype_full fields for token_manipulation_event to understand the specific type of credential manipulation detected.
- Check the associated user account and system involved in the alert to determine if the activity aligns with expected behavior or if it indicates potential unauthorized access.
- Investigate the timeline of events leading up to and following the token manipulation event to identify any additional suspicious activities or patterns.
- Correlate the alert with other security events or logs to assess if this incident is part of a broader attack or isolated.
- Evaluate the risk score and severity to prioritize the response and determine if immediate action is required to mitigate potential threats.

### False positive analysis

- Routine administrative tasks involving token manipulation can trigger alerts. Review the context of the event to determine if it aligns with expected administrative behavior.
- Automated scripts or software updates that require token changes might be flagged. Identify and whitelist these processes if they are verified as safe and necessary for operations.
- Security tools or monitoring solutions that interact with access tokens for legitimate purposes may cause false positives. Ensure these tools are recognized and excluded from triggering alerts.
- User behavior analytics might misinterpret legitimate user actions as suspicious. Regularly update user profiles and behavior baselines to minimize these occurrences.
- Scheduled maintenance activities that involve access token modifications should be documented and excluded from detection rules during their execution time.

### Response and remediation

- Isolate the affected system immediately to prevent further unauthorized access or lateral movement within the network.
- Revoke and reset any compromised credentials or access tokens identified in the alert to prevent further misuse.
- Conduct a thorough review of recent access logs and token usage to identify any unauthorized access or actions taken by the adversary.
- Apply security patches and updates to the affected system and any related systems to close vulnerabilities that may have been exploited.
- Implement enhanced monitoring on the affected system and related accounts to detect any further suspicious activity or attempts at credential manipulation.
- Notify the security team and relevant stakeholders about the incident, providing details of the threat and actions taken, and escalate to higher management if the threat level increases.
- Review and update access control policies and token management practices to prevent similar incidents in the future, ensuring that least privilege principles are enforced.
