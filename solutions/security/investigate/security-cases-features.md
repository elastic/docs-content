---
navigation_title: Security case features
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/cases-open-manage.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-open-manage.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Security case features [security-cases-features]

{{elastic-sec}} includes additional case features beyond the core functionality. For general case management, refer to [](/explore-analyze/cases/manage-cases.md).

## Add Timelines [cases-timeline]

Attach [Timelines](/solutions/security/investigate/timeline.md) to cases to preserve your investigation context and share it with your team. When you link a Timeline, other analysts can see the exact queries, filters, and events you examined, making it easier to collaborate, hand off investigations, or document your evidence trail.

::::{tip}
To insert a Timeline link in the case description, click the Timeline icon (![Timeline icon](/solutions/images/security-add-timeline-button.png "title =20x20")).
::::

## Add events [cases-examine-events]

```{applies_to}
stack: ga 9.2
```

Attach events to cases to document suspicious activity and preserve evidence for your investigation. You can add events from Timeline or from the **Events** tab on the **Hosts**, **Network**, or **Users** pages. This helps you build a chronological record of what happened, share findings with your team, and support post-incident analysis. 

View attached events in the case's **Events** tab, where they're organized from newest to oldest. You can find the **Events** tab in the following places:

- {applies_to}`serverless:` {applies_to}`stack: ga 9.3+`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga =9.2`: Go to the case's details page.

## Add indicators [cases-indicators]

Attach [threat intelligence indicators](/solutions/security/investigate/indicators-of-compromise.md) to cases to document evidence of compromise and connect your investigation to known threats. This helps you correlate alerts with threat actor tactics, track IOCs across related incidents, and build a complete picture of an attack.