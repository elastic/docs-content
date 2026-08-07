---
applies_to:
  stack: experimental 9.5
  serverless: experimental
description: Nightshift provides automated on-call assistance and alert triage for Elastic Observability.
products:
  - id: observability
  - id: cloud-serverless
---

# Nightshift

Nightshift is an AI-powered observability feature built into Elastic. It monitors your systems, discovers Significant Events, investigates likely causes, and helps your team remediate incidents.

Nightshift works by:

1. **Extracting Knowledge Indicators (KIs)**: Nightshift reads your stream data and extracts stable facts: what services are running, what infrastructure is in use, what technologies are present, and how they relate to each other. Refer to [Knowledge Indicators](../streams/significant-events/knowledge-indicators.md).
2. **Generating and running detection rules**: Based on KIs, Nightshift generates ES|QL detection rules and runs them continuously. When rule firing patterns change, it detects the change. See [How Significant Events works](../streams/significant-events/how-it-works.md).
3. **Surfacing Significant Events**: When detections correlate into something meaningful, Nightshift promotes a Significant Event with a concise summary of what's happening, with severity, evidence, and suggested next steps.
4. **Investigating automatically**: For `critical` and `high` severity Significant Events, Nightshift triggers an automatic [investigation](./investigations.md) where it reads your system memory, runs targeted queries, and produces a root cause hypothesis with remediation options.
5. **Learning over time**: The [memory](./memory.md) system captures knowledge from each incident so future investigations are faster and more precise.

## Requirements [nightshift-requirements]

- **Enterprise license**: Nightshift requires an active Elastic Enterprise license or trial on {{serverless-full}}.
- **Streams**: Your data must be organized in [Streams](/solutions/observability/streams/streams.md). Nightshift attaches to streams and runs the KI extraction and detection pipeline per stream.
- **Generative AI connector**: A [Generative AI connector](kibana://reference/connectors-kibana/gen-ai-connectors.md) is required to run KI extraction, rule generation, and investigations.

## Nightshift UI [nightshift-landing-page]

The Nightshift UI is your central hub for active Significant Events. It shows `critical` and `high` severity Significant Events detected across your streams, [investigations](./investigations.md) that are running and resolved, and what needs your attention.

### Access the Nightshift UI [nightshift-landing-page-access]

From your {{observability}} project, select **Streams** → **Significant Events** → **Nightshift** to open the Nightshift UI. If you don't see any Significant Events, Nightshift might still be running its initial KI extraction and rule generation. If your streams have sufficient data, Significant Events surface automatically.

### Significant Events list [nightshift-events-list]

Nightshift is divided into the following:

- **Needs action** and **Resolved** panels: These panels show the count of events that need action and resolved events. Select the panel to go to the list of active or resolved significant events.
- **Blast radius**: This panel shows the most affected services. Select a service to filter Significant Events related to it.

### View all events [nightshift-events-view-all]

Click **View all Significant Events** to open the full list of Significant Events. Here you can review Significant Events with severity ratings below `critical` and `high` and investigate them.

### Significant Event flyout [nightshift-event-detail]

Click any event in the **Needs action** or **Resolved** list to open the event flyout.

The top of the flyout shows the event title, triage status (**Needs action** or **Resolved**), investigation status (**Investigating** or **Investigated**), timestamp, and a plain-language summary of what Nightshift detected.

#### Detections [nightshift-event-detail-detections]

**Detections** lists the individual signals that contributed to this Significant Event. Each detection shows the rule that fired, the change point type (for example, spike or distribution change), the stream it came from, and the detection pattern. Select any detection to open more details.

#### Investigations [nightshift-event-detail-investigations]

**Investigations** shows the investigation Nightshift ran for this event.

For more on what investigations produce and how they work, see [Investigations](./investigations.md).

## Chat with an AI Agent about a Significant Event [nightshift-chat]

Every Significant Event has an **Open in chat** button. Select it to open a conversation with the AI Agent. You can:

- Ask for more detail about what happened and why.
- Request remediation options.
- Ask about affected services or dependencies.
- Explore hypotheses the investigation didn't fully cover.

The AI Agent has access to the event's detections, associated KIs, and [memory](./memory.md) pages about your system.

## Give feedback [nightshift-feedback]

Use the **Submit feedback** {icon}`comment` button at the top of the page to share your experience. Your feedback goes directly to the team.

## Learn more [nightshift-landing-page-nav]

- [Investigations](./investigations.md): Learn how Nightshift investigates Significant Events and produces root cause hypotheses
- [Memory](./memory.md): Learn how Nightshift stores and uses system knowledge to improve investigation quality over time
- [How Significant Events works](../streams/significant-events/how-it-works.md): Pipeline internals for KI extraction, rule generation, detection, and discovery
- [Knowledge Indicators](../streams/significant-events/knowledge-indicators.md): Get an in-depth overview of how KIs work
- [Operator guide](../streams/significant-events/operator-guide.md): Learn more about system impact, cost drivers, and operational procedures
