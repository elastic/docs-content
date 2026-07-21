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

Discoveries are saved automatically after Attack Discovery runs, so you can revisit them for review, reporting, and ongoing investigations. Use the table to open the guide that matches what you need to do.

## Choose the right page for your goal [choose-page]

| Best for | Available in | Go to |
|---|---|---|
| Day-to-day triage of attack findings together with their related alerts, including assign, tag, filter, and case actions. | {applies_to}`stack: preview =9.4, ga 9.5+` {applies_to}`serverless: ga` | [Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md) |
| Manage saved discoveries without alert-linked triage. Update status, share findings, run bulk actions, and search discoveries on the dedicated Attack Discovery UI (the primary manage surface before Attacks in {{stack}} 9.5). | {applies_to}`stack: ga 9.1-9.4` | [Attack Discovery page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attack-discovery-page.md) |

:::{note}
:applies_to: {"stack": "ga 9.5+", "serverless": "ga"}
On the Elastic AI SOC Engine (EASE) tier, the **Attacks** view is unavailable. Use the [Attack Discovery page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attack-discovery-page.md) instead.
:::
