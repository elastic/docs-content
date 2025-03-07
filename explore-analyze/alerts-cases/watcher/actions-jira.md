---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Jira action"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/actions-jira.html
---

# Jira action [actions-jira]

Use the `jira` action to create issues in [Atlassian’s Jira Software](https://www.atlassian.com/software/jira). To create issues you need to [configure at least one Jira account](#configuring-jira) in `elasticsearch.yml`.

## Configuring Jira actions [configuring-jira-actions]

You configure Jira actions in the `actions` array. Action-specific attributes are specified using the `jira` keyword.

The following snippet shows a simple jira action definition:

```js
"actions" : {
  "create-jira-issue" : {
    "transform" : { ... },
    "throttle_period" : "5m",
    "jira" : {
      "account" : "integration-account", <1>
      "fields" : {
          "project" : {
            "key": "PROJ" <2>
          },
          "issuetype" : {
            "name": "Bug" <3>
          },
          "summary" : "Encountered {{ctx.payload.hits.total}} errors in the last 5 minutes", <4>
          "description" : "Encountered {{ctx.payload.hits.total}} errors in the last 5 minutes (facepalm)", <5>
          "labels" : ["auto"], <6>
          "priority" : {
            "name" : "High" <7>
          }
      }
    }
  }
}
```

1. The name of a Jira account configured in `elasticsearch.yml`.
2. The key of the Jira project in which the issue will be created.
3. The name of the issue type.
4. The summary of the Jira issue.
5. The description of the Jira issue.
6. The labels to apply to the Jira issue.
7. The priority of the Jira issue.
%  NOTCONSOLE

## Jira action attributes [jira-action-attributes]

Depending of how Jira projects are configured, the issues can have many different fields and values. Therefore the `jira` action can accept any type of sub fields within its `issue` field. These fields will be directly used when calling Jira’s [Create Issue API](https://docs.atlassian.com/jira/REST/cloud/#api/2/issue-createIssue), allowing any type of custom fields to be used.

::::{note}
The `project.key` (or `project.id`), the `issuetype.name` (or `issuetype.id`) and `issue.summary` are always required to create an issue in Jira.
::::

| Name | Required | Description |
| --- | --- | --- |
| `account` | no | The Jira account to use to send the message. |
| `proxy.host` | no | The proxy host to use (only in combination with `proxy.port`) |
| `proxy.port` | no | The proxy port to use (only in combination with `proxy.host`) |
| `fields.project.key` | yes | The key of the Jira project in which the issue will be created.                                       It can be replaced by `issue.project.id` if the identifier of the                                       project is known. |
| `fields.issuetype.name` | yes | A name that identifies the type of the issue. Jira provides default                                       issue types like `Bug`, `Task`, `Story`, `New Feature` etc. It can                                       be replaced by `issue.issuetype.id` if the identifier of the type                                       is known. |
| `fields.summary` | yes | The summary (or title) of the issue. |
| `fields.description` | no | The description of the issue. |
| `fields.labels` | no | The labels to apply to the Jira issue. |
| `fields.priority.name` | no | The priority of the Jira issue. Jira provides default `High`,                                       `Medium` and `Low` priority levels. |
| `fields.assignee.name` | no | Name of the user to assign the issue to. |
| `fields.reporter.name` | no | Name of the user identified as the reporter of the issue.                                      Defaults to the user account. |
| `fields.environment` | no | Name of the environment related to the issue. |
| `fields.customfield_XXX` | no | Custom field XXX of the issue (ex: "customfield_10000": "09/Jun/81") |

## Configuring Jira accounts [configuring-jira]

You configure the accounts {{watcher}} can use to communicate with Jira in the `xpack.notification.jira` namespace in `elasticsearch.yml`.

{{watcher}} supports Basic Authentication for Jira Software. To configure a Jira account you need to specify (see [secure settings](../../../deploy-manage/security/secure-settings.md)):

```yaml
bin/elasticsearch-keystore add xpack.notification.jira.account.monitoring.secure_url
bin/elasticsearch-keystore add xpack.notification.jira.account.monitoring.secure_user
bin/elasticsearch-keystore add xpack.notification.jira.account.monitoring.secure_password
```
::::{warning}
Storing sensitive data (`url`, `user` and `password`) in the configuration file or the cluster settings is insecure and has been deprecated. Please use {{es}}'s secure [keystore](../../../deploy-manage/security/secure-settings.md) method instead.

::::

To avoid credentials that transit in clear text over the network, {{watcher}} will reject `url` settings like `http://internal-jira.elastic.co` that are based on plain text HTTP protocol. This default behavior can be disabled with the explicit `allow_http` setting:

::::{note}
The `url` field can also contain a path, that is used to create an issue. By default this is `/rest/api/2/issue`. If you set this as well, make sure that this path is the full path to the endpoint to create an issue.
::::

```yaml
xpack.notification.jira:
  account:
    monitoring:
      allow_http: true
```

::::{warning}
It is strongly advised to use Basic Authentication with secured HTTPS protocol only.
::::

You can also specify defaults for the [Jira issues](elasticsearch://reference/elasticsearch/configuration-reference/watcher-settings.md#jira-account-attributes):

```yaml
xpack.notification.jira:
  account:
    monitoring:
      issue_defaults:
        project:
          key: proj
        issuetype:
          name: Bug
        summary: "X-Pack Issue"
        labels: ["auto"]
```

If you configure multiple Jira accounts, you either need to configure a default account or specify which account the notification should be sent with in the `jira` action.

```yaml
xpack.notification.jira:
  default_account: team1
  account:
    team1:
      ...
    team2:
      ...
```
