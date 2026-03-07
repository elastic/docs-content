---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Rapid7 Threat Command CVEs Correlation" prebuilt detection rule.'
---

# Rapid7 Threat Command CVEs Correlation

## Triage and analysis

### Investigating Rapid7 Threat Command CVEs Correlation

Rapid7 Threat Command CVEs Correlation rule allows matching CVEs from user indices within the vulnerabilities collected from Rapid7 Threat Command integrations.

The matches will be based on the latest values of CVEs from the last 180 days. So it's essential to validate the data and review the results by investigating the associated activity to determine if it requires further investigation.

If a vulnerability matches a local observation, the following enriched fields will be generated to identify the vulnerability, field, and type matched.

- `threat.indicator.matched.atomic` - this identifies the atomic vulnerability that matched the local observation
- `threat.indicator.matched.field` - this identifies the vulnerability field that matched the local observation
- `threat.indicator.matched.type` - this identifies the vulnerability type that matched the local observation

Additional investigation can be done by reviewing the source of the activity and considering the history of the vulnerability that was matched. This can help understand if the activity is related to legitimate behavior.

- Investigation can be validated and reviewed based on the data that was matched and by viewing the source of that activity.
- Consider the history of the vulnerability that was matched. Has it happened before? Is it happening on multiple machines? These kinds of questions can help understand if the activity is related to legitimate behavior.
- Consider the user and their role within the company: is this something related to their job or work function?
