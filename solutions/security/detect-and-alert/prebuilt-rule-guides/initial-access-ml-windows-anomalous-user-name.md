---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Windows Username" prebuilt detection rule.
---

# Unusual Windows Username

## Triage and analysis

### Investigating Unusual Windows Username
Detection alerts from this rule indicate activity for a Windows user name that is rare and unusual. Here are some possible avenues of investigation:
- Consider the user as identified by the username field. Is this program part of an expected workflow for the user who ran this program on this host? Could this be related to occasional troubleshooting or support activity?
- Examine the history of user activity. If this user only manifested recently, it might be a service account for a new software package. If it has a consistent cadence (for example if it runs monthly or quarterly), it might be part of a monthly or quarterly business process.
- Examine the process arguments, title and working directory. These may provide indications as to the source of the program or the nature of the tasks that the user is performing.
- Consider the same for the parent process. If the parent process is a legitimate system utility or service, this could be related to software updates or system management. If the parent process is something user-facing like an Office application, this process could be more suspicious.
