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
sub:
  search-load-sources: Detection rules (the number of enabled rules, how often they run, and lookback windows longer than the most recent day), other alerting rules, transforms, dashboards, Discover, ES|QL queries, and external clients that query the project
  search-saturation-signals: rule failures or timeouts in the Rule Monitoring tab
  search-reduce-load: disable rules you don't need, shorten lookbacks where your false positive tolerance allows, stagger rule schedules, and narrow time ranges on dashboards
---

# {{elastic-sec}} solution & project type overview [es-overview]

:::{include} ../get-started/_snippets/security-overview.md
:::

## Search performance [security-search-performance]
```{applies_to}
serverless: ga
```

:::{include} /solutions/_snippets/serverless-search-performance.md
:::

## Related reference

* [{{elastic-sec}} reference documentation](/reference/security/index.md) 
* [{{elastic-sec}} API documentation](/solutions/security/apis.md)
* [Fleet and Elastic Agent](https://www.elastic.co/docs/reference/fleet/)

Browse the latest [{{elastic-sec}} release notes](https://www.elastic.co/docs/release-notes/security) for more information on new features, enhancements, and fixes.
