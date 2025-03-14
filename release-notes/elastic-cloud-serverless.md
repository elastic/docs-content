---
navigation_title: "Elastic Cloud Serverless"
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/serverless-changelog.html
---

# {{serverless-full}} changelog [elastic-cloud-serverless-changelog]
Review the changes, fixes, and more to {{serverless-full}}.

For {{serverless-full}} API changes, refer to [APIs Changelog](https://www.elastic.co/docs/api/changes).

For Cloud Console changes, check out [Elastic Cloud Hosted release notes](asciidocalypse://docs/cloud/docs/release-notes/cloud-hosted/index.md).

% Release notes include only features, enhancements, and fixes. Add breaking changes, deprecations, and known issues to the applicable release notes sections.

% ## version.next [elastic-cloud-serverless-changelog-releasedate]

% ### Features and enhancements [elastic-cloud-serverless-releasedate-features-enhancements]

% ### Fixes [elastic-cloud-serverless-releasedate-fixes]

## March 10, 2025 [serverless-changelog-03102025]

### Features and enhancements [elastic-cloud-serverless-03102025-features-enhancements]
* The Create Rule flyout, used by solutions, now features the improved rule form in Elastic Observability Serverless ({kibana-pull}206685[#206685]).
* Resolves duplicate conversations in Elastic Observability Serverless ({kibana-pull}208044[#208044]).
* Split the SLO Details view from the Overview page in Elastic Observability Serverless ({kibana-pull}212826[#212826]).
* Adds the reason message to the rules recovery context in Elastic Observability Serverless ({kibana-pull}211411[#211411]).
* Runtime metrics dashboards now support different ingest paths in Elastic Observability Serverless ({kibana-pull}211822[#211822]).
* Adds SSL options for Fleet Server hosts settings in Fleet ({kibana-pull}208091[#208091]).
* Introduces globe projection for Dashboards and visualizations ({kibana-pull}212437[#212437]).
* Registered a custom integrations search provider in Fleet ({kibana-pull}213013[#213013]).
* Adds support for searchAfter and PIT (point-in-time) parameters in the Get Agents List API in Fleet ({kibana-pull}213486[#213486]).

### Fixes [elastic-cloud-serverless-03102025-fixes]
* Fixes an issue where Korean characters were split into two characters with a space in between when typing in the options list search input in Dashboards and visualizations ({kibana-pull}213164[#213164]).
* Prevented crashes when editing a Lens chart with a by-reference annotation layer in Dashboards and visualizations ({kibana-pull}213090[#213090]).
* Improves instructions for the summarize function in Elastic Observability Serverless ({kibana-pull}212936[#212936]).
* Fixes a "Product Documentation function not available" error in Elastic Observability Serverless ({kibana-pull}212676[#212676]).
* Fixes conversation tests in Elastic Observability Serverless ({kibana-pull}213338[#213338]).
* Allowed wildcard filters in SLO queries in Elastic Observability Serverless ({kibana-pull}213119[#213119]).
* Fixes missing summary data in error samples in Elastic Observability Serverless ({kibana-pull}213430[#213430]).
* Fixes a failing test: Stateful Observability - Deployment-agnostic A… in Elastic Observability Serverless ({kibana-pull}213530[#213530]).
* Reduced the review rule upgrade endpoint response size in Elastic Security Serverless ({kibana-pull}211045[#211045]).
* Refactors conversation pagination in Elastic Security Serverless ({kibana-pull}211831[#211831]).
* Fixes alert insights color order in Elastic Security Serverless ({kibana-pull}212980[#212980]).
* Prevented empty conversation IDs in the chat/complete route in Elastic Security Serverless ({kibana-pull}213049[#213049]).
* Fixes issues with unstructured syslog flow in Elastic Security Serverless ({kibana-pull}213042[#213042]).
* Adds bulkGetUserProfiles privilege to Security Feature in Elastic Security Serverless ({kibana-pull}211824[#211824]).
* Fixes a Risk Score Insufficient Privileges warning due to missing cluster privileges in Elastic Security Serverless ({kibana-pull}212405[#212405]).
* Updates Bedrock prompts in Elastic Security Serverless ({kibana-pull}213160[#213160]).
* Adds organizationId and projectId OpenAI headers, along with support for arbitrary headers in Elastic Security Serverless ({kibana-pull}213117[#213117]).
* Ensures dataview selections persist reliably in timeline for Elastic Security Serverless ({kibana-pull}211343[#211343]).
* Fixes incorrect validation when a named parameter was used as a function in ES|QL ({kibana-pull}213355[#213355]).
* Fixes incorrect overall swim lane height in Machine Learning ({kibana-pull}213245[#213245]).
* Prevented a crash when applying a filter in the Machine Learning anomaly table ({kibana-pull}213075[#213075]).
* Fixes suppressed alerts alignment in the alert flyout in Elastic Security Serverless ({kibana-pull}213029[#213029]).
* Fixes an issue in solution project navigation where panels sometimes failed to toggle closed ({kibana-pull}211852[#211852]).
* Updates wording for options in the sortBy dropdown component ({kibana-pull}206464[#206464]).
* Allowed EU hooks hostname in the Torq connector for Elastic Security Serverless ({kibana-pull}212563[#212563]).

## March 3, 2025 [serverless-changelog-03032025]

### Features and enhancements [elastic-cloud-serverless-03032025-features-enhancements]
* Introduces a background task that streamlines the upgrade process for agentless deployments in Elastic Security Serverless ({kibana-pull}207143[#207143]).
* Improves asset inventory onboarding with better context integration in Elastic Security Serverless ({kibana-pull}212315[#212315]).
* Adds syntax highlighting for working with ES|QL queries in Elastic Observability Serverless ({kibana-pull}212669[#212669]).
* Updates the delete confirmation modal in Elastic Observability Serverless ({kibana-pull}212695[#212695]).
* Removes the enablement check in `PUT /api/streams/{id}` for classic streams ({kibana-pull}212289[#212289]).

### Fixes [elastic-cloud-serverless-03032025-fixes]
* Fixes issues affecting popularity scores in Discover ({kibana-pull}211201[#211201]).
* Corrects sorting behavior in the profiler storage explorer for Elastic Observability Serverless ({kibana-pull}212583[#212583]).
* Adds a loader to prevent flickering in the KB settings tab in Elastic Observability Serverless ({kibana-pull}212678[#212678]).
* Resolves incorrect enable button behavior in the Entity Store modal in Elastic Security Serverless ({kibana-pull}212078[#212078]).
* Converts the isolate host action into a standalone flyout in Elastic Security Serverless ({kibana-pull}211853[#211853]).
* Ensures model responses are correctly persisted to the chosen conversation ID in Elastic Security Serverless ({kibana-pull}212122[#212122]).
* Corrects image resizing issues for `xpack.security.loginAssistanceMessage` in Elastic Security Serverless ({kibana-pull}212035[#212035]).
* Fixes automatic import to correctly generate pipelines for parsing CSV files with special characters in Elastic Security Serverless column names ({kibana-pull}212513[#212513]).
* Fixes validation issues for empty EQL queries in Elastic Security Serverless ({kibana-pull}212117[#212117]).
* Resolves dual hover actions in the table tab in Elastic Security Serverless ({kibana-pull}212316[#212316]).
* Updates structured log processing to support multiple log types in Elastic Security Serverless ({kibana-pull}212611[#212611]).
* Ensures the delete model dialog prevents accidental multiple clicks in Machine Learning ({kibana-pull}211580[#211580]).

## February 24, 2025 [serverless-changelog-02242025]

### Features and enhancements [elastic-cloud-serverless-02242025-features-enhancements]
* Exposes SSL options for {es} and remote {es} outputs in the UI ({kibana-pull}208745[#208745]).
* Displays a warning and a tooltip for the `_score` column in the Discover grid ({kibana-pull}211013[#211013]).
* Allows command/ctrl click for the "New" action in the top navigation ({kibana-pull}210982[#210982]).
* Adds the ability for a user to create an API Key in synthetics settings that applies only to specified space(s) ({kibana-pull}211816[#211816]).
* Adds "unassigned" as an asset criticality level for `bulk_upload` ({kibana-pull}208884[#208884]).
* Sets the Enable visualizations in flyout advanced setting to "On" by default ({kibana-pull}211319[#211319]).
* Preserves user-made chart configurations when changing the query if the actions are compatible with the current chart, such as adding a "where" filter or switching compatible chart types. ({kibana-pull}210780[#210780]).
* Adds effects when clicking the favorite button in the list of dashboards and ES|QL queries, and adds favorite button to breadcrumb trails ({kibana-pull}201596[#201596]).
* Enable `/api/streams/{id}/_group` endpoints for GroupStreams ({kibana-pull}210114[#210114]).

### Fixes [elastic-cloud-serverless-02242025-fixes]
* Fixes Discover session embeddable drilldown ({kibana-pull}211678[#211678]).
* Passes system message to inferenceCliente.chatComplete ({kibana-pull}211263[#211263]).
* Ensures system message is passed to the inference plugin ({kibana-pull}209773[#209773]).
* Adds automatic re-indexing when encountering `semantic_text` bug ({kibana-pull}210386[#210386]).
* Removes unnecessary breadcrumbs in profiling ({kibana-pull}211081[#211081]).
* Adds minHeight to profiler flamegraphs ({kibana-pull}210443[#210443]).
* Adds system message in copy conversation JSON payload ({kibana-pull}212009[#212009]).
* Changes the confirmation message after RiskScore Saved Object configuration is updated ({kibana-pull}211372[#211372]).
* Adds a no data message in the flyout when an analyzer is not enabled ({kibana-pull}211981[#211981]).
* Fixes the Fleet Save and continue button ({kibana-pull}211563[#211563]).
* Suggest triple quotes when the user selects the `KQL` / `QSTR` ({kibana-pull}211457[#211457]).
* Adds remote cluster instructions for syncing integrations ({kibana-pull}211997[#211997]).
* Allows deploying a model after a failed deployment in Machine Learning ({kibana-pull}211459[#211459]).
* Ensures the members array is unique for GroupStreamDefinitions ({kibana-pull}210089[#210089]).
* Improves function search for easier navigation and discovery ({kibana-pull}210437[#210437]).

## February 17, 2025 [serverless-changelog-02172025]

### Features and enhancements [elastic-cloud-serverless-02172025-features-enhancements]
* Adds alert status management to the AI Assistant connector ({kibana-pull}203729[#203729]).
* Enables the new Borealis theme ({kibana-pull}210468[#210468]).
* Applies compact Display options Popover layout ({kibana-pull}210180[#210180]).
* Increases search timeout toast lifetime to 1 week ({kibana-pull}210576[#210576]).
* Improves performance in `dependencies` endpoints to prevent high CPU usage ({kibana-pull}209999[#209999]).
* Adds "Logs" tab to mobile services ({kibana-pull}209944[#209944]).
* Adds "All logs" data view to the Classic navigation ({kibana-pull}209042[#209042]).
* Changes default to "native" function calling if the connector configuration is not exposed ({kibana-pull}210455[#210455]).
* Updates entity insight badge to open entity flyouts ({kibana-pull}208287[#208287]).
* Standardizes actions in Alerts KPI visualizations ({kibana-pull}206340[#206340]).
* Allows the creation of dynamic aggregations controls for ES|QL charts ({kibana-pull}210170[#210170]).
* Fixes the values control FT ({kibana-pull}211159[#211159]).
* Trained models: Replaces the download button by extending the deploy action ({kibana-pull}205699[#205699]).
* Adds the `useCustomDragHandle` property ({kibana-pull}210463[#210463]).

### Fixes [elastic-cloud-serverless-02172025-fixes]
* Fixes an issue where clicking on the name badge for a synthetics monitor on an SLO details page would lead to a page that failed to load monitor details ({kibana-pull}210695[#210695]).
* Fixes an issue where the popover in the rules page may get stuck when being clicked more than once ({kibana-pull}208996[#208996]).
* Fixes an error in the cases list when the case assignee is an empty string ({kibana-pull}209973[#209973]).
* Fixes an issue with assigning color mappings when multiple layers are defined ({kibana-pull}208571[#208571]).
* Fixes an issue where behind text colors were not correctly assigned, such as in `Pie`, `Treemap` and `Mosaic` charts. ({kibana-pull}209632[#209632]).
* Fixes an issue where dynamic coloring has been disabled from Last value aggregation types ({kibana-pull}209110[#209110]).
* Fixes panel styles ({kibana-pull}210113[#210113]).
* Fixes incorrectly serialized `searchSessionId` attribute ({kibana-pull}210765[#210765]).
* Fixes the "Save to library" action that could break the chart panel ({kibana-pull}210125[#210125]).
* Fixes link settings not persisting ({kibana-pull}211041[#211041]).
* Fixes "Untitled" export title when exporting CSV from a dashboard ({kibana-pull}210143[#210143]).
* Missing items in the trace waterfall shouldn't break it entirely ({kibana-pull}210210[#210210]).
* Removes unused `error.id` in `getErrorGroupMainStatistics` queries ({kibana-pull}210613[#210613]).
* Fixes connector test in MKI ({kibana-pull}211235[#211235]).
* Clicking a link in the host/user flyout does not refresh details panel ({kibana-pull}209863[#209863]).
* Makes 7.x signals/alerts compatible with 8.18 alerts UI ({kibana-pull}209936[#209936]).
* Handle empty categorization results from LLM ({kibana-pull}210420[#210420]).
* Remember page index in Rule Updates table ({kibana-pull}209537[#209537]).
* Adds concurrency limits and request throttling to prebuilt rule routes ({kibana-pull}209551[#209551]).
* Fixes package name validation on the Datastream page ({kibana-pull}210770[#210770]).
* Makes entity store description more generic ({kibana-pull}209130[#209130]).
* Deletes 'critical services' count from the Entity Analytics Dashboard header ({kibana-pull}210827[#210827]).
* Disables sorting IP ranges in value list modal ({kibana-pull}210922[#210922]).
* Updates entity store copies ({kibana-pull}210991[#210991]).
* Fixes generated name for integration title ({kibana-pull}210916[#210916]).
* Fixes formatting and sorting for custom ES|QL vars ({kibana-pull}209360[#209360]).
* Fixes WHERE autocomplete with MATCH before LIMIT ({kibana-pull}210607[#210607]).
* Updates install snippets to include all platforms ({kibana-pull}210249[#210249]).
* Updates component templates with deprecated setting ({kibana-pull}210200[#210200]).
* Hides saved query controls in AIOps ({kibana-pull}210556[#210556]).
* Fixes unattended Transforms in integration packages not automatically restarting after reauthorizing ({kibana-pull}210217[#210217]).
* Reinstates switch to support generating public URLs for embed when supported ({kibana-pull}207383[#207383]).
* Provides a fallback view to recover from Stack Alerts page filters bar errors ({kibana-pull}209559[#209559]).

## February 10, 2025 [serverless-changelog-02102025]

### Features and enhancements [elastic-cloud-serverless-02102025-features-enhancements]
* Rule connector - handle multiple prompt ({kibana-pull}209221[#209221]).
* Added max_file_size_bytes advanced option to malware for all operating systems ({kibana-pull}209541[#209541]).
* Introduce GroupStreams ({kibana-pull}208126[#208126]).
* Service example added to entity store upload ({kibana-pull}209023[#209023]).
* Update the `bucket_span` for ML jobs in the security_host module ({kibana-pull}209663[#209663]).
* Improved handling for operator-defined role mappings ({kibana-pull}208710[#208710]).
* Added `object_src` directive to `Content-Security-Policy-Report-Only` header ({kibana-pull}209306[#209306]).

### Fixes [elastic-cloud-serverless-02102025-fixes]
* Fixes highlight for HJSON ({kibana-pull}208858[#208858]).
* Disable pointer events on drag + resize ({kibana-pull}208647[#208647]).
* Restore show missing dataView error message in case of missing datasource ({kibana-pull}208363[#208363]).
* Fixes issue with `Amsterdam` theme where charts render with the incorrect background color ({kibana-pull}209595[#209595]).
* Fixes an issue in Lens Table where a split-by metric on a terms rendered incorrect colors in table cells ({kibana-pull}208623[#208623]).
* Force return 0 on empty buckets on count if null flag is disabled ({kibana-pull}207308[#207308]).
* Fixes all embeddables rebuilt on refresh ({kibana-pull}209677[#209677]).
* Fixes using data view runtime fields during rule execution for the custom threshold rule ({kibana-pull}209133[#209133]).
* Running processes missing from processes table ({kibana-pull}209076[#209076]).
* Fixes missing exception stack trace ({kibana-pull}208577[#208577]).
* Fixes the preview chart in the Custom Threshold rule creation form when the field name has slashes ({kibana-pull}209263[#209263]).
* Display No Data in Threshold breached component ({kibana-pull}209561[#209561]).
* Fixes an issue where APM charts were rendered without required transaction type or service name, causing excessive alerts to appear ({kibana-pull}209552[#209552]).
* Fixed bug that caused issues with loading SLOs by status, SLI type, or instance id ({kibana-pull}209910[#209910]).
* Update colors in the AI Assistant icon ({kibana-pull}210233[#210233]).
* Update the simulate function calling setting to support "auto" ({kibana-pull}209628[#209628]).
* Fixes structured log template to use single quotes ({kibana-pull}209736[#209736]).
* Fixes ES|QL alert on alert ({kibana-pull}208894[#208894]).
* Fixes issue with multiple ip addresses in strings ({kibana-pull}209475[#209475]).
* Keeps the histogram config on time change ({kibana-pull}208053[#208053]).
* WHERE replacement ranges correctly generated for every case ({kibana-pull}209684[#209684]).
* Updates removed params of the Fleet -> Logstash output configurations ({kibana-pull}210115[#210115]).
* Fixes log rate analysis, change point detection, and pattern analysis embeddables not respecting filters from Dashboard's controls ({kibana-pull}210039[#210039]).

## February 3, 2025 [serverless-changelog-02032025]

### Features and enhancements [elastic-cloud-serverless-02032025-features-enhancements]
* Rework saved query privileges ({kibana-pull}202863[#202863]).
* In-table search ({kibana-pull}206454[#206454]).
* Refactor RowHeightSettings component to EUI layout ({kibana-pull}203606[#203606]).
* Chat history details in conversation list ({kibana-pull}207426[#207426]).
* Cases assignees sub feature ({kibana-pull}201654[#201654]).
* Adds preview logged requests for new terms, threshold, query, ML rule types ({kibana-pull}203320[#203320]).
* Adds in-text citations to security solution AI assistant responses ({kibana-pull}206683[#206683]).
* Remove Tech preview badge for GA ({kibana-pull}208523[#208523]).
* Adds new View job detail flyouts for Anomaly detection and Data Frame Analytics ({kibana-pull}207141[#207141]).
* Adds a default "All logs" temporary data view in the Observability Solution view ({kibana-pull}205991[#205991]).
* Adds Knowledge Base entries API ({kibana-pull}206407[#206407]).
* Adds Kibana Support for Security AI Prompts Integration ({kibana-pull}207138[#207138]).
* Changes to support event.ingested as a configurable timestamp field for init and enable endpoints ({kibana-pull}208201[#208201]).
* Adds Spaces column to Anomaly Detection, Data Frame Analytics and Trained Models management pages ({kibana-pull}206696[#206696]).
* Adds simple flyout based file upload to Search ({kibana-pull}206864[#206864]).
* Bump kube-stack Helm chart onboarding version ({kibana-pull}208217[#208217]).
* Log deprecated api usages ({kibana-pull}207904[#207904]).
* Added support for human readable name attribute for saved objects audit events ({kibana-pull}206644[#206644]).
* Enhanced Role management to manage larger number of roles by adding server side filtering, pagination and querying ({kibana-pull}194630[#194630]).
* Added Entity Store data view refresh task ({kibana-pull}208543[#208543]).
* Increase maximum Osquery timeout to 24 hours ({kibana-pull}207276[#207276]).

### Fixes [elastic-cloud-serverless-02032025-fixes]
* Remove use of `fr` unit ({kibana-pull}208437[#208437]).
* Fixes load more request size ({kibana-pull}207901[#207901]).
* Persist `runPastTimeout` setting ({kibana-pull}208611[#208611]).
* Allow panel to extend past viewport on resize ({kibana-pull}208828[#208828]).
* Knowledge base install updates ({kibana-pull}208250[#208250]).
* Fixes conversations test in MKI ({kibana-pull}208649[#208649]).
* Fixes ping heatmap regression when Inspect flag is turned off !! ({kibana-pull}208726[#208726]).
* Fixes monitor status rule for empty kql query results !! ({kibana-pull}208922[#208922]).
* Fixes multiple flyouts ({kibana-pull}209158[#209158]).
* Adds missing fields to input manifest templates ({kibana-pull}208768[#208768]).
* "Select a Connector" popup does not show up after the user selects any connector and then cancels it from Endpoint Insights ({kibana-pull}208969[#208969]).
* Logs shard failures for eql event queries on rule details page and in event log ({kibana-pull}207396[#207396]).
* Adds filter to entity definitions schema ({kibana-pull}208588[#208588]).
* Fixes missing ecs mappings ({kibana-pull}209057[#209057]).
* Apply the timerange to the fields fetch in the editor ({kibana-pull}208490[#208490]).
* Update java.ts - removing serverless link ({kibana-pull}204571[#204571]).

## January 27, 2025 [serverless-changelog-01272025]

### Features and enhancements [elastic-cloud-serverless-01272025-features-enhancements]
* Breaks out timeline and note privileges in Elastic Security Serverless ({{kibana-pull}}201780[#201780]).
* Adds service enrichment to the detection engine in Elastic Security Serverless ({{kibana-pull}}206582[#206582]).
* Updates the Entity Store Dashboard to prompt for the Service Entity Type in Elastic Security Serverless ({{kibana-pull}}207336[#207336]).
* Adds `enrichPolicyExecutionInterval` to entity enablement and initialization APIs in Elastic Security Serverless ({{kibana-pull}}207374[#207374]).
* Introduces a lookback period configuration for the Entity Store in Elastic Security Serverless ({{kibana-pull}}206421[#206421]).
* Allows pre-configured connectors to opt into exposing their configurations by setting `exposeConfig` in Alerting ({{kibana-pull}}207654[#207654]).
* Adds selector syntax support to log source profiles in Elastic Observability Serverless ({{kibana-pull}}206937[#206937]).
* Displays stack traces in the logs overview tab in Elastic Observability Serverless ({{kibana-pull}}204521[#204521]).
* Enables the use of the rule form to create rules in Elastic Observability Serverless ({{kibana-pull}}206774[#206774]).
* Checks only read privileges of existing indices during rule execution in Elastic Security Serverless ({{kibana-pull}}177658[#177658]).
* Updates KNN search and query template autocompletion in Elasticsearch Serverless ({{kibana-pull}}207187[#207187]).
* Updates JSON schemas for code editors in Machine Learning ({{kibana-pull}}207706[#207706]).
* Reindexes the `.kibana_security_session_1` index to the 8.x format in Security ({{kibana-pull}}204097[#204097]).

### Fixes [elastic-cloud-serverless-01272025-fixes]
* Fixes editing alerts filters for multi-consumer rule types in Alerting ({{kibana-pull}}206848[#206848]).
* Resolves an issue where Chrome was no longer hidden for reports in Dashboards and Visualizations ({{kibana-pull}}206988[#206988]).
* Updates library transforms and duplicate functionality in Dashboards and Visualizations ({{kibana-pull}}206140[#206140]).
* Fixes an issue where drag previews are now absolutely positioned in Dashboards and Visualizations ({{kibana-pull}}208247[#208247]).
* Fixes an issue where an accessible label now appears on the range slider in Dashboards and Visualizations ({{kibana-pull}}205308[#205308]).
* Fixes a dropdown label sync issue when sorting by "Type" ({{kibana-pull}}206424[#206424]).
* Fixes an access bug related to user instructions in Elastic Observability Serverless ({{kibana-pull}}207069[#207069]).
* Fixes the Open Explore in Discover link to open in a new tab in Elastic Observability Serverless ({{kibana-pull}}207346[#207346]).
* Returns an empty object for tool arguments when none are provided in Elastic Observability Serverless ({{kibana-pull}}207943[#207943]).
* Ensures similar cases count is not fetched without the proper license in Elastic Security Serverless ({{kibana-pull}}207220[#207220]).
* Fixes table leading actions to use standardized colors in Elastic Security Serverless ({{kibana-pull}}207743[#207743]).
* Adds missing fields to the AWS S3 manifest in Elastic Security Serverless ({{kibana-pull}}208080[#208080]).
* Prevents redundant requests when loading Discover sessions and toggling chart visibility in ES|QL ({{kibana-pull}}206699[#206699]).
* Fixes a UI error when agents move to an orphaned state in Fleet ({{kibana-pull}}207746[#207746]).
* Restricts non-local Elasticsearch output types for agentless integrations and policies in Fleet ({{kibana-pull}}207296[#207296]).
* Fixes table responsiveness in the Notifications feature of Machine Learning ({{kibana-pull}}206956[#206956]).

## January 13, 2025 [serverless-changelog-01132025]

### Features and enhancements [elastic-cloud-serverless-01132025-features-enhancements]
* Adds last alert status change to Elastic Security Serverless flyout ({{kibana-pull}}205224[#205224]).
* Case templates are now GA ({{kibana-pull}}205940[#205940]).
* Adds format to JSON messages in Elastic Observability Serverless Logs profile ({{kibana-pull}}205666[#205666]).
* Adds inference connector in Elastic Security Serverless AI features ({{kibana-pull}}204505[#204505]).
* Adds inference connector for Auto Import in Elastic Security Serverless ({{kibana-pull}}206111[#206111]).
* Adds Feature Flag Support for Cloud Security Posture Plugin in Elastic Security Serverless ({{kibana-pull}}205438[#205438]).
* Adds the ability to sync Machine Learning saved objects to all spaces ({{kibana-pull}}202175[#202175]).
* Improves messages for recovered alerts in Machine Learning Transforms ({{kibana-pull}}205721[#205721]).

### Fixes [elastic-cloud-serverless-01132025-fixes]
* Fixes an issue where "KEEP" columns are not applied after an Elasticsearch error in Discover ({{kibana-pull}}205833[#205833]).
* Resolves padding issues in the document comparison table in Discover ({{kibana-pull}}205984[#205984]).
* Fixes a bug affecting bulk imports for the knowledge base in Elastic Observability Serverless ({{kibana-pull}}205075[#205075]).
* Enhances the Find API by adding cursor-based pagination (search_after) as an alternative to offset-based pagination ({{kibana-pull}}203712[#203712]).
* Updates Elastic Observability Serverless to use architecture-specific Elser models ({{kibana-pull}}205851[#205851]).
* Fixes dynamic batching in the timeline for Elastic Security Serverless ({{kibana-pull}}204034[#204034]).
* Resolves a race condition bug in Elastic Security Serverless related to OpenAI errors ({{kibana-pull}}205665[#205665]).
* Improves the integration display by ensuring all policies are listed in Elastic Security Serverless ({{kibana-pull}}205103[#205103]).
* Renames color variables in the user interface for better clarity and consistency  ({{kibana-pull}}204908[#204908]).
* Allows editor suggestions to remain visible when the inline documentation flyout is open in ES|QL ({{kibana-pull}}206064[#206064]).
* Ensures the same time range is applied to documents and the histogram in ES|QL ({{kibana-pull}}204694[#204694]).
* Fixes validation for the "required" field in multi-text input fields in Fleet ({{kibana-pull}}205768[#205768]).
* Fixes timeout issues for bulk actions in Fleet ({{kibana-pull}}205735[#205735]).
* Handles invalid RRule parameters to prevent infinite loops in alerts ({{kibana-pull}}205650[#205650]).
* Fixes privileges display for features and sub-features requiring "All Spaces" permissions in Fleet ({{kibana-pull}}204402[#204402]).
* Prevents password managers from modifying disabled input fields ({{kibana-pull}}204269[#204269]).
* Updates the listing control in the user interface ({{kibana-pull}}205914[#205914]).
* Improves consistency in the help dropdown design ({{kibana-pull}}206280[#206280]).

## January 6, 2025 [serverless-changelog-01062025]

### Features and enhancements [elastic-cloud-serverless-01062025-features-enhancements]
* Introduces case observables in Elastic Security Serverless ({{kibana-pull}}190237[#190237]).
* Adds a JSON field called "additional fields" to ServiceNow cases when sent using connector, containing the internal names of the ServiceNow table columns ({{kibana-pull}}201948[#201948]).
* Adds the ability to configure the appearance color mode to sync dark mode with the system value ({{kibana-pull}}203406[#203406]).
* Makes the "Copy" action visible on cell hover in Discover ({{kibana-pull}}204744[#204744]).
* Updates the `EnablementModalCallout` name to `AdditionalChargesMessage` in Elastic Security Serverless ({{kibana-pull}}203061[#203061]).
* Adds more control over which Elastic Security Serverless alerts in Attack Discovery are included as context to the large language model ({{kibana-pull}}205070[#205070]).
* Adds a consistent layout and other UI enhancements for {{ml}} pages ({{kibana-pull}}203813[#203813]).

### Fixes [elastic-cloud-serverless-01062025-fixes]
* Fixes an issue that caused dashboards to lag when dragging the time slider ({{kibana-pull}}201885[#201885]).
* Updates the CloudFormation template to the latest version and adjusts the documentation to reflect the use of a single Firehose stream created by the new template ({{kibana-pull}}204185[#204185]).
* Fixes Integration and Datastream name validation in Elastic Security Serverless ({{kibana-pull}}204943[#204943]).
* Fixes an issue in the Automatic Import process where there is now inclusion of the `@timestamp` field in ECS field mappings whenever possible ({{kibana-pull}}204931[#204931]).
* Allows Automatic Import to safely parse Painless field names that are not valid Painless identifiers in `if` contexts ({{kibana-pull}}205220[#205220]).
* Aligns the Box Native Connector configuration fields with the source of truth in the connectors codebase, correcting mismatches and removing unused configurations ({{kibana-pull}}203241[#203241]).
* Fixes the "Show all agent tags" option in Fleet when the agent list is filtered ({{kibana-pull}}205163[#205163]).
* Updates the Results Explorer flyout footer buttons alignment in Data Frame Analytics ({{kibana-pull}}204735[#204735]).
* Adds a missing space between lines in the Data Frame Analytics delete job modal ({{kibana-pull}}204732[#204732]).
* Fixes an issue where the Refresh button in the Anomaly Detection Datafeed counts table was unresponsive ({{kibana-pull}}204625[#204625]).
* Fixes the inference timeout check in File Upload ({{kibana-pull}}204722[#204722]).
* Fixes the side bar navigation for the Data Visualizer ({{kibana-pull}}205170[#205170]).

## December 16, 2024 [serverless-changelog-12162024]

### Features and enhancements [elastic-cloud-serverless-12162024-features-enhancements]
* Optimizes the Kibana Trained Models API ({{kibana-pull}}200977[#200977]).
* Adds a **Create Case** action to the **Log rate analysis** page ({{kibana-pull}}201549[#201549]).
* Improves AI Assistant’s response quality by giving it access to Elastic’s product documentation ({{kibana-pull}}199694[#199694]).
* Adds support for suppressing EQL sequence alerts ({{kibana-pull}}189725[#189725]).
* Adds an **Advanced settings** section to the SLO form ({{kibana-pull}}200822[#200822]).
* Adds a new sub-feature privilege under **Synthetics and Uptime** `Can manage private locations` ({{kibana-pull}}201100[#201100]).

### Fixes [elastic-cloud-serverless-12162024-fixes]
* Fixes point visibility regression ({{kibana-pull}}202358[#202358]).
* Improves help text of creator and view count features on dashboard listing page ({{kibana-pull}}202488[#202488]).
* Highlights matching field values when performing a KQL search on a keyword field ({{kibana-pull}}201952[#201952]).
* Supports "Inspect" in saved search embeddables ({{kibana-pull}}202947[#202947]).
* Fixes your ability to clear the user-specific system prompt ({{kibana-pull}}202279[#202279]).
* Fixes error when opening rule flyout ({{kibana-pull}}202386[#202386]).
* Fixes to Ops Genie as a default connector ({{kibana-pull}}201923[#201923]).
* Fixes actions on charts ({{kibana-pull}}202443[#202443]).
* Adds flyout to table view in Infrastructure Inventory ({{kibana-pull}}202646[#202646]).
* Fixes service names with spaces not being URL encoded properly for `context.viewInAppUrl` ({{kibana-pull}}202890[#202890]).
* Allows access query logic to handle user ID and name conditions ({{kibana-pull}}202833[#202833]).
* Fixes APM rule error message for invalid KQL filter ({{kibana-pull}}203096[#203096]).
* Rejects CEF logs from Automatic Import and redirects you to the CEF integration instead ({{kibana-pull}}201792[#201792]).
* Updates the install rules title and message ({{kibana-pull}}202226[#202226]).
* Fixes error on second entity engine init API call ({{kibana-pull}}202903[#202903]).
* Restricts unsupported log formats ({{kibana-pull}}202994[#202994]).
* Removes errors related to Enterprise Search nodes ({{kibana-pull}}202437[#202437]).
* Improves web crawler name consistency ({{kibana-pull}}202738[#202738]).
* Fixes editor cursor jumpiness ({{kibana-pull}}202389[#202389]).
* Fixes rollover datastreams on subobjects mapper exception ({{kibana-pull}}202689[#202689]).
* Fixes spaces sync to retrieve 10,000 trained models ({{kibana-pull}}202712[#202712]).
* Fixes log rate analysis embeddable error on the Alerts page ({{kibana-pull}}203093[#203093]).
* Fixes Slack API connectors not displayed under Slack connector type when adding new connector to rule ({{kibana-pull}}202315[#202315]).

## December 9, 2024 [serverless-changelog-12092024]

### Features and enhancements [elastic-cloud-serverless-12092024-features-enhancements]
* Elastic Observability Serverless adds a new sub-feature for managing private locations ({{kibana-pull}}201100[#201100]).
* Elastic Observability Serverless adds the ability to configure SLO advanced settings from the UI ({{kibana-pull}}200822[#200822]).
* Elastic Security Serverless adds support for suppressing EQL sequence alerts ({{kibana-pull}}189725[#189725]).
* Elastic Security Serverless adds a `/trained_models_list` endpoint to retrieve complete data for the Trained Model UI ({{kibana-pull}}200977[#200977]).
* Machine Learning adds an action to include log rate analysis in a case ({{kibana-pull}}199694[#199694]).
* Machine Learning enhances the Kibana API to optimize trained models ({{kibana-pull}}201549[#201549]).

### Fixes [elastic-cloud-serverless-12092020-fixes]
* Fixes Slack API connectors not being displayed under the Slack connector type when adding a new connector to a rule in Alerting ({{kibana-pull}}202315[#202315]).
* Fixes point visibility regression in dashboard visualizations ({{kibana-pull}}202358[#202358]).
* Improves help text for creator and view count features on the Dashboard listing page ({{kibana-pull}}202488[#202488]).
* Highlights matching field values when performing a KQL search on a keyword field in Discover ({{kibana-pull}}201952[#201952]).
* Adds support for the **Inspect** option in saved search embeddables in Discover ({{kibana-pull}}202947[#202947]).
* Enables the ability to clear user-specific system prompts in Elastic Observability Serverless ({{kibana-pull}}202279[#202279]).
* Fixes an error when opening the rule flyout in Elastic Observability Serverless ({{kibana-pull}}202386[#202386]).
* Improves handling of Opsgenie as the default connector in Elastic Observability Serverless ({{kibana-pull}}201923[#201923]).
* Fixes issues with actions on charts in Elastic Observability Serverless ({{kibana-pull}}202443[#202443]).
* Adds a flyout to the table view in Infrastructure Inventory in Elastic Observability Serverless ({{kibana-pull}}202646[#202646]).
* Fixes service names with spaces not being URL-encoded properly for `{{context.viewInAppUrl}}` in Elastic Observability Serverless ({{kibana-pull}}202890[#202890]).
* Enhances access query logic to handle user ID and name conditions in Elastic Observability Serverless ({{kibana-pull}}202833[#202833]).
* Fixes an APM rule error message when a KQL filter is invalid in Elastic Observability Serverless ({{kibana-pull}}203096[#203096]).
* Restricts and rejects CEF logs in automatic import and redirects them to the CEF integration in Elastic Security Serverless ({{kibana-pull}}201792[#201792]).
* Updates the copy of the install rules title and message in Elastic Security Serverless ({{kibana-pull}}202226[#202226]).
* Clears errors on the second entity engine initialization API call in Elastic Security Serverless ({{kibana-pull}}202903[#202903]).
* Restricts unsupported log formats in Elastic Security Serverless ({{kibana-pull}}202994[#202994]).
* Removes errors related to Enterprise Search nodes in Elasticsearch Serverless ({{kibana-pull}}202437[#202437]).
* Ensures consistency in web crawler naming in Elasticsearch Serverless ({{kibana-pull}}202738[#202738]).
* Fixes editor cursor jumpiness in ES|QL ({{kibana-pull}}202389[#202389]).
* Implements rollover of data streams on subobject mapper exceptions in Fleet ({{kibana-pull}}202689[#202689]).
* Fixes trained models to retrieve up to 10,000 models when spaces are synced in Machine Learning ({{kibana-pull}}202712[#202712]).
* Fixes a Log Rate Analysis embeddable error on the Alerts page in AiOps ({{kibana-pull}}203093[#203093]).

## December 3, 2024 [serverless-changelog-12032024]

### Features and enhancements [elastic-cloud-serverless-12032024-features-enhancements]
* Adds tabs for Import Entities and Engine Status to the Entity Store ({{kibana-pull}}201235[#201235]).
* Adds status tracking for agentless integrations to {{fleet}} ({{kibana-pull}}199567[#199567]).
* Adds a new {{ml}} module that can detect anomalous activity in host-based logs ({{kibana-pull}}195582[#195582]).
* Allows custom Mapbox Vector Tile sources to style map layers and provide custom legends ({{kibana-pull}}200656[#200656]).
* Excludes stale SLOs from counts of healthy and violated SLOs ({{kibana-pull}}201027[#201027]).
* Adds a **Continue without adding integrations** button to the {{elastic-sec}} Dashboards page that takes you to the Entity Analytics dashboard ({{kibana-pull}}201363[#201363]).
* Displays visualization descriptions under their titles ({{kibana-pull}}198816[#198816]).

### Fixes [elastic-cloud-serverless-12032024-fixes]
* Hides the **Clear** button when no filters are selected ({{kibana-pull}}200177[#200177]).
* Fixes a mismatch between how wildcards were handled in previews versus actual rule executions ({{kibana-pull}}201553[#201553]).
* Fixes incorrect Y-axis and hover values in the Service Inventory’s Log rate chart ({{kibana-pull}}201361[#201361]).
* Disables the **Add note** button in the alert details flyout for users who lack privileges ({{kibana-pull}}201707[#201707]).
* Fixes the descriptions of threshold rules that use cardinality ({{kibana-pull}}201162[#201162]).
* Disables the **Install All** button on the **Add Elastic Rules** page when rules are installing ({{kibana-pull}}201731[#201731]).
* Reintroduces a data usage warning on the Entity Analytics Enablement modal ({{kibana-pull}}201920[#201920]).
* Improves accessibility for the **Create a connector** page ({{kibana-pull}}201590[#201590]).
* Fixes a bug that could cause {{agents}} to get stuck updating during scheduled upgrades ({{kibana-pull}}202126[#202126]).
* Fixes a bug related to starting {{ml}} deployments with autoscaling and no active nodes ({{kibana-pull}}201256[#201256]).
* Initializes saved objects when the **Trained Model** page loads ({{kibana-pull}}201426[#201426]).
* Fixes the display of deployment stats for unallocated deployments of {{ml}} models ({{kibana-pull}}202005[#202005]).
* Enables the solution type search for instant deployments ({{kibana-pull}}201688[#201688]).
* Improves the consistency of alert counts across different views ({{kibana-pull}}202188[#202188]).
