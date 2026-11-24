---
navigation_title: Elastic app for Slack
applies_to:
  serverless:
    observability: preview
description: What your team sees when it works with the Elastic app for Slack, what each person does to set it up, what happens to your Slack messages, and which Slack permissions the app requests.
products:
  - id: observability
  - id: cloud-serverless
---

# Elastic app for Slack [nightshift-slack-app]

The Elastic app for Slack brings {{nightshift}} into your Slack workspace as `@Elastic`. In a connected channel, anyone can mention `@Elastic` to ask a question, and {{nightshift}} answers in the thread. Automations can also post investigation results to a connected channel.

This page follows the people who meet `@Elastic`, in the order they meet it: the admins who set it up, the people who ask it questions, and the security reviewers who need to know where Slack data goes. The messages `@Elastic` posts are shown here, so nothing in your channels comes as a surprise.

:::{image} ../../images/nightshift-slack-mention-answer.png
:alt: A Slack thread where a person mentions @Elastic and gets a threaded answer with a View in Kibana link
:screenshot:
:::

## Who does what [nightshift-slack-app-people]

| Role | What they do | Where they do it |
| --- | --- | --- |
| Slack admin | Approves the app if your workspace requires approval, and decides whether `@Elastic` can work in private channels. | Slack |
| {{nightshift}} admin | Connects the Slack workspace to the project, then connects each channel. Needs **nightshift**: **All** and **Manage engines**. Refer to [Grant access](./privileges.md). Without **Manage engines**, {{kib}} shows the Slack settings but you can't change them. | {{kib}} |
| Channel member | Invites `@Elastic` to the channel, then mentions it to ask questions. | Slack |
| Security reviewer | Reviews the permissions, the identity `@Elastic` acts as, and where Slack data goes. | This page |

Slack users don't need an Elastic account, and they aren't matched to Elastic users. Refer to [Who `@Elastic` acts as](#nightshift-slack-app-identity).

## Set up `@Elastic` [nightshift-slack-app-setup]

Setting up takes three people, or one person wearing all three hats.

### Connect the workspace ({{nightshift}} admin and Slack admin) [nightshift-slack-app-setup-workspace]

1. On the {{nightshift}} **Settings** page, on the **General** tab, in the **Slack** section, select **Connect Slack**.
1. Slack asks you to allow the app. Select **More permissions** to see everything it requests before you select **Allow**. Each permission is explained in [Slack permissions](#nightshift-slack-app-scopes).

   Private channel access is optional on this screen. Allow it only if your team wants to mention `@Elastic` in private channels. Refer to [Private channels](#nightshift-slack-app-private).
1. Back in {{kib}}, confirm the workspace when asked **Is this the right workspace?**. The section is now titled **Slack channels**, shows the workspace name next to its title, and asks you to connect channels.

   :::{image} ../../images/nightshift-slack-settings-connected.png
   :alt: Nightshift Settings with the Slack workspace connected and a Connect channels button
   :screenshot:
   :::

One installation serves the whole Slack workspace. Several Elastic projects, such as production and staging, can connect to the same workspace, and each channel connects to exactly one of them.

### Invite `@Elastic` to a channel (channel member) [nightshift-slack-app-setup-invite]

In the channel, invite the app, for example with `/invite @Elastic`. Until an admin connects the channel, `@Elastic` posts this and answers nothing:

> Thanks for adding Elastic! This channel isn't connected yet. Ask your Elastic admin to connect it in Kibana Settings using channel ID `C0123456789`.

Copy the channel ID from this message and send it to your {{nightshift}} admin.

### Connect the channel ({{nightshift}} admin) [nightshift-slack-app-setup-channel]

1. In **Slack channels**, select **Connect channels**.
1. In **Connect a channel**, select the channel from the **Channel** list, then select **Connect**. The list shows public channels that `@Elastic` has been invited to and that no project has connected yet. For a private channel, invite `@Elastic` in Slack, then enter its channel ID or a link copied from Slack.

   :::{image} ../../images/nightshift-slack-connect-dialog.png
   :alt: The Connect a channel dialog in Nightshift Settings
   :screenshot:
   :::

When the channel is connected, `@Elastic` tells the channel which project it now answers for:

> Elastic `<project ID>` (`<project host>`) is connected to this channel and ready. Mention @Elastic in a thread to get started.

If `@Elastic` isn't in the channel yet, or the channel is private and the workspace doesn't allow private channel access, {{kib}} refuses it and says what to do:

> Invite @Elastic to the channel, then try again. If the channel is private, the workspace also needs private channel access. To allow it, disconnect the workspace and connect it again. A Slack admin may need to approve it, and you will need to reconnect your channels.

A channel answers for one project only. If another project already connected it, {{kib}} says the channel is already connected to another Elastic deployment, and that project has to disconnect it first.

Slack Connect channels shared with another organization aren't supported in Tech Preview. `@Elastic` ignores messages from the other organization, and investigations can't read the channel.

## Ask `@Elastic` a question [nightshift-slack-app-ask]

Anyone in a connected channel can mention `@Elastic`, either in a new message or in an existing thread. `@Elastic` replies in the thread, never in the channel itself.

1. **It shows that it's working.** The thread shows a plan titled **Rolling up my sleeves**, with a row for each step it runs, such as a query or a file it reads.
1. **The answer appears when it's done.** The answer appears under the plan, and the plan's title changes to **Finished N steps**, or **Done** when no steps ran.
1. **You can open the whole conversation.** Under every answer, `@Elastic` shows how many tool calls it made, how many tokens it used, how long it took, and a **View in {{kib}}** link to the conversation in {{nightshift}}.

To follow up, mention `@Elastic` again in the same thread. It continues the same conversation, so you don't need to repeat yourself.

When you mention it in a thread, `@Elastic` also reads the thread's first message and up to four of the latest messages from other people since its last answer. In a long thread, it may read only the first message.

`@Elastic` answers people. When another app posts a message that mentions `@Elastic`, it doesn't answer. That message can start an automation instead.

A mention that opens a new conversation counts toward the daily investigation limits, even though it doesn't start an investigation. Follow-up mentions in the same thread don't count. Refer to [Investigation limits](./investigation/limits.md).

### Troubleshoot `@Elastic` responses [nightshift-slack-app-notices]

The following table lists the messages that `@Elastic` posts when it can't answer your question, and what to do. If your project rejects a request for another reason, `@Elastic` posts the project's explanation without changing it.

| Where or when | The message `@Elastic` posts | What to do |
| --- | --- | --- |
| You mention it in a channel that isn't connected | This channel isn't connected yet. Ask your Elastic admin to connect it in Kibana Settings using channel ID `C0123456789`, then mention me again. | Send the channel ID to your admin. `@Elastic` posts this at most once every 10 minutes per channel, so later mentions in that window get no reply. |
| You open its **Messages** tab | Direct messages aren't supported yet. Mention me in a channel that's connected to Kibana instead. | Mention it in a connected channel. `@Elastic` posts this at most once an hour, and Slack doesn't let you type a message to the app. |
| You mention it while it's still answering in the same thread | Elastic is still answering an earlier message in this thread. Please ask again once that reply is posted. | `@Elastic` waits up to two minutes for the earlier answer before it posts this. Ask again once the answer is posted. |
| Your project can't be reached, or refuses the request | Sorry, I couldn't reach Elastic right now. Please try again in a few minutes. | `@Elastic` retries for about two minutes before it posts this. Try again later. If it keeps happening, ask your admin to check the Slack connection. Refer to [Who `@Elastic` acts as](#nightshift-slack-app-identity). |
| The Slack connection needs to be set up again | Your Elastic connection has expired. Please reconnect it in Kibana and try again. | Ask your {{nightshift}} admin to disconnect and connect the workspace again. |
| A daily limit is reached | The daily limit of 5 for manual investigations has been reached. An admin can raise it in nightshift settings. The number is your project's limit, and the message names the limit that was reached. | Ask your {{nightshift}} admin. Refer to [Investigation limits](./investigation/limits.md). |
| The answer fails or stops | Elastic response failed., Elastic could not finish this turn., or Elastic stopped working on this request., under a plan titled **Stopped**, with a **View in {{kib}}** link | Open the conversation in {{kib}}, or ask again. |
| The agent finishes without an answer | Elastic completed without a response. | Open the conversation in {{kib}}, or ask again. |
| Slack rejects the answer | Couldn't post the answer here - Slack rejected the message. Open this conversation in Kibana to read it. | Open the conversation in {{kib}}. |
| The agent needs more input | Elastic needs more information to continue. Open the conversation in Kibana to answer. | Answer in {{kib}}. |
| The answer is longer than Slack allows | The answer, ending with: _Response truncated. Open the conversation in Kibana for the full answer._ | Select **View in {{kib}}**. |

When your project refuses your message, for example because the daily limit is reached, or `@Elastic` can't get it there at all, `@Elastic` also adds a `:warning:` reaction to your message, so you can spot it in a busy channel. An answer that fails after it started gets no reaction.

## Follow an investigation in Slack (on-call engineers) [nightshift-slack-app-investigations]

An automation can post an investigation to a connected channel, for example when an alert arrives from another tool. Within a minute, {{nightshift}} replies in the alert's thread with **⏳ Investigating…**, the automation's name, and a **View Full Investigation** button.

When the investigation finishes, {{nightshift}} edits that same message with the result: a title, the severity, the automation, **What happened**, **Impact**, **Conclusion**, and **Investigation details**, and the **View Full Investigation** button. If the investigation fails or times out, the message shows **⚠️ Investigation failed** or **⚠️ Investigation timed out** under the title, and says why under **What went wrong**.

In an investigation's thread, your team can work in two ways:

- **Mention `@Elastic`** to ask a question. You get an answer, and the investigation doesn't run again.
- **Reply without a mention** to add context. Every reply from a person is added to the investigation and runs it again, even a reply such as "thanks". `@Elastic` doesn't reply to you. Instead, when the run finishes, it updates the investigation's message in the thread. These runs don't count toward the daily limits, but each one uses model tokens.

Replies without a mention work in public channels only. Refer to [Investigate in Slack](./use-cases/investigate-in-slack.md).

## Private channels [nightshift-slack-app-private]

In a private channel, `@Elastic` answers mentions the same way it does in a public channel. Nothing else from a private channel reaches your project: messages there can't start automations, replies without a mention aren't added to an investigation, and investigations can't read the channel.

Private channel access is optional, and it's decided once for the whole Slack workspace, for every Elastic project connected to it. `@Elastic` still sees only the private channels that someone invites it to.

To allow it later, disconnect the workspace in {{kib}}, connect it again, and allow private channel access when Slack asks. A Slack admin may need to approve it. Disconnecting removes this project's channels, so connect them again afterwards. Then invite `@Elastic` to the private channel and connect it by channel ID or link, because private channels aren't in the **Channel** list.

To take private channel access away, remove the app from the workspace in Slack, then install it again and decline private channel access. Slack doesn't remove a permission from an existing installation. Removing the app disconnects every channel in every Elastic project connected to the workspace, so plan it with the other projects' admins.

## What `@Elastic` does with your messages [nightshift-slack-app-reads]

**When you mention `@Elastic`**
:   Your message, the thread's first message, and up to four of the latest messages from other people since `@Elastic` last answered there. Each of those thread messages is capped at 2,000 characters. The relay reads the thread again for every mention and doesn't keep it.

**Your name**
:   The display names of the people in the thread, so that answers and the investigation record show who said what. The relay holds names in memory for up to six hours and doesn't write them to disk. It doesn't read email addresses.

**Every message in a connected public channel**
:   The relay sends every message event in a connected public channel to your project, so that automations can match them, for example alerts that another app posts. This includes edits and deletions, and a deletion can include the deleted text. Messages that mention `@Elastic` go to the conversation instead, but edits and deletions of those messages are forwarded like any other message. Editing a message never changes an answer that `@Elastic` already gave.

**During an investigation**
:   An investigation can read recent messages in a connected public channel that `@Elastic` is a member of: the last two hours of a channel by default, and at most seven days at a time, or a whole thread. It can't read private channels, Slack Connect channels, direct messages, or channels that aren't connected to the project.

**What it never reads**
:   Channels that `@Elastic` isn't a member of, the content of files, and direct messages beyond the fact that one arrived.

## Who `@Elastic` acts as [nightshift-slack-app-identity]

`@Elastic` doesn't act as the person who mentions it. Every answer comes from what the {{nightshift}} service accounts and the connectors in the space can reach. Refer to [Privileges that {{nightshift}} runs with](./privileges.md#nightshift-privileges-accounts).

This matters for the people in the channel. Everyone in a connected channel can read what {{nightshift}} can read, including guests and people who join the channel later. Connect only the channels whose members should see that data. If only certain people should see some data, put that data in a separate project with its own {{nightshift}} setup.

When an admin connects Slack, {{kib}} creates a service account for the Slack connection, named `nightshift-relay-agent-builder-<ID>`. The relay uses it for two calls to your project: passing each mention to the {{nightshift}} agent, and forwarding messages from connected public channels so that automations can match them. The agent runs as the `nightshift_agent` account, so the Slack connection doesn't change what an answer can read.

Only the relay can use the account. For every call, it exchanges the account ID for a short-lived token, so no long-lived key is stored. When you disconnect the workspace, {{kib}} deletes the account.

The account's privileges are also capped by those of the admin who connected Slack. If that admin couldn't chat with the {{nightshift}} agent in **Agent Builder**, every mention gets **Sorry, I couldn't reach Elastic right now. Please try again in a few minutes.** Trying again doesn't help. Have an admin with **Agent Builder**: **All** disconnect the workspace and connect it again.

## Where your Slack data goes [nightshift-slack-app-data]

| Where | What's kept | How long |
| --- | --- | --- |
| The Slack relay | The workspace installation and its Slack bot token, which channels connect to which project, the channel names, the project's {{kib}} URL, and the ID of the project's Slack connection service account. The token and the account ID are encrypted. No message content. | Until the channel or workspace is disconnected, or the app is removed from Slack |
| The Slack relay, in transit | Slack events waiting to be delivered to your project, encrypted | Deleted when your project accepts the event, or within an hour if it can't be delivered |
| The Slack relay, per answer | IDs and state for an answer in progress, such as which message to update. No message content. | About an hour after the answer's last update |
| Your project | Conversations, investigations, and the Slack messages they include, with the names of the people who wrote them | Until you delete them. Refer to [Deleting data](./cost-and-models.md#nightshift-data). |
| Your project, the `.workflows-events` data stream | Every message event in a connected public channel, with its text, including events that no automation matches. Workflows logs them as trigger events. | No retention period is set on the data stream |
| Models through EIS | The Slack messages in a thread, sent along with the rest of the conversation or investigation | Refer to [What it sends to models](./cost-and-models.md#nightshift-data) |
| Slack | The messages that `@Elastic` posts | Your Slack workspace's retention settings |

The relay runs in a single AWS region, `us-east-1`, during Tech Preview. Slack events for every project pass through it, whatever region the project is in. If your organization requires Slack data to stay in a specific region, check this before you connect Slack.

For how Elastic processes personal data, including the Data Processing Addendum and GDPR, refer to the [Elastic Trust Center](https://www.elastic.co/trust).

## Disconnect or remove the app [nightshift-slack-app-disconnect]

Each way out affects different people. Tell the channel before you do it.

**Disconnect a channel**
:   On the {{nightshift}} **Settings** page, select **Disconnect channel** next to the channel. `@Elastic` stops answering there and replies to mentions with the "isn't connected yet" message. Automations that post to the channel stop posting. `@Elastic` stays in the channel until someone removes it in Slack.

**Disconnect the workspace**
:   In **Slack channels**, open the {icon}`boxes_vertical` menu and select **Disconnect workspace**. Every channel connected to this project stops answering. Other Elastic projects connected to the same workspace aren't affected. When the last project disconnects, the relay revokes the bot token and deletes its record of the installation. The app stays installed in Slack until a Slack admin removes it.

**Remove the app from Slack**
:   When a Slack admin removes the app from the workspace, the relay deletes the installation and every channel connection, for every Elastic project connected to the workspace.

:::{image} ../../images/nightshift-slack-workspace-menu.png
:alt: The Slack workspace actions menu in Nightshift Settings, with Disconnect workspace
:screenshot:
:::

Disconnecting doesn't delete conversations or investigations from your project, or the messages that `@Elastic` already posted in Slack.

## Slack permissions [nightshift-slack-app-scopes]

Slack shows these permissions when you install the app. The following table lists each one and what `@Elastic` uses it for. Slack sends `@Elastic` channel messages only from channels that it has been invited to, and `@Elastic` passes their content to a project only when the channel is connected to that project. In a channel that isn't connected, `@Elastic` answers a mention only with a notice that the channel isn't connected yet.

| Permission | Required | What `@Elastic` uses it for |
| --- | --- | --- |
| `app_mentions:read` | Yes | Receive messages that mention `@Elastic`. |
| `assistant:write` | Yes | Show its progress in the thread while it works on an answer. |
| `channels:history` | Yes | Read the thread that a mention is in, receive messages in connected public channels for automations, and let investigations read recent messages in a connected public channel. |
| `channels:read` | Yes | List the public channels it has been invited to, so admins can pick one in {{kib}}, and check that it's a member before an admin connects a channel. |
| `chat:write` | Yes | Post and update answers, notices, and investigation results in threads. |
| `im:history` | Yes | Receive direct messages, only so that it can reply that they aren't supported. |
| `reactions:write` | Yes | Add a `:warning:` reaction when your project refuses a message or can't be reached. |
| `users:read` | Yes | Show people's display names instead of Slack user IDs. It doesn't read email addresses. |
| `groups:history` | No | In private channels that it's invited to, read the thread that a mention is in. |
| `groups:read` | No | Check that it's a member of a private channel before an admin connects it. |

The app subscribes to these Slack events: `app_mention`, `message.channels`, `message.groups`, `message.im`, `member_joined_channel`, `app_home_opened`, and `app_uninstalled`. Slack sends `message.groups` only when private channel access is allowed, and the relay drops private channel messages that don't mention `@Elastic`.

## Learn more [nightshift-slack-app-next]

- [Set up Slack](./investigation/set-up.md#nightshift-set-up-slack): Connect the workspace and your channels.
- [Investigate in Slack](./use-cases/investigate-in-slack.md): Ask `@Elastic` for help and follow up in a thread.
- [Investigate alerts from your other tools](./use-cases/external-alerts.md): Start investigations from alerts that other apps post in Slack.
- [Grant access](./privileges.md): Find out which privileges {{nightshift}} runs with.
- [Your data and {{nightshift}}](./cost-and-models.md#nightshift-data): Find out what {{nightshift}} sends to models and stores.
