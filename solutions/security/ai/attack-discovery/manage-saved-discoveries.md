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

Which page you use to manage saved discoveries depends on what you're trying to do.

## Choose the right page for your goal [choose-page]

The **Attack Discovery** page is your primary place to generate, save, and triage discoveries.

If you'd rather split generation and triage into separate flows, you can instead:

- Go to **Attack Discovery** to run LLM analysis on demand and create new attack discoveries.
- Go to **Attacks** for day-to-day triage of all attacks (manual and scheduled), and to manage their investigation lifecycle.

::::{note}
:applies_to: {stack: preview 9.4, serverless: preview}
Splitting generation and triage into separate flows requires turning on the [**Enable alerts and attacks alignment**](/solutions/security/get-started/configure-advanced-settings.md#enable-alerts-and-attacks-alignment) setting to display the **Attacks** page.
::::

## Next steps [next-steps]

- [Learn about Attack Discovery](/solutions/security/ai/attack-discovery/attack-discovery.md)
- [Investigate threats with Timeline](/solutions/security/investigate/timeline.md)
- [Manage security cases](/solutions/security/investigate/security-cases.md)
- [Automate attack triage with Elastic Workflows](/explore-analyze/workflows/use-cases/security/automate-security-operations/ai-driven-alert-triage.md)
