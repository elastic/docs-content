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

## 9.1.0 [elastic-observability-9.1.0-release-notes]

### Features [elastic-observability-9.1.0-features]

* Adds the anonymization advanced setting for Observability AI Assistant ({kibana-pull}224607[#224607]).
* Allows users to change the Knowledge Base model post-installation in AI Assistant Settings. ({kibana-pull}221319[#221319]).
* Adds ELSER and e5 on EIS ({kibana-pull}220993[#220993]).
* Only shows ELSER in EIS if the pre-configured endpoint is available ({kibana-pull}220096[#220096]).
* Allows users to specify a Knowledge Base model to support non-English languages ({kibana-pull}218448[#218448]).
* Allows users to archive conversations with the AI Assistant ({kibana-pull}216012[#216012]).
* Allows users to share AI Assistant conversations ({kibana-pull}211854[#211854]).
* Adds accordion sections for the **Attributes** tables ({kibana-pull}224185[#224185]).
* Allows users to add the APM trace waterfall to other solutions ({kibana-pull}216098[#216098]).
* Adds the **History** tab view for calendar-based SLOs to the SLO details page ({kibana-pull}223825[#223825]).
* Allows users to view definitions, delete SLOs, and purge SLI data from a single page, without needing to consider instances ({kibana-pull}222238[#222238]).
* Adds the **Definition** tab to SLO pages ({kibana-pull}212826[#212826]).
* Adds suggested dashboards to alerts ({kibana-pull}223424[#223424]).
* Adds the **Add to case** button to alerts ({kibana-pull}223184[#223184]).
* Allows users to save `group by` information with dynamic mapping for custom threshold rules ({kibana-pull}219826[#219826]).
* Allows users to link dashboards in **Rules** and **Alerts** pages ({kibana-pull}219019[#219019]).
* Allows users to add an investigation guide to alert **Details** pages ({kibana-pull}217106[#217106]).
* Adds KQL filter to TLS alerting rule ({kibana-pull}215110[#215110]).
* Adds the `context.grouping` action variable in SLO burn rate and ES query rules ({kibana-pull}213550[#213550]).
* Adds the `context.grouping` action variable in custom threshold and APM rules ({kibana-pull}212895[#212895]).
* Allows users to generate an alert for each row in query results in the ES query ES|QL rule ({kibana-pull}212135[#212135]).
* Adds filter controls on Observability **Alerts** pages ({kibana-pull}198495[#198495]).
* Adds support for maintenance windows in Synthetics ({kibana-pull}222174[#222174]).
* Allows users to choose the spaces where Synthetics monitors are available ({kibana-pull}221568[#221568]).
* Allows users to rename private location labels and tags in Synthetics ({kibana-pull}221515[#221515]).
* Adds monitor downtime alert when Synthetics monitor has no data ({kibana-pull}220127[#220127]).
* Adds a compact view to the Synthetics **Overview** page ({kibana-pull}219060[#219060]).
* Adds drilldown functionality to Synthetics stats overview embeddable ({kibana-pull}217688[#217688]).
* Adds failure store metrics to the **Data Set Quality** page ({kibana-pull}220874[#220874]).
* Adds support for span links in the service map ({kibana-pull}215645[#215645]).
* Adds support for `GroupStreamDefinition` to `/api/streams` endpoints ({kibana-pull}208126[#208126]).

### Enhancements [elastic-observability-9.1.0-enhancements]

* Submits a comment in cases by pressing **+ Enter** ({kibana-pull}228473[#228473]).
* Updates SLO starter prompt ({kibana-pull}224493[#224493]).
* Integrates new tail sampling settings ({kibana-pull}224479[#224479]).
* Gets model ID from anonymization rules ({kibana-pull}224280[#224280]).
* Updates system prompt to inform about anonymization ({kibana-pull}224211[#224211]).
* Adds investigation guide empty state ({kibana-pull}223974[#223974]).
* Adds anonymization support ({kibana-pull}223351[#223351]).
* Remaps `iInCircle` and `questionInCircle` and deprecates `help` icon ({kibana-pull}223142[#223142]).
* Shows cases on alert detail overview ({kibana-pull}222903[#222903]).
* Removes is_correction and confidence attributes from knowledge base entry ({kibana-pull}222814[#222814]).
* Refetches alert detail rule data on edit flyout submit ({kibana-pull}222118[#222118]).
* Updates spec.max to 3.4 ({kibana-pull}221544[#221544]).
* Adds EDOT logging level to central config ({kibana-pull}219722[#219722]).
* Removes metrics and logs from get_service_stats API ({kibana-pull}218346[#218346]).
* Removes double confirmation when deleting conversation ({kibana-pull}217991[#217991]).
* Updates 790 deployment environment discrepancy ({kibana-pull}217899[#217899]).
* Adds embeddable Trace Waterfall Enhancements ({kibana-pull}217679[#217679]).
* Returns 404 if `screenshot_ref` only when truly not present ({kibana-pull}215241[#215241]).
* Adds the ability to create an APM availability or latency SLO for all services ({kibana-pull}214653[#214653]).
* Includes `spaceID` in SLI documents ({kibana-pull}214278[#214278]).
* Updates delete confirmation modal ({kibana-pull}212695[#212695]).
* Enables syntax highlighting for ES|QL ({kibana-pull}212669[#212669]).
* Shows dashboards with different ingest path on runtime metrics ({kibana-pull}211822[#211822]).
* Adds the ability for a user to create an API Key in Synthetics settings that applies only to specified spaces ({kibana-pull}211816[#211816]).
* Enables editing central config for EDOT Agents and SDKs ({kibana-pull}211468[#211468]).
* Adds the reason message to the rules recovery context ({kibana-pull}211411[#211411]).
* Removes enablement check in `PUT /api/streams/{id}` for classic streams ({kibana-pull}212289[#212289]).
* Uses bulk endpoint to import knowledge base entries ({kibana-pull}222084[#222084]).
* Changes embeddable view when only one monitor if one location is selected ({kibana-pull}218402[#218402]).
* Improves how related alerts are suggested ({kibana-pull}215673[#215673]).
* Updates handling of duplicate conversations in hte AI Assistant({kibana-pull}208044[#208044]).
* Indicates when failure store is not enabled for a data stream [#221644]({kibana-pull}221644).

### Fixes [elastic-observability-9.1.0-fixes]

* Fixes for `metric_item` component ({kibana-pull}227969[#227969]).
* Fixes incorrect rendering of statistics in **TransactionsTable** ({kibana-pull}227494[#227494]).
* Injects user prompt before tool call when query actions are clicked ({kibana-pull}227462[#227462]).
* Fixes editing of private location with no monitors assigned ({kibana-pull}227411[#227411]).
* Fixes missing sparklines from **Dependencies** table ({kibana-pull}227211[#227211]).
* Shows tool validation error when processing a Gemini stream finishes with `MALFORMED_FUNCTION_CALL` ({kibana-pull}227110[#227110]).
* Makes Uptime available in stack solution view when enabled ({kibana-pull}226999[#226999]).
* Fixes product docs installation status ({kibana-pull}226919[#226919]).
* Fixes embeddings model dropdown with legacy endpoint on upgrade ({kibana-pull}226878[#226878]).
* Fixes the EIS callout being cut off for large font sizes ({kibana-pull}226633[#226633]).
* Fixes response handling of get_apm_dependencies tool call ({kibana-pull}226601[#226601]).
* Fixes span flyout in operation page ({kibana-pull}226423[#226423]).
* Collapses `*query` tool calls ({kibana-pull}226078[#226078]).
* Fixes broken operation page ({kibana-pull}226036[#226036]).
* Limits environment name length when creating Machine Learning jobs ({kibana-pull}225973[#225973]).
* Fixes schema page ({kibana-pull}225481[#225481]).
* Hides settings from Serverless navigation ({kibana-pull}225436[#225436]).
* Fixes **Agent Explorer** page ({kibana-pull}225071[#225071]).
* Adds query rewriting ({kibana-pull}224498[#224498]).
* Fixes SLO federated view bug when listed remote clusters and index name exceed 4096 bytes ({kibana-pull}224478[#224478]).
* Returns suggested dashboards only for custom threshold alerts ({kibana-pull}224458[#224458]).
* Fixes broken EDOT JVM metrics dashboard when classic agent metrics are present ({kibana-pull}224052[#224052]).
* Uses bulk helper for bulk importing knowledge base entries ({kibana-pull}223526[#223526]).
* Removes `run soon` for private location sync task ({kibana-pull}222062[#222062]).
* Adjusts example to NDJSON format ({kibana-pull}221617[#221617]).
* Prevents non-aggregatable messages from showing if no data matches ({kibana-pull}221599[#221599]).
* Deletes user instruction if text is empty ({kibana-pull}221560[#221560]).
* Checks for documents before starting semantic text migration ({kibana-pull}221152[#221152]).
* Hides data set details when `dataStream` comes from a remote cluster ({kibana-pull}220529[#220529]).
* Makes API tests more resilient ({kibana-pull}220503[#220503]).
* Removes index write blocks ({kibana-pull}220362[#220362]).
* Receives `aria-labelledby` from Elastic Charts svg ({kibana-pull}220298[#220298]).
* Queries alerts using the `alert.start` field and updates alerts function API test to check alert information ({kibana-pull}219651[#219651]).
* Fixes Alerts environment query follow up ({kibana-pull}219571[#219571]).
* Prevents flyout mode from opening on mount ({kibana-pull}219420[#219420]).
* Changes the alerts query to include environment not defined value ({kibana-pull}219228[#219228]).
* Disables using logical `AND` when filter is removed ({kibana-pull}218910[#218910]).
* Ensures index templates are created ({kibana-pull}218901[#218901]).
* Uses fields instead of `_source` in the metadata endpoint ({kibana-pull}218869[#218869]).
* Fixes span url link when transactionId missing in span Links ({kibana-pull}218232[#218232]).
* Fixes Bedrock error when displaying results and visualize query ({kibana-pull}218213[#218213]).
* Makes create annotations from keyboard navigable ({kibana-pull}217918[#217918]).
* Fixes EDOT error summary ({kibana-pull}217885[#217885]).
* Removes direct function calling from the chat input ({kibana-pull}217359[#217359]).
* Adds error text in environment filter when input is invalid ({kibana-pull}216782[#216782]).
* Changes "TPM" abbreviation to trace per minute for screen-readers ({kibana-pull}216282[#216282]).
* Fixes waterfall margin left position ({kibana-pull}216229[#216229]).
* Adds `aria-label` to transaction type select on service overview ({kibana-pull}216014[#216014]).
* Uses `nameTooltip` api for dependencies tables ({kibana-pull}215940[#215940]).
* Fixes page height of the AI Assistant app in solution views ({kibana-pull}215646[#215646]).
* Only allow `.ndjson` files when bulk importing to the knowledge base ({kibana-pull}215433[#215433]).
* Removes unnecessary field service.environment from top dependency spans endpoint ({kibana-pull}215321[#215321]).
* Updates retrieve_elastic_doc api test ({kibana-pull}215237[#215237]).
* Fixes id overflow ({kibana-pull}215199[#215199]).
* Fixes contextual insights scoring ({kibana-pull}214259[#214259]).
* Updates knowledge base installation flow ({kibana-pull}214133[#214133]).
* Always shows inspect configuration button ({kibana-pull}213619[#213619]).
* Fixes failing test in Observability stack deployments `Deployment-agnostic A…` ({kibana-pull}213530[#213530]).
* Fixes conversation tests ({kibana-pull}213338[#213338]).
* Fixes sorting in profiler storage explorer ({kibana-pull}212583[#212583]).
* Adds system message in copy conversation JSON payload ({kibana-pull}212009[#212009]).
* Removed unnecessary breadcrumbs in Universal Profiling ({kibana-pull}211081[#211081]).
* Added minHeight to profiler flamegraphs ({kibana-pull}210443[#210443]).
* Adds system message ({kibana-pull}209773[#209773]).
* Ensures that when an SLO is created, the ID is verified across all spaces ({kibana-pull}214496[#214496]).
* Fixes the **Outcome Preview** table so columns always fill the page width after a resize in **Streams** ({kibana-pull}226000[#226000]).
* Adds discernible text for the **Refresh data preview** button in **Streams** ({kibana-pull}225816[#225816]).
* Ensures the members array is unique for `GroupStreamDefinitions` in **Streams** ({kibana-pull}210089[#210089]).
* Applies chunking algorithm for `getIndexBasicStats` in Dataset Health ({kibana-pull}221153[#221153]).
* Improves finding functions in Universal Profiling ({kibana-pull}210437[#210437]).
* Adds logical `AND` to monitor tags and locations filter ({kibana-pull}217985[#217985]).

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