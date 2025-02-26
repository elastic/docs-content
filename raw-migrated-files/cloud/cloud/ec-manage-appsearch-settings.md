# Add App Search user settings [ec-manage-appsearch-settings]

Change how App Search runs by providing your own user settings. User settings are appended to the `app-search.yml` configuration file for your instance and provide custom configuration options.

::::{tip} 
Some settings that could break your cluster if set incorrectly are blocked. Review the [list of settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md#ec-appsearch-settings) that are generally safe in cloud environments. For detailed information about App Search settings, check the [App Search documentation](https://swiftype.com/documentation/app-search/self-managed/configuration).
::::


To add user settings:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, go to the **Edit** page.
4. At the bottom of the **App Search** section, expand the **User settings overrides** caret.
5. Update the user settings.
6. Select **Save changes**.

::::{note} 
If a setting is not supported by {{ech}}, you get an error message when you try to save.
::::



## Supported App Search settings [ec-appsearch-settings] 

{{ech}} supports the following App Search settings.

`app_search.auth.source`
:   The origin of authenticated App Search users. Options are `standard`, `elasticsearch-native`, and `elasticsearch-saml`.

`app_search.auth.name`
:   (SAML only) Name of the realm within the Elasticsearch realm chain.

