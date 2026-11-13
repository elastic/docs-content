---
navigation_title: Settings and limits
applies_to:
  serverless:
    observability: preview
description: Control what Elastic nightshift can reach and how much it runs. Manage connectors and Slack, set daily run limits, add custom context, and pause detection.
products:
  - id: observability
  - id: cloud-serverless
---

# {{nightshift}} settings and limits [nightshift-settings]

On the **Settings** page, admins can controls what {{nightshift}} can reach and what it can run, including connectors and Slack channels, daily run limits, custom context, and detection.

## Before you begin [nightshift-settings-prereqs]

Make sure you have the privileges to open {{nightshift}} **Settings**, and to turn developer mode on or off if you need it. Refer to [Grant access](./get-started/privileges.md#nightshift-privileges-admin).

## Open Settings [nightshift-settings-open]

1. Select **Nightshift** in the navigation menu.
1. On the home page, select {icon}`boxes_vertical` → **Settings**.

The page has three tabs:

| Setting tab| Description |
| --- | --- |
| [General](#nightshift-settings-general) | Add or remove a connector, connect Slack, or turn on developer mode |
| [Investigations](#nightshift-settings-investigations) | Limit investigations, add custom context, or allow outbound hosts for the sandbox |
| [Detections](#nightshift-settings-detections) | Pause detection, change its schedule, limit its runs, or change continuous KI onboarding. From the **Detections** page, select **Settings** in the header to go straight to the **Detections** tab. |
| [Stop or pause {{nightshift}}](#nightshift-settings-stop) | Stop {{nightshift}} from running |

When you change a run limit, a schedule setting, continuous KI onboarding, or token tracking, select **Save changes** in the bar at the bottom of the page. Other controls, such as **Save allowlist**, custom context, and **Pause detection engine**, save on their own.

## General [nightshift-settings-general]

**Connectors**
:   The connectors that investigations use, such as **Local Elasticsearch**, External {{es}}, and GitHub. Select **Add connector**, or **Open in Stack Management** to manage all connectors in {{kib}}. Preconfigured connectors are read-only. Refer to [Connect your data and tools](./investigation/set-up.md).

**Slack channels**
:   Select **Connect Slack** to connect the `@Elastic` Slack app to your workspace, then connect the channels where people can ask `@Elastic` for help and where automations post results. Refer to [Connect your data and tools](./investigation/set-up.md#nightshift-set-up-slack).

**Nightshift developer mode**
:   Shows extra tabs, details, and settings for expert users. Refer to [Developer mode](#nightshift-settings-developer-mode).

### Developer mode [nightshift-settings-developer-mode]

Developer mode shows experimental and expert parts of {{nightshift}}. It's off by default and applies to everyone in the space. To turn it on, on the **General** tab, turn on **Enable nightshift developer mode**. It adds:

- The **Signals** tab on the **Detections** page. Refer to [Rules and signals](./detection/rules-and-signals.md).
- The **Decision Trees** tab on the **Knowledge** page. Refer to [Decision trees](./context/decision-trees.md).
- **Advanced developer settings** on the **Detections** tab, including the cost estimate. Refer to [Advanced developer settings](#nightshift-settings-advanced-dev).
- Extra details, such as the service account's role and raw metadata on Knowledge Indicators.
- A **Knowledge** section on the **General** tab, to purge what {{nightshift}} learned.

**Purge knowledge learned after a point in time**
:   Use it after a suspected prompt injection, or when wrong knowledge got in. It permanently deletes the investigations, Memory, Wiki pages, and decision tree versions in this space that were written after the time you set in **Delete everything learned after**. Knowledge written before that time is kept. Select **Preview impact** to check what it deletes, then **Purge knowledge**. You can't undo this, and snapshots can still hold the deleted documents.

## Investigations [nightshift-settings-investigations]

### Run limits [nightshift-settings-run-limits]

The **Automatic** (5), **Manual** (5), and **All investigations** (10) daily limits, and the **Enforce daily limits** switch. Refer to [Investigation limits](./investigation/limits.md).

### Service account [nightshift-settings-service-account]

Shows whether the service account that runs every investigation is **Set up** for the space. Refer to [Privileges that {{nightshift}} runs with](./get-started/privileges.md#nightshift-privileges-accounts).

### Custom context [nightshift-settings-custom-context]

Notes added to the instructions of every investigation and chat in the space, up to 200 snippets. Select **Edit investigation context** to add, edit, or delete them. For what to write, refer to [Custom context](./investigation/extend.md#nightshift-extend-custom-context).

### Sandbox egress allowlist [nightshift-settings-egress]

The hosts that commands in the investigation sandbox can reach. The hosts of your active connectors are included automatically, so you need it only for other hosts, such as a package index to install a tool, or an API that has no connector.

Enter one hostname or rule per line in **Allowed hosts and rules**, up to 32 rules, then select **Save allowlist**. The allowlist applies to the current space.

:::{dropdown} Allowlist rule examples
| Rule | Allows |
| --- | --- |
| `api.github.com` | All requests to this host |
| `*.datadoghq.com` | All requests to every subdomain |
| `pypi.org GET,HEAD /simple/` | Only `GET` and `HEAD` requests to this path |
| `deny api.github.com POST /gists` | Blocks `POST` requests to this path, even if another rule allows the host |
:::

## Detections [nightshift-settings-detections]

### Pause or resume detection [nightshift-settings-pause]

Pause detection while you change your sources, or to stop its cost.

1. On the **Detections** tab, in **Detection engine activity**, select **Pause detection engine**.
1. Confirm.

Pausing stops Knowledge Indicator extraction, query alerting, rule creation, and significant event discovery in this space. It turns off the rules behind KI queries and cancels running detection workflows. Workflows that every space shares stay on, but their executions in this space are cancelled. Other spaces keep running, and no data is deleted.

The **Detections** page now shows **Paused**. To start again, select **Resume detection engine**, which turns the stopped rules and workflows back on. Scheduled discovery and continuous KI onboarding turn back on only if they were on before the pause.

### Scheduled detection [nightshift-settings-scheduled]

**Enable scheduled discovery** runs discovery automatically in the current space, so that rules and signals become significant events. It's on by default when you turn on detection. Turn it off to stop discovery without pausing the whole engine, and turn it on again to resume. Expand **Advanced schedule settings** to change the schedule.

:::{dropdown} Advanced schedule settings
| Setting | What it does | Default |
| --- | --- | --- |
| **Detection interval (minutes)** | How often scheduled detection runs | 10 |
| **Target coverage (minutes)** | The window within which every active rule is scanned at least once. It must be longer than the detection interval, so rules are spread across runs. | 30 |
| **Review interval (minutes)** | How often scheduled discovery review runs | 10 |
| **Discovery batch size** | The maximum number of detections sent to each scheduled discovery pass | 3 |
| **Review passes** | The maximum number of discovery passes in each scheduled review run | 3 |
:::

### Detection run limits [nightshift-settings-detection-limits]

Daily limits on scheduled detection runs. Runs that you start yourself aren't limited.

| Limit | Counts | Default |
| --- | --- | --- |
| **Discovery daily limit** | Scheduled discovery runs | 15 |
| **Knowledge indicators extraction daily limit** | Scheduled Knowledge Indicator extraction runs | 3 |

Each limit has its own **Enforce daily limits** switch, on by default. The limits apply to the whole deployment and reset at midnight UTC. When one is reached, scheduled runs stop until the reset, and the **Detections** page shows a message.

### Continuous KI onboarding [nightshift-settings-ki-onboarding]

**Enable continuous KI onboarding** extracts Knowledge Indicators from your enabled sources at an interval, so they follow changes in your system. It turns on when the space gets its first source. **Onboarding interval (hours)** sets the minimum time between runs for one source: 12 by default, `0` for no wait. Turning it off cancels running extractions and keeps the KIs already extracted, and you can still start learning by hand. Refer to [Continuous KI onboarding](./context/knowledge-indicators.md#sig-events-ki-continuous).

### Advanced developer settings [nightshift-settings-advanced-dev]

With developer mode on, the **Detections** tab has an **Advanced developer settings** section with the cost estimate and maintenance tools.

:::{dropdown} Advanced developer settings
**Approximate inference cost across all spaces**
:   An estimate of what {{nightshift}} costs, once you turn on **Enable token tracking in this space**. Refer to [Monitor your cost](./cost-and-models.md#nightshift-cost-monitor).

**Stale event cleanup**
:   Closes open significant events whose rules no longer exist. This cleanup also runs automatically every day. Select **Clean up stale events** to run it now.

**Reset Significant Events data**
:   Permanently deletes the Knowledge Indicators, rules, and detections that {{nightshift}} generated in this space, and turns off continuous KI onboarding and scheduled discovery. Significant event history, investigations, source definitions, and your data are kept. You can't undo this.

**Significant events tuning**
:   Select **Edit tuning document** to change how significant event discovery is tuned. Changes can lower the quality of detection. Select **Reset to defaults** to undo them.
:::

## Engine states [nightshift-settings-states]

The **Detections** page shows the state of the detection engine:

| State | Means |
| --- | --- |
| **Monitoring** | Detection runs normally. |
| **Paused** | An admin paused detection. Nothing runs on a schedule, and your data and results are kept. |
| **Unknown** | {{nightshift}} couldn't read the engine's state. Refresh the page. |

## Stop or pause {{nightshift}} [nightshift-settings-stop]

You can't turn {{nightshift}} off or remove its setup. To stop it from running and from using tokens:

1. **Pause detection.** On the **Detections** tab, select **Pause detection engine**. Refer to [Pause or resume detection](#nightshift-settings-pause).
1. **Turn off automations.** Investigations have no pause. On the **Automations** page, turn off **Enabled** for each automation. Refer to [Automations](./investigation/automations.md#nightshift-automations-manage).
1. **Lower the run limits.** On the **Investigations** tab, set the three investigation run limits to the lowest value, and keep **Enforce daily limits** on. A low **Manual investigations daily limit** also blocks Slack mentions and **Investigate** on alerts. Follow-up questions on open investigations are never blocked.

To start again, resume detection, turn your automations back on, and restore the limits.

## Next steps [nightshift-settings-next]

- [Cost and models](./cost-and-models.md): Find out what {{nightshift}} costs, and which settings keep it predictable.
- [Investigation limits](./investigation/limits.md): Learn what happens when a limit is reached.
- [Grant access to {{nightshift}}](./get-started/privileges.md): Give admins the privileges to change these settings.
