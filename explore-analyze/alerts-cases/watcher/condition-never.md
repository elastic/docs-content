---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Never condition"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/condition-never.html
---

# Never condition [condition-never]

Use the `never` condition to skip performing the watch actions whenever the watch is triggered. The watch input is processed, a record is added to the watch history, and watch execution ends. This condition is generally used for testing.

## Using the never condition [_using_the_never_condition]

There are no attributes to specify for the `never` condition. To use the it, you specify the condition type and associate it with an empty object:

```js
"condition" : {
  "never" : {}
}
```
%  NOTCONSOLE
