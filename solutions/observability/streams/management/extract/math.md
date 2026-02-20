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

# Math processor [streams-math-processor]

The **Math** processor evaluates arithmetic or logical expressions and stores the result in the target field.

To calculate a value using an expression and store the result in a target field:

1. Select **Create** → **Create processor**.
1. Select **Math** from the **Processor** menu.
1. Set the **Target field** where you want to write the expression result.
1. Set your expression in the **Expression** field. You can directly reference fields in your expression (for example, `bytes / duration`).
