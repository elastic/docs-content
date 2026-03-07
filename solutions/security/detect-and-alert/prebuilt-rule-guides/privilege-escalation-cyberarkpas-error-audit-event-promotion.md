---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "CyberArk Privileged Access Security Error" prebuilt detection rule.'
---

# CyberArk Privileged Access Security Error

## Setup

The CyberArk Privileged Access Security (PAS) Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.

## Triage and analysis

This is a promotion rule for CyberArk error events, which are alertable events per the vendor.
Consult vendor documentation on interpreting specific events.
