---
navigation_title: Elastic Observability
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/whats-new.html
products:
  - id: observability
---

# Elastic {{observability}} release notes [elastic-observability-release-notes]
Review the changes, fixes, and more in each version of Elastic {{observability}}.

To check for security updates, go to [Security announcements for the Elastic stack](https://discuss.elastic.co/c/announcements/security-announcements/31).

% Release notes include only features, enhancements, and fixes. Add breaking changes, deprecations, and known issues to the applicable release notes sections.

% ## version.next [elastic-observability-next-release-notes]

% ### Features and enhancements [elastic-observability-next-features-enhancements]
% *

% ### Fixes [elastic-observability-next-fixes]
% *

## 9.4.4 [elastic-observability-9.4.4-release-notes]

### Features and enhancements [elastic-observability-9.4.4-features-enhancements]

* Truncates long service names in the {{product.apm}} **Traces** table with an ellipsis, shows the full name on hover [#275553]({{kib-pull}}275553).
* Adds a defensive check to ensure {{product.apm}} integration policy updates always include API keys in their configuration [#274647]({{kib-pull}}274647).
* Improves Synthetics performance by bounding screenshot and step queries to a window around the check run's timestamp [#273513]({{kib-pull}}273513).
* Enables Synthetics to respect the `observability:searchExcludedDataTiers` advanced setting, allowing operators to exclude slow data tiers from Synthetics searches to reduce latency and search thread pool pressure [#273418]({{kib-pull}}273418).

### Fixes [elastic-observability-9.4.4-fixes]

* Fixes alert untracking on the {{observability}} **Alert Details** page for alerts from non-observability rule types [#278643]({{kib-pull}}278643).
* Fixes `retest_on_failure: false` being ignored when updating an existing Synthetics monitor through the API [#277701]({{kib-pull}}277701).
* Fixes crashes in the {{apm-app}} caused by missing or malformed URL query parameters [#276420]({{kib-pull}}276420).
* Fixes the key column shrinking too narrow in {{product.apm}} metadata key-value tables [#275941]({{kib-pull}}275941).
* Fixes the **Cases** link in alert details routing to an internal URL instead of the Cases app when accessed from external apps [#275647]({{kib-pull}}275647).
* Fixes the {{product.apm}} service **Logs** tab incorrectly filtering by `service.environment` [#275555]({{kib-pull}}275555).
* Fixes the Task Manager API key invalidation task from prematurely invalidating shared API keys still in use by other active tasks [#275157]({{kib-pull}}275157).
* Fixes Synthetics monitor label deletions not persisting after save [#274404]({{kib-pull}}274404).
* Fixes Streams processing not being applied to a second OpenTelemetry metrics data stream when its first processing step is added [#269988]({{kib-pull}}269988).

## 9.4.3 [elastic-observability-9.4.3-release-notes]

### Features and enhancements [elastic-observability-9.4.3-features-enhancements]
* Improves investigation skill matching in the AI Agent to more reliably load for alert-related queries [#269377]({{kib-pull}}269377).
* Improves the AI Agent investigation skill with a hypothesis-driven methodology [#268973]({{kib-pull}}268973).

### Fixes [elastic-observability-9.4.3-fixes]
* Fixes the **SLOs** link in the {{product.apm}} SLO overview flyout to include all-environment SLOs [#273367]({{kib-pull}}273367).
* Fixes example log messages in the **Logs → Anomalies** page from overlapping and becoming unreadable [#273221]({{kib-pull}}273221).
* Fixes the AI Agent investigation skill to anchor time range queries to the alert start time when investigating an alert [#271983]({{kib-pull}}271983).
* Fixes knowledge base recall in Observability AI Assistant when the selected connector is an inference endpoint [#271753]({{kib-pull}}271753).

## 9.4.2 [elastic-observability-9.4.2-release-notes]

### Fixes [elastic-observability-9.4.2-fixes]
* Fixes false **missing integration** warnings for project Synthetics monitors on private locations [#270137]({{kib-pull}}270137).
* Fixes horizontal scroll clipping on the {{product.apm}} **Traces** page [#269936]({{kib-pull}}269936).
* Fixes the **Explain this log entry** AI insight in the logs flyout collapsing and losing its state on auto-refresh [#268895]({{kib-pull}}268895).
* Fixes the Streams **Significant Events** tab and import/export flyouts to correctly enforce the Enterprise license requirement [#268515]({{kib-pull}}268515).
* Fixes the **SLO Overview** **No data** tile to correctly count newly created SLOs and SLOs whose summary transform has not yet produced a document [#266315]({{kib-pull}}266315).
* Fixes the **Modify suggestions** button in Streams so clicking it while the popover is open correctly closes the popover [#265254]({{kib-pull}}265254).


## 9.4.1 [elastic-observability-9.4.1-release-notes]

There are no user-facing changes in {{observability}} for the 9.4.1 release.

## 9.4.0 [elastic-observability-9.4.0-release-notes]

### Features and enhancements [elastic-observability-9.4.0-features-enhancements]

* Removes the confirmation modal when switching to AI Agent mode [#264839]({{kib-pull}}264839).
* Adds the `observability.investigation` skill to the Elastic Agent, providing structured investigation methodology across all Observability tools for service health, dependency analysis, and log and trace correlation [#262293]({{kib-pull}}262293).
* Adds AI Agent as the default Observability chat experience. AI Assistant has been deprecated. Users can return to AI Assistant through **GenAI Settings** [#260570]({{kib-pull}}260570).
* Adds a continuous Knowledge Indicator extraction workflow to Streams **Significant Events Discovery** that automatically identifies stream features on a configurable schedule [#260322]({{kib-pull}}260322).
* Consolidates LLM connector listing through the inference plugin for consistent AI connector management [#258530]({{kib-pull}}258530).
* Adds a Streams exploration skill to the AI Agent Builder [#258330]({{kib-pull}}258330).
* Adds entity retrieval and enrichment capabilities for contextual data loading in AI-powered features [#256628]({{kib-pull}}256628).
* Adds Synthetics monitor attachment support to the AI Agent for contextual monitor data [#256540]({{kib-pull}}256540).
* Updates the AI Agent system prompt to use the time range from screen context attachments [#256343]({{kib-pull}}256343).
* Adds the `get_logs` tool and a log search skill to the AI Agent for natural-language log retrieval [#256206]({{kib-pull}}256206).
* Adds Gemini 2.5 Flash Lite, Claude 4.5 Haiku, and Claude 4.6 Sonnet preconfigured connectors [#253109]({{kib-pull}}253109).
* Adds host metrics and correlation data to the Alerts AI Insight for enriched alert context [#252973]({{kib-pull}}252973).
* Adds SLO and service entity attachments to the AI Agent Builder for richer observability context [#252390]({{kib-pull}}252390).
* Adds an Anthropic Claude Opus 4.6 preconfigured connector [#252177]({{kib-pull}}252177).
* Adds the `get_service_topology` tool to the AI Agent for retrieving APM service topology data [#251770]({{kib-pull}}251770).
* Adds the `get_runtime_metrics` tool to the AI Agent for retrieving service runtime metrics [#251768]({{kib-pull}}251768).
* Adds the `get_traces` tool to the AI Agent for retrieving distributed trace samples [#250952]({{kib-pull}}250952).
* Enhances the `get_log_groups` tool (formerly `get_log_categories`) with exception support [#250331]({{kib-pull}}250331).
* Adds latency percentile sorting and retrieval to the `get_trace_metrics` AI Agent tool [#249488]({{kib-pull}}249488).
* Adds new preconfigured connectors for AI inference providers [#249379]({{kib-pull}}249379).
* Adds an Elastic Inference Service (EIS) pricing callout to the Observability AI Assistant **Knowledge Base** settings for semantic search models [#249298]({{kib-pull}}249298).
* Improves context provided to the Alerts AI Insight for more accurate analysis [#248195]({{kib-pull}}248195).
* Adds the `get_trace_change_points` tool to the AI Agent for identifying performance change points in traces [#247810]({{kib-pull}}247810).
* Adds log and metric change point analysis tools to the AI Agent [#242423]({{kib-pull}}242423).
* Adds a **Partitioning** tab to classic streams with support for query-based stream routing [#261162]({{kib-pull}}261162).
* Adds a **Create enrich policy** link to the Streams enrich processor form [#260800]({{kib-pull}}260800).
* Enables users to iteratively refine AI-generated partition suggestions in Streams by providing natural language guidance [#260264]({{kib-pull}}260264).
* Adds an `enrich` processor to Streams for enriching log data using Elasticsearch enrich policies [#256971]({{kib-pull}}256971).
* Adds a `split` and `sort` processor to Streams [#251681]({{kib-pull}}251681).
* Improves condition filtering in the Streams processing editor [#251129]({{kib-pull}}251129).
* Adds a `network_direction` processor to Streams [#250894]({{kib-pull}}250894).
* Adds a `redact` processor to Streams for masking sensitive field values [#250389]({{kib-pull}}250389).
* Adds a features table with a detail flyout and bulk delete to the Streams management interface [#250379]({{kib-pull}}250379).
* Adds an `includes` operator to the Streams routing condition editor [#248985]({{kib-pull}}248985).
* Adds empty state messaging to the Streams stream listing [#248636]({{kib-pull}}248636).
* Adds background task-based significant events query generation in Streams, with dedicated `_task` and `_status` API endpoints [#248608]({{kib-pull}}248608).
* Adds empty state messaging to the Streams **Partitioning** and **Processing** tabs [#248463]({{kib-pull}}248463).
* Adds a **Queries** tab to Streams for managing query-based routing configurations [#248243]({{kib-pull}}248243).
* Adds a `concat` processor to Streams [#247940]({{kib-pull}}247940).
* Adds abort support and silent mode for AI-generated stream descriptions in Streams [#247082]({{kib-pull}}247082).
* Adds `uppercase`, `lowercase`, and `trim` processors to Streams [#246540]({{kib-pull}}246540).
* Adds a range operator to the Streams condition editor, supporting inclusive and exclusive boundaries with date math [#243011]({{kib-pull}}243011).
* Adds integration health detection and self-healing for Synthetics monitors to automatically recover from integration failures [#256738]({{kib-pull}}256738).
* Adds a reset API endpoint for individual Synthetics monitors [#256696]({{kib-pull}}256696).
* Updates browser monitors on private locations to explicitly enable network and screenshot data streams [#255967]({{kib-pull}}255967).
* Improves the maintenance window callout for private location Synthetics monitors [#252847]({{kib-pull}}252847).
* Reduces the default sync interval for private location monitors and makes the interval configurable [#252708]({{kib-pull}}252708).
* Adds a configurable timeout for browser monitors running on private locations [#252156]({{kib-pull}}252156).
* Adds OpenAPI examples to SLO API endpoints [#259859]({{kib-pull}}259859).
* Improves SLO template discoverability in the SLO creation workflow [#256545]({{kib-pull}}256545).
* Displays APM SLOs in the **Service Inventory** for at-a-glance SLO health per service [#249374]({{kib-pull}}249374).
* Enables creating and managing SLOs directly from the **Service Inventory** [#249259]({{kib-pull}}249259).
* Adds cluster-wide SLO health scanning using API-triggered background tasks [#248004]({{kib-pull}}248004).
* Enables the instance selector on the **SLO Details** page when browsing grouped SLOs without a specific instance selected [#247638]({{kib-pull}}247638).
* Enables management of SLO stale threshold settings on Elastic Serverless [#246760]({{kib-pull}}246760).
* Changes default APM alert rules to group by `transaction.name` for more precise alert scoping [#261929]({{kib-pull}}261929).
* Adds alert and SLO health badges to the APM **Service Map** for at-a-glance service status [#261822]({{kib-pull}}261822).
* Adds a unified APM correlations API endpoint for both latency and failed transaction analysis [#254607]({{kib-pull}}254607).
* Adds error handling to the Observability landing page redirect logic to prevent crashes on invalid routes [#254171]({{kib-pull}}254171).
* Adds support for ECS-formatted errors in APM service details [#254138]({{kib-pull}}254138).
* Enables exploring service map requests in Discover directly from the APM **Service Map** [#254011]({{kib-pull}}254011).
* Adds OTel and semconv support for Kubernetes pods and containers, and Docker containers in the APM **Infrastructure** tab [#252188]({{kib-pull}}252188).
* Shows RED metrics charts in Discover for `traces.*` queries [#249909]({{kib-pull}}249909).
* Adds a **View in Discover** link to the **Alert Details** page for APM rule-based alerts, enabling direct navigation to the triggering documents [#248990]({{kib-pull}}248990).
* Enables troubleshooting of requests between nodes directly from the APM **Service Map** [#248646]({{kib-pull}}248646).
* Replaces the legacy APM trace waterfall component with the unified Trace Waterfall for a consistent trace viewing experience [#248629]({{kib-pull}}248629).
* Migrates the traces panel in Discover to the unified flyout system [#247451]({{kib-pull}}247451).
* Adds critical path highlighting to the traces view in Discover [#246952]({{kib-pull}}246952).
* Synchronizes span link and error count badges in the unified Trace Waterfall [#246510]({{kib-pull}}246510).
* Metrics exploration in Discover is now generally available [#261325]({{kib-pull}}261325).
* Improves `METRICS_INFO` failure handling in the UI to prevent error states [#260940]({{kib-pull}}260940).
* Adds tooltip descriptions to metrics in the **View details** flyout [#257053]({{kib-pull}}257053).
* Supports multi-dimension breakdowns in Lens series layers [#251731]({{kib-pull}}251731).
* Migrates the metrics panel in the Discover flyout to the unified flyout system [#251395]({{kib-pull}}251395).
* Supports multi-dimension breakdown in Discover's unified metrics view [#250727]({{kib-pull}}250727).
* Connects the Discover sidebar field breakdown selection to the metrics view breakdown dimension [#248920]({{kib-pull}}248920).
* Enables multi-terms chart aggregations in {{esql}}-powered Lens visualizations [#244743]({{kib-pull}}244743).
* Enables **Unified Rules** as the default experience [#258214]({{kib-pull}}258214).
* Adds the ability to acknowledge and unacknowledge alerts from the Observability **Alerts** page [#252945]({{kib-pull}}252945).
* Extends no-data behavior options from metric threshold rules to custom threshold rules [#251976]({{kib-pull}}251976).
* Supports KQL filtering across all aggregation types in Custom Threshold Rules [#248845]({{kib-pull}}248845).
* Adds a unified rules list for managing all Observability alert rules in one place [#242208]({{kib-pull}}242208).
* Enables the Fleet `POST /api/fleet/service_tokens` endpoint and Remote Elasticsearch outputs in serverless deployments [#260515]({{kib-pull}}260515).
* Adds data detection and loading indicators to Observability onboarding flows [#257870]({{kib-pull}}257870).
* Adds an EDOT Cloud Forwarder quick-start tile to the Observability onboarding experience for ingesting VPC Flow, ELB Access, and CloudTrail logs from AWS S3 [#250325]({{kib-pull}}250325).
* Adds Windows host support to the OpenTelemetry host onboarding flow [#248478]({{kib-pull}}248478).
* Adds a **Manage jobs** link to the Machine Learning left navigation for direct access to anomaly detection jobs [#260605]({{kib-pull}}260605).
* Adds **Visualizations** and **Annotation Groups** tabs to the Dashboards interface and removes the standalone Visualize Library from solution navigations [#241795]({{kib-pull}}241795).

### Fixes [elastic-observability-9.4.0-fixes]

* Fixes an issue where Observability alerts sent recovery notifications but remained `active` in {{kib}} instead of transitioning to `recovered` [#261012]({{kib-pull}}261012).
* Fixes the layout of the Elastic Inference Service (EIS) pricing callout [#262780]({{kib-pull}}262780).
* Adds the EIS cost callout to all relevant AI Assistant settings locations [#255588]({{kib-pull}}255588).
* Fixes AI/Inference connector creation to correctly use the `location` field for provider configuration [#250838]({{kib-pull}}250838).
* Updates the AI Insight UI description [#250137]({{kib-pull}}250137).
* Fixes truncated inline attachments in the AI Agent [#249799]({{kib-pull}}249799).
* Updates AI Insights and flyout configuration to use the Observability Agent [#249776]({{kib-pull}}249776).
* Adds `maxQueue` backpressure to the anonymization regex worker pool to prevent memory pressure under load [#249108]({{kib-pull}}249108).
* Fixes the icon in the **Elastic documentation not available** callout in AI Assistant settings [#247885]({{kib-pull}}247885).
* Exposes the `canReadFailureStore` permission on a per-stream basis [#264087]({{kib-pull}}264087).
* Fixes dimension type conflicts in Streams by casting dimension values [#263472]({{kib-pull}}263472).
* Fixes an error in Streams when generating patterns from invalid AI suggestions [#260325]({{kib-pull}}260325).
* Adds support for Cross-Cluster Replication (CCR) and clusters without security enabled in Streams [#259175]({{kib-pull}}259175).
* Fixes AI pipeline suggestions in Streams that were using incorrect field names on ECS and OTel streams [#258139]({{kib-pull}}258139).
* Marks {{esql}} rule execution errors as user-triggered in Streams rules to prevent unnecessary Task Manager retries [#255011]({{kib-pull}}255011).
* Fixes time range refresh in Streams to apply the updated time range correctly [#253295]({{kib-pull}}253295).
* Fixes overlapping badge display for processor names in Streams [#251874]({{kib-pull}}251874).
* Fixes a `too_small` validation error for AI pipeline suggestions with empty grok patterns [#251113]({{kib-pull}}251113).
* Fixes filtering by multiline string fields in Streams [#250047]({{kib-pull}}250047).
* Fixes query synchronization on save and adds debounce to the Streams Significant Events preview chart [#249833]({{kib-pull}}249833).
* Prevents editing of AI-generated significant event queries to protect their integrity [#249716]({{kib-pull}}249716).
* Fixes child stream name validation in Streams to prevent spaces in stream names [#249384]({{kib-pull}}249384).
* Fixes document rejection in Streams partitioning when documents arrive during routing evaluation [#247953]({{kib-pull}}247953).
* Fixes time range state being lost when navigating to the **Retention** tab in Streams [#247544]({{kib-pull}}247544).
* Fixes field name autocomplete in the Streams **Processing** tab for newly mapped fields [#246934]({{kib-pull}}246934).
* Fixes a `mapper_parsing_exception` error in wired streams during document ingestion [#245838]({{kib-pull}}245838).
* Fixes the **Failed Tests by Step** panel in Synthetics to update correctly when the time range changes [#263317]({{kib-pull}}263317).
* Fixes the flyout toggle state sticking when switching between Synthetics monitors in the details flyout [#253314]({{kib-pull}}253314).
* Fixes Synthetics package policy ID management by removing `spaceId` from the policy ID and storing it as a reference in the monitor saved object [#251018]({{kib-pull}}251018).
* Fixes project monitors to use the monitor query ID for package policies [#248762]({{kib-pull}}248762).
* Fixes duplicate Synthetics test results appearing on the monitor status heat map at higher granularity [#248761]({{kib-pull}}248761).
* Fixes a validation error when applying maintenance windows to lightweight Synthetics monitors [#247880]({{kib-pull}}247880).
* Fixes Synthetics console state persisting across journey steps [#247376]({{kib-pull}}247376).
* Fixes Synthetics tasks to only update package policies for monitors that reference maintenance windows, preventing unnecessary updates [#246088]({{kib-pull}}246088).
* Fixes default rule creation to only trigger when creating or editing a monitor, not on navigation events [#245441]({{kib-pull}}245441).
* Adds a spaces constraint to private locations, restricting monitor creation to associated spaces [#233662]({{kib-pull}}233662).
* Fixes an error on the burn rate alert details page for suppressed alerts [#256435]({{kib-pull}}256435).
* Fixes dashboard filters not being applied to the SLO embeddable when grouping fields are used [#255746]({{kib-pull}}255746).
* Fixes alert visibility and filters for grouped SLOs on the **SLO details** page [#254601]({{kib-pull}}254601).
* Fixes SLO filter behavior for filters containing spaces and wildcard characters [#251033]({{kib-pull}}251033).
* Aligns APM service navigation in serverless with stateful deployments [#263119]({{kib-pull}}263119).
* Fixes APM routing and settings page navigation [#262723]({{kib-pull}}262723).
* Fixes **Service Map** layout failures when the Dagre rendering algorithm encounters errors [#262240]({{kib-pull}}262240).
* Improves static dashboard selection in the APM **Metrics** tab by incorporating service runtime version into dashboard resolution [#258483]({{kib-pull}}258483).
* Fixes crashes on APM transaction pages for mobile services [#257447]({{kib-pull}}257447).
* Fixes APM waterfall view crashes when Elasticsearch documents are missing optional fields [#257368]({{kib-pull}}257368).
* Fixes APM app crashes caused by invalid `rangeFrom` or `rangeTo` URL query parameter values [#256887]({{kib-pull}}256887).
* Fixes a 500 error on the APM error group details page caused by missing `transaction.sampled` fields [#255788]({{kib-pull}}255788).
* Fixes a crash on the APM service **Metrics** tab caused by a stale `controlGroupState` reference [#254999]({{kib-pull}}254999).
* Fixes trace sample titles in APM from wrapping vertically [#254536]({{kib-pull}}254536).
* Improves the copy displayed when a trace relationship is missing in APM [#251850]({{kib-pull}}251850).
* Fixes the waterfall summary panel width in the Discover traces view [#250556]({{kib-pull}}250556).
* Fixes flyout remounting when switching document types in the Trace Waterfall [#250406]({{kib-pull}}250406).
* Fixes incorrect dependency statistics in the APM **Dependencies** view [#249434]({{kib-pull}}249434).
* Adds a cold start badge to the unified Trace Waterfall to identify slow cold-start spans [#248857]({{kib-pull}}248857).
* Fixes missing service environment values in APM custom links [#248631]({{kib-pull}}248631).
* Prevents nested button rendering in the full traces view in Discover [#247808]({{kib-pull}}247808).
* Fixes missing spans in the traces view in Discover [#247689]({{kib-pull}}247689).
* Fixes trace links that were calculating date ranges incorrectly [#247531]({{kib-pull}}247531).
* Fixes a spurious error rate chart warning on first page load in APM [#247052]({{kib-pull}}247052).
* Adds OTel host metric support to the **Hosts** table [#261564]({{kib-pull}}261564).
* Fixes **Hosts** exclusion filters so hosts with excluded metadata values are no longer shown after enrichment [#260426]({{kib-pull}}260426).
* Fixes **Hosts** filter option suggestions to match the selected schema (ECS or semconv) [#259825]({{kib-pull}}259825).
* Fixes OTel metric mapping in the **Infrastructure** tab so host, pod, and container metrics no longer show `N/A` when data exists [#259552]({{kib-pull}}259552).
* Improves **View details** flyout UI layout [#259428]({{kib-pull}}259428).
* Fixes semconv metric calculations on the **Hosts** page to prevent `N/A` values and align CPU, memory, and disk usage [#259372]({{kib-pull}}259372).
* Fixes asset details locator parameters in custom dashboards [#256412]({{kib-pull}}256412).
* Fixes the dimensions dropdown position when in fullscreen mode [#255049]({{kib-pull}}255049).
* Fixes focus management when entering fullscreen mode in the metrics grid [#254701]({{kib-pull}}254701).
* Updates the Discover metrics flyout to use {{esql}} instead of legacy SQL [#254537]({{kib-pull}}254537).
* Fixes pagination in the dimensions list in the **View details** flyout [#251250]({{kib-pull}}251250).
* Fixes metrics grid panel titles not updating when the panel order changes [#250963]({{kib-pull}}250963).
* Reverts a change that inadvertently removed infrastructure UI custom dashboards [#249973]({{kib-pull}}249973).
* Replaces the custom chart header with the Lens highlight implementation for consistency [#249450]({{kib-pull}}249450).
* Fixes series tooltips not working in fullscreen chart views [#248148]({{kib-pull}}248148).
* Fixes the **Metrics explorer** search bar layout on smaller screen sizes [#246945]({{kib-pull}}246945).
* Adds `maxSize` constraints to unbounded array schemas in rule connector configurations to prevent oversized payloads [#261021]({{kib-pull}}261021).
* Converts the notification policy and alert action API endpoints from internal to public (experimental) [#260510]({{kib-pull}}260510).
* Fixes Index Threshold rule `filterKuery` wildcard behavior on keyword fields so generated queries return the expected matches [#260283]({{kib-pull}}260283).
* Fixes metric threshold rule evaluation for wildcard KQL filters when no data view is available [#260046]({{kib-pull}}260046).
* Fixes alert tags when source tags are provided as a string [#259729]({{kib-pull}}259729).
* Fixes missing action variables in the Slack Web API connector when using text message mode [#259499]({{kib-pull}}259499).
* Fixes custom threshold rules where wildcard filters were not returning results or triggering alerts [#256979]({{kib-pull}}256979).
* Fixes alerts wildcard queries on keyword fields by correctly passing the alerts data view to query building [#255225]({{kib-pull}}255225).
* Falls back to an Elasticsearch API Key when UIAM API Key grant fails for rule execution [#254707]({{kib-pull}}254707).
* Fixes {{esql}} rule execution to correctly handle empty result sets [#250759]({{kib-pull}}250759).
* Fixes {{esql}} rule execution to propagate errors correctly for user-visible error reporting [#250605]({{kib-pull}}250605).
* Fixes KQL autocomplete in the custom threshold rule creation form [#250044]({{kib-pull}}250044).
* Adds no-data behavior options to alert rules for controlling alert behavior when data stops reporting [#247669]({{kib-pull}}247669).
* Fixes the **Related dashboards** tab for Elasticsearch Query rules and other stack rules in Observability [#247564]({{kib-pull}}247564).
* Fixes integration limit enforcement in `parseIntegrationsTSV` to apply after deduplication [#252486]({{kib-pull}}252486).
* Fixes Elastic Agent from incorrectly interpreting JavaScript template literals as policy variables [#247284]({{kib-pull}}247284).
* Fixes minor issues in the Observability onboarding flow [#246208]({{kib-pull}}246208).
* Renames workflow label references to tags throughout the Observability UI for consistency [#260329]({{kib-pull}}260329).
* Fixes crashes caused by malformed URLs in plugins; affected instances now attempt automatic recovery [#257245]({{kib-pull}}257245).
* Fixes dashboard scanning to correctly include sections [#254600]({{kib-pull}}254600).
* Fixes the annotation API on Elastic Serverless [#254285]({{kib-pull}}254285).
* Fixes a race condition in the data quality controller that caused incorrect Discover navigation [#254139]({{kib-pull}}254139).
* Fixes an infinite loading loop in the document flyout when using relative time ranges [#251647]({{kib-pull}}251647).
* Adjusts the panel height in Discover for improved layout [#250778]({{kib-pull}}250778).
* Fixes **View In Context** links in the Discover modal that were not respecting the selected date range [#248939]({{kib-pull}}248939).
* Fixes loss of UI state in signal-specific Discover flyout tabs when refreshing a query [#248203]({{kib-pull}}248203).
* Fixes broken breadcrumbs and sidebar navigation for Data Visualizer and AIOps within solution views [#248167]({{kib-pull}}248167).
* Fixes double scrollbars appearing in fullscreen flyouts [#247744]({{kib-pull}}247744).

## 9.3.8 [elastic-observability-9.3.8-release-notes]

### Features and enhancements [elastic-observability-9.3.8-features-enhancements]
* Adds a defensive check to ensure {{product.apm}} integration policy updates always include API keys in their configuration [#274647]({{kib-pull}}274647).


### Fixes [elastic-observability-9.3.8-fixes]
* Fixes `retest_on_failure: false` being ignored when updating an existing Synthetics monitor through the API [#277701]({{kib-pull}}277701).
* Fixes crashes in the {{apm-app}} caused by missing or malformed URL query parameters [#276420]({{kib-pull}}276420).
* Fixes the **Cases** link in alert details routing to an internal URL instead of the Cases app when accessed from external apps [#275647]({{kib-pull}}275647).
* Fixes the Task Manager API key invalidation task from prematurely invalidating shared API keys still in use by other active tasks [#275157]({{kib-pull}}275157).

## 9.3.7 [elastic-observability-9.3.7-release-notes]

### Features and enhancements [elastic-observability-9.3.7-features-enhancements]
* Adds a defensive check to ensure {{product.apm}} integration policy updates always include API keys in their configuration [#274647]({{kib-pull}}274647).


### Fixes [elastic-observability-9.3.7-fixes]
* Fixes deleted monitor labels from reappearing on the next fetch [#274404]({{kib-pull}}274404).
* Fixes Canvas autoplay from stopping at the first page [#272619]({{kib-pull}}272619).

## 9.3.6 [elastic-observability-9.3.6-release-notes]

### Fixes [elastic-observability-9.3.6-fixes]
* Fixes example log messages in the **Logs → Anomalies** page from overlapping and becoming unreadable [#273221]({{kib-pull}}273221).
* Fixes the **SLO Overview** **No data** tile to correctly count newly created SLOs and SLOs whose summary transform has not yet produced a document [#266315]({{kib-pull}}266315).

## 9.3.5 [elastic-observability-9.3.5-release-notes]

### Fixes [elastic-observability-9.3.5-fixes]
* Fixes the **Hosts** page KPI tiles showing `N/A` and the **Hosts** table displaying stale data when the in-app **Refresh** button is used with a relative time range after the page has been idle [#265515]({{kib-pull}}265515).
* Fixes `too_small` zod error for AI pipeline suggestions with empty string grok patterns [#251113]({{kib-pull}}251113).

## 9.3.4 [elastic-observability-9.3.4-release-notes]

### Features and enhancements [elastic-observability-9.3.4-features-enhancements]
* Defaults new APM alert rules to group by `transaction.name`, providing more granular out-of-the-box alerting for latency threshold, failed transaction rate, and error count rules. Existing rules are unaffected [#261929]({{kib-pull}}261929).

### Fixes [elastic-observability-9.3.4-fixes]
* Fixes an issue where Observability alerts sent recovery notifications but remained `active` in {{kib}} instead of transitioning to `recovered` [#261012]({{kib-pull}}261012).
* Fixes the Serverless APM navigation so **Service inventory** stays active on service map, service groups, and related paths, matching stateful behavior [#263119]({{kib-pull}}263119).
* Fixes the **Hosts** table on the Observability Overview page to display OTel (semconv) host metrics alongside ECS metrics, so hosts ingesting through OpenTelemetry are no longer missing from the table [#261564]({{kib-pull}}261564).
* Fixes an issue where malformed URL query parameters could crash APM and other plugins; affected pages now automatically recover by applying parameter defaults and redirecting to the corrected URL [#257245]({{kib-pull}}257245).

## 9.3.3 [elastic-observability-9.3.3-release-notes]

### Fixes [elastic-observability-9.3.3-fixes]
* Fixes **Hosts** exclusion filters so hosts with excluded metadata values are no longer shown after enrichment [#260426]({{kib-pull}}260426).
* Fixes Index threshold rule `filterKuery` wildcard behavior on keyword fields so generated queries return the expected matches [#260283]({{kib-pull}}260283).
* Fixes metric threshold rule evaluation for wildcard KQL filters when no data view is available, so alerts evaluate correctly [#260046]({{kib-pull}}260046).
* Fixes **Hosts** filter option suggestions to match the selected schema (ECS or semconv) [#259825]({{kib-pull}}259825).
* Fixes alert tags when source tags are provided as a string [#259729]({{kib-pull}}259729).
* Fixes OTel metric mapping in the **Infrastructure** tab so host, pod, and container metrics no longer show `N/A` when data exists [#259552]({{kib-pull}}259552).
* Fixes missing action variables in Slack Web API text message mode [#259499]({{kib-pull}}259499).
* Fixes semconv metric calculations on the **Hosts** page to prevent `N/A` values and align CPU, memory, and disk usage calculations [#259372]({{kib-pull}}259372).
* Improves static dashboard selection in the APM **Metrics** tab by incorporating service runtime version into dashboard resolution [#258483]({{kib-pull}}258483).

## 9.3.2 [elastic-observability-9.3.2-release-notes]


### Features and enhancements [elastic-observability-9.3.2-features-enhancements]
* Adds Gemini 2.5 Flash Lite, Claude 4.5 Haiku, and Claude 4.6 Sonnet preconfigured connectors [#253109]({{kib-pull}}253109).


### Fixes [elastic-observability-9.3.2-fixes]
* Fixes error on burn rate alert details page for suppressed alerts [#256435]({{kib-pull}}256435).
* Fixes asset details locator parameters in custom dashboards [#256412]({{kib-pull}}256412).
* Fixes `Missing required fields (transaction.sampled) in event` error [#255788]({{kib-pull}}255788).
* Fixes alerts wildcard queries on keyword fields [#255225]({{kib-pull}}255225).
* Fixes alert visibility and filters for grouped SLOs on details page [#254601]({{kib-pull}}254601).
* Fixes `scanDashboards` include sections [#254600]({{kib-pull}}254600).

## 9.3.1 [elastic-observability-9.3.1-release-notes]


### Features and enhancements [elastic-observability-9.3.1-features-enhancements]
* Adds error handling to {{observability}} landing page redirect logic [#254171]({{kib-pull}}254171).
* Adds support for ECS formatted errors in service details [#254138]({{kib-pull}}254138).


### Fixes [elastic-observability-9.3.1-fixes]
* Fixes race condition in data quality controller causing incorrect Discover filtering [#254139]({{kib-pull}}254139).
* Fixes toggle state from sticking between monitors in the details flyout [#253314]({{kib-pull}}253314).
* Fixes `too_small` zod error for AI pipeline suggestions with empty string grok patterns [#251113]({{kib-pull}}251113).
* Fixes wildcard and space behavior in SLO filters [#251033]({{kib-pull}}251033).
* Fixes the handling of empty results in ES|QL rule execution [#250759]({{kib-pull}}250759).
* Fixes error handling in `executeEsqlRequest` to propagate ES|QL execution errors [#250605]({{kib-pull}}250605).
* Fixes query sync on save and adds debounce for preview chart [#249833]({{kib-pull}}249833).
* Fixes editing feature of significant event queries [#249716]({{kib-pull}}249716).


## 9.3.0 [elastic-observability-9.3.0-release-notes]

### Features and enhancements [elastic-observability-9.3.0-features-enhancements]

* Adds the math, replace, drop, and convert processors [#246050]({{kib-pull}}246050), [#242310]({{kib-pull}}242310), [#242161]({{kib-pull}}242161), [#240023]({{kib-pull}}240023).
* Adds **Suggest ingest pipeline** feature [#243950]({{kib-pull}}243950).
* Enforces field name spacing in wired streams and detects type mismatches in processor configurations [#244221]({{kib-pull}}244221).
* Allows users to configure Streams visibility on a space-by-space basis [#244285]({{kib-pull}}244285).
* Adds AI pattern suggestions for the Streams dissect processor [#242377]({{kib-pull}}242377).
* Improves processing warnings with truncation logic and wrapped text [#239188]({{kib-pull}}239188).
* Adds support for `geo_point` fields to classic streams [#244356]({{kib-pull}}244356).
* Allows users to add custom description for processors [#243998]({{kib-pull}}243998).
* Adds a tour of the Streams UI [#244808]({{kib-pull}}244808).
* Adds a message to tell users when a stream is missing [#244366]({{kib-pull}}244366).
* Prevents conflicts in **Processing** tab when editing and reordering streams [#244228]({{kib-pull}}244228).
* Adds field type icons to the **Processing** UI [#242134]({{kib-pull}}242134), [#241825]({{kib-pull}}241825).
* Adds timezone and locale parameters to Streamlang [#241369]({{kib-pull}}241369).
* Adds an empty state for **Processing** tab when no data is available [#244893]({{kib-pull}}244893).
* Adds specific error messaging to the Streams schema editor when expensive queries are turned off [#243406]({{kib-pull}}243406).
* Adds autoscroll to **Review partitioning suggestions** panels [#242891]({{kib-pull}}242891).
* Adds space ownership validation for unlink operations, preventing users from unlinking attachments that belong to a different space [#245250]({{kib-pull}}245250).
* Improves Streams attachment filters with multi-type selection, server-side filtering, and suggestions limit [#245248]({{kib-pull}}245248).
* Adds details flyout and improved UX to the Streams attachment feature [#244880]({{kib-pull}}244880).
* Hides document match filter controls in the processing preview for users without manage privileges [#242119]({{kib-pull}}242119).
* Adds messaging to show nested processors and conditions [#240778]({{kib-pull}}240778).
* Adds abort capabilities and silent mode when generating stream descriptions [#247082]({{kib-pull}}247082).
* Allows users to bulk mute and unmute alerts [#245690]({{kib-pull}}245690).
* Adds a **Find Alert Rule Templates** API that shows installed templates in the **Create new rule** modal [#245373]({{kib-pull}}245373).
* Adds a unified rules list [#242208]({{kib-pull}}242208).
* Adds **View in discover** button to alert details for Infrastructure rules [#236880]({{kib-pull}}236880).
* Adds new pre-configured connectors and updates existing ones [#242791]({{kib-pull}}242791).
* Allows users to view and filter by manually added workflow tags [#244251]({{kib-pull}}244251).
* Shows alert workflow tags on the **Overview** tab of the alert details flyout [#246440]({{kib-pull}}246440).
* Adds a warning when deleting API keys currently in use by alerting rules [#243353]({{kib-pull}}243353).
* Allows users to configure custom global ingest pipelines on SLO rollup data [#245025]({{kib-pull}}245025).
* Adds index sorting to SLI index settings [#244978]({{kib-pull}}244978).
* Allows users to view the SLO associated with a burn rate rule from the rule details page [#240535]({{kib-pull}}240535).
* Adds SLO attachments and migrates UI to attachments API [#244092]({{kib-pull}}244092).
* Adds new sub-feature privileges for Synthetics global parameters [#243821]({{kib-pull}}243821).
* Adds badge sync to **Trace timeline** [#246510]({{kib-pull}}246510).
* Adds errors to **Trace timeline** [#245161]({{kib-pull}}245161).
* Replaces current document count chart with RED metrics [#236635]({{kib-pull}}236635).
* Adds **Span links** badge to **Trace timeline** [#244389]({{kib-pull}}244389).
* Adds `deactivate_all_instrumentations`, `deactivate_instrumentations`, `send_logs`, `send_metrics`, and `send_traces` agent configuration settings for EDOT PHP [#246021]({{kib-pull}}246021).
* Adds dashboard suggestions for **ECS**, **K8s**, and **OTel** dashboards when selecting **Pods** in Infra Inventory UI [#245784]({{kib-pull}}245784).
* Ensures Infra Inventory UIs reflect supported schemas [#244481]({{kib-pull}}244481).
* Adds metrics dashboard for non-EDOT agents in the OTEL native ingestion path [#236978]({{kib-pull}}236978).
* Adds `sampling_rate` central configuration to EDOT PHP [#241908]({{kib-pull}}241908).
* Adds `opamp_polling_interval` and `sampling_rate` central configuration to EDOT Node.js [#241048]({{kib-pull}}241048).
* Adds **Edit tags** to alert actions [#243792]({{kib-pull}}243792).
* Adds the **ELSER in EIS** model option for the Observability and Search AI Assistant Knowledge Base [#243298]({{kib-pull}}243298).
* Removes the `AI Assistants Settings` privilege [#239144]({{kib-pull}}239144).
* Observability Agent for Agent Builder is released in 9.3. This includes Observability related tools and AI Insights for alerts, logs in Discover, and errors in APM.
* Adds **Similar errors** section with Occurrences chart [#244665]({{kib-pull}}244665).
* Updates Observability Serverless side navigation [#235984]({{kib-pull}}235984).


### Fixes [elastic-observability-9.3.0-fixes]

* Decouples Streams AI features from the AI Assistant [#242019]({{kib-pull}}242019).
* Fixes stale query value being used when saving significant events and adds debouncing to preview chart [#249833]({{kib-pull}}249833).
* Taking bulk actions on Streams features now requires the `manage` permission [#246129]({{kib-pull}}246129).
* Fixes the simulation of geo points [#241824]({{kib-pull}}241824).
* Fixes processing field name autocomplete that wasn't working on new fields [#246934]({{kib-pull}}246934).
* Turns off geopoint mapping in the processing preview [#245506]({{kib-pull}}245506).
* Fixes manual ingest pipeline script validation [#245439]({{kib-pull}}245439).
* Fixes cell actions populating as undefined with empty cells [#243766]({{kib-pull}}243766).
* Removes mentions of template snippets (mustache templates) from descriptions [#243656]({{kib-pull}}243656).
* Speeds up field simulation [#241313]({{kib-pull}}241313).
* Fixes child stream input validation [#242581]({{kib-pull}}242581).
* Fixes invalid state for wired streams toggle [#241266]({{kib-pull}}241266).
* Fixes wrapping issues in AI suggestions [#240883]({{kib-pull}}240883).
* Fixes related dashboards for ES Query and other stack rules supported in observability [#247564]({{kib-pull}}247564).
* Fixes default alerts flow when default rules are not defined [#245736]({{kib-pull}}245736).
* Adds managed field to `dataViewSpecSchema` [#244134]({{kib-pull}}244134).
* Fixes empty **Related dashboards** menu when linking dashboards to a rule [#243496]({{kib-pull}}243496).
* Prevents default alerts from being created when connectors are not defined [#237504]({{kib-pull}}237504).
* Copies alert states to payload [#240411]({{kib-pull}}240411).
* Replaces metric names inside filter values [#238849]({{kib-pull}}238849).
* Provides users with more granular control over how alerts behave when data stops being reported for metric threshold rules [#247669]({{kib-pull}}247669).
* Reverts show transform errors across all SLO pages [#243013]({{kib-pull}}243013).
* Reverts fix issue where filters do not apply to overview stats [#242978]({{kib-pull}}242978).
* Fixes inconsistent browser back button behavior on SLO page [#242761]({{kib-pull}}242761).
* Fixes layout of the **SLO management** page filters [#239418]({{kib-pull}}239418).
* Excludes stale SLOs from "group by" stats [#240077]({{kib-pull}}240077).
* Fixes alerts being incorrectly triggered when a monitor is down [#237479]({{kib-pull}}237479).
* Creates default rules when creating or editing a monitor, not from navigation-based events [#245441]({{kib-pull}}245441).
* Uses monitor query id for project monitors package policies [#248762]({{kib-pull}}248762).
* Fixes duplicate test results on monitor status heatmap [#248761]({{kib-pull}}248761).
* Fixes validation error with maintenance windows on lightweight Synthetics monitors [#247880]({{kib-pull}}247880).
* Fixes console state from persisting across journey steps [#247376]({{kib-pull}}247376).
* Fixes Elastic Agent from interpreting JS template literals as policy variables  [#247284]({{kib-pull}}247284).
* Fixes Synthetics tasks to only update relevant monitors when maintenance windows exist [#246088]({{kib-pull}}246088).
* Turns off max attempts for the private locations sync task [#237784]({{kib-pull}}237784).
* Fixes creating and updating private location monitors [#238326]({{kib-pull}}238326).
* Fixes the icon in the "Elastic documentation not available" callout in AI Assistant settings [#247885]({{kib-pull}}247885).
* Fixes issue with the `Authorization` header when  making calls through the {{kib}} tool [#244017]({{kib-pull}}244017).
* Updates system prompt title for generic deployments [#243266]({{kib-pull}}243266).
* Fixes the AI Assistant button tooltip from persisting when not being hovered over [#237202]({{kib-pull}}237202).
* Fixes error when the AI Assistant is off [#238811]({{kib-pull}}238811).
* Fixes Knowledge base model label in the AI Assistant settings [#239824]({{kib-pull}}239824).
* Fixes Kibana tool from failing when using a proxy [#236653]({{kib-pull}}236653).
* Fixes overlapping components in the Observability AI Assistant flyout on small screens [#241026]({{kib-pull}}241026).
* Fixes error handling for tool response [#241425]({{kib-pull}}241425).
* Fixes **AI Assistant visibility** setting syncing issues [#239555]({{kib-pull}}239555).
* Updates the AI agent used for Observability AI insights [#249776]({{kib-pull}}249776).
* Fixes alias resolution when checking lock index mappings [#244559]({{kib-pull}}244559).
* Adds `maxQueue` backpressure to anonymization regex worker pool [#249108]({{kib-pull}}249108).
* Fixes ES|QL query execution timeout issues[#238200]({{kib-pull}}238200).
* Fixes handling of missing `error.id` [#243638]({{kib-pull}}243638).
* Hides non-trace services in **Service Inventory** and **Service Map** [#241080]({{kib-pull}}241080), [#240104]({{kib-pull}}240104).
* Updates `useAnyOfApmParams` to include mobile services [#237500]({{kib-pull}}237500).
* Fixes dependencies and service map for `txn == exit-span` use cases [#235392]({{kib-pull}}235392).
* Fixes AI insights with fallback message fields [#243437]({{kib-pull}}243437).
* Fixes missing service environment in custom links [#248631]({{kib-pull}}248631).
* Updates the **Open in Discover** query in the **Related logs** section of the **Overview** tab [#240409]({{kib-pull}}240409).
* Fixes missing spans in discover traces view [#247689]({{kib-pull}}247689).
* Fixes **Trace timeline** tests [#247252]({{kib-pull}}247252).
* Fixes traces duplicate spans in Discover [#244984]({{kib-pull}}244984).
* Fixes trace links calculating date range incorrectly [#247531]({{kib-pull}}247531).
* Fixes error rate chart warning on first load [#247052]({{kib-pull}}247052).
* Fixes broken links from **View In Context** Discover modal [#248939]({{kib-pull}}248939).
* Fixes loss of UI state in signal-specific Discover fly-out tabs when refreshing a query [#248203]({{kib-pull}}248203).
* Fixes **Metrics explorer** search bar issue on some screen sizes [#246945]({{kib-pull}}246945).
* Replaces `host.hostname` with `host.name` in Infrastructure tab [#246386]({{kib-pull}}246386).
* Fixes charts not filtering by `host.name` [#242673]({{kib-pull}}242673).
* Removes filtering capabilities in host metrics [#239724]({{kib-pull}}239724).
* Fixes broken metadata filtering when typing "OR" in host flyouts [#233836]({{kib-pull}}233836).
* Fixes CPU query by changing the gap policy to include zeros [#239596]({{kib-pull}}239596).
* Fixes the incorrectly formatted **Values** dropdown in Storybook [#241812]({{kib-pull}}241812).
* Escapes special characters when creating ES|QL query for Lens charts [#241662]({{kib-pull}}241662).
* Adds missing transaction action links [#241336]({{kib-pull}}241336).
* Updates metrics experience API routes to delegate authorization to Elasticsearch [#241195]({{kib-pull}}241195).
* Fixes error when clearing custom link filters [#241164]({{kib-pull}}241164).
* Improves metrics profile resolution by removing index pattern and time series validation [#241047]({{kib-pull}}241047).
* Fixes KPIs subtitle logic [#243217]({{kib-pull}}243217).
* Fixes JVM metric conflicts with explicit cast [#244151]({{kib-pull}}244151).
* Removes unnecessary `_source` from queries [#239205]({{kib-pull}}239205).
* Fixes onboarding issues [#246208]({{kib-pull}}246208).
* Adds **Background Search** to the ECH Observability navigation menu [#237494]({{kib-pull}}237494).
* Aligns **Members** link across solutions [#240992]({{kib-pull}}240992).
* Fixes icon colors for navigation menu [#237970]({{kib-pull}}237970).
* Fixes gap while loading data [#238879]({{kib-pull}}238879).
* Fixes **Dataset Quality** flyout rendering [#237840]({{kib-pull}}237840).

## 9.2.8 [elastic-observability-9.2.8-release-notes]

### Features and enhancements [elastic-observability-9.2.8-features-enhancements]
* Adds no-data behavior options to custom threshold rules, including options to recover, remain active, or trigger a no-data alert [#251976]({{kib-pull}}251976).


### Fixes [elastic-observability-9.2.8-fixes]
* Fixes **Hosts** exclusion filters by applying post-enrichment filtering to excluded metadata values [#260426]({{kib-pull}}260426).
* Fixes **Hosts** filter option suggestions to match the selected schema (ECS or semconv) [#259825]({{kib-pull}}259825).
* Fixes alert tags when source tags are provided as a string [#259729]({{kib-pull}}259729).
* Fixes OTel metric mapping in the **Infrastructure** tab so host, pod, and container metrics no longer show `N/A` when data exists [#259552]({{kib-pull}}259552).
* Fixes semconv metric calculations on the **Hosts** page to prevent `N/A` values and align CPU, memory, and disk usage calculations [#259372]({{kib-pull}}259372).

## 9.2.7 [elastic-observability-9.2.7-release-notes]


### Fixes [elastic-observability-9.2.7-fixes]
* Fixes error on burn rate alert details page for suppressed alerts [#256435]({{kib-pull}}256435).
* Fixes `Missing required fields (transaction.sampled) in event` error [#255788]({{kib-pull}}255788).
* Fixes alerts wildcard queries on keyword fields [#255225]({{kib-pull}}255225).
* Fixes alert visibility and filters for grouped SLOs on details page [#254601]({{kib-pull}}254601).

## 9.2.6 [elastic-observability-9.2.6-release-notes]

### Features and enhancements [elastic-observability-9.2.6-features-enhancements]
* Adds error handling to {{observability}} landing page redirect logic [#254171]({{kib-pull}}254171).
* Adds support for ECS-formatted errors in service details [#254138]({{kib-pull}}254138).


### Fixes [elastic-observability-9.2.6-fixes]
* Fixes toggle state from sticking between monitors in the details flyout [#253314]({{kib-pull}}253314).
* Fixes wildcard and space behavior in SLO filters [#251033]({{kib-pull}}251033).

## 9.2.5 [elastic-observability-9.2.5-release-notes]


### Fixes [elastic-observability-9.2.5-fixes]
* Fixes incorrect dependencies stats [#249434]({{kib-pull}}249434).
* Adds `maxQueue` backpressure to anonymization regex worker pool [#249108]({{kib-pull}}249108).
* Fixes broken links from **View In Context** Discover modal [#248939]({{kib-pull}}248939).
* Uses monitor query id for project monitors package policies [#248762]({{kib-pull}}248762).
* Fixes an issue where synthetics test results showed up as duplicated on the monitor status heat map, for higher granularity columns [#248761]({{kib-pull}}248761).
* Fixes loss of UI state in signal-specific Discover fly-out tabs when refreshing a query [#248203]({{kib-pull}}248203).
* Fixes missing spans in Discover's traces view [#247689]({{kib-pull}}247689).
* Adds more granular control over how alerts behave when data stops being reported for metric threshold rules [#247669]({{kib-pull}}247669).
* Fixes Synthetics tasks to only update relevant monitors when maintenance windows exist [#246088]({{kib-pull}}246088).
*

## 9.2.4 [elastic-observability-9.2.4-release-notes]


### Fixes [elastic-observability-9.2.4-fixes]
* Fixes the icon in the "Elastic documentation not available" callout in AI Assistant Settings [#247885]({{kib-pull}}247885).
* Fixes validation error with maintenance windows on lightweight Synthetics monitors [#247880]({{kib-pull}}247880).
* Fixes related dashboards for ES Query and other stack rules supported in Observability [#247564]({{kib-pull}}247564).
* Fixes console state from persisting across journey steps [#247376]({{kib-pull}}247376).
* Fixes Elastic Agent from interpreting JS template literals as policy variables  [#247284]({{kib-pull}}247284).
* Fixes Synthetics tasks to only update relevant monitors when maintenance windows exist [#246088]({{kib-pull}}246088).
* Fixes default alerts flow from breaking when default rules are not defined [#245736]({{kib-pull}}245736).
* Fixes error handling for tool response [#241425]({{kib-pull}}241425).

## 9.2.3 [elastic-observability-9.2.3-release-notes]

### Features and enhancements [elastic-observability-9.2.3-features-enhancements]
* Adds a message to tell users when a stream is missing [#244366]({{kib-pull}}244366).
* Adds a warning when deleting API keys that are currently in use by alerting rules [#243353]({{kib-pull}}243353).
* Shows supported schemas in the Infrastructure inventory [#244481]({{kib-pull}}244481).


### Fixes [elastic-observability-9.2.3-fixes]
* Fixes alias resolution when checking lock index mappings [#244559]({{kib-pull}}244559).
* Adds managed field to `dataViewSpecSchema` [#244134]({{kib-pull}}244134).
* Removes mentions of template snippets from descriptions [#243656]({{kib-pull}}243656).

## 9.2.2 [elastic-observability-9.2.2-release-notes]

### Features and enhancements [elastic-observability-9.2.2-features-enhancements]
* Adds new sub-feature privileges for Synthetics global parameters [#243821]({{kib-pull}}243821).

### Fixes [elastic-observability-9.2.2-fixes]
* Fixes issue with the `Authorization` header when  making calls through the {{kib}} tool [#244017]({{kib-pull}}244017).
* Stops UI from breaking when the `error.id` field is missing [#243638]({{kib-pull}}243638).
* Updates system prompt title for generic deployments [#243266]({{kib-pull}}243266).
* Fixes KPIs subtitle logic [#243217]({{kib-pull}}243217).
* Reverts the PR that introduced transform errors across all SLO pages [#243013]({{kib-pull}}243013).
* Reverts the "Fix issue where filters do not apply to overview stats" PR [#242978]({{kib-pull}}242978).
* Fixes charts not filtering by `host.name` [#242673]({{kib-pull}}242673).
* Fixes issue with custom links clearing filter views when a new field is selected or deleted [#241164]({{kib-pull}}241164).
* Fixes CPU query by changing the gap policy to include zeros [#239596]({{kib-pull}}239596).

## 9.2.1 [elastic-observability-9.2.1-release-notes]

### Fixes [elastic-observability-9.2.1-fixes]
* Fixes simulation of geo points in Streams [#241824]({{kib-pull}}241824).
* Speeds up field simulation in Streams [#241313]({{kib-pull}}241313).
* Fixes the incorrectly formatted **Values** dropdown in Storybook [#241812]({{kib-pull}}241812).
* Escapes special characters when creating ES|QL query for Lens charts [#241662]({{kib-pull}}241662).
* Hides non-trace services in **Service Inventory** and **Service Map** [#241080]({{kib-pull}}241080), [#240104]({{kib-pull}}240104).


## 9.2.0 [elastic-observability-9.2.0-release-notes]

### Features and enhancements[elastic-observability-9.2.0-features]

* Lets you create routing conditions directly from preview table in Streams. [#235560]({{kib-pull}}235560).
* Allows Streams users to manually map new fields from the **Schema** tab [#235919]({{kib-pull}}235919).
* Adds AI suggestion partitioning to Streams [#235759]({{kib-pull}}235759).
* Improves processing warnings in Streams [#239188]({{kib-pull}}239188).
* Adds ingest pipeline processor template suggestions to the Streams manual ingest pipeline processor editor [#236919]({{kib-pull}}236919).
* Add triple quotes support to the Streams manual ingest pipeline processor editor [#236595]({{kib-pull}}236595).
* Adds persistent field mappings for Streams processors [#233799]({{kib-pull}}233799).
* Updates the Observability navigation menu [#233784]({{kib-pull}}233784), [#236808]({{kib-pull}}236808).
* Adds functional tests for Logs Essentials tier to cover tier-specific behavior [#234904]({{kib-pull}}234904).
* Enables Observability onboarding Playwright tests for the Logs Essentials tier [#234644]({{kib-pull}}234644).
* Adds **View in Discover** to the alerts details page for Synthetics Monitor Status and TLS alert rules. [#234104]({{kib-pull}}234104).
* Adds **View in discover** to the alerts details page for SLO burn rate and ES query rules [#233855]({{kib-pull}}233855).
* Adds **View in discover** button to alert details header [#233259]({{kib-pull}}233259).
* Adds time range filter to links from alert details to related dashboards [#230601]({{kib-pull}}230601).
* Adds rules callout in metric, logs, and inventory rules [#237085]({{kib-pull}}237085).
* Enables filters and saved queries in custom threshold rules [#229453]({{kib-pull}}229453).
* Adds option to recover alerts when the monitor is back up or when the condition is no longer met. [#229962]({{kib-pull}}229962).
* Adds the **Trace timeline** to Discover flyout [#234072]({{kib-pull}}234072).
* Adds `send_traces`, `send_metrics`, and `send_logs` agent configuration settings for EDOT Node.js [#233798]({{kib-pull}}233798).
* Shows errors in context of traces [#234178]({{kib-pull}}234178)
* Adds option to link dashboards to SLOs [#233265]({{kib-pull}}233265).
* Adds dashboard references to SLO saved objects [#232583]({{kib-pull}}232583).
* Adds dashboard tags for linked dashboards and suggested dashboards on the alert details page's **Related dashboards** tab [#228902]({{kib-pull}}228902).
* Fetches referenced panels when fetching dashboards [#228811]({{kib-pull}}228811).
* Moves the installation settings for AI Assistant's Knowledge Base and Product Docs components into a single location [#232559]({{kib-pull}}232559), [#228695]({{kib-pull}}228695).
* Makes AI Assistant aware of LLM-facing documentation for integrations installed in your cluster [#237085]({{kib-pull}}237085).
* Adds `raw_request` to traces for `.gen-ai`, `.gemini`, and `.bedrock` connectors [#232229]({{kib-pull}}232229).
* Adds manual test for bulk import functionality for AI Assistant [#225497]({{kib-pull}}225497).
* Improves the AI Assistant Settings page by updating the logos to be solution-specific [#224906]({{kib-pull}}224906).
* Adds native function calling schema change to the OpenAI connector when the API provider is set to `other` [#232097]({{kib-pull}}232097).
* Adds native function calling for self-managed LLMs [#232109]({{kib-pull}}232109).
* Improves Gemini prompts [#223476]({{kib-pull}}223476).
* Adds **GenAI Settings** to **Stack management** [#227289]({{kib-pull}}227289).
* Moves the **AI Assistant visibility** setting to **GenAI Settings** page [#233727]({{kib-pull}}233727).
* Adds UI tests to validate the onboarding page [#232363]({{kib-pull}}232363).
* Shows span links when APM indices are available [#232135]({{kib-pull}}232135).
* Adds error count and badge and support for span types to trace samples [#227413]({{kib-pull}}227413) [#227208]({{kib-pull}}227208).
* Disables add-to-case functionality when all selected alerts are already added to a case [#231877]({{kib-pull}}231877).
* Allows users to paste screenshots into markdown comment fields for cases [#226077]({{kib-pull}}226077).
* Extracts case observables automatically when attaching alerts to a case [#233027]({{kib-pull}}233027).
* Allows attaching any event to a case, not only alert events [#230970]({{kib-pull}}230970).
* Adds `opamp_polling_interval` and `sampling_rate` to central config for EDOT application agents [#231835]({{kib-pull}}231835).
* Adds `kibana.alert.grouping` field to Synthetics monitor status rule [#230513]({{kib-pull}}230513).
* Adds a public endpoint for manually testing synthetic monitors [#227760]({{kib-pull}}227760).
* Adds error param to agent config API [#230298]({{kib-pull}}230298).
* Creates an API to detect existing schemas [#226597]({{kib-pull}}226597).
* Adds option to the shared logs overview to see all available log events even when ML features are not available [#225785]({{kib-pull}}225785).

### Fixes [elastic-observability-9.2.0-fixes]

* Fixes layout of SLO management page combo box filter [#239418]({{kib-pull}}239418).
* Fixes icon colors for navigation menu [#237970]({{kib-pull}}237970).
* Updates `useAnyOfApmParams` to include mobile services [#237500]({{kib-pull}}237500).
* Adds background search to Observability navigation [#237494]({{kib-pull}}237494).
* Fixes the multiselect issue inside the toolbar selector when search is used [#237494]({{kib-pull}}237494).
* Fixes the page height of the AI Assistant page [#233924]({{kib-pull}}233924).
* Fixes knowledge base model label in AI Assistant settings [#239824]({{kib-pull}}239824).
* Fixes **Show alert details** actions button [#233113]({{kib-pull}}233113).
* Fixes `get_alerts_dataset_info` to fail completely if any parallel `select_relevant_fields` request fails [#232281]({{kib-pull}}232281).
* Adjusts Kubernetes OTel test to work in serverless nightly workflow [#231462]({{kib-pull}}231462).
* Fixes title generation for conversations in the Observability AI Assistant with self-managed LLMs  [#231198]({{kib-pull}}231198).
* Fixes inventory date picker state [#231141]({{kib-pull}}231141).
* Enables recovery strategy switch for monitor status rules [#231091]({{kib-pull}}231091).
* Includes `ContentManagement` plugin to allow linked dashboards [#237085]({{kib-pull}}229685).
* Improves performance of clustering [#238394]({{kib-pull}}238394).
* Fixes multiselect issue in Discover toolbar [#236091]({{kib-pull}}236091).
* Improves accessibility for Streams badges [#235625]({{kib-pull}}235625).
* Fixes code area responsiveness in Stream management [#232630]({{kib-pull}}232630).

## 9.1.10 [elastic-observability-9.1.10-release-notes]


### Features and enhancements [elastic-observability-9.1.10-features-enhancements]
* Adds API to enable auto-syncing of global parameters to private locations [#239284]({{kib-pull}}239284).


### Fixes [elastic-observability-9.1.10-fixes]
* Fixes validation error with maintenance windows on lightweight Synthetics monitors [#247880]({{kib-pull}}247880).
* Fixes related dashboards for ES Query and other stack rules supported in Observability [#247564]({{kib-pull}}247564).
* Fixes console state from persisting across journey steps [#247376]({{kib-pull}}247376).
* Fixes Elastic Agent from interpreting JS template literals as policy variables [#247284]({{kib-pull}}247284).
* Fixes Synthetics tasks to only update relevant monitors when maintenance windows exist [#246088]({{kib-pull}}246088).
* Fixes trace links to correctly calculate date range [#247531]({{kib-pull}}247531).

## 9.1.9 [elastic-observability-9.1.9-release-notes]

### Features and enhancements [elastic-observability-9.1.9-features-enhancements]
*  Adds a warning when deleting API keys that are currently in use by alerting rules [#243353]({{kib-pull}}243353).

### Fixes [elastic-observability-9.1.9-fixes]
* Fixes alias resolution when checking lock index mappings [#244559]({{kib-pull}}244559).

## 9.1.8 [elastic-observability-9.1.8-release-notes]

### Features and enhancements [elastic-observability-9.1.8-features-enhancements]
* Adds new sub-feature privileges for Synthetics global parameters [#243821]({{kib-pull}}243821).

### Fixes [elastic-observability-9.1.8-fixes]
* Stops UI from breaking when the `error.id` field is missing [#243638]({{kib-pull}}243638).
* Reverts the PR that introduced transform errors across all SLO pages [#243013]({{kib-pull}}243013).
* Fixes issue with custom links clearing filter views when a new field is selected or deleted [#241164]({{kib-pull}}241164).
* Fixes CPU query by changing the gap policy to include zeros [#239596]({{kib-pull}}239596).

## 9.1.7 [elastic-observability-9.1.7-release-notes]

### Fixes [elastic-observability-9.1.7-fixes]
* Adds missing transaction action links [#241336]({{kib-pull}}241336).
* Fixes overlapping components in the Observability AI Assistant flyout on small screens [#241026]({{kib-pull}}241026).
* Excludes stale SLOs from "group by" stats [#240077]({{kib-pull}}240077).
* Fixes Kibana tool from failing when using a proxy [#236653]({{kib-pull}}236653).
* Hides non-trace services in **Service Inventory** and **Service Map** [#241080]({{kib-pull}}241080), [#240104]({{kib-pull}}240104).

## 9.1.6 [elastic-observability-9.1.6-release-notes]

### Fixes [elastic-observability-9.1.6-fixes]

* Fixes layout of SLO management page combo box filter [#239418]({{kib-pull}}239418).
* Removes {{es}} `_sources` from query responses [#239205]({{kib-pull}}239205).
* Fixes rule condition chart parser replacing metric names in filter values [#238849]({{kib-pull}}238849).
* Fixes creating and updating private location monitors [#238326]({{kib-pull}}238326).
* Disables max attempts for the private locations sync task [#237784]({{kib-pull}}237784).
* Fixes `useAnyOfApmParams` to include mobile services [#237500]({{kib-pull}}237500).
* Fixes a bug with Synthetics alerting where a down monitor triggered recovered alerts when it shouldn't [#237479]({{kib-pull}}237479).
* Fixes the AI Assistant button tooltip by closing the tooltip when the button is not being hovered over [#237202]({{kib-pull}}237202).

## 9.1.5 [elastic-observability-9.1.5-release-notes]

### Features and enhancements[elastic-observability-9.1.5-features]

* Allows implementation of a default LLM connector from settings [#236103]({{kib-pull}}236103).

### Fixes [elastic-observability-9.1.5-fixes]

* Removes span documents from `getServiceAgent` function [#236732]({{kib-pull}}236732).
* Removes incorrect `fleet.ssl` configuration [#236788]({{kib-pull}}236788).
* Fixes malformed synthetics package policies [#236176]({{kib-pull}}236176).
* Reverts filter policy inputs [#236104]({{kib-pull}}236104).
* Removes extra synthetics package policies [#235200]({{kib-pull}}235200).

## 9.1.4 [elastic-observability-9.1.4-release-notes]

### Enhancements [elastic-observability-9.1.4-enhancements]

* Save button is disabled in user-specific system prompt flyout when there's no input [#233184]({{kib-pull}}233184).


## 9.1.3 [elastic-observability-9.1.3-release-notes]

### Fixes [elastic-observability-9.1.3-fixes]

* Fixes Synthetics monitor filters [#231562]({{kib-pull}}231562).

## 9.1.2 [elastic-observability-9.1.2-release-notes]

### Fixes [elastic-observability-9.1.2-fixes]

* Fixes lock manager setup bug [#230519]({{kib-pull}}230519).
* Adds timestamp range filter to exclude frozen tier [#230375]({{kib-pull}}230375).
* Adjusts end-to-end onboarding tests to work in serverless environment [#229969]({{kib-pull}}229969).

## 9.1.1 [elastic-observability-9.1.1-release-notes]

### Fixes [elastic-observability-9.1.1-fixes]

* Fixes global parameters sync for non-default private locations [#230157]({{kib-pull}}230157).

## 9.1.0 [elastic-observability-9.1.0-release-notes]

### Features and enhancements[elastic-observability-9.1.0-features]

* Adds the anonymization advanced setting for Observability AI Assistant [#224607]({{kib-pull}}224607).
* Allows users to change the Knowledge Base model post-installation in AI Assistant Settings [#221319]({{kib-pull}}221319).
* Adds ELSER and e5 on EIS [#220993]({{kib-pull}}220993).
* Only shows ELSER in EIS if the pre-configured endpoint is available [#220096]({{kib-pull}}220096).
* Allows users to specify a Knowledge Base model to support non-English languages [#218448]({{kib-pull}}218448).
* Allows users to archive conversations with the AI Assistant [#216012]({{kib-pull}}216012).
* Allows users to share AI Assistant conversations [#211854]({{kib-pull}}211854).
* Adds accordion sections for the **Attributes** tables [#224185]({{kib-pull}}224185).
* Allows users to add the APM trace waterfall to other solutions [#216098]({{kib-pull}}216098).
* Adds the **History** tab view for calendar-based SLOs to the SLO details page [#223825]({{kib-pull}}223825).
* Allows users to view definitions, delete SLOs, and purge SLI data from a single page, without needing to consider instances [#222238]({{kib-pull}}222238).
* Adds the **Definition** tab to SLO pages [#212826]({{kib-pull}}212826).
* Adds suggested dashboards to alerts [#223424]({{kib-pull}}223424).
* Adds the **Add to case** button to alerts [#223184]({{kib-pull}}223184).
* Allows users to save `group by` information with dynamic mapping for custom threshold rules [#219826]({{kib-pull}}219826).
* Allows users to link dashboards in **Rules** and **Alerts** pages [#219019]({{kib-pull}}219019).
* Allows users to add an investigation guide to alert **Details** pages [#217106]({{kib-pull}}217106).
* Adds KQL filter to TLS alerting rule [#215110]({{kib-pull}}215110).
* Adds the `context.grouping` action variable in SLO burn rate and {{es}} query rules [#213550]({{kib-pull}}213550).
* Adds the `context.grouping` action variable in custom threshold and APM rules [#212895]({{kib-pull}}212895).
* Allows users to generate an alert for each row in query results in the {{es}} query {{esql}} rule [#212135]({{kib-pull}}212135).
* Adds filter controls on Observability **Alerts** pages [#198495]({{kib-pull}}198495).
* Adds support for maintenance windows in Synthetics [#222174]({{kib-pull}}222174).
* Allows users to choose the spaces where Synthetics monitors are available [#221568]({{kib-pull}}221568).
* Allows users to rename private location labels and tags in Synthetics [#221515]({{kib-pull}}221515).
* Adds monitor downtime alert when Synthetics monitor has no data [#220127]({{kib-pull}}220127).
* Adds a compact view to the Synthetics **Overview** page [#219060]({{kib-pull}}219060).
* Adds drilldown functionality to Synthetics stats overview embeddable [#217688]({{kib-pull}}217688).
* Adds failure store metrics to the **Data Set Quality** page [#220874]({{kib-pull}}220874).
* Adds support for span links in the service map [#215645]({{kib-pull}}215645).
* Adds support for `GroupStreamDefinition` to `/api/streams` endpoints [#208126]({{kib-pull}}208126).
* Submits a comment in cases by pressing **+ Enter** [#228473]({{kib-pull}}228473).
* Updates SLO starter prompt [#224493]({{kib-pull}}224493).
* Integrates new tail sampling settings [#224479]({{kib-pull}}224479).
* Gets model ID from anonymization rules [#224280]({{kib-pull}}224280).
* Prefer `observabilityAIAssistantAPIClient` over supertest [#222753]({{kib-pull}}222753).
* Updates system prompt to inform about anonymization [#224211]({{kib-pull}}224211).
* Adds investigation guide empty state [#223974]({{kib-pull}}223974).
* Adds anonymization support [#223351]({{kib-pull}}223351).
* Remove `semantic_text` migration [#220886]({{kib-pull}}220886)
* Remaps `iInCircle` and `questionInCircle` and deprecates `help` icon [#223142]({{kib-pull}}223142).
* Shows cases on alert detail overview [#222903]({{kib-pull}}222903).
* Removes is_correction and confidence attributes from knowledge base entry [#222814]({{kib-pull}}222814).
* Refetches alert detail rule data on edit flyout submit [#222118]({{kib-pull}}222118).
* Adds new rule form to the **Create rule** flyout [#206685]({{kib-pull}}206685)
* Updates spec.max to 3.4 [#221544]({{kib-pull}}221544).
* Adds EDOT logging level to central config [#219722]({{kib-pull}}219722).
* Adds 'logging_level' agent configuration setting for EDOT Node.js [#222883]({{kib-pull}}222883).
* Adds 'deactivate_...' agent configuration settings for EDOT Node.js [#224502]({{kib-pull}}224502)
* Removes metrics and logs from get_service_stats API [#218346]({{kib-pull}}218346).
* Adds **Logs** tab to mobile services [#209944]({{kib-pull}}209944)
* Removes double confirmation when deleting conversation [#217991]({{kib-pull}}217991).
* Updates 790 deployment environment discrepancy [#217899]({{kib-pull}}217899).
* Adds embeddable Trace Waterfall Enhancements [#217679]({{kib-pull}}217679).
* Returns 404 if `screenshot_ref` only when truly not present [#215241]({{kib-pull}}215241).
* Adds the ability to create an APM availability or latency SLO for all services [#214653]({{kib-pull}}214653).
* Handle `ELASTIC_PROFILER_STACK_TRACE_IDS` for `apm-profiler` integration [#217020]({{kib-pull}}217020)
* Includes `spaceID` in SLI documents [#214278]({{kib-pull}}214278).
* Updates delete confirmation modal [#212695]({{kib-pull}}212695).
* Enables syntax highlighting for {{esql}} [#212669]({{kib-pull}}212669).
* Shows dashboards with different ingest path on runtime metrics [#211822]({{kib-pull}}211822).
* Adds the ability for a user to create an API Key in Synthetics settings that applies only to specified spaces [#211816]({{kib-pull}}211816).
* Enables editing central config for EDOT Agents and SDKs [#211468]({{kib-pull}}211468).
* Adds the reason message to the rules recovery context [#211411]({{kib-pull}}211411).
* Removes enablement check in `PUT /api/streams/{id}` for classic streams [#212289]({{kib-pull}}212289).
* Uses bulk endpoint to import knowledge base entries [#222084]({{kib-pull}}222084).
* Changes embeddable view when only one monitor if one location is selected [#218402]({{kib-pull}}218402).
* Improves how related alerts are suggested [#215673]({{kib-pull}}215673).
* Updates handling of duplicate conversations in the AI Assistant[#208044]({{kib-pull}}208044).
* Indicates when failure store is not enabled for a data stream [#221644]({{kib-pull}}221644).

### Fixes [elastic-observability-9.1.0-fixes]

* Fixes for `metric_item` component [#227969]({{kib-pull}}227969).
* Fixes incorrect rendering of statistics in **TransactionsTable** [#227494]({{kib-pull}}227494).
* Injects user prompt before tool call when query actions are clicked [#227462]({{kib-pull}}227462).
* Fixes editing of private location with no monitors assigned [#227411]({{kib-pull}}227411).
* Fixes missing sparklines from **Dependencies** table [#227211]({{kib-pull}}227211).
* Shows tool validation error when processing a Gemini stream finishes with `MALFORMED_FUNCTION_CALL` [#227110]({{kib-pull}}227110).
* Makes Uptime available in stack solution view when enabled [#226999]({{kib-pull}}226999).
* Fixes product docs installation status [#226919]({{kib-pull}}226919).
* Fixes embeddings model dropdown with legacy endpoint on upgrade [#226878]({{kib-pull}}226878).
* Fixes the EIS callout being cut off for large font sizes [#226633]({{kib-pull}}226633).
* Fixes response handling of get_apm_dependencies tool call [#226601]({{kib-pull}}226601).
* Fixes span flyout in operation page [#226423]({{kib-pull}}226423).
* Collapses `*query` tool calls [#226078]({{kib-pull}}226078).
* Fixes broken operation page [#226036]({{kib-pull}}226036).
* Limits environment name length when creating Machine Learning jobs [#225973]({{kib-pull}}225973).
* Fixes schema page [#225481]({{kib-pull}}225481).
* Hides settings from Serverless navigation [#225436]({{kib-pull}}225436).
* Fixes **Agent Explorer** page [#225071]({{kib-pull}}225071).
* Adds query rewriting [#224498]({{kib-pull}}224498).
* Fixes SLO federated view bug when listed remote clusters and index name exceed 4096 bytes [#224478]({{kib-pull}}224478).
* Returns suggested dashboards only for custom threshold alerts [#224458]({{kib-pull}}224458).
* Fixes broken EDOT JVM metrics dashboard when classic agent metrics are present [#224052]({{kib-pull}}224052).
* Uses bulk helper for bulk importing knowledge base entries [#223526]({{kib-pull}}223526).
* Removes `run soon` for private location sync task [#222062]({{kib-pull}}222062).
* Adjusts example to NDJSON format [#221617]({{kib-pull}}221617).
* Prevents non-aggregatable messages from showing if no data matches [#221599]({{kib-pull}}221599).
* Deletes user instruction if text is empty [#221560]({{kib-pull}}221560).
* Checks for documents before starting semantic text migration [#221152]({{kib-pull}}221152).
* Hides data set details when `dataStream` comes from a remote cluster [#220529]({{kib-pull}}220529).
* Makes API tests more resilient [#220503]({{kib-pull}}220503).
* Removes index write blocks [#220362]({{kib-pull}}220362).
* Receives `aria-labelledby` from Elastic Charts svg [#220298]({{kib-pull}}220298).
* Queries alerts using the `alert.start` field and updates alerts function API test to check alert information [#219651]({{kib-pull}}219651).
* Fixes Alerts environment query follow up [#219571]({{kib-pull}}219571).
* Prevents flyout mode from opening on mount [#219420]({{kib-pull}}219420).
* Changes the alerts query to include environment not defined value [#219228]({{kib-pull}}219228).
* Disables using logical `AND` when filter is removed [#218910]({{kib-pull}}218910).
* Ensures index templates are created [#218901]({{kib-pull}}218901).
* Uses fields instead of `_source` in the metadata endpoint [#218869]({{kib-pull}}218869).
* Fixes span url link when transactionId missing in span Links [#218232]({{kib-pull}}218232).
* Fixes Bedrock error when displaying results and visualize query [#218213]({{kib-pull}}218213).
* Makes create annotations from keyboard navigable [#217918]({{kib-pull}}217918).
* Fixes EDOT error summary [#217885]({{kib-pull}}217885).
* Removes direct function calling from the chat input [#217359]({{kib-pull}}217359).
* Adds error text in environment filter when input is invalid [#216782]({{kib-pull}}216782).
* Changes "TPM" abbreviation to trace per minute for screen-readers [#216282]({{kib-pull}}216282).
* Fixes waterfall margin left position [#216229]({{kib-pull}}216229).
* Fixes fold/unfold button in traces waterfall explorer not clickable [#216972]({{kib-pull}}216972)
* Adds `aria-label` to transaction type select on service overview [#216014]({{kib-pull}}216014).
* Uses `nameTooltip` api for dependencies tables [#215940]({{kib-pull}}215940).
* Fixes page height of the AI Assistant app in solution views [#215646]({{kib-pull}}215646).
* Only allow `.ndjson` files when bulk importing to the knowledge base [#215433]({{kib-pull}}215433).
* Removes unnecessary field service.environment from top dependency spans endpoint [#215321]({{kib-pull}}215321).
* Updates retrieve_elastic_doc api test [#215237]({{kib-pull}}215237).
* Fixes id overflow [#215199]({{kib-pull}}215199).
* Fixes contextual insights scoring [#214259]({{kib-pull}}214259).
* Updates knowledge base installation flow [#214133]({{kib-pull}}214133).
* Always shows inspect configuration button [#213619]({{kib-pull}}213619).
* Fixes failing test in Observability stack deployments `Deployment-agnostic A…` [#213530]({{kib-pull}}213530).
* Fixes conversation tests [#213338]({{kib-pull}}213338).
* Fixes sorting in profiler storage explorer [#212583]({{kib-pull}}212583).
* Adds system message in copy conversation JSON payload [#212009]({{kib-pull}}212009).
* Removed unnecessary breadcrumbs in Universal Profiling [#211081]({{kib-pull}}211081).
* Added minHeight to profiler flamegraphs [#210443]({{kib-pull}}210443).
* Adds system message [#209773]({{kib-pull}}209773).
* Ensures that when an SLO is created, the ID is verified across all spaces [#214496]({{kib-pull}}214496).
* Fixes the **Outcome Preview** table so columns always fill the page width after a resize in **Streams** [#226000]({{kib-pull}}226000).
* Adds discernible text for the **Refresh data preview** button in **Streams** [#225816]({{kib-pull}}225816).
* Ensures the members array is unique for `GroupStreamDefinitions` in **Streams** [#210089]({{kib-pull}}210089).
* Applies chunking algorithm for `getIndexBasicStats` in Dataset Health [#221153]({{kib-pull}}221153).
* Improves finding functions in Universal Profiling [#210437]({{kib-pull}}210437).
* Adds logical `AND` to monitor tags and locations filter [#217985]({{kib-pull}}217985).

## 9.0.8 [elastic-observability-9.0.8-release-notes]

### Features and enhancements[elastic-observability-9.0.8-features]
* Allows implementation of a default LLM connector from settings [#236103]({{kib-pull}}236103).

### Fixes [elastic-observability-9.0.8-fixes]
* Removes span documents from `getServiceAgent` function [#236732]({{kib-pull}}236732).

## 9.0.7 [elastic-observability-9.0.7-release-notes]

### Features and enhancements[elastic-observability-9.0.7-features]
There are no user-facing changes in the 9.0.7 release.

## 9.0.6 [elastic-observability-9.0.6-release-notes]

### Fixes [elastic-observability-9.0.6-fixes]
* Fixes AI Assistant for Observability settings to only show for Enterprise users [#231989]({{kib-pull}}231989).

## 9.0.5 [elastic-observability-9.0.5-release-notes]

### Features and enhancements[elastic-observability-9.0.5-features]
* Submit a comment in a case by pressing `ctrl/cmd` + `enter` [#228473]({{kib-pull}}228473).

### Fixes [elastic-observability-9.0.5-fixes]
* Instructs AI Assistant not to perform destructive actions [#229497]({{kib-pull}}229497).
* Fixes service error for table column sorting [#229199]({{kib-pull}}229199).
* Fixes Dependencies inventory page issue where loading spinner spins indefinitely when no data exists [#228094]({{kib-pull}}228094).

## 9.0.4 [elastic-observability-9.0.4-release-notes]

### Fixes [elastic-observability-9.0.4-fixes]

* Fixes missing sparklines in the Dependencies table in the APM UI [#227211]({{kib-pull}}227211).
* Fixes legacy Uptime monitoring UI not showing when turned on [#226999]({{kib-pull}}226999).
* Fixes response handling of `get_apm_dependencies` tool call [#226601]({{kib-pull}}226601).
* Fixes query function calls when using Claude LLM [#226078]({{kib-pull}}226078).
* Fixes Agent Explorer boundary errors  [#225071]({{kib-pull}}225071).
* Fixes broken EDOT JVM metrics dashboard when classic APM agent metrics are present [#224052]({{kib-pull}}224052).

## 9.0.3 [elastic-observability-9.0.3-release-notes]

### Enhancements [elastic-observability-9.0.3-features-enhancements]

* Improve the system prompt and instructions for working with Claude models [#221965]({{kib-pull}}221965).

### Fixes [elastic-observability-9.0.3-fixes]

* Tool instructions are no longer shown in the system message when tools are disabled [#223278]({{kib-pull}}223278).

## 9.0.2 [elastic-observability-9.0.2-release-notes]

### Enhancements [elastic-observability-9.0.2-features-enhancements]

* Enhanced the handling of missing `service.environment` attributes [#217899]({{kib-pull}}217899).

### Fixes [elastic-observability-9.0.2-fixes]

* Fixes issue with updating SLOs created in a version later than 8.18 that were failing due to an invalid ingest pipeline [#221158]({{kib-pull}}221158).
* Fixes `error_marker.tsx` to support mobile-services [#220424]({{kib-pull}}220424).
* Fixes alerts environment query follow up [#219571]({{kib-pull}}219571).
* Fixes the alerts query to include "environment not defined" value [#219228]({{kib-pull}}219228).

## 9.0.1 [elastic-observability-9.0.1-release-notes]

### Fixes [elastic-observability-9.0.1-fixes]
* Fixes an error that prevented query results from displaying and visualizing correctly in Bedrock [#218213]({{kib-pull}}218213)

## 9.0.0 [elastic-observability-9.0.0-release-notes]

### Features and enhancements [elastic-observability-9.0.0-features-enhancements]
* Improves SLO navigation by separating details from the overview panel [#212826]({{kib-pull}}212826)
* Enables the new Borealis theme [#210468]({{kib-pull}}210468)
* Returns a 404 response only when the `screenshot_ref` is truly missing [#215241]({{kib-pull}}215241)
* Includes the `spaceId` field in Service Level Indicator (SLI) documents [#214278]({{kib-pull}}214278)
* Includes the recovery reason message in the rule context [#211411]({{kib-pull}}211411)
* Enhances Synthetic SLOs by adding location context and correcting badge link behavior [#210695]({{kib-pull}}210695)
* Updates the default sampling frequency to 19Hz [#202278]({{kib-pull}}202278)

### Fixes [elastic-observability-9.0.0-fixes]
* Resolves an issue that prevented the chat feature from functioning correctly on the Alerts page [#197126]({{kib-pull}}197126)
* Addresses a missing versioning issue in `inventory_view_saved_object` that could prevent the Observability Infrastructure Inventory view from loading post-upgrade [#207007]({{kib-pull}}207007)
* Enables the use of wildcard filters in SLO queries [#213119]({{kib-pull}}213119)
* Updates the `Close project` navigation label to `Log out` to better reflect the intended action for users in serverless environments [#211463]({{kib-pull}}211463)
* Fixes an issue where clicking a name badge for a synthetics monitor led to a page that failed to load monitor details [#210695]({{kib-pull}}210695)
* Fixes code scanning alert no. 456: Incomplete string escaping or encoding [#193909]({{kib-pull}}193909)
* Fixes code scanning alert: Incomplete string escaping or encoding [#193365]({{kib-pull}}193365)
