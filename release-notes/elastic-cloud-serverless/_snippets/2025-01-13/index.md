## 2025-01-13 [elasticsearch-serverless-release-notes-2025-01-13]
### Features and enhancements [elasticsearch-serverless-2025-01-13-features-enhancements]
* [Traces] Prevent nested button in full traces in discover. [#247808](https://github.com/elastic/kibana/pull/247808) 
* [Discover] Fix double scroll in fullscreen flyouts. [#247744](https://github.com/elastic/kibana/pull/247744) 

**Dashboards and Visualizations**
* Feature Branch. [#245588](https://github.com/elastic/kibana/pull/245588) 
  Controls are now available as a panel type, which means that they can be freely placed anywhere in your Dashboards! The output filters are limited to their sections, which allows you to target only a subset of panels with a given control. If desired, controls can still be pinned to the top of the Dashboard with a global scope.

**Data ingestion and Fleet**
* Adds capability for rolling back a recent upgrade of a Fleet-managed Elastic Agent upgrade using Fleet UI or API. [#247398](https://github.com/elastic/kibana/pull/247398) 

**Distributed**
* Settings registration and test for logging hot-threads on large management queue size.
  % [#5195](https://github.com/elastic/elasticsearch-serverless/pull/5195)


**ES|QL**
* ESQL: Add timezone to add and sub operators, and ConfigurationAware planning support. [#140101](https://github.com/elastic/elasticsearch/pull/140101) 
* Convert `PackedValuesBlockHash.bytes` to `BreakingBytesRefBuilder` for better memory tracking. [#140171](https://github.com/elastic/elasticsearch/pull/140171) 
* ESQL: Improve Lookup Join performance with CachedDirectoryReader. [#139314](https://github.com/elastic/elasticsearch/pull/139314) 
* ES|QL: add syntax support and parsing for SET approximate. [#139908](https://github.com/elastic/elasticsearch/pull/139908) 
* Mark MATCH_PHRASE second argument as constantOnly . [#247003](https://github.com/elastic/kibana/pull/247003) 

**Elastic Observability solution**
* Feat(slo): instance selector visible when current instance is not defined. [#247638](https://github.com/elastic/kibana/pull/247638) 
  Enhanced the SLO Details page to properly handle grouped SLOs when no specific instance is selected. Users can now search the SLO instances

**Elastic Security solution**
* Improves Attack discovery hallucination detection. [#247965](https://github.com/elastic/kibana/pull/247965) 
* [Privmon] Prepare Monitoring Entity Source CRUD APIs for GA. [#246978](https://github.com/elastic/kibana/pull/246978) 

**Machine learning**
* Trained Models: Adds button to synchronize saved objects. [#247691](https://github.com/elastic/kibana/pull/247691) 
* Inference/AI Connector: mark 429 errors as user errors. [#246640](https://github.com/elastic/kibana/pull/246640) 

**Management**
* [Streamlang] Add uppercase, lowercase and trim processors. [#246540](https://github.com/elastic/kibana/pull/246540) 
* [Streamlang] Expose range to the UI. [#243011](https://github.com/elastic/kibana/pull/243011) 

**Network**
* Always log connection failure at WARN level for sniffed node. [#140149](https://github.com/elastic/elasticsearch/pull/140149) 

**Operations**
* Set heap limit to min(60%, 4gb) for containers if unset. [#246073](https://github.com/elastic/kibana/pull/246073) 
  Containers now set the default Node.js heap to 75% of available memory up to a maximum of 4096mb.  Previously this was set to 50%.

**Search**
* Trigger topology checks when nodes leave the cluster.
  % [#5166](https://github.com/elastic/elasticsearch-serverless/pull/5166)

* Search: Change fielddata circuit breaker/indices cache defaults.
  % [#5053](https://github.com/elastic/elasticsearch-serverless/pull/5053)

* Fix the inference endpoints pull-down on semantic text UI. [#247417](https://github.com/elastic/kibana/pull/247417) 
  Improves the inference endpoint selector layout to keep long endpoint names readable and stable while clarifying ML-node startup behavior.
* Display the API key tab if the user has permission. [#246979](https://github.com/elastic/kibana/pull/246979) 
  Improves the Connection Details flyout by hiding the API Keys tab for users without API key management permissions, providing a cleaner experience.

**Vector search**
* DiskBBQ tail centroids should always be block encoded too. [#139835](https://github.com/elastic/elasticsearch/pull/139835) 
* Dense vector docvalues: add base64 format. [#140094](https://github.com/elastic/elasticsearch/pull/140094) 
* Improve locality by placing parent - child centroids next to each other. [#140293](https://github.com/elastic/elasticsearch/pull/140293) 

### Fixes [elasticsearch-serverless-2025-01-13-fixes]
* [Data Table] Fix link's color contrast. [#247721](https://github.com/elastic/kibana/pull/247721) 
* Encode search term in cases page. [#247992](https://github.com/elastic/kibana/pull/247992) 
* [Discover] Fix trace links calculating date range incorrectly. [#247531](https://github.com/elastic/kibana/pull/247531) 
* Fix `ToolbarSelector` when clicking on tabs. [#247836](https://github.com/elastic/kibana/pull/247836) 
* Fixes a bug where Agent Builder Index Search tools would fail on aliases that contained semantic_text fields. [#247877](https://github.com/elastic/kibana/pull/247877) 
* Update total event in ES document when attaching an event. [#247996](https://github.com/elastic/kibana/pull/247996) 

**Dashboards and Visualizations**
* Increase default top values from 3/5 to 9 categories. [#247015](https://github.com/elastic/kibana/pull/247015) 
* Refetches controls options when the timerange changes. [#248068](https://github.com/elastic/kibana/pull/248068) 

**Elastic Observability solution**
* Fixes validation error with maintenance windows on lightweight synthetics monitors. [#247880](https://github.com/elastic/kibana/pull/247880) 
* Only update relevant monitors where maintenance windows exists. [#246088](https://github.com/elastic/kibana/pull/246088) 
  Only update Synthetics package policies that use maintenance windows when maintenance windows are updated or deleted. Prevents extra Synthetics package policies from being updated when maintenance windows are updated or deleted, even if the monitor itself does not use maintenance windows.
* Default Rule creation. [#245441](https://github.com/elastic/kibana/pull/245441) 
* Fixes the icon in the "Elastic documentation not available" callout in AI Assistant Settings. [#247885](https://github.com/elastic/kibana/pull/247885) 

**Elastic Security solution**
* Changes placement of `Migrations` and `Inventory` in Security Solution Nav. [#247002](https://github.com/elastic/kibana/pull/247002) 
* Encode URL Components for entities. [#247707](https://github.com/elastic/kibana/pull/247707) 
* [Detection Engine] fixes "Rule settings pop-up remain open on clicking 'Save' button after enabling/ disabling auto gap fill.". [#247678](https://github.com/elastic/kibana/pull/247678) 
* Fix API doesn't use an associated conversation's system prompt . [#248020](https://github.com/elastic/kibana/pull/248020) 
* [Attacks/Alerts][Attacks page][Table section] Hide tabs for generic attack groups. [#248444](https://github.com/elastic/kibana/pull/248444) 
* Change alert suppression icon. [#247964](https://github.com/elastic/kibana/pull/247964) 
* [Attack Discovery][Bug] Attack-Discovery misclassified system error "Security AI Anonymization settings configured to not allow any fields" (#246595). [#248439](https://github.com/elastic/kibana/pull/248439) 

**Inference**
* Include rerank in supported tasks for IBM watsonx integration. [#140331](https://github.com/elastic/elasticsearch/pull/140331) 

**Machine learning**
* Data Visualizer: fixes display of map view for small screen sizes. [#247615](https://github.com/elastic/kibana/pull/247615) 
* Disable ES|QL field stats for TS command. [#247641](https://github.com/elastic/kibana/pull/247641) 

**Reindex**
* Disable _delete_by_query and _update_by_query for CCS/stateful. [#140301](https://github.com/elastic/elasticsearch/pull/140301) 

**Search**
* Bugfix: Deleted async search won't show on any API. [#140385](https://github.com/elastic/elasticsearch/pull/140385) 
* Fix API key visibility toggle accessibility on search homepage. [#247982](https://github.com/elastic/kibana/pull/247982) 
  Fixes accessibility issue where the "Show API key" button aria-label did not update to "Hide API key" when toggled, causing screen readers to announce incorrect state.
* Fix: Only run ML saved object check if saving semantic text mapping. [#248462](https://github.com/elastic/kibana/pull/248462) 
  Fixes an issue when running Elasticsearch with a Basic license, where users might encounter errors when updating index mappings, even when adding non-ML field types. This issue has been resolved so that mapping updates now work as expected, while advanced semantic text features continue to require the appropriate license.
* Disabled 'API keys' button on Elasticsearch homepage when logged in user have insufficient permissions. [#248072](https://github.com/elastic/kibana/pull/248072) 
* Fix OpenAI connector header focus order. [#248204](https://github.com/elastic/kibana/pull/248204) 
  Fixes OpenAI connector header add flow so the newly added header Key input receives focus instead of leaving focus on the “Add header” button (addresses accessibility focus order).

% **Snapshot and restore**
% * Fix read/write counts for copy in repo analysis. [#140086](https://github.com/elastic/elasticsearch/pull/140086) 

**TSDB**
* Retrieve routing hash from synthetic id for translog operations. [#140221](https://github.com/elastic/elasticsearch/pull/140221) 

### Documentation [elasticsearch-serverless-2025-01-13-docs]
% * Applies_to syntax changes. [#140275](https://github.com/elastic/elasticsearch/pull/140275) 
% * Add API reference links to longform Elasticsearch REST examples. [#138466](https://github.com/elastic/elasticsearch/pull/138466) 
