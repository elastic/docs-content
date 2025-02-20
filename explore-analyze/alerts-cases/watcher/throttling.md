---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/master/_throttling.html
---

# Throttling [_throttling]

Keep in mind that the throttle period can affect when a watch is actually executed. The default throttle period is five seconds (5000 ms). If you configure a schedule that’s more frequent than the throttle period, the throttle period overrides the schedule. For example, if you set the throttle period to one minute (60000 ms) and set the schedule to every 10 seconds, the watch is executed no more than once per minute. For more information about throttling, see [Acknowledgement and throttling](actions.md#actions-ack-throttle).

