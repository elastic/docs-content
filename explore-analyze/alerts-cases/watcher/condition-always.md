---
navigation_title: Always condition
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/condition-always.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
description: Reference for the always condition that executes watch actions on every trigger.
---

# Always condition [condition-always]

Use the **always** condition to perform the watch actions whenever the watch is triggered, unless they are throttled. This condition is useful for executing actions on a fixed schedule, such as sending a weekly status report email.

The `always` condition enables you to perform watch actions on a fixed schedule, such as, *"Every Friday at noon, send a status report email to `sys.admin@example.com`"*

## Using the always condition [_using_the_always_condition]

This is the default if you omit the condition definition from a watch.

There are no attributes to specify for the `always` condition. To explicitly use this condition, specify the condition type and associate it with an empty object:

```js
"condition" : {
  "always" : {}
}
```
