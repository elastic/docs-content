---
applies_to:
  serverless: ga
  stack: ga 9.3+
---

# Math processor [streams-math-processor]

The math processor evaluates arithmetic or logical expressions and stores the result in the target field.

To calculate a value using an expression and store the result in a target field:

1. Select **Create** → **Create processor**.
1. Select **Math** from the **Processor** menu.
1. Set the **Target field** where you want to write the expression result.
1. Set your expression in the **Expression** field. You can directly reference fields in your expression (for example, `bytes / duration`).
