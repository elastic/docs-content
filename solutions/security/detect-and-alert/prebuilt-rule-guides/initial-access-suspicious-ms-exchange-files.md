---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Microsoft Exchange Server UM Writing Suspicious Files" prebuilt detection rule.
---

# Microsoft Exchange Server UM Writing Suspicious Files

## Triage and analysis

Positive hits can be checked against the established Microsoft [baselines](https://github.com/microsoft/CSS-Exchange/tree/main/Security/Baselines).

Microsoft highly recommends that the best course of action is patching, but this may not protect already compromised systems
from existing intrusions. Other tools for detecting and mitigating can be found within their Exchange support
[repository](https://github.com/microsoft/CSS-Exchange/tree/main/Security)

