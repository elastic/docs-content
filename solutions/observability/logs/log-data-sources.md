---
applies_to:
  stack: all
  serverless: all
products:
  - id: observability
---

# Configure log data sources

The `observability:logSources` {{kib}} advanced setting defines which index patterns your deployment or project uses to store and query log data.

Configure this setting at **Stack Management** → **Advanced Settings** or by searching for `Advanced Settings` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).


::::{note}
Adding indices to the `observability:logSources` setting that don't contain log data may cause degraded functionality. Changes to this setting can also impact the sources queried by log threshold rules.
::::

## Configure log data sources using the `saved_objects` API

To configure log data sources using an API, use the `saved_objects` API. To do this,

1. From **Stack Management** → **Saved Objects**, [export](/explore-analyze/find-and-organize/saved-objects.md#export-saved-objects-export) the log data views, which are stored as an `infrastructure-monitoring-log-view` saved object type, to use as a template.
1. Modify the relevant data view fields in the exported JSON.
1. Import the saved object using the [import saved objects API](https://www.elastic.co/docs/api/doc/kibana/v8/operation/operation-importsavedobjectsdefault).