---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-explosion.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# Mapping explosion [mapping-explosion]

In Elasticsearch, a mapping or [mapped field](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md) defines the fields in an index and their data types, such as text for full-text search, keyword for exact filtering, or boolean for true/false values. Think of it as a schema that tells Elasticsearch how to interpret and store each piece of data. When the total number of mapped fields across an index grows excessively large, the cluster can experience performance degradation such as slower searches, high heap usage, and prolonged startup times. 

By default, {{es}} allows for [dynamic mappings](/manage-data/data-store/mapping/dynamic-mapping.md) which allows on-the-fly creation of fields. Runaway field growth is colloquially called "mapping explosion". Excessively mapped fields within or across indices can cause the cluster to experience performance degradation such as slower searches, [high JVM memory pressure](/troubleshoot/elasticsearch/high-jvm-memory-pressure.md), and prolonged startup times.

To guard against mapping explosion, {{es}} default enforces field limit of `1000` by way of its [`index.mapping.total_fields.limit`](elasticsearch://reference/elasticsearch/index-settings/mapping-limit.md) setting. {{es}} will reject ingestion requests which would induce further mapped fields for any specific index once its limit threshold is reached with error

```text
Limit of total fields [<index.mapping.total_fields.limit>] has been exceeded while adding new fields [<count>]
```

Advanced users may choose to bypass this rejection with [`index.mapping.total_fields.ignore_dynamic_beyond_limit`](elasticsearch://reference/elasticsearch/index-settings/mapping-limit.md) setting after weighing its effects against their use case.

Mapping explosion typically signals an upstream data formatting issue that should be addressed client-side as [described in this blog](https://www.elastic.co/blog/3-ways-to-prevent-mapping-explosion-in-elasticsearch).

Mapping explosion may surface as the following performance symptoms:

* [CAT nodes](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes) reporting high heap or CPU on the main node and/or nodes hosting the indices shards. This may potentially escalate to temporary node unresponsiveness and/or main overwhelm.
* [CAT tasks](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-tasks) reporting long search durations only related to this index or indices, even on simple searches.
* [CAT tasks](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-tasks) reporting long index durations only related to this index or indices. This usually relates to [pending tasks](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-pending-tasks) reporting that the coordinating node is waiting for all other nodes to confirm they are on mapping update request.
* [CAT pending tasks](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-pending-tasks) reporting a task queue backlog with a lot of `put-mapping [MY_INDEX_NAME/MY_INDEX_UUID]` messages.
* Discover’s **Fields for wildcard** page-loading API command or [Dev Tools](../../explore-analyze/query-filter/tools/console.md) page-refreshing Autocomplete API commands are taking a long time (more than 10 seconds) or timing out in the browser’s Developer Tools Network tab. For more information, refer to our [walkthrough on troubleshooting Discover](https://www.elastic.co/blog/troubleshooting-guide-common-issues-kibana-discover-load).
* Discover’s **Available fields** taking a long time to compile Javascript in the browser’s Developer Tools Performance tab. This may potentially escalate to temporary browser page unresponsiveness.
* Kibana’s [alerting](../../explore-analyze/alerts-cases/alerts.md) or [security rules](../../solutions/security/detect-and-alert.md) may error `The content length (X) is bigger than the maximum allowed string (Y)` where `X` is attempted payload and `Y` is {{kib}}'s [`server-maxPayload`](kibana://reference/configuration-reference/general-settings.md#server-maxpayload).
* Long {{es}} start-up durations.
* Kibana Javascript erring within browser while loading a Dashboard or Discover with message `Maximum call stack size exceeded`.


## Prevent or prepare [prevent]

[Mappings](../../manage-data/data-store/mapping.md) cannot be field-reduced once initialized. {{es}} indices default to [dynamic mappings](../../manage-data/data-store/mapping.md) which doesn’t normally cause problems unless it’s combined with overriding [`index.mapping.total_fields.limit`](elasticsearch://reference/elasticsearch/index-settings/mapping-limit.md). The default `1000` limit is considered generous, though overriding to `10000` doesn’t cause noticeable impact depending on use case. However, to give a bad example, overriding to `100000` and this limit being hit by mapping totals would usually have strong performance implications.

If your index mapped fields expect to contain a large, arbitrary set of keys, you may instead consider:

* Setting [`index.mapping.total_fields.ignore_dynamic_beyond_limit`](elasticsearch://reference/elasticsearch/index-settings/mapping-limit.md) to `true`. Instead of rejecting documents that exceed the field limit, this will ignore dynamic fields once the limit is reached.
* Using the [flattened](elasticsearch://reference/elasticsearch/mapping-reference/flattened.md) data type. Note, however, that flattened objects is [not fully supported in {{kib}}](https://github.com/elastic/kibana/issues/25820) yet. For example, this could apply to sub-mappings like { `host.name` , `host.os`, `host.version` }. Desired fields are still accessed by [runtime fields](../../manage-data/data-store/mapping/define-runtime-fields-in-search-request.md).
* Disable [dynamic mappings](../../manage-data/data-store/mapping.md). This cannot effect current index mapping, but can apply going forward via an [index template](../../manage-data/data-store/templates.md).

Modifying to the [nested](elasticsearch://reference/elasticsearch/mapping-reference/nested.md) data type would not resolve the core issue.


## Check for issue [check]

To confirm the field totals of an index to check for mapping explosion:

* Check {{es}} cluster logs for errors similar to `Limit of total fields [X] in index [Y] has been exceeded` where `X` is the value of  `index.mapping.total_fields.limit` and `Y` is the index name. The correlated client-side ingesting source HTTP 400 `mapper_parsing_exception` log error would be `Limit of total fields [X] has been exceeded while adding new fields [Z]` where `Z` is attempted new fields.
* Review the elected-master node logs for a flood of `[elasticsearch.server][INFO] update_mapping [_doc]` messages. If they time out, a large amount of `org.elasticsearch.cluster.metadata.ProcessClusterEventTimeoutException: failed to process cluster event (put-mapping [<INDEX_NAME>/<INDEX_UUID>]) within 30s` messages display as well.
* For top-level fields, poll [field capabilities](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-field-caps) for `fields=*`.
* Search the output of [get mapping](../../manage-data/data-store/mapping.md) for `"type"`.
* If you’re inclined to use the [third-party tool JQ](https://stedolan.github.io/jq), you can process the [get mapping](../../manage-data/data-store/mapping.md) `mapping.json` output.

    ```sh
    cat mapping.json | jq -c 'to_entries[]| .key as $index| [.value.mappings| to_entries[]|select(.key=="properties") | {(.key):([.value|..|.type?|select(.!=null)]|length)}]| map(to_entries)| flatten| from_entries| ([to_entries[].value]|add)| {index: $index, field_count: .}'
    ```


You can use [analyze index disk usage](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-disk-usage) to find fields which are never or rarely populated as easy wins.


## Complex explosions [complex]

Mapping explosions also covers when an individual index field totals are within limits but combined indices fields totals are very high. It’s very common for symptoms to first be noticed on a [data view](../../explore-analyze/find-and-organize/data-views.md) and be traced back to an individual index or a subset of indices via the [resolve index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-resolve-index).

However, though less common, it is possible to only experience mapping explosions on the combination of backing indices. For example, if a [data stream](../../manage-data/data-store/data-streams.md)'s backing indices are all at field total limit but each contain unique fields from one another.

This situation most easily surfaces by adding a [data view](../../explore-analyze/find-and-organize/data-views.md) and checking its **Fields** tab for its total fields count. This statistic does tells you overall fields and not only where [`index:true`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-index.md), but serves as a good baseline.

If your issue only surfaces via a [data view](../../explore-analyze/find-and-organize/data-views.md), you may consider this menu’s **Field filters** if you’re not using [multi-fields](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md). Alternatively, you may consider a more targeted index pattern or using a negative pattern to filter-out problematic indices. For example, if `logs-*` has too high a field count because of problematic backing indices `logs-lotsOfFields-*`, then you could update to either `logs-*,-logs-lotsOfFields-*` or `logs-iMeantThisAnyway-*`.


## Resolve [resolve]

Mapping explosion is not easily resolved, so it is better prevented via the above. Encountering it usually indicates unexpected upstream data changes or planning failures. If encountered, we recommend reviewing your data architecture. The following options are additional to the ones discussed earlier on this page; they should be applied as best use-case applicable:

* Disable [dynamic mappings](../../manage-data/data-store/mapping.md).
* [Reindex](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) into an index with a corrected mapping, either via [index template](../../manage-data/data-store/templates.md) or [explicitly set](../../manage-data/data-store/mapping.md).
* If index is unneeded and/or historical, consider [deleting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete).
* [Export](logstash-docs-md://lsr/plugins-inputs-elasticsearch.md) and [re-import](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md) data into a mapping-corrected index after [pruning](logstash-docs-md://lsr/plugins-filters-prune.md) problematic fields via Logstash.

[Splitting index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-split) would not resolve the core issue.
