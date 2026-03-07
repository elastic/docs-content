---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Linux Username" prebuilt detection rule.'
---

# Unusual Linux Username

## Triage and analysis

### Investigating Unusual Linux Username
Detection alerts from this rule indicate activity for a Linux user name that is rare and unusual. Here are some possible avenues of investigation:
- Consider the user as identified by the username field. Is this program part of an expected workflow for the user who ran this program on this host? Could this be related to troubleshooting or debugging activity by a developer or site reliability engineer?
- Examine the history of user activity. If this user only manifested recently, it might be a service account for a new software package. If it has a consistent cadence (for example if it runs monthly or quarterly), it might be part of a monthly or quarterly business process.
- Examine the process arguments, title and working directory. These may provide indications as to the source of the program or the nature of the tasks that the user is performing.
