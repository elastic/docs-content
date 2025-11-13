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



::::{dropdown} Alerts aren't generated for rules with alert flapping off and an alert delay higher than 1

**Details**

On October 22, 2025, it was discovered that alerts aren't generated for rules that have **Alert flapping detection** turned off and the alert delay set to a value higher than 1.

**Workaround**

Set the alert delay value to 1 or turn on **Alert flapping detection**.

::::

## Resolved

:::{dropdown} Entity store transform is unavailable 

**Details**

A new feature introduced to the entity store caused the transform to scan for nonexistent indices.

**Workaround** 

Restart the entity store:
1. Find **Entity Store** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Entity Store** page, turn the toggle off.
3. Turn the toggle back on.

**Resolved** 

This was resolved on November 4, 2025.

::::

:::{dropdown} CSPM and Asset Management integrations don't ingest data when deployed using agent-based technology if {{kib}} is hosted on AWS
Applies to: {{serverless-short}} deployments hosted on AWS

**Details**

If your {{serverless-short}} deployment is hosted on AWS, new Cloud Security Posture Management (CSPM) and Asset Inventory integrations will fail to produce findings when deployed using agent-based deployment. {{serverless-short}} deployments hosted on GCP or Azure are not affected. Integrations that use agentless deployment are not affected. 

**Workaround** 

Two workarounds are available:

1. Turn off the **Enable Cloud Connector** advanced setting. 
    1. Go to the **Advanced Settings** menu using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
    2. In the **Security Solution** section, turn off the **Enable Cloud Connector** option.
    3. Your agent-based integration deployments will work as expected.
2. Use agentless deployment. 
    1. Instead of using agent-based deployment, use agentless deployment. Agentless deployment works as expected.


**Resolved** 

This was resolved on November 5, 2025.

::::


:::{dropdown} In {{sec-serverless}}, the entity risk score feature may stop persisting risk score documents

On May 30, 2025, it was discovered that the entity risk score feature may stop persisting risk score documents if risk scoring was previously turned on. This is due to a bug that prevents the `entity_analytics_create_eventIngest_from_timestamp-pipeline-<space_name>` ingest pipeline (which is set as a default pipeline for the risk scoring index in an earlier {{serverless-short}} release) from being created when {{kib}} starts up.

While document persistence may initially succeed, it will eventually fail after 0 to 30 days. This is how long it takes for the risk score data stream to roll over and apply its underlying index settings to the new default pipeline.

**Workaround**

To resolve this issue, manually create the ingest pipeline in each space that has entity risk scoring turned on. You can do this using a PUT request, which is described in the example below. When reviewing the example, note that `default` in the example ingest pipeline name below is the {{kib}} space ID.

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

After you complete this step, risk scores should automatically begin to successfully persist during the entity risk engine's next run. Details for the next run time are described on the **Entity risk score** page, where you can also manually run the risk score by clicking **Run Engine**.

**Resolved**

This was resolved on June 17, 2025.

:::

:::{dropdown} Installing the {{elastic-defend}} integration or a new agent policy in {{sec-serverless}} forces an upgrade of prebuilt rules

On April 10, 2025, it was discovered that when you install a new {{elastic-defend}} integration or agent policy, the installed prebuilt detection rules upgrade to their latest versions (if any new versions are available). The upgraded rules lose any user-added rule actions, exceptions, and customizations. 

**Workaround**

To resolve this issue, before you add an {{elastic-defend}} integration to a policy in {{fleet}}, apply any pending prebuilt rule updates. This will prevent rule actions, exceptions, and customizations from being overwritten.

**Resolved**

This was resolved on April 14, 2025.

:::