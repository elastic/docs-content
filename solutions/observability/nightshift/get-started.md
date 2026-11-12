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

{{nightshift}} has two parts that you set up separately. Start with investigations: in a few steps, {{nightshift}} investigates a real problem in your data. Turn on detection when you're ready, so it also finds problems that none of your alerts catch.

| Guide | What you get | Time |
| --- | --- | --- |
| [Set up investigations](./get-started/investigations.md) | {{nightshift}} enabled, your data and code connected, a first investigation, and a first automation | About 15 minutes |
| [Set up detection](./get-started/detection.md) | {{nightshift}} watching your logs and grouping unusual changes into significant events | 5 minutes. First KIs and rules within minutes, first signals after 40 to 100 minutes |

## Before you begin [nightshift-get-started-requirements]

- **An {{obs-serverless}} project on the Complete tier.** In Tech Preview, {{nightshift}} runs only in the default space. To check what works with your deployment, refer to [Reference architecture](./reference-architecture.md).
- **Data to work with.** Logs, metrics, or traces in your project, or in another cluster that you can reach with an API key.
- **An admin for the first step.** An admin enables {{nightshift}} once for the space. The predefined **Admin** role can do this. For other roles, refer to [Grant access to {{nightshift}}](./get-started/privileges.md).

You don't need an LLM connector: {{nightshift}} uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md). To open {{nightshift}}, select **Nightshift** in the navigation menu, or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

## Next steps [nightshift-get-started-next-steps]

- [Set up investigations](./get-started/investigations.md): Start here
- [Set up detection](./get-started/detection.md): Find problems that no alert covers
- [What you can do with {{nightshift}}](./use-cases/index.md): Explore the use cases
