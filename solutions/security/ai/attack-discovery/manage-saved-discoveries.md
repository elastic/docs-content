---
navigation_title: Manage saved discoveries
applies_to:
  stack: ga 9.1
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Manage saved discoveries [manage-saved-discoveries]

Attack discoveries are automatically saved on the **Attack Discovery** page each time you generate them. Once saved, discoveries remain available for later review, reporting, and tracking over time. This allows you to revisit discoveries to monitor trends, maintain audit trails, and support investigations as your environment evolves.

<!-- 9.5 unifies manual and scheduled attacks into the Attacks page (docs-content#6949) and may eventually restrict this legacy view/manage flow to the EASE tier once the Attacks page GA-promotes (item 7 of that issue). That update will be doc'd in a separate PR once item 7 lands — not included here. -->

## Compare the Attack Discovery and Attacks pages [compare-pages]

Discoveries and attacks can be managed from two different places in {{elastic-sec}}:

* [Manage discoveries on the Attack Discovery page](/solutions/security/ai/attack-discovery/manage-discoveries.md), where discoveries are generated and saved.
* {applies_to}`stack: preview 9.4` {applies_to}`serverless: preview` [Use the Attacks page](/solutions/security/ai/attack-discovery/attacks-page.md), a unified triage view that correlates attacks with their alerts.

Some tasks are available from only one page, and some are available from both. Use the following table to find where to go:

| Task | Attack Discovery page | Attacks page |
|---|---|---|
| Change status | [✓](/solutions/security/ai/attack-discovery/manage-discoveries.md#discovery-status) | [✓](/solutions/security/ai/attack-discovery/attacks-page.md#change-attack-status) |
| Share a discovery | [✓](/solutions/security/ai/attack-discovery/manage-discoveries.md#share-attack-discoveries) | — |
| Take bulk actions | [✓](/solutions/security/ai/attack-discovery/manage-discoveries.md#take-bulk-actions) | — |
| Search and filter | [✓](/solutions/security/ai/attack-discovery/manage-discoveries.md#search-filter-discoveries) | [✓](/solutions/security/ai/attack-discovery/attacks-page.md#attacks-filter-search) |
| Schedule discovery runs | [✓](/solutions/security/ai/attack-discovery/schedule-discoveries.md) | [✓](/solutions/security/ai/attack-discovery/attacks-page.md#attacks-schedule-discoveries) |
| View overview visualizations | — | [✓](/solutions/security/ai/attack-discovery/attacks-page.md#attacks-how-it-works) |
| Assign or unassign | — | [✓](/solutions/security/ai/attack-discovery/attacks-page.md#assign-attacks) |
| Apply tags | — | [✓](/solutions/security/ai/attack-discovery/attacks-page.md#apply-attack-tags) |
| Run a workflow | — | [✓](/solutions/security/ai/attack-discovery/attacks-page.md#run-workflow-from-attack) |
| Add to case | [✓](/solutions/security/ai/attack-discovery/attack-discovery.md#attack-discovery-workflows) | [✓](/solutions/security/ai/attack-discovery/attacks-page.md#attacks-add-to-case) |
| Investigate in Timeline | [✓](/solutions/security/ai/attack-discovery/attack-discovery.md#attack-discovery-workflows) | [✓](/solutions/security/ai/attack-discovery/attacks-page.md#attacks-investigate-timeline) |
| View in AI chat | [✓](/solutions/security/ai/attack-discovery/attack-discovery.md#attack-discovery-workflows) | [✓](/solutions/security/ai/attack-discovery/attacks-page.md#attacks-view-in-ai-chat) |

## Next steps [next-steps]

- [Learn about Attack Discovery](/solutions/security/ai/attack-discovery/attack-discovery.md)
- [Investigate threats with Timeline](/solutions/security/investigate/timeline.md)
- [Manage security cases](/solutions/security/investigate/security-cases.md)
- [Automate attack triage with Elastic Workflows](/explore-analyze/workflows/use-cases/security/automate-security-operations/ai-driven-alert-triage.md)
