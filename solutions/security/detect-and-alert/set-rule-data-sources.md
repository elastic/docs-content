---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/exclude-cold-frozen-data-individual-rules.html
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Configure which Elasticsearch indices rules query and exclude cold or frozen data from rule execution.
---

# Set rule data sources [exclude-cold-frozen-data-individual-rules]

Every detection rule needs a data source that tells it which {{es}} indices to query. By default, rules inherit the index patterns defined in the [`securitySolution:defaultIndex`](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices) advanced setting. You can override this default on a per-rule basis to target specific indices, exclude data tiers, or use a {{data-source}} with runtime fields.

## Per-rule index patterns [per-rule-index-patterns]

When you create or edit a rule, the **Index patterns** field (or **Data view** selector) controls which {{es}} indices the rule queries. This field is prepopulated with the space-level defaults, but you can change it for any individual rule.

Common reasons to override the defaults:

* **Target a narrower set of indices**: If a rule only applies to Windows endpoint data, restricting its index patterns to `winlogbeat-*` or `logs-endpoint.events.process-*` reduces the volume of data the rule scans and improves performance.

* **Broaden to additional indices**: If a rule needs data from a source that isn't in the space-level defaults (for example, a custom integration or a third-party feed), add the relevant index pattern.

* **Use a {{data-source}}**: Instead of specifying index patterns directly, you can select a {{data-source}} from the drop-down. The rule then uses the {{data-source}}'s index patterns and any [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) defined on it, which can be useful for enrichment or field normalization.

::::{tip}
For indicator match rules, the **Indicator index patterns** field controls which threat intelligence indices the rule queries separately from the main source index patterns. By default, this uses the [`securitySolution:defaultThreatIndex`](/solutions/security/get-started/configure-advanced-settings.md) setting (`logs-ti_*`).
::::

::::{note}
{{esql}} and {{ml}} rules do not use the index patterns field. {{esql}} rules define their data source within the query itself (using the `FROM` command). {{ml-cap}} rules rely on the {{ml}} job's datafeed configuration.
::::

## Exclude cold and frozen data [exclude-cold-frozen-tier]

Cold data tiers store time series data that's accessed infrequently and rarely updated, while frozen data tiers hold time series data that's accessed even less frequently and never updated. Rules may perform slower or time out if they query data stored in these [data tiers](../../../manage-data/lifecycle/data-tiers.md).

### Best practices

* **Retention in hot tier**: Keep data in the hot tier ({{ilm}} hot phase) for at least 24 hours. {{ilm-cap}} policies that move ingested data from the hot phase to another phase (for example, cold or frozen) in less than 24 hours may cause performance issues or rule execution errors.
* **Replicas for mission-critical data**: Your data should have replicas if it must be highly available. Since frozen tiers don't have replicas by default, shard unavailability can cause partial rule run failures. Shard unavailability may also be encountered during or after {{stack}} upgrades. If this happens, you can manually rerun rules over the affected time period once the shards are available.

### Limitations

* To avoid rule failures, do not modify {{ilm}} policies for {{elastic-sec}}-controlled indices, such as alert and list indices.
* Source data must have an {{ilm}} policy that keeps it in the hot or warm tiers for at least 24 hours before moving to cold or frozen tiers.

### Exclusion options

You have two options for excluding cold and frozen data from rules:

* **Space-level setting (all rules)**: Configure the `excludedDataTiersForRuleExecution` [advanced setting](../get-started/configure-advanced-settings.md#exclude-cold-frozen-data-rule-executions) to exclude cold or frozen data from all rules in a {{kib}} space. This does not apply to {{ml}} rules. Only available on {{stack}}.

* **Per-rule Query DSL filter (individual rules)**: Add a Query DSL filter to the rule that ignores cold or frozen documents at query time. This gives you per-rule control and is described below.

::::{important}
* Per-rule Query DSL filters are not supported for {{esql}} and {{ml}} rules.
* Even with this filter applied, indicator match and event correlation rules may still fail if a frozen or cold shard that matches the rule's index pattern is unavailable during rule execution. If failures occur, modify the rule's index patterns to only match indices containing hot-tier data.
::::

### Sample Query DSL filters [query-dsl-filter-examples]

Exclude frozen-tier documents:

```console
{
   "bool":{
      "must_not":{
         "terms":{
            "_tier":[
               "data_frozen"
            ]
         }
      }
   }
}
```

Exclude cold and frozen-tier documents:

```console
{
   "bool":{
      "must_not":{
         "terms":{
            "_tier":[
               "data_frozen", "data_cold"
            ]
         }
      }
   }
}
```

To apply a filter, paste the Query DSL into the **Custom query** filter bar when creating or editing a rule.

## More data source configuration options

This page covers per-rule data source settings. For broader configuration options:

* **Change the defaults all rules inherit**: Modify the space-level [`securitySolution:defaultIndex`](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices) setting to update the index patterns that new rules use by default.
* **Configure deployment-level data source settings**: Refer to [Advanced data source configuration](/solutions/security/detect-and-alert/advanced-data-source-configuration.md) for {{ccs}} setup and logsdb index mode compatibility.
