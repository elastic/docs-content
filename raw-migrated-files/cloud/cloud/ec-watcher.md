# Enable Watcher [ec-watcher]

::::{note}
If you are looking for Kibana alerting, check [Alerting and Actions](../../../explore-analyze/alerts-cases.md) in the Kibana Guide.
::::


Watcher lets you take action based on changes in your data. It is designed around the principle that, if you can query something in Elasticsearch, you can alert on it. Simply define a query, condition, schedule, the actions to take, and Watcher will do the rest.

Watcher can be enabled when configuring your cluster. You can run Alerting on a separate cluster from the cluster whose data you are actually watching.


## Before you begin [ec_before_you_begin_8]

Some restrictions apply when adding alerts. To learn more, check [Restrictions for alerts (via Watcher)](../../../deploy-manage/deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-watcher).

To enable Watcher on a cluster, you may first need to perform one or several of the following steps. The options shown in the UI differ between stack versions; if an option is not available, you can skip it.

* To receive default Elasticsearch Watcher alerts (cluster status, nodes changed, version mismatch), you need to have monitoring enabled to send to the Admin email address specified in Kibana. To enable this, go to **Advanced Settings > Admin email**.

To learn more about Kibana alerting and how to use it, check [Alerting and Actions](../../../explore-analyze/alerts-cases.md).


## Send alerts by email [ec-watcher-allowlist]

Alerting can send alerts by email. You can configure notifications similar to the [operational emails](../../../deploy-manage/cloud-organization/operational-emails.md) that Elasticsearch Service sends automatically to alert you about performance issues in your clusters.

Watcher in Elastic Cloud is preconfigured with an email service and can be used without any additional configuration. Alternatively, a custom mail server can be configured as described in [Configuring a custom mail server](../../../explore-analyze/alerts-cases/watcher.md#ec-watcher-custom-mail-server)

You can optionally add [HTML sanitization](../../../explore-analyze/alerts-cases/watcher/actions-email.md#email-html-sanitization) settings under [Elasticsearch User settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) in the [Elasticsearch Service Console](https://cloud.elastic.co?page=docs&placement=docs-body) so that HTML elements are sanitized in the email notification.

For more information on sending alerts by email, check [Email action](../../../explore-analyze/alerts-cases/watcher/actions-email.md).


## Cloud email service limits [ec-cloud-email-service-limits]

The following quotas apply when using the Elastic email service:

* Email sending quota: 500 emails per 15min period
* Maximum number of recipients per message: 30 recipients per email (To, CC and BCC all count as recipients).
* Maximum message size (including attachments): 10 MB per message (after base64 encoding).
* The email-sender can’t be customized (Any custom `From:` header will be removed)


## Advanced usage [ec_advanced_usage]


### Slack and PagerDuty integration [ec-advanced-usage]

Under the hood, Alerting is configured through `elasticsearch.yml`. If you want to customize your Alerting settings, you can provide custom `elasticsearch.yml` snippet which is appended to your configuration.

To provide the custom snippet, you can use the console [Elasticsearch settings editor](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) for your deployment.

For example if you want to use the Slack integration:

There are three steps to integrate Elasticsearch with Slack:

1. Generate a Webhook URL in Slack.  It will look similar to `https://hooks.slack.com/services/..`
2. Add a Slack account name to your [Elasticsearch User settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md)
3. Associate the Slack account with the Slack Webhook in the Elasticsearch keystore

To add a webhook in Slack, select the settings icon, then choose **Add an app** and search for `webhook`.

The following example shows a configuration with multiple Slack accounts (`account1`, `account2`, and `account3`) specified in `elasticsearch.yml`:

```sh
xpack.notification.slack:
  default_account: account1
  account:
    account1:
      message_defaults:
        from: account1
        to: channel1
    account2:
      message_defaults:
        from: account2
        to: channel2
    account3:
      message_defaults:
        from: account3
        to: channel3
```


### Slack Webhook account settings [slack-webhook-setting]

The Slack Webhook is set for each account in the Elasticsearch Keystore with the following settings:

Setting name
:   `xpack.notification.slack.account.ACCOUNT_NAME.secure_url` where ACCOUNT_NAME is the Slack account, such as `account1`.

Type
:   Single string

Secret
:   The Webhook URL you generated in Slack earlier.

::::{note}
To specify a Slack account to use for a Watcher Alert that isn’t set as `default_account`, you must create an Advanced Watch and explicitly define which Slack account to use in the actions section.
::::


If you have a Slack account that is not currently set as *default_account*, and you want to use this account for a Watcher Alert, you must create an Advanced Watch and explicitly define in the Actions section of the UI which Slack account to use.

```sh
PUT _watcher/watch/test-alarm
{
  "metadata" : {
    ...
  },
  "trigger" : {
    ...
  },
  "input" : {
    ...
  },
  "actions" : {
    "notify-slack" : {
      "throttle_period" : "10s",
      "slack" : {
        "account" : "account2",
        "message" : {
          "to" : [ "#testing-channel" ],
          "text" : "You Know, for Search"
        }
      }
    }
  }
}
```

**In Elasticsearch versions before 7.0:**, you are not required to use the Elasticsearch keystore. Instead, you can use the console Elasticsearch settings editor for your deployment.

:::{image} ../../../images/cloud-user-settings.png
:alt: Advanced Alerting configuration
:::


## Configuring a custom mail server [ec-watcher-custom-mail-server]

It is possible to use a custom mail service instead of the one configured by default. It can be configured by following the [Elasticsearch documentation for configuring email accounts](https://www.elastic.co/guide/en/elasticsearch/reference/current/actions-email.html).

An example on how to configure a new account from the Elastic cloud console:

1. From your deployment menu, go to the **Edit** page.
2. In the **Elasticsearch** section, select **Manage user settings and extensions**.
3. Add the settings for a new mail account.

    ```yaml
    xpack.notification.email:
      default_account: my_email_service
      account:
        my_email_service:
            smtp:
                auth: true
                starttls.enable: true
                starttls.required: true
                host: email-smtp.us-east-1.amazonaws.com
                port: 587
                user: <username>
    ```

4. Select **Save changes**.
5. To complete the configuration, the password for the email service has to be added to the keystore

    1. Follow the steps described in our security settings documentation to [Add a secret value](../../../deploy-manage/security/secure-settings.md#ec-add-secret-values) to the keystore
    2. Set the **Setting name** as `xpack.notification.email.account.my_email_service.smtp.secure_password` (The account name must match the configuration in the user settings).

6. The new email account is now set up. It will now be used by default for watcher email actions.

For a full reference of all available settings, see the [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/notification-settings.html#email-notification-settings).

