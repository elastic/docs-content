---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Credential Manipulation - Prevented - Elastic Endgame" prebuilt detection rule.'
---

# Credential Manipulation - Prevented - Elastic Endgame

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Credential Manipulation - Prevented - Elastic Endgame

Elastic Endgame is a security solution that prevents unauthorized credential manipulation, a tactic often used by adversaries to escalate privileges by altering access tokens. Attackers exploit this to gain elevated access within a system. The detection rule identifies such attempts by monitoring alerts for token manipulation events, leveraging Elastic Endgame's prevention capabilities to thwart these threats effectively.

### Possible investigation steps

- Review the alert details to confirm the presence of event.kind:alert and event.module:endgame, ensuring the alert is related to Elastic Endgame's prevention capabilities.
- Examine the event.action and endgame.event_subtype_full fields to identify the specific type of token manipulation event that was prevented.
- Investigate the source and destination of the alert by analyzing associated IP addresses, user accounts, and hostnames to determine if the attempt was internal or external.
- Check for any related alerts or logs around the same timeframe to identify potential patterns or coordinated attempts at credential manipulation.
- Assess the impacted system's current security posture and review recent changes or anomalies in user behavior that might have led to the attempted manipulation.
- Consult the MITRE ATT&CK framework for additional context on Access Token Manipulation (T1134) to understand potential adversary techniques and improve defensive measures.

### False positive analysis

- Routine administrative tasks involving legitimate token manipulation can trigger alerts. Review the context of the event to determine if it aligns with expected administrative activities.
- Automated scripts or software updates that modify access tokens as part of their normal operation may cause false positives. Identify these processes and consider adding them to an exception list if they are verified as non-threatening.
- Security tools or monitoring solutions that interact with access tokens for legitimate purposes might be flagged. Validate these tools and exclude them from the rule if they are confirmed to be safe.
- User behavior that involves frequent token changes, such as developers testing applications, can lead to false positives. Monitor these activities and create exceptions for known users or groups performing these tasks regularly.
- Ensure that the rule is not overly broad by refining the query to focus on specific actions or contexts that are more indicative of malicious behavior, reducing the likelihood of false positives.

### Response and remediation

- Immediately isolate the affected system to prevent further unauthorized access or lateral movement within the network.
- Revoke and reset any potentially compromised credentials associated with the affected system to mitigate unauthorized access.
- Conduct a thorough review of access logs and token usage to identify any unauthorized access or privilege escalation attempts.
- Restore the affected system from a known good backup to ensure the integrity of the system and its credentials.
- Implement additional monitoring on the affected system and related accounts to detect any further suspicious activity.
- Escalate the incident to the security operations team for a detailed investigation and to assess the potential impact on other systems.
- Review and update access control policies to ensure that only necessary permissions are granted, reducing the risk of privilege escalation.
