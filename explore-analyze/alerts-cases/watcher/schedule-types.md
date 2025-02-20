---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/master/_schedule_types.html
---

# Schedule Types [_schedule_types]

{{watcher}} provides several types of schedule triggers:

* [`hourly`](#schedule-hourly)
* [`daily`](#schedule-daily)
* [`weekly`](#schedule-weekly)
* [`monthly`](#schedule-monthly)
* [`yearly`](#schedule-yearly)
* [`cron`](#schedule-cron)
* [`interval`](#schedule-interval)

## {{watcher}} hourly schedule [schedule-hourly]


A [`schedule`](trigger-schedule.md) that triggers at a particular minute every hour of the day. To use the `hourly` schedule, you specify the minute (or minutes) when you want the scheduler to start the watch execution with the `minute` attribute.

::::{note}
If you don’t specify the `minute` attribute for an `hourly` schedule, it defaults to `0` and the schedule triggers on the hour every hour--`12:00`, `13:00`, `14:00`, and so on.
::::


### Configuring a once an hour schedule [_configuring_a_once_an_hour_schedule]

To configure a once an hour schedule, you specify a single time with the `minute` attribute.

For example, the following `hourly` schedule triggers at minute 30 every hour-- `12:30`, `13:30`, `14:30`, …​:

```js
{
  "trigger" : {
    "schedule" : {
      "hourly" : { "minute" : 30 }
    }
  }
}
```


### Configuring a multiple times hourly schedule [_configuring_a_multiple_times_hourly_schedule]

To configure an `hourly` schedule that triggers at multiple times during the hour, you specify an array of minutes. For example, the following schedule triggers every 15 minutes every hour--`12:00`, `12:15`, `12:30`, `12:45`, `1:00`, `1:15`, …​:

```js
{
  "trigger" : {
    "schedule" : {
      "hourly" : { "minute" : [ 0, 15, 30, 45 ] }
    }
  }
}
```



## {{watcher}} Daily schedule [schedule-daily]


A [`schedule`](trigger-schedule.md) that triggers at a particular time every day. To use the `daily` schedule, you specify the time of day (or times) when you want the scheduler to start the watch execution with the `at` attribute.

Times are specified in the form `HH:mm` on a 24-hour clock. You can also use the reserved values `midnight` and `noon` for `00:00` and `12:00`, and [specify times using objects](#specifying-times-using-objects).

::::{note}
If you don’t specify the `at` attribute for a `daily` schedule, it defaults to firing once daily at midnight, `00:00`.
::::


### Configuring a daily schedule [_configuring_a_daily_schedule]

To configure a once a day schedule, you specify a single time with the `at` attribute. For example, the following `daily` schedule triggers once every day at 5:00 PM:

```js
{
  "trigger" : {
    "schedule" : {
      "daily" : { "at" : "17:00" }
    }
  }
}
```


### Configuring a multiple times daily schedule [_configuring_a_multiple_times_daily_schedule]

To configure a `daily` schedule that triggers at multiple times during the day, you specify an array of times. For example, the following `daily` schedule triggers at `00:00`, `12:00`, and `17:00` every day.

```js
{
  "trigger" : {
    "schedule" : {
      "daily" : { "at" : [ "midnight", "noon", "17:00" ] }
    }
  }
}
```


### Specifying times using objects [specifying-times-using-objects]

In addition to using the `HH:mm` string syntax to specify times, you can specify a time as an object that has `hour` and `minute` attributes.

For example, the following `daily` schedule triggers once every day at 5:00 PM:

```js
{
  "trigger" : {
    "schedule" : {
      "daily" : {
        "at" : {
          "hour" : 17,
          "minute" : 0
        }
      }
    }
  }
}
```

To specify multiple times using the object notation, you specify multiple hours or minutes as an array. For example, following `daily` schedule triggers at `00:00`, `00:30`, `12:00`, `12:30`, `17:00` and `17:30` every day:

```js
{
  "trigger" : {
    "schedule" : {
      "daily" : {
        "at" : {
          "hour" : [ 0, 12, 17 ],
          "minute" : [0, 30]
        }
      }
    }
  }
}
```


### Specifying a time zone for a daily schedule [specifying-time-zone-for-daily-schedule]

By default, daily schedules are evaluated in the UTC time zone. To use a different time zone, you can specify the `timezone` parameter in the schedule. For example, the following `daily` schedule triggers at 6:00 AM and 6:00 PM in the `Pacific/Galapagos` time zone:

```js
{
  "trigger" : {
    "schedule" : {
      "timezone" : "Pacific/Galapagos",
      "daily" : {
        "at" : {
          "hour" : [ 6, 18 ],
          "minute" : 0
        }
      }
    }
  }
}
```



## {{watcher}} weekly schedule [schedule-weekly]


A [`schedule`](trigger-schedule.md) that triggers at a specific day and time every week. To use the `weekly` schedule, you specify the day and time (or days and times) when you want the scheduler to start the watch execution with the `on` and `at` attributes.

You can specify the day of the week by name, abbreviation, or number (with Sunday being the first day of the week):

* `sunday`, `monday`, `tuesday`, `wednesday`, `thursday`, `friday` and `saturday`
* `sun`, `mon`, `tue`, `wed`, `thu`, `fri` and `sat`
* `1`, `2`, `3`, `4`, `5`, `6` and `7`

Times are specified in the form `HH:mm` on a 24-hour clock. You can also use the reserved values `midnight` and `noon` for `00:00` and `12:00`.

### Configuring a weekly schedule [_configuring_a_weekly_schedule]

To configure a once a week schedule, you specify the day with the `on` attribute and the time with the `at` attribute. For example, the following `weekly` schedule triggers once a week on Friday at 5:00 PM:

```js
{
  "trigger" : {
    "schedule" : {
      "weekly" : { "on" : "friday", "at" : "17:00" }
    }
  }
}
```

::::{note}
You can also specify the day and time with the `day` and `time` attributes, they are interchangeable with `on` and `at`.
::::



### Configuring a multiple times weekly schedule [_configuring_a_multiple_times_weekly_schedule]

To configure a `weekly` schedule that triggers multiple times a week, you can specify an array of day and time values. For example, the following `weekly` schedule triggers every Tuesday at 12:00 PM and every Friday at 5:00 PM:

```js
{
  "trigger" : {
    "schedule" : {
      "weekly" : [
        { "on" : "tuesday", "at" : "noon" },
        { "on" : "friday", "at" : "17:00" }
      ]
    }
  }
}
```

Alternatively, you can specify days and times in an object that has `on` and `minute` attributes that contain an array of values. For example, the following `weekly` schedule triggers every Tuesday and Friday at 12:00 PM and 17:00 PM:

```js
{
  "trigger" : {
    "schedule" : {
      "weekly" : {
        "on" : [ "tuesday", "friday" ],
        "at" : [ "noon", "17:00" ]
      }
    }
  }
}
```



## Use a different time zone for a weekly schedule [_use_a_different_time_zone_for_a_weekly_schedule]

By default, weekly schedules are evaluated in the UTC time zone. To use a different time zone, you can specify the `timezone` parameter in the schedule. For example, the following `weekly` schedule triggers at 6:00 AM and 6:00 PM on Tuesdays and Fridays in the `America/Buenos_Aires` time zone:

```js
{
  "trigger" : {
    "schedule" : {
      "timezone" : "America/Buenos_Aires",
      "weekly" : {
        "on" : [ "tuesday", "friday" ],
        "at" : [ "6:00", "18:00" ]
      }
    }
  }
}
```


## {{watcher}} monthly schedule [schedule-monthly]


A [`schedule`](trigger-schedule.md) that triggers at a specific day and time every month. To use the `monthly` schedule, you specify the day of the month and time (or days and times) when you want the scheduler to start the watch execution with the `on` and `at` attributes.

You specify the day of month as a numeric value between `1` and `31` (inclusive). Times are specified in the form `HH:mm` on a 24-hour clock. You can also use the reserved values `midnight` and `noon` for `00:00` and `12:00`.

### Configuring a monthly schedule [_configuring_a_monthly_schedule]

To configure a once a month schedule, you specify a single day and time with the `on` and `at` attributes. For example, the following `monthly` schedule triggers on the 10th of each month at noon:

```js
{
  "trigger" : {
    "schedule" : {
      "monthly" : { "on" : 10, "at" : "noon" }
    }
  }
}
```

::::{note}
You can also specify the day and time with the `day` and `time` attributes, they are interchangeable with `on` and `at`.
::::



### Configuring a multiple times monthly schedule [_configuring_a_multiple_times_monthly_schedule]

To configure a `monthly` schedule that triggers multiple times a month, you can specify an array of day and time values. For example, the following `monthly` schedule triggers at 12:00 PM on the 10th of each month and at 5:00 PM on the 20th of each month:

```js
{
  "trigger" : {
    "schedule" : {
      "monthly" : [
        { "on" : 10, "at" : "noon" },
        { "on" : 20, "at" : "17:00" }
      ]
    }
  }
}
```

Alternatively, you can specify days and times in an object that has `on` and `at` attributes that contain an array of values. For example, the following `monthly` schedule triggers at 12:00 AM and 12:00 PM on the 10th and 20th of each month.

```js
{
  "trigger" : {
    "schedule" : {
      "monthly" : {
        "on" : [ 10, 20 ],
        "at" : [ "midnight", "noon" ]
      }
    }
  }
}
```



## Configuring time zones for monthly schedules [_configuring_time_zones_for_monthly_schedules]

By default, monthly schedules are evaluated in the UTC time zone. To use a different time zone, you can specify the `timezone` parameter in the schedule. For example, the following `monthly` schedule triggers at 6:00 AM and 6:00 PM on the 15th of each month in the `Asia/Tokyo` time zone:

```js
{
  "trigger" : {
    "schedule" : {
      "timezone" : "Asia/Tokyo",
      "monthly" : {
        "on" : [ 15 ],
        "at" : [ 6:00, 18:00 ]
      }
    }
  }
}
```


## {{watcher}} yearly schedule [schedule-yearly]


A [`schedule`](trigger-schedule.md) that triggers at a specific day and time every year. To use the `yearly` schedule, you specify the month, day, and time (or months, days, and times) when you want the scheduler to start the watch execution with the `in`, `on`, and `at` attributes.

You can specify the month by name, abbreviation, or number:

* `january`, `february`, `march`, `april`, `may`, `june`, `july`, `august`, `september`, `october`, `november` and `december`
* `jan`, `feb`, `mar`, `apr`, `may`, `jun`, `jul`, `aug`, `sep`, `oct`, `nov` and `dec`
* `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11` and `12`

You specify the day of month as a numeric value between `1` and `31` (inclusive). The Times are specified in the form `HH:mm` on a 24-hour clock. You can also use the reserved values `midnight` and `noon` for `00:00` and `12:00`.

### Configuring a yearly schedule [_configuring_a_yearly_schedule]

To configure a once a year schedule, you specify the month with the `in` attribute, the day with the  `on` attribute, and the time with the `at` attribute. For example, the following `yearly` schedule triggers once a year at noon on January 10th:

```js
{
  "trigger" : {
    "schedule" : {
      "yearly" : { "in" : "january", "on" : 10, "at" : "noon" }
    }
  }
}
```

::::{note}
You can also specify the month, day, and time with the `month`, `day`, and `time` attributes, they are interchangeable with `in`, `on`, and `at`.
::::



### Configuring a multiple times yearly schedule [_configuring_a_multiple_times_yearly_schedule]

To configure a `yearly` schedule that triggers multiple times a year, you can specify an array of month, day, and time values. For example, the following `yearly` schedule triggers twice a year: at noon on January 10th, and at 5:00 PM on July 20th.

```js
{
  "trigger" : {
    "schedule" : {
      "yearly" : [
        { "in" : "january", "on" : 10, "at" : "noon" },
        { "in" : "july", "on" : 20, "at" : "17:00" }
      ]
    }
  }
}
```

Alternatively, you can specify the months, days, and times in an object that has `in`, `on`, and `minute` attributes that contain an array of values. For example, the following `yearly` schedule triggers at 12:00 AM and 12:00 PM on January 10th, January 20th, December 10th, and December 20th.

```js
{
  "trigger" : {
    "schedule" : {
      "yearly" : {
        "in" : [ "jan", "dec" ],
        "on" : [ 10, 20 ],
        "at" : [ "midnight", "noon" ]
      }
    }
  }
}
```



## Configuring a yearly schedule with a different time zone [_configuring_a_yearly_schedule_with_a_different_time_zone]

By default, the `yearly` schedule is evaluated in the UTC time zone. To use a different time zone, you can specify the `timezone` parameter in the schedule. For example, the following `yearly` schedule triggers at 3:30 PM and 8:30 PM on June 4th in the `Antarctica/Troll` time zone:

```js
{
  "trigger" : {
    "schedule" : {
      "timezone" : "Antarctica/Troll",
      "yearly" : {
          "in" : "june",
          "on" : 4,
          "at" : [ 15:30, 20:30 ]
      }
    }
  }
}
```


## {{watcher}} cron schedule [schedule-cron]


Defines a [`schedule`](trigger-schedule.md) using a [cron expression](https://www.elastic.co/guide/en/elasticsearch/reference/current/api-conventions.html#api-cron-expressions) that specifiues when to execute a watch.

::::{tip}
While cron expressions are powerful, a regularly occurring schedule is easier to configure with the other schedule types. If you must use a cron schedule, make sure you verify it with [`elasticsearch-croneval`](https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-croneval.html) .
::::


### Configure a cron schedule with one time [_configure_a_cron_schedule_with_one_time]

To configure a `cron` schedule, you simply specify the cron expression as a string value. For example, the following snippet configures a `cron` schedule that triggers every day at noon:

```js
{
  ...
  "trigger" : {
    "schedule" : {
      "cron" : "0 0 12 * * ?"
    }
  }
  ...
}
```


### Configure a cron schedule with multiple times [_configuring_a_multiple_times_cron_schedule]

To configure a `cron` schedule that triggers multiple times, you can specify an array of cron expressions. For example, the following `cron` schedule triggers every even minute during weekdays and every uneven minute during the weekend:

```js
{
  ...
  "trigger" : {
    "schedule" : {
      "cron" : [
        "0 0/2 * ? * MON-FRI",
        "0 1-59/2 * ? * SAT-SUN"
      ]
    }
  }
  ...
}
```



## Use a different time zone for a cron schedule [configue_cron_time-zone]

By default, cron expressions are evaluated in the UTC time zone. To use a different time zone, you can specify the `timezone` parameter in the schedule. For example, the following `cron` schedule triggers at 6:00 AM and 6:00 PM during weekends in the `America/Los_Angeles` time zone:

```js
{
  ...
  "trigger" : {
    "schedule" : {
      "timezone" : "America/Los_Angeles",
      "cron" : [
        "0 6,18 * * * SAT-SUN",
      ]
    }
  }
  ...
}
```

### Use croneval to validate cron expressions [croneval]

{{es}} provides a [`elasticsearch-croneval`](https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-croneval.html) command line tool in the `$ES_HOME/bin` directory that you can use to check that your cron expressions are valid and produce the expected results.

To validate a cron expression, pass it in as a parameter to `elasticsearch-croneval`:

```bash
bin/elasticsearch-croneval "0 0/1 * * * ?"
```



## {{watcher}} interval schedule [schedule-interval]


A [`schedule`](trigger-schedule.md) that triggers at a fixed time interval. The interval can be set in seconds, minutes, hours, days, or weeks:

* `"Xs"` - trigger every `X` seconds. For example, `"30s"` means every 30 seconds.
* `"Xm"` - trigger every `X` minutes. For example, `"5m"` means every 5 minutes.
* `"Xh"` - trigger every `X` hours. For example, `"12h"` means every 12 hours.
* `"Xd"` - trigger every `X` days. For example, `"3d"` means every 3 days.
* `"Xw"` - trigger every `X` weeks. For example, `"2w"` means every 2 weeks.

If you don’t specify a time unit, it defaults to seconds.

::::{note}
The interval value differs from the standard *time value* used in Elasticsearch. You cannot configure intervals in milliseconds or nanoseconds.
::::


### Configuring an interval schedule [_configuring_an_interval_schedule]

To configure an `interval` schedule, you specify a string value that represents the interval. If you omit the unit of time (`s`,`m`, `h`, `d`, or `w`), it defaults to seconds.

For example, the following `interval` schedule triggers every five minutes:

```js
{
  "trigger" : {
    "schedule" : {
      "interval" : "5m"
    }
  }
}
```



