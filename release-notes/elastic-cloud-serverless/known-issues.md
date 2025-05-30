---
navigation_title: Known issues
---
# {{serverless-full}} known issues [elastic-cloud-serverless-known-issues]
Known issues are significant defects or limitations that may impact your implementation. These issues are actively being worked on and will be addressed in a future release. Review the {{serverless-full}} known issues to help you make informed decisions, such as upgrading to a new version.

% Use the following template to add entries to this page.

% :::{dropdown} Title of known issue
% **Applicable versions for the known issue and the version for when the known issue was fixed**
% On [Month Day, Year], a known issue was discovered that [description of known issue].
% For more information, check [Issue #](Issue link).

% **Workaround** 
% Workaround description.

## Active

:::{dropdown} In {{sec-serverless}}, the entity risk score feature may stop persisting risk score documents

On May 30, 2025, it was discovered that the entity risk score feature eventually stop persisting risk score documents if risk scoring was previously turned on. This is due to a bug that prevents the default ingest pipeline for the risk scoring index (`entity_analytics_create_eventIngest_from_timestamp-pipeline-<space_name>`) to be created when {{kib}} starts up. While document persistence may initially appear to succeed, it eventually fails after 0 to 30 days, which is how long it takes for the risk score data stream to roll over and its underlying index’s settings to take on the new default pipeline.

**Workaround**

To resolve this issue, manually create the ingest pipeline in each space in which you have turned on entity risk scoring. This can be done using a PUT request, which is described in the example below. When reviewing the example, note that `default` in the example ingest pipeline name below is the space ID. 

```
PUT /_ingest/pipeline/entity_analytics_create_eventIngest_from_timestamp-pipeline-default
{
  "_meta": {
    "managed_by": "entity_analytics",
    "managed": true
  },
  "description": "Pipeline for adding timestamp value to event.ingested",
  "processors": [
    {
      "set": {
        "field": "event.ingested",
        "value": "{{_ingest.timestamp}}"
      }
    }
  ]
}
```

After the above step is complete, risk scores should automatically begin to successfully persist during the entity risk engine's next run cycle. Details for the next run time are described on the  Entity risk score page. From the page, you can manually run the risk score again by clicking **Run Engine**. 

:::

## Resolved

:::{dropdown} In {{sec-serverless}}, installing an {{elastic-defend}} integration or a new agent policy upgrades installed prebuilt rules, reverting user customizations and overwriting user-added actions and exceptions

On April 10, 2025, it was discovered that when you install a new {{elastic-defend}} integration or agent policy, the installed prebuilt detection rules upgrade to their latest versions (if any new versions are available). The upgraded rules lose any user-added rule actions, exceptions, and customizations. 

**Workaround**

To resolve this issue, before you add an {{elastic-defend}} integration to a policy in {{fleet}}, apply any pending prebuilt rule updates. This will prevent rule actions, exceptions, and customizations from being overwritten.

**Resolved**

This was resolved on April 14, 2025.

:::