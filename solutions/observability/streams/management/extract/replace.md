---
applies_to:
  serverless: ga
  stack: ga 9.3+
---

# Replace processor [streams-replace-processor]

The replace processor replaces parts of a string field that match a regular expression pattern with a replacement string.

To use the replace processor:

1. Select **Create** → **Create processor**.
1. Select **Replace** from the **Processor** menu.
1. Set the **Source Field** to the field that contains the string you want to replace.
1. Set the **Pattern** to the regular expression or text that you want to replace.
1. Set the **Replacement** to the value that will replace the portion of the string matching your pattern. Replacements can be text, an empty value, or a capture group reference.

This functionality uses the {{es}} gsub processor. Refer to the [gsub processor](elasticsearch://reference/enrich-processor/gsub-processor.md) {{es}} documentation for more information.