---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Persistence via Login Hook" prebuilt detection rule.
---

# Potential Persistence via Login Hook

## Triage and analysis

Starting in Mac OS X 10.7 (Lion), users can specify certain applications to be re-opened when a user reboots their machine. This can be abused to establish or maintain persistence on a compromised system.
