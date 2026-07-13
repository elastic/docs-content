## June 26, 2026 [elastic-release-notes-2026-06-26]

<!-- _Released: June 26, 2026_ -->
### Features and enhancements [elastic-2026-06-26-features-enhancements]
* Add `IP_LOCATION` command to ES|QL. [#149421](https://github.com/elastic/elasticsearch/pull/149421) [#132489](https://github.com/elastic/elasticsearch/issues/132489) [#150231](https://github.com/elastic/elasticsearch/issues/150231)
* Add circuit breaker protection for multi-search requests. [#150115](https://github.com/elastic/elasticsearch/pull/150115)
* Enable deleting a backing index through the modify data streams API. [#151137](https://github.com/elastic/elasticsearch/pull/151137)
* Improve security behavior when no password is configured. [#151405](https://github.com/elastic/elasticsearch/pull/151405)
* Enable `DOC` partitioning by default for ES|QL `COUNT`. [#150107](https://github.com/elastic/elasticsearch/pull/150107)
* Improve ES|QL ungrouped aggregation performance with vectorization. [#151598](https://github.com/elastic/elasticsearch/pull/151598)
* Improve ES|QL `TopN` performance by pruning constant sort keys. [#147769](https://github.com/elastic/elasticsearch/pull/147769) [#143518](https://github.com/elastic/elasticsearch/issues/143518)
* Improve ES|QL passthrough column handling with `FIRST` in FUSE queries. [#150220](https://github.com/elastic/elasticsearch/pull/150220) [#141596](https://github.com/elastic/elasticsearch/issues/141596)
* Enable ES|QL views REST API in serverless. [#151431](https://github.com/elastic/elasticsearch/pull/151431)
* Enable file-based workload identity for ES|QL S3 and Azure sources. [#151348](https://github.com/elastic/elasticsearch/pull/151348)
* Improve ES|QL external data source read performance with page-index prefetch. [#151241](https://github.com/elastic/elasticsearch/pull/151241)
* Improve ES|QL automatic type casting for compound expressions. [#148800](https://github.com/elastic/elasticsearch/pull/148800) [#141995](https://github.com/elastic/elasticsearch/issues/141995)
* Add `authorization.cloud_api_key.id` to datafeed GET responses for operator visibility. [#150473](https://github.com/elastic/elasticsearch/pull/150473)
* Add `data_storage_class` and `metadata_storage_class` settings for GCP repository. [#151058](https://github.com/elastic/elasticsearch/pull/151058)
* Add PromQL top-level `or` set operator support. [#151486](https://github.com/elastic/elasticsearch/pull/151486)
* Support implicit `le` in PromQL `histogram_quantile`. [#151456](https://github.com/elastic/elasticsearch/pull/151456)
* Improve vector search performance with optimized blob cache memory advice. [#150066](https://github.com/elastic/elasticsearch/pull/150066)
* Improve Painless script compile-time memory allocation checks. [#151339](https://github.com/elastic/elasticsearch/pull/151339)

### Fixes [elastic-2026-06-26-fixes]
* Fix auto date histogram aggregation serialization for rounding info. [#151156](https://github.com/elastic/elasticsearch/pull/151156) [#151155](https://github.com/elastic/elasticsearch/issues/151155)
* Fix time series aggregation serialization when size is set. [#151152](https://github.com/elastic/elasticsearch/pull/151152) [#151151](https://github.com/elastic/elasticsearch/issues/151151)
* Fix matrix stats aggregation serialization for multi-value mode. [#151154](https://github.com/elastic/elasticsearch/pull/151154) [#151153](https://github.com/elastic/elasticsearch/issues/151153)
* Fix PromQL query errors for binary expressions with nested aggregations. [#151635](https://github.com/elastic/elasticsearch/pull/151635)
* Fix inference failures that halt node startup after `commons-lang3` upgrade. [#151794](https://github.com/elastic/elasticsearch/pull/151794)
* Fix ES|QL query failures when combining numeric fields of different sizes. [#151632](https://github.com/elastic/elasticsearch/pull/151632)
* Fix ES|QL union type field resolution errors for surrogate characters. [#151633](https://github.com/elastic/elasticsearch/pull/151633) [#151475](https://github.com/elastic/elasticsearch/issues/151475)
* Fix ES|QL passthrough field loading in time series metadata queries. [#151804](https://github.com/elastic/elasticsearch/pull/151804) [#151540](https://github.com/elastic/elasticsearch/issues/151540)
* Fix ES|QL query crashes when reading fields across multiple index segments. [#149683](https://github.com/elastic/elasticsearch/pull/149683)
* Fix ES|QL `FROM` and `EXTERNAL` WITH-clause syntax in error messages. [#151544](https://github.com/elastic/elasticsearch/pull/151544)
* Fix search tier autoscaling during search node scaling events.
* Fix incorrect per-project took and status in cross-cluster search cluster details. [#150380](https://github.com/elastic/elasticsearch/pull/150380)
* Fix REST client deadlock when retrying across multiple nodes. [#147726](https://github.com/elastic/elasticsearch/pull/147726) [#141558](https://github.com/elastic/elasticsearch/issues/141558)
* Fix vector search on GPU-built INT8 scalar quantized indexes not using quantized vectors. [#149512](https://github.com/elastic/elasticsearch/pull/149512) [#148975](https://github.com/elastic/elasticsearch/issues/148975)
* Fix TSDB query hangs caused by invalid synthetic ID escape prefixes. [#151695](https://github.com/elastic/elasticsearch/pull/151695)
