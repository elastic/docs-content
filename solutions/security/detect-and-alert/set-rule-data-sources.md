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

**Target a narrower set of indices.** If a rule only applies to Windows endpoint data, restricting its index patterns to `winlogbeat-*` or `logs-endpoint.events.process-*` reduces the volume of data the rule scans and improves performance.

**Broaden to additional indices.** If a rule needs data from a source that isn't in the space-level defaults (for example, a custom integration or a third-party feed), add the relevant index pattern.

**Use a {{data-source}}.** Instead of specifying index patterns directly, you can select a {{data-source}} from the drop-down. The rule then uses the {{data-source}}'s index patterns and any [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) defined on it, which can be useful for enrichment or field normalization.

::::{tip}
For indicator match rules, the **Indicator index patterns** field controls which threat intelligence indices the rule queries separately from the main source index patterns. By default, this uses the [`securitySolution:defaultThreatIndex`](/solutions/security/get-started/configure-advanced-settings.md) setting (`logs-ti_*`).
::::

::::{note}
{{esql}} and {{ml}} rules do not use the index patterns field. {{esql}} rules define their data source within the query itself (using the `FROM` command). {{ml}} rules rely on the {{ml}} job's datafeed configuration.
::::

## Exclude cold and frozen data [exclude-cold-frozen-tier]

Rules may perform slower or time out if they query data stored in cold or frozen [data tiers](../../../manage-data/lifecycle/data-tiers.md). You have two options for excluding this data:

**Space-level setting (all rules).** Configure the `excludedDataTiersForRuleExecution` [advanced setting](../get-started/configure-advanced-settings.md#exclude-cold-frozen-data-rule-executions) to exclude cold or frozen data from all rules in a {{kib}} space. This does not apply to {{ml}} rules. Only available on {{stack}}.

**Per-rule Query DSL filter (individual rules).** Add a Query DSL filter to the rule that ignores cold or frozen documents at query time. This gives you per-rule control and is described below.

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

## Related pages

* [Advanced data source configuration](/solutions/security/detect-and-alert/advanced-data-source-configuration.md): Deployment-level settings that affect data sources, including {{ccs}} and logsdb index mode.
* [Update default {{elastic-sec}} indices](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices): Change the space-level default index patterns inherited by all rules.
* [Rule settings reference](/solutions/security/detect-and-alert/rule-settings-reference.md): Shared rule settings including timestamp override, which controls which timestamp field the rule uses when querying data.
