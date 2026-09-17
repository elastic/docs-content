---
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Understand scheduled triggers and how to create and configure them.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Scheduled triggers

Scheduled triggers run workflows automatically at specific times or intervals, without requiring manual intervention. Use scheduled triggers for recurring tasks like reports, data cleanup, or periodic health checks.

Scheduled workflows run with the privileges of the user who last saved the workflow. For details, refer to [Workflow authorization](/explore-analyze/workflows/authorization.md).

You can configure scheduled triggers using:

* **Interval-based scheduling**: Run on a recurring interval (every _x_ minutes, hours, or days)
* **Recurrence rule (RRule) expressions**: Run at specific times in the specified timezone (for example, daily at 2 AM EST)

## Interval-based scheduling

Interval-based scheduling runs a workflow repeatedly at a fixed interval.

The following example shows the basic syntax for an interval-based scheduled trigger:

```yaml
triggers:
  - type: scheduled
    with:
      every: <amount><unit>
```

The supported units are:

* Seconds: `s`  (minimum supported value: `60s`)
* Minutes: `m`
* Hours: `h`
* Days: `d`

### Examples [interval-examples]

Every 5 minutes:

```yaml
triggers:
  - type: scheduled
    with:
      every: 5m
```      

Every hour:

```yaml
triggers:
  - type: scheduled
    with:
      every: 1h
```

Every day:

```yaml
triggers:
  - type: scheduled
    with:
      every: 1d
```

Every week:

```yaml
triggers:
  - type: scheduled
    with:
      every: 7d
```

:::{important}
The minimum supported interval is 1 minute (`1m` or `60s`). Schedules shorter than that are rejected at save time. Pre-9.4 schedules with sub-minute intervals are auto-migrated to `1m` on first edit.
:::

## RRule-based scheduling

RRule-based scheduling runs a workflow at specific times using recurrence rules. This option supports daily, weekly, and monthly frequencies with timezone awareness.

:::{important}
Only `DAILY`, `WEEKLY`, and `MONTHLY` `freq` values are supported. `HOURLY`, `YEARLY`, `MINUTELY`, and `SECONDLY` are rejected. For "every hour", use the interval format (`every: "1h"`) instead.
:::

:::{tip}
`tzid` defaults to `UTC` if omitted. For any business-hours schedule, set `tzid` explicitly to avoid daylight-saving surprises. You can also set a workflow-wide default with [`settings.timezone`](/explore-analyze/workflows/authoring-techniques/settings.md#workflows-settings-timezone); `rrule.tzid` overrides it when both are set.
:::

The following example shows the basic syntax for an RRule-based scheduled trigger:

```yaml
triggers:
  - type: scheduled
    with:
      rrule:
        freq: DAILY
        interval: 1
        tzid: UTC
        dtstart: 2024-01-15T09:00:00Z
        byhour: []
        byminute: []
        byweekday: []
        bymonthday: []
```

### RRule fields

The following table describes the available fields for configuring RRule-based scheduled triggers:

| Field | Required | Description | Values |
| --- | --- | --- | --- |
| `freq` | Yes | Frequency type | `DAILY`, `WEEKLY`, or `MONTHLY` |
| `interval` | Yes | Interval between occurrences | Positive integer (for example, `2` with `freq: WEEKLY` runs every 2 weeks) |
| `tzid` | No | Timezone identifier. Defaults to `UTC`. | IANA timezone name. For example, `UTC`, `America/New_York`, `Europe/London` |
| `dtstart` | No | Start date | ISO format (for example, `2024-01-15T09:00:00Z`) |
| `byhour` | No | Hours to run | Array of integers `0`-`23` |
| `byminute` | No | Minutes to run | Array of integers `0`-`59` |
| `byweekday` | Required when `freq` is `WEEKLY` | Days of the week | Array of weekdays: `MO`, `TU`, `WE`, `TH`, `FR`, `SA`, `SU` |
| `bymonthday` | Required when `freq` is `MONTHLY` | Days of the month | Array of integers `1`-`31`. Use negative values to count from the end of the month (for example, -1 for the last day of the month) |

### Set the run time and timezone [rrule-run-time]

`dtstart` and `tzid` control different things, and confusing them is a common reason a workflow runs at an unexpected hour:

* `dtstart` is a single moment in time. The offset in the timestamp decides which moment: a trailing `Z` means UTC, and `-05:00` means five hours behind UTC. Setting `tzid` doesn't change which moment `dtstart` refers to.
* `tzid` sets the timezone for calculating recurrences. It determines the clock time of each run and follows daylight saving time in that zone. Use an IANA timezone name, such as `America/Chicago`, rather than a fixed offset.

To run a workflow at a specific local time, set `byhour` and `byminute`. Both use `tzid`, so runs stay at that local time when daylight saving time starts or ends. The following example runs every day at 4:00 PM in Chicago:

```yaml
triggers:
  - type: scheduled
    with:
      rrule:
        freq: DAILY
        interval: 1
        tzid: America/Chicago
        byhour: [16]
        byminute: [0]
```

If you omit `byhour` and `byminute`, each run instead uses the clock time that `dtstart` falls on in `tzid`. This is where a `Z` timestamp is most likely to surprise you: `2026-05-11T16:00:00Z` is 4:00 PM UTC, which is 11:00 AM in Chicago, so the following trigger runs daily at 11:00 AM.

```yaml
triggers:
  - type: scheduled
    with:
      rrule:
        freq: DAILY
        interval: 1
        tzid: America/Chicago
        dtstart: 2026-05-11T16:00:00Z
```

To schedule 4:00 PM in Chicago from `dtstart` alone, write the same moment as either `2026-05-11T21:00:00Z` or `2026-05-11T16:00:00-05:00`.

`dtstart` is also the earliest moment a workflow can run, and the schedule skips any occurrence before it. If you omit `dtstart`, the schedule starts when you save the workflow.

To check a schedule, go to the **Workflows** list and hover over the workflow's trigger icon. The tooltip shows **Next execution** using your {{kib}} display timezone.

### Examples [rrule-examples]

Daily at multiple times (6 AM, 12 PM, 6 PM) UTC:

```yaml
triggers:
  - type: scheduled
    with:
      rrule:
        freq: DAILY
        interval: 1
        tzid: UTC
        byhour: [6, 12, 18]
        byminute: [0]
```

Daily with a custom start date at 9 AM UTC:

```yaml
triggers:
  - type: scheduled
    with:
      rrule:
        freq: DAILY
        interval: 1
        tzid: UTC
        dtstart: 2024-01-15T09:00:00Z
        byhour: [9]
        byminute: [0]
```

Every weekday at 8 AM and 5 PM EST:

```yaml
triggers:
  - type: scheduled
    with:
      rrule:
        freq: DAILY
        interval: 1
        tzid: America/New_York
        byweekday: [MO, TU, WE, TH, FR]
        byhour: [8, 17]
        byminute: [0]
```

Weekly - every Tuesday at 10:30 AM UTC:

```yaml
triggers:
  - type: scheduled
    with:
      rrule:
        freq: WEEKLY
        interval: 1
        tzid: UTC
        byweekday: [TU]
        byhour: [10]
        byminute: [30]
```

Every 2 weeks on Monday at 9 AM UTC:

```yaml
triggers:
  - type: scheduled
    with:
      rrule:
        freq: WEEKLY
        interval: 2
        tzid: UTC
        byweekday: [MO]
        byhour: [9]
        byminute: [0]
```

Monthly on 1st and 15th at 10:30 AM UTC:

```yaml
triggers:
  - type: scheduled
    with:
      rrule:
        freq: MONTHLY
        interval: 1
        tzid: UTC
        bymonthday: [1, 15]
        byhour: [10]
        byminute: [30]
```

Monthly on the last day of the month at 11 PM UTC:

```yaml
triggers:
  - type: scheduled
    with:
      rrule:
        freq: MONTHLY
        interval: 1
        tzid: UTC
        bymonthday: [-1]
        byhour: [23]
        byminute: [0]
```

Business hours monitoring (weekdays at 8 AM and 5 PM EST):

```yaml
triggers:
  - type: scheduled
    with:
      rrule:
        freq: DAILY
        interval: 1
        tzid: America/New_York
        byweekday: [MO, TU, WE, TH, FR]
        byhour: [8, 17]
        byminute: [0]
```

