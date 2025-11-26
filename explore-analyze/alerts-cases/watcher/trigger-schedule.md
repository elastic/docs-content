---
navigation_title: Schedule trigger
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/trigger-schedule.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
description: Reference for schedule triggers that define time-based watch execution.
---

# Schedule trigger [trigger-schedule]

Schedule triggers define when watch execution should start based on date and time. All times are in UTC unless a timezone is explicitly specified in the schedule. {{watcher}} uses the system clock to determine the current time, so you should synchronize the clocks of all nodes in the cluster using a time service such as NTP.

{{watcher}} uses the system clock to determine the current time. To ensure schedules are triggered when expected, you should synchronize the clocks of all nodes in the cluster using a time service such as [NTP](http://www.ntp.org/).

::::{note}
{{watcher}} can’t correct for manual adjustments to the system clock. Be aware when making such changes that watch execution may be affected with watches being skipped or repeated if the adjustment covers their target execution time. This applies to changes made via NTP as well.
::::

When specifying a timezone for a watch, keep in mind the effect daylight savings time transitions may have on the schedule, especially if the watch is scheduled to run during the transition. Here’s how {{watcher}} handles watches scheduled during discontinuities:

## Gap Transitions [_gap_transitions]

These occur when the clock moves forward, such as when daylight savings time starts and cause certain hours or minutes to be skipped. If your watch is scheduled to run during a gap transition, the watch is executed at the same time as before the transition.

Example: If a watch is scheduled to run daily at 1:30AM in the `Europe/London` time zone and the clock moves forward one hour from 1:00AM (GMT+0) to 2:00AM (GMT+1), the watch is executed at 2:30AM (GMT+1) which would have been 1:30AM before the transition. Subsequent executions happen at 1:30AM (GMT+1).

## Overlap Transitions [_overlap_transitions]

These occur when the clock moves backward, such as when daylight savings time ends and cause certain hours or minutes to be repeated. If your watch is scheduled to run during an overlap transition, only the first occurrence of the time causes to the watch to execute with the second being skipped.

Example: If a watch is scheduled to run at 1:30 AM and the clock moves backward one hour from 2:00AM to 1:00AM, the watch is executed at 1:30AM and the second occurrence after the change is skipped.
