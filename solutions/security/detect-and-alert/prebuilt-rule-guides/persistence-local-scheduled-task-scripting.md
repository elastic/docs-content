---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Scheduled Task Created by a Windows Script" prebuilt detection rule.
---

# Scheduled Task Created by a Windows Script

## Triage and analysis

Decode the base64 encoded Tasks Actions registry value to investigate the task's configured action.
