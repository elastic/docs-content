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

## 9.1.6 [elastic-observability-9.1.6-release-notes]

### Fixes [elastic-observability-9.1.6-fixes]

* Fixes layout of SLO management page combo box filter [#239418]({{kib-pull}}239418).
* Removes {{es}} `_sources` from query responses [#239205]({{kib-pull}}239205).
* Fixes rule condition chart parser replacing metric names in filter values [#238849]{{kib-pull}}(238849).
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
