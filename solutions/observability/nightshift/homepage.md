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

The home page is your inbox for investigations. Every investigation lands here, whether you started it, a teammate asked in Slack, or an automation started it when an alert fired. {{nightshift}} sorts them by severity, so you can work from the most urgent problem down.

To open it, select **Nightshift** in the navigation menu.

:::{image} ../../images/nightshift-home.png
:alt: The Elastic nightshift home page with tiles that count Critical, High, Medium, and Low investigations, and a list of investigations grouped under High
:screenshot:
:::

## An inbox sorted by severity [nightshift-homepage-inbox]

When an investigation finishes, {{nightshift}} rates how serious the problem is and files the investigation under **Critical**, **High**, **Medium**, or **Low**. Investigations that are still running wait in **In progress** at the top.

- **The tiles** at the top count the investigations at each severity. Select a tile to jump to that group.
- **Each card** is one investigation: what it's about, a one-line summary, the services it affects, and who's on it.
- **Search** narrows the list, for example to one service.

Work through it like an inbox: open the most severe investigation, read what {{nightshift}} found, decide what to do, and then assign it or close it. If you disagree with a severity, change it in the investigation.

## Work with an investigation [nightshift-homepage-work]

Select a card to open the investigation next to the list. There you can:

- Read what happened, the impact, the likely cause, and the proposed actions.
- Assign teammates, and change the status or severity.
- Select **Open chat** to ask follow-up questions.

:::{image} ../../images/nightshift-home-after-setup.png
:alt: The home page with one investigation open next to the list, showing its status, severity, what happened, and an impact chart
:screenshot:
:::

To read the results in detail and check the reasoning, refer to [How investigations work](./investigation/index.md).

## Go to the rest of {{nightshift}} [nightshift-homepage-header]

The header at the top of the home page takes you everywhere else:

| Select | To |
| --- | --- |
| **Investigate** | Start an investigation by describing a problem. Refer to [Investigate anything](./use-cases/investigate-anything.md). |
| **Automations** | Have investigations start by themselves. Refer to [Automations](./investigation/automations.md). |
| **Detections** | Review the problems that detection found. Refer to [How detection works](./detection/index.md). |
| {icon}`boxes_vertical` → **Knowledge** | See what {{nightshift}} learned about your system. Refer to [How {{nightshift}} builds context](./context/index.md). |
| {icon}`boxes_vertical` → **Settings** | Manage connectors, Slack, and limits. Refer to [Settings and limits](./settings.md). |

Until {{nightshift}} is set up, the home page shows the **Get started** checklist instead. Refer to [Get started](./get-started.md).

## Next steps [nightshift-homepage-next]

- [Investigate anything](./use-cases/investigate-anything.md): Start your first investigation from the home page
- [Automatically investigate your alerts](./use-cases/auto-investigate-alerts.md): Fill your inbox without starting each investigation yourself
- [How investigations work](./investigation/index.md): Read an investigation and check its reasoning
