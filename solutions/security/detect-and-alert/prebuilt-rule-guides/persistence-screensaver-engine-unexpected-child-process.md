---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unexpected Child Process of macOS Screensaver Engine" prebuilt detection rule.
---

# Unexpected Child Process of macOS Screensaver Engine

## Triage and analysis

- Analyze the descendant processes of the ScreenSaverEngine process for malicious code and suspicious behavior such
as a download of a payload from a server.
- Review the installed and activated screensaver on the host. Triage the screensaver (.saver) file that was triggered to
identify whether the file is malicious or not.

