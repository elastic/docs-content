---
navigation_title: Manual runs
description: "Manually run Attack Discovery from the Attacks view, or from the Attack Discovery page in 9.4."
applies_to:
  stack: preview =9.4, ga 9.5+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Manually run Attack Discovery from the Attacks view [manual-runs-from-attacks-page]

Manually run Attack Discovery when you want to analyze the current alert selection right away, for example after you change settings or during an active investigation. Discoveries from a manual run appear in the **Attacks** table alongside scheduled discoveries.

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.5+", "serverless": {"security": "ga"} }

To manually run Attack Discovery from the **Attacks** view:

1. Go to **Detections** → **Views** → **Attacks**.
2. Select **Settings** next to **Run** to open the **Attack discovery settings** flyout.
3. [Configure Attack Discovery settings](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md). Under **Generation**, confirm an LLM connector is selected. If you don't already have one, refer to [Configure access to LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md).
4. Start the run. Select **Save and run** in the flyout, or close the flyout and select **Run**. A notification confirms that generation has started.

Analysis can take from a few seconds to several minutes, depending on the number of alerts and the model. Open **Generations** in the **Attacks** view header to watch progress. 

When the run finishes, refresh the **Attacks** view to see new discoveries in the same table as scheduled discoveries (labeled as manually generated). If the run fails, [troubleshoot it with AI](/solutions/security/ai/attack-discovery/troubleshoot-runs-from-attacks-page.md). Select **Run** again anytime to start another analysis with the current alert selection. To run Attack Discovery automatically at intervals, [schedule a run](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md).

:::{note}
Attack Discovery uses the same data anonymization settings as [Elastic AI Assistant](/solutions/security/ai/ai-assistant.md). Configure which alert fields are sent to the LLM, and which are obfuscated, in the Elastic AI Assistant settings. Consider the privacy policies of third-party LLMs before sending them sensitive data.
:::

::::

::::{applies-item} stack: preview =9.4

Start manual runs from the [Attack Discovery page](/solutions/security/ai/attack-discovery/run-from-attack-discovery-page.md#attack-discovery-generate-discoveries). Use the **Attacks** page for triage, or [schedule a run](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md) for recurring analysis.

::::

:::::
