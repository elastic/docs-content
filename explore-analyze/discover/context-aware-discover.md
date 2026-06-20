---
navigation_title: Context-aware experiences
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover.html#context-aware-discover
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Discover provides specialized interfaces for logs, metrics, traces, and security data. Learn how context-aware experiences adapt to your data type and solution context.
---

# Context-aware experiences in Discover [context-aware-discover]

**Discover** adapts its interface and features based on your data type and solution context. When you explore logs, metrics, traces, or security data within {{observability}} or Security solutions, **Discover** provides specialized views and capabilities tailored to that specific type of data.

Context-aware experiences combine the right tools, visualizations, and workflows for your data type, making exploration more efficient and intuitive.

## Available context-aware experiences

**Discover** currently offers specialized experiences for the following data types:

* **{{observability}}:**
  * **[Logs exploration](/solutions/observability/logs/discover-logs.md)** - Tailored for exploring log data with log-specific features and UI elements.
  * **[Metrics exploration](/solutions/observability/infra-and-hosts/discover-metrics.md)** {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview` - Optimized for metrics data with metric-specific visualizations and analysis tools.
% LINK/PAGE TBD  * **Traces exploration** - Specialized interface for distributed tracing data.
% * **Security:**
% LINK/PAGE TBD  * **Security data exploration** - Enhanced features for security event analysis.

When you access **Discover** outside of a specific solution context, or when working with data types that don't have specialized experiences, you get the default **Discover** interface with all its core functionality for general-purpose data exploration.

## Working with multiple data types

Your query may include multiple data types that each have tailored experiences. For example, if you query both `logs-*` and `traces-*` indices within an {{observability}} context.

In this case, **Discover** provides the default experience until it detects that you're interacting with a single type of data. For example, when you [expand a document to view its details](discover-get-started.md#look-inside-a-document), **Discover** recognizes the data type and switches to the appropriate context-aware experience for that document.

## Check which experience is active

You can verify which experience is currently active for your current Discover session. This helps you confirm whether the type of data you're exploring is properly detected or if Discover is using its default experience.

1. Select **Inspect** from Discover's toolbar.
2. Open the **View** dropdown, then select **Profiles**.

The various profiles listed show details such as the active solution and data source contexts, which determine Discover's context-aware experiences.

## Benefits of context-aware experiences

Context-aware experiences provide several advantages:

* **Optimized UI**: Field layouts, visualizations, and controls are tailored to the data type.
* **Relevant features**: Only the features that make sense for your data type are surfaced.
* **Solution integration**: Quick access to related applications and workflows within your solution area.
* **Specialized queries**: Query suggestions and filters appropriate for the data type.

By adapting to your context, **Discover** reduces complexity and helps you work more efficiently with your specific type of data.

