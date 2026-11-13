---
navigation_title: Cost and models
applies_to:
  serverless:
    observability: preview
description: Find out what Elastic nightshift costs, what drives the cost, how to keep it predictable, which models it uses, and what happens to your data.
products:
  - id: observability
  - id: cloud-serverless
---

# Cost and models [nightshift-cost]

{{nightshift}} is billed by the AI model tokens it uses. In Elastic's testing, a typical investigation costs about $1.50, and detection costs a few dollars per day. Daily run limits keep the total predictable, and you can lower them at any time.

This page also explains which models {{nightshift}} uses, and what happens to your data.

## What you're billed for [nightshift-cost-billed]

{{nightshift}} sends its model calls through the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md). EIS bills per million tokens, for both input and output. Tokens are the units that a model reads and writes: your question, the data that {{nightshift}} queries, its reasoning, and its answer all count.

The token cost appears on your {{obs-serverless}} bill. For rates, refer to [EIS pricing](/explore-analyze/elastic-inference/eis.md#pricing) and [{{obs-serverless}} billing dimensions](/deploy-manage/cloud-organization/billing/elastic-observability-billing-dimensions.md#observability-billing-elastic-managed-llms).

Workflow executions that {{nightshift}} runs aren't billed separately. You pay only for the tokens.

## Typical cost [nightshift-cost-typical]

These figures come from Elastic's testing. Your cost depends on your data and how you use {{nightshift}}.

| Activity | Typical cost |
| --- | --- |
| One investigation | About $1.50 |
| Detection | A few dollars per day |
| A follow-up question in chat | Usually a few cents, depending on the model you pick in chat |

For example, with the default run limits, at most 10 investigations start each day. At the typical cost, that's about $15 per day for investigations, plus detection.

Your cost goes up with data volume, the number of detection sources, follow-ups, and investigation length: an investigation that tests many hypotheses or reads a lot of code uses more tokens than one that finds the cause quickly.

Context works the other way: because investigations start from what {{nightshift}} already learned about your system, they spend fewer tokens on finding indices, services, and dependencies again. Refer to [How {{nightshift}} builds context](./context/index.md).

## What uses tokens [nightshift-cost-drivers]

| Activity | When it runs | How to limit it |
| --- | --- | --- |
| Investigations that you start | When you select **Investigate** on the home page, an alert, or a significant event, or mention `@Elastic` in Slack | **Manual investigations daily limit** |
| Investigations that automations start | When an automation's trigger fires | **Automatic investigations daily limit**, and each automation's **Daily trigger limit** |
| Follow-up questions | When you ask in chat or in the Slack thread | Not limited |
| Knowledge Indicator extraction | When you add a source, generate KIs, or continuous KI onboarding runs | **Knowledge indicators extraction daily limit**, fewer sources, longer onboarding interval |
| Detection discovery | On the detection schedule | **Discovery daily limit**, fewer or narrower sources |

For the cost profile of each detection phase, refer to [Cost drivers](./significant-events/operator-guide.md#sig-events-op-costs) in the operator guide.

## Keep your cost under control [nightshift-cost-control]

Start with the defaults, then use the controls in the previous table: [Run limits](./settings.md#nightshift-settings-run-limits), [Detection run limits](./settings.md#nightshift-settings-detection-limits), [sources](./detection/sources.md), and [Continuous KI onboarding](./settings.md#nightshift-settings-ki-onboarding). Also:

- **Turn off a noisy automation**, or lower its **Daily trigger limit**. Refer to [Automations](./investigation/automations.md).
- **Pause detection.** Stops all detection cost in the space until you resume it. Refer to [Pause or resume detection](./settings.md#nightshift-settings-pause).

## Monitor your cost [nightshift-cost-monitor]

Your bill is the source of truth. To check your token use, go to [**Billing** → **Usage**](https://cloud.elastic.co/billing/usage) in the {{ecloud}} console and look for line items with the **Inference** billing dimension. Refer to [Monitor your token usage](/explore-analyze/elastic-inference/eis.md#monitor-your-token-usage).

{{nightshift}} can also show an estimate of its own cost. To turn it on, you need permission to save Advanced Settings.

1. On the {{nightshift}} home page, open the {icon}`boxes_vertical` menu and select **Settings**.
1. On the **General** tab, turn on **Enable nightshift developer mode**. Refer to [Developer mode](./settings.md#nightshift-settings-developer-mode).
1. Select the **Detections** tab, and scroll to **Advanced developer settings**.
1. In **Approximate inference cost across all spaces**, turn on **Enable token tracking in this space**.
1. Select **Save changes**.

The estimate shows the cost for **Today** and **This month**, split into **Discovery**, **Investigation**, and **KI extraction**. Select **Refresh** to update it. It counts only calls made while tracking is on, so right after you turn it on, it shows **No recorded calls**.

The estimate covers all spaces in the deployment, and it's approximate. It uses EIS list prices, and leaves out embedding and reranking calls, cache-write tokens, and calls that fail before their tokens are recorded. Turning tracking on or off doesn't change what you pay.

## Models [nightshift-models]

Elastic picks the models that {{nightshift}} uses, and runs them through EIS. You don't need to set up an LLM connector, and you can't change the models that investigations and scheduled detection use. Elastic picks a model for each step, and can change these models over time.

The model picker in the Agent Builder chat applies only to your follow-up questions in that chat. It doesn't change investigations.

Elastic plans to offer on-premises deployment options for {{nightshift}} in 2027, which may include a choice of model. This is a plan, not a commitment, and it can change.

EIS routes each request to the nearest region where it runs. To keep requests in certain regions, refer to [Region and hosting](/explore-analyze/elastic-inference/eis-region-and-hosting.md).

## Your data and {{nightshift}} [nightshift-data]

This section explains what {{nightshift}} reads, what it sends to models, and what it keeps. For how Elastic handles data in its AI features, refer to the [data and AI FAQ](https://www.elastic.co/trust/faq#data-ai) in the Elastic Trust Center.

**Where it runs**
:   Your data stays in your {{obs-serverless}} project, except the excerpts that {{nightshift}} sends to models. Models run only through EIS: you can't bring your own model, and there's no air-gapped option.

**What it reads**
:   Investigations reach your data and code through the connectors in the space, with the credentials stored in each connector. Detection reads the data that your detection sources select. Refer to [Privileges that {{nightshift}} runs with](./get-started/privileges.md#nightshift-privileges-accounts).

**What it sends to models**
:   To investigate, {{nightshift}} sends your question or alert, the results of its queries, excerpts of logs, metrics, and traces, code it reads, and Slack messages in the thread to a model through EIS. Detection sends samples of the logs in your sources.

**Model providers**
:   Depending on the model, EIS processes requests on Elastic infrastructure or with trusted third-party model providers. Refer to [Supported models](/explore-analyze/elastic-inference/eis-supported-models.md).

**What it stores**
:   Investigations, the Wiki, Memory, decision trees, Knowledge Indicators, rules, and significant events are stored in your project, in the space where {{nightshift}} runs. Results that automations post to Slack are also stored in Slack.

**Your code**
:   When an investigation needs code, it clones the repository into a temporary sandbox, searches it, and discards it when the investigation ends. {{nightshift}} doesn't copy, sync, or index your repositories. The sandbox can only reach the hosts of your connectors and the hosts on the [sandbox egress allowlist](./settings.md#nightshift-settings-egress).

**Who can read it**
:   Everyone with the **Read** privilege for {{nightshift}} in the space can read its investigations, Wiki, and Memory. Everyone in a connected Slack channel can ask `@Elastic` and read its answers. Those answers come from what the service account and connectors can reach, not from the permissions of the person who asks.

**Changes to your environment**
:   {{nightshift}} reads and proposes. It doesn't change your systems: a person decides whether to apply each proposed action, and applies it.

**Deleting data**
:   An Agent Builder admin can delete an investigation from its {icon}`boxes_vertical` menu on the home page. Investigations can't be archived. Delete a memory on the **Memory** tab. Wiki pages can be archived, not deleted. In [developer mode](./settings.md#nightshift-settings-developer-mode), you can purge everything that {{nightshift}} learned after a point in time. Snapshots can still hold deleted documents.

## Learn more [nightshift-cost-next]

- [Settings and limits](./settings.md): Change the limits that keep your cost predictable.
- [Investigation limits](./investigation/limits.md): Find out what happens when a limit is reached.
- [Known issues](./known-issues.md): Check the Tech Preview limits on cost controls.