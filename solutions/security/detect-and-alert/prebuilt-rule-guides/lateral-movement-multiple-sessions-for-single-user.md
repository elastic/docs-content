---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Multiple Okta Sessions Detected for a Single User" prebuilt detection rule.'
---

# Multiple Okta Sessions Detected for a Single User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Multiple Okta Sessions Detected for a Single User

Okta is a widely used identity management service that facilitates secure user authentication and access control. Adversaries may exploit Okta by hijacking session cookies, allowing unauthorized access to user accounts from different locations. The detection rule identifies anomalies by flagging multiple session initiations with distinct session IDs for the same user, excluding legitimate Okta system actors, thus highlighting potential unauthorized access attempts.

### Possible investigation steps

- Review the Okta logs to identify the specific user account associated with the multiple session initiations and note the distinct session IDs.
- Check the geographic locations and IP addresses associated with each session initiation to determine if there are any unusual or unexpected locations.
- Investigate the timestamps of the session initiations to see if they align with the user's typical login patterns or if they suggest simultaneous logins from different locations.
- Examine the okta.actor.id and okta.actor.display_name fields to ensure that the sessions were not initiated by legitimate Okta system actors.
- Contact the user to verify if they recognize the session activity and if they have recently logged in from multiple devices or locations.
- Assess if there are any other related security alerts or incidents involving the same user account that could indicate a broader compromise.

### False positive analysis

- Legitimate multiple device usage: Users may legitimately access their accounts from multiple devices, leading to multiple session initiations. To handle this, create exceptions for users who frequently use multiple devices for work.
- Frequent travel or remote work: Users who travel often or work remotely may trigger this rule due to accessing Okta from various locations. Consider setting up location-based exceptions for these users.
- Shared accounts: In environments where account sharing is common, multiple sessions may be expected. Implement policies to discourage account sharing or create exceptions for known shared accounts.
- Automated scripts or integrations: Some users may have automated processes that initiate multiple sessions. Identify these scripts and exclude them from the rule by their specific session patterns.
- Testing and development environments: Users involved in testing or development may generate multiple sessions as part of their work. Exclude these environments from the rule to prevent false positives.

### Response and remediation

- Immediately terminate all active sessions for the affected user account to prevent further unauthorized access.
- Reset the user's password and invalidate any existing session cookies to ensure that any stolen session cookies are rendered useless.
- Conduct a thorough review of recent login activity and session logs for the affected user to identify any suspicious or unauthorized access patterns.
- Notify the user of the potential compromise and advise them to verify any recent account activity for unauthorized actions.
- Escalate the incident to the security operations team for further investigation and to determine if additional accounts or systems may be affected.
- Implement multi-factor authentication (MFA) for the affected user account if not already in place, to add an additional layer of security against unauthorized access.
- Update and enhance monitoring rules to detect similar anomalies in the future, focusing on unusual session patterns and access from unexpected locations.

## Setup

The Okta Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
