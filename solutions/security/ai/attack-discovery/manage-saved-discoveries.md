---
navigation_title: Manage saved discoveries
description: "Choose where to triage saved Attack Discovery findings: the Attacks view or the Attack Discovery page."
applies_to:
  stack: ga 9.1
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Manage saved discoveries [manage-saved-discoveries]

Attack Discovery saves findings automatically after each run. From there you can update status, filter and search discoveries, take triage actions such as assign or open a case, and review linked alerts. Where you do that work depends on your version. Pick a guide from the following table based on your needs and version.

| Best for | Available in | Go to |
|---|---|---|
| Day-to-day triage of attack findings together with their related alerts, including assign, tag, filter, and case actions. | {applies_to}`stack: preview =9.4, ga 9.5+` {applies_to}`serverless: ga` | [Manage from the Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md) |
| Update status, share findings, run bulk actions, and search discoveries on the Attack Discovery page (primary before Attacks in {{stack}} 9.5). | {applies_to}`stack: ga 9.1-9.4` | [Manage from the Attack Discovery page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attack-discovery-page.md) |

:::{note}
:applies_to: {"stack": "ga 9.5+", "serverless": "ga"}
On the Elastic AI SOC Engine (EASE) tier, the **Attacks** view is unavailable. Use the [Attack Discovery page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attack-discovery-page.md) instead.
:::
