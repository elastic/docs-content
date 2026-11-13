---
navigation_title: Known issues
applies_to:
  serverless:
    observability: preview
description: Check the known issues and Tech Preview limitations of Elastic nightshift, and how to work around them.
products:
  - id: observability
  - id: cloud-serverless
---

# Known issues and Tech Preview limitations [nightshift-known-issues]

{{nightshift}} is in Tech Preview. This page lists what doesn't work yet, what can go wrong, and how to work around it. Check it when something behaves differently than you expect.

## Availability [nightshift-known-issues-availability]

**{{serverless-full}} only**
:   {{nightshift}} runs only in {{obs-serverless}} projects on the Complete tier. It isn't available on {{ech}} or self-managed deployments.

    **Workaround:** Investigations can query those clusters through an External {{es}} connector; detection can't. Refer to [Reference architecture](./reference-architecture.md).

**Default space only**
:   {{nightshift}} works only in the default space. In any other space, it shows **Nightshift only works in the default space for now**, with a button to open the default space.

    **Workaround:** Use {{nightshift}} in the default space. Its investigations can still query data that the connectors reach.

**No private connectivity to external clusters**
:   An External {{es}} connector reaches a cluster only over the public internet. Mutual TLS (mTLS) and private connectivity, such as AWS PrivateLink, aren't supported.

    **Workaround:** Expose a secured endpoint, or send the data to a {{serverless-short}} project. Refer to [Self-managed cluster](./reference-architecture.md#nightshift-reference-architecture-self-managed).

**One {{nightshift}} agent**
:   You can't create your own investigation agents or change the agent's instructions.

    **Workaround:** Guide it with custom context and automation instructions. Refer to [Give {{nightshift}} context](./context/index.md#nightshift-context-give).

## Data and detection [nightshift-known-issues-detection]

**Detection learns from logs only**
:   Detection learns from and watches logs. Sources that query metrics or traces, such as {{esql}} `TS` queries, aren't supported yet.

    **Workaround:** Investigations can still query metrics and traces through your connectors.

**Detection needs time to warm up**
:   After you turn on detection, the first Knowledge Indicators and rules appear within a few minutes. Expect the first signals 40 to 100 minutes after you turn it on. Early on, it can have few rules, or rules with no matches.

    **Workaround:** Wait, and check progress on the **Detections** page. Refer to [How long learning takes](./detection/learning.md#nightshift-detection-learning-warmup).

**Stats queries don't become rules**
:   Only match queries become detection rules. Stats query KIs stay on the **Knowledge Indicators** tab.

    **Workaround:** Investigations can still run stats queries. Refer to [Where rules come from](./detection/rules-and-signals.md#nightshift-detection-rules-origins).

**Significant event severity can run high**
:   Significant events can have a higher severity than the problem deserves.

    **Workaround:** Check the event's confidence and signals before you act on its severity. Refer to [Review significant events](./detection/significant-events.md#nightshift-detection-events-severity).

## Investigations [nightshift-known-issues-investigations]

**A conclusion can be wrong, and still sound sure**
:   An investigation can reach a wrong conclusion and state it with confidence. It can also conclude that data doesn't exist when it's stored in an index it didn't check, for example "no {{k8s}} metrics found".

    **Workaround:** Check the hypothesis tree and evidence, and tell {{nightshift}} where your data lives in [custom context](./context/index.md#nightshift-context-custom). Refer to [Check the evidence before you act](./investigation/index.md#nightshift-investigations-accuracy).

**Investigations focus on recent data**
:   An investigation looks at the most recent data first. If you investigate an older alert, it can report that the problem isn't happening anymore.

    **Workaround:** Give the time range in your question, for example "Why was checkout slow between 19:50 and 20:30 UTC on 2026-11-10?".

**An investigation can stay in progress**
:   Sometimes an investigation shows **Investigating** for much longer than usual. Most investigations finish within five minutes. An investigation stops after 60 minutes at most.

    **Workaround:** Wait for the 60-minute timeout, or start the investigation again.

**Only Agent Builder admins can delete investigations**
:   Only Agent Builder admins can delete an investigation, from its {icon}`boxes_vertical` menu on the home page. Nobody can archive an investigation.

    **Workaround:** Close investigations when the problem is handled, so the home page shows which ones are still open. To remove everything learned after a point in time, including investigations, use **Purge knowledge** in [developer mode](./settings.md#nightshift-settings-developer-mode).

**GitHub OAuth doesn't work for investigations**
:   Investigations run as a service account, which can't use the personal credentials that GitHub OAuth stores for each user.

    **Workaround:** Connect GitHub with a fine-grained personal access token. Refer to [Get started](./get-started/investigations.md#nightshift-get-started-other-sources).

**Four connector types**
:   Investigations can use Local and External {{es}}, GitHub, and HTTP connectors. Slack connects your team, not data.

    **Workaround:** Reach any other tool with an HTTP API through an HTTP connector, and describe the API in custom context. Refer to [Connect any system with an HTTP API](./investigation/extend.md#nightshift-extend-http).

**Connectors on ports other than 443 fail**
:   A connector whose URL has a port other than 443, such as the `:9243` port in some {{ecloud}} endpoints, passes its test but fails in investigations with a `502` error.

    **Workaround:** Use an endpoint on port 443. For an {{ecloud}} endpoint, remove the port from the URL.

**Anyone with connector access can run your connectors**
:   Any user who can use connectors in {{kib}} can run the connectors that {{nightshift}} uses, with their stored credentials. HTTP connectors can't be restricted.

    **Workaround:** Give every connector read-only credentials, such as a read-only {{es}} API key and a read-only GitHub token. Refer to [How investigations use connections](./investigation/set-up.md#nightshift-set-up-how).

## Automations and Slack [nightshift-known-issues-slack]

**No Microsoft Teams**
:   {{nightshift}} works in Slack only. You can't ask it for help or post automation results in Microsoft Teams.

    **Workaround:** Use {{nightshift}} in {{kib}}, or connect a Slack workspace. Refer to [Slack](./investigation/set-up.md#nightshift-set-up-slack).

**Public Slack channels only**
:   `@Elastic` works only in public channels. It doesn't work in private channels, direct messages, or Slack Connect channels, even though the authorization screen offers private-channel access. {{nightshift}} doesn't join channels on its own.

    **Workaround:** Use a public channel, and connect it on **Settings** → **General**. Refer to [Connect your data and tools](./investigation/set-up.md#nightshift-set-up-slack).

**Slack is the only destination**
:   An automation can post results only to a Slack channel, with **Post in Slack**. It can't send direct messages or email, or create tickets.

    **Workaround:** To route significant events elsewhere, use an action policy. Refer to [Route significant events](./detection/significant-events.md#nightshift-detection-events-route).

**Investigations started in Slack are read-only in {{kib}}**
:   When an investigation starts from Slack, its chat in {{kib}} is read-only. You also can't close an investigation from Slack.

    **Workaround:** Ask follow-up questions in the Slack thread. Close the investigation in {{kib}}.

**Each new alert starts its own investigation**
:   An alert or significant event that's already part of an open investigation joins it. A new alert from the same rule starts its own investigation, and automations can't group repeat firings into one. A flapping alert can use up your daily limit quickly.

    **Workaround:** Set a **Daily trigger limit** on the automation. Refer to [One problem, one investigation](./investigation/index.md#nightshift-investigations-dedup) and [Daily trigger limit](./investigation/automations.md#nightshift-automations-daily-limit).

**Schedules use presets**
:   Scheduled automations run hourly, daily, or weekly. Custom cron schedules aren't supported.

    **Workaround:** For an hourly schedule, select **between hours** to limit it to working hours. Refer to [Automations](./investigation/automations.md#nightshift-automations-trigger-schedule).

**Edit the automation, not its workflow**
:   {{nightshift}} creates a workflow for each automation, with the same name, and it appears on the **Workflows** page. If you edit that workflow directly, the automation can stop working.

    **Workaround:** Make your changes in the automation. Saving it rewrites the workflow.

## Limits and cost [nightshift-known-issues-limits]

**Limits count runs, not money**
:   Run limits count investigations and detection runs, not cost. There's no dollar budget.

    **Workaround:** Lower the limits to match your budget, using the typical costs. Refer to [Cost and models](./cost-and-models.md#nightshift-cost-control).

**No bring-your-own model**
:   Elastic picks the models that {{nightshift}} uses, and runs them through EIS. You can't connect your own LLM, and there's no air-gapped option.

    **Workaround:** None in Tech Preview. Refer to [Models](./cost-and-models.md#nightshift-models).

**No token cap for one investigation**
:   You can't limit the tokens that one investigation uses. Token use for each investigation shows only in its Agent Builder conversation, not in {{nightshift}}.

    **Workaround:** Use the daily run limits and each automation's **Daily trigger limit** to cap how many investigations start. Check the cost estimate in [Monitor your cost](./cost-and-models.md#nightshift-cost-monitor).

**Limits apply to the whole deployment**
:   Run limits are shared by every space in the deployment. You can't set a limit for one space.

    **Workaround:** Set the limits for the deployment as a whole.

**Run history doesn't say which limit was reached**
:   When a limit stops an automation's run, its **Run history** shows a reason such as "Deployment-wide investigation limit reached", but not which of the three investigation limits it was.

    **Workaround:** On **Settings** → **Investigations**, compare each limit with the count of investigations that started today. Refer to [Run limits](./settings.md#nightshift-settings-run-limits).

**Follow-ups aren't limited**
:   Follow-up questions on open investigations are never blocked by a limit, so they add cost even when a limit is reached.

    **Workaround:** Close investigations when the problem is handled. Alerts never join a closed investigation.

**The in-product cost estimate is approximate**
:   The cost estimate is under **Advanced developer settings** on **Settings** → **Detections**, available only in developer mode. It leaves out some calls, and counts only calls made while token tracking is on.

    **Workaround:** Use the {{ecloud}} billing page for exact numbers. Refer to [Monitor your cost](./cost-and-models.md#nightshift-cost-monitor).

## User interface [nightshift-known-issues-ui]

**You can't edit the Wiki or Memory**
:   {{nightshift}} manages the Wiki and Memory itself. You can archive entries, but not edit them or add your own.

    **Workaround:** Archive wrong entries, and add what's right as custom context. Refer to [Correct what {{nightshift}} learned](./context/index.md#nightshift-context-correct).

## Give feedback [nightshift-known-issues-feedback]

Found a problem that isn't on this page? On the {{nightshift}} home page, open the {icon}`boxes_vertical` menu and select **Feedback**.

## Learn more [nightshift-known-issues-next]

- [Settings and limits](./settings.md): Change the limits and settings mentioned on this page.
- [Cost and models](./cost-and-models.md): Find out what {{nightshift}} costs, and what happens to your data.
- [How investigations work](./investigation/index.md): Learn how to check an investigation's reasoning.
