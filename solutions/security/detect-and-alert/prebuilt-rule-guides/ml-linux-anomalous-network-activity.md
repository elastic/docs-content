---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Linux Network Activity" prebuilt detection rule.
---

# Unusual Linux Network Activity

## Triage and analysis

### Investigating Unusual Linux Network Activity
Detection alerts from this rule indicate the presence of network activity from a Linux process for which network activity is rare and unusual.  Here are some possible avenues of investigation:
- Consider the IP addresses and ports. Are these used by normal but infrequent network workflows? Are they expected or unexpected?
- If the destination IP address is remote or external, does it associate with an expected domain, organization or geography? Note: avoid interacting directly with suspected malicious IP addresses.
- Consider the user as identified by the username field. Is this network activity part of an expected workflow for the user who ran the program?
- Examine the history of execution. If this process only manifested recently, it might be part of a new software package. If it has a consistent cadence (for example if it runs monthly or quarterly), it might be part of a monthly or quarterly business or maintenance process.
- Examine the process arguments, title and working directory. These may provide indications as to the source of the program or the nature of the tasks it is performing.
