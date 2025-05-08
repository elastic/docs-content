---
navigation_title: "Indicators of compromise"
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/indicators-of-compromise.html
  - https://www.elastic.co/guide/en/serverless/current/security-indicators-of-compromise.html
applies_to:
  stack: all
  serverless:
    security: all
---


# Troubleshoot indicators of compromise [troubleshoot-indicators-page]

If indicator data is not appearing in the Indicators table after you installed a threat intelligence integration:

* Verify that the index storing indicator documents is included in the [default {{elastic-sec}} indices](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices) (`securitySolution:defaultIndex`). The index storing indicator documents will differ based on the way you’re collecting indicator data:

    * **{{agent}} integrations** - `logs_ti*`
    * **{{filebeat}} integrations** - `filebeat-*`

* Ensure the indicator data you’re ingesting is mapped to [Elastic Common Schema (ECS)](ecs://reference/index.md).

::::{note}
These troubleshooting steps also apply to the [Threat Intelligence view](/solutions/security/get-started/enable-threat-intelligence-integrations.md).
::::


% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):
