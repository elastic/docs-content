---
navigation_title: Alerting concepts
applies_to:
  serverless: preview
  stack: unavailable
products:
  - id: kibana
  - id: cloud-serverless
description: "How Kibana alerting v2 fits together, detection and notification model, rule modes, and the main terms you’ll see in the product."
---

# Kibana alerting v2 concepts [kibana-alerting-v2-concepts]

Use this page to learn how an Kibana alerting v2 rule runs end to end, why detection and notification are separate layers, and what common terms are used to describe Kibana alerting v2 features. Read from top to bottom for the full picture, or jump to [Key terms](#key-terms) when you need a definition while authoring rules or sorting out unexpected behavior.

## How Kibana alerting v2 works

A Kibana alerting v2 rule defines what to look for in your data. It evaluates source data such as logs, metrics, traces, or alert events from other rules on a configurable schedule using an ES|QL query and produces alert event documents when conditions are met.

Each rule is set to **Detect** or **Alert** mode. Detect mode saves what the rule found each run. You can use it to try out a query without opening issues or sending notifications. Alert mode does that too, but also keeps an ongoing problem you can work in **Alerts**, which is what notification policies hook into.

Besides mode, a typical rule includes the following:

| Part | What it does |
|------|----------------|
| **Query** | An ES\|QL query that defines what to look at and what counts as a match. |
| **Schedule** | How often the rule runs and how far back each run looks. |
| **Grouping** (optional) | Fields that split results so each value (for example, each host) is tracked on its own. |
| **Notification policies and workflows** | In Alert mode, policies decide when an episode should notify someone; workflows are the concrete steps, such as sending email. |

These parts work together when a rule runs. Each run looks roughly like this:

1. The rule runs its query over the lookback window.
2. The system writes signals, one saved result per match. In Alert mode it also updates alert and episode information for each series (each grouped track you care about).
3. In Alert mode, the dispatcher decides whether a notification policy applies, whether throttling allows a send, and whether to run a workflow.
4. You work from the Alerts UI, Discover, or dashboards. You can add more rules later that build on the same data.

In Detect mode, step 3 does not apply because there are no episodes for policies to target.

## Detection and notification

Kibana alerting v2 follows a two-layer model: detection first, then notification. This model gives you room to change how you evaluate data and reach people without redoing both every time.

* **Detection**: The detection layer is driven by rules. On the schedule you specify, rules evaluate your data and record what matched (signals only in Detect mode, or full alert lifecycle in Alert mode). 
* **Notification** The notification layer is driven by notification policies and workflows. These might contact people or systems after the detection layer has produced something that can be used. 

## Key terms

Understanding these terms helps you pick the right rule settings, understand why something landed in Discover but not Alerts, why a notification did or did not fire, and similar cases. The definitions below move from raw findings through alerts, then how grouping forms series and episodes, then notification, to the dispatcher.

### Signals

A **signal** is a saved result when the query returned matching data. You can search, chart, or inspect signals. Think of them as a log of what the rule saw. In Detect mode, signals are the main output. Use them to validate behavior before you switch to Alert mode.

*Example:* A rule counts error responses in the last five minutes. In Detect mode, each run adds signals you can open in Discover, no alert inbox entry and no emails.

### Alerts

In Alert mode the system still writes signals, but it also maintains **alerts**, which are tracked items whose state can change over time (for example while a problem is active versus after it has calmed down). Those are what you open and triage in **Alerts**.

*Example:* The same error-count rule in Alert mode creates a tracked alert you can follow until errors stay below your threshold again.

### Series

A **series** is the bucket the rule uses for _one thing you are watching_ when you group by a field, for example one series per host or per service. Everything the rule records for that value stays in that bucket and stays separate from other values. If you do not group, the rule behaves as if there is a single series for the whole rule.

*Example:* You group by host name. `web-east` and `web-west` are two series. When the rule finds a problem on `web-east`, that history stays separate from `web-west`.

### Episodes

An **episode** belongs to exactly one **series**. It is one full incident for that series, from the first time the condition goes bad until it's no longer an issue. The rule runs on its schedule many times in between. The episode is what ties those runs into a single story you can treat as one unit.

*Example:* On `web-east`, errors cross your threshold on Monday, stay high through Tuesday, then drop on Wednesday—that entire stretch is one episode. If the same host crosses the threshold again later, that starts a new episode on the same series.

### Notification policies

A **notification policy** is separate from the rule. It describes when an episode should trigger notification, how often that may happen, and which workflow to use. One policy can apply to many rules.

*Example:* When an episode is active, notify at most once per hour.

### Workflows

A **workflow** is the set of actions a policy runs, for example, send email, open a ticket, post to chat, or a short sequence. The policy points at a workflow. The rule does not embed those steps.

*Example:* A workflow that sends one email to an on-call address.

### Dispatcher

The **dispatcher** connects detection output to policies and workflows. After episodes are updated, it applies policies, respects throttling, records outcomes, and starts workflows when appropriate.

*Example:* An episode becomes active, the dispatcher finds a matching policy, checks that a notification is allowed, and runs the email workflow.
