## 2026-05-04 [elastic-release-notes-2026-05-04]
### Features and enhancements [elastic-2026-05-04-features-enhancements]
* Add index-based range accessors to FileList. [#147892](https://github.com/elastic/elasticsearch/pull/147892)
* Make Parquet codec factory thread-safe. [#147796](https://github.com/elastic/elasticsearch/pull/147796)
* ESQL: Eliminate redundant S3 HEAD calls via suffix range and object reuse. [#147962](https://github.com/elastic/elasticsearch/pull/147962)
* ESQL: Push down unrelated filters past MV_EXPAND. [#144979](https://github.com/elastic/elasticsearch/pull/144979) [#144636](https://github.com/elastic/elasticsearch/issues/144636)
* ESQL: Adaptive S3 prefetch depth and zero-copy strings. [#147936](https://github.com/elastic/elasticsearch/pull/147936)
* Parquet decode-in-place: eliminate scratch-to-block copy. [#147829](https://github.com/elastic/elasticsearch/pull/147829)
* ESQL: Late materialization for Parquet reading. [#147960](https://github.com/elastic/elasticsearch/pull/147960)
* Surface implicit privileges in get-role API. [#147781](https://github.com/elastic/elasticsearch/pull/147781)
* Add EncryptionService for encrypt/decrypt operations using PEK. [#147418](https://github.com/elastic/elasticsearch/pull/147418)
* Implicit Index Privileges SPI. [#147176](https://github.com/elastic/elasticsearch/pull/147176)
* Disable the cooldown after download detection.
* Include original target and query in profiled search results . [#145230](https://github.com/elastic/elasticsearch/pull/145230) [#143783](https://github.com/elastic/elasticsearch/issues/143783)
* Rename gettor method in SearchResponse for the search profile shard results. [#147911](https://github.com/elastic/elasticsearch/pull/147911)
* Implement updateServiceSettings for VoyageAI. [#147676](https://github.com/elastic/elasticsearch/pull/147676)
* Add stack version and production release to APM attributes. [#147633](https://github.com/elastic/elasticsearch/pull/147633)
* Add doc_values mapping attribute to RoutingFieldMapper. [#146576](https://github.com/elastic/elasticsearch/pull/146576)
* Blob cache defer gap list evaluation. [#147556](https://github.com/elastic/elasticsearch/pull/147556)

### Fixes [elastic-2026-05-04-fixes]
* Use DocValuesSkipper entries when checking for interactive shards.
* ESQL: Validate unsupported grouping types earlier. [#147650](https://github.com/elastic/elasticsearch/pull/147650) [#147596](https://github.com/elastic/elasticsearch/issues/147596)
* ESQL: Fix nullify under join and enrich. [#145743](https://github.com/elastic/elasticsearch/pull/145743) [#141827](https://github.com/elastic/elasticsearch/issues/141827)
* ESQL: Disallow empty lists in named params, only. [#147748](https://github.com/elastic/elasticsearch/pull/147748) [#147448](https://github.com/elastic/elasticsearch/issues/147448)
* ESQL: Fix aggregate windows to use backward looking semantics. [#147289](https://github.com/elastic/elasticsearch/pull/147289)
* ES|QL: Better validation for fulltext functions after LIMIT BY. [#147682](https://github.com/elastic/elasticsearch/pull/147682)
* ES|QL: fix _index LIKE with ? wildcard. [#147462](https://github.com/elastic/elasticsearch/pull/147462) [#146364](https://github.com/elastic/elasticsearch/issues/146364)
* Return null blocks for range fields with doc_values disabled. [#147602](https://github.com/elastic/elasticsearch/pull/147602) [#146527](https://github.com/elastic/elasticsearch/issues/146527)
* Fix up FTF error after FORK. [#147614](https://github.com/elastic/elasticsearch/pull/147614)
* Fix COUNT(*) pushdown for coalesced splits. [#147977](https://github.com/elastic/elasticsearch/pull/147977)
* Bugfix - Block Loader Pushdown + Union Types. [#147940](https://github.com/elastic/elasticsearch/pull/147940)
* Return 400 for malformed OTLP protobuf. [#147797](https://github.com/elastic/elasticsearch/pull/147797)
* Fix PosixCloseableMappedByteBuffer.slice() to preserve concrete type. [#147903](https://github.com/elastic/elasticsearch/pull/147903)
* Check that precondition should not be overwritten on update. [#148111](https://github.com/elastic/elasticsearch/pull/148111)
* Check cluster state block in `_resolve/index`. [#147698](https://github.com/elastic/elasticsearch/pull/147698)
* Fix ordering race in RoleReferenceIntersection. [#147765](https://github.com/elastic/elasticsearch/pull/147765)
* Wait for offline warming ignore stale shutdown entries.
* Set locationToSync for no-op FAILURE results. [#147367](https://github.com/elastic/elasticsearch/pull/147367)
* Fix race in FsBlobContainer.moveBlobAtomic by replacing move op with hard link. [#147405](https://github.com/elastic/elasticsearch/pull/147405)
* Defer snapshot commit release for deleted indices.
* Fix SearchHit leak in chunked fetch failure cleanup path. [#147855](https://github.com/elastic/elasticsearch/pull/147855) [#147812](https://github.com/elastic/elasticsearch/issues/147812)
* Fix: correctly serialise sparse field pruning options in mixed cluster scenarios. [#147823](https://github.com/elastic/elasticsearch/pull/147823)
