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

Attack discoveries are automatically saved each time they're generated. Once saved, discoveries remain available for later review, reporting, and tracking over time. This allows you to revisit discoveries to monitor trends, maintain audit trails, and support investigations as your environment evolves.

Where you manage saved discoveries depends on your version.

## Choose the right page for your version [choose-page]

The **Attack Discovery** page is your primary place to generate, save, and triage discoveries.

::::{note}
:applies_to: {stack: preview 9.4, serverless: preview}
If you turn on the [**Enable alerts and attacks alignment**](/solutions/security/get-started/configure-advanced-settings.md#enable-alerts-and-attacks-alignment) setting to display the **Attacks** page, you can split these tasks instead:

- Go to **Attack Discovery** to run LLM analysis on demand and create new attack discoveries.
- Go to **Attacks** for day-to-day triage of all attacks (manual and scheduled), and to manage their investigation lifecycle.
::::

<!-- In a future release (9.5 and serverless), the Attacks page becomes the only place to triage discoveries, replacing the Attack Discovery page's triage role, per docs-content#6949. Not documented yet per explicit instruction — revisit once shipped and confirmed. -->

## Next steps [next-steps]

- [Learn about Attack Discovery](/solutions/security/ai/attack-discovery/attack-discovery.md)
- [Investigate threats with Timeline](/solutions/security/investigate/timeline.md)
- [Manage security cases](/solutions/security/investigate/security-cases.md)
- [Automate attack triage with Elastic Workflows](/explore-analyze/workflows/use-cases/security/automate-security-operations/ai-driven-alert-triage.md)
