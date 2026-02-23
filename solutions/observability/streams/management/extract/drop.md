---
applies_to:
  serverless: ga
  stack: ga 9.3+
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Drop document processor [streams-drop-processor]

The **Drop document** processor prevents documents from being indexed when they meet a specific condition, without raising an error.

To configure a condition for dropping documents:

1. Select **Create** → **Create processor**.
1. Select **Drop document** from the **Processor** menu.
1. Set the **Condition** for when you want to drop a document.

  :::{warning}
  The default is the `always` condition. Not setting a specific condition results in every document that matches the drop condition getting dropped from indexing.
  :::

This functionality uses the {{es}} [Drop processor](elasticsearch://reference/enrich-processor/drop-processor.md) internally, but you configure it in Streamlang. Streamlang doesn’t always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).