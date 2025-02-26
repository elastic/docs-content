---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-custom-links.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-create-custom-links.html

navigation_title: "Create custom links"
---

# Custom links in the Applications UI [apm-custom-links]

::::{note}

**For serverless Observability projects**, the **Editor** role or higher is required to create and manage custom links. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


Elastic’s custom link feature allows you to easily create up to 500 dynamic links based on your specific APM data. Custom links can be filtered to only appear in the Applications UI for relevant services, environments, transaction types, or transaction names.

Ready to dive in? Jump straight to the [examples](#custom-links-examples).


## Create a link [custom-links-create]

Each custom link consists of a label, URL, and optional filter. The easiest way to create a custom link is from within the actions dropdown in the transaction detail page. This method will automatically apply filters, scoping the link to that specific service, environment, transaction type, and transaction name.

Alternatively, you can create a custom link in the Applications UI by navigating to **Settings** > **Customize UI**, and selecting **Create custom link**.


### Label [custom-links-label]

The name of your custom link. The actions context menu displays this text, so keep it as short as possible.

::::{tip}
Custom links are displayed alphabetically in the actions menu.
::::



### URL [custom-links-url]

The URL your link points to. URLs support dynamic field name variables, encapsulated in double curly brackets: `{{field.name}}`. These variables will be replaced with transaction metadata when the link is clicked.

Because everyone’s data is different, you’ll need to examine your traces to see what metadata is available for use. To do this, select a trace in the Applications UI, and click **Metadata** in the **Trace Sample** table.

:::{image} ../../../images/observability-example-metadata.png
:alt: Example metadata
:class: screenshot
:::


### Filters [custom-links-filters]

Filter each link to only appear for specific services or transactions. You can filter on the following fields:

* `service.name`
* `service.env`
* `transaction.type`
* `transaction.name`

Multiple values are allowed when comma-separated.


## Custom link examples [custom-links-examples]

Not sure where to start with custom links? Take a look at the examples below and customize them to your liking!


### Email [custom-links-examples-email]

Email the owner of a service.

|     |     |
| --- | --- |
| Label | `Email <SERVICE_NAME> engineer` |
| Link | `mailto:<TEAM_OR_ENGINEER>@<COMPANY_NAME>.com` |
| Filters | `service.name:<SERVICE_NAME>` |

**Example**

This link opens an email addressed to the team or owner of `python-backend`. It will only appear on services with the name `python-backend`.

|     |     |
| --- | --- |
| Label | `Email python-backend engineers` |
| Link | `mailto:python_team@elastic.co` |
| Filters | `service.name:python-backend` |


### GitHub issue [custom-links-examples-gh]

Open a GitHub issue with pre-populated metadata from the selected trace sample.

|     |     |
| --- | --- |
| Label | `Open an issue in <REPO_NAME>` |
| Link | `https://github.com/<ORG>/<REPO>/issues/new?title=<TITLE>&body=<BODY>` |
| Filters | `service.name:client` |

**Example**

This link opens a new GitHub issue in the apm-agent-rum repository. It populates the issue body with relevant metadata from the currently active trace. Clicking this link results in the following issue being created:

:::{image} ../../../images/observability-create-github-issue.png
:alt: Example github issue
:class: screenshot
:::

|     |     |
| --- | --- |
| Label | `Open an issue in apm-rum-js` |
| Link | `https://github.com/elastic/apm-agent-rum-js/issues/new?title=Investigate+APM+trace&body=Investigate+the+following+APM+trace%3A%0D%0A%0D%0Aservice.name%3A+{{service.name}}%0D%0Atransaction.id%3A+{{transaction.id}}%0D%0Acontainer.id%3A+{{container.id}}%0D%0Aurl.full%3A+{{url.full}}` |
| Filters | `service.name:client` |

See the [GitHub automation documentation](https://help.github.com/en/github/managing-your-work-on-github/about-automation-for-issues-and-pull-requests-with-query-parameters) for a full list of supported query parameters.


### Jira task [custom-links-examples-jira]

Create a Jira task with pre-populated metadata from the selected trace sample.

|     |     |
| --- | --- |
| Label | `Open an issue in Jira` |
| Link | `https://<JIRA_BASE_URL>/secure/CreateIssueDetails!init.jspa?<ARGUMENTS>` |

**Example**

This link creates a new task on the Engineering board in Jira. It populates the issue body with relevant metadata from the currently active trace. Clicking this link results in the following task being created in Jira:

:::{image} ../../../images/observability-create-jira-issue.png
:alt: Example jira issue
:class: screenshot
:::

|     |     |
| --- | --- |
| Label | `Open a task in Jira` |
| Link | `https://test-site-33.atlassian.net/secure/CreateIssueDetails!init.jspa?pid=10000&issuetype=10001&summary=Created+via+APM&description=Investigate+the+following+APM+trace%3A%0D%0A%0D%0Aservice.name%3A+{{service.name}}%0D%0Atransaction.id%3A+{{transaction.id}}%0D%0Acontainer.id%3A+{{container.id}}%0D%0Aurl.full%3A+{{url.full}}` |

See the [Jira application administration knowledge base](https://confluence.atlassian.com/jirakb/how-to-create-issues-using-direct-html-links-in-jira-server-159474.md) for a full list of supported query parameters.


### Dashboards [custom-links-examples-kib]

Link to a custom dashboard.

|     |     |
| --- | --- |
| Label | `Open transaction in custom visualization` |
| Link | `https://kibana-instance/app/kibana#/dashboard?_g=query:(language:kuery,query:'transaction.id:{{transaction.id}}'...` |

**Example**

This link opens the current `transaction.id` in a custom dashboard. There are no filters set.

|     |     |
| --- | --- |
| Label | `Open transaction in Python drilldown viz` |
| URL | `https://kibana-instance/app/kibana#/dashboard?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-24h,to:now))&_a=(description:'',filters:!(),fullScreenMode:!f,options:(hidePanelTitles:!f,useMargins:!t),panels:!((embeddableConfig:(),gridData:(h:15,i:cb79c1c0-1af8-472c-aaf7-d158a76946fb,w:24,x:0,y:0),id:c8c74b20-6a30-11ea-92ab-b5d3feff11df,panelIndex:cb79c1c0-1af8-472c-aaf7-d158a76946fb,type:visualization,version:'7.7')),query:(language:kuery,query:'transaction.id:{{transaction.id}}'),timeRestore:!f,title:'',viewMode:edit)` |


### Slack channel [custom-links-examples-slack]

Open a specified slack channel.

|     |     |
| --- | --- |
| Label | `Open SLACK_CHANNEL` |
| Link | `https://COMPANY_SLACK.slack.com/archives/SLACK_CHANNEL` |
| Filters | `service.name` : `SERVICE_NAME` |

**Example**

This link opens a company slack channel, #apm-user-support. It only appears when `transaction.name` is `GET user/login`.

|     |     |
| --- | --- |
| Label | `Open #apm-user-support` |
| Link | `https://COMPANY_SLACK.slack.com/archives/efk52kt23k` |
| Filters | `transaction.name:GET user/login` |


### Website [custom-links-examples-web]

Open an internal or external website.

|     |     |
| --- | --- |
| Label | `Open <WEBSITE>` |
| Link | `https://<COMPANY_SLACK>.slack.com/archives/<SLACK_CHANNEL>` |
| Filters | `service.name:<SERVICE_NAME>` |

**Example**

This link opens more data on a specific `user.email`. It only appears on front-end transactions.

|     |     |
| --- | --- |
| Label | `View user internally` |
| Link | `https://internal-site.company.com/user/{{user.email}}` |
| Filters | `service.name:client` |