---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Screensaver Plist File Modified by Unexpected Process" prebuilt detection rule.'
---

# Screensaver Plist File Modified by Unexpected Process

## Triage and analysis

- Analyze the plist file modification event to identify whether the change was expected or not
- Investigate the process that modified the plist file for malicious code or other suspicious behavior
- Identify if any suspicious or known malicious screensaver (.saver) files were recently written to or modified on the host
