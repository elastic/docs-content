---
navigation_title: Triggers
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/trigger.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Triggers [trigger]

Every watch must have a `trigger` that defines when the watch execution process should start. When you create a watch, its trigger is registered with the appropriate *Trigger Engine*. The trigger engine is responsible for evaluating the trigger and triggering the watch when needed.

{{watcher}} is designed to support different types of triggers, but only time-based [`schedule`](trigger-schedule.md) triggers are currently available.
