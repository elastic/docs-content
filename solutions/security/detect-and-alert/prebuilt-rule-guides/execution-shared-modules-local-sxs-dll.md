---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Execution via local SxS Shared Module" prebuilt detection rule.
---

# Execution via local SxS Shared Module

## Triage and analysis

The SxS DotLocal folder is a legitimate feature that can be abused to hijack standard modules loading order by forcing an executable on the same application.exe.local folder to load a malicious DLL module from the same directory.

