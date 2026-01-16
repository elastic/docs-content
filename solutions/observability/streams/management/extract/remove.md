---
applies_to:
  serverless: ga
  stack: ga 9.3+
---

# Remove processor [streams-remove-processor]

The remove processor removes a field (**Remove**) or removes a field and all its nested fields (**Remove by prefix**) from your documents.

To remove a field:

1. Select **Create** → **Create processor**.
1. From the **Processor** menu, select **Remove** to remove a field or **Remove by prefix** to remove a field and all its nested fields.
1. Set the **Source Field** to the field you want to remove.

This functionality uses the {{es}} [remove processor](elasticsearch://reference/enrich-processor/remove-processor.md) internally, but you configure it in Streamlang. Streamlang doesn’t always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).