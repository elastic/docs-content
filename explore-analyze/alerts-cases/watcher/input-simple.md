---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Simple input"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/input-simple.html
---

# Simple input [input-simple]

Use the `simple` input to load static data into the execution context when the watch is triggered. This enables you to store the data centrally and reference it with templates.

You can define the static data as a string (`str`), numeric value (`num`), or an object (`obj`):

```js
"input" : {
  "simple" : {
    "str" : "val1",
    "num" : 23,
    "obj" : {
      "str" : "val2"
    }
  }
}
```
%  NOTCONSOLE

For example, the following watch uses the `simple` input to set the recipient name for a daily reminder email:

```js
{
  "trigger" : {
    "schedule" : {
      "daily" : { "at" : "noon" }
    }
  },
  "input" : {
    "simple" : {
      "name" : "John"
    }
  },
  "actions" : {
    "reminder_email" : {
      "email" : {
        "to" : "to@host.domain",
        "subject" : "Reminder",
        "body" : "Dear {{ctx.payload.name}}, by the time you read these lines, I'll be gone"
      }
    }
  }
}
```
%  NOTCONSOLE
