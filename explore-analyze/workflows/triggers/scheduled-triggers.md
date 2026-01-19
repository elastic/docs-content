---
navigation_title: Scheduled triggers
applies_to:
  stack: preview 9.3+
  serverless: preview
products:
  - id: kibana
  - id: elasticsearch
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Scheduled workflow triggers

Scheduled triggers run workflows automatically at specific times or intervals, without requiring manual intervention. Use scheduled triggers for recurring tasks like reports, data cleanup, or periodic health checks.

You can configure scheduled triggers using:

* **Interval-based scheduling**: Run on a recurring interval (every _x_ minutes, hours, or days)
* **Recurrence rule (RRule) expressions**: Run at specific times in the specified timezone (for example, daily at 2 AM EST)

## Interval-based scheduling

Interval-based scheduling runs a workflow repeatedly at a fixed interval, such as daily or weekly.

The following example shows the basic syntax for an interval-based scheduled trigger:

```yaml
triggers:
  - type: scheduled
    with:
      interval: <amount><unit>
```

The supported units are:

* Seconds: `s`  (minimum supported value: `30s`)
* Minutes: `m`
* Hours: `h`
* Days: `d`

### Examples [interval-examples]

Every 5 minutes:

```yaml
triggers:
  - type: scheduled
    with:
      interval: 5m
```      

Every hour:

```yaml
triggers:
  - type: scheduled
    with:
      interval: 1h
```

Every day:

```yaml
triggers:
  - type: scheduled
    with:
      interval: 1d
```

Every week:

```yaml
triggers:
  - type: scheduled
    with:
      interval: 7d
```

## RRule-based scheduling

RRule-based scheduling runs a workflow at specific times using recurrence rules. This option supports daily, weekly, and monthly frequencies with timezone awareness.

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
| `tzid` | Yes | Timezone identifier | For example, `UTC`, `America/New_York`, `Europe/London` |
| `dtstart` | No | Start date | ISO format (for example, `2024-01-15T09:00:00Z`) |
| `byhour` | No | Hours to run | Array of integers `0`-`23` |
| `byminute` | No | Minutes to run | Array of integers `0`-`59` |
| `byweekday` | Required when `freq` is `WEEKLY` | Days of the week | Array of weekdays: `MO`, `TU`, `WE`, `TH`, `FR`, `SA`, `SU` |
| `bymonthday` | Required when `freq` is `MONTHLY` | Days of the month | Array of integers `1`-`31`. Use negative values to count from the end of the month (for example, -1 for the last day of the month) |

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
