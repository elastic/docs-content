---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Windows Network Activity" prebuilt detection rule.'
---

# Unusual Windows Network Activity

## Triage and analysis

### Investigating Unusual Windows Network Activity
Detection alerts from this rule indicate the presence of network activity from a Windows process for which network activity is very unusual.  Here are some possible avenues of investigation:
- Consider the IP addresses, protocol and ports. Are these used by normal but infrequent network workflows? Are they expected or unexpected?
- If the destination IP address is remote or external, does it associate with an expected domain, organization or geography? Note: avoid interacting directly with suspected malicious IP addresses.
- Consider the user as identified by the username field. Is this network activity part of an expected workflow for the user who ran the program?
- Examine the history of execution. If this process only manifested recently, it might be part of a new software package. If it has a consistent cadence (for example if it runs monthly or quarterly), it might be part of a monthly or quarterly business process.
- Examine the process arguments, title and working directory. These may provide indications as to the source of the program or the nature of the tasks it is performing.
- Consider the same for the parent process. If the parent process is a legitimate system utility or service, this could be related to software updates or system management. If the parent process is something user-facing like an Office application, this process could be more suspicious.
- If you have file hash values in the event data, and you suspect malware, you can optionally run a search for the file hash to see if the file is identified as malware by anti-malware tools.
