---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "User Added to the Admin Group" prebuilt detection rule.
---

# User Added to the Admin Group

## Triage and analysis

To thoroughly investigate the actions that occurred **after a user was elevated to administrator**, it's essential to conduct a search on the Timeline. This allows you to review and understand the sequence of events that followed the elevation, helping to identify any potentially malicious or unauthorized activities that might have taken place. **Analyzing these actions is crucial for maintaining security and ensuring that the elevation was not exploited for harmful purposes.**

> **Note**:
> This investigation guide uses the [Investigate Markdown Plugin](https://www.elastic.co/guide/en/security/current/interactive-investigation-guides.html) introduced in Elastic Stack version 8.8.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

**Consider reviewing these actions:**

- Have persistency items been added?
- Is any software installed after elevation?
- Were any additional users created after elevation?

$investigate_0
$investigate_1
$investigate_2

