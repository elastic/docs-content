# Add Enterprise Search user settings [ece-manage-enterprise-search-settings]

:::{important}
Enterprise Search is not available in {{stack}} 9.0+.
:::

Change how Enterprise Search runs by providing your own user settings. User settings are appended to the `ent-search.yml` configuration file for your instance and provide custom configuration options.

Refer to the [Configuration settings reference](https://www.elastic.co/guide/en/enterprise-search/current/configuration.html#configuration-file) in the Enterprise Search documentation for a full list of configuration settings. Settings supported on Elastic Cloud Enterprise are indicated by an {{ecloud}} icon (![logo cloud](https://doc-icons.s3.us-east-2.amazonaws.com/logo_cloud.svg "Supported on {{ecloud}}")). Be sure to refer to the documentation version that matches the Elastic Stack version used in your deployment.

To add user settings:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. In the **Enterprise Search** section, select **Edit user settings**. For deployments with existing user settings, you may have to expand the **Edit enterprise-search.yml** caret instead.
5. Update the user settings.
6. Select **Save changes**.

::::{note}
If a setting is not supported by Elastic Cloud Enterprise, an error message displays when you try to save your settings.
::::


