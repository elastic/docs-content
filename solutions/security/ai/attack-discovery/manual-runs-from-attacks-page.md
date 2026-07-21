---
navigation_title: Manual runs
description: "Manually run Attack Discovery from the Attacks view, or from the Attack Discovery page in 9.4."
applies_to:
  stack: preview =9.4, ga 9.5+
  serverless: ga
products:
  - id: security
  - id: cloud-serverless
---

# Manually run Attack Discovery from the Attacks view [manual-runs-from-attacks-page]

Manually run Attack Discovery when you want to start analysis yourself, instead of waiting for a schedule.

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.5+", "serverless": "ga" }

To manually run Attack Discovery from the **Attacks** view:

1. Go to **Detections > Views > Attacks**.
2. [Configure alert retrieval, generation, and validation](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md) in **Settings**, and confirm an LLM connector is selected.
3. Select **Run**. A notification confirms that generation has started.

Analysis can take from a few seconds to several minutes, depending on the number of alerts and the model. When the run finishes, the discoveries you started appear in the same **Attacks** table as scheduled discoveries (labeled as manually generated). Select **Run** again anytime to start another analysis with the current alert selection.

:::{note}
Attack Discovery uses the same data anonymization settings as [Elastic AI Assistant](/solutions/security/ai/ai-assistant.md). Configure which alert fields are sent to the LLM, and which are obfuscated, in the Elastic AI Assistant settings. Consider the privacy policies of third-party LLMs before sending them sensitive data.
:::

::::

::::{applies-item} stack: preview =9.4

In 9.4, start manual runs from the [Attack Discovery page](/solutions/security/ai/attack-discovery/run-from-attack-discovery-page.md#attack-discovery-generate-discoveries). Use the **Attacks** page for triage and [schedules](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md).

::::

:::::
