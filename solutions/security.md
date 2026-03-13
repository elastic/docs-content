---
navigation_title: Security solution
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/index.html
  - https://www.elastic.co/guide/en/security/current/es-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-overview.html
  - https://www.elastic.co/guide/en/kibana/current/xpack-siem.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
  - id: kibana
description: Elastic Security combines threat detection analytics, cloud native security, and endpoint protection capabilities in a single solution.
---

# {{elastic-sec}} solution & project type overview [es-overview]

:::{include} ../get-started/_snippets/security-overview.md
:::

## Agent skills

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/security/alert-triage
A skill is available to help AI agents triage Elastic Security alerts.
:::

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/security/case-management
A skill is available to help AI agents create and manage Elastic Security cases.
:::

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/security/detection-rule-management
A skill is available to help AI agents create, tune, and manage detection rules.
:::

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/security/generate-security-sample-data
A skill is available to help AI agents generate sample security data for demos and testing.
:::

## Related reference

* [{{elastic-sec}} reference documentation](/reference/security/index.md) 
* [{{elastic-sec}} API documentation](/solutions/security/apis.md)
* [Fleet and Elastic Agent](https://www.elastic.co/docs/reference/fleet/)

Browse the latest [{{elastic-sec}} release notes](https://www.elastic.co/docs/release-notes/security) for more information on new features, enhancements, and fixes.