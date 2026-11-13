---
navigation_title: Get started
applies_to:
  serverless:
    observability: preview
description: Get started with Elastic nightshift. Set up investigations first, then turn on detection when you're ready.
products:
  - id: observability
  - id: cloud-serverless
---

# Get started with {{nightshift}} [nightshift-get-started]

Set up {{nightshift}} in two parts. Start with investigations, point it at an alert, or describe a problem in your own words, and it finds the likely cause in your data. Then turn on detection, so it also finds problems that none of your alerts catch.

- [Set up investigations](./get-started/investigations.md): Follow this guide to enable {{nightshift}}, connect your data and code, run a first investigation, and set up a first automation .
- [Set up detection](./get-started/detection.md): Follow this guide to let {{nightshift}} watch your logs and group unusual changes and incidents into significant events.

## Before you begin [nightshift-get-started-requirements]

Make sure you meet the following requirements:

- **An {{obs-serverless}} project on the Complete tier.** In Tech Preview, {{nightshift}} runs only in the default space. To check what works with your deployment, refer to [Reference architecture](./reference-architecture.md).
- **Data to work with.** Logs, metrics, or traces in your project, or in another cluster that you can reach with an API key.
- **An admin to enable {{nightshift}}.** The predefined **Admin** role can do this. For other roles, refer to [Grant access to {{nightshift}}](./get-started/privileges.md).

You don't need an LLM connector. {{nightshift}} uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md). To open {{nightshift}}, select **Nightshift** in the navigation menu, or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).