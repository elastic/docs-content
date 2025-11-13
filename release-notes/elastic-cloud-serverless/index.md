---
navigation_title: Elastic Cloud Serverless
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/serverless-changelog.html
products:
  - id: cloud-serverless
---

# {{serverless-full}} changelog [elastic-cloud-serverless-changelog]
Review the changes, fixes, and more to {{serverless-full}}.

## November 10, 2025 [serverless-changelog-11102025]

### Features and enhancements [serverless-changelog-11102025-features-enhancements]

* Adds nightly maintenance for anomaly detection results indices to keep to manageable size [#136065]({{es-pull}}136065)
* Adds the ability to preview index requests in transforms [#137455]({{es-pull}}137455)
* Allows field capabilities to span across Elasticsearch Serverless projects [#137530]({{es-pull}}137530)
* Improves {{esql}} performance by skipping unnecessary query plan diff calculations in Elasticsearch Serverless [#137721]({{es-pull}}137721)
* Passes the {{es}} version in the EIS inference request header in Elasticsearch Serverless [#137643]({{es-pull}}137643)
* Introduces a synthetic `_id` format for time-series data streams [#137274]({{es-pull}}137274)
* Updates the Dashboard top navigation to include a **Save** menu [#237211]({{kib-pull}}237211)
* Moves visualization configuration settings, including appearance, titles and text, axis, and legend to a flyout panel in **Lens** [#240804]({{kib-pull}}240804)
* Supports subqueries in the Discover pretty printer [#241473]({{kib-pull}}241473)
* Adds context-aware autocomplete for Discover subqueries with nesting restrictions [#241912]({{kib-pull}}241912)
* Adds subquery support for columns after and validation in Discover [#241567]({{kib-pull}}241567)
* Adds support for Discover subqueries in FROM clauses across tools [#242166]({{kib-pull}}242166)
* Enables users to view the SLO associated with a burn rate rule on the rule details page in Elastic Observability Serverless [#240535]({{kib-pull}}240535)
* Exposes `sampling_rate` agent central config options to users in Elastic Observability Serverless [#241908]({{kib-pull}}241908)
* Makes the Elastic logo open a custom home page in solution view [#241571]({{kib-pull}}241571)
* Enforces the `object_src 'none'` directive in the {{kib}} content security policy [#241029]({{kib-pull}}241029)
* Adds origin configuration options for authentication providers [#239993]({{kib-pull}}239993)
* Adds the ability to cancel {{ml}} file uploads [#241297]({{kib-pull}}241297)
* Improves display of long field values in Data Visualizer top values list [#241006]({{kib-pull}}241006)
* Adds a temperature parameter to Inference AI, and OpenAI, Bedrock, and Gemini connectors [#239806]({{kib-pull}}239806)
* Adds support for custom headers in the OpenAI integration [#238710]({{kib-pull}}238710)
* Fixes public Update spaces APIs [#242136]({{kib-pull}}242136)
* Improves layout for custom inference endpoints [#241779]({{kib-pull}}241779)
* Displays field data types in the Processing table and step editor [#241825]({{kib-pull}}241825)
* Adds timezone and locale parameters to Streamlang [#241369]({{kib-pull}}241369)
* Displays field data types in the Streams Partitioning UI [#242134]({{kib-pull}}242134)
* Adds autocomplete for field values in Streams Partitioning and Processing tabs [#241119]({{kib-pull}}241119)
* Hides document match filter controls for users without manage privileges [#242119]({{kib-pull}}242119)

### Fixes [serverless-changelog-11102025-fixes]

* Fixes feature display order when using explain in Learning to Rank (LTR) [#137671]({{es-pull}}137671)
* Fixes an issue where missing geotile buckets caused errors in Transform [#137476]({{es-pull}}137476)
* Ensures {{esql}} full text functions accept `null` values as field parameters in Elasticsearch Serverless  [#137430]({{es-pull}}137430)
* Fixes a missing attribute issue in {{esql}} full text functions in Elasticsearch Serverless [#137395]({{es-pull}}137395)
* Fixes a bug in `RankDocRetrieverBuilder` when `from` is set to the default -1 value [#137637]({{es-pull}}137637)
* Prevents use-after-close errors in async search by making `MutableSearchResponse` reference-counted  [#134359]({{es-pull}}134359)
* Removes early phase failures during batched search execution [#136889]({{es-pull}}136889)
* Improves SQL validation errors by providing more descriptive exception messages [#137560]({{es-pull}}137560)
* Correctly accounts for additional settings providers when determining data stream effective settings [#137407]({{es-pull}}137407)
* Adds proxy SSL options for download sources [#241115]({{kib-pull}}241115)
* Ensures {{fleet}} policy name uniqueness is enforced consistently across spaces [#239631]({{kib-pull}}239631)
* Shows warnings on the sync integrations UI when referencing other entities [#241623]({{kib-pull}}241623)
* Escapes special characters when creating {{esql}} queries for **Lens** charts in Elastic Observability Serverless [#241662]({{kib-pull}}241662)
* Fixes "Values" dropdown display on smaller screens in Elastic Observability Serverless [#241812]({{kib-pull}}241812)
* Excludes stale SLOs from group-by statistics in Elastic Observability Serverless [#240077]({{kib-pull}}240077)
* Fixes missing `EngineMetadata.type` in generic entity popovers in Elastic Security Serverless [#239661]({{kib-pull}}239661)
* Sanitizes lookup names when creating indices in Elastic Security Serverless [#240228]({{kib-pull}}240228)
* Supports multiple values in IOC flyout table tab in Elastic Security Serverless [#236110]({{kib-pull}}236110)
* Fixes top-N popover overlapping the new case flyout in Elastic Security Serverless [#242045]({{kib-pull}}242045)
* Fixes threshold source event handling in Elastic Security Serverless [#238707]({{kib-pull}}238707)
* Ensures Timeline {{esql}} query editor displays correctly in full screen mode in Elastic Security Serverless  [#242027]({{kib-pull}}242027)
* Fixes invalid state for the **Enable wired streams** toggle [#241266]({{kib-pull}}241266)
* Fixes simulation of geo points in Streams [#241824]({{kib-pull}}241824)
* Decouples Streams AI features from Observability AI Assistant [#242019]({{kib-pull}}242019)
* Only applies tag changes when the connector supports them [#241944]({{kib-pull}}241944)

## November 3, 2025 [serverless-changelog-11032025]

### Features and enhancements [serverless-changelog-11032025-features-enhancements]

* Moves the **Lens** visualization toolbar from the workspace section to the configuration panel [#239879]({{kib-pull}}239879)
* Adds support for rolling back integrations to previous versions [#240761]({{kib-pull}}240761)
* Adds support for subqueries in the {{esql}} abstract syntax tree (AST) [#241227]({{kib-pull}}241227)
* Adds subquery support for the walker and visitor in the {{esql}} AST [#241451]({{kib-pull}}241451)
* Adds support for expressions in `LOOKUP JOIN` autocomplete [#240735]({{kib-pull}}240735)
* Adds support for multi-value variables in `MV_CONTAINS` [#239266]({{kib-pull}}239266)
* Adds client-side validation for `LOOKUP JOIN ON` expressions [#240930]({{kib-pull}}240930)
* Improves the {{esql}} suggestions logic to provide more semantically intelligent suggestions [#241081]({{kib-pull}}241081)
* Adds an `isStream` parameter to the `chat/complete` endpoint to support non-streaming responses in the Observability AI Assistant [#240819]({{kib-pull}}240819)
* Makes the `opamp_polling_interval` and `sampling_rate` agent configuration variables available to EDOT Node.js [#241048]({{kib-pull}}241048)
* Adds a free-text popup for the `runscript` argument to provide user input to the selected script [#239436]({{kib-pull}}239436)
* Adds the deployment name to the breadcrumbs in {{ech}} [#238078]({{kib-pull}}238078)
* Adds a **Give feedback** button to the Anomaly Explorer and Single Metric Viewer [#239883]({{kib-pull}}239883)
* Adds a new `temperature` parameter to the AI Connector configuration schema [#239626]({{kib-pull}}239626)
* Makes the Update spaces APIs public [#241109]({{kib-pull}}241109)
* Adds support for the `convert` processor in stream data processing [#240023]({{kib-pull}}240023)
* Improves message feedback in collapsed Processors/Conditions sections [#240778]({{kib-pull}}240778)
* Optimizes workflow output in Agent Builder tools by removing workflow execution details from tool calls, reducing LLM token consumption and improving agent performance and reliability [#241040]({{kib-pull}}241040)

### Fixes [serverless-changelog-11032025-fixes]

* Fixes layout issues for Markdown embeddables in small panels [#240806]({{kib-pull}}240806)
* Fixes an issue where labels in the **Create index** flow did not automatically render with the default vector tile scaling after saving or applying styling changes [#240728]({{kib-pull}}240728)
* Fixes `template_path` asset selection for certain integration packages [#240750]({{kib-pull}}240750)
* Omits system properties when syncing ingest pipelines [#241096]({{kib-pull}}241096)
* Fixes autocomplete for time series sources after a comma [#241402]({{kib-pull}}241402)
* Fixes a bottom gap that appeared while loading data in some cases [#238879]({{kib-pull}}238879)
* Hides non-trace services in service maps [#240104]({{kib-pull}}240104)
* Fixes an issue where the `kibana` tool failed when running {{kib}} behind a proxy [#236653]({{kib-pull}}236653)
* Fixes overlapping components in the Observability AI Assistant flyout on small screens [#241026]({{kib-pull}}241026)
* Aligns the **Members** link in the side navigation across all solutions [#240992]({{kib-pull}}240992)
* Updates Metrics experience API routes to delegate authorization to {{es}} [#241195]({{kib-pull}}241195)
* Copies alert states to the payload [#240411]({{kib-pull}}240411)
* Adds missing fields to transaction data [#241336]({{kib-pull}}241336)
* Simplifies metrics profile resolution by removing index pattern and time series validation [#241047]({{kib-pull}}241047)
* Allows partial matches on rule names when searching installed rules [#237496]({{kib-pull}}237496)
* Fixes a regression in threshold rule logic where threshold rules with no `group by` fields defined would no longer generate alerts [#241022]({{kib-pull}}241022)
* Fixes an issue where the alert details flyout on the **Risk contributions** tab did not display data in some cases [#241153]({{kib-pull}}241153)
* Fixes a table pagination issue on the Intelligence page [#241108]({{kib-pull}}241108)
* Fixes an issue with the **Regenerate** button in the Security Assistant [#241240]({{kib-pull}}241240)
* Fixes an issue where the Security AI Assistant's Index Entry form was showing incorrect field suggestions, missing searchable fields that exist as multi-fields or nested properties in {{es}} mappings [#239453]({{kib-pull}}239453)
* Fixes an issue where agent-based integrations failed to produce data [#241390]({{kib-pull}}241390)
* Fixes an infinite loop bug related to bootstrapping list resources [#241052]({{kib-pull}}241052)
* Reduces re-renders on resize and items change [#239888]({{kib-pull}}239888)
* Fixes index names causing an incompatible cluster error when product docs are installed with multiple inference IDs [#240506]({{kib-pull}}240506)
* Ensures all authentication fields are displayed correctly [#240913]({{kib-pull}}240913)
* Ensures the `max_tokens` parameter is passed as expected by the service [#241188]({{kib-pull}}241188)
* Updates the inference creation endpoint to ensure the `max_tokens` parameter is passed as expected when creating an Anthropic Connector [#241212]({{kib-pull}}241212)
* Removes the default fallback region for the Bedrock Connector [#241157]({{kib-pull}}241157)
* Fixes wrapping issues in the Streams UI [#240883]({{kib-pull}}240883)
* Speeds up field simulation in Streams [#241313]({{kib-pull}}241313)
* Updates action response codes [#240420]({{kib-pull}}240420)
* Fixes an infinite loop bug in the **Investigation guide** editor [#240472]({{kib-pull}}240472)

## October 27, 2025 [serverless-changelog-10272025]

### Features and enhancements [elastic-security-10272025-features-enhancements]
* Adds support for deleting export schedules [#238197]({{kib-pull}}238197)
* Moves the **Lens** visualization toolbar from the **Visualization parameters** section to the flyout header [#239176]({{kib-pull}}239176)
* Changes the processing order in {{esql}} so the breakdown is applied before the date histogram [#239685]({{kib-pull}}239685)
* Adds a **View in Discover** button to the Alert details page for infrastructure rules [#236880]({{kib-pull}}236880)
* Introduces CDR Data View versioning and migration logic [#238547]({{kib-pull}}238547)
* Fixes layout wrapping for fields in the Machine Learning Overview and Notifications pages [#239113]({{kib-pull}}239113)
* Removes the AI Assistant Settings privilege [#239144]({{kib-pull}}239144)
* Adds ingest pipeline processor template suggestions to the manual ingest pipeline processor editor [#236919]({{kib-pull}}236919)
* Adds the `kibana.alert.index_pattern` field to all alerts [#239450]({{kib-pull}}239450)

### Fixes [elastic-security-10272025-fixes]
* Fixes missing accessibility announcements in form rows [#240132]({{kib-pull}}240132)
* Improves the **Cases** table loading behavior to prevent flashing [#240155]({{kib-pull}}240155)
* Fixes a bug in Lens that incorrectly assigned unsaved data view references [#239431]({{kib-pull}}239431)
* Fixes an error when selecting the `(blank)` value in options lists [#239791]({{kib-pull}}239791)
* Pauses fetch operations until initialization completes [#239228]({{kib-pull}}239228)
* Fixes a bug that prevented users from resetting unsaved changes when enabling **timeRestore** and setting a time range [#239992]({{kib-pull}}239992)
* Fixes a search session restoration issue [#239822]({{kib-pull}}239822)
* Allows {{fleet}} setup retries on start in all environments [#240342]({{kib-pull}}240342)
* Adds **FORK with KEEP/STATS** options to transformational commands [#240011]({{kib-pull}}240011)
* Fixes dependencies and service map issues for `txn == exit-span` use cases [#235392]({{kib-pull}}235392)
* Fixes the model label display in AI Assistant Settings [#239824]({{kib-pull}}239824)
* Updates the **Open in Discover** query in the related Logs section of the **Overview** tab [#240409]({{kib-pull}}240409)
* Fixes an issue where the Onboarding Integrations list wasn’t fetched for all pages [#239709]({{kib-pull}}239709)
* Fixes an issue where schedules couldn’t be created with **Cases** as the connector type [#239748]({{kib-pull}}239748)
* Fixes an issue where operators couldn’t be removed after selection in the **Add rule exception** flyout [#236051]({{kib-pull}}236051)
* Fixes `react-query` ID collision issues [#240517]({{kib-pull}}240517)
* Updates GenAI Settings to reflect the selected `AI Assistants Visibility` value from the header selector on the Settings page [#239555]({{kib-pull}}239555)
* Fixes the Inference endpoints UI to ensure the list loads correctly when the provider is custom [#240189]({{kib-pull}}240189)
* Fixes the URL in **Disk Usage** alerting rules [#240279]({{kib-pull}}240279)
* Fixes data preview metadata pop-up display issues by adding a tooltip and copy button to handle long IDs [#239768]({{kib-pull}}239768)
* Fixes the **Agents** and **Playground** icons in the side navigation to render correctly in dark mode [#240475]({{kib-pull}}240475)
* Ensures only valid queries are returned for significant events [#239501]({{kib-pull}}239501)
* Hides filtering capabilities in Hosts Metrics [#239724]({{kib-pull}}239724)

## October 20, 2025 [serverless-changelog-10202025]

### Features and enhancements [serverless-changelog-10202025-features-enhancements]

* [Agent Builder](/solutions/search/elastic-agent-builder.md) is now available in technical preview and is enabled by default on {{serverless-full}}
* Lets you remove root privileges from {{fleet}} managed agents [#237790]({{kib-pull}}237790)
* Adds the `xpack.fleet.experimentalFeatures` setting [#238840]({{kib-pull}}238840)
* Supports expression suggestions within function parameters [#236343]({{kib-pull}}236343)
* Updates the Observability Serverless navigation menu [#235984]({{kib-pull}}235984)
* Allows the Observability AI Assistant to retrieve information from the  `.integration_knowledge*` system index [#237085]({{kib-pull}}237085)
* Adds file download relative URI to response actions that provide file output [#237713]({{kib-pull}}237713)
* Updates the UI and API for process descendants in trusted applications [#236318]({{kib-pull}}236318)
* Adds usage statistics collection for CSPM cloud connectors [#236992]({{kib-pull}}236992)
* Enhances the error message for malformed roles [#239098]({{kib-pull}}239098)
* Enables editing feature condition in the feature identification flyout and adds the **Open in Discover** button [#238646]({{kib-pull}}238646)
* Improves processing warnings for Streams [#239188]({{kib-pull}}239188)
* Enables AI-powered significant event identification for Streams [#239070]({{kib-pull}}239070)
* Enables numerical ID service for Cases [#238555]({{kib-pull}}238555)
* Adds agent ID as a default observables type [#238533]({{kib-pull}}238533)


### Fixes [serverless-changelog-10202025-fixes]

* Updates `nodemailer` [#238816]({{kib-pull}}238816)
* Improves error handling on the **Visualize Listing** page [#238355]({{kib-pull}}238355)
* Prevents adhoc dataviews in {{esql}} charts from being filtered out in the KQL search bar [#238731]({{kib-pull}}238731)
* Fixes a bug in Lens that broke **Click to filter** on table rows when any column was used as a formula [#239222]({{kib-pull}}239222)
* Fixes metric color assignment when breakdown and a max dimension are defined in Lens [#238901]({{kib-pull}}238901)
* Fixes "package not found" error when skipping cloud onboarding for a prerelease package [#238629]({{kib-pull}}238629)
* Fixes an issue with integration policy upgrades [#238542]({{kib-pull}}238542)
* Fixes `ignore_above` mapping for `flattened` fields [#238890]({{kib-pull}}238890)
* Fixes missing fields when using combined filters with the `ignoreFilterIfFieldNotInIndex` UI setting [#238945]({{kib-pull}}238945)
* Displays the available options when editing an existing variable control [#239315]({{kib-pull}}239315)
* Fixes `KEEP` behavior in {{esql}} when a query initially returns no results [#239063]({{kib-pull}}239063)
* Adds a 10 second request timeout to {{esql}} query execution [#238200]({{kib-pull}}238200)
* Uses `runWithCache` for bulk {{fleet}} operations [#238326]({{kib-pull}}238326)
* Fixes error when Observability AI Assistant was disabled [#238811]({{kib-pull}}238811)
* Removes unecessary `_source` field from queries [#239205]({{kib-pull}}239205)
* Makes the rule condition chart parser replace metric names inside filter values (e.g., A in "Accounts") [#238849]({{kib-pull}}238849)
* Fixes recover alert while monitor is down [#237479]({{kib-pull}}237479)
* Fixes layout of SLO management page combo box filter [#239418]({{kib-pull}}239418)
* Adds missing aria-label to BetaBadge component [#239400]({{kib-pull}}239400)
* Fixes the "missing authentication credentials" issue in `TelemetryConfigWatcher` and `PolicyWatcher` [#237796]({{kib-pull}}237796)
* Fixes an issue with Automatic Migration that prevented you from switching between migrations while translating rules [#238679]({{kib-pull}}238679)
* Fixes artifacts spaces migration (`v9.1`) to ensure all artifacts are processed [#238740]({{kib-pull}}238740)
* Checks for integrations permissions before loading component [#239122]({{kib-pull}}239122)
* Prioritizes connector `defaultModel` over stored conversation model [#237947]({{kib-pull}}237947)
* Deselects current selection after index pattern update [#239245]({{kib-pull}}239245)
* Fixes graph not rendering when switching tabs or refreshing the page [#238038]({{kib-pull}}238038)
* Adds unique accessible labels for **Show top field values** buttons [#237972]({{kib-pull}}237972)
* Fixes tool calling unavailable tools [#237174]({{kib-pull}}237174)
* Adds Jira's `otherFields` JSON editor to case creation flow [#238435]({{kib-pull}}238435)
* Updates connector API [#236863]({{kib-pull}}236863)
* Separates sync alert and auto-extract updates in activity log [#236519]({{kib-pull}}236519)
* Fixes auto extraction of observables in EASE [#239000]({{kib-pull}}239000)
* Removes `autoFocus` to preserve proper focus upon modal close [#239366]({{kib-pull}}239366)
* Adds manual focus to the Cases action button's actions [#239504]({{kib-pull}}239504)
* Fixes the behavior of Security serverless projects' Tier 1 and Tier 2 analyst roles by revoking their Endpoint exceptions read access

## October 15, 2025 [serverless-changelog-10152025]
* {{serverless-full}} is now available in two new Amazon Web Services [regions](/deploy-manage/deploy/elastic-cloud/regions.md): `ap-northeast-1` (Tokyo) and `eu-west-2` (London)


## October 13, 2025 [serverless-changelog-10132025]

### Features and enhancements [serverless-changelog-10132025-features-enhancements]

* Adds a **Show agentless resources** toggle on the Fleet > Settings page for debugging and diagnostics [#237528]({{kib-pull}}237528)
* Allows you to carry over the controls when navigating to a dashboard, preserving the histogram [#237070]({{kib-pull}}237070)
* Enables the risk score reset feature [#237829]({{kib-pull}}237829)
* Uses {{esql}} for calculating risk scores [#237871]({{kib-pull}}237871)
* Adds Security ML modules for GCP Audit and Azure Activity Logs [#236849]({{kib-pull}}236849)
* Removes the global empty state redirect [#237612]({{kib-pull}}237612)
* Replaces the existing document count chart with RED metrics [#236635]({{kib-pull}}236635)

### Fixes [serverless-changelog-10132025-fixes]

* Fixes an error that occurred when deleting orphaned integration policies [#237875]({{kib-pull}}237875)
* Prevents creation of default alerts when no connectors are defined [#237504]({{kib-pull}}237504)
* Turns off the maximum attempts limit for the private locations sync task [#237784]({{kib-pull}}237784)
* Fixes a flyout rendering issue [#237840]({{kib-pull}}237840)
* Corrects icon colors in the side navigation [#237970]({{kib-pull}}237970)
* Fixes a bug that affected the controls on the Alerts page [#236756]({{kib-pull}}236756)
* Updates the names of the **Security solution default** and **Security solution alerts** data views in the data view picker [#238354]({{kib-pull}}238354)
* Fixes a bug that caused the flyout on the Files management page to crash when there were uploaded files [#237588]({{kib-pull}}237588)
* Introduces a separate error message for empty login attempts with `saml/oidc` providers [#237611]({{kib-pull}}237611)
* Fixes an issue in the component template creation flow where creating a new template with an `@custom` suffix in its name could incorrectly update mappings for unrelated data streams and trigger rollover prompts [#237952]({{kib-pull}}237952)
* Fixes an issue where the retriever query copied from the **Search your data** JavaScript tutorial failed with `parsing_exception` when passed as a query parameter in the Node.js client; retriever queries are now passed in the request body to ensure correct serialization [#237654]({{kib-pull}}237654)
* Ensures the Index management mappings editor synchronizes the model deployment status correctly [#237812]({{kib-pull}}237812)
* Fixes an accessibility issue where resetting changes or removing all terms in the Synonyms panel was not announced by screen readers [#237877]({{kib-pull}}237877)
* Fixes an issue in the RAG Playground where invalid fields were highlighted but no error message appeared [#238284]({{kib-pull}}238284)
* Improves the performance of the clustering algorithm [#238394]({{kib-pull}}238394)


## October 6, 2025 [serverless-changelog-10062025]

### Features and enhancements [serverless-changelog-10062025-features-enhancements]
* Adds support for encrypted headers in the Webhook connector to enhance security [#233695]({{kib-pull}}233695)
* Allows users to add custom fields to the IBM Resilient connector [#236144]({{kib-pull}}236144)
* Renames Fleet Server Host SSL options for clarity [#236887]({{kib-pull}}236887)
* Enables Discover tabs by default, allowing you to manage multiple data explorations in parallel [#235150]({{kib-pull}}235150)
* Automatically extracts case observables in the **Add to case** workflow [#233027]({{kib-pull}}233027)
* Introduces missing icons and updates v2 icons for the ECH Observability navigation [#236808]({{kib-pull}}236808)
* Adds a metrics dashboard for non-EDOT agents in the OpenTelemetry native ingestion path [#236978]({{kib-pull}}236978)
* Adds public APIs for Attack Discovery and Attack Discovery schedules [#236736]({{kib-pull}}236736)
* Enables automatic observable extraction in the Alerts table [#235433]({{kib-pull}}235433)
* Turns on the `newDataViewPickerEnabled` feature flag [#234101]({{kib-pull}}234101)
* Adds the ability to discover privileged users from the Entity Analytics Okta integration [#237129]({{kib-pull}}237129)
* Allows you to select which AI Assistant to show in the Elastic header; moves the **AI Assistant visibility** setting to the **GenAI Settings** page [#233727]({{kib-pull}}233727)
* Adds a new `update_all` endpoint for product documentation management [#231884]({{kib-pull}}231884)
* Adds an icon for Contextual AI in the AI Connector and Inference endpoint creation UI [#236951]({{kib-pull}}236951)
* Enables the new background search experience for improved performance [#236818]({{kib-pull}}236818)
* Adds triple-quote support to the Manual Ingest Pipeline Processor editor [#236595]({{kib-pull}}236595)
* Introduces the German locale for Kibana in `beta` [#236903]({{kib-pull}}236903)
* Adds an advanced option to disable filtering of file-backed volumes and CD-ROMs in the **Device Control** plugin [#236620]({{kib-pull}}236620)

### Fixes [serverless-changelog-10062025-fixes]
* Rolls over the reporting data stream automatically when a newer template version is available [#234119]({{kib-pull}}234119)
* Fixes an issue where exported CSV columns in Lens tables could appear out of order [#236673]({{kib-pull}}236673)
* Fixes a bug causing Controls to fetch data twice [#237169]({{kib-pull}}237169)
* Removes the incorrect `fleet.ssl` configuration option [#236788]({{kib-pull}}236788)
* Fixes MSI commands (#233750) [#236994]({{kib-pull}}236994)
* Removes unnecessary span documents from the `getServiceAgent` function [#236732]({{kib-pull}}236732)
* Cleans up extra Synthetics package policies [#235200]({{kib-pull}}235200)
* Reverts a change to the page attachment type in {{obs-serverless}} [#236958]({{kib-pull}}236958)
* Removes `null` values in the confirmation dialog when bulk-editing index patterns for rules [#236572]({{kib-pull}}236572)
* Increases the z-index of Timeline and related flyout components so they appear above the side navigation [#236655]({{kib-pull}}236655)
* Adds support for API key wildcard search [#221959]({{kib-pull}}221959)
* Hides the **Show forecast** button when changing jobs in the Single Metric Viewer [#236724]({{kib-pull}}236724)
* Improves performance of the Trained Models list [#237072]({{kib-pull}}237072)
* Fixes partition field settings errors in the Single Metric Viewer dashboard panels [#237046]({{kib-pull}}237046)
* Fixes layout issues with the **Parse in streams** button on smaller flyouts [#236548]({{kib-pull}}236548)
* Displays `(missing value)` and `(empty)` instead of `null` in charts and tables [#233369]({{kib-pull}}233369)
* Fixes privilege requirements for reindexing indices in Upgrade Assistant [#237055]({{kib-pull}}237055)


## September 29, 2025 [serverless-changelog-09292025]

### Features and enhancements [serverless-changelog-09292025-features-enhancements]

* Updates the Observability navigation menu [#236001]({{kib-pull}}236001)
* Enables cancelling response actions sent to hosts running Microsoft Defender Endpoint [#230399]({{kib-pull}}230399)
* Adds each alert's reason for closing to the Alerts page [#226590]({{kib-pull}}226590)
* Adds the Endpoint exceptions sub-privilege [#233433]({{kib-pull}}233433)
* Updates the source saved object schema to enable integrations sync markers [#236457]({{kib-pull}}236457)
* Updates the indicator details flyout [#230593]({{kib-pull}}230593)
* Adds an advanced policy `windows.advanced.firewall_anti_tamper` that lets you set the firewall anti-tamper plugin to off or detect-only [#236431]({{kib-pull}}236431)
* Displays document count chart for {{esql}} categorize queries [#231459]({{kib-pull}}231459)
* Lets you manually map new fields from the schema editor [#235919]({{kib-pull}}235919)
* Adds AI-generative partition suggestions to Streams [#235759]({{kib-pull}}235759)
* In Streams, allows you to create routing conditions directly from preview table cells [#235560]({{kib-pull}}235560)
* Adds an option to convert an index to a lookup index to the **Manage index** menu [#233998]({{kib-pull}}233998)
* Improves code examples in the Synonyms UI [#235944]({{kib-pull}}235944)
* Automatically copies source data into the alerts-as-data documents for other ES Query rule types [#230010]({{kib-pull}}230010)
* Replaces the dashboard editor toolbar with the **Add** menu [#230324]({{kib-pull}}230324)
* Adds support for package spec v3.5 [#235942]({{kib-pull}}235942)
* Adds in-product documentation for the {{esql}} `FORK` command [#236494]({{kib-pull}}236494)
* Adds **View in discover** button in alert details page for SLO burn rate and ES query rules [#233855]({{kib-pull}}233855)

### Fixes [serverless-changelog-09292025-fixes]

* Adjusts **Cancel** button height in Discover's tabs enabled view [#236118]({{kib-pull}}236118)
* Fixes dashboard title not updating when edited from content editor [#236561]({{kib-pull}}236561)
* Adds a unique count to transforms on the integrations overview to fix overcounting error [#236177]({{kib-pull}}236177)
* Fixes malformed synthetics package policies [#236176]({{kib-pull}}236176)
* Fixes controls trigger across various commands [#236121]({{kib-pull}}236121)
* Reverts filter policy inputs [#236104]({{kib-pull}}236104)
* Fixes the multiselect issue inside the toolbar selector when search is used [#236091]({{kib-pull}}236091)
* Integrates dataview logic into host KPIs charts [#236084]({{kib-pull}}236084)
* Fixes integrations RAG [#234211]({{kib-pull}}234211)
* Ensures the data view picker icon is always vertically centered [#236379]({{kib-pull}}236379)
* Fixes browser fields cache [#234381]({{kib-pull}}234381)
* Fixes the URL passed to detection rule actions via the `{{context.results_link}}` placeholder [#236067]({{kib-pull}}236067)
* Refactors `nav_control_popover` [#235780]({{kib-pull}}235780)
* Allows `xpack.spaces.defaultSolution` to be configured via docker [#236570]({{kib-pull}}236570)
* Fixes the Job details fly-out on the Analytics Map page [#236131]({{kib-pull}}236131)
* Limits `msearch` usage for log rate analysis [#235611]({{kib-pull}}235611)
* Fixes display of alerts from anomaly detection rules in [#236289]({{kib-pull}}236289)
* Adds `time` field to the get data views response schema [#235975]({{kib-pull}}235975)
* Adds `managed` field to the get data views response schema [#236237]({{kib-pull}}236237)
* Validates {{ls}} pipeline IDs sent to Kibana APIs [#236347]({{kib-pull}}236347)


## September 22, 2025 [serverless-changelog-09222025]

### Features and enhancements [serverless-changelog-09222025-features-enhancements]

* Adds a new connector for Jira Service Management [#235408]({{kib-pull}}235408)
* Adds OAuth2 client credentials authentication support to {{kib}} Webhook connectors [#218442]({{kib-pull}}218442)
* Completes OTel configuration pipelines by adding an exporter [#233090]({{kib-pull}}233090)
* Enables controls in Discover from the editor [#229598]({{kib-pull}}229598)
* Displays errors in the context of a trace [#234178]({{kib-pull}}234178)
* Creates functional tests for the Logs Essentials tier [#234904]({{kib-pull}}234904)
* Sets up the saved object infrastructure for Cloud Connectors and implements the end-to-end persistence flow for creating integrations with Cloud Connector support [#230137]({{kib-pull}}230137)
* Removes the **Tech Preview** badge and feature flag for Automatic Troubleshooting [#234853]({{kib-pull}}234853)
* Adds advanced options for opting out of collecting ransomware diagnostics on macOS [#235193]({{kib-pull}}235193)
* Adds the **Tech Preview** badge for the preconfigured `rerank` endpoint in the inference endpoints UI [#235222]({{kib-pull}}235222)
* Adds a default placeholder icon for future AI connectors [#235166]({{kib-pull}}235166)
* Adds search functionality to the Query rules details page [#232579]({{kib-pull}}232579)
* Adds a link to Agent Builder in the **View Data** dropdown [#234679]({{kib-pull}}234679)
* Adds the AutoOps Search tier page, which provides project-level insights and deeper insights into {{serverless-short}} resources (VCUs) and performances
% Relates to https://github.com/elastic/autoops/issues/20 and https://github.com/elastic/autoops/issues/200

### Fixes [serverless-changelog-09222025-fixes]

* Skips automatic scrolling when a panel is visible [#233226]({{kib-pull}}233226)
* Fixes an issue with the Actions column header size [#235227]({{kib-pull}}235227)
* Clears time field sorting when switching from classic to {{esql}} mode [#235338]({{kib-pull}}235338)
* Fixes a bug where previously installed product docs (E5) were not upgraded during a Kibana version upgrade [#234792]({{kib-pull}}234792)
* Improves the accessibility of the badges on individual stream pages [#235625]({{kib-pull}}235625)
* Fixes the autocomplete configuration for the `pinned` retriever by removing the `match_criteria` field [#234903]({{kib-pull}}234903)
* Fixes a bug by allowing the use of `cmd + /` for comment toggling in the Monaco editor [#235334]({{kib-pull}}235334)
* Adds a check for all privileges for {{sec-serverless}} when creating lists [#234602]({{kib-pull}}234602)


## September 19, 2025 [serverless-changelog-09192025]

### Features and enhancements [serverless-changelog-09192025-features-enhancements]
* {{serverless-full}} is now available in three new Google Cloud Platform [regions](/deploy-manage/deploy/elastic-cloud/regions.md): GCP South Carolina (`us-east1`), GCP Virginia (`us-east4`), and GCP Oregon (`us-west1`).


## September 15, 2025 [serverless-changelog-09152025]

### Features and enhancements [serverless-changelog-09152025-features-enhancements]

* Improves the {{esql}} suggestions logic when a query changes [#231767]({{kib-pull}}231767)
* Updates the appearance popover in Lens metric charts [#233992]({{kib-pull}}233992)
* Adds support for installing `alerting_rule_template` assets from packages [#233533]({{kib-pull}}233533)
* Removes the default query limit of 10 [#234349]({{kib-pull}}234349)
* Adds support for remote cluster lookup mode indices in the editor [#232907]({{kib-pull}}232907)
* Extends {{esql}} autocomplete to include columns from lookup indices and enrichment policies after `LOOKUP JOIN` and `ENRICH` commands [#233221]({{kib-pull}}233221)
* Adds a trace waterfall visualization for logs [#234072]({{kib-pull}}234072)
* Adds end-to-end UI tests for onboarding page validation [#232363]({{kib-pull}}232363)
* Updates the Playwright end-to-end tests to support Logs Essentials tier functionality [#234644]({{kib-pull}}234644)
* Introduces a Security Risk Scoring AI Assistant tool [#233647]({{kib-pull}}233647)
* Enables the SentinelOne `runscript` response action [#234492]({{kib-pull}}234492)
* Extends the `origin_info_collection` advanced policy setting to include `origin_url`, `origin_referrer_url`, and `Ext.windows.zone_identifier` fields for Windows process events [#234268]({{kib-pull}}234268)
* Restricts access to the Value report page to `admin` and `soc_manager` roles in complete tier [#234377]({{kib-pull}}234377)
* Ensures the **Tech Preview** badge is shown for the default inference endpoint for e5 on the inference endpoints UI [#234811]({{kib-pull}}234811)
* Ensures mapped fields are remembered across simulations [#233799]({{kib-pull}}233799)

### Fixes [serverless-changelog-09152025-fixes]

* Hides the side navigation during report generation [#234675]({{kib-pull}}234675)
* Fixes a bug where the save modal allowed duplicate saves of dashboards, visualizations, and other assets [#233933]({{kib-pull}}233933)
* Fixes an issue with special character handling when creating a pipeline from the flyout [#233651]({{kib-pull}}233651)
* Fixes a bug where the toggle column only worked on the Alerts page [#234278]({{kib-pull}}234278)
* Correctly updates the `@timestamp` and `event.ingested` fields when a privileged user is updated [#233735]({{kib-pull}}233735)
* Returns a `500` response code if there is an error during monitoring engine initialization [#234368]({{kib-pull}}234368)
* Fixes table highlighting issues in flyouts [#234222]({{kib-pull}}234222)
* Fixes issues in AI Assistant where it didn't append conversation messages or update titles [#233219]({{kib-pull}}233219)
* Enables repeated System Prompt navigation from the **Conversations** tab [#234812]({{kib-pull}}234812)
* Increases the `bulkGet` limit [#234151]({{kib-pull}}234151)
* Fixes an issue on the API Keys Management page that occurred when loading API keys with null names [#234083]({{kib-pull}}234083)
* Fixes an Anomaly Detection bug where custom URLs omitted generated fields in datafeed preview requests [#234709]({{kib-pull}}234709)
* Ensures full tool traces are displayed in flyouts [#234654]({{kib-pull}}234654)

## September 8, 2025 [serverless-changelog-09082025]

### Features and enhancements [serverless-changelog-09082025-features-enhancements]

* Makes maintenance windows globally available [#233870]({{kib-pull}}233870)
* Updates `@elastic/charts` to 71.0.0 and enables new metric chart in Lens [#229815]({{kib-pull}}229815)
* Adds toggle that grants permission for agents to write to `logs` datastream [#233374]({{kib-pull}}233374).
* Adds Knowledge Base integration support [#230107]({{kib-pull}}230107)
* Adds support for duration variable type to {{fleet}} [#231027]({{kib-pull}}231027)
* Uses native function calling for self-managed LLMs [#232109]({{kib-pull}}232109)
* Unifies installation settings and improves status display for AI Assistant's Knowledge Base & product documentation [#232559]({{kib-pull}}232559)
* Links dashboards to SLO [#233265]({{kib-pull}}233265)
* Disables add-to-case functionality when all selected alerts are already attached [#231877]({{kib-pull}}231877)
* Disables save button on empty input [#233184]({{kib-pull}}233184)
* Adds **View in discover** button to alert details header [#233259]({{kib-pull}}233259)
* Adds `send_traces`, `send_metrics`, and `send_logs` agent configuration settings for EDOT Node.js [#233798]({{kib-pull}}233798)
* Updates missing index pattern table action [#233258]({{kib-pull}}233258)
* Shows trace context for logs [#232784]({{kib-pull}}232784)
* Adds IPv6 support to address fields in the Remote Clusters UI [#233415]({{kib-pull}}233415)
* Updates the {{es-serverless}} project creation in the UI to use the general purpose profile.
  The API continues to support alternative `optimized_for` options. Refer to [](/deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md#elasticsearch-billing-managing-elasticsearch-costs).
  % Relates to https://github.com/elastic/cloud/pull/146418


### Fixes [serverless-changelog-09082025-fixes]

* Fixes resize bug [#233755]({{kib-pull}}233755)
* Fixes the page height of the Observability AI Assistant page [#233924]({{kib-pull}}233924)
* Updates kibana MITRE data to `v17.1` [#231375]({{kib-pull}}231375)
* Fixes import of endpoint exceptions [#233142]({{kib-pull}}233142)
* Fixes a bug that affected display of mitre attack data [#233805]({{kib-pull}}233805).
* Prevents users who don't have crud privilege from deleting notes [#233948]({{kib-pull}}233948).
* Fixes rule editor flyout for Anomaly Explorer when no filter lists have been configured [#233085]({{kib-pull}}233085)
* Fixes `FormattedMessage` rendering escaped HTML instead of markup [#234079]({{kib-pull}}234079)


## September 1, 2025 

### Features and enhancements [serverless-changelog-09012025-features-enhancements]

* Allows users to configure index settings when importing geospatial files in **File Upload** [#232308]({{kib-pull}}232308)
* Adds tooltip support for the {{esql}} layer [#232147]({{kib-pull}}232147)
* Enables automatic content package installation when matching datasets are ingested using the `enableAutoInstallContentPackages` feature flag [#232668]({{kib-pull}}232668)
* Increases query history capacity to store more than 20 queries [#232955]({{kib-pull}}232955)
* Improves validation for functions in query inputs [#230139]({{kib-pull}}230139)
* Adds support for native function calling schema to the OpenAI connector when the API provider is set to "Other" [#232097]({{kib-pull}}232097)
* Retries inference calls when aborted due to transient errors [#232610]({{kib-pull}}232610)
* Adds the `raw_request` field to traces for better debugging [#232229]({{kib-pull}}232229)
* Adds dashboard references to SLO saved objects [#232583]({{kib-pull}}232583)
* Displays span links when APM indices are available [#232135]({{kib-pull}}232135)
* Adds a new `policy_response_failure` defend insight type [#231908]({{kib-pull}}231908)
* Enables conversation sharing in chat interfaces [#230614]({{kib-pull}}230614)
* Adds a new data view to the Privmon dashboard page [#233264]({{kib-pull}}233264)
* Improves the layout of custom URLs list in **Data Frame Analytics** [#232575]({{kib-pull}}232575)
* Adds icons for **AI21 Labs** and **Llama Stack** to the AI connector/inference endpoints creation UI [#232098]({{kib-pull}}232098)
* Ensures consistent Grok pattern generation across features [#230076]({{kib-pull}}230076)

### Fixes [serverless-changelog-09012025-fixes]

* Ensures that maintenance windows with scoped queries apply to all rule types [#232307]({{kib-pull}}232307)
* Fixes pagination issues in alerting tables [#233030]({{kib-pull}}233030)
* Removes unused `availableOptions` from {{esql}} values in query saved objects [#231690]({{kib-pull}}231690)
* Removes unnecessary output warning messages in {{serverless-short}} deployments [#232785]({{kib-pull}}232785)
* Requires the `agents:all` privilege to use **Manage auto-upgrade agent** UI actions [#232429]({{kib-pull}}232429)
* Fixes read permission failures on the lookup indexes route [#233282]({{kib-pull}}233282)
* Refactors anonymization logic to walk JSON objects instead of stringifying them [#232319]({{kib-pull}}232319)
* Disables the **Save** button until a file is detected [#233141]({{kib-pull}}233141)
* Adds a missing **Alert details actions** button to the UI [#233113]({{kib-pull}}233113)
* Prevents SessionView crashes by normalizing event process arguments [#232462]({{kib-pull}}232462)
* Adds maximum function call limits to prevent recursive tool invocations [#231719]({{kib-pull}}231719)
* Ensures validation logic so the Elastic Managed LLM behaves as expected during testing [#231873]({{kib-pull}}231873)
* Fixes the **Restore status** tab display for system indices [#232839]({{kib-pull}}232839)
* Fixes responsiveness issues in the Stream management code editor area [#232630]({{kib-pull}}232630)
* Fixes an empty tooltip issue when creating tags [#232853]({{kib-pull}}232853)
* Fixes an issue where the **Create tag** modal wouldn't close properly [#233012]({{kib-pull}}233012)

## August 28, 2025 [serverless-changelog-08282025]

### Features and enhancements [serverless-changelog-08282025-features-enhancements]

* {{serverless-full}} is now available in three new Microsoft Azure [regions](/deploy-manage/deploy/elastic-cloud/regions.md): 
    * `northeurope` (North Europe), located in Ireland 
    * `australiaeast` (Australia East), located in Victoria, Australia
    * ` westus2` (West US 2), located in Washington, United States



## August 25, 2025 [serverless-changelog-08252025]

### Features and enhancements [serverless-changelog-08252025-features-enhancements]
* Adds support for a new `url` variable type in {{fleet}} packages, enabling improved input validation of URL values [#231062]({{kib-pull}}231062)
* Adds the `kibana.alert.grouping` field to the **Synthetics monitor status** rule in {{obs-serverless}}  [#230513]({{kib-pull}}230513)
* Enables polling and sampling for EDOT central configuration in {{obs-serverless}} [#231835]({{kib-pull}}231835)
* Adds a check to confirm that uploaded files are indexed and searchable in {{ml-cap}} [#231614]({{kib-pull}}231614)
* Updates sections and improves field handling in {{ml-cap}} [#231037]({{kib-pull}}231037)
* Improves the layout of the custom URLs list in {{ml-cap}} [#231751]({{kib-pull}}231751)

### Fixes [serverless-changelog-08252025-fixes]
* Fixes a rendering issue that affected progress elements in Canvas [#232432]({{kib-pull}}232432)
* Fixes the enforcement of deployment mode restrictions when creating package policies in {{fleet}} [#231679]({{kib-pull}}231679)
* Ensures transform index templates include `index.mapping.ignore_malformed: true` to prevent failures due to invalid values in source indices in {{fleet}} [#232439]({{kib-pull}}232439)
* Fixes visibility issues with the DocViewer flyout in **Saved Search** embeddables in Discover [#229108]({{kib-pull}}229108)
* Restores legacy monitor filters in {{obs-serverless}} [#231562]({{kib-pull}}231562)
* Handles multi-line values more reliably in {{obs-serverless}} [#230929]({{kib-pull}}230929)
* Fixes broken views on AI Assistant settings pages for non-Enterprise license holders in {{obs-serverless}} [#231989]({{kib-pull}}231989)
* Enables the recovery strategy toggle for monitor status rules in {{obs-serverless}} [#231091]({{kib-pull}}231091)
* Fixes AI Assistant anonymization rules to avoid nested or overlapping masks when processing text in {{obs-serverless}} [#231981]({{kib-pull}}231981)
* Fixes an issue that prevented the contextual flyout from showing full details in vulnerability findings in {{sec-serverless}} [#231778]({{kib-pull}}231778)
* Includes various bug fixes and improvements to the Manifest Manager in {{sec-serverless}} [#231039]({{kib-pull}}231039)
* Fixes an issue where the `unusedUrlsCLeanupTask` run interval did not update correctly when changed [#231883]({{kib-pull}}231883)
* Updates the prompt text for the `mv_slice` feature in {{ml-cap}} [#231870]({{kib-pull}}231870)
* Fixes a broken link in the **Build** breadcrumb that incorrectly pointed to the search indices page in {{es-serverless}} [#232504]({{kib-pull}}232504)
* Fixes inconsistencies in case activity statistics [#231948]({{kib-pull}}231948)
* Adds support for a `reporting_user` role with a reserved set of privileges [#231533]({{kib-pull}}231533)



## August 18, 2025 [serverless-changelog-08182025]

### Features and enhancements [serverless-changelog-08182025-features-enhancements]

* Removes the category selection step when adding filters to maintenance windows so you can add filters to maintenance windows based on alert fields from all solutions [#227888]({{kib-pull}}227888)
* Adds the ability to see all available log events in the shared logs overview even when ML features are not available [#225785]({{kib-pull}}225785)
* Improves Gemini prompts [#223476]({{kib-pull}}223476)
* Improves the AI Assistant Settings page by adding solution-specific logos [#224906]({{kib-pull}}224906)
* Enables the `trustedAppsAdvancedMode` feature flag by default [#230111]({{kib-pull}}230111)
* Updates the PrivMon UX [#231921]({{kib-pull}}231921)
* Improves error messages when your {{kib}} session fails to refresh a token [#231118]({{kib-pull}}231118)
* Adds inline markdown visualization [#229191]({{kib-pull}}229191)
* Adds an `AI` section to the `Stack Management` menu [#227289]({{kib-pull}}227289)
* Sets the default retention period for Logs anomaly detection to 120 days [#231080]({{kib-pull}}231080)


### Fixes [serverless-changelog-08182025-fixes]

* Fixes a bug that stopped reports from spaces with a dash in them from appearing in the reporting list [#230876]({{kib-pull}}230876)
* Fixes Timeslider focus ring visibility in Firefox [#231351]({{kib-pull}}231351)
* Fixes error handling in the Links panel's **Save to library** modal [#231168]({{kib-pull}}231168)
* Fixes keyboard interaction on range slider control [#230893]({{kib-pull}}230893)
* Fixes older color mapping configuration in Lens [#231563]({{kib-pull}}231563)
* Fixes lost references when returning to unsaved dashboards with reference panels [#231517]({{kib-pull}}231517)
* Fixes rendering of aggregate metric fields in {{esql}} mode [#231481]({{kib-pull}}231481)
* Disables sorting for json-like fields in {{esql}} mode [#231289]({{kib-pull}}231289)
* Fixes a bug affecting the Inventory date picker's state [#231141]({{kib-pull}}231141)
* Fixes title generation for the Observability AI Assistant in conversations with self-managed LLMs [#231198]({{kib-pull}}231198)
* Fixes an endless loop that could occur during {{esql}} `LOOKUP JOIN`s [#231217]({{kib-pull}}231217)
* Adjusts the Kubernetes OTel test to work in serverless nightly workflow [#231462]({{kib-pull}}231462)
* Updates the `ContentManagement` plugin to enable linked dashboards in more places [#229685]({{kib-pull}}229685)
* Provides the `aria-labelledby` attribute to the **Add cases** selector modal [#231887]({{kib-pull}}231887)
* Fixes incorrect threat enrichment for partially matched `AND` conditions in IM rules [#230773]({{kib-pull}}230773)
* Fixes Benchmark page accessibility issues [#229521]({{kib-pull}}229521)
* Fixes an issue that prevented the creation of Knowledge Base `Index` entries in deployments with a large number of indices and mappings [#231376]({{kib-pull}}231376)
* Fixes an index sync bug that prevented deletion of stale users [#229789]({{kib-pull}}229789)
* Fixes custom field grouping options in the Alerts table [#230121]({{kib-pull}}230121)
* Fixes a bug that made the {{esql}} form read-only in the Rule upgrade flyout [#231699]({{kib-pull}}231699)
* Removes the default port the from interactive setup cluster address form, unless specified [#230582]({{kib-pull}}230582)
* Fixes positioning of the **Add rule** popover on the Role Mappings page [#231551]({{kib-pull}}231551)

## August 11, 2025 [serverless-changelog-08112025]

### Features and enhancements [serverless-changelog-08112025-features-enhancements]
* Adds **DOES NOT MATCH** capability to the IM rule type in Elastic Security Serverless [#227084]({{kib-pull}}227084)
* Adds Automatic Import documentation links to log descriptions and error messages [#229375]({{kib-pull}}229375)
* Improves dashboard usability at 400% zoom [#228978]({{kib-pull}}228978)
* Adds an **unsaved changes** modal in Discover [#225252]({{kib-pull}}225252)
* Adds a recovery mode switch for status alerts in Elastic Observability Serverless [#229962]({{kib-pull}}229962)
* Adds an error parameter to the agent config API in Elastic Observability Serverless [#230298]({{kib-pull}}230298)
* Adds an inference timeout to anonymization settings in Elastic Observability Serverless [#230640]({{kib-pull}}230640)
* Fetches referenced panels when loading dashboards in Elastic Observability Serverless [#228811]({{kib-pull}}228811)
* Installs product docs with KB installation in Elastic Observability Serverless [#228695]({{kib-pull}}228695)
* Links from alert details to related dashboards now include a time range filter in Elastic Observability Serverless [#230601]({{kib-pull}}230601)
* Updates the default Gemini model for the Gemini Connector in Playground from Gemini 1.5 Pro to Gemini 2.5 Pro in Elasticsearch Serverless [#230457]({{kib-pull}}230457)

### Fixes [serverless-changelog-08112025-fixes]
* Removes unnecessary promises in dashboards [#230313]({{kib-pull}}230313)
* Fixes date math plus sign encoding in dashboards [#230469]({{kib-pull}}230469)
* Logs a warning if filter and query state are malformed in dashboards [#230088]({{kib-pull}}230088)
* Fixes duplicate panel action hangs when a dashboard has collapsed sections closed on page load [#230842]({{kib-pull}}230842)
* Fixes a screen reader–only header for accessibility in dashboards [#230470]({{kib-pull}}230470)
* Fixes missing validation errors in the package policy editor in Fleet [#229932]({{kib-pull}}229932)
* Fixes agentless integrations where `organization`, `division`, or `team` data fields were being overwritten by package metadata in Fleet [#230479]({{kib-pull}}230479)
* Fixes the output SSL config order in Fleet [#230758]({{kib-pull}}230758)
* Fixes glitches in the **data view creation** flyout in Discover when accessed from another page [#228749]({{kib-pull}}228749)
* Fixes a setup bug in the Elastic Observability Serverless lock manager [#230519]({{kib-pull}}230519)
* Adds a loading state in Elastic Observability Serverless for installing or uninstalling product docs [#229579]({{kib-pull}}229579)
* Includes a timestamp range filter to exclude the frozen tier in Elastic Observability Serverless [#230375]({{kib-pull}}230375)
* Adjusts e2e onboarding tests to work in Elastic Observability Serverless [#229969]({{kib-pull}}229969)
* Moves the `scheduleNow` call to the privmon engine init instead of the monitoring source engine in Elastic Security Serverless [#230263]({{kib-pull}}230263)
* Creates the Privileged user monitoring default index source only if it doesn't already exist in Elastic Security Serverless [#229693]({{kib-pull}}229693)
* Fixes Privileged user monitoring index sync in non-default spaces in Elastic Security Serverless [#230420]({{kib-pull}}230420)
* Adds a validation error if the actions throttle is shorter than the rule interval in Elastic Security Serverless [#229976]({{kib-pull}}229976)
* Excludes deprecated features from spaces solution visibility [#230385]({{kib-pull}}230385)
* Ensures form fields persist when validation fails in Machine Learning [#230321]({{kib-pull}}230321)
* Improves accessibility of the Streams table [#225659]({{kib-pull}}225659)
* Fixes a bug that prevented saving linked TSVB visualizations when changing the data view [#228685]({{kib-pull}}228685)
* Fixes a null property error in the Elasticsearch Serverless Playground [#230729]({{kib-pull}}230729)

## August 4, 2025 [serverless-changelog-08042025]

### Features and enhancements [serverless-changelog-08042025-features-enhancements]
* Updates AGENTLESS_DISABLED_INPUTS list in Fleet [#229117]({{kib-pull}}229117)
* Enables filter and saved query options in the optional Elastic Observability Serverless query filter [#229453]({{kib-pull}}229453)
* Introduces dashboard migration endpoints in Elastic Security Serverless [#229112]({{kib-pull}}229112)
* Adds the ability to save Playgrounds within a space in Elasticsearch Serverless [#229511]({{kib-pull}}229511)
* Enhances grok semantics extraction with Onigurama regex patterns in Discover [#229409]({{kib-pull}}229409)
* Adds **Prettify** button to the editor and removes the ability to unwrap in Discover [#228159]({{kib-pull}}228159)
* Adds support for expressions in Discover STATS [#229513]({{kib-pull}}229513)
* Allows pasting screenshots into Markdown comment fields for cases in Elastic Observability Serverless [#226077]({{kib-pull}}226077)
* Adds `detection_rule_upgrade_status` to snapshot telemetry in Elastic Security Serverless [#223086]({{kib-pull}}223086)
* Adds EASE value report in Elastic Security Serverless [#228877]({{kib-pull}}228877)
* Adds Machine Learning ability to filter AI Connector providers by solution type [#228116]({{kib-pull}}228116)
* Improves Console reliability by removing odd retry logic and adding Elasticsearch host selector [#229574]({{kib-pull}}229574)
* Improves rate limiter UX [#227678]({{kib-pull}}227678)
* Adds table list view to the space selector screen [#229046]({{kib-pull}}229046)
* Adds `kibana.alert.grouping` field to infra alerts [#229054]({{kib-pull}}229054)
* Organization IdP routes are now public in the OpenAPI specifications.

### Fixes [serverless-changelog-08042025-fixes]
* Fixes loading of saved queries in the Alerting rule definition [#229964]({{kib-pull}}229964)
* Fixes dashboard panel rendering when the defer-below-the-fold setting is on and panels are focused/unfocused [#229662]({{kib-pull}}229662)
* Fixes ES|QL loading button state for long-running queries in **Lens** [#226565]({{kib-pull}}226565)
* Fixes extra padding below Advanced Options when inline editing in **Lens** [#229967]({{kib-pull}}229967)
* Improves Discover document viewer error handling where errors in one tab no longer break other tabs [#229220]({{kib-pull}}229220)
* Improves performance of breakdown field search in Discover [#229335]({{kib-pull}}229335)
* Enables **Save query** button after making changes in the Discover save query menu [#229053]({{kib-pull}}229053)
* Displays function license availability in Discover inline docs [#229961]({{kib-pull}}229961)
* Fixes incorrect filtering logic when removing a comment field in Discover [#230116]({{kib-pull}}230116)
* Modifies title generation to be scope-aware in Elastic Observability Serverless [#227434]({{kib-pull}}227434)
* Prevents destructive actions via the Elasticsearch tool in Elastic Observability Serverless [#229497]({{kib-pull}}229497)
* Replaces `EuiErrorBoundary` with `KibanaErrorBoundary` in Elastic Observability Serverless [#229710]({{kib-pull}}229710)
* Fixes keyboard accessibility for the Waterfall flyout in Elastic Observability Serverless [#229926]({{kib-pull}}229926)
* Allows knowledge base UI to work offline in Elastic Observability Serverless [#229874]({{kib-pull}}229874)
* Fixes diff display bug when importing rule customizations in Elastic Security Serverless [#228475]({{kib-pull}}228475)
* Adds missing announcements for filter in/out actions on bar charts in Elastic Security Serverless [#227388]({{kib-pull}}227388)
* Fixes toast counter badge stacking order [#229300]({{kib-pull}}229300)
* Fixes console error when adding Region map visualization for Machine Learning to a dashboard [#228669]({{kib-pull}}228669)
* Fixes product docs install logic when the target version is higher than the current version for Machine Learning [#229704]({{kib-pull}}229704)
* Adds support for the `name` attribute in create and update actions for saved objects [#228464]({{kib-pull}}228464)
* Fixes missing data view [#229467]({{kib-pull}}229467)

## July 28, 2025 [serverless-changelog-07282025]

### Features and enhancements [serverless-changelog-07282025-features-enhancements]
* Enhances the integrations overview by rendering an accordion for sample events in Data ingestion and Fleet [#228799]({{kib-pull}}228799)
* Displays related dashboard tags directly in the {{obs-serverless}} UI [#228902]({{kib-pull}}228902)
* Adds the `kibana.alert.grouping` field to {{esql}} rule definitions [#228580]({{kib-pull}}228580)
* Adds support for ingress IP filters. IP filter policies allow you to restrict traffic coming into your project to specific IP addresses or CIDR blocks.

### Fixes [serverless-changelog-07282025-fixes]
* Fixes incorrect handling of the `pollEnabled` configuration in reporting [#228707]({{kib-pull}}228707)
* Fixes an issue in Firefox where scrolling was disabled in the **Lens** editor flyout [#228625]({{kib-pull}}228625)
* Fixes an issue in Firefox that prevented scrolling in the **ES|QL** inline editor in Discover [#228849]({{kib-pull}}228849)
* Fixes an issue in *Lens* reports where PNG and PDF exports were clipped or misaligned [#228603]({{kib-pull}}228603)
* Corrects how the **Body cell lines** display option is handled when the default value is `-1` [#228697]({{kib-pull}}228697)
* Updates field stats logic to better select sub-fields when needed [#228969]({{kib-pull}}228969)
* Prevents search highlighting from affecting field action filters in the logs overview [#227652]({{kib-pull}}227652)
* Fixes an issue where dependency panels could infinitely load when no data was available [#228094]({{kib-pull}}228094)
* Fixes column sorting in the service error table [#229199]({{kib-pull}}229199)
* Ensures artifact links are visible even without endpoint list privileges [#226561]({{kib-pull}}226561)
* Fixes the incorrect background color in **Build Block Alerts** rows [#228226]({{kib-pull}}228226)
* Simplifies the **Misconfigurations** index pattern logic [#227995]({{kib-pull}}227995)
* Fixes an issue where **Security Assistant** settings landed on the wrong page when using a basic license [#229163]({{kib-pull}}229163)
* Removes the use of `removeIfExists` in the sync task scheduler [#228783]({{kib-pull}}228783)
* Fixes the width of the patterns field selector menu [#228791]({{kib-pull}}228791)
* Ensures the Gemini Vertex AI documentation link is available in the AI Connector [#228348]({{kib-pull}}228348)
* Fixes a skipped autocomplete test in the console [#229274]({{kib-pull}}229274)
* Ignores missing filters in rule parameters instead of causing errors [#229422]({{kib-pull}}229422)


## July 22, 2025 [serverless-changelog-07222025]

### Features and enhancements [serverless-changelog-07222025-features-enhancements]

* Improves perceived performance for dashboard flyouts [#226052]({{kib-pull}}226052)
* Renders {{esql}} controls using **OptionsList** UI components [#227334]({{kib-pull}}227334)
* Adds `MIGRATE` to signed actions [#228566]({{kib-pull}}228566)
* Excludes metrics data streams [#227842]({{kib-pull}}227842)
* Adds a package rollback API [#226754]({{kib-pull}}226754)
* Displays related error count and adds a failure badge [#227413]({{kib-pull}}227413)
* Adds form row labels to the {{esql}} Editor [#228103]({{kib-pull}}228103)
* Registers a UI setting for anonymization [#224607]({{kib-pull}}224607)
* Adds support for span types [#227208]({{kib-pull}}227208)
* Introduces a public "test now" endpoint [#227760]({{kib-pull}}227760)
* Enables custom roles by default [#227878]({{kib-pull}}227878)
* Allows submitting case comments by pressing **⌘+Enter** (or **Ctrl+Enter**) [#228473]({{kib-pull}}228473)
* Increases the number of supported **Group by** fields in threshold rules from 3 to 5 [#227465]({{kib-pull}}227465)
* Adds the **Search AI Lake** view to AutoOps for {{serverless-full}} to provide storage usage insights

### Fixes [serverless-changelog-07222025-fixes]

* Fixes an issue in **Lens** where **Partition** charts (for example, Pie) blocked selection of legacy palettes [#228051]({{kib-pull}}228051)
* Correctly forwards the secondary prefix when the state value is an empty string (`None` option) in **Lens** [#228183]({{kib-pull}}228183)
* Fixes loading state and improves error handling in the dashboard save modal [#227861]({{kib-pull}}227861)
* Hides hidden indices from autocomplete when using a lookup index [#227819]({{kib-pull}}227819)
* Fixes incorrect validation between aggregation expressions [#227989]({{kib-pull}}227989)
* Fixes product docs installation status [#226919]({{kib-pull}}226919).
* Resolves issues in the `metric_item` component [#227969]({{kib-pull}}227969)
* Fixes a bug with the embeddings model dropdown when upgrading with a legacy endpoint [#226878]({{kib-pull}}226878)
* Fixes filtering by "unmodified" rules in the update table [#227859]({{kib-pull}}227859)
* Fixes an issue where alert status showed as untracked for newly created schedule rules [#226575]({{kib-pull}}226575)
* Improves copy in the bulk update modal [#227803]({{kib-pull}}227803).
* Enables soft-deleting of rule gaps on rule deletion [#227231]({{kib-pull}}227231)
* Migrates the anonymization in-memory table to `EuiBasicTable` for improved selection control [#222825]({{kib-pull}}222825)
* Fixes styling issues in flyouts [#228078]({{kib-pull}}228078)
* Fixes sub-menu behavior in the solution nav when collapsed [#227705]({{kib-pull}}227705)


## July 15, 2025 [serverless-changelog-07152025]

### Features and enhancements [serverless-changelog-07152025-features-enhancements]
* {{serverless-full}} is now available in two new Amazon Web Services [regions](/deploy-manage/deploy/elastic-cloud/regions.md): `eu-central-1` (Frankfurt) and `us-east-2` (Ohio).
* Adds the ability to add tags from the **Agent details** page [#225433]({{kib-pull}}225433)
* Adds a **Profiles inspector** to Discover [#222999]({{kib-pull}}222999)
* Displays a callout about new rules in Elastic Observability Serverless **Metrics**, **Logs**, and **Inventory** rule types [#224387]({{kib-pull}}224387)
* Adds a manual test for bulk import functionality in Elastic Observability Serverless [#225497]({{kib-pull}}225497)
* Groups vulnerabilities by resource and cloud account using IDs instead of names in Elastic Security Serverless [#225492]({{kib-pull}}225492)
* Updates the default Gemini model in Elastic Security Serverless [#225917]({{kib-pull}}225917)
* Streamlines the side navigation in Elasticsearch Serverless [#225709]({{kib-pull}}225709)

### Fixes [serverless-changelog-07152025-fixes]
* Fixes an issue where reports timed out and failed with an invalid header error [#225919]({{kib-pull}}225919)
* Ensures "Values from a query" options refresh when reloading dashboards [#225101]({{kib-pull}}225101)
* Removes warnings related to kebab-case naming [#226114]({{kib-pull}}226114)
* Prevents custom titles from being overwritten in Lens embeddables after reload [#225664]({{kib-pull}}225664)
* Prevents adhoc data views from being recommended in **Controls** [#225705]({{kib-pull}}225705)
* Hides the **Select all** checkbox in single-select controls [#226311]({{kib-pull}}226311)
* Fixes a bug where edited queries were overwritten when a request completed [#224671]({{kib-pull}}224671)
* Keeps the selected document stable when resizing the flyout with keyboard controls [#225594]({{kib-pull}}225594)
* Ensures suggested dashboards only appear for custom threshold alerts in Elastic Observability Serverless [#224458]({{kib-pull}}224458)
* Fixes schema page rendering issues in Elastic Observability Serverless [#225481]({{kib-pull}}225481)
* Limits environment name length when creating a Machine Learning job in Elastic Observability Serverless [#225973]({{kib-pull}}225973)
* Fixes broken **Operation** page in Elastic Observability Serverless [#226036]({{kib-pull}}226036)
* Fixes visual issues in Elastic Observability Serverless chat when `prefers-reduce-motion` is enabled [#226552]({{kib-pull}}226552)
* Prevents collapse of *query tool* calls in Elastic Observability Serverless [#226078]({{kib-pull}}226078)
* Adds a title to the rule gap histogram on the **Rules** dashboard in Elastic Security Serverless [#225274]({{kib-pull}}225274)
* Moves alerts redirect higher in the Elastic Security Serverless component tree to improve routing [#225650]({{kib-pull}}225650)
* Opens entity links in a flyout instead of navigating away in Elastic Security Serverless [#225381]({{kib-pull}}225381)
* Stops showing ML rule installation and upgrade errors on Basic license for Elastic Security Serverless [#224676]({{kib-pull}}224676)
* Updates the **Related Interactions** input placeholder and validation message in Elastic Security Serverless [#225775]({{kib-pull}}225775)
* Falls back to default value when `lookbackInterval` is empty in Anomaly Detection rules [#225249]({{kib-pull}}225249)
* Fixes time range handling in embedded anomaly swim lanes [#225803]({{kib-pull}}225803)
* Adds discernible text to the **Refresh data preview** button [#225816]({{kib-pull}}225816)
* Improves error handling in **Search Playground** when context limit is exceeded using Elastic Managed LLM [#225360]({{kib-pull}}225360)

## July 7, 2025 [serverless-changelog-07072025]

### Features and enhancements [serverless-changelog-07072025-features-enhancements]

* Adds action to add or remove tags on the **Agent details** page in {{fleet}} [#225433]({{kib-pull}}225433)
* Adds a new **Profiles** tab to the Inspector flyout in Discover [#222999]({{kib-pull}}222999)
* Adds new rules callout to Metric, Logs, and Inventory rules in {{obs-serverless}} [#224387]({{kib-pull}}224387)
* Adds manual test for bulk import functionality in {{obs-serverless}} [#225497]({{kib-pull}}225497)
* Uses `id` instead of `name` to group vulnerabilities by resource and cloud account in {{sec-serverless}} [#225492]({{kib-pull}}225492)
* Updates Gemini model in {{sec-serverless}} [#225917]({{kib-pull}}225917)
* Updates the navigation menu in {{es-serverless}} [#225709]({{kib-pull}}225709)
* Adds performance charts to the **Usage and performance** section on the project overview page in {{serverless-full}}


### Fixes [serverless-changelog-07072025-fixes]

* Fixes an issue causing reports to fail with an invalid header error [#225919]({{kib-pull}}225919)
* Refreshes `Values from a query` options upon dashboard reload [#225101]({{kib-pull}}225101)
* Removes kebab-case warnings in Console [#226114]({{kib-pull}}226114)
* Fixes the default title being overwritten by a custom title upon reload in Lens [#225664]({{kib-pull}}225664)
* Fixes an issue with dashboards where adhoc dataviews were recommended as most relevant when creating a control [#225705]({{kib-pull}}225705)
* Hides the **Select all** checkbox from single select controls in dashboards [#226311]({{kib-pull}}226311)
* Fixes edited query being overwritten by the original query when it is resolved in Discover [#224671]({{kib-pull}}224671)
* Prevents selected document from changing when resizing the **Document** flyout with a keyboard in Discover [#225594]({{kib-pull}}225594)
* Only returns suggested dashboards for custom threshold alerts in {{obs-serverless}} [#224458]({{kib-pull}}224458)
* Fixes `Unable to load page` error on the **Schema** page in {{obs-serverless}} [#225481]({{kib-pull}}225481)
* Limits environment name length when creating an ML job in {{obs-serverless}} [#225973]({{kib-pull}}225973)
* Fixes `Unable to load page` error on the **Operations** page in {{obs-serverless}} [#226036]({{kib-pull}}226036)
* Fixes an issue with the AI assistant chat display in {{obs-serverless}} when a device has `Reduce motion` turned on [#226552]({{kib-pull}}226552)
* Collapses *query tool calls in {{obs-serverless}} [#226078]({{kib-pull}}226078)
* Adds a title to the rule gap histogram in the **Rules** dashboard in {{sec-serverless}} [#225274]({{kib-pull}}225274)
* Moves the alerts redirect higher in the components tree in {{sec-serverless}} [#225650]({{kib-pull}}225650)
* Updates entity links across {{sec-serverless}} to open flyouts instead of redirecting to other pages [#225381]({{kib-pull}}225381)
* Stops ML rule installation and upgrade errors from showing up for users with Basic licenses [#224676]({{kib-pull}}224676)
* Updates placeholder text and validation message for **Related integrations** in {{sec-serverless}}  [#225775]({{kib-pull}}225775)
* Resets to the default value when the `lookbackInterval` field is empty in Machine Learning [#225249]({{kib-pull}}225249)
* Fixes the handling of time range in embedded anomaly swim lane in Machine Learning [#225803]({{kib-pull}}225803)
* Adds discernible text to the refresh button on the **Streams** > **Processing** page [#225816]({{kib-pull}}225816)
* Fixes handling of context limit errors in Playground when using the Elastic Managed LLM [#225360]({{kib-pull}}225360)

## June 30, 2025 [serverless-changelog-06302025]

### Features and enhancements[serverless-changelog-06302025-features-enhancements]

* Adds the ability to schedule reports with a recurring schedule and view previously scheduled reports [#224849]({{kib-pull}}224849)
* Adds internal CRUD API routes in *Lens* [#223296]({{kib-pull}}223296)
* Adds `Select all` and `Deselect all` buttons to the options list popover to allow you to make bulk selections in Dashboards and Visualizations [#221010]({{kib-pull}}221010)
* Adds the flip LOOKUP JOIN parameter in {{esql}} to GA in docs [#225117]({{kib-pull}}225117)
* Passes the `TimeRange` into the `getESQLResults` in order for queries with `_tstart` and `_tend` to work properly in Discover [#225054]({{kib-pull}}225054)
* Enables the "expand to fit" query function on mount in Discover [#225509]({{kib-pull}}225509)
* Adds Logs Essentials for APM/Infra in {{obs-serverless}} [#223030]({{kib-pull}}223030)
* Allows users to choose which space monitors will be available in {{obs-serverless}} [#221568]({{kib-pull}}221568)
* Remaps `iInCircle` and `questionInCircle`, and deprecates the `help` icon in the global header [#223142]({{kib-pull}}223142)
* Adds docs for the chat completion public API in {{obs-serverless}} [#224235]({{kib-pull}}224235) 
* Enables the Security Entity Analytics Privileged user monitoring feature in {{sec-serverless}} [#224638]({{kib-pull}}224638)
* Displays visualizations in the key insights panel of the Privileged User Monitoring dashboard in {{sec-serverless}} [#223092]({{kib-pull}}223092)
* Introduces a new UI to optionally update the `kibana.alert.workflow_status` field for alerts associated with Attack discoveries in {{sec-serverless}} [#225029]({{kib-pull}}225029) 
* Enables the runscript feature flag in {{sec-serverless}} [#224819]({{kib-pull}}224819)
* Adds the incremental ID service; exposes the ID in the UI in {{sec-serverless}} [#222874]({{kib-pull}}222874)
* Adds the `windows.advanced.events.security.provider_etw` field as an advanced policy option in Elastic Defend in {{sec-serverless}} [#222197]({{kib-pull}}222197) 
* Adds new starter prompts to the AI Assistant in {{sec-serverless}} [#224981]({{kib-pull}}224981)
* Adds the ability to revert prebuilt rules to their base version in {{sec-serverless}} [#223301]({{kib-pull}}223301)
* Adds support for a collapsible section in the integration readme in {{kib}} Security [#223916]({{kib-pull}}223916)
* Adds new severity colors, alignment, and UX for filtering anomalies in {{ml-cap}} [#221081]({{kib-pull}}221081)
* Updates NL-2-ESQL docs [#224868]({{kib-pull}}224868)
* Adds keyword highlighting for {{esql}} patterns, and the ability to open a new Discover tab to filter for docs that match the selected pattern [#222871]({{kib-pull}}222871)
* Enables adaptive allocations and allows you to set max allocations in {{ml-cap}} [#222726]({{kib-pull}}222726)
* Adds a loading indicator while data sources are being fetched [#225005]({{kib-pull}}225005)
* Introduces a new home page in {{es-serverless}} [#223172]({{kib-pull}}223172)
* Adds a Search Home page in {{stack}} classic and the solution navigation in {{es-serverless}} [#225162]({{kib-pull}}225162)
* Adds updates to streamline the solution navigation in {{es-serverless}} [#224755]({{kib-pull}}224755)

### Fixes [serverless-changelog-06302025-fixes]

* Fixes the panel title sync with saved object when using `defaultTitle` in Dashboards and Visualizations [#225237]({{kib-pull}}225237)
* Fixes a performance issue in the Lens {{esql}} charts in Dashboards and Visualizations [#225067]({{kib-pull}}225067)
* Fixes visual issues with truncated long labels and hover styles in Dashboards and Visualizations [#225430]({{kib-pull}}225430)
* Fixes controls selections that caused multiple fetches in Dashboards and Visualizations [#224761]({{kib-pull}}224761)
* Ensures package policy names are unique when moving across spaces in Data ingestion and {{fleet}} [#224804]({{kib-pull}}224804) 
* Fixes export CSV in the Agent list in Data ingestion and {{fleet}} [#225050]({{kib-pull}}225050)
* Replaces call to registry when deleting {{kib}} assets for custom packages in Data ingestion and {{fleet}} [#224886]({{kib-pull}}224886)
* Fixes UI error when no tags filter is selected in Data ingestion and {{fleet}} [#225413]({{kib-pull}}225413)
* Uses bulk helper for bulk importing knowledge base entries in {{obs-serverless}} [#223526]({{kib-pull}}223526)
* Improves the knowledge base retrieval by rewriting the user prompt before querying {{es}} in {{obs-serverless}} [#224498]({{kib-pull}}224498)
* Fixes the Agent Explorer page in {{obs-serverless}} [#225071]({{kib-pull}}225071)
* Hides Settings from serverless navigation in {{obs-serverless}} [#225436]({{kib-pull}}225436)
* Replaces hard-coded CSS values to us the `euiTheme` instead in {{sec-serverless}} [#225307]({{kib-pull}}225307)
* Fixes URL query handling for asset inventory flyout in {{sec-serverless}} [#225199]({{kib-pull}}225199)
* Adds missing model Claude 3.7 to accepted models in {{es-serverless}} [#224943]({{kib-pull}}224943)






## June 26, 2025 [serverless-changelog-06262025]

### Features and enhancements [serverless-changelog-06262025-features-enhancements]
* {{serverless-full}} is now available in the Microsoft Azure `eastus` [region](/deploy-manage/deploy/elastic-cloud/regions.md). 

## June 23, 2025 [serverless-changelog-06232025]

### Features and enhancements [serverless-changelog-06232025-features-enhancements]

* Adds new setting `xpack.actions.webhook.ssl.pfx.enabled` to disable PFX file support for SSL client authentication in Webhook connectors [#222507]({{kib-pull}}222507)
* Introduces **Scheduled Reports** feature [#221028]({{kib-pull}}221028)
* Adds `xpack.actions.email.services.enabled` setting to control availability of email services in connectors [#223363]({{kib-pull}}223363)
* Enables support for adding observables, procedures, and custom fields to alerts for TheHive [#207255]({{kib-pull}}207255)
* Improves visual highlight behavior in the add panel UI [#223614]({{kib-pull}}223614)
* Supports agentless traffic filters for Elastic Agent [#222082]({{kib-pull}}222082)
* Adds support for suggesting all operators in the query editor [#223503]({{kib-pull}}223503)
* Introduces accordion sections and attribute tables in UI components [#224185]({{kib-pull}}224185)
* Adds monitor downtime alert when no data is available [#220127]({{kib-pull}}220127)
* Introduces **Maintenance Windows** functionality [#222174]({{kib-pull}}222174)
* Enables editing of labels and tags for private locations in **Synthetics** [#221515]({{kib-pull}}221515)
* Adds new tail-based sampling settings to integration policies [#224479]({{kib-pull}}224479)
* Enables model ID retrieval from anonymization rules [#224280]({{kib-pull}}224280)
* Updates SLO starter prompt text for improved guidance [#224493]({{kib-pull}}224493)
* Introduces `deactivate_...` agent configuration settings for EDOT Node.js [#224502]({{kib-pull}}224502)
* Updates system prompt to include information about anonymization [#224211]({{kib-pull}}224211)
* Adds support for Microsoft Defender's `runscript` command in the **Response Console** [#222377]({{kib-pull}}222377)
* Moves Automatic Migration from **Tech Preview** to General Availability [#224544]({{kib-pull}}224544)
* Adds simplified bulk editing for alert suppression rules [#223090]({{kib-pull}}223090)
* Introduces **XSOAR Connector** [#212049]({{kib-pull}}212049)
* Adds `name` field to the Rule Migrations UI and data model [#223860]({{kib-pull}}223860)
* Enables collection of `dns` events for macOS in **Elastic Defend** [#223566]({{kib-pull}}223566)
* Adds usage callout for **Elastic Indexing Service (EIS)** [#221566]({{kib-pull}}221566)
* Adds `ecs@mappings` component template to transform destination index templates [#223878]({{kib-pull}}223878)
* Renames advanced policy setting `disable_origin_info_collection` to `origin_info_collection` and changed its default behavior to Opt-In [#223882]({{kib-pull}}223882)
* Introduces cleanup task for unused URLs [#220138]({{kib-pull}}220138)
* Marks the **Session Invalidation API** as Stable [#224076]({{kib-pull}}224076)
* Hides the Adaptive Allocations toggle for Trained Models in **Serverless** environments [#224097]({{kib-pull}}224097)
* Adds option to disable **AIOps** features in Kibana [#221286]({{kib-pull}}221286)
* Enables autocompletion for **ES|QL** queries in the Console UI [#219980]({{kib-pull}}219980)
* Improves layout and content of rule listing and overview pages [#223603]({{kib-pull}}223603)
* Adds support for changing settings when re-processing Rule Migrations [#222542]({{kib-pull}}222542)
* Implements navigation UI for the **Overview Page** in **Entity Analytics** [#221748]({{kib-pull}}221748)
* Adds support for partial result handling in **ES|QL** [#223198]({{kib-pull}}223198)
* Adds an **Executable Name** tab to the TopN view [#224291]({{kib-pull}}224291)


### Fixes [serverless-changelog-06232025-fixes]

* Fixes pagination not working correctly in certain tables [#223537]({{kib-pull}}223537)
* Fixes bulk actions selecting incorrect agents when `namespace` filter is used [#224036]({{kib-pull}}224036)
* Corrects `z-index` issues in the **ESQL Query Editor** [#222841]({{kib-pull}}222841)
* Updates ARIA tags for improved accessibility in selected fields UI [#224224]({{kib-pull}}224224)
* Ensures **Last Successful Screenshot** matches the correct step in Synthetics [#224220]({{kib-pull}}224220)
* Improves network error handling for error details panel [#224296]({{kib-pull}}224296)
* Fixes broken **EDOT JVM Metrics Dashboard** when classic agent metrics are present [#224052]({{kib-pull}}224052)
* Fixes **SLO federated view** bug caused by exceeding index name byte limit [#224478]({{kib-pull}}224478)
* Fixes issue where OSS models failed when streaming was enabled [#224129]({{kib-pull}}224129)
* Corrects display issues for rule filters in the UI [#222963]({{kib-pull}}222963)
* Fixes time normalization bug for day units in rule scheduling [#224083]({{kib-pull}}224083)
* Resolves issue where unknown fields weren't supported in **Data Visualizer** and **Field Statistics** [#223903]({{kib-pull}}223903)
* Fixes Bedrock connector not using proxy configuration settings [#224130]({{kib-pull}}224130)
* Passes correct namespace to `migrateInputDocument` logic [#222313]({{kib-pull}}222313)
* Adjusts app menu header `z-index` to avoid clashing with the portable dev console [#224708]({{kib-pull}}224708)
* Reverts to using `.watches` system index in Watcher UI [#223898]({{kib-pull}}223898)
* Fixes several issues introduced in versions 8.18.0 through 9.1.0, including broken pagination (limited to 10 items), erroneous error banners, and broken search functionality.
* Fixes **Discard** button state change logic for toggles [#223493]({{kib-pull}}223493)
* Removes `originId` from connectors during rule import [#223454]({{kib-pull}}223454)

## June 17, 2025 [serverless-changelog-06172025]

### Features and enhancements [serverless-changelog-06172025-features-enhancements]
* {{serverless-full}} is now available in two new Google Cloud Platform [regions](/deploy-manage/deploy/elastic-cloud/regions.md): GCP Belgium (`europe-west1`) and GCP Mumbai (`asia-south1`) 

## June 16, 2025 [serverless-changelog-06162025]

### Features and enhancements [serverless-changelog-06162025-features-enhancements]
* Adds support for deleting active or inactive alerts after one day without a status update [#216613]({{kib-pull}}216613)
* Adds AWS SES email configuration options: `xpack.actions.email.services.ses.host` and `ses.port` [#221389]({{kib-pull}}221389)
* Adds point visibility option for area and line charts in **Lens** [#222187]({{kib-pull}}222187)
* Enables feature flag for the tabular integrations Fleet UI [#222842]({{kib-pull}}222842)
* Displays partial results when an ES|QL query times out due to the `search:timeout` setting [#219027]({{kib-pull}}219027)
* Improves handling of long fields in the **Discover** editor [#223222]({{kib-pull}}223222)
* Adds a primary **Add to case** button to Elastic Observability Serverless [#223184]({{kib-pull}}223184)
* Renders suggested dashboards in relevant contexts in Elastic Observability Serverless [#223424]({{kib-pull}}223424)
* Adds a **History** tab for calendar-based SLOs in the Elastic Observability Serverless SLO details page [#223825]({{kib-pull}}223825)
* Updates the `spec.max` setting to version 3.4 for Elastic Observability Serverless [#221544]({{kib-pull}}221544)
* Adds support for anonymizing sensitive data for Elastic Observability Serverless [#223351]({{kib-pull}}223351)
* Adds `logging_level` configuration in Elastic Observability Serverless for EDOT Node.js agent [#222883]({{kib-pull}}222883)
* Removes `is_correction` and `confidence` attributes from Elastic Observability Serverless Knowledge Base entries [#222814]({{kib-pull}}222814)
* Displays linked cases in the Elastic Observability Serverless alert details overview [#222903]({{kib-pull}}222903)
* Refetches alert rule data when edits are submitted in the Elastic Observability Serverless flyout [#222118]({{kib-pull}}222118)
* Adds `disable_origin_info_collection` to endpoint policy advanced settings in Elastic Security Serverless [#222030]({{kib-pull}}222030)
* Improves alert filtering in Elastic Security Serverless by including ECS `data_stream` fields under `kibana.alert.original_data_stream.*` [#220447]({{kib-pull}}220447)
* Adds a rare scripts job to the preconfigured Security:Windows anomaly detection jobs [#223041]({{kib-pull}}223041)
* Adds `converse` and `converseStream` subActions to Bedrock connectors for Machine Learning [#223033]({{kib-pull}}223033)
* Improves error handling in the AI Connector creation UI for Machine Learning [#221859]({{kib-pull}}221859)
* Disables trace visualizations in **Discover** for Logs Essentials serverless mode in Elastic Observability Serverles [#222991]({{kib-pull}}222991)
* Adds the **Attributes** tab to the Elastic Observability Serverless document viewer [#222391]({{kib-pull}}222391)

### Fixes [serverless-changelog-06162025-fixes]
* Reverts instructions for installing the complete Elastic Agent [#223520]({{kib-pull}}223520)
* Fixes incorrect function signatures in bucket functions for **Discover** [#222553]({{kib-pull}}222553)
* Reverts CSV export time range fix in **Discover** [#223249]({{kib-pull}}223249)
* Adds `aria-labelledby` to Elastic Charts SVG for accessibility in Elastic Observability Serverless [#220298]({{kib-pull}}220298)
* Hides **Data set details** when `dataStream` comes from a remote cluster in Elastic Observability Serverless [#220529]({{kib-pull}}220529)
* Prevents unnecessary re-render after completing a **Run test** action in Elastic Observability Serverless [#222503]({{kib-pull}}222503)
* Skips tool instructions in system messages when tools are disabled in Elastic Observability Serverless [#223278]({{kib-pull}}223278)
* Fixes broken **View in Discover** link in Elastic Security Serverless [#217993]({{kib-pull}}217993)
* Expands metrics pattern for the Java EDOT dashboard  in Elastic Observability Serverless [#223539]({{kib-pull}}223539)
* Applies `autoFocus` to the `cc` and `bcc` fields in the Elastic Observability Serverless email connector form [#223828]({{kib-pull}}223828)
* Fixes rendering issues in the Elastic Security Serverless Threat Enrichment component [#223164]({{kib-pull}}223164)
* Ensures ingest pipelines are installed in all relevant spaces and assigned to appropriate indices in Elastic Security Serverless [#221937]({{kib-pull}}221937)
* Fixes card overflow issues on the **Machine Learning Overview** page [#223431]({{kib-pull}}223431)
* Applies chunking algorithm to `getIndexBasicStats` to improve performance [#221153]({{kib-pull}}221153)

## June 9, 2025 [serverless-changelog-06092025]

### Features and enhancements [serverless-changelog-06092025-features-enhancements]

* Ensures the Report UI only displays reports generated in the current space [#221375]({{kib-pull}}221375).
* Color mapping is now GA. `palette` definitions are deprecated and turning off Legacy mode will replace the palette with an equivalent color mapping configuration in* **Lens**. [#220296]({{kib-pull}}220296).
* Updates time based charts to use the multi-layer time axis by default, providing a better time window context and improved label positioning. [#210579]({{kib-pull}}210579).
* Adds an integration flyout to Agent policy details in {{fleet}} [#220229]({{kib-pull}}220229).
* Enables the `enableSyncIntegrationsOnRemote` feature flag in {{fleet}} [#220215]({{kib-pull}}220215).
* Enables migration of a single agent to another cluster via the actions menu in {{fleet}}. [#222111]({{kib-pull}}222111).
* Adds a button allowing users to skip to the next section in the fields list in **Discover** [#221792]({{kib-pull}}221792).
* Adds the **SLO Management** page to {{obs-serverless}}, allowing users to view definitions, delete SLOs, and purge SLI data without having to consider instances [#222238]({{kib-pull}}222238).
* Adds a new APM dashboard for the Golang OpenTelemetry runtime metrics in {{obs-serverless}} [#220242]({{kib-pull}}220242).
* Uses the bulk API to import knowledge base entries in {{obs-serverless}} [#222084]({{kib-pull}}222084).
* Improves system prompt and instructions for the `context` function in the Elastic Observability AI Assistant to work better with Claude models [#221965]({{kib-pull}}221965).
* Sets `observabilityAIAssistantAPIClient` as the preferred test for type-safe endpoint calls with scoped users in the Elastic Observability AI Assistant [#222753]({{kib-pull}}222753).
* Adds a custom script selector component to the **Response console** in {{sec-serverless}} [#204965]({{kib-pull}}204965).
* Updates the `AssetCriticalityBadge` colors to the Borealis theme in {{sec-serverless}} [#222024]({{kib-pull}}222024).
* Updates the risk severity colors to the Borealis theme in {{sec-serverless}} [#222061]({{kib-pull}}222061).
* Enables **Content Connectors** in the **Stack Management** menu in {{sec-serverless}} [#221856]({{kib-pull}}221856).
* Implements PKI authentication support for the `.gen-ai` connector’s `OpenAI Other` provider [#219984]({{kib-pull}}219984).

### Fixes [serverless-changelog-06092025-fixes]

* Fixes {{kib}} being stuck in a reboot loop when `cancelAlertsOnRuleTimeout` is set to `false` [#222263]({{kib-pull}}222263).
* Adds saved object version for collapsible sections [#222450]({{kib-pull}}222450).
* Fixes the `UnenrollInactiveAgentsTask` query in {{fleet}} to un-enroll only those agents that are inactive for longer than `unenroll_timeout` [#222592]({{kib-pull}}222592).
* Adds **Actions** header to the unified data table in **Discover** [#220824]({{kib-pull}}220824).
* Fixes `COALESCE` validation in **ES|QL** [#222425]({{kib-pull}}222425).
* Fixes incorrect suggestions after a named variable such as `?value` is entered in a `WHERE` query in **ES|QL** [#222312]({{kib-pull}}222312).
* Replaces `onChangedItemIndices` with `onChangeRenderedItems` when determining which service details to fetch in {{obs-serverless}} [#222439]({{kib-pull}}222439).
* Fixes pagination on the Services **Inventory** page when progressive loading is enabled in {{obs-serverless}} [#220514]({{kib-pull}}220514).
* Refactors styling for the timeline in {{sec-serverless}} from `styled-components` to `emotion` [#222438]({{kib-pull}}222438).
* Fixes wrong content appearing when switching tabs in the **Ingest your data** section on the **Get started** page in {{sec-serverless}} [#222271]({{kib-pull}}222271).
* Fixes incorrect header text in the **Rule exception** flyout in {{sec-serverless}} [#222248]({{kib-pull}}222248).
* Fixes an issue with adding a field when no pipeline has been generated during import in Machine Learning [#222775]({{kib-pull}}222775).
* Fixes an issue with the OpenAI connector not using the action proxy configuration for all subactions in Machine Learning [#219617]({{kib-pull}}219617).
* Fixes an issue with **Anomaly Explorer** where the selected Overall swimlane bucket is not respected for `viewBy jobId` in Machine Learning [#222845]({{kib-pull}}222845).
* Fixes error handling when one or more connectors is deleted [#221958]({{kib-pull}}221958).

## June 2, 2025 [serverless-changelog-06022025]

### Features and enhancements [serverless-changelog-06022025-features-enhancements]

* Adds collapsible sections to Dashboards [#220877]({{kib-pull}}220877)
* Introduces a new `Density` setting for the Lens Data Table[#220252]({{kib-pull}}220252)
* Allows the "Open in lens" button to open in the same tab [#217528]({{kib-pull}}217528)
* Allows you to select the data stream type when creating policies for input packages in {{fleet}} [#214216]({{kib-pull}}214216)
* Adds a single agent migration endpoint in {{fleet}}, allowing a user to migrate an individual agent to another cluster [#220601]({{kib-pull}}220601)
* Adds shortcuts to the editor in Discover [#221331]({{kib-pull}}221331)
* Allows you to change the Knowledge Base model after installation in {{obs-serverless}} [#221319]({{kib-pull}}221319)
* Adds investigation guide configuration to all Observability rules in {{obs-serverless}} [#217106]({{kib-pull}}217106)
* Remove semantic_text migration from {{obs-serverless}} [#220886]({{kib-pull}}220886)
* Searches for the CVE ID in all search parameters instead of only the name in {{sec-serverless}} [#221099]({{kib-pull}}221099)
* Updates the "Highlighted fields" button in the details flyout and enables the feature flag in {{sec-serverless}} [#221862]({{kib-pull}}221862)
* Introduces new `empty` states for the Change Point Detection page in {{ml-cap}} [#219072]({{kib-pull}}219072)


### Fixes [serverless-changelog-06022025-fixes]

* Uses msearch to fetch the alerts for maintenance windows with a scoped query [#221702]({{kib-pull}}221702)
* Fixes querying installed packages in {{fleet}} [#221624]({{kib-pull}}221624)
* Fixes an issue that prevented the style components from receiving the correct `colorMode` in {{fleet}} [#221979]({{kib-pull}}221979)
* Makes the **Pin** button more accessible in Discover [#219230]({{kib-pull}}219230)
* Fixes an issue where the `Filter by field type` menu screen reader announcements were using duplicated in Discover [#221090]({{kib-pull}}221090)
* Removes an unneeded tabindex from Discover [#221265]({{kib-pull}}221265)
* Changes the field list icon when mapping changes from unmapped to mapped in Discover [#221308]({{kib-pull}}221308)
* Updates the doc viewer table's `aria-label` in Discover [#221736]({{kib-pull}}221736)
* Shows the ES|QL request URL in the Inspector flyout in Discover [#221816]({{kib-pull}}221816)
* Fixes index pattern parsing in Discover, which previously led to incomplete index pattern values being displayed [#221084]({{kib-pull}}221084)
* Ensures a non-aggregatable message is not shown if no data matches on the Dataset quality page in {{obs-serverless}} [#221599]({{kib-pull}}221599)
* Deletes user instruction if the text is empty in {{obs-serverless}} [#221560]({{kib-pull}}221560)
* Adjusts the bulk import knowledge base example to ndjson format in {{obs-serverless}} [#221617]({{kib-pull}}221617)
* Modifies `RuleTypeModalComponent` to filter rule types that have `requiresAppContext` in {{obs-serverless}} [#220005]({{kib-pull}}220005)
* Correctly nests APM > Synthetics Serverless navigation in {{obs-serverless}} [#222115]({{kib-pull}}222115)
* Removes the "run soon for sync private location" task in {{obs-serverless}} [#222062]({{kib-pull}}222062)
* Fixes the error count waterfall navigation reload issue in {{obs-serverless}} [#221664]({{kib-pull}}221664)
* Fixes the Bedrock model on preconfigured connectors in {{sec-serverless}} [#221411]({{kib-pull}}221411)
* Removes the hard-coded width settings for the Threat Match mapping components in {{sec-serverless}} [#218628]({{kib-pull}}218628)
* Fixes the banner title in event preview in {{sec-serverless}}  [#222266]({{kib-pull}}222266)
* Ensures to only auto deploy Elastic models during file upload in {{ml-cap}} [#221357]({{kib-pull}}221357)
* Fixes the inference endpoint assignment to the trained model object in {{ml-cap}}  [#222076]({{kib-pull}}222076)
* Fixes an issue where `/etc/default/kibana` on deb packages and `/etc/sysconfig/kibana` on rpm packages would be overwritten during upgrading [#221276]({{kib-pull}}221276)

## May 26, 2025 [serverless-changelog-05262025]

### Features and enhancements [serverless-changelog-05262025-features-enhancements]

* Suggests full text search in our recommendations [#221239]({{kib-pull}}221239)
* Flattens grid layout [#218900]({{kib-pull}}218900)
* Enables ELSER and E5 on EIS [#220993]({{kib-pull}}220993)
* Links dashboards on the Rule and Alert pages [#219019]({{kib-pull}}219019)
* Saves `group by` information with dynamic mapping [#219826]({{kib-pull}}219826)
* Introduces a new endpoint scheme for SIEM migration [#219597]({{kib-pull}}219597)
* Extends default log pattern on server side to include error information [#219940]({{kib-pull}}219940)


### Fixes [serverless-changelog-05262025-fixes]

* Fixes `getTimezone` default value [#220658]({{kib-pull}}220658)
* Loads correct system color mode at bootstrap [#218417]({{kib-pull}}218417)
* Fixes embeddables not refreshing on manual refresh or auto-refresh [#221326]({{kib-pull}}221326)
* Improves Discover session input focus behavior [#220876]({{kib-pull}}220876)
* Fixes suggestions after triple quote pair [#221200]({{kib-pull}}221200)
* Passes app state and global state to locator when redirecting from `/stream` path [#215867]({{kib-pull}}215867)
* Considers status rule locations only if not an empty array [#220983]({{kib-pull}}220983)
* Fixes a bug where update of an SLO created in a version older than 8.18 failed due to an invalid ingest pipeline [#221158]({{kib-pull}}221158)
* Checks for documents before starting semantic text migration [#221152]({{kib-pull}}221152)
* Improves error telemetry [#220938]({{kib-pull}}220938)
* Retrieves active integrations from installed integrations API [#218988]({{kib-pull}}218988)
* Fixes spaces search functionality for spaces created with avatar type as image [#220398]({{kib-pull}}220398)
* Fixes inability to clear Document ID in data view field editor preview [#220891]({{kib-pull}}220891)
* Reworks cookie and session storage to prevent unexpected logouts for certain users with certain use cases [#220430]({{kib-pull}}220430)
* Changes the AI Connector description [#221154]({{kib-pull}}221154)

## May 19, 2025 [serverless-changelog-05192025]

### Features and enhancements [serverless-changelog-05192025-features-enhancements]
* Supports recurring task scheduling with `rrule` in Alerting [#217728]({{kib-pull}}217728)
* Adds an embeddable panel to display alerts in **Dashboards** [#216076]({{kib-pull}}216076)
* Adds **Compare to** badge for **Metric chart** visualizations [#214811]({{kib-pull}}214811)
* Allows specifying an embedding model during onboarding for the Elastic Observability Serverless Knowledge Base [#218448]({{kib-pull}}218448)
* Enables click actions for **Stacktrace** and **Degraded Fields** in **Discover** for Elastic Observability Serverless [#214413]({{kib-pull}}214413)
* Shows **ELSER** in **EIS** only when available in Elastic Observability Serverless [#220096]({{kib-pull}}220096)
* Adds the ability to create alert rules from **ES|QL** dashboard visualizations via context menu or right-clicking a data point [#217719]({{kib-pull}}217719)
* Enables the `enableAutomaticAgentUpgrades` feature flag for Fleet [#219932]({{kib-pull}}219932)
* Adds Cloud Connectors support to Fleet for **CSPM** [#212200]({{kib-pull}}212200)
* Ensures alerts created within **Maintenance Windows** trigger actions after the window expires [#219797]({{kib-pull}}219797)
* Adds **Copy value** button to field value cells in **Discover** [#218817]({{kib-pull}}218817)
* Hides the **Selected only** toggle in pages that don't support value-based filtering in **Discover** [#220624]({{kib-pull}}220624)
* Updates default model IDs for **Bedrock** and **OpenAI** connectors in Elastic Security Serverless [#220146]({{kib-pull}}220146)
* Integrates AI prompts in Elastic Security Serverless [#216106]({{kib-pull}}216106)
* Adds an **ES|QL** control option to the dashboard controls dropdown [#219495]({{kib-pull}}219495)
* Enables full-text search in `STATS ... WHERE` **ES|QL** queries [#220691]({{kib-pull}}220691)
* Prevents downloading trained models that are already present in other spaces and displays a warning in Machine Learning [#220238]({{kib-pull}}220238)

### Fixes [serverless-changelog-05192025-fixes]
* Removes extra icon from map visualization tooltips [#220134]({{kib-pull}}220134)
* Fixes color mapping issues for custom ranges and multi-field values in visualizations [#207957]({{kib-pull}}207957)
* Fixes layout issues in embeddable dashboard panel headings with descriptions [#219428]({{kib-pull}}219428)
* Fixes invalid dashboards incorrectly showing 404 errors instead of validation messages [#211661]({{kib-pull}}211661)
* Fixes success message and auto-scroll behavior after adding a panel to a dashboard from the library [#220122]({{kib-pull}}220122)
* Fixes drill-down state not saving in by-value **Discover** sessions [#219857]({{kib-pull}}219857)
* Marks icons as presentational for accessibility in **Discover** [#219696]({{kib-pull}}219696)
* Fixes broken **Span Links** flyout in **Trace Explorer** in Elastic Observability Serverless [#219763]({{kib-pull}}219763)
* Prevents undefined errors in **Transaction flyout** in Elastic Observability Serverless [#220224]({{kib-pull}}220224)
* Fixes issues with **Processes** query in Elastic Observability Serverless [#220381]({{kib-pull}}220381)
* Removes unnecessary index write blocks in Elastic Observability Serverless [#220362]({{kib-pull}}220362)
* Improves resilience of API tests in Elastic Observability Serverless [#220503]({{kib-pull}}220503)
* Uses update-by-query for `semantic_text` migration in Elastic Observability Serverless [#220255]({{kib-pull}}220255)
* Fixes errors in `error_marker.tsx` to support **Mobile Services** in Elastic Observability Serverless [#220424]({{kib-pull}}220424)
* Moves from visualization responses to visualization tables in Elastic Security Serverless [#214888]({{kib-pull}}214888)
* Prevents risk score search requests from being aborted in Elastic Security Serverless [#219858]({{kib-pull}}219858)
* Fixes issue where exceptions list and actions were overwritten during legacy prebuilt rule upgrades in Elastic Security Serverless [#218519]({{kib-pull}}218519)
* Fixes incorrect validation for names containing asterisks in **ES|QL** [#219832]({{kib-pull}}219832)
* Fixes overridden SSL config in full agent policy advanced YAML for Fleet [#219902]({{kib-pull}}219902)

## May 5, 2025 [serverless-changelog-050525]

### Features and enhancements [serverless-changelog-050525-features-enhancements]

* Adds grouping per row to the {{esql}} rule type [#212135](https://github.com/elastic/kibana/pull/212135)
* Adds a compact view on the Monitors overview page in {{obs-serverless}} [#219060](https://github.com/elastic/kibana/pull/219060)
* Adds backend schema changes for investigation guides in {{obs-serverless}} [#216377](https://github.com/elastic/kibana/pull/216377)
* Adds the `context.grouping` action variable for the SLO Burn rate and {{esql}} rules in {{obs-serverless}} [#213550](https://github.com/elastic/kibana/pull/213550)
* Updates the styles for the color formatter to appear like a badge in Discover [#189391](https://github.com/elastic/kibana/pull/189391)
* Enhances the handling of missing `service.environment` attributes in {{obs-serverless}} [#217899](https://github.com/elastic/kibana/pull/217899)
* Adds `logging_level` to the agent central configuration for the EDOT Java agent in {{obs-serverless}} [#219722](https://github.com/elastic/kibana/pull/219722)
* Updates {{kib}} MITRE data to `v16.1` [#215026](https://github.com/elastic/kibana/pull/215026)
* Makes the {{fleet}} agents tag filter searchable and sortable [#219639](https://github.com/elastic/kibana/pull/219639)
* Adds logic to exclude the `temperature` parameter from the body request of some OpenAI models [#218887](https://github.com/elastic/kibana/pull/218887)
* Adds the ability to switch between relative and absolute time range in Discover [#218056](https://github.com/elastic/kibana/pull/218056)

### Fixes [serverless-changelog-050525-fixes]

* Fixes ignored dynamic templates [#219875](https://github.com/elastic/kibana/pull/219875)
% Dashboards and visualizations
* Syncs the Dashboard {{esql}} query and filters with the corresponding one in Visualizations [#218997](https://github.com/elastic/kibana/pull/218997)
* Fixes the option list control, making two requests upon refreshing [#219625](https://github.com/elastic/kibana/pull/219625)
* Ensures that an individual alert is sent per monitor configuration when the "Receive distinct alerts per location" toggle is unchecked in {{obs-serverless}} [#219291](https://github.com/elastic/kibana/pull/219291)
* Fixes an error that occurred when you interacted with the monitor status rule flyout's numeric controls in {{obs-serverless}} [#218994](https://github.com/elastic/kibana/pull/218994)
* Fixes an issue where the Observability AI Assistant flyout reopened after navigating to another page URL [#219420](https://github.com/elastic/kibana/pull/219420)
* Fixes an issue with alerts filtering when the service environment was not defined in {{obs-serverless}} [#219228](https://github.com/elastic/kibana/pull/219228)
* Handles missing `trace` in API response [#219512](https://github.com/elastic/kibana/pull/219512)
* Correctly displays an error message if there are failures when creating anomaly detection jobs [#219364](https://github.com/elastic/kibana/pull/219364)
* Adds optional chaining to prevent undefined error in `custom_link_flyout.tsx` in {{obs-serverless}} [#219668](https://github.com/elastic/kibana/pull/219668)
* Corrects quotes in {{esql}} queries for function arguments in {{obs-serverless}} [#217680](https://github.com/elastic/kibana/pull/217680)
* Queries alerts using the `alert.start` field in {{obs-serverless}} [#219651](https://github.com/elastic/kibana/pull/219651)
* Fixes a scroll error for the Rules flyout in {{sec-serverless}} [#218697](https://github.com/elastic/kibana/pull/218697)
* Adds a privilege check for enabling the **Run Engine** button in {{sec-serverless}}  [#213054](https://github.com/elastic/kibana/pull/213054)
* Removes checks for an unused connector role in {{sec-serverless}} [#219358](https://github.com/elastic/kibana/pull/219358)
* Fixes the rule import error message display [#218701](https://github.com/elastic/kibana/pull/218701)
* Fixes the capability required for the SIEM Migrations Topic in {{fleet}} [#219427](https://github.com/elastic/kibana/pull/219427)
* Ensures the ability to change providers without error in {{ml-cap}} [#219020](https://github.com/elastic/kibana/pull/219020)
* Fixes broken icons in integrations from the Home plugin [#219206](https://github.com/elastic/kibana/pull/219206)





## April 28, 2025 [serverless-changelog-04282025]

### Features and enhancements [serverless-changelog-04282025-features-enhancements]

* Adds the option to use the logical `AND` when filtering Monitors by multiple tags or locations [#217985](https://github.com/elastic/kibana/pull/217985)
* Makes Attack Discovery alerts persistent and searchable [#218906](https://github.com/elastic/kibana/pull/218906)
* Improves edit ReadMe functionality for custom integrations [#215259](https://github.com/elastic/kibana/pull/215259)
* Removes metrics and logs from the `get_service_stats` API [#218346](https://github.com/elastic/kibana/pull/218346)
* Allows you to customize the table tab [#218686](https://github.com/elastic/kibana/pull/218686)
* Enables keyboard navigation for the create annotations form [#217918](https://github.com/elastic/kibana/pull/217918)


### Fixes [serverless-changelog-04282025-fixes]

* Fixes keyword format in metric visualizations [#218233](https://github.com/elastic/kibana/pull/218233)
* Fixes monitor history histogram and group by location issue [#218550](https://github.com/elastic/kibana/pull/218550)
* Prevents other conditions from changing when you change the condition type of a monitor status rule [#216426](https://github.com/elastic/kibana/pull/216426)
* Filters out null values from `sourceDataStreams` [#218772](https://github.com/elastic/kibana/pull/218772)
* Fixes span url link when `transactionId` is missing in span links [#218232](https://github.com/elastic/kibana/pull/218232)
* Fixes logical `AND` behavior when a filter is removed [#218910](https://github.com/elastic/kibana/pull/218910)
* Fixes a bug that prevented index template creation [#218901](https://github.com/elastic/kibana/pull/218901)
* Prevents unnecessary suggestion requests [#218927](https://github.com/elastic/kibana/pull/218927)
* Uses fields instead of `_source` in the metadata endpoint [#218869](https://github.com/elastic/kibana/pull/218869)
* Fills gaps in table tooltips [#218926](https://github.com/elastic/kibana/pull/218926)
* Makes output and fleet server non-editable for agentless integration policies [#218905](https://github.com/elastic/kibana/pull/218905)
* Improves anomaly charts object safety [#217552](https://github.com/elastic/kibana/pull/217552)
* Fixes title announcements in the details step of the anomaly detection job wizard [#218570](https://github.com/elastic/kibana/pull/218570)
* Fixes incorrect optimization for endpoint artifacts [#216437](https://github.com/elastic/kibana/pull/216437)


## April 21, 2025 [serverless-changelog-04212025]

### Features and enhancements [serverless-changelog-04212025-features-enhancements]
* Adds public Maintenance Window APIs for Alerting [#216756](https://github.com/elastic/kibana/pull/216756)
* Enables KQL filter for Elastic Observability Serverless TLS rules [#216973](https://github.com/elastic/kibana/pull/216973)
* Adds drilldown to synthetics stats overview embeddable for Elastic Observability Serverless [#217688](https://github.com/elastic/kibana/pull/217688)
* Updates the Elastic Observability Serverless embeddable view when only one monitor in one location is selected [#218402](https://github.com/elastic/kibana/pull/218402)
* Improves accessibility in the Elastic Observability Serverless create connector flyout [#218426](https://github.com/elastic/kibana/pull/218426)
* Removes double confirmation when deleting conversations in Elastic Observability Serverless [#217991](https://github.com/elastic/kibana/pull/217991)
* APM URLs now encode the service name in Elastic Observability Serverless [#217092](https://github.com/elastic/kibana/pull/217092)
* Adds improvements to the Embeddable Trace Waterfall in Elastic Observability Serverless [#217679](https://github.com/elastic/kibana/pull/217679)
* Updates the highlighted fields in the Elastic Security Serverless overview tab [#216740](https://github.com/elastic/kibana/pull/216740)
* Adds the ability to handle ELASTIC_PROFILER_STACK_TRACE_IDS for apm-profiler integration in Elastic Obserbability Serverless [#217020](https://github.com/elastic/kibana/pull/217020)
* Adds the ability to open links in a new window for Vega visualizations [#216200](https://github.com/elastic/kibana/pull/216200)
* Adds the ability to opt out of event-driven Memory Protection scanning in Elastic Security Serverless advanced policies [#218354](https://github.com/elastic/kibana/pull/218354)
* Replaces the Elastic Security Serverless analyzer sourcerer [#218183](https://github.com/elastic/kibana/pull/218183)
* Enables suggestions for `CHANGE_POINT` command in ES|QL [#218100](https://github.com/elastic/kibana/pull/218100)
* Adds callouts for Fleet breaking changes for integration upgrades [#217257](https://github.com/elastic/kibana/pull/217257)
* Adds support for local `xpack.productDocBase.artifactRepositoryUrl` file path in Machine Learning [#217046](https://github.com/elastic/kibana/pull/217046)
* Adds defaultSolution to spaces configuration [#218360](https://github.com/elastic/kibana/pull/218360)
* Adds support for dots in the role mappings. Dots (.) can be used as part of the role mappings and the groups that are returned by the custom IdPs to match to.

### Fixes [serverless-changelog-04212025-fixes]
* Fixes allow_hidden usage in the request for fields in Discover [#217628](https://github.com/elastic/kibana/pull/217628)
* Fixes an issue in Discover where keydown event propagation now stops when unified doc tabs are focused [#218300](https://github.com/elastic/kibana/pull/218300)
* Fixes an issue where sync global parameters are now called in the endpoints to add, edit, or delete global params in Elastic Observability Serverless [#216197](https://github.com/elastic/kibana/pull/216197)
* Adds the ability to allow group for ip type fields in Elastic Observability Serverless [#216062](https://github.com/elastic/kibana/pull/216062)
* Fixes the EDOT error summary in Elastic Observability Serverless [#217885](https://github.com/elastic/kibana/pull/217885)
* Fixes test run logs per page in Elastic Observability Serverless [#218458](https://github.com/elastic/kibana/pull/218458)
* Fixes the display results and Visualize query Bedrock error in Elastic Observability Serverless [#218213](https://github.com/elastic/kibana/pull/218213)
* Fixes prebuilt rules force upgrade on Endpoint policy creation in Elastic Security Serverless [#217959](https://github.com/elastic/kibana/pull/217959)
* Fixes related integrations render performance on rule editing pages in Elastic Security Serverless [#217254](https://github.com/elastic/kibana/pull/217254)
* Fixes the broken tooltip suggestions descriptions in ES|QL [#218067](https://github.com/elastic/kibana/pull/218067)
* Adds the ability to retrieve empty columns in ES|QL [#218085](https://github.com/elastic/kibana/pull/218085)
* Fixes an issue in ES|QL where tables with no data would break [#217937](https://github.com/elastic/kibana/pull/217937)
* Fixes the ES|QL editor menus when using Safari [#218167](https://github.com/elastic/kibana/pull/218167)
* Fixes the wrong source validation in case of unknown patterns in ES|QL [#218352](https://github.com/elastic/kibana/pull/218352)
* Fixes vCPU usage message in the Machine Learning start deployment dialog [#218557](https://github.com/elastic/kibana/pull/218557)
* Removes the listing limit warning [#217945](https://github.com/elastic/kibana/pull/217945)
* Fixes an issue where the placeholder in the monaco editor would disappear when a value is set [#217828](https://github.com/elastic/kibana/pull/217828)
* Fixes an issue where the Saved Objects Rotate Encryption Key API would not affect sharable encrypted object types that exist in all spaces [#217625](https://github.com/elastic/kibana/pull/217625)
* Fixes an issue where refreshing multiple tabs when you log out will simultaneously log in successfully [#212148](https://github.com/elastic/kibana/pull/212148)

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
* Upcoming removal of SMS multifactor authentication method. In October, we made multifactor authentication mandatory for all users. As an additional security measure, the SMS MFA method will be removed in April. If you’re still using SMS, you will be prompted to set up a more secure MFA method, and your registered SMS MFA devices will be automatically deleted from Elastic Cloud.

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
* Disables `prompt=login` and sign out of Okta before initiating SSO. Fixes an issue when using organization SAML SSO where users are required to re-authenticate with the external IdP due to ForceAuthn=true being sent in SAML requests. SAML requests will now send `ForceAuthn=false`.

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
* Introduces new deployment performance metrics charts. AutoOps provides aggregate metrics at the cluster level for key performance indicators. The data is tier-based, offering users a comprehensive understanding of each tier and the entire cluster.
* Deprecates Cloud Defend billing alerts. Following the deprecation of Cloud Defend in {{serverless-short}}, removes the billing logic associated with the feature.

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
