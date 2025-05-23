---
mapped_pages:
  - https://www.elastic.co/docs/manage-data/ingest/transform-enrich/common-mistakes.html
applies_to:
  stack: ga
  serverless: ga
---

# Common mistakes

Here we are not discussing any performance metrics and if one way or the other one is faster, has less heap usage etc. What we are looking for is ease of maintenance and readability. Anybody who knows a bit about ingest pipelines should be able to fix a lot of issues. This section should provide a clear guide to “oh I have written this myself, ah that is the easier way to write it”.

## if statements

### Contains and lots of ORs

This \== statement can be rewritten

```painless
"if": "ctx?.kubernetes?.container?.name == 'admin' || ctx?.kubernetes?.container?.name == 'def' 
|| ctx?.kubernetes?.container?.name == 'demo' || ctx?.kubernetes?.container?.name == 'acme' 
|| ctx?.kubernetes?.container?.name == 'wonderful'
```

to the following easier maintainable and readable comprehension

```painless
["admin","def", ...].contains(ctx.kubernetes?.container?.name)
```

The big implication here is that now the value `admin.contains('admin')` is executed. So if you only want to partially match because your data is `demo-admin-demo` then you still need to write: `ctx.kubernetes.container.name.contains('admin') ||...`

The `?` work without any issue as it will be rewritten to `admin.contains(null)`.

### Missing ? and contains operation

Here is another example, which would fail if `openshift` is not properly set since it is not using `?`, also the `()` are not really doing anything. As well as the unnecessary check of `openshift.origin` and then `openshift.origin.threadId`

```painless
"if": "ctx.openshift.eventPayload != null 
&& (ctx.openshift.eventPayload.contains('Start expire sessions')) 
&& ctx.openshift.origin != null 
&& ctx.openshift.origin.threadId != null 
&& (ctx.openshift.origin.threadId.contains('Catalina-utility'))",
```

This can become this:

```painless
"if": "ctx.openshift?.eventPayload instanceof String 
&& ctx.openshift.eventPayload.contains('Start expire sessions') 
&& ctx.openshift?.origin?.threadId instanceof String 
&& ctx.openshift.origin.threadId.contains('Catalina-utility')",
```

### Contains operation and null check

This includes an initial null check, which is not necessary.

```painless
"if": "ctx.event?.action !=null 
&& ['bandwidth','spoofed syn flood prevention','dns authentication','tls attack prevention',
    'tcp syn flood detection','tcp connection limiting','http rate limiting',
    'block malformed dns traffic','tcp connection reset','udp flood detection',
    'dns rate limiting','malformed http filtering','icmp flood detection',
    'dns nxdomain rate limiting','invalid packets'].contains(ctx.event.action)"
```

This behaves nearly the same:

```painless
"if": "['bandwidth','spoofed syn flood prevention','dns authentication','tls attack prevention',
        'tcp syn flood detection','tcp connection limiting','http rate limiting',
        'block malformed dns traffic','tcp connection reset','udp flood detection',
        'dns rate limiting','malformed http filtering','icmp flood detection',
        'dns nxdomain rate limiting','invalid packets'].contains(ctx.event?.action)"
```

The difference is in the execution itself which should not matter since it is Java under the hood and pretty fast as this. In reality what happens is the following when doing the first one with the initial: `ctx.event?.action != null` If action is null, then it will exit here and not even perform the contains operation. In our second example we basically run the contains operation x times, for every item in the array and have `valueOfarray.contains('null')` then.

### Checking null and type unnecessarily

This is just unnecessary

```painless
"if": "ctx?.openshift?.eventPayload != null && ctx.openshift.eventPayload instanceof String"
```

Because this is the same.

```painless
"if": "ctx.openshift?.eventPayload instanceof String"
```

Similar to the one above, in addition to that, we do not have `?` for dot-walking.

```json
{
  "fail": {
    "message": "This cannot be parsed as it a list and not a single message",
    "if": "ctx._tmp.leef_kv.labelAbc != null && ctx._tmp.leef_kv.labelAbc instanceof List"
  }
},
```

This version is easier to read and maintain since we remove the unnecessary null check and add dot walking.

```json
{
  "fail": {
    "message": "This cannot be parsed as it a list and not a single message",
    "if": "ctx._tmp?.leef_kv?.labelAbc instanceof List"
  }
},
```

### Checking null and for a value

This is interesting as it misses the `?` and therefore will have a null pointer exception if `event.type` is ever null.

```painless
"if": "ctx.event.type == null || ctx.event.type == '0'"
```

This needs to become this:

```painless
"if": "ctx.event?.type == null || ctx.event?.type == '0'"
```

The reason why we need twice the `?` is because we are using an OR operator `||` therefore both parts of the if statement are executed.

### Checking null

It is not necessary to write a `?` after the ctx itself. For first level objects such as `ctx.message`, `ctx.demo` it is enough to write it like this. If ctx is ever null you face other problems (basically the entire context, so the entire `_source` is empty and there is not even a _source... it's basically all null)

```painless
"if": "ctx?.message == null"
```

Is the same as:

```painless
"if": "ctx.message == null"
```

### Checking null multiple times

This is similar to other topics discussed above already. It is often not needed to check using the `?` a 2nd time when you already walked the object / path.

```painless
"if": "ctx.arbor?.ddos?.subsystem == 'CLI' && ctx.arbor?.ddos?.command_line !=null"
```

Same as:

```painless
"if": "ctx.arbor?.ddos?.subsystem == 'CLI' && ctx.arbor.ddos.command_line !=null"
```

Because the if condition is always executed left to right and therefore when `CLI` fails, the 2nd part of the if condition is not triggered. This means that we already walked the `ctx.arbor.ddos` path and therefore know that this object exists.

### Checking null way to often

This:

```painless
"if": "ctx.process != null && ctx.process.thread != null 
       && ctx.process.thread.id != null && (ctx.process.thread.id instanceof String)"
```

Can become just this:

```painless
"if": "ctx.process?.thread?.id instanceof String"
```

That is what the `?` is for, instead of listing every step individually and removing the unnecessary `()` as well.

### Checking emptiness

This:

```painless
"if": "ctx?.user?.geo?.region != null && ctx?.user?.geo?.region != ''"
```

Is the same as this. You do not need to write in the second && clause the ? anymore. Since you already proven that this is not null.

```painless
"if": "ctx.user?.geo?.region != null && ctx.user.geo.region != ''"
```

Alternatively you can use (elvis, but if geo.region is a number/object, anything else than a String, you have a problem)

```painless
"if": "ctx.user?.geo?.region?.isEmpty() ?: false"
```

Alternatively you can use:

```painless
"if": "ctx.user?.geo?.region instanceof String && ctx.user.geo.region.isEmpty() == false"
```

Here is a full reproducible example:

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "user": {
          "geo": {
            "region": "123"
          }
        }
      }
    },
    {
      "_source": {
        "user": {
          "geo": {
            "region": ""
          }
        }
      }
    },
    {
      "_source": {
        "user": {
          "geo": {
            "region": null
          }
        }
      }
    },
    {
      "_source": {
        "user": {
          "geo": null
        }
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "set": {
          "field": "demo",
          "value": true,
          "if": "if": "ctx.user?.geo?.region != null && ctx.user.geo.region != ''"
        }
      }
    ]
  }
}
```

## Going from mb,gb values to bytes

We recommend to store everything as bytes in Elastic in `long` and then use the advanced formatting in Kibana Data View to render the bytes to human readable.

Things like this:

```json
{
  "gsub": {
    "field": "document.size",
    "pattern": "M",
    "replacement": "",
    "ignore_missing": true,
    "if": "ctx?.document?.size != null && ctx.document.size.endsWith(\"M\")"
  }
},
{
  "gsub": {
    "field": "document.size",
    "pattern": "(\\d+)\\.(\\d+)G",
    "replacement": "$1$200",
    "ignore_missing": true,
    "if": "ctx?.uws?.size != null && ctx.document.size.endsWith(\"G\")"
  }
},
{
  "gsub": {
    "field": "document.size",
    "pattern": "G",
    "replacement": "000",
    "ignore_missing": true,
    "if": "ctx?.uws?.size != null && ctx.document.size.endsWith(\"G\")"
  }
}
```

Can become this:

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "document": {
          "size": "100M"
        }
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "bytes": {
          "field": "document.size"
        }
      }
    ]
  }
}
```

## Rename processor

The rename processor renames a field. There are two flags:

- ignore_missing
- ignore_failure

Ignore missing is useful when you are not sure that the field you want to rename from exist. Ignore_failure will help you with any failure encountered. The rename processor can only rename to non-existing fields. If you already have the field `abc` and you want to rename `def` to `abc` then the operation fails. The `ignore_failure` helps you in this case.

## Script processor

Sometimes we have to fallback to script processors.

### Calculating event.duration in a complex manner

There are many things wrong:

- Square bracket access for fields.
- Unnecessary if statement with multiple `!=` null statements instead of `?` usage.
- SubString parsing instead of using DateTime features.
- Event.duration is directly accessed without checking if event is even available.
- Event.duration is wrong, this gives milliseconds. `Event.duration` should be in Nanoseconds.

```json
{
  "script": {
    "source": """
       String timeString = ctx['temp']['duration'];
       ctx['event']['duration'] = Integer.parseInt(timeString.substring(0,2))*360000 + Integer.parseInt(timeString.substring(3,5))*60000 + Integer.parseInt(timeString.substring(6,8))*1000 + Integer.parseInt(timeString.substring(9,12));
     """,
    "if": "ctx.temp != null && ctx.temp.duration != null"
  }
},
```

This becomes this.

We use the if condition to ensure that `ctx.event` is available. The `[:]` is a shorthand to writing `ctx.event = New HashMap();`. We leverage the `DateTimeFormatter` and the `LocalTime` and use a builtin function to calculate the `NanoOfDay`.

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "temp": {
          "duration": "00:00:06.448"
        }
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
      "script": {
        "source": """
           if(ctx.event == null){
             ctx.event = [:];
           }
           DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm:ss.SSS");
           LocalTime time = LocalTime.parse(ctx.temp.duration, formatter);
           ctx.event.duration = time.toNanoOfDay();
         """,
        "if": "ctx.temp != null && ctx.temp.duration != null"
      }
    }
    ]
  }
}
```

## Unnecessary complex script to stitch together IP

- No check if destination is available as object
- Using square brackets for accessing
- Unnecessary casting to Integer, we parse it as a String later anyway, so doesn't really matter.
- Unnecessary allocation of additional field String ip , we can set the ctx. directly.

```json
{
  "script": {
    "source": """
        String[] ipSplit = ctx['destination']['ip'].splitOnToken('.');
        String ip = Integer.parseInt(ipSplit[0]) + '.' + Integer.parseInt(ipSplit[1]) + '.' + Integer.parseInt(ipSplit[2]) + '.' +Integer.parseInt(ipSplit[3]);
        ctx['destination']['ip'] = ip;
    """,
    "if": "(ctx['destination'] != null) && (ctx['destination']['ip'] != null)"
  }
}
```

Can become this. Instead of specifying `String[]` you can also just write `def temp`.

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "destination": {
          "ip": "192.168.0.1.3.4.5.6.4"
        }
      }
    }
  ],
  "pipeline": {
    "processors": [
    {
      "script": {
        "source": """
            String[] temp = ctx.destination.ip.splitOnToken('.');
            ctx.destination.ip = temp[0]+"."+temp[1]+"."+temp[2]+"."+temp[3];
        """,
        "if": "ctx.destination?.ip != null"
      }
    }
    ]
  }
}
```

## Removing of @timestamp

I encountered this bit:

```json
{
  "set": {
    "field": "openshift.timestamp",
    "value": "{{openshift.date}} {{openshift.time}}",
    "if": "ctx?.openshift?.date != null && ctx?.openshift?.time != null && ctx?.openshift?.timestamp == null"
  }
},
{
  "remove": {
    "field": "@timestamp",
    "ignore_missing": true,
    "if": "ctx?.openshift?.timestamp != null || ctx?.openshift?.timestamp1 != null"
  }
},
{
  "date": {
    "field": "openshift.timestamp",
    "formats": [
      "yyyy-MM-dd HH:mm:ss",
      "ISO8601"
    ],
    "timezone": "Europe/Vienna",
    "if": "ctx?.openshift?.timestamp != null"
  }
}
```

The removal is completely unnecessary. The date processor always overwrites the value in `@timestamp` unless you specify the target field.

## Mustache tips and tricks

### Accessing values in an array

Using the `.index` in this case accessing the first value in the array can be done with `.0`

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "host": {
          "hostname": "abc"
        },
        "tags": [
          "cool-host"
        ]
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "set": {
          "field": "host.alias",
          "value": "{{tags.0}}"
        }
      }
    ]
  }
}
```
