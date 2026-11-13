---
navigation_title: Review and triage discoveries
description: "Learn whether to triage saved Attack Discovery findings in the Attacks view or on the Attack Discovery page, based on your version and deployment."
applies_to:
  stack: ga 9.1
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Manage saved discoveries [manage-saved-discoveries]

Attack Discovery saves findings automatically after each run. From there you can update status, filter and search discoveries, take triage actions such as assign or open a case, and review linked alerts. Where you do that work depends on your version and deployment.

| Best for | Available in | Go to |
|---|---|---|
| Day-to-day triage of attack findings together with their related alerts, including assign, tag, filter, and case actions. The **Attacks** view isn't available in [Elastic AI SOC Engine (EASE)](/solutions/security/ai/ease/ease-intro.md) projects. | {applies_to}`serverless: ga` {applies_to}`stack: preview =9.4, ga 9.5+` | [Manage from the Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md) |
| Update status, share findings, run bulk actions, and search discoveries on the **Attack Discovery** page. In {{serverless-short}}, only EASE projects include this page. | {applies_to}`serverless: ga` {applies_to}`stack: deprecated =9.5, ga 9.1-9.4` | [Manage from the Attack Discovery page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attack-discovery-page.md) |
