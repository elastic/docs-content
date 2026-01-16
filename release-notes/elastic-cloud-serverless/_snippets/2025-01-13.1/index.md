## 2025-01-13 [elasticsearch-serverless-release-notes-2025-01-13]
### Features and enhancements [elasticsearch-serverless-2025-01-13-features-enhancements]

**ES|QL**
* ESQL: Add timezone to add and sub operators, and ConfigurationAware planning support. [#140101](https://github.com/elastic/elasticsearch/pull/140101) 
* [ES|QL] Convert `PackedValuesBlockHash.bytes` to `BreakingBytesRefBuilder` for better memory tracking. [#140171](https://github.com/elastic/elasticsearch/pull/140171) 
* ESQL: Improve Lookup Join performance with CachedDirectoryReader. [#139314](https://github.com/elastic/elasticsearch/pull/139314) 
* ES|QL: add syntax support and parsing for SET approximate. [#139908](https://github.com/elastic/elasticsearch/pull/139908) 

**Management**
* [Observability:Streams][Streamlang] Add uppercase, lowercase and trim processors. [#246540](https://github.com/elastic/kibana/pull/246540) 
* [Streams] [Streamlang] Expose range to the UI. [#243011](https://github.com/elastic/kibana/pull/243011) 

**Dashboards and Visualizations**
* [Controls Anywhere] Feature Branch. [#245588](https://github.com/elastic/kibana/pull/245588) 

**Data ingestion and Fleet**
* [Fleet] Implement agent upgrade rollback. [#247398](https://github.com/elastic/kibana/pull/247398) 

**Operations**
* [build] Set heap limit to min(75%, 4gb) for containers if unset. [#246073](https://github.com/elastic/kibana/pull/246073) 

**Elastic Observability solution**
* Feat(slo): instance selector visible when current instance is not defined. [#247638](https://github.com/elastic/kibana/pull/247638) 
* Settings registration and test for logging hot-threads on large management queue size.
  % [#5195](https://github.com/elastic/elasticsearch-serverless/pull/5195)

* Trigger topology checks when nodes leave the cluster.
  % [#5166](https://github.com/elastic/elasticsearch-serverless/pull/5166)

* Search: Change fielddata circuit breaker/indices cache defaults.
  % [#5053](https://github.com/elastic/elasticsearch-serverless/pull/5053)

* [Traces][Discover] Fix double scroll in fullscreen flyouts. [#247744](https://github.com/elastic/kibana/pull/247744) 
* [Discover][Traces] Prevent nested button in full traces in discover. [#247808](https://github.com/elastic/kibana/pull/247808) 

**Vector Search**
* DiskBBQ tail centroids should always be block encoded too. [#139835](https://github.com/elastic/elasticsearch/pull/139835) 
* Improve locality by placing parent - child centroids next to each other. [#140293](https://github.com/elastic/elasticsearch/pull/140293) 
* Dense vector docvalues: add base64 format. [#140094](https://github.com/elastic/elasticsearch/pull/140094) 

**Network**
* Always log connection failure at WARN level for sniffed node. [#140149](https://github.com/elastic/elasticsearch/pull/140149) 

**Elastic Security solution**
* [Entity Analytics][Privmon] Prepare Monitoring Entity Source CRUD APIs for GA. [#246978](https://github.com/elastic/kibana/pull/246978) 
* [Attack discovery] Improves Attack discovery hallucination detection. [#247965](https://github.com/elastic/kibana/pull/247965) 

**Search**
* Display the API key tab if the user has permission. [#246979](https://github.com/elastic/kibana/pull/246979) 
* Fix the inference endpoints pull-down on semantic text UI. [#247417](https://github.com/elastic/kibana/pull/247417) 

**Machine learning**
* [ML] Trained Models: Adds button to synchronize saved objects. [#247691](https://github.com/elastic/kibana/pull/247691) 
* [ML] Inference/AI Connector: mark 429 errors as user errors. [#246640](https://github.com/elastic/kibana/pull/246640) 

**Discover**
* [ES|QL] Mark MATCH_PHRASE second argument as constantOnly . [#247003](https://github.com/elastic/kibana/pull/247003) 

### Fixes [elasticsearch-serverless-2025-01-13-fixes]
* Fix GCP CLI storage wipe test.
  % [#5175](https://github.com/elastic/elasticsearch-serverless/pull/5175)

* Bugfix: Deleted async search won't show on any API. [#140385](https://github.com/elastic/elasticsearch/pull/140385) 
* [Cases] Update total event in ES document when attaching an event. [#247996](https://github.com/elastic/kibana/pull/247996) 
* [Discover] Fix `ToolbarSelector` when clicking on tabs. [#247836](https://github.com/elastic/kibana/pull/247836) 
* [Cases] Encode search term in cases page. [#247992](https://github.com/elastic/kibana/pull/247992) 
* [APM][Discover] Fix trace links calculating date range incorrectly. [#247531](https://github.com/elastic/kibana/pull/247531) 
* [Lens][Data Table] Fix link's color contrast. [#247721](https://github.com/elastic/kibana/pull/247721) 
* Use simplified retriever, and log requests and error responses. [#247877](https://github.com/elastic/kibana/pull/247877) 

**Inference**
* [Inference API] Include rerank in supported tasks for IBM watsonx integration. [#140331](https://github.com/elastic/elasticsearch/pull/140331) 

**Snapshot/Restore**
% * Fix read/write counts for copy in repo analysis. [#140086](https://github.com/elastic/elasticsearch/pull/140086) 

**Reindex**
* Disable _delete_by_query and _update_by_query for CCS/stateful. [#140301](https://github.com/elastic/elasticsearch/pull/140301) 

**TSDB**
* Retrieve routing hash from synthetic id for translog operations. [#140221](https://github.com/elastic/elasticsearch/pull/140221) 

**Elastic Security solution**
* [Security Solution][Attacks/Alerts][Attacks page][Table section] Hide tabs for generic attack groups. [#248444](https://github.com/elastic/kibana/pull/248444) 
* [Security Solution][Attack Discovery][Bug] Attack-Discovery misclassified system error "Security AI Anonymization settings configured to not allow any fields" (#246595). [#248439](https://github.com/elastic/kibana/pull/248439) 
* [Security Solution] Changes placement of `Migrations` and `Inventory` in Security Solution Nav. [#247002](https://github.com/elastic/kibana/pull/247002) 
* [Security solution] Fix API doesn't use an associated conversation's system prompt . [#248020](https://github.com/elastic/kibana/pull/248020) 
* [Security Solution][Detection Engine] fixes "Rule settings pop-up remain open on clicking 'Save' button after enabling/ disabling auto gap fill.". [#247678](https://github.com/elastic/kibana/pull/247678) 
* [Security Solution] Change alert suppression icon. [#247964](https://github.com/elastic/kibana/pull/247964) 
* [Security Solution] Encode URL Components for entities. [#247707](https://github.com/elastic/kibana/pull/247707) 

**Search**
* Fix API key visibility toggle accessibility on search homepage. [#247982](https://github.com/elastic/kibana/pull/247982) 
* [Bug] [Search Homepage] Disable API keys on insufficient permissions. [#248072](https://github.com/elastic/kibana/pull/248072) 
* Fix OpenAI connector header focus order. [#248204](https://github.com/elastic/kibana/pull/248204) 
* [Search] Fix: Only run ML saved object check if saving semantic text mapping. [#248462](https://github.com/elastic/kibana/pull/248462) 

**Elastic Observability solution**
* [Synthetics] Only update relevant monitors where maintenance windows exists. [#246088](https://github.com/elastic/kibana/pull/246088) 
* [Synthetics] Fix validation of maintenance windows in project monitors. [#247880](https://github.com/elastic/kibana/pull/247880) 
* [Obs AI] Fix product documentation not available callout icon. [#247885](https://github.com/elastic/kibana/pull/247885) 
* [Synthetics] Default Rule creation. [#245441](https://github.com/elastic/kibana/pull/245441) 

**Dashboards and Visualizations**
* [Lens] Increase default top values from 3/5 to 9 categories. [#247015](https://github.com/elastic/kibana/pull/247015) 
* [ES|QL] Refetches controls options when the timerange changes. [#248068](https://github.com/elastic/kibana/pull/248068) 

**Machine learning**
* [ML] Data Visualizer: fixes display of map view for small screen sizes. [#247615](https://github.com/elastic/kibana/pull/247615) 
* [ML] Disable ES|QL field stats for TS command. [#247641](https://github.com/elastic/kibana/pull/247641) 

### Documentation [elasticsearch-serverless-2025-01-13-docs]
% * [DOCS]: Add API reference links to longform Elasticsearch REST examples. [#138466](https://github.com/elastic/elasticsearch/pull/138466) 
% * [Docs] Applies_to syntax changes. [#140275](https://github.com/elastic/elasticsearch/pull/140275) 
