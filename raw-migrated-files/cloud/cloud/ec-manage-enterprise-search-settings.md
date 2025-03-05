# Add Enterprise Search user settings [ec-manage-enterprise-search-settings]

:::{important}
Enterprise Search is not available in {{stack}} 9.0+.
:::

Change how Enterprise Search runs by providing your own user settings. User settings are appended to the `ent-search.yml` configuration file for your instance and provide custom configuration options.

Refer to the [Configuration settings reference](https://www.elastic.co/guide/en/enterprise-search/current/configuration.html#configuration-file) in the Enterprise Search documentation for a full list of configuration settings. Settings supported on {{ech}} are indicated by an {{ecloud}} icon (![logo cloud](https://doc-icons.s3.us-east-2.amazonaws.com/logo_cloud.svg "Supported on {{ecloud}}")). Be sure to refer to the documentation version that matches the Elastic Stack version used in your deployment.

To add user settings:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, go to the **Edit** page.
4. In the **Enterprise Search** section, select **Edit user settings**. For deployments with existing user settings, you may have to expand the **Edit enterprise-search.yml** caret instead.
5. Update the user settings.
6. Select **Save changes**.

::::{note}
If a setting is not supported by {{ech}}, an error message displays when you try to save your settings.
::::


