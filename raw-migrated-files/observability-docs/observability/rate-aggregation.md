# Rate aggregation [rate-aggregation]

You can use a rate aggregation to analyze the rate at which a specific field changes over time. This type of aggregation is useful when you want to analyze fields like counters.

For example, imagine you have a counter field called restarts that increments each time a service restarts. You can use rate aggregation to get an alert if the service restarts more than X times within a specific time window (for example, per day).


## How rates are calculated [how-rates-are-calculated] 

Rates used in alerting rules are calculated by comparing the maximum value of the field in the previous bucket to the maximum value of the field in the current bucket and then dividing the result by the number of seconds in the selected interval. For example, if the value of the restarts increases, the rate would be calculated as:

`(max_value_in_current_bucket - max_value_in_previous_bucket)/interval_in_seconds`

In this example, let’s assume you have one document per bucket with the following data:

```json
{
"timestamp": 0000,
"restarts": 0
}

{
"timestamp": 60000,
"restarts": 1
}
```

Let’s assume the timestamp is a UNIX timestamp in milliseconds, and we started counting on Thursday, January 1, 1970 12:00:00 AM. In that case, the rate will be calculated as follows:

`(max_value_in_current_bucket - max_value_in_previous_bucket)/interval_in_seconds`, where:

* `max_value_in_current_bucket` [now-1m → now]: 1
* `max_value_in_previous_bucket` [now-2m → now-1m]: 0
* `interval_in_seconds`: 60

The rate calculation would be: `(1 - 0) / 60 = 0.0166666666667`

If you want to alert when the rate of restarts is above 1 within a 1-minute window, you would set the threshold above `0.0166666666667`.

The calculation you need to use depends on the interval that’s selected.

