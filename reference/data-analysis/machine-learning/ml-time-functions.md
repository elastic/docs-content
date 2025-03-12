---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-time-functions.html
---

# Time functions [ml-time-functions]

The time functions detect events that happen at unusual times, either of the day or of the week. These functions can be used to find unusual patterns of behavior, typically associated with suspicious user activity.

The {{ml-features}} include the following time functions:

* [`time_of_day`](ml-time-functions.md#ml-time-of-day)
* [`time_of_week`](ml-time-functions.md#ml-time-of-week)

::::{note}
* You cannot create forecasts for {{anomaly-jobs}} that contain time functions.
* The `time_of_day` function is not aware of the difference between days, for instance work days and weekends. When modeling different days, use the `time_of_week` function. In general, the `time_of_week` function is more suited to modeling the behavior of people rather than machines, as people vary their behavior according to the day of the week.
* Shorter bucket spans (for example, 10 minutes) are recommended when performing a `time_of_day` or `time_of_week` analysis. The time of the events being modeled are not affected by the bucket span, but a shorter bucket span enables quicker alerting on unusual events.
* Unusual events are flagged based on the previous pattern of the data, not on what we might think of as unusual based on human experience. So, if events typically occur between 3 a.m. and 5 a.m., an event occurring at 3 p.m. is flagged as unusual.
* When Daylight Saving Time starts or stops, regular events can be flagged as anomalous. This situation occurs because the actual time of the event (as measured against a UTC baseline) has changed. This situation is treated as a step change in behavior and the new times will be learned quickly.

::::



## Time_of_day [ml-time-of-day]

The `time_of_day` function detects when events occur that are outside normal usage patterns. For example, it detects unusual activity in the middle of the night.

The function expects daily behavior to be similar. If you expect the behavior of your data to differ on Saturdays compared to Wednesdays, the `time_of_week` function is more appropriate.

This function supports the following properties:

* `by_field_name` (optional)
* `over_field_name` (optional)
* `partition_field_name` (optional)

For more information about those properties, see the [create {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-job).

```js
{
  "function" : "time_of_day",
  "by_field_name" : "process"
}
```

If you use this `time_of_day` function in a detector in your {{anomaly-job}}, it models when events occur throughout a day for each process. It detects when an event occurs for a process that is at an unusual time in the day compared to its past behavior.


## Time_of_week [ml-time-of-week]

The `time_of_week` function detects when events occur that are outside normal usage patterns. For example, it detects login events on the weekend.

::::{important}
The `time_of_week` function models time in epoch seconds modulo the duration of a week in seconds. It means that the `typical` and `actual` values are seconds after a whole number of weeks since 1/1/1970 in UTC which is a Thursday. For example, a value of `475` is 475 seconds after midnight on Thursday in UTC.
::::


This function supports the following properties:

* `by_field_name` (optional)
* `over_field_name` (optional)
* `partition_field_name` (optional)

For more information about those properties, see the [create {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-job).

```js
{
  "function" : "time_of_week",
  "by_field_name" : "eventcode",
  "over_field_name" : "workstation"
}
```

If you use this `time_of_week` function in a detector in your {{anomaly-job}}, it models when events occur throughout the week for each `eventcode`. It detects when a workstation event occurs at an unusual time during the week for that `eventcode` compared to other workstations. It detects events for a particular workstation that are outside the normal usage pattern.

