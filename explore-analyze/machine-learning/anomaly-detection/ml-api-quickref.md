---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-api-quickref.html
---

# API quick reference [ml-api-quickref]

All {{ml}} {{anomaly-detect}} endpoints have the following base:

```js
/_ml/
```

The main resources can be accessed with a variety of endpoints:

* [`/anomaly_detectors/`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ml-anomaly): Create and manage {{anomaly-jobs}}
* [`/calendars/`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ml-anomaly): Create and manage calendars and scheduled events
* [`/datafeeds/`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ml-anomaly): Select data from {{es}} to be analyzed
* [`/filters/`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ml-anomaly): Create and manage filters for custom rules
* [`/results/`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ml-anomaly): Access the results of an {{anomaly-job}}
* [`/model_snapshots/`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ml-anomaly): Manage model snapshots

For a full list, see [{{ml-cap}} {{anomaly-detect}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ml-anomaly).
