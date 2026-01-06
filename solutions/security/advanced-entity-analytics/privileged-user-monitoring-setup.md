---
navigation_title: Set up privileged user monitoring
applies_to:
  stack: ga 9.3, preview 9.1
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Set up and manage privileged user monitoring

:::{admonition} Requirements
To use privileged user monitoring, you must:

* Have the appropriate user role or privileges
* {applies_to}`serverless: removed` {applies_to}`stack: removed 9.3` Turn on the required advanced setting

For more information, refer to [Privileged user monitoring requirements](/solutions/security/advanced-entity-analytics/privileged-user-monitoring-requirements.md).
:::

Before you can start monitoring privileged users, you need to define which users in your environment are considered privileged.

Privileged users typically include accounts with elevated access rights that allow them to configure security settings, manage user permissions, or access sensitive data. 

## Define privileged users

You can define privileged users in the following ways:

* {applies_to}`stack: ga 9.3` {applies_to}`stack: preview 9.2` {applies_to}`serverless: ga` [Add a supported integration](#privmon-integrations) with your organization’s user identities. If your environment is already ingesting data from a supported integration, the setup steps are skipped—you're taken directly to the Privileged user monitoring dashboard, where you can start [monitoring user activity](/solutions/security/advanced-entity-analytics/monitor-privileged-user-activitites.md).
* [Select an existing index](#privmon-index) or create a new custom index with privileged user data.
* [Bulk-upload](#privmon-upload) a list of privileged users using a CSV or TXT file. 
* Use the Entity analytics APIs to [mark individual users as privileged]({{kib-apis}}/operation/operation-createprivmonuser) or [bulk-upload multiple privileged users]({{kib-apis}}/operation/operation-privmonbulkuploaduserscsv).

To get started, find the **Privileged user monitoring** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

### Add a supported integration [privmon-integrations]
```yaml {applies_to}
stack: ga 9.3, preview 9.2
serverless: ga
```

1. On the **Privileged user monitoring** page, select an integration. The supported integrations are:
   * [Active Directory Entity Analytics](integration-docs://reference/entityanalytics_ad.md). Users in the following security groups will be automatically assigned as privileged:
      * Domain Admins
      * Enterprise Admins
   * [Okta Entity Analytics](integration-docs://reference/entityanalytics_okta.md). Refer to [Standard administrator roles and permissions](https://help.okta.com/en-us/content/topics/security/administrators-admin-comparison.htm) for a list of Okta roles that will be automatically assigned as privileged users.
2. Follow the steps to install the integration. 

### Select or create an index [privmon-index]

1. On the **Privileged user monitoring** page, click **Index**.
2. From the **Select index** popup, you can create new or choose existing indices as your data source.
3. Select **Add privileged users**.

All user names, specified in the `user.name` field in your selected indices, will be defined as privileged users.

### Import a list of privileged users from a text file [privmon-upload]

1. On the **Privileged user monitoring** page, click **File**.
2. Select or drag and drop the file you want to import. The maximum file size is 1 MB.
3. Select **Add privileged user**.

The file must contain at least one column, with each user record listed on a separate row:

1. The first column specifies the privileged user's user name.
2. An optional second column may specify a label, representing the user’s role, group, team, or similar.

File structure example:

```txt
superadmin
admin01,Domain Admin
sec_ops
jdoe,IT Support
```

:::{note}
Any lines that don’t follow the required file structure will be highlighted, and those users won't be added. We recommend that you fix any invalid lines and re-upload the file.
:::

After setting up your privileged users, you can start [monitoring their activity](/solutions/security/advanced-entity-analytics/monitor-privileged-user-activitites.md) and related insights on the Privileged user monitoring dashboard.

You can update the selected data sources at any time by selecting **Manage data sources**.

## Manage data sources

Use the **Manage data sources** page to update your selected data sources.

You can use multiple data source types, such as an index and a CSV file, at the same time to define privileged users. Users defined through different data source types are monitored together.

On this page, you can:

* {applies_to}`stack: ga 9.3` {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview` Change which integrations you're using as data sources.
* View, remove, and change indices after initially defining them.
* Import a new supported file with a list of privileged users.

   :::{note}
   Importing a new file will overwrite any users added from a previous file. This doesn't affect users defined through other data source types.
   :::