---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Email action"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/actions-email.html
---

# Email action [actions-email]

Use the `email` action to send email notifications. To send email, you must [configure at least one email account](#configuring-email) in `elasticsearch.yml`.

Email notifications can be plain text or styled using HTML. You can include information from the watch execution payload using [templates](how-watcher-works.md#templates) and attach the entire watch payload to the message.

See [Email action attributes](#email-action-attributes) for the supported attributes. Any attributes that are missing from the email action definition are looked up in the email account configuration. The required attributes must either be set in the email action definition or the account’s `email_defaults`.

## Configuring email actions [configuring-email-actions]

You configure email actions in the `actions` array. Action-specific attributes are specified using the `email` keyword.

For example, the following email action uses a template to include data from the watch payload in the email body:

```js
"actions" : {
  "send_email" : { <1>
    "email" : { <2>
      "to" : "username@example.org", <3>
      "subject" : "Watcher Notification", <4>
      "body" : "{{ctx.payload.hits.total}} error logs found" <5>
    }
  }
}
```

1. The id of the action.
2. The action type is set to `email`.
3. One or more addresses to send the email to. Must be specified in the action definition or in the email account configuration.
4. The subject of the email can contain static text and Mustache [templates](how-watcher-works.md#templates).
5. The body of the email can contain static text and Mustache [templates](how-watcher-works.md#templates). Must be specified in the action definition or in the email account configuration.
%  NOTCONSOLE

## Configuring email attachments [configuring-email-attachments]

You can attach the execution context payload or data from an any HTTP service to the email notification. There is no limit on the number of attachments you can configure.

To configure attachments, specify a name for the attached file and the type of attachment: `data`, `http` or `reporting`. The `data` attachment type attaches the execution context payload to the email message. The `http` attachment type enables you to issue an HTTP request and attach the response to the email message. When configuring the `http` attachment type, you must specify the request URL. The `reporting` attachment type is a special type to include PDF rendered dashboards from kibana. This type is consistently polling the kibana app if the dashboard rendering is done, preventing long running HTTP connections, that are potentially killed by firewalls or load balancers in-between.

```js
"actions" : {
  "email_admin" : {
    "email": {
      "to": "John Doe <john.doe@example.com>",
      "attachments" : {
        "my_image.png" : { <1>
          "http" : { <2>
            "content_type" : "image/png",
            "request" : {
              "url": "http://example.org/foo/my-image.png" <3>
            }
          }
        },
        "dashboard.pdf" : {
          "reporting" : {
            "url": "http://example.org:5601/api/reporting/generate/dashboard/Error-Monitoring"
          }
        },
        "data.yml" : {
          "data" : {
            "format" : "yaml" <4>
          }
        }
      }
    }
  }
}
```

1. The ID of the attachment, which is used as the file name in the email attachment.
2. The type of the attachment and its specific configuration.
3. The URL from which to retrieve the attachment.
4. Data attachments default to JSON if you don’t specify the format.
%  NOTCONSOLE

| Name | Description |
| --- | --- |
| `content_type` | Sets the content type for the email attachment. By default,                    the content type is extracted from the response sent by the                    HTTP service. You can explicitly specify the content type to                    ensure that the type is set correctly in the email in case                    the response does not specify the content type or it’s specified                    incorrectly. Optional. |
| `inline` | Configures as an attachment to sent with disposition `inline`. This                    allows the use of embedded images in HTML bodies, which are displayed                    in certain email clients. Optional. Defaults to `false`. |
| `request` | Contains the HTTP request attributes. At a minimum, you must                    specify the `url` attribute to configure the host and path to                    the service endpoint. See [Webhook action attributes](actions-webhook.md#webhook-action-attributes) for                    the full list of HTTP request attributes. Required. |

| Name | Description |
| --- | --- |
| `format` | Attaches the watch data, equivalent to specifying `attach_data`                in the watch configuration. Possible values are `json` or `yaml`.                Defaults to `yaml` if not specified. |

| Name | Description |
| --- | --- |
| `url` | The URL to trigger the dashboard creation |
| `inline` | Configures as an attachment to sent with disposition `inline`. This                    allows the use of embedded images in HTML bodies, which are displayed                    in certain email clients. Optional. Defaults to `false`. |
| `retries` | The reporting attachment type tries to poll regularly to receive the                    created PDF. This configures the number of retries. Defaults to `40`.                    The setting `xpack.notification.reporting.retries` can be configured                    globally to change the default. |
| `interval` | The time to wait between two polling tries. Defaults to `15s` (this                    means, by default watcher tries to download a dashboard for 10 minutes,                    forty times fifteen seconds). The setting `xpack.notification.reporting.interval`                    can be configured globally to change the default. |
| `auth` | Additional auth configuration for the request, see                    [use watcher](../../report-and-share/automating-report-generation.md#use-watcher) for details |
| `proxy` | Additional proxy configuration for the request. See [HTTP input attributes](input-http.md#http-input-attributes)                    on how to configure the values. |

### Attaching reports to an email [email-action-reports]

You can use the `reporting` attachment type in an `email` action to automatically generate a Kibana report and distribute it via email.

See [Automating report generation](../../report-and-share/automating-report-generation.md).

## Email action attributes [email-action-attributes]

| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `account` | no | the default account | The [email account](#configuring-email) to use to send the email. |
| `from` | no | - | The email [address](#email-address) from which the email                                                            will be sent. The `from` field can contain Mustache                                                            [templates](how-watcher-works.md#templates) as long as it resolves to a                                                            valid email address. |
| `to` | yes | - | The email [addresses](#email-address) of the `to` recipients.                                                            The `to` field can contain Mustache [templates](how-watcher-works.md#templates)                                                            as long as it resolves to a valid email address. |
| `cc` | no | - | The email [addresses](#email-address) of the `cc` recipients.                                                            The `cc` field can contain Mustache [templates](how-watcher-works.md#templates)                                                            as long as it resolves to a valid email address. |
| `bcc` | no | - | The email [addresses](#email-address) of the `bcc` recipients.                                                            The `bcc` field can contain Mustache [templates](how-watcher-works.md#templates)                                                            as long as it resolves to a valid email address. |
| `reply_to` | no | - | The email [addresses](#email-address) that will be set on the                                                            message’s `Reply-To` header. The `reply_to` field can contain                                                            Mustache [templates](how-watcher-works.md#templates) as long as it resolves to                                                            a valid email address. |
| `subject` | no | - | The subject of the email. The subject can be static text or                                                            contain Mustache [templates](how-watcher-works.md#templates). |
| `body` | no | - | The body of the email. When this field holds a string, it                                                            will default to the text body of the email. Set as an object                                                            to specify either the text or the html body or both (using                                                            the fields below) |
| `body.text` | no | - | The plain text body of the email. The body can be static text                                                            or contain Mustache [templates](how-watcher-works.md#templates). |
| `body.html` | no | - | The html body of the email. The body can be static text or                                                            contain Mustache [templates](how-watcher-works.md#templates). This body will be                                                            sanitized to remove dangerous content such as scripts. This                                                            behavior can be disabled by setting                                                            `xpack.notification.email.html.sanitization.enabled: false` in                                                            `elasticsearch.yaml`. |
| `priority` | no | - | The priority of this email. Valid values are: `lowest`, `low`,                                                            `normal`, `high` and `highest`. The priority can contain a                                                            Mustache [template](how-watcher-works.md#templates) as long as it resolves to                                                            one of the valid values. |
| `attachments` | no | - | Attaches the watch payload (`data` attachment) or a file                                                            retrieved from an HTTP service (`http` attachment) to the                                                            email. For more information, see                                                            [Configuring Email Attachments](#configuring-email-attachments). |
| `attach_data` | no | false | Indicates whether the watch execution data should be attached                                                            to the email. You can specify a Boolean value or an object.                                                            If `attach_data` is set to  `true`, the data is attached as a                                                            YAML file. This attribute is deprecated, use the `attachments`                                                            attribute to add a `data` attachment to attach the watch payload. |
| `attach_data.format` | no | yaml | When `attach_data` is specified as an object, this field                                                            controls the format of the attached data. The supported formats                                                            are `json` and `yaml`. This attribute is deprecated, use the                                                            `attachments` attribute to add a `data` attachment to attach                                                            the watch payload. |

$$$email-address$$$

Email Address
:   An email address can contain two possible parts—​the address itself and an optional personal name as described in [RFC 822](http://www.ietf.org/rfc/rfc822.txt). The address can be represented either as a string of the form `user@host.domain` or `Personal Name <user@host.domain>`. You can also specify an email address as an object that contains `name` and `address` fields.

$$$address-list$$$

Address List
:   A list of addresses can be specified as a an array: `[ 'Personal Name <user1@host.domain>', 'user2@host.domain' ]`.

## Configuring email accounts [configuring-email]

{{watcher}} can send email using any SMTP email service. Email messages can contain basic HTML tags. You can control which groups of tags are allowed by [Configuring HTML Sanitization Options](#email-html-sanitization).

You configure the accounts {{watcher}} can use to send email in the `xpack.notification.email` namespace in `elasticsearch.yml`. The password for the specified SMTP user is stored securely in the [{{es}} keystore](../../../deploy-manage/security/secure-settings.md).

If your email account is configured to require two step verification, you need to generate and use a unique App Password to send email from {{watcher}}. Authentication will fail if you use your primary password.

### Email profiles [email-profile]

{{watcher}} provides three email profiles that control how MIME messages are structured: `standard` (default), `gmail`, and `outlook`. These profiles accommodate differences in how various email systems interpret the MIME standard. If you are using Gmail or Outlook, we recommend using the corresponding profile. Use the `standard` profile if you are using another email system.

For more information about configuring {{watcher}} to work with different email systems, see:

* [Sending email from Gmail](#gmail)
* [Sending email from Outlook.com](#outlook)
* [Sending email from Microsoft Exchange](#exchange)
* [Sending email from Amazon SES (Simple Email Service)](#amazon-ses)

If you configure multiple email accounts, you must either configure a default account or specify which account the email should be sent with in the `email` action.

```yaml
xpack.notification.email:
  default_account: team1
  account:
    team1:
      ...
    team2:
      ...
```

### Sending email from Gmail [gmail]

Use the following email account settings to send email from the [Gmail](https://mail.google.com) SMTP service:

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

To store the account SMTP password, use the keystore command (see [secure settings](../../../deploy-manage/security/secure-settings.md))

```yaml
bin/elasticsearch-keystore add xpack.notification.email.account.gmail_account.smtp.secure_password
```

If you get an authentication error that indicates that you need to continue the sign-in process from a web browser when {{watcher}} attempts to send email, you need to configure Gmail to [Allow Less Secure Apps to access your account](https://support.google.com/accounts/answer/6010255?hl=en).

If two-step verification is enabled for your account, you must generate and use a unique App Password to send email from {{watcher}}. See [Sign in using App Passwords](https://support.google.com/accounts/answer/185833?hl=en) for more information.

#### Sending email from Outlook.com [outlook]

Use the following email account settings to send email action from the [Outlook.com](https://www.outlook.com/) SMTP service:

```yaml
xpack.notification.email.account:
    outlook_account:
        profile: outlook
        smtp:
            auth: true
            starttls.enable: true
            host: smtp-mail.outlook.com
            port: 587
            user: <email.address>
```

To store the account SMTP password, use the keystore command (see [secure settings](../../../deploy-manage/security/secure-settings.md))

```yaml
bin/elasticsearch-keystore add xpack.notification.email.account.outlook_account.smtp.secure_password
```

When sending emails, you have to provide a from address, either a default one in your account configuration or as part of the email action in the watch.

::::{note}
You need to use a unique App Password if two-step verification is enabled. See [App passwords and two-step verification](http://windows.microsoft.com/en-us/windows/app-passwords-two-step-verification) for more information.
::::

#### Sending email from Amazon SES (Simple Email Service) [amazon-ses]

Use the following email account settings to send email from the [Amazon Simple Email Service](http://aws.amazon.com/ses) (SES) SMTP service:

```yaml
xpack.notification.email.account:
    ses_account:
        email_defaults:
            from: <email address of service account> <1>
        smtp:
            auth: true
            starttls.enable: true
            starttls.required: true
            host: email-smtp.us-east-1.amazonaws.com <2>
            port: 587
            user: <username>
```

1. In certain cases `email_defaults.from` is validated by Amazon SES to ensure that it is a valid local email account.
2. `smtp.host` varies depending on the region.

To store the account SMTP password, use the keystore command (see [secure settings](../../../deploy-manage/security/secure-settings.md))

```yaml
bin/elasticsearch-keystore add xpack.notification.email.account.ses_account.smtp.secure_password
```

::::{note}
You need to use your Amazon SES SMTP credentials to send email through Amazon SES. For more information, see [Obtaining Your Amazon SES SMTP Credentials](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.md). You might also need to verify [your email address](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.md) or [your whole domain](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-domains.md) at AWS.
::::

#### Sending email from Microsoft Exchange [exchange]

Use the following email account settings to send email action from Microsoft Exchange:

```yaml
xpack.notification.email.account:
    exchange_account:
        profile: outlook
        email_defaults:
            from: <email address of service account> <1>
        smtp:
            auth: true
            starttls.enable: true
            host: <your exchange server>
            port: 587
            user: <email address of service account> <2>
```

1. Some organizations configure Exchange to validate that the `from` field is a valid local email account.
2. Many organizations support use of your email address as your username, though it is a good idea to check with your system administrator if you receive authentication-related failures.

To store the account SMTP password, use the keystore command (see [secure settings](../../../deploy-manage/security/secure-settings.md))

```yaml
bin/elasticsearch-keystore add xpack.notification.email.account.exchange_account.smtp.secure_password
```

#### Configuring HTML sanitization options [email-html-sanitization]

The `email` action supports sending messages with an HTML body. However, for security reasons, {{watcher}} [sanitizes](https://en.wikipedia.org/wiki/HTML_sanitization) the HTML.

You can control which HTML features are allowed or disallowed by configuring the `xpack.notification.email.html.sanitization.allow` and `xpack.notification.email.html.sanitization.disallow` settings in `elasticsearch.yml`. You can specify individual HTML elements and [HTML feature groups](elasticsearch://reference/elasticsearch/configuration-reference/watcher-settings.md#html-feature-groups). By default, {{watcher}} allows the following features: `body`, `head`, `_tables`, `_links`, `_blocks`, `_formatting` and `img:embedded`.

For example, the following settings allow the HTML to contain tables and block elements, but disallow  `<h4>`, `<h5>` and `<h6>` tags.

```yaml
xpack.notification.email.html.sanitization:
    allow: _tables, _blocks
    disallow: h4, h5, h6
```

To disable sanitization entirely, add the following setting to `elasticsearch.yml`:

```yaml
xpack.notification.email.html.sanitization.enabled: false
```
