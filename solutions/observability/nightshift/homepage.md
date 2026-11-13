---
navigation_title: Home page
applies_to:
  serverless:
    observability: preview
description: The Elastic nightshift home page is your inbox for investigations, sorted by severity, so you know what to look at first.
products:
  - id: observability
  - id: cloud-serverless
---

# The home page [nightshift-homepage]

The home page is your inbox for investigations. Every investigation lands here, whether you started it, a teammate asked in Slack, or an automation started when an alert fired. {{nightshift}} sorts investigations by severity, so you can work from the most urgent problem down to the lowest severity.

Select **Nightshift** in the navigation menu to open the home page.

:::{image} ../../images/nightshift-home.png
:alt: The Elastic nightshift home page with tiles that count Critical, High, Medium, and Low investigations, and a list of investigations grouped under High
:screenshot:
:::

## An inbox sorted by severity [nightshift-homepage-inbox]

When an investigation finishes, {{nightshift}} rates how serious the problem is and files the investigation under **Critical**, **High**, **Medium**, or **Low**. Investigations that are still running wait in **In progress**.

- **Tiles**: Tiles show the count of investigations at each severity level. Select a tile to jump to that group.
- **Investigation cards**: Each card is one investigation.  The card includes a one-line summary, the services it affects, and who's assigned to it.
- **Search**: Use the search to narrow the list of investigations, for example, to one service.

Work through it like an inbox: open the most severe investigation, read what {{nightshift}} found, decide what to do, and then assign it or close it. If you disagree with a severity, change it in the investigation.

## Work with an investigation [nightshift-homepage-work]

Select an investigation card to open the investigation information. From here, you can:

- Read what happened, the impact, the likely cause, and the proposed actions.
- Assign teammates and change the status or severity.
- Select **Open chat** to ask follow-up questions.

To read the results in detail and check the reasoning, refer to [How investigations work](./investigation/index.md).

## Navigate through {{nightshift}} [nightshift-homepage-header]

The home page header takes you everywhere else:

| Action | Description |
| --- | --- |
| **Investigate** | Start an investigation by describing a problem. Refer to [Investigate anything](./use-cases/investigate-anything.md). |
| **Automations** | Have investigations start by themselves. Refer to [Automations](./investigation/automations.md). |
| **Detections** | Review the problems that detection found. Refer to [How detection works](./detection/index.md). |
| {icon}`boxes_vertical` → **Knowledge** | See what {{nightshift}} learned about your system. Refer to [How {{nightshift}} builds context](./context/index.md). |
| {icon}`boxes_vertical` → **Settings** | Manage connectors, Slack, and limits. Refer to [Settings and limits](./settings.md). |

If {{nightshift}} isn't set up, the home page shows the **Get started** checklist. Refer to [Get started](./get-started.md).

## Next steps [nightshift-homepage-next]

- [Investigate anything](./use-cases/investigate-anything.md): Start your first investigation from the home page
- [Automatically investigate your alerts](./use-cases/auto-investigate-alerts.md): Fill your inbox without starting each investigation yourself
- [How investigations work](./investigation/index.md): Read an investigation and check its reasoning
