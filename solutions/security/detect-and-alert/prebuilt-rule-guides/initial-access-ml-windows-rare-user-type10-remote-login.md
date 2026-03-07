---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Windows Remote User" prebuilt detection rule.'
---

# Unusual Windows Remote User

## Triage and analysis

### Investigating Unusual Windows Remote User
Detection alerts from this rule indicate activity for a rare and unusual Windows RDP (remote desktop) user. Here are some possible avenues of investigation:
- Consider the user as identified by the username field. Is the user part of a group who normally logs into Windows hosts using RDP (remote desktop protocol)? Is this logon activity part of an expected workflow for the user?
- Consider the source of the login. If the source is remote, could this be related to occasional troubleshooting or support activity by a vendor or an employee working remotely?
