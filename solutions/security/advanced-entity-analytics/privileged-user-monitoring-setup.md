---
navigation_title: Set up privileged user monitoring
applies_to:
  stack: preview 9.1
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Set up and manage privileged user monitoring

:::{admonition} Requirements
To use privileged user monitoring, you must:

* Have the appropriate user role or privileges
* Turn on the required advanced setting

For more information, refer to [Privileged user monitoring requirements](/solutions/security/advanced-entity-analytics/privileged-user-monitoring-requirements.md).
:::

Before you can start monitoring privileged users, you need to define which users in your environment are considered privileged.

Privileged users typically include accounts with elevated access rights that allow them to configure security settings, manage user permissions, or access sensitive data. 

## Define privileged users

You can define privileged users in the following ways:

* [Select an existing index](#privmon-index) or create a new custom index with privileged user data.
* [Bulk-upload](#privmon-upload) a list of privileged users using a CSV or TXT file. 
* Use the Entity analytics APIs to [mark individual users as privileged]({{kib-apis}}/operation/operation-createprivmonuser) or [bulk-upload multiple privileged users]({{kib-apis}}/operation/operation-privmonbulkuploaduserscsv).

To get started, find the **Privileged user monitoring** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

### Select or create an index [privmon-index]

1. On the **Privileged user monitoring** page, click **Index**.
2. From the **Select index** popup, you can create new or choose existing indices as your data source.
3. Select **Add privileged users**.

All user names, specified in the `user.name` field in your selected indices, will be defined as privileged users.

### Import a list of privileged users from a text file [privmon-upload]

1. On the **Privileged user monitoring** page, click **File**.
2. Select or drag and drop the file you want to import. The maximum file size is 1 MB.
3. Select **Add privileged user**.

:::{note}
* Any lines that don’t follow the required file structure will be highlighted, and those users won't be added. We recommend that you fix any invalid lines and re-upload the file.

* You can only import one file as a data source. Any users previously imported through a text file are overwritten.
:::

After setting up your privileged users, you can start [monitoring their activity](/solutions/security/advanced-entity-analytics/monitor-privileged-user-activitites.md) and related insights on the **Privileged user monitoring** dashboard.

You can update the selected data sources at any time by selecting **Manage data sources**.

## Manage data sources

