---
navigation_title: Elasticsearch user settings
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-add-user-settings.html
---

# Add Elasticsearch user settings [ece-add-user-settings]

Change how Elasticsearch runs by providing your own user settings. User settings are appended to the `elasticsearch.yml` configuration file for your cluster and provide custom configuration options. Elastic Cloud Enterprise supports many of the user settings for the version of Elasticsearch that your cluster is running.

::::{note}
ECE blocks the configuration of certain settings that could break your cluster if misconfigured, including some zen discovery and security settings. For a list of settings that are generally safe in cloud environments, refer to the [Elasticsearch configuration reference](elasticsearch://reference/elasticsearch/configuration-reference/index.md).
::::

To change {{es}} user settings:

1. [Log into the Cloud UI](./log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. In the **Elasticsearch** section, select **Manage user settings and extensions**. For deployments with existing user settings, you may have to expand the **User setting overrides** caret for each node type instead.
5. Update the user settings.
6. Select **Save changes**.

    ::::{warning}
    If you encounter the **Edit elasticsearch.yml** carets, be sure to make your changes on all Elasticsearch node types.
    ::::

## Example: enable email notifications from Gmail [ece_enable_email_notifications_from_gmail]

You can configure email notifications to Gmail for a user that you specify. For details, refer to [Configuring email actions](../../../explore-analyze/alerts-cases/watcher/actions-email.md).

::::{important}
Before you add the `xpack.notification.email*` setting in Elasticsearch user settings, make sure you add the account SMTP password to the keystore as a [secret value](../../../deploy-manage/security/secure-settings.md).
::::
