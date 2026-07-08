## July 2, 2026 [elastic-release-notes-2026-07-02]

<!-- _Released: July 2, 2026_ -->
### Features and enhancements [elastic-2026-07-02-features-enhancements]

* Allow users to snooze and unsnooze individual alert instances. [#264090](https://github.com/elastic/kibana/pull/264090)
* Add cases analytics data view for analyzing cases in Discover and Lens. [#269581](https://github.com/elastic/kibana/pull/269581)
* Add workflow step to push cases to external connectors. [#267539](https://github.com/elastic/kibana/pull/267539)
* Add anomalies section to entity details flyout and details tab. [#273139](https://github.com/elastic/kibana/pull/273139)
* Add rule restore from changes history in Elastic Security. [#274605](https://github.com/elastic/kibana/pull/274605)
* Add rule suggestion skill for Elastic Security. [#269559](https://github.com/elastic/kibana/pull/269559)
* Improve display of long service names in the Traces table. [#275553](https://github.com/elastic/kibana/pull/275553) [#274838](https://github.com/elastic/kibana/issues/274838)
* Improve authentication options for Agent Builder connectors. [#273410](https://github.com/elastic/kibana/pull/273410)
* Improve performance of Synthetics check-group screenshot and step queries. [#273513](https://github.com/elastic/kibana/pull/273513)

### Fixes [elastic-2026-07-02-fixes]
* Fix incorrect handling of environment in service logs. [#275555](https://github.com/elastic/kibana/pull/275555) [#274661](https://github.com/elastic/kibana/issues/274661)
* Fix Workflows `while` loops failing when referenced step output exceeds 10KB. [#275041](https://github.com/elastic/kibana/pull/275041)
* Fix Agent Builder not finding Google Drive files owned by a shared drive. [#274303](https://github.com/elastic/kibana/pull/274303)
* Fix missing manual input dialog for workflow executions in Elastic Security. [#271586](https://github.com/elastic/kibana/pull/271586)
* Fix shared API keys invalidated when one referencing task is removed. [#275157](https://github.com/elastic/kibana/pull/275157)
* Fix broken "Defer loading panels below the fold" dashboard setting. [#275632](https://github.com/elastic/kibana/pull/275632)
* Fix dashboard API returning 400 status for server-side transform errors. [#272694](https://github.com/elastic/kibana/pull/272694)
