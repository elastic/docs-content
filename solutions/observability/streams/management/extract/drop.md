---
applies_to:
  serverless: ga
  stack: ga 9.3+
---

# Drop document processor [streams-drop-processor]

The drop document processor prevents documents from being indexed when they meet a specific condition, without raising an error.

To configure a condition for dropping documents:

1. Select **Create** → **Create processor**.
1. Select **Drop document** from the **Processor** menu.
1. Set the **Condition** for when you want to drop a document.

This functionality uses the {{es}} drop pipeline processor. Refer to the [drop processor](elasticsearch://reference/enrich-processor/drop-processor.md) {{es}} documentation for more information.