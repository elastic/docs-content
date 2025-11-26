---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_throttling.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
description: Explanation of how throttling affects watch execution frequency and scheduling.
---

# Throttling [_throttling]

The throttle period can affect when a watch is actually executed. The default throttle period is five seconds (5000 ms). If you configure a schedule that's more frequent than the throttle period, the throttle period overrides the schedule, limiting how often the watch can run. For example, if you set the throttle period to one minute (60000 ms) and set the schedule to every 10 seconds, the watch executes no more than once per minute.

