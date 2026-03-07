---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Creation or Modification of Domain Backup DPAPI private key" prebuilt detection rule.
---

# Creation or Modification of Domain Backup DPAPI private key

## Triage and analysis

Domain DPAPI Backup keys are stored on domain controllers and can be dumped remotely with tools such as Mimikatz. The resulting .pvk private key can be used to decrypt ANY domain user masterkeys, which then can be used to decrypt any secrets protected by those keys.

