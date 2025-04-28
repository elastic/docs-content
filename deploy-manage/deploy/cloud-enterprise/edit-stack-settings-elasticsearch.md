---
navigation_title: Elasticsearch user settings
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-add-user-settings.html
---

# Add {{es}} user settings [ece-add-user-settings]

Change how {{es}} runs by providing your own user settings. User settings are appended to the `elasticsearch.yml` configuration file for your cluster and provide custom configuration options.

:::{important}
If a feature requires both standard `elasticsearch.yml` settings and [secure settings](/deploy-manage/security/secure-settings.md), configure the secure settings first. Updating standard user settings can trigger a cluster rolling restart, and if the required secure settings are not yet in place, the nodes might fail to start. Adding secure settings does not trigger a restart.
:::

{{ece}} automatically rejects `elasticsearch.yml` settings that could break your cluster, including some zen discovery and security settings.

For a list of supported settings, check [Supported {{es}} settings](elasticsearch://reference/elasticsearch/configuration-reference/index.md).

To add or edit {{es}} user settings:

1. [Log into the Cloud UI](./log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. In the **Elasticsearch** section, select **Manage user settings and extensions**. For deployments with existing user settings, you may have to expand the **User setting overrides** caret for each node type instead.
5. Update the user settings.
6. Select **Save changes**.

    ::::{warning}
    If you encounter the **Edit elasticsearch.yml** carets, be sure to make your changes on all {{es}} node types.
    ::::

## Example: enable email notifications [ece_enable_email_notifications_from_gmail]

To enable email notifications in your {{es}} cluster, you need to configure an email account and related settings. For complete instructions, refer to [Configuring email accounts](/explore-analyze/alerts-cases/watcher/actions-email.md#configuring-email).

```yaml
xpack.notification.email.account:
    gmail_account:
        profile: gmail
        smtp:
            auth: true
            starttls.enable: true
            host: smtp.gmail.com
            port: 587
            user: <username>
```

Before you add the `xpack.notification.email*` user settings, make sure to store the SMTP password in the keystore as a [secure setting](../../../deploy-manage/security/secure-settings.md). In the previous example, use the key `xpack.notification.email.account.gmail_account.smtp.secure_password`.