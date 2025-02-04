# Ruby Agent version 4.x [release-notes-4.x]

[[release-notes-4.7.3] ==== 4.7.3


#### Fixed [_fixed] 

* Address a bug where if `capture_headers` is false, `ContextBuilder` will raise `"undefined method 'has_key?' for nil:NilClass"` [#1449](https://github.com/elastic/apm-agent-ruby/pull/1449)

[[release-notes-4.7.2] ==== 4.7.2


#### Fixed [_fixed_2] 

* Address machineType not being returned in GCP metadata [#1435](https://github.com/elastic/apm-agent-ruby/pull/1435)

[[release-notes-4.7.1] ==== 4.7.1


#### Fixed [_fixed_3] 

* Skip capturing cookie header when it’s set separately [#1405](https://github.com/elastic/apm-agent-ruby/pull/1405)
* Changes/fixes to metadata.cloud.* fields collected for GCP [#1415](https://github.com/elastic/apm-agent-ruby/pull/1415)
* Pin version of bigdecimal for ruby 2.4 [#1417](https://github.com/elastic/apm-agent-ruby/pull/1417)
* Use response method on Faraday error for older versions of the library [#1419](https://github.com/elastic/apm-agent-ruby/pull/1419)
* Fix ActionDispatchSpy#render_exception for Rails 7.1 [#1423](https://github.com/elastic/apm-agent-ruby/pull/1423)
* Use graphql < 2.1 when Ruby < 2.7 [#1425](https://github.com/elastic/apm-agent-ruby/pull/1425)
* Guard against various Faraday exception response formats [#1428](https://github.com/elastic/apm-agent-ruby/pull/1428)

## 4.7.0 [release-notes-4.7.0]


#### Fixed [_fixed_4] 

* Handle Faraday response being nil [#1382](https://github.com/elastic/apm-agent-ruby/pull/1382)
* Fix error with invalid %-encoding [#1400](https://github.com/elastic/apm-agent-ruby/pull/1400)


#### Added [_added] 

* Add keyword args for span_method helper [#1395](https://github.com/elastic/apm-agent-ruby/pull/1395)


## 4.6.2 [release-notes-4.6.2]


#### Fixed [_fixed_5] 

* Fix Faraday::RackBuilder::StackLocked [#1371](https://github.com/elastic/apm-agent-ruby/pull/1371)


## 4.6.1 [release-notes-4.6.1]


#### Fixed [_fixed_6] 

* Fix growing number of open file descriptors when HTTP request to APM is never sent [#1351](https://github.com/elastic/apm-agent-ruby/pull/1351)
* Fix setting span http status code when Faraday Middleware is used [#1368](https://github.com/elastic/apm-agent-ruby/pull/1368)
* Handle whitespace when splitting tracestate entries [#1353](https://github.com/elastic/apm-agent-ruby/pull/1353)


## 4.6.0 [release-notes-4.6.0]


#### Added [_added_2] 

* Added transaction_name to reported error to allow grouping by transaction name [#1267](https://github.com/elastic/apm-agent-ruby/pull/1267)
* Added ability to query server for version (useful in the future) [#1278](https://github.com/elastic/apm-agent-ruby/pull/1278)
* Added instrumentation for [https://github.com/zendesk/racecar/](https://github.com/zendesk/racecar/) Racecar Kafka library [#1284](https://github.com/elastic/apm-agent-ruby/pull/1284)

### Changed [_changed]

* Expanded filtering to sanitize any key that contains the string *auth* [#1266](https://github.com/elastic/apm-agent-ruby/pull/1266)
* Rename `log_ecs_formatting` option to `log_ecs_reformatting`, deprecate old option name [#1248](https://github.com/elastic/apm-agent-ruby/pull/1248)
* When the configuration value for `log_path` is set, override the `logger` to point to that path instead of using e.g. Rails logger [#1247](https://github.com/elastic/apm-agent-ruby/pull/1247)
* Only send tracestate header for distributed tracing when it has content [#1277](https://github.com/elastic/apm-agent-ruby/pull/1277)
* Use the hostname as the Kubernetes pod name in the Container Info metadata if the pod id is parsed from cgroup [#1314](https://github.com/elastic/apm-agent-ruby/pull/1314)

#### Fixed [_fixed_7]

* Small change to Sidekiq tests to handle new configuration passing method [#1283](https://github.com/elastic/apm-agent-ruby/pull/1283)
* Set transaction sample rate to 0 when it’s unsampled [#1339](https://github.com/elastic/apm-agent-ruby/pull/1339)
* Don’t send unsampled transactions to APM server >= 8.0 [#1341](https://github.com/elastic/apm-agent-ruby/pull/1341)




## 4.5.1 [release-notes-4.5.1]


#### Changed [_changed_2] 

* Update elasticsearch spy to use new transport gem name [#1257](https://github.com/elastic/apm-agent-ruby/pull/1257)
* Standardize placeholder for phone numbers as [PHONENUMBER] per [https://github.com/elastic/apm/blob/main/specs/agents/tracing-instrumentation-aws.md](https://github.com/elastic/apm/blob/main/specs/agents/tracing-instrumentation-aws.md) [#1246](https://github.com/elastic/apm-agent-ruby/pull/1246)

### Fixed [_fixed_8]

* Fixed dependencies to allow CI to build successfully [#1259](https://github.com/elastic/apm-agent-ruby/pull/1259)
* Fixed warnings related to TimeTask timeouts [#1255](https://github.com/elastic/apm-agent-ruby/pull/1255)



## 4.5.0 [release-notes-4.5.0]


#### Changed [_changed_3] 

* Stop collecting the field `http.request.socket.encrypted` [#1181](https://github.com/elastic/apm-agent-ruby/pull/1181)


#### Fixed [_fixed_9] 

* Fixed MongoDB spy thread safety [#1202](https://github.com/elastic/apm-agent-ruby/pull/1202)
* Fixed span context fields for DynamoDB instrumentation [#1178](https://github.com/elastic/apm-agent-ruby/pull/1178)
* Fixed span context fields for S3 instrumentation [#1179](https://github.com/elastic/apm-agent-ruby/pull/1179)
* Update user agent info to match spec [#1182](https://github.com/elastic/apm-agent-ruby/pull/1182)


## 4.4.0 [release-notes-4.4.0]


#### Added [_added_3] 

* Optional span to be ended instead of current span [#1039](https://github.com/elastic/apm-agent-ruby/pull/1039)
* Config option `log_ecs_formatting` [#1053](https://github.com/elastic/apm-agent-ruby/pull/1053)


#### Fixed [_fixed_10] 

* Fixed detecting Linux on Alpine for CPU/MEM metrics [#1057](https://github.com/elastic/apm-agent-ruby/pull/1057)


## 4.3.0 [release-notes-4.3.0]


#### Added [_added_4] 

* Add JVM memory metrics [#1040](https://github.com/elastic/apm-agent-ruby/pull/1040)


## 4.2.0 [release-notes-4.2.0]


#### Added [_added_5] 

* Add support for AWS Storage Table/CosmosDB [#999](https://github.com/elastic/apm-agent-ruby/pull/999)


#### Fixed [_fixed_11] 

* Align HTTP span types/subtypes with spec [#1014](https://github.com/elastic/apm-agent-ruby/pull/1014)
* Passing a full URL as a path to `Net::HTTP` [#1029](https://github.com/elastic/apm-agent-ruby/pull/1029)
* Fix growing number of open file descriptors [#1033](https://github.com/elastic/apm-agent-ruby/pull/1033)


## 4.1.0 [release-notes-4.1.0]


#### Added [_added_6] 

* Azure App Services instance metadata [#1007](https://github.com/elastic/apm-agent-ruby/pull/1007)


#### Changed [_changed_4] 

* `hostname` is now reported split by `configured_hostname` and `detected_hostname` [#1009](https://github.com/elastic/apm-agent-ruby/pull/1009)


#### Fixed [_fixed_12] 

* `service_node_name` is now correctly reported as `service.node.configured_name` [#1009](https://github.com/elastic/apm-agent-ruby/pull/1009)
* Fix JSON parsing when using yajl-ruby [#1012](https://github.com/elastic/apm-agent-ruby/pull/1012)
* Fix SpanHelpers when methods take blocks [#1013](https://github.com/elastic/apm-agent-ruby/pull/1013)
* Fix missing `environment` param when fetching from Central Config [#1014](https://github.com/elastic/apm-agent-ruby/pull/1014)


## 4.0.0 [release-notes-4.0.0]


#### Upgrading [_upgrading] 

Be aware that this release changes the agent’s general approach to instrumenting third party libraries. It now uses `Module#prepend` over alias method chaining.

This doesn’t necessarily impact your application but it could if you are using other gems that use the old approach to patch the same method. Mixing the two approaches can lead to infinite recursion.


#### Removed [_removed] 

* Removed support for Ruby 2.3 and JRuby 9.1 [#901](https://github.com/elastic/apm-agent-ruby/pull/901)
* Config option `active`, see `enabled` [#900](https://github.com/elastic/apm-agent-ruby/pull/900)
* Config option `custom_key_filters`, see `sanitize_field_names` [#900](https://github.com/elastic/apm-agent-ruby/pull/900)
* Config option `default_tags`, see `global_labels` [#900](https://github.com/elastic/apm-agent-ruby/pull/900)
* Config option `default_labels`, see `global_labels` [#900](https://github.com/elastic/apm-agent-ruby/pull/900)
* Config option `ignore_url_patterns`, see `transaction_ignore_urls` [#900](https://github.com/elastic/apm-agent-ruby/pull/900)
* Config option `use_legacy_sql_parser`, legacy parser no longer included [#900](https://github.com/elastic/apm-agent-ruby/pull/900)


#### Changed [_changed_5] 

* Integrations (Spies) use Module#prepend over class_eval [#890](https://github.com/elastic/apm-agent-ruby/pull/890)
* The secrets filter no longer filters based on values, see `sanitize_field_names` [#900](https://github.com/elastic/apm-agent-ruby/pull/900)
* The secrets filter is aligned with other agents, see `sanitize_field_names` [#900](https://github.com/elastic/apm-agent-ruby/pull/900)


#### Added [_added_7] 

* Added `set_service` API [#1006](https://github.com/elastic/apm-agent-ruby/pull/1006)


#### Fixed [_fixed_13] 

* AWS S3 spy accepts symbol bucket names [#998](https://github.com/elastic/apm-agent-ruby/pull/998)
* AWS S3 spy passing on blocks [#998](https://github.com/elastic/apm-agent-ruby/pull/998)
* SQL scanner now recognizes CQL style comments [#1004](https://github.com/elastic/apm-agent-ruby/pull/1004)


