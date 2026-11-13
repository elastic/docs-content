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

Attack Discovery saves findings automatically after each run. From there you can update status, filter and search discoveries, take triage actions such as assign or open a case, and review linked alerts. Where you do that work depends on your subscription, version, and deployment:

| When to use this | Manage from | {{stack}} Enterprise | {{serverless-short}} Complete |
|---|---|:---:|:---:|
| Triage attack findings together with their related alerts, including assign, tag, filter, and case actions. | [**Attacks** view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md) | ✓ (9.4+) | ✓ |
| Update status, share findings, run bulk actions, and search discoveries. | [**Attack Discovery** page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attack-discovery-page.md) | ✓ (9.1–9.5 only) | — |

:::{note}
Attack Discovery isn't available with a {{stack}} Basic, Gold, or Platinum subscription, or in {{serverless-short}} Security Analytics Essentials projects.
:::

:::{dropdown} Manage discoveries in Elastic AI SOC Engine (EASE) projects
[EASE](/solutions/security/ai/ease/ease-intro.md) projects don't have the **Attacks** view. Manage attack discoveries from the [**Attack Discovery** page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attack-discovery-page.md).
:::
