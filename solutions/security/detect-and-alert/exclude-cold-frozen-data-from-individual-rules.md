---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/exclude-cold-frozen-data-individual-rules.html
---

# Exclude cold and frozen data from individual rules [exclude-cold-frozen-data-individual-rules]

Your rule might perform slower or fail if it queries data from cold or frozen [data tiers](../../../manage-data/lifecycle/data-tiers.md). To help Elasticsearch exclude cold and frozen data more efficiently, apply a Query DSL filter that ignores cold and frozen documents when your rule executes. You can add the filter when creating a new rule or updating an existing one.

::::{tip} 
To ensure that rules in your {{kib}} space exclude cold and frozen documents when executing, configure the `excludedDataTiersForRuleExecution` [advanced setting](../get-started/configure-advanced-settings.md#exclude-cold-frozen-data-rule-executions). This setting does not apply to {{ml}} rules.
::::


::::{important} 
* This method is not supported for {{esql}} and {{ml}} rules.
* Even when applying this filter, indicator match and event correlation rules may still fail if a frozen or cold shard that matches the rule’s specified index pattern is unavailable during rule executions. If failures occur, we recommend modifying the rule’s index patterns to only match indices containing hot tier data.

::::


Here is a sample Query DSL filter that excludes frozen tier documents during rule execution:

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

Here is another sample Query DSL filter that excludes cold and frozen tier documents during rule execution:

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

