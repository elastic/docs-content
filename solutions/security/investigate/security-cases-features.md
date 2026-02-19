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

## Timeline integration [cases-timeline]

You can integrate Timeline with your cases to provide additional context and investigation capabilities.

::::{tip}
You can insert a Timeline link in the case description by clicking the Timeline icon (![Timeline icon](/solutions/images/security-add-timeline-button.png "title =20x20")).
::::

For more information about Timeline, refer to [Timeline](/solutions/security/investigate/timeline.md).

## Add events [cases-examine-events]

```{applies_to}
stack: ga 9.2
```

Attach events to cases from Timeline or from the **Events** tab on the **Hosts**, **Network**, or **Users** pages. After adding events, view them in the case's **Events** tab, where they're organized from newest to oldest.

You can find the **Events** tab in the following places:

- {applies_to}`serverless:` {applies_to}`stack: ga 9.3+`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga =9.2`: Go to the case's details page.

## Add indicators [cases-indicators]

You can add threat intelligence indicators to cases for enhanced investigation. Refer to [Review indicator details in a case](/solutions/security/investigate/indicators-of-compromise.md#review-indicator-in-case) for more information.