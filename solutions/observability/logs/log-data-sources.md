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

::::{important}
Using the `saved_objects` API to import log data sources has the following limitations:

* To import the log data source, you need to import the entire **Advanced Settings** saved object, meaning you will be importing all advanced settings not just the `logSources` setting.
* This approach is backwards compatible, but not forwards compatible. You can't import the settings from an older version to a newer version.
::::

To configure log data sources using the `saved_objects` API and the **Advanced Settings** saved object:

1. Go to **Saved Objects** from the navigation menu under **Management** or use the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md).
1. [Export](/explore-analyze/find-and-organize/saved-objects.md#saved-objects-import-and-export) the **Advanced Settings** saved object, to use as a template.
1. Modify the `observability:logSources` setting and any other settings you want to update in the exported JSON.
1. Import the saved object using the [import saved objects API]({{kib-apis}}/operation/operation-importsavedobjectsdefault).
