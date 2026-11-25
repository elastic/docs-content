---
navigation_title: Connect data and tools
applies_to:
  serverless:
    observability: preview
description: Connect Elastic nightshift to your Elasticsearch data, GitHub code, other APIs, and Slack, so investigations can test more hypotheses and reach your team where it works.
products:
  - id: observability
  - id: cloud-serverless
---

# Connect data and tools to your {{nightshift}} investigations [nightshift-set-up]

An investigation can only test what it can reach. Connect the telemetry, code, configuration, and runbooks that your team uses during an incident, and investigations can check them too. Setting up for the first time? Start with [Get started](../get-started.md).

Investigations can use the following connections:

- [Local {{es}}](#nightshift-set-up-local-es): Logs, metrics, and traces in your {{nightshift}} project, created when {{nightshift}} is enabled.
- [External {{es}}](#nightshift-set-up-external-es): Data in another cluster or project, or in projects linked through [{{cps}}](/deploy-manage/cross-project-search-config.md).
- [GitHub](#nightshift-set-up-github): Code, configuration, runbooks, and recent commits, pull requests, and issues. Connecting gives more information on *why* something broke.
- [HTTP](#nightshift-set-up-http): Data from any other API, such as a runbook service or deploy history. Optional.
- [Slack](#nightshift-set-up-slack): A place to ask for help and to post results. Optional, but required to post automation results to a channel.

To reach any other tool, use an HTTP connector. Refer to [Extend investigations](./extend.md).

## Before you begin [nightshift-set-up-prereqs]

- An admin has [enabled {{nightshift}}](../get-started.md#nightshift-get-started-enable).
- You have the privileges to open the **Settings** page. Refer to [Grant access](../privileges.md#nightshift-privileges-admin).

You manage connections on the **General** tab of the **Settings** page. On the {{nightshift}} home page, open the {icon}`boxes_vertical` menu and select **Settings**.

To add a connector, select **Add connector**. The flyout lists the connector types that investigations can use, with how many you have of each. Select **Create connector** next to a type. Investigations can use only connectors that you add from this flyout. A connector that you create in **Stack Management** isn't assigned to investigations. To manage connectors in the rest of {{kib}}, select **Open in Stack Management**. Refer to [Connectors](kibana://reference/connectors-kibana.md).


## How investigations use connections [nightshift-set-up-how]

Investigations reach your systems through connectors, from a temporary sandbox.

- **Each investigation gets its own sandbox**: which is discarded when the investigation ends.
- **Connectors hold shared credentials**: A connector uses one set of credentials for every investigation, from whoever started it.
- **Access is as read-only as your credentials**: Give every connector, HTTP included, credentials that can only read, such as a read-only {{es}} API key and GitHub token. A connector with write access lets investigations write too. The exception is a connector for remediation workflows. Refer to [Remediate with workflows](./extend.md#nightshift-extend-remediate).
- **The sandbox can reach only known hosts**: A command that uses a connector can reach that connector's host. To allow other hosts, refer to [Sandbox egress allowlist](#nightshift-set-up-egress).

## Set up a Local {{es}} connector [nightshift-set-up-local-es]

When {{nightshift}} is enabled, it creates a **Local Elasticsearch** connector, type `.elasticsearch`, that investigations use to query the logs, metrics, and traces in this project. You don't need to set anything up. Don't delete it.

The **Local Elasticsearch** connector searches only this project. To search projects linked through [{{cps}}](/deploy-manage/cross-project-search-config.md), add an External {{es}} connector with an API key that has connected cluster access. Refer to [Search projects linked through {{cps}}](#nightshift-set-up-cps).

## Set up an External {{es}} connector [nightshift-set-up-external-es]

Add an External {{es}} connector when your data is in another cluster or project, for example a separate production deployment, or in projects linked through {{cps}}. For what works with each deployment type, refer to [Reference architecture](../reference-architecture.md).

For the steps, including the API key request, refer to [Add data](../get-started.md#nightshift-get-started-add-data). After setup, start from **Add connector** on the **General** tab, then select **Create connector** next to **External Elasticsearch**.

:::{dropdown} Authentication
**API key format.** Paste the `encoded` value as it is. You don't need to add the `ApiKey` prefix: {{kib}} adds it when it's missing. If you already added it, that works too.

**Username and password.** You can also authenticate with a **Username and password**. The user needs at least the `read` privilege on the indices that investigations search. An API key is easier to limit and to revoke.

For all connector settings, refer to [External {{es}} connector](kibana://reference/connectors-kibana/elasticsearch-action-type.md).
:::


### Search projects linked through {{cps}} [nightshift-set-up-cps]

To let investigations search the projects linked to your {{nightshift}} project, create an External {{es}} connector that points to the {{nightshift}} project, with an API key that you create in the {{ecloud}} console. An API key that you create in {{kib}} can't search linked projects.

1. In the [{{ecloud}} console](https://cloud.elastic.co/), open your {{nightshift}} project and select **Manage project**.
1. Select **Actions** at the top right, then **Create API key**.
1. Turn on **Cloud resource access**, and grant at least the **Viewer** role on the project.
1. Turn on **Connected cluster access**.
1. Create the key, and copy its `encoded` value.
1. Copy the {{es}} endpoint of the {{nightshift}} project.
1. Create an External {{es}} connector with this endpoint and API key. Follow the steps in [Add data](../get-started.md#nightshift-get-started-add-data), and skip the API key request.

## Set up GitHub [nightshift-set-up-github]

Connect GitHub so investigations can read the code, configuration, Helm charts, and runbooks behind your services, and check what changed recently. For example, an investigation into database lock timeouts can find the commit that changed the query.

{{nightshift}} doesn't copy, sync, or index your repositories. Refer to [Your code](../cost-and-models.md#nightshift-data).

For the steps to create a fine-grained personal access token and connect it, refer to [Connect GitHub](../get-started.md#nightshift-get-started-other-sources). After setup, start from **Add connector** on the **General** tab, then select **Create connector** next to **GitHub**. Leave **Receive events** turned off: investigations don't need it.

To point investigations at the right repositories, name them in the instructions of an automation, or in custom context. For example, "The source for the checkout services is in `acme/checkout`." Refer to [Automation instructions](./automations.md#nightshift-automations-instructions) and [Custom context](./extend.md#nightshift-extend-custom-context).

For all GitHub connector settings, refer to [GitHub connector](kibana://reference/connectors-kibana/github-action-type.md).

## HTTP [nightshift-set-up-http]

Add an HTTP connector to reach any other system with an HTTP API, for example a runbook service, your CI system, or a deploy log: on the **General** tab, select **Add connector**, then **HTTP**. Describe the API in custom context. Refer to [Connect any system with an HTTP API](./extend.md#nightshift-extend-http).

## Set up Slack [nightshift-set-up-slack]

Connect Slack so your team can ask {{nightshift}} for help in a channel, and automations can post results there. An admin connects the workspace once, then each channel. Private channels need extra access and work only with mentions. Refer to [Private channels](../slack-app.md#nightshift-slack-app-private).

1. On the {{nightshift}} **Settings** page, on the **General** tab, in the **Slack** section, select **Connect Slack**.
1. Authorize the `@Elastic` Slack app in Slack. When {{kib}} asks **Is this the right workspace?**, select **Yes**.

   The authorization applies to the whole Slack workspace, including every Elastic deployment that's connected to it.
1. In Slack, invite `@Elastic` to each channel that you want to use, for example with `/invite @Elastic`.
1. Back in **Slack channels**, select **Connect channels**.
1. In **Connect a channel**, select the channel from the **Channel** list, then select **Connect**. The list shows only public channels, so for a private channel, or any channel that isn't listed, enter its channel ID or a link copied from Slack.

The channel appears in the **Channels** table with its name and ID. A private channel shows only its ID. `@Elastic` answers only in connected channels.

To stop `@Elastic` from answering in a channel, select **Disconnect channel** next to it. The bot stays in the channel until someone removes it in Slack, and replies that the channel isn't connected when someone mentions it. To remove the whole workspace, open the workspace's actions menu and select **Disconnect workspace**.

A mention of `@Elastic` that opens a new conversation in a connected channel gets an answer, not an investigation. It still counts toward the **Manual investigations daily limit**. For what your team can do in Slack, refer to [Investigate in Slack](../use-cases/investigate-in-slack.md). For the Slack permissions that the app requests, how it behaves in channels, and what Slack data Elastic stores, refer to [Elastic app for Slack](../slack-app.md).

## Sandbox egress allowlist [nightshift-set-up-egress]

The investigation sandbox can reach only your connectors' hosts and the hosts you allow. To allow others, such as a package index to install a tool, use the allowlist on the **Investigations** tab of the **Settings** page. For the rule syntax, refer to [Sandbox egress allowlist](../settings.md#nightshift-settings-egress).

## Next steps [nightshift-set-up-next]

- [How investigations work](./index.md): Learn how investigations use your data and code.
- [Automations](./automations.md): Start investigations for you, and post the results to Slack.
- [Investigate in Slack](../use-cases/investigate-in-slack.md): Ask {{nightshift}} for help from a connected channel.
- [Extend investigations](./extend.md): Add custom context, connect other APIs, and let investigations run your workflows.
