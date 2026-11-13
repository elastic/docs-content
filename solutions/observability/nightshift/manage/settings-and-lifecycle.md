---
applies_to:
  serverless:
    observability: preview
description: Find the Elastic nightshift Settings page, pause detection, and see what the General, Investigations, and Detections tabs control.
products:
  - id: observability
  - id: cloud-serverless
---

# Settings and lifecycle [nightshift-settings-lifecycle]

An admin controls how Elastic nightshift runs from its **Settings** page. You can pause detection, set how often scheduled detection runs, limit how many investigations start each day, and manage the connectors, Slack channels, and context that investigations use.

## Before you begin [nightshift-settings-lifecycle-prereqs]

You need a role that can manage engines. Only users with that role see the **Settings** page.

To open it, select the {icon}`boxes_vertical` menu on the Elastic nightshift home page, then **Settings**. The page has **General**, **Investigations**, and **Detections** tabs.

## Engine states [nightshift-settings-lifecycle-states]

Each engine is in one of these states:

- **On**: The engine runs normally.
- **Paused**: The engine stops its automated work. People can still use it manually.

## Pause or resume detection [nightshift-settings-lifecycle-pause]

1. On the **Settings** page, open the **Detections** tab.
1. In **Detection engine activity**, select **Pause detection engine**.

Confirm the pause when prompted. Pausing stops detection activity in this space, including Knowledge Indicator extraction, query alerting, rule creation, and significant event discovery. It disables the Significant Events workflows in the space and cancels their in-flight executions, and it disables the alerting rules that back Knowledge Indicator queries. Other spaces keep running, and no data is deleted.

Select **Resume detection engine** to restore the managed workflows and rules that pausing turned off.

## Settings tabs [nightshift-settings-lifecycle-tabs]

### General [nightshift-settings-lifecycle-general]

- **Connectors**: The connectors that investigations use, with their names and types. Select **Add connector** to add one, or **Open in Stack Management** to manage them in {{kib}}. Refer to [Connect your data and tools](../get-started/connect-your-data-and-tools.md).
- **Slack channels**: Connect the Elastic Slack app and the channels where `@elastic` answers. Refer to [Connect Slack](../get-started/connect-your-data-and-tools.md#nightshift-connect-slack).

### Investigations [nightshift-settings-lifecycle-investigations]

The **Investigations** tab has an **Investigation process** section with these settings:

- **Run limits**: Daily limits on how many new investigations start. The limits count investigations, not spend, and they apply to the whole deployment, not to one space. Turn **Enforce daily limits** on or off, then set:
  - **Automatic investigations daily limit**: The investigations that all automations start, combined.
  - **Manual investigations daily limit**: The investigations that people start from the home page, a Slack mention, the API, or the CLI.
  - **All investigations daily limit**: Automatic and manual investigations together. It can be lower than the two limits added up.

  Each field shows how many investigations have started today, and the count resets at midnight UTC. When a limit is reached, the investigations it covers are blocked until it resets. Follow-ups on open investigations are never blocked. A start that a limit denies appears as **Skipped** in the automation's **Run history**, with the reason. When a limit denies a start that a Slack message triggered, Elastic nightshift also replies in the Slack thread, once per channel each UTC day, with a link to these settings. Each automation trigger also has its own **Daily trigger limit**. Refer to [Set up an automation](../set-up-an-automation.md#nightshift-set-up-automation-create).

  % TODO(verify): What are the default values of the three run limits? Source: the Kibana nightshift_investigations README says the three limits are deployment-wide and default to 5 for automatic, 5 for manual, and 10 for all investigations, and so does nightshift-program#1886. A screenshot of the Investigations tab shows 20, 5, and 10, so the first field may have been changed, or the default may have changed since the README.
- **Service account**: Whether the service account that runs investigations is set up. Elastic nightshift runs every investigation as this account, not as the user who starts it, and the account's role sets what it can read and change.
- **Custom context**: Notes that Elastic nightshift adds to its instructions for every investigation and chat. Select **Edit investigation context** to change them. Refer to [Add custom context](./manage-knowledge-and-memory.md#nightshift-manage-knowledge-custom-context).
- **Sandbox egress allowlist**: The outbound hosts and rules that sandbox commands can reach. Hosts of active connectors are included automatically. Enter one hostname or rule per line, up to 32 rules, and select **Save allowlist**. For example, a rule can be a host such as `api.github.com`, a wildcard such as `*.datadoghq.com`, or a host with methods and a path, and it can start with `deny`.

### Detections [nightshift-settings-lifecycle-detections]

The **Detections** tab has a **Detection process** section with these settings:

- **Detection engine activity**: Pause detection in this space. Refer to [Pause or resume detection](#nightshift-settings-lifecycle-pause).
- **Scheduled detection**: Turn on **Enable scheduled discovery** to run the detection process automatically in the current space. Expand **Advanced schedule settings** to change the schedule:
  - **Detection interval (minutes)**: How often scheduled detection runs.
  - **Target coverage (minutes)**: The window within which every active rule is scanned at least once. It must exceed the detection interval, so that the rules are spread across runs.
  - **Review interval (minutes)**: How often scheduled discovery review runs.
  - **Discovery batch size**: The maximum number of detections sent to each scheduled discovery pass.
  - **Review passes**: The maximum number of discovery passes in each scheduled review run.
- **Run limits**: Daily limits on scheduled detection runs only. Manual runs aren't limited. For each limit, turn on **Enforce daily limits**, then set:
  - **Discovery daily limit**: The scheduled discovery runs each UTC day.
  - **Knowledge indicators extraction daily limit**: The scheduled Knowledge Indicator extraction runs each UTC day.

  Each limit shows how many scheduled runs counted today, such as "35 counted scheduled admissions today", and when the current UTC day resets. When a limit is reached, new scheduled runs are blocked until the limit resets at midnight UTC. You can still start a run manually. The **Detections** page shows a message at the top, such as "Discovery reached daily run limit of 15 for this deployment. Further scheduled runs will be paused until the limit resets at midnight (UTC). You can still trigger discovery process manually." The limits apply to the whole deployment, not to one space.

  % TODO(verify): What are the default values for the detection limits? Source: one screenshot shows 15 for the Discovery limit and 3 for the Knowledge Indicator extraction limit, and a later one shows 200 and 40, so I can't tell which values are defaults and which someone set.
- **Automatic onboarding**: Turn on **Enable continuous KI onboarding** to run Knowledge Indicator onboarding on enabled sources at the configured interval. It turns on when the space gets its first source. Set **Onboarding interval (hours)** to the minimum number of hours between onboarding runs for a given source. Enter `0` for no cooldown between runs.

## Next steps [nightshift-settings-lifecycle-next]

- [Operator guide](../significant-events/operator-guide.md): Learn about system impact and recovery procedures
