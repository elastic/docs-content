---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---

# Configure log data sources

The `observability:logSources` {{kib}} advanced setting defines which index patterns your deployment or project uses to store and query log data.

Configure this setting from the **Advanced Settings** page, which you can open from the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).


::::{note}
Adding indices to the `observability:logSources` setting that don't contain log data may cause degraded functionality. Changes to this setting can also impact the sources queried by log threshold rules.
::::

## Configure log data sources using the `saved_objects` API

::::{important}
Using the `saved_objects` API to import log data sources has the following limitations:

* To import the log data source, you need to import the entire **Advanced Settings** saved object. This overwrites any other changes that you've made to your **Advanced Settings** in the target cluster, not just `observability:logSources`.
* This approach is backward compatible, but not forward compatible. You cannot import the settings from an older version to a newer version.
::::

To configure log data sources using the `saved_objects` API and the **Advanced Settings** saved object:

1. Go to **Advanced Settings** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Configure your custom log sources in `observability:logSources`.
1. Go to the **Saved Objects** management page from the navigation or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).
1. [Export](/explore-analyze/find-and-organize/saved-objects.md#saved-objects-import-and-export) the **Advanced Settings** saved object.
1. Import the saved object to your target cluster using the [import saved objects API]({{kib-apis}}/operation/operation-importsavedobjectsdefault).
