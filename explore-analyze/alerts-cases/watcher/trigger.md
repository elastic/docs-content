---
navigation_title: Triggers
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/trigger.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
description: Reference for watch triggers that define when watch execution starts.
---

# Watch triggers [trigger]

Every watch must have a trigger that defines when the watch execution process should start. When you create a watch, its trigger is registered with the trigger engine, which evaluates the trigger and starts the watch when conditions are met. {{watcher}} currently supports time-based schedule triggers.

{{watcher}} is designed to support different types of triggers, but only time-based [`schedule`](trigger-schedule.md) triggers are currently available.
