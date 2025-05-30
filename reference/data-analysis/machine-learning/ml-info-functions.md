---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-info-functions.html
products:
  - id: machine-learning
---

# Information content functions [ml-info-functions]

The information content functions detect anomalies in the amount of information that is contained in strings within a bucket. These functions can be used as a more sophisticated method to identify incidences of data exfiltration or C2C activity, when analyzing the size in bytes of the data might not be sufficient.

The {{ml-features}} include the following information content functions:

* `info_content`, `high_info_content`, `low_info_content`


## Info_content, High_info_content, Low_info_content [ml-info-content]

The `info_content` function detects anomalies in the amount of information that is contained in strings in a bucket.

If you want to monitor for unusually high amounts of information, use `high_info_content`. If want to look at drops in information content, use `low_info_content`.

These functions support the following properties:

* `field_name` (required)
* `by_field_name` (optional)
* `over_field_name` (optional)
* `partition_field_name` (optional)

For more information about those properties, see the [create {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-job).

```js
{
  "function" : "info_content",
  "field_name" : "subdomain",
  "over_field_name" : "highest_registered_domain"
}
```

If you use this `info_content` function in a detector in your {{anomaly-job}}, it models information that is present in the `subdomain` string. It detects anomalies where the information content is unusual compared to the other `highest_registered_domain` values. An anomaly could indicate an abuse of the DNS protocol, such as malicious command and control activity.

::::{note}
In this example, both high and low values are considered anomalous. In many use cases, the `high_info_content` function is often a more appropriate choice.
::::


```js
{
  "function" : "high_info_content",
  "field_name" : "query",
  "over_field_name" : "src_ip"
}
```

If you use this `high_info_content` function in a detector in your {{anomaly-job}}, it models information content that is held in the DNS query string. It detects `src_ip` values where the information content is unusually high compared to other `src_ip` values. This example is similar to the example for the `info_content` function, but it reports anomalies only where the amount of information content is higher than expected.

```js
{
  "function" : "low_info_content",
  "field_name" : "message",
  "by_field_name" : "logfilename"
}
```

If you use this `low_info_content` function in a detector in your {{anomaly-job}}, it models information content that is present in the message string for each `logfilename`. It detects anomalies where the information content is low compared to its past behavior. For example, this function detects unusually low amounts of information in a collection of rolling log files. Low information might indicate that a process has entered an infinite loop or that logging features have been disabled.

