---
navigation_title: FAQ
applies_to:
  serverless:
    observability: preview
description: Get short answers to the questions people ask most about Elastic nightshift, from deployment support and data use to accuracy, detection, connectors, and cost.
products:
  - id: observability
  - id: cloud-serverless
---

# Frequently asked questions [nightshift-faq]

Short answers to the questions that teams ask most before and after they turn on {{nightshift}}. Each answer links to the page with the details.

## Availability and setup [nightshift-faq-setup]

What you need before you start, and where {{nightshift}} runs.

### Does {{nightshift}} work with {{ech}} or self-managed clusters? [nightshift-faq-deployments]

{{nightshift}} runs only in an {{obs-serverless}} project, but you don't need to move your data into it. Investigations can query an {{ech}} deployment, or a self-managed cluster with a public, secured endpoint, through an External {{es}} connector, and other tools through HTTP connectors. Detection watches only data in the {{nightshift}} project and in projects linked through {{cps}}. Refer to [What works where](./reference-architecture.md#nightshift-reference-architecture-matrix).

### Do I need runbooks or alert rules to start? [nightshift-faq-runbooks]

No. Telemetry in your project is enough for your first investigation. Runbooks, repositories, and custom context improve results, and you can add them later. Refer to [Get started](./get-started.md).

### Can I use {{nightshift}} in Microsoft Teams? [nightshift-faq-teams]

No. In Tech Preview, {{nightshift}} works in {{kib}} and in public Slack channels, through `@Elastic`. Refer to [Slack](./investigation/set-up.md#nightshift-set-up-slack).

## Data, privacy, and models [nightshift-faq-data]

Where your data goes and which models process it. The full answer is in one place: [Your data and {{nightshift}}](./cost-and-models.md#nightshift-data).

### Does my data leave my project? [nightshift-faq-data-use]

What {{nightshift}} stores stays in your project, in the space where it runs. To investigate, it sends excerpts of your data to models through the Elastic {{infer-cap}} Service (EIS). Refer to [Your data and {{nightshift}}](./cost-and-models.md#nightshift-data) and the [data and AI FAQ](https://www.elastic.co/trust/faq#data-ai) in the Elastic Trust Center.

### Can I choose the model, or bring my own? [nightshift-faq-models]

No. Elastic picks the models and runs them through EIS. Refer to [No bring-your-own model](./known-issues.md#nightshift-known-issues-limits) and [Models](./cost-and-models.md#nightshift-models).

## Accuracy and control [nightshift-faq-control]

How far you can trust a conclusion, and what {{nightshift}} can and can't do in your environment.

### Does {{nightshift}} change my systems? [nightshift-faq-changes]

It doesn't apply changes. It proposes actions, and a person decides whether to apply each one. It can only reach what your connectors' credentials allow, so give every connector read-only credentials. Refer to [How investigations use connections](./investigation/set-up.md#nightshift-set-up-how). To add an approval step before a change runs, use a workflow. Refer to [Workflows](./investigation/extend.md#nightshift-extend-workflows).

### Is there an accuracy rate? [nightshift-faq-accuracy]

No. Elastic doesn't publish an accuracy rate for {{nightshift}}. Each conclusion comes with its hypotheses and evidence, so you can check it before you act. Refer to [Check the evidence before you act](./investigation/index.md#nightshift-investigations-accuracy).

### What about prompt injection through logs or alerts? [nightshift-faq-prompt-injection]

{{nightshift}} reads text from your logs, alerts, and other connected tools, and that text can try to steer it. Proposed actions are never applied automatically, the sandbox reaches only your connectors' hosts and the hosts you allow, and read-only connector credentials limit what an investigation can do. If wrong knowledge got in, use **Purge knowledge** in developer mode to delete what {{nightshift}} learned after a point in time. Refer to [Developer mode](./settings.md#nightshift-settings-developer-mode).

### Can I delete an investigation? [nightshift-faq-delete]

Only Agent Builder admins can, from its {icon}`boxes_vertical` menu on the home page. Refer to [Known issues](./known-issues.md#nightshift-known-issues-investigations).

### How do I stop or pause {{nightshift}}? [nightshift-faq-stop]

Pause the detection engine, turn off your automations, and set the investigation run limits to the lowest value. In Tech Preview, you can't turn {{nightshift}} off completely. Refer to [Stop or pause {{nightshift}}](./settings.md#nightshift-settings-stop).

## Detection [nightshift-faq-detection]

What detection watches, and how it creates rules.

### Why does detection use only logs? [nightshift-faq-logs-only]

In Tech Preview, detection learns from logs only; investigations query logs, metrics, and traces. Refer to [What a source is](./detection/sources.md#nightshift-detection-sources-what).

### How do Knowledge Indicators become rules? [nightshift-faq-ki-rules]

Match query KIs with a high severity become rules automatically. To turn another query KI into a rule, promote it from **Knowledge** → **Knowledge Indicators**. Refer to [Where rules come from](./detection/rules-and-signals.md#nightshift-detection-rules-origins).

### Why are there no significant events yet? [nightshift-faq-no-events]

Detection needs time to learn. The first KIs and rules appear within a few minutes, and the first signals 40 to 100 minutes after you turn it on. After that, it raises significant events only when something changes. Refer to [How long learning takes](./detection/learning.md#nightshift-detection-learning-warmup).

## Connectors and context [nightshift-faq-connectors]

How {{nightshift}} reaches your tools, and how you tell it about your environment.

### Why doesn't {{nightshift}} use my connector? [nightshift-faq-connector-unused]

Investigations use only the connectors listed on **Settings** → **General**. Add connectors there with **Add connector**, which assigns them to {{nightshift}}. If the connector is listed, check that its URL uses port 443. Refer to [Connect your data and tools](./investigation/set-up.md#nightshift-set-up-prereqs).

### Can {{nightshift}} use tools other than Elastic and GitHub? [nightshift-faq-other-tools]

Yes, through an HTTP connector to the tool's API. Describe the API in custom context, so investigations know what it returns and when to call it. Refer to [Custom context](./investigation/extend.md#nightshift-extend-custom-context).

### Can I tell {{nightshift}} to remember something? [nightshift-faq-remember]

Not directly. In Tech Preview, you can't write to the Wiki or Memory. Add what it should always know as custom context. Refer to [Give {{nightshift}} context](./context/index.md#nightshift-context-give).

## Cost [nightshift-faq-cost]

What drives cost, and what limits it.

### What does {{nightshift}} cost? [nightshift-faq-cost-typical]

{{nightshift}} is billed by the model tokens it uses, for investigations and for detection. For typical figures from Elastic's testing, refer to [Typical cost](./cost-and-models.md#nightshift-cost-typical).

### What happens when a limit is reached? [nightshift-faq-limit-reached]

Investigations of that kind don't start until the limit resets at midnight UTC. Investigations that already started keep running, and follow-up questions still work. Refer to [What happens when a limit is reached](./investigation/limits.md#nightshift-limits-reached).

### Can I cap the tokens of one investigation? [nightshift-faq-token-cap]

No. Limits count investigations, not tokens. You can check the token use of an investigation in its Agent Builder conversation. Refer to [Known issues](./known-issues.md#nightshift-known-issues-limits).

## Learn more [nightshift-faq-next]

- [Known issues](./known-issues.md): Check the Tech Preview limitations and their workarounds.
- [Reference architecture](./reference-architecture.md): Check what works with your deployment.
- [Cost and models](./cost-and-models.md): Find out what {{nightshift}} costs and what happens to your data.
