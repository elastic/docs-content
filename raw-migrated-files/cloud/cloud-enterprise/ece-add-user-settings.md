# Add Elasticsearch user settings [ece-add-user-settings]

Change how Elasticsearch runs by providing your own user settings. User settings are appended to the `elasticsearch.yml` configuration file for your cluster and provide custom configuration options. Elastic Cloud Enterprise supports many of the user settings for the version of Elasticsearch that your cluster is running.

::::{tip}
Some settings that could break your cluster if set incorrectly are blocked, such as certain zen discovery and security settings. For examples of a few of the settings that are generally safe in cloud environments, check [Additional Examples of Supported User Settings](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-change-user-settings-examples.html) and  [Editing Your User Settings](https://www.elastic.co/guide/en/cloud/current/ec-editing-user-settings.html) that can be enabled on our Elastic Cloud hosted offering.
::::


To add user settings:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. In the **Elasticsearch** section, select **Edit elasticsearch.yml**. For deployments with existing user settings, you may have to expand the **User setting overrides** caret for each node type instead.
5. Update the user settings.
6. Select **Save changes**.

    ::::{warning}
    If you encounter the **Edit elasticsearch.yml** carets, be sure to make your changes on all Elasticsearch node types.
    ::::



## Enable email notifications from Gmail [ece_enable_email_notifications_from_gmail]

You can configure email notifications to Gmail for a user that you specify. For details, refer to [Configuring email actions](../../../explore-analyze/alerts/watcher/actions-email.md).

::::{warning}
Before you add the `xpack.notification.email*` setting in Elasticsearch user settings, make sure you add the account SMTP password to the keystore as a [secret value](../../../deploy-manage/security/secure-settings.md).
::::
