---
navigation_title: "Elastic Cloud Serverless"
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/serverless-changelog.html
---

# {{serverless-full}} changelog [elastic-cloud-serverless-changelog]
Review the changes, fixes, and more to {{serverless-full}}.

For {{serverless-full}} API changes, refer to [APIs Changelog](https://www.elastic.co/docs/api/changes).

% Release notes include only features, enhancements, and fixes. Add breaking changes, deprecations, and known issues to the applicable release notes sections.

% ## version.next [elastic-cloud-serverless-changelog-releasedate]

% ### Features and enhancements [elastic-cloud-serverless-releasedate-features-enhancements]

% ### Fixes [elastic-cloud-serverless-releasedate-fixes]

## April 21, 2025 [serverless-changelog-04212025]

### Fixes [serverless-changelog-04212025-fixes]
* Fixes prebuilt rules force upgrade on Elastic Security Serverless Endpoint policy creation [#217959]({{kib-pull}}217959) 
* Fixes related integrations render performance on Elastic Security Serverless rule editing pages [#217254]({{kib-pull}}217254)

## April 14, 2025 [serverless-changelog-04142025]

### Features and enhancements [serverless-changelog-04142025-features-enhancements]
* Enables archiving of conversations in the Elastic Observability Serverless AI Assistant [#216012]({{kib-pull}}216012)
* Moves job and trained model management features into **Stack Management** [#204290]({{kib-pull}}204290)
* Adds Engine initialization API to Elastic Security Serverless [#215663]({{kib-pull}}215663)
* Allows creating an ES|QL control by entering a question mark (`?`) in the query [#216839]({{kib-pull}}216839)
* Improves UI handling of multiple CVEs and package fields [#216411]({{kib-pull}}216411)
* Adds support for Windows MSI commands for Fleet and Elastic Agent installations [#217217]({{kib-pull}}217217)
* Reuses shared integration policies when duplicating agent policies in Fleet [#217872]({{kib-pull}}217872)
* Enables adding badges to all list items in the side navigation except the section header [#217301]({{kib-pull}}217301)

### Fixes [serverless-changelog-04142025-fixes]
* Fixes error message when previewing index templates used by data streams [#217604]({{kib-pull}}217604)
* Wraps text in search bars [#217556]({{kib-pull}}217556)
* Adds support for `textBased` layers in ES|QL visualizations [#216358]({{kib-pull}}216358)
* Corrects the alert count displayed in **Monitor** details [#216761]({{kib-pull}}216761)
* Fixes the **Save visualization** action on the Monitors **Overview** tab [#216695]({{kib-pull}}216695)
* Removes direct function calling from the chat input Elastic Observability Serverless AI Assistant [#217359]({{kib-pull}}217359)
* Adds missing `aria-label` attributes to some buttons under the Services and Services Groups pages [#217325]({{kib-pull}}217325)
* Improves knowledge base installation flow and inference endpoint management [#214133]({{kib-pull}}214133)
* Improves `aria-label` for `EuiCodeBlock` on the APM onboarding page [#217292]({{kib-pull}}217292)
* Adds `source` and `target` fields to the `Dataset Quality Navigated` event [#217575]({{kib-pull}}217575)
* Improves `aria-label` attributes for latency correlations [#217512]({{kib-pull}}217512)
* Fixes navigation to the **Search Connectors** page [#217749]({{kib-pull}}217749)
* Sorts the **Environment** dropdown alphabetically in the APM UI [#217710]({{kib-pull}}217710)
* Ensures the Request Inspector shows accurate request and response data for successful scenarios [#216519]({{kib-pull}}216519)
* Fixes the `Change Point Detection` embeddable in dashboards [#217178]({{kib-pull}}217178)
* Fixes page crashes caused by the **Use full data** button [#217291]({{kib-pull}}217291)
* Filters inference connectors that lack existing endpoints in **Connectors** [#217641]({{kib-pull}}217641)
* Fixes focusability and keyboard access issues with the **Export** tab in the **Share this dashboard** modal [#217313]({{kib-pull}}217313)

## April 7, 2025 [serverless-changelog-04072025]

### Features and enhancements [elastic-cloud-serverless-04072025-features-enhancements]

* Adds keyboard navigation for drag-and-drop interactions in Dashboards [#208286]({{kib-pull}}208286)
* Adds 'Read More' and 'Read Less' functionality to fields in Document view in Discover [#215326]({{kib-pull}}215326)
* Injects and extracts tag references in Dashboards [#214788]({{kib-pull}}214788)
* Adds an option to User Settings that allows the Kibana interface to display in a high contrast mode [#216242]({{kib-pull}}216242)
* Adds a back external link indicator to the side navigation [#215946]({{kib-pull}}215946)
* Adds a default metrics dashboard for Node.js open telemetry in Elastic Observability Serverless [#215735]({{kib-pull}}215735)
* Replaces Sourcerer with the the Discover Data View picker in Elastic Security Serverless [#210585]({{kib-pull}}210585)
* Replaces Sourcerer in the global header in Elastic Security Serverless [#216685]({{kib-pull}}216685)
* Handles grouping in multivalue fields in Elastic Security Serverless [#215913]({{kib-pull}}215913)
* Adds validation and autocomplete support for the `CHANGE_POINT` command in {{esql}} [#216043]({{kib-pull}}216043)
* Adds support for aggregrate filtering in the {{esql}} editor [#216379]({{kib-pull}}216379)
* Changes the agent details last activity value to show the formatted datetime in Fleet [#215531]({{kib-pull}}215531)
* Allows SSL configuration to be disabled for the Fleet agent Logstash output [#216216]({{kib-pull}}216216)
* Enhances the display for anomaly time function values for Machine Learning [#216142]({{kib-pull}}216142)
* Adds Voyage AI and DeepSeek icons for Machine Learning [#216651]({{kib-pull}}216651)
* Moves rule settings to a flyout instead of a modal [#216162]({{kib-pull}}216162)


### Fixes [elastic-cloud-serverless-04072025-fixes]
* Fixes a race condition in `useBatchedPublishingSubjects` in Dashboards and visualizations [#216399]({{kib-pull}}216399)
* Fixes State being dropped when editing visualize embeddables in Dashboards and visualizations [#216901]({{kib-pull}}216901)
* Updates the HTTP API response from 201 to 200 in Dashboards and visualizations [#217054]({{kib-pull}}217054)
* Fixes an issue where scaling edits weren't saved in Dashboards and visualizations [#217235]({{kib-pull}}217235)
* Fixes an issue where the Discover flyout closed when the focus was on filter [#216630]({{kib-pull}}216630)
* Fixes the CSV export for {{esql}} embeddable in Discover [#216325]({{kib-pull}}216325)
* Fixes the JSON view for {{esql}} record in DocViewer [#216642]({{kib-pull}}216642)
* Adds items count to fields accordion titled `aria-label` in Discover  [#216993]({{kib-pull}}216993)
* Makes service inventory icons visible if the `agentName` is returned in Elastic Observability Serverless [#216220]({{kib-pull}}216220)
* Changes the TPM abbreviation to trace per minute for screen readers in Elastic Observability Serverless [#216282]({{kib-pull}}216282)
* Adds the `aria-label` to the fold traces button in Elastic Observability Serverless [#216485]({{kib-pull}}216485)
* Adds the `aria-label` to the technical preview badge in Elastic Observability Serverless [#216483]({{kib-pull}}216483)
* Allows only `.ndjson` files when bulk importing to the knowledge base in Elastic Observability Serverless [#215433]({{kib-pull}}215433)
* Fixes the span link invalid filter in Elastic Observability Serverless [#215322]({{kib-pull}}215322)
* Fixes the missing URL in the transaction summary in Elastic Observability Serverless [#215397]({{kib-pull}}215397)
* Fixes the query for transaction marks in Elastic Observability Serverless [#215819]({{kib-pull}}215819)
* Updates the `retrieve_elastic_doc` API test in Elastic Observability Serverless [#215237]({{kib-pull}}215237)
* Adds error text in the environment filter when the input is invalid in Elastic Observability Serverless [#216782]({{kib-pull}}216782)
* Fixes the **Fold/unfold** button in traces waterfall explorer in Elastic Observability Serverless [#216972]({{kib-pull}}216972)
* Fixes the alert severity order in Elastic Security Serverless [#215813]({{kib-pull}}215813)
* Fixes the error callout placement on the **Entity Store** page's **Engine Status** tab in Elastic Security Serverless [#216228]({{kib-pull}}216228)
* Reads `config` from preconfigured connectors in AI Assistant and Attack Discovery in Elastic Security Serverless [#216700]({{kib-pull}}216700)
* Fixes bedrock `modelId` encoding in Elastic Security Serverless [#216915]({{kib-pull}}216915)
* Fixes the AI Assistant prompt in Elastic Security Serverless [#217058]({{kib-pull}}217058)
* Hides "not" operators from the suggestions menu in {{esql}} [#216355]({{kib-pull}}216355)
* Fixes the CSV report time range when exporting from Discover in {{esql}} [#216792]({{kib-pull}}216792)
* Fixes unenroll inactive agent tasks if the first set of agents returned is equal to `UNENROLLMENT_BATCH_SIZE` in Fleet [#216283]({{kib-pull}}216283)
* Supports integrations having secrets with multiple values in Fleet [#216918]({{kib-pull}}216918)
* Adds overlay to the add/edit integration page in Fleet [#217151]({{kib-pull}}217151)


## March 31, 2025 [serverless-changelog-03312025]

### Features and enhancements [elastic-cloud-serverless-03312025-features-enhancements]
* Introduced an embeddable trace waterfall visualization in Elastic Observability Serverless [#216098]({{kib-pull}}216098)
* Adds support for span links in Elastic Observability Serverless service maps [#215645]({{kib-pull}}215645)
* Enables KQL filting for TLS alerting rules in Elastic Observability Serverless [#215110]({{kib-pull}}215110)
* Ensures a 404 response is returned only when `screenshot_ref` is truly missing in Elastic Observability Serverless [#215241]({{kib-pull}}215241)
* Adds a rule gaps histogram to the Elastic Security Serverless rules dashboard [#214694]({{kib-pull}}214694)
* Adds support for multiple CVEs and improves the vulnerability data grid, flyout, and contextual flyout UI in Elastic Security Serverless [#213039]({{kib-pull}}213039)
* Updates API key permissions for refreshing data view API for Elastic Security Serverless [#215738]({{kib-pull}}215738)
* Adds the ability to limit notes per document instead of globally in Elastic Security Serverless [#214922]({{kib-pull}}214922)
* Adds the ability to add badges to subitems in the side navigation [#214854]({{kib-pull}}214854)


### Fixes [elastic-cloud-serverless-03312025-fixes]
* Fixes color palette assignment issues in partition charts [#215426]({{kib-pull}}215426)
* Adjusts page height for the AI Assistant app in solution views [#215646]({{kib-pull}}215646)
* Adds the `aria-label` to latency selector in Elastic Observabiity Serverless service overview [#215644]({{kib-pull}}215644)
* Adds the `aria-label` to popover service in Elastic Observabiity Serverless service overview [#215640]({{kib-pull}}215640)
* Adds the `aria-label` to "Try our new inventory" button in Elastic Observabiity Serverless [#215633]({{kib-pull}}215633)
* Adds the `aria-label` to Transaction type select in Elastic Observabiity Serverless service overview [#216014]({{kib-pull}}216014)
* Fixes an issue when selecting monitor frequency [#215823]({{kib-pull}}215823)
* Implements the `nameTooltip` API for Elastic Observabiity Serverless dependency tables [#215940]({{kib-pull}}215940)
* Fixes a location filter issue in the Elastic Observabiity Serverless status rule executor [#215514]({{kib-pull}}215514)
* Consolidates custom Fleet onboarding logic in Elastic Observabiity Serverless [#215561]({{kib-pull}}215561)
* Fixes left margin positioning in Elastic Observabiity Serverless waterfall visualizations [#216229]({{kib-pull}}216229)
* Corrects risk score table refresh issues in the Elastic Security Serverless Entity Analytics Dashboard [#215472]({{kib-pull}}215472)
* Fixes the Elastic Security Serverless host details flyout left panel tabs [#215672]({{kib-pull}}215672)
* Fixes an issue where the Entity Store init API did not check for index privileges in Elastic Security Serverless [#215329]({{kib-pull}}215329)
* Adds a `manage_ingest_pipeline` privilege check for Risk Engine enablement in Elastic Security Serverless [#215544]({{kib-pull}}215544)
* Updates API to dynamically retrieve `spaceID` for Elastic Security Serverless [#216063]({{kib-pull}}216063)
* Fixes the visibility of the {{esql}} date picker [#214728]({{kib-pull}}214728)
* Enables the {{esql}} time picker when time parameters are used with `cast` [#215820]({{kib-pull}}215820)
* Updates the Fleet minimum package spec version to 2.3 [#214600]({{kib-pull}}214600)
* Fixes text overflow and alignment in agent details integration input status in Fleet [#215807]({{kib-pull}}215807)
* Fixes pagination in the Anomaly Explorer Anomalies Table for Machine Learning [#214714]({{kib-pull}}214714)
* Ensures proper permissions for viewing Machine Learning nodes [#215503]({{kib-pull}}215503)
* Adds a custom link color option for the top banner [#214241]({{kib-pull}}214241)
* Updates the task state version after execution [#215559]({{kib-pull}}215559)


## March 24, 2025 [serverless-changelog-03242025]

### Features and enhancements [elastic-cloud-serverless-0324025-features-enhancements] 
* Enables smoother scrolling in Kibana [#214512]({{kib-pull}}214512)
* Adds `context.grouping` action variable in Custom threshold and APM rules [#212895]({{kib-pull}}212895)
* Adds the ability to create an APM availability or latency SLO for all services [#214653]({{kib-pull}}214653)
* Enables editing central config for EDOT Agents / SDKs [#211468]({{kib-pull}}211468)
* Uses Data View name for Rule Data View display [#214495]({{kib-pull}}214495)
* Highlights the code examples in our inline docs [#214915]({{kib-pull}}214915)
* Updates data feeds for anomaly detection jobs to exclude Elastic Agent and Beats processes [#213927]({{kib-pull}}213927)
* Adds Mustache lambdas for alerting action [#213859]({{kib-pull}}213859)
* Adds 'page reload' screen reader warning [#214822]({{kib-pull}}214822)

### Fixes [elastic-cloud-serverless-03242025-fixes]
* Fixes color by value for Last value array mode [#213917]({{kib-pull}}213917)
* Fixes can edit check [#213887]({{kib-pull}}213887)
* Fixes opening a rollup data view in Discover [#214656]({{kib-pull}}214656)
* Fixes entry item in waterfall shouldn't be orphan [#214700]({{kib-pull}}214700)
* Filters out upstream orphans in waterfall [#214704]({{kib-pull}}214704)
* Fixes KB bulk import UI example [#214970]({{kib-pull}}214970)
* Ensures that when an SLO is created, its ID is verified across all spaces [#214496]({{kib-pull}}214496)
* Fixes contextual insights scoring [#214259]({{kib-pull}}214259)
* Prevents `getChildrenGroupedByParentId` from including the parent in the children list [#214957]({{kib-pull}}214957)
* Fixes ID overflow bug [#215199]({{kib-pull}}215199)
* Removes unnecessary `field service.environment` from top dependency spans endpoint [#215321]({{kib-pull}}215321)
* Fixes missing `user_agent` version field and shows it on the trace summary [#215403]({{kib-pull}}215403)
* Fixes rule preview works for form's invalid state [#213801]({{kib-pull}}213801)
* Fixes session view error on the alerts tab [#214887]({{kib-pull}}214887)
* Adds index privileges check to `applyDataViewIndices` [#214803]({{kib-pull}}214803)
* Changes the default Risk score lookback period from `30m` to `30d` [#215093]({{kib-pull}}215093)
* Fixes issue with alert grouping re-render [#215086]({{kib-pull}}215086)
* Limits the `transformID` length to 36 characters [#213405]({{kib-pull}}213405)
* Fixes Data view refresh not supporting the `indexPattern` parameter [#215151]({{kib-pull}}215151)
* Uses Risk Engine `SavedObject` intead of `localStorage` on the Risk Score web page [#215304]({{kib-pull}}215304)
* Fixes autocomplete for comments when there is a space [#214696]({{kib-pull}}214696)
* Makes sure that the variables in the editor are always up to date [#214833]({{kib-pull}}214833)
* Calculates the query for retrieving the values correctly [#214905]({{kib-pull}}214905)
* Fixes overlay in integrations on mobile [#215312]({{kib-pull}}215312)
* Fixes chart in single metric anomaly detection wizard [#214837]({{kib-pull}}214837)
* Fixes regression that caused the cases actions to disappear from the detections engine alerts table bulk actions menu [#215111]({{kib-pull}}215111)
* Changes "Close project" to "Log out" in nav menu in serverless mode [#211463]({{kib-pull}}211463)
* Fixes search profiler index reset field when query is changed [#215420]({{kib-pull}}215420)


## March 17, 2025 [serverless-changelog-03172025]

### Features and enhancements [elastic-cloud-serverless-0317025-features-enhancements] 

* Enables read-only editor mode in Lens to explore panel configuration [#208554]({{kib-pull}}208554)
* Allows you to share Observability AI Assistant conversations [#211854]({{kib-pull}}211854)
* Adds context-aware logic to Logs view in Discover [#211176]({{kib-pull}}211176)
* Replaces the Alerts status filter with filter controls [#198495]({{kib-pull}}198495)
* Adds SSL fields to agent binary source settings [#213211]({{kib-pull}}213211)
* Allows users to create a snooze schedule for rules via API [#210584]({{kib-pull}}210584)
* Splits up the top dependencies API for improved speed and response size [#211441]({{kib-pull}}211441)
* Adds working default metrics dashboard for Python OTel [#213599]({{kib-pull}}213599)
* Includes spaceID in SLI documents [#214278]({{kib-pull}}214278)
* Adds support for the `MV_EXPAND` command with the {{esql}} rule type [#212675]({{kib-pull}}212675)
* Enables endpoint actions for events [#206857]({{kib-pull}}206857)
* Introduces GA support for the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type on {{serverless-full}}
* Adds the ability for users to [customize prebuilt rules](https://github.com/elastic/kibana/issues/174168). Users can modify most rule parameters, export and import prebuilt rules — including customized ones — and upgrade prebuilt rules while retaining customization settings [#212761]({{kib-pull}}212761)


### Fixes [elastic-cloud-serverless-03172025-fixes]
* Fixes a bug with ServiceNow where users could not create the connector from the UI form using OAuth [#213658]({{kib-pull}}213658)
* Prevents unnecessary re-render when switching between View and Edit modes [#213902]({{kib-pull}}213902)
* Adds `event-annotation-group` to saved object privileges for dashboards [#212926]({{kib-pull}}212926)
* Makes the **Inspect configuration** button permanently visible [#213619]({{kib-pull}}213619)
* Fixes service maps not building paths when the trace's root transaction has a `parent.id` [#212998]({{kib-pull}}212998)
* Fixes span links with OTel data [#212806]({{kib-pull}}212806)
* Makes {{kib}} retrieval namespace-specific [#213505]({{kib-pull}}213505)
* Ensures semantic queries contribute to scoring when retrieving knowledge from search connectors [#213870]({{kib-pull}}213870)
* Passes `telemetry.sdk` data when loading a dashboard [#214356]({{kib-pull}}214356)
* Fixes `checkPrivilege` to query with indices [#214002]({{kib-pull}}214002)
* Adds support for rollup data views that reference aliases [#212592]({{kib-pull}}212592)
* Fixes an issue with the **Save** button not working when editing event filters [#213805]({{kib-pull}}213805)
* Fixes dragged elements becoming invisible when dragging-and-dropping in Lens [#213928]({{kib-pull}}213928)
* Fixes alignment of the Alerts table in the Rule Preview panel [#214028]({{kib-pull}}214028)
* Fixes Bedrock defaulting region to `us-east-1` [#214251]({{kib-pull}}214251)
* Fixes an issue with the Agent binary download field being blank when a policy uses the default download source [#214360]({{kib-pull}}214360)
* Fixes navigation issues with alert previews [#213455]({{kib-pull}}213455)
* Fixes an issue with changing the width of a Timeline column width bug [#214178]({{kib-pull}}214178)
* Reworks the `enforce_registry_filters` advanced option in Elastic Defend to align with Endpoint [#214106]({{kib-pull}}214106)
* Ensures cell actions are initialized in Event Rendered view and fixes cell action handling for nested event renderers [#212721]({{kib-pull}}212721)
* Supports `date_nanos` in `BUCKET` in the {{esql}} editor [#213319]({{kib-pull}}213319)
* Fixes appearance of warnings in the {{esql}} editor [#213685]({{kib-pull}}213685)
* Makes the Apply time range switch visible in the Job selection flyout when opened from the Anomaly Explorer [#213382]({{kib-pull}}213382)



## March 10, 2025 [serverless-changelog-03102025]

### Features and enhancements [elastic-cloud-serverless-03102025-features-enhancements]
* Adds an improved rule form for the Create Rule flyout in Elastic Observability Serverless [#206685]({{kib-pull}}206685)
* Resolves duplicate conversations in Elastic Observability Serverless [#208044]({{kib-pull}}208044)
* Splits the SLO Details view from the Overview page in Elastic Observability Serverless [#212826]({{kib-pull}}212826)
* Adds the reason message to the rules recovery context in Elastic Observability Serverless [#211411]({{kib-pull}}211411)
* Runtime metrics dashboards now support different ingest paths in Elastic Observability Serverless [#211822]({{kib-pull}}211822)
* Adds SSL options for Fleet Server hosts settings in Fleet [#208091]({{kib-pull}}208091)
* Introduces globe projection for Dashboards and visualizations [#212437]({{kib-pull}}212437)
* Registers a custom integrations search provider in Fleet [#213013]({{kib-pull}}213013)
* Adds support for searchAfter and PIT (point-in-time) parameters in the Get Agents List API in Fleet [#213486]({{kib-pull}}213486)

### Fixes [elastic-cloud-serverless-03102025-fixes]
* Fixes an issue where Korean characters were split into two characters with a space in between when typing in the options list search input in Dashboards and visualizations [#213164]({{kib-pull}}213164)
* Prevents crashes when editing a Lens chart with a by-reference annotation layer in Dashboards and visualizations [#213090]({{kib-pull}}213090)
* Improves instructions for the summarize function in Elastic Observability Serverless [#212936]({{kib-pull}}212936)
* Fixes a "Product Documentation function not available" error in Elastic Observability Serverless [#212676]({{kib-pull}}212676)
* Fixes conversation tests in Elastic Observability Serverless [#213338]({{kib-pull}}213338)
* Allows wildcard filters in SLO queries in Elastic Observability Serverless [#213119]({{kib-pull}}213119)
* Fixes missing summary data in error samples in Elastic Observability Serverless [#213430]({{kib-pull}}213430)
* Fixes a failing test: Stateful Observability - Deployment-agnostic A… in Elastic Observability Serverless [#213530]({{kib-pull}}213530)
* Reduces the review rule upgrade endpoint response size in Elastic Security Serverless [#211045]({{kib-pull}}211045)
* Refactors conversation pagination in Elastic Security Serverless [#211831]({{kib-pull}}211831)
* Fixes alert insights color order in Elastic Security Serverless [#212980]({{kib-pull}}212980)
* Prevents empty conversation IDs in the chat/complete route in Elastic Security Serverless [#213049]({{kib-pull}}213049)
* Fixes issues with unstructured syslog flow in Elastic Security Serverless [#213042]({{kib-pull}}213042)
* Adds bulkGetUserProfiles privilege to Security Feature in Elastic Security Serverless [#211824]({{kib-pull}}211824)
* Fixes a Risk Score Insufficient Privileges warning due to missing cluster privileges in Elastic Security Serverless [#212405]({{kib-pull}}212405)
* Updates Bedrock prompts in Elastic Security Serverless [#213160]({{kib-pull}}213160)
* Adds organizationId and projectId OpenAI headers, along with support for arbitrary headers in Elastic Security Serverless [#213117]({{kib-pull}}213117)
* Ensures dataview selections persist reliably in timeline for Elastic Security Serverless [#211343]({{kib-pull}}211343)
* Fixes incorrect validation when a named parameter was used as a function in {{esql}} [#213355]({{kib-pull}}213355)
* Fixes incorrect overall swim lane height in Machine Learning [#213245]({{kib-pull}}213245)
* Prevented a crash when applying a filter in the Machine Learning anomaly table [#213075]({{kib-pull}}213075)
* Fixes suppressed alerts alignment in the alert flyout in Elastic Security Serverless [#213029]({{kib-pull}}213029)
* Fixes an issue in solution project navigation where panels sometimes failed to toggle closed [#211852]({{kib-pull}}211852)
* Updates wording for options in the sortBy dropdown component [#206464]({{kib-pull}}206464)
* Allows EU hooks hostname in the Torq connector for Elastic Security Serverless [#212563]({{kib-pull}}212563)

## March 3, 2025 [serverless-changelog-03032025]

### Features and enhancements [elastic-cloud-serverless-03032025-features-enhancements]
* Introduces a background task that streamlines the upgrade process for agentless deployments in Elastic Security Serverless [#207143]({{kib-pull}}207143)
* Improves asset inventory onboarding with better context integration in Elastic Security Serverless [#212315]({{kib-pull}}212315)
* Adds syntax highlighting for working with {{esql}} queries in Elastic Observability Serverless [#212669]({{kib-pull}}212669)
* Updates the delete confirmation modal in Elastic Observability Serverless [#212695]({{kib-pull}}212695)
* Removes the enablement check in PUT /api/streams/{id} for classic streams [#212289]({{kib-pull}}212289)

### Fixes [elastic-cloud-serverless-03032025-fixes]
* Fixes issues affecting popularity scores in Discover [#211201]({{kib-pull}}211201)
* Corrects sorting behavior in the profiler storage explorer for Elastic Observability Serverless [#212583]({{kib-pull}}212583)
* Adds a loader to prevent flickering in the KB settings tab in Elastic Observability Serverless [#212678]({{kib-pull}}212678)
* Resolves incorrect enable button behavior in the Entity Store modal in Elastic Security Serverless [#212078]({{kib-pull}}212078)
* Converts the isolate host action into a standalone flyout in Elastic Security Serverless [#211853]({{kib-pull}}211853)
* Ensures model responses are correctly persisted to the chosen conversation ID in Elastic Security Serverless [#212122]({{kib-pull}}212122)
* Corrects image resizing issues for xpack.security.loginAssistanceMessage in Elastic Security Serverless [#212035]({{kib-pull}}212035)
* Fixes automatic import to correctly generate pipelines for parsing CSV files with special characters in Elastic Security Serverless column names [#212513]({{kib-pull}}212513)
* Fixes validation issues for empty EQL queries in Elastic Security Serverless [#212117]({{kib-pull}}212117)
* Resolves dual hover actions in the table tab in Elastic Security Serverless [#212316]({{kib-pull}}212316)
* Updates structured log processing to support multiple log types in Elastic Security Serverless [#212611]({{kib-pull}}212611)
* Ensures the delete model dialog prevents accidental multiple clicks in Machine Learning [#211580]({{kib-pull}}211580)

## February 24, 2025 [serverless-changelog-02242025]

### Features and enhancements [elastic-cloud-serverless-02242025-features-enhancements]
* Exposes SSL options for {{es}} and remote {{es}} outputs in the UI [#208745]({{kib-pull}}208745)
* Displays a warning and a tooltip for the _score column in the Discover grid [#211013]({{kib-pull}}211013)
* Allows `Command/Ctrl` click for the "New" action in the top navigation [#210982]({{kib-pull}}210982)
* Adds the ability for a user to create an API Key in synthetics settings that applies only to specified space(s) [#211816]({{kib-pull}}211816)
* Adds "unassigned" as an asset criticality level for bulk_upload [#208884]({{kib-pull}}208884)
* Sets the Enable visualizations in flyout advanced setting to "On" by default [#211319]({{kib-pull}}211319)
* Preserves user-made chart configurations when changing the query if the actions are compatible with the current chart, such as adding a "where" filter or switching compatible chart types [#210780]({{kib-pull}}210780)
* Adds effects when clicking the **Favorite** button in the list of dashboards and {{esql}} queries, and adds the button to breadcrumb trails [#201596]({{kib-pull}}201596)
* Enables `/api/streams/{id}/_group` endpoints for GroupStreams [#210114]({{kib-pull}}210114)

### Fixes [elastic-cloud-serverless-02242025-fixes]
* Fixes Discover session embeddable drilldown [#211678]({{kib-pull}}211678)
* Passes system message to inferenceCliente.chatComplete [#211263]({{kib-pull}}211263)
* Ensures system message is passed to the inference plugin [#209773]({{kib-pull}}209773)
* Adds automatic re-indexing when encountering a semantic_text bug [#210386]({{kib-pull}}210386)
* Removes unnecessary breadcrumbs in profiling [#211081]({{kib-pull}}211081)
* Adds minHeight to profiler flamegraphs [#210443]({{kib-pull}}210443)
* Adds system message in copy conversation JSON payload [#212009]({{kib-pull}}212009)
* Changes the confirmation message after RiskScore Saved Object configuration is updated [#211372]({{kib-pull}}211372)
* Adds a no data message in the flyout when an analyzer is not enabled [#211981]({{kib-pull}}211981)
* Fixes the Fleet **Save and continue** button [#211563]({{kib-pull}}211563)
* Suggests triple quotes when the user selects the KQL / QSTR [#211457]({{kib-pull}}211457)
* Adds remote cluster instructions for syncing integrations [#211997]({{kib-pull}}211997)
* Allows deploying a model after a failed deployment in Machine Learning [#211459]({{kib-pull}}211459)
* Ensures the members array is unique for GroupStreamDefinitions [#210089]({{kib-pull}}210089)
* Improves function search for easier navigation and discovery [#210437]({{kib-pull}}210437)

## February 17, 2025 [serverless-changelog-02172025]

### Features and enhancements [elastic-cloud-serverless-02172025-features-enhancements]
* Adds alert status management to the AI Assistant connector [#203729]({{kib-pull}}203729)
* Enables the new Borealis theme [#210468]({{kib-pull}}210468)
* Applies compact Display options Popover layout [#210180]({{kib-pull}}210180)
* Increases search timeout toast lifetime to 1 week [#210576]({{kib-pull}}210576)
* Improves performance in dependencies endpoints to prevent high CPU usage [#209999]({{kib-pull}}209999)
* Adds "Logs" tab to mobile services [#209944]({{kib-pull}}209944)
* Adds "All logs" data view to the Classic navigation [#209042]({{kib-pull}}209042)
* Changes default to "native" function calling if the connector configuration is not exposed [#210455]({{kib-pull}}210455)
* Updates entity insight badge to open entity flyouts [#208287]({{kib-pull}}208287)
* Standardizes actions in Alerts KPI visualizations [#206340]({{kib-pull}}206340)
* Allows the creation of dynamic aggregations controls for {{esql}} charts [#210170]({{kib-pull}}210170)
* Fixes the values control FT [#211159]({{kib-pull}}211159)
* Trained models: Replaces the **Download** button by extending the deploy action [#205699]({{kib-pull}}205699)
* Adds the useCustomDragHandle property [#210463]({{kib-pull}}210463)

### Fixes [elastic-cloud-serverless-02172025-fixes]
* Fixes an issue where clicking on the name badge for a synthetics monitor on an SLO details page would lead to a page that failed to load monitor details [#210695]({{kib-pull}}210695)
* Fixes an issue where the popover in the rules page may get stuck when being clicked more than once [#208996]({{kib-pull}}208996)
* Fixes an error in the cases list when the case assignee is an empty string [#209973]({{kib-pull}}209973)
* Fixes an issue with assigning color mappings when multiple layers are defined [#208571]({{kib-pull}}208571)
* Fixes an issue where behind text colors were not correctly assigned, such as in Pie, Treemap, and Mosaic charts [#209632]({{kib-pull}}209632)
* Fixes an issue where dynamic coloring has been disabled from Last value aggregation types [#209110]({{kib-pull}}209110)
* Fixes panel styles [#210113]({{kib-pull}}210113)
* Fixes incorrectly serialized searchSessionId attribute [#210765]({{kib-pull}}210765)
* Fixes the "Save to library" action that could break the chart panel [#210125]({{kib-pull}}210125)
* Fixes link settings not persisting [#211041]({{kib-pull}}211041)
* Fixes "Untitled" export title when exporting CSV from a dashboard [#210143]({{kib-pull}}210143)
* Missing items in the trace waterfall shouldn't break it entirely [#210210]({{kib-pull}}210210)
* Removes unused `error.id` in `getErrorGroupMainStatistics` queries [#210613]({{kib-pull}}210613)
* Fixes connector test in MKI [#211235]({{kib-pull}}211235)
* Fixes an issue where clicking a link in the host/user flyout did not refresh the details panel [#209863]({{kib-pull}}209863)
* Makes 7.x signals/alerts compatible with 8.18 alerts UI [#209936]({{kib-pull}}209936)
* Handles empty categorization results from LLM [#210420]({{kib-pull}}210420)
* Remembers page index in Rule Updates table [#209537]({{kib-pull}}209537)
* Adds concurrency limits and request throttling to prebuilt rule routes [#209551]({{kib-pull}}209551)
* Fixes package name validation on the Datastream page [#210770]({{kib-pull}}210770)
* Makes entity store description more generic [#209130]({{kib-pull}}209130)
* Deletes 'critical services' count from the Entity Analytics Dashboard header [#210827]({{kib-pull}}210827)
* Disables sorting IP ranges in value list modal [#210922]({{kib-pull}}210922)
* Updates entity store copies [#210991]({{kib-pull}}210991)
* Fixes generated name for integration title [#210916]({{kib-pull}}210916)
* Fixes formatting and sorting for custom {{esql}} vars [#209360]({{kib-pull}}209360)
* Fixes WHERE autocomplete with MATCH before LIMIT [#210607]({{kib-pull}}210607)
* Updates install snippets to include all platforms [#210249]({{kib-pull}}210249)
* Updates component templates with deprecated setting [#210200]({{kib-pull}}210200)
* Hides saved query controls in AIOps [#210556]({{kib-pull}}210556)
* Fixes unattended Transforms in integration packages not automatically restarting after reauthorizing [#210217]({{kib-pull}}210217)
* Reinstates switch to support generating public URLs for embed when supported [#207383]({{kib-pull}}207383)
* Provides a fallback view to recover from Stack Alerts page filters bar errors [#209559]({{kib-pull}}209559)

## February 10, 2025 [serverless-changelog-02102025]

### Features and enhancements [elastic-cloud-serverless-02102025-features-enhancements]
* Handles multiple prompt for the Rule connector [#209221]({{kib-pull}}209221)
* Adds `max_file_size_bytes` advanced option to malware for all operating systems [#209541]({{kib-pull}}209541)
* Introducs GroupStreams [#208126]({{kib-pull}}208126)
* Service example added to entity store upload [#209023]({{kib-pull}}209023)
* Updates the bucket_span for ML jobs in the security_host module [#209663]({{kib-pull}}209663)
* Improves handling for operator-defined role mappings [#208710]({{kib-pull}}208710)
* Adds object_src directive to Content-Security-Policy-Report-Only header [#209306]({{kib-pull}}209306)

### Fixes [elastic-cloud-serverless-02102025-fixes]
* Fixes highlight for HJSON [#208858]({{kib-pull}}208858)
* Disables pointer events on drag + resize [#208647]({{kib-pull}}208647)
* Restores show missing dataView error message in case of missing datasource [#208363]({{kib-pull}}208363)
* Fixes issue with Amsterdam theme where charts render with the incorrect background color [#209595]({{kib-pull}}209595)
* Fixes an issue in Lens Table where a split-by metric on a terms rendered incorrect colors in table cells [#208623]({{kib-pull}}208623)
* Forces return 0 on empty buckets on count if null flag is disabled [#207308]({{kib-pull}}207308)
* Fixes all embeddables rebuilt on refresh [#209677]({{kib-pull}}209677)
* Fixes using data view runtime fields during rule execution for the custom threshold rule [#209133]({{kib-pull}}209133)
* Fixes running processes that were missing from the processes table [#209076]({{kib-pull}}209076)
* Fixes missing exception stack trace [#208577]({{kib-pull}}208577)
* Fixes the preview chart in the Custom Threshold rule creation form when the field name has slashes [#209263]({{kib-pull}}209263)
* Display No Data in Threshold breached component [#209561]({{kib-pull}}209561)
* Fixes an issue where APM charts were rendered without required transaction type or service name, causing excessive alerts to appear [#209552]({{kib-pull}}209552)
* Fixes bug that caused issues with loading SLOs by status, SLI type, or instance id [#209910]({{kib-pull}}209910)
* Updates colors in the AI Assistant icon [#210233]({{kib-pull}}210233)
* Updates the simulate function calling setting to support "auto" [#209628]({{kib-pull}}209628)
* Fixes structured log template to use single quotes [#209736]({{kib-pull}}209736)
* Fixes {{esql}} alert on alert [#208894]({{kib-pull}}208894)
* Fixes issue with multiple IP addresses in strings [#209475]({{kib-pull}}209475)
* Keeps the histogram config on time change [#208053]({{kib-pull}}208053)
* WHERE replacement ranges correctly generated for every case [#209684]({{kib-pull}}209684)
* Updates removed parameters of the Fleet -> Logstash output configurations [#210115]({{kib-pull}}210115)
* Fixes log rate analysis, change point detection, and pattern analysis embeddables not respecting filters from Dashboard's controls [#210039]({{kib-pull}}210039)

## February 3, 2025 [serverless-changelog-02032025]

### Features and enhancements [elastic-cloud-serverless-02032025-features-enhancements]
* Rework saved query privileges [#202863]({{kib-pull}}202863)
* In-table search [#206454]({{kib-pull}}206454)
* Refactor RowHeightSettings component to EUI layout [#203606]({{kib-pull}}203606)
* Chat history details in conversation list [#207426]({{kib-pull}}207426)
* Cases assignees sub feature [#201654]({{kib-pull}}201654)
* Adds preview logged requests for new terms, threshold, query, ML rule types [#203320]({{kib-pull}}203320)
* Adds in-text citations to security solution AI assistant responses [#206683]({{kib-pull}}206683)
* Remove Tech preview badge for GA [#208523]({{kib-pull}}208523)
* Adds new View job detail flyouts for Anomaly detection and Data Frame Analytics [#207141]({{kib-pull}}207141)
* Adds a default "All logs" temporary data view in the Observability Solution view [#205991]({{kib-pull}}205991)
* Adds Knowledge Base entries API [#206407]({{kib-pull}}206407)
* Adds Kibana Support for Security AI Prompts Integration [#207138]({{kib-pull}}207138)
* Changes to support event.ingested as a configurable timestamp field for init and enable endpoints [#208201]({{kib-pull}}208201)
* Adds Spaces column to Anomaly Detection, Data Frame Analytics and Trained Models management pages [#206696]({{kib-pull}}206696)
* Adds simple flyout based file upload to Search [#206864]({{kib-pull}}206864)
* Bump kube-stack Helm chart onboarding version [#208217]({{kib-pull}}208217)
* Log deprecated api usages [#207904]({{kib-pull}}207904)
* Added support for human readable name attribute for saved objects audit events [#206644]({{kib-pull}}206644)
* Enhanced Role management to manage larger number of roles by adding server side filtering, pagination and querying [#194630]({{kib-pull}}194630)
* Added Entity Store data view refresh task [#208543]({{kib-pull}}208543)
* Increase maximum Osquery timeout to 24 hours [#207276]({{kib-pull}}207276)

### Fixes [elastic-cloud-serverless-02032025-fixes]
* Remove use of fr unit [#208437]({{kib-pull}}208437)
* Fixes load more request size [#207901]({{kib-pull}}207901)
* Persist runPastTimeout setting [#208611]({{kib-pull}}208611)
* Allow panel to extend past viewport on resize [#208828]({{kib-pull}}208828)
* Knowledge base install updates [#208250]({{kib-pull}}208250)
* Fixes conversations test in MKI [#208649]({{kib-pull}}208649)
* Fixes ping heatmap regression when Inspect flag is turned off [#208726]({{kib-pull}}208726)
* Fixes monitor status rule for empty kql query results [#208922]({{kib-pull}}208922)
* Fixes multiple flyouts [#209158]({{kib-pull}}209158)
* Adds missing fields to input manifest templates [#208768]({{kib-pull}}208768)
* "Select a Connector" popup does not show up after the user selects any connector and then cancels it from Endpoint Insights [#208969]({{kib-pull}}208969)
* Logs shard failures for eql event queries on rule details page and in event log [#207396]({{kib-pull}}207396)
* Adds filter to entity definitions schema [#208588]({{kib-pull}}208588)
* Fixes missing ecs mappings [#209057]({{kib-pull}}209057)
* Apply the timerange to the fields fetch in the editor [#208490]({{kib-pull}}208490)
* Update java.ts - removing serverless link [#204571]({{kib-pull}}204571)

## January 27, 2025 [serverless-changelog-01272025]

### Features and enhancements [elastic-cloud-serverless-01272025-features-enhancements]
* Breaks out timeline and note privileges in Elastic Security Serverless [#201780]({{kib-pull}}201780)
* Adds service enrichment to the detection engine in Elastic Security Serverless [#206582]({{kib-pull}}206582)
* Updates the Entity Store Dashboard to prompt for the Service Entity Type in Elastic Security Serverless [#207336]({{kib-pull}}207336)
* Adds enrichPolicyExecutionInterval to entity enablement and initialization APIs in Elastic Security Serverless [#207374]({{kib-pull}}207374)
* Introduces a lookback period configuration for the Entity Store in Elastic Security Serverless [#206421]({{kib-pull}}206421)
* Allows pre-configured connectors to opt into exposing their configurations by setting exposeConfig in Alerting [#207654]({{kib-pull}}207654)
* Adds selector syntax support to log source profiles in Elastic Observability Serverless [#206937]({{kib-pull}}206937)
* Displays stack traces in the logs overview tab in Elastic Observability Serverless [#204521]({{kib-pull}}204521)
* Enables the use of the rule form to create rules in Elastic Observability Serverless [#206774]({{kib-pull}}206774)
* Checks only read privileges of existing indices during rule execution in Elastic Security Serverless [#177658]({{kib-pull}}177658)
* Updates KNN search and query template autocompletion in Elasticsearch Serverless [#207187]({{kib-pull}}207187)
* Updates JSON schemas for code editors in Machine Learning [#207706]({{kib-pull}}207706)
* Reindexes the .kibana_security_session_1 index to the 8.x format in Security [#204097]({{kib-pull}}204097)

### Fixes [elastic-cloud-serverless-01272025-fixes]
* Fixes editing alerts filters for multi-consumer rule types in Alerting [#206848]({{kib-pull}}206848)
* Resolves an issue where Chrome was no longer hidden for reports in Dashboards and Visualizations [#206988]({{kib-pull}}206988)
* Updates library transforms and duplicate functionality in Dashboards and Visualizations [#206140]({{kib-pull}}206140)
* Fixes an issue where drag previews are now absolutely positioned in Dashboards and Visualizations [#208247]({{kib-pull}}208247)
* Fixes an issue where an accessible label now appears on the range slider in Dashboards and Visualizations [#205308]({{kib-pull}}205308)
* Fixes a dropdown label sync issue when sorting by "Type" [#206424]({{kib-pull}}206424)
* Fixes an access bug related to user instructions in Elastic Observability Serverless [#207069]({{kib-pull}}207069)
* Fixes the Open Explore in Discover link to open in a new tab in Elastic Observability Serverless [#207346]({{kib-pull}}207346)
* Returns an empty object for tool arguments when none are provided in Elastic Observability Serverless [#207943]({{kib-pull}}207943)
* Ensures similar cases count is not fetched without the proper license in Elastic Security Serverless [#207220]({{kib-pull}}207220)
* Fixes table leading actions to use standardized colors in Elastic Security Serverless [#207743]({{kib-pull}}207743)
* Adds missing fields to the AWS S3 manifest in Elastic Security Serverless [#208080]({{kib-pull}}208080)
* Prevents redundant requests when loading Discover sessions and toggling chart visibility in {{esql}} [#206699]({{kib-pull}}206699)
* Fixes a UI error when agents move to an orphaned state in Fleet [#207746]({{kib-pull}}207746)
* Restricts non-local Elasticsearch output types for agentless integrations and policies in Fleet [#207296]({{kib-pull}}207296)
* Fixes table responsiveness in the Notifications feature of Machine Learning [#206956]({{kib-pull}}206956)

## January 13, 2025 [serverless-changelog-01132025]

### Features and enhancements [elastic-cloud-serverless-01132025-features-enhancements]
* Adds last alert status change to Elastic Security Serverless flyout [#205224]({{kib-pull}}205224)
* Case templates are now GA [#205940]({{kib-pull}}205940)
* Adds format to JSON messages in Elastic Observability Serverless Logs profile [#205666]({{kib-pull}}205666)
* Adds inference connector in Elastic Security Serverless AI features [#204505]({{kib-pull}}204505)
* Adds inference connector for Auto Import in Elastic Security Serverless [#206111]({{kib-pull}}206111)
* Adds Feature Flag Support for Cloud Security Posture Plugin in Elastic Security Serverless [#205438]({{kib-pull}}205438)
* Adds the ability to sync Machine Learning saved objects to all spaces [#202175]({{kib-pull}}202175)
* Improves messages for recovered alerts in Machine Learning Transforms [#205721]({{kib-pull}}205721)

### Fixes [elastic-cloud-serverless-01132025-fixes]
* Fixes an issue where "KEEP" columns are not applied after an Elasticsearch error in Discover [#205833]({{kib-pull}}205833)
* Resolves padding issues in the document comparison table in Discover [#205984]({{kib-pull}}205984)
* Fixes a bug affecting bulk imports for the knowledge base in Elastic Observability Serverless [#205075]({{kib-pull}}205075)
* Enhances the Find API by adding cursor-based pagination (search_after) as an alternative to offset-based pagination [#203712]({{kib-pull}}203712)
* Updates Elastic Observability Serverless to use architecture-specific Elser models [#205851]({{kib-pull}}205851)
* Fixes dynamic batching in the timeline for Elastic Security Serverless [#204034]({{kib-pull}}204034)
* Resolves a race condition bug in Elastic Security Serverless related to OpenAI errors [#205665]({{kib-pull}}205665)
* Improves the integration display by ensuring all policies are listed in Elastic Security Serverless [#205103]({{kib-pull}}205103)
* Renames color variables in the user interface for better clarity and consistency [#204908]({{kib-pull}}204908)
* Allows editor suggestions to remain visible when the inline documentation flyout is open in {{esql}} [#206064]({{kib-pull}}206064)
* Ensures the same time range is applied to documents and the histogram in {{esql}} [#204694]({{kib-pull}}204694)
* Fixes validation for the "required" field in multi-text input fields in Fleet [#205768]({{kib-pull}}205768)
* Fixes timeout issues for bulk actions in Fleet [#205735]({{kib-pull}}205735)
* Handles invalid RRule parameters to prevent infinite loops in alerts [#205650]({{kib-pull}}205650)
* Fixes privileges display for features and sub-features requiring "All Spaces" permissions in Fleet [#204402]({{kib-pull}}204402)
* Prevents password managers from modifying disabled input fields [#204269]({{kib-pull}}204269)
* Updates the listing control in the user interface [#205914]({{kib-pull}}205914)
* Improves consistency in the help dropdown design [#206280]({{kib-pull}}206280)

## January 6, 2025 [serverless-changelog-01062025]

### Features and enhancements [elastic-cloud-serverless-01062025-features-enhancements]
* Introduces case observables in Elastic Security Serverless [#190237]({{kib-pull}}190237)
* Adds a JSON field called "additional fields" to ServiceNow cases when sent using connector, containing the internal names of the ServiceNow table columns [#201948]({{kib-pull}}201948)
* Adds the ability to configure the appearance color mode to sync dark mode with the system value [#203406]({{kib-pull}}203406)
* Makes the "Copy" action visible on cell hover in Discover [#204744]({{kib-pull}}204744)
* Updates the EnablementModalCallout name to AdditionalChargesMessage in Elastic Security Serverless [#203061]({{kib-pull}}203061)
* Adds more control over which Elastic Security Serverless alerts in Attack Discovery are included as context to the large language model [#205070]({{kib-pull}}205070)
* Adds a consistent layout and other UI enhancements for {{ml}} pages [#203813]({{kib-pull}}203813)

### Fixes [elastic-cloud-serverless-01062025-fixes]
* Fixes an issue that caused dashboards to lag when dragging the time slider [#201885]({{kib-pull}}201885)
* Updates the CloudFormation template to the latest version and adjusts the documentation to reflect the use of a single Firehose stream created by the new template [#204185]({{kib-pull}}204185)
* Fixes Integration and Datastream name validation in Elastic Security Serverless [#204943]({{kib-pull}}204943)
* Fixes an issue in the Automatic Import process where there is now inclusion of the @timestamp field in ECS field mappings whenever possible [#204931]({{kib-pull}}204931)
* Allows Automatic Import to safely parse Painless field names that are not valid Painless identifiers in if contexts [#205220]({{kib-pull}}205220)
* Aligns the Box Native Connector configuration fields with the source of truth in the connectors codebase, correcting mismatches and removing unused configurations [#203241]({{kib-pull}}203241)
* Fixes the "Show all agent tags" option in Fleet when the agent list is filtered [#205163]({{kib-pull}}205163)
* Updates the Results Explorer flyout footer buttons alignment in Data Frame Analytics [#204735]({{kib-pull}}204735)
* Adds a missing space between lines in the Data Frame Analytics delete job modal [#204732]({{kib-pull}}204732)
* Fixes an issue where the **Refresh** button in the Anomaly Detection Datafeed counts table was unresponsive [#204625]({{kib-pull}}204625)
* Fixes the inference timeout check in File Upload [#204722]({{kib-pull}}204722)
* Fixes the side bar navigation for the Data Visualizer [#205170]({{kib-pull}}205170)

## December 16, 2024 [serverless-changelog-12162024]

### Features and enhancements [elastic-cloud-serverless-12162024-features-enhancements]
* Optimizes the Kibana Trained Models API [#200977]({{kib-pull}}200977)
* Adds a Create Case action to the Log rate analysis page [#201549]({{kib-pull}}201549)
* Improves AI Assistant’s response quality by giving it access to Elastic’s product documentation [#199694]({{kib-pull}}199694)
* Adds support for suppressing EQL sequence alerts [#189725]({{kib-pull}}189725)
* Adds an Advanced settings section to the SLO form [#200822]({{kib-pull}}200822)
* Adds a new sub-feature privilege under Synthetics and Uptime Can manage private locations [#201100]({{kib-pull}}201100)

### Fixes [elastic-cloud-serverless-12162024-fixes]
* Fixes point visibility regression [#202358]({{kib-pull}}202358)
* Improves help text of creator and view count features on dashboard listing page [#202488]({{kib-pull}}202488)
* Highlights matching field values when performing a KQL search on a keyword field [#201952]({{kib-pull}}201952)
* Supports "Inspect" in saved search embeddables [#202947]({{kib-pull}}202947)
* Fixes your ability to clear the user-specific system prompt [#202279]({{kib-pull}}202279)
* Fixes error when opening rule flyout [#202386]({{kib-pull}}202386)
* Fixes to Ops Genie as a default connector [#201923]({{kib-pull}}201923)
* Fixes actions on charts [#202443]({{kib-pull}}202443)
* Adds flyout to table view in Infrastructure Inventory [#202646]({{kib-pull}}202646)
* Fixes service names with spaces not being URL encoded properly for context.viewInAppUrl [#202890]({{kib-pull}}202890)
* Allows access query logic to handle user ID and name conditions [#202833]({{kib-pull}}202833)
* Fixes APM rule error message for invalid KQL filter [#203096]({{kib-pull}}203096)
* Rejects CEF logs from Automatic Import and redirects you to the CEF integration instead [#201792]({{kib-pull}}201792)
* Updates the install rules title and message [#202226]({{kib-pull}}202226)
* Fixes error on second entity engine init API call [#202903]({{kib-pull}}202903)
* *estricts unsupported log formats [#202994]({{kib-pull}}202994)
* Removes errors related to Enterprise Search nodes [#202437]({{kib-pull}}202437)
* Improves web crawler name consistency [#202738]({{kib-pull}}202738)
* Fixes editor cursor jumpiness [#202389]({{kib-pull}}202389)
* Fixes rollover datastreams on subobjects mapper exception [#202689]({{kib-pull}}202689)
* Fixes spaces sync to retrieve 10,000 trained models [#202712]({{kib-pull}}202712)
* Fixes log rate analysis embeddable error on the Alerts page [#203093]({{kib-pull}}203093)
* Fixes Slack API connectors not displayed under Slack connector type when adding new connector to rule [#202315]({{kib-pull}}202315)

## December 9, 2024 [serverless-changelog-12092024]

### Features and enhancements [elastic-cloud-serverless-12092024-features-enhancements]
* Elastic Observability Serverless adds a new sub-feature for managing private locations [#201100]({{kib-pull}}201100)
* Elastic Observability Serverless adds the ability to configure SLO advanced settings from the UI [#200822]({{kib-pull}}200822)
* Elastic Security Serverless adds support for suppressing EQL sequence alerts [#189725]({{kib-pull}}189725)
* Elastic Security Serverless adds a /trained_models_list endpoint to retrieve complete data for the Trained Model UI [#200977]({{kib-pull}}200977)
* Machine Learning adds an action to include log rate analysis in a case [#199694]({{kib-pull}}199694)
* Machine Learning enhances the Kibana API to optimize trained models [#201549]({{kib-pull}}201549)

### Fixes [elastic-cloud-serverless-12092020-fixes]
* Fixes Slack API connectors not being displayed under the Slack connector type when adding a new connector to a rule in Alerting [#202315]({{kib-pull}}202315)
* Fixes point visibility regression in dashboard visualizations [#202358]({{kib-pull}}202358)
* Improves help text for creator and view count features on the Dashboard listing page [#202488]({{kib-pull}}202488)
* Highlights matching field values when performing a KQL search on a keyword field in Discover [#201952]({{kib-pull}}201952)
* Adds support for the Inspect option in saved search embeddables in Discover [#202947]({{kib-pull}}202947)
* Enables the ability to clear user-specific system prompts in Elastic Observability Serverless [#202279]({{kib-pull}}202279)
* Fixes an error when opening the rule flyout in Elastic Observability Serverless [#202386]({{kib-pull}}202386)
* Improves handling of Opsgenie as the default connector in Elastic Observability Serverless [#201923]({{kib-pull}}201923)
* Fixes issues with actions on charts in Elastic Observability Serverless [#202443]({{kib-pull}}202443)
* Adds a flyout to the table view in Infrastructure Inventory in Elastic Observability Serverless [#202646]({{kib-pull}}202646)
* Fixes service names with spaces not being URL-encoded properly for `{{context.viewInAppUrl}}` in Elastic Observability Serverless [#202890]({{kib-pull}}202890)
* Enhances access query logic to handle user ID and name conditions in Elastic Observability Serverless [#202833]({{kib-pull}}202833)
* Fixes an APM rule error message when a KQL filter is invalid in Elastic Observability Serverless [#203096]({{kib-pull}}203096)
* Restricts and rejects CEF logs in automatic import and redirects them to the CEF integration in Elastic Security Serverless [#201792]({{kib-pull}}201792)
* Updates the copy of the install rules title and message in Elastic Security Serverless [#202226]({{kib-pull}}202226)
* Clears errors on the second entity engine initialization API call in Elastic Security Serverless [#202903]({{kib-pull}}202903)
* Restricts unsupported log formats in Elastic Security Serverless [#202994]({{kib-pull}}202994)
* Removes errors related to Enterprise Search nodes in Elasticsearch Serverless [#202437]({{kib-pull}}202437)
* Ensures consistency in web crawler naming in Elasticsearch Serverless [#202738]({{kib-pull}}202738)
* Fixes editor cursor jumpiness in {{esql}} [#202389]({{kib-pull}}202389)
* Implements rollover of data streams on subobject mapper exceptions in Fleet [#202689]({{kib-pull}}202689)
* Fixes trained models to retrieve up to 10,000 models when spaces are synced in Machine Learning [#202712]({{kib-pull}}202712)
* Fixes a Log Rate Analysis embeddable error on the Alerts page in AiOps [#203093]({{kib-pull}}203093)

## December 3, 2024 [serverless-changelog-12032024]

### Features and enhancements [elastic-cloud-serverless-12032024-features-enhancements]
* Adds tabs for Import Entities and Engine Status to the Entity Store [#201235]({{kib-pull}}201235)
* Adds status tracking for agentless integrations to {{fleet}} [#199567]({{kib-pull}}199567)
* Adds a new {{ml}} module that can detect anomalous activity in host-based logs [#195582]({{kib-pull}}195582)
* Allows custom Mapbox Vector Tile sources to style map layers and provide custom legends [#200656]({{kib-pull}}200656)
* Excludes stale SLOs from counts of healthy and violated SLOs [#201027]({{kib-pull}}201027)
* Adds a "Continue without adding integrations" message to the {{elastic-sec}} Dashboards page that takes you to the Entity Analytics dashboard [#201363]({{kib-pull}}201363)
* Displays visualization descriptions under their titles [#198816]({{kib-pull}}198816)

### Fixes [elastic-cloud-serverless-12032024-fixes]
* Hides the **Clear** button when no filters are selected [#200177]({{kib-pull}}200177)
* Fixes a mismatch between how wildcards were handled in previews versus actual rule executions [#201553]({{kib-pull}}201553)
* Fixes incorrect Y-axis and hover values in the Service Inventory’s Log rate chart [#201361]({{kib-pull}}201361)
* Disables the **Add note** button in the alert details flyout for users who lack privileges [#201707]({{kib-pull}}201707)
* Fixes the descriptions of threshold rules that use cardinality [#201162]({{kib-pull}}201162)
* Disables the **Install All** button on the Add Elastic Rules page when rules are installing [#201731]({{kib-pull}}201731)
* Reintroduces a data usage warning on the Entity Analytics Enablement modal [#201920]({{kib-pull}}201920)
* Improves accessibility for the Create a connector page [#201590]({{kib-pull}}201590)
* Fixes a bug that could cause {{agents}} to get stuck updating during scheduled upgrades [#202126]({{kib-pull}}202126)
* Fixes a bug related to starting {{ml}} deployments with autoscaling and no active nodes [#201256]({{kib-pull}}201256)
* Initializes saved objects when the Trained Model page loads [#201426]({{kib-pull}}201426)
* Fixes the display of deployment stats for unallocated deployments of {{ml}} models [#202005]({{kib-pull}}202005)
* Enables the solution type search for instant deployments [#201688]({{kib-pull}}201688)
* Improves the consistency of alert counts across different views [#202188]({{kib-pull}}202188)
