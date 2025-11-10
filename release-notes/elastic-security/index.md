---
navigation_title: Elastic Security
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/release-notes.html
  - https://www.elastic.co/guide/en/security/current/whats-new.html
products:
  - id: security
---
# {{elastic-sec}} release notes

Review the changes, fixes, and more in each version of {{elastic-sec}}.

To check for security updates, go to [Security announcements for the Elastic stack](https://discuss.elastic.co/c/announcements/security-announcements/31).

:::{tip}
{{elastic-sec}} runs on {{kib}}, so we recommend also reviewing the [{{kib}} release notes](kibana://release-notes/index.md) for relevant updates.
:::

% Release notes include only features, enhancements, and fixes. Add breaking changes, deprecations, and known issues to the applicable release notes sections.

% ## version.next [elastic-security-X.X.X-notes]

% ### Features and enhancements [elastic-security-X.X.X-features-enhancements]
% *

% ### Fixes [elastic-security-X.X.X-fixes]

% *


## 9.2.0 [elastic-security-9.2.0-release-notes]

### Features and enhancements [elastic-security-9.2.0-features-enhancements]

* Adds the Security Entity Analytics risk score reset feature [#237829]({{kib-pull}}237829).
* Introduces a Security risk scoring AI Assistant tool [#233647]({{kib-pull}}233647).
* Uses {{esql}} for calculating entity risk scores [#237871]({{kib-pull}}237871).
* Enables privileged user monitoring and the Entity analytics navigation item by default [#237436]({{kib-pull}}237436).
* Enables discovering privileged users from the Entity Analytics Okta integration [#237129]({{kib-pull}}237129).
* Adds the data view picker to the **Privileged user monitoring** dashboard page [#233264]({{kib-pull}}233264).
* Implements minor UI changes on **Privileged user monitoring** dashboard page [#231921]({{kib-pull}}231921).
* Populates the `entity.attributes.Privileged` field in the entity store for users [#237038]({{kib-pull}}237038).
* Adds public APIs for attack discovery and attack discovery schedules [#236736]({{kib-pull}}236736).
* Displays total execution time for automatic migrations [#236147]({{kib-pull}}236147).
* Adds **Update missing index pattern** option to the automatic migration **Translated rules** page [#233258]({{kib-pull}}233258).
* Introduces new API endpoints for automatic migration of dashboards [#229112]({{kib-pull}}229112).
* Adds a new deployment method, "cloud connector", for the CSPM and Asset Discovery integrations [#235442]({{kib-pull}}235442), [#230137]({{kib-pull}}230137).
* Implements CDR Data View versioning and migration logic [#238547]({{kib-pull}}238547).
* Makes automatic troubleshooting generally available [#234853]({{kib-pull}}234853).
* Updates the automatic troubleshooting feature to detect warnings and failures in {{elastic-defend}} policy responses and suggest possible remediations [#231908]({{kib-pull}}231908).
* Adds an advanced setting that keeps the alert suppression window active after you close an alert, preventing new alerts during that period [#231079]({{kib-pull}}231079).
* Adds `DOES NOT MATCH` capability to indicator match rules [#227084]({{kib-pull}}227084).
* Adds the `customized_fields` and `has_base_version` fields to the `rule_source` object schema [#234793]({{kib-pull}}234793).
* Enables the auto-extract observables toggle in the alerts table for both row and bulk actions when adding alerts to a case [#235433]({{kib-pull}}235433).
* Enables the new data view picker [#234101]({{kib-pull}}234101).
* Adds a `managed` property to data views, marking Kibana-managed data views with a **Managed** tag [#223451]({{kib-pull}}223451).
* Adds support for specifying a reason when closing an alert [#226590]({{kib-pull}}226590).
* Adds a source event ID link to the alert flyout's **Highlighted fields** section, allowing you to quickly preview the event that triggered the alert [#224451]({{kib-pull}}224451).
* Updates the indicator details flyout's UI to be more consistent with the alert details flyout's UI [#230593]({{kib-pull}}230593).
* Restricts **Value report** page access to `admin` and `soc_manager` roles in the Security Analytics Complete {{serverless-short}} feature tier [#234377]({{kib-pull}}234377).
* Implements the **Value report** page for the Elastic AI SOC Engine (EASE) {{serverless-short}} project type [#228877]({{kib-pull}}228877).
* Adds conversation sharing functionality to the Security AI Assistant, allowing you to share conversations with team members [#230614]({{kib-pull}}230614).
* Adds a non-CVE reference link list to the vulnerability details flyout [#225601]({{kib-pull}}225601).
* Adds support for using the `runscript` response action on SentinelOne-enrolled hosts [#234492]({{kib-pull}}234492).
* Adds support for using the `cancel` response action on MDE-enrolled hosts [#230399]({{kib-pull}}230399).
* Adds support for trusted applications advanced mode [#230111]({{kib-pull}}230111).
* Introduces the {{elastic-defend}} **Endpoint Exceptions** sub-feature privilege [#233433]({{kib-pull}}233433).
* Adds an {{elastic-defend}} advanced policy setting that allows you to disable the firewall anti-tamper plugin or move it into detect-only mode [#236431]({{kib-pull}}236431).
* Adds two new {{elastic-defend}} advanced policy settings that allow you to opt out of collecting ransomware diagnostics on macOS [#235193]({{kib-pull}}235193).
* Adds an {{elastic-defend}} advanced policy setting to disable the filtering of file-backed volumes and CD-ROMs in the `device_control` plugin [#236620]({{kib-pull}}236620).
* Adds an {{elastic-defend}} option to remediate orphaned state by attempting to start {{agent}} service.
* Adds a new device data stream to the {{elastic-defend}} integration.
* Adds two new dashboards to the {{elastic-defend}} integration.
* Adds more {{elastic-defend}} options to the {{ls}} output, allowing for finer control.
* Increases the throughput of {{elastic-defend}}'s {{ls}} connections by increasing the maximum size it can upload at once.
* Adds {{elastic-defend}} support for device control on macOS and Windows.
* Adds architecture of PE file in Windows malware alerts to {{elastic-defend}}.
* Adds the `Endpoint.state.orphaned` indicator to {{elastic-defend}} policy response.
* Adds {{elastic-defend}} support for cluster migration.
* Adds firewall anti-tamper plug-in to protect {{elastic-endpoint}} processes against network blocking via Windows Firewall.
* Includes `origin_url`, `origin_referrer_url`, and `Ext.windows.zone_identifier` fields to {{elastic-defend}} by default to Windows image load and process events, if the information can be retrieved.
* Improves {{elastic-defend}} by integrating a new Event Tracing for Windows (ETW) provider (Microsoft-Windows-Ldap-Client) to create new event types that prebuilt endpoint rules can use to detect malicious LDAP activity.
* Improves reporting reliability and accuracy of {{elastic-defend}}'s {{es}} connection.
* Enriches {{elastic-defend}} macOS network connect events with `network.direction`. Possible values are `ingress` and `egress`.
* Improves {{elastic-defend}} malware scan queue efficiency by not blocking scan requests when an oplock for the file being scanned cannot be acquired.
* Adds an {{elastic-defend}} advanced policy setting `windows.advanced.events.security.event_disabled` that lets users disable security event collection per event ID.
* Shortens the time it takes {{elastic-defend}} to recover from a `DEGRADED` status caused by communication issues with {{agent}}.
* Improves the `verify` command to ensure {{elastic-endpoint}} service is running, otherwise {{agent}} has to fix it automatically.
* Adds experimental {{elastic-defend}} support for Windows on ARM. This is pre-release software under active development, and should not be run on any production systems. We welcome feedback in our [community Slack](https://ela.st/slack).
* Improves the reliability of {{elastic-defend}} Kafka connections.

### Fixes [elastic-security-9.2.0-fixes]

* Fixes an issue where the names of the `Security solution default` and `Security solution alerts` data views were displayed incorrectly [#238354]({{kib-pull}}238354).
* Fixes an issue where the navigation manu overlapped expandable flyouts [#236655]({{kib-pull}}236655).
* Ensures the data view picker icon is always vertically centered [#236379]({{kib-pull}}236379).
* Integrates data view logic into host KPIs charts [#236084]({{kib-pull}}236084).
* Fixes integrations RAG in automatic migration rule translations [#234211]({{kib-pull}}234211).
* Removes the feature flag for privileged user monitoring [#233960]({{kib-pull}}233960).
* Returns a 500 response code if there is an error during privileged user monitoring engine initialization [#234368]({{kib-pull}}234368).
* Ensures that privileged user `@timestamp` and `event.ingested` fields are updated when a privileged user is updated [#233735]({{kib-pull}}233735).
* Fixes a bug in privileged user monitoring index synchronization where stale users weren't removed after index pattern changes [#229789]({{kib-pull}}229789).
* Updates the privileged user monitoring UI to replace hard-coded CSS values with the EUI theme [#225307]({{kib-pull}}225307).
* Fixes incorrect threat enrichment for partially matched `AND` conditions in indicator match rules [#230773]({{kib-pull}}230773).
* Adds a validation error to prevent users from setting a custom action interval shorter than the rule's check interval [#229976]({{kib-pull}}229976).
* Fixes accessibility issues on the **Benchmarks** page [#229521]({{kib-pull}}229521).
* Simplifies the Cloud Security Posture Misconfigurations data view by removing redundancy in the index pattern definition [#227995]({{kib-pull}}227995).
* Fixes an issue causing "missing authentication credentials" warnings in `TelemetryConfigWatcher` and `PolicyWatcher`, reducing unnecessary warning log entries in the `securitySolution` plugin.
* Fixes an {{elastic-defend}} issue on Linux by preventing unnecessary locking within Malware Protections to avoid invalid watchdog firings.
* Fixes issues that could sometimes cause crashes of the {{elastic-defend}} user-mode process on very busy Windows systems.
* Adds support in {{elastic-defend}} for installing eBPF event probes on Linux endpoints when cgroup2 is mounted in a non-standard location or not mounted at all.
* Adds support in {{elastic-defend}} for installing eBPF probes on Linux endpoints when taskstats is compiled out of the kernel.
* Fixes an issue in {{elastic-defend}} where Linux network events could have source and destination bytes swapped.
* Fixes a bug where Linux capabilities were included in {{elastic-endpoint}} network events despite being disabled.
* Fixes an issue where {{elastic-defend}} would incorrectly calculate throughput capacity when sending documents to output. This may have limited event throughput on extremely busy endpoints.
* Improves the reliability of local {{elastic-defend}} administrative shell commands. In rare cases, a command could fail to execute due to issues with interprocess communication.
* Fixes an issue in {{elastic-defend}} where host isolation could auto-release incorrectly. Host isolation now only releases when {{elastic-endpoint}} becomes orphaned. Intermittent {{elastic-agent}} connectivity changes no longer alter the host isolation state.
* Fixes a bug in {{elastic-defend}} where Linux endpoints would report `process.executable` as a relative, instead of absolute, path.
* Fixes an issue which could cause {{elastic-defend}} to improperly report success when self-healing rollback attempted to terminate a process with an active debugger on Windows.
* Fixes an issue in {{elastic-defend}} installation logging where only the first character of install paths (usually 'C') was logged.
* Fixes an issue to improve reliability of health status reporting between {{elastic-endpoint}} and {{agent}}.
* Fixes a race condition in {{elastic-defend}} that occasionally resulted in corrupted process command lines on Windows. This could cause incorrect values for `process.command_line`, `process.args_count`, and `process.args`, leading to false positives.
* Fixes an issue in {{elastic-defend}} that could result in a crash if a specified {{ls}} output configuration contained a certificate that couldn't be parsed.


## 9.1.6 [elastic-security-9.1.6-release-notes]

### Features and enhancements [elastic-security-9.1.6-features-enhancements]
* Adds the `customized_fields` and `has_base_version` fields to the `rule_source` object schema  [#234793]({{kib-pull}}234793).
* Implements CDR Data View versioning and migration logic [#238547]({{kib-pull}}238547).

### Fixes [elastic-security-9.1.6-fixes]
* Fixes {{elastic-endpoint}} artifacts spaces migration to ensure all artifacts are processed [#238740]({{kib-pull}}238740).
* Fixes an issue causing "missing authentication credentials" warnings in `TelemetryConfigWatcher` and `PolicyWatcher`, reducing unnecessary warning log entries in the `securitySolution` plugin. [#237796]({{kib-pull}}237796).


## 9.1.5 [elastic-security-9.1.5-release-notes]

### Features and enhancements [elastic-security-9.1.5-features-enhancements]
* Adds an {{elastic-defend}} option to remediate orphaned state by attempting to start Elastic Agent service.
* Increases the throughput of {{elastic-defend}} Logstash connections by increasing the maximum size it can upload at once.
* Improves reliability and accuracy of reporting of the {{elastic-defend}}'s {{es}} connection.

### Fixes [elastic-security-9.1.5-fixes]
* Fixes browser fields caching to use the `dataView` ID instead of the index pattern [#234381]({{kib-pull}}234381).
* Removes `null` in confirmation dialog when bulk editing index patterns for rules [#236572]({{kib-pull}}236572).
* Fixes the URL passed to detection rule actions via the `{{context.results_link}}` placeholder [#236067]({{kib-pull}}236067).
* Fixes system prompt updates from the Conversations tab in AI Assistant [#234812]({{kib-pull}}234812).
* Fixes an issue in the Highlighted fields table in the alert details flyout [#234222]({{kib-pull}}234222).
* Fixes an issue in rule exceptions to include the `matches` operator only for supported fields [#233127]({{kib-pull}}233127).
* Adds support in {{elastic-defend}} for installing eBPF event probes on Linux endpoints when cgroup2 is mounted in a non-standard location or not mounted at all.
* Adds support in {{elastic-defend}} for installing eBPF probes on Linux endpoints when taskstats is compiled out of the kernel.
* Fixes an issue in {{elastic-defend}} where Linux network events could have source and destination bytes swapped.
* Removes `.process.thread.capabilities.permitted` and `.process.thread.capabilities.effective` from Linux network events in {{elastic-defend}}.
* Fixes an issue in {{elastic-defend}} where host isolation could auto-release incorrectly. Host isolation now only releases when {{elastic-endpoint}} becomes orphaned. Intermittent {{elastic-agent}} connectivity changes no longer alter the host isolation state.
* Fixes an issue where {{elastic-defend}} would incorrectly calculate throughput capacity when sending documents to output.  This may have limited event throughput on extremely busy endpoints.
* Fixes an issue in {{elastic-defend}} installation logging where only the first character of install paths (usually 'C') would be logged.


## 9.1.4 [elastic-security-9.1.4-release-notes]

### Features and enhancements [elastic-security-9.1.4-features-enhancements]
* Adds more Linux diagnostic process `ptrace` events.

### Fixes [elastic-security-9.1.4-fixes]
* Fixes filtering on the **Alerts** page by checking for an empty dataView [#235144]({{kib-pull}}235144).
* Fixes a bug where the toggle column functionality only functioned on the **Alerts** page [#234278]({{kib-pull}}234278).
* Fixes a bug where Linux capabilities were included in {{elastic-endpoint}} network events despite being disabled.
* Makes the delivery of {{elastic-endpoint}} command line commands more robust. In rare cases, commands could previously fail due to interprocess communication issues.

## 9.1.3 [elastic-security-9.1.3-release-notes]

### Fixes [elastic-security-9.1.3-fixes]
* Fixes a bug that prevented the vulnerability findings contextual flyout from showing details [#231778]({{kib-pull}}231778).
* Fixes an issue preventing the creation of Knowledge Base Index Entries in deployments with a large number of indices/mappings [#231376]({{kib-pull}}231376).
* Fixes a bug where Linux endpoints would report `process.executable` as a relative, instead of absolute, path.

## 9.1.2 [elastic-security-9.1.2-release-notes]

### Features and enhancements [elastic-security-9.1.2-features-enhancements]
* Adds Automatic Import documentation links for users in log description and the error message so that users have better access to the data types that are valid [#229375]({{kib-pull}}229375).
* To help identify which parts of `elastic-endpoint.exe` are using a significant amount of CPU, {{elastic-defend}} on Windows can now include CPU profiling data in diagnostics. To request CPU profiling data using the command line, refer to [{{agent}} command reference](/reference/fleet/agent-command-reference.md#_options). To request CPU profiling data using {{kib}}, check the **Collect additional CPU metrics** box when requesting {{agent}} diagnostics.
* Improves {{elastic-defend}} malware scan queue efficiency on Windows by not blocking scan requests when an oplock for the file being scanned cannot be acquired.
* Allows {{elastic-defend}} to automatically recover in some situations when it loses connectivity with {{agent}}.

### Fixes [elastic-security-9.1.2-fixes]
* Fixes privileged user monitoring index sync in non-default {{kib}} spaces [#230420]({{kib-pull}}230420).
* Only creates a privileged user monitoring default index source if one doesn't currently exist [#229693]({{kib-pull}}229693).
* Fixes a race condition in {{elastic-defend}} that may occasionally result in corrupted process command lines on Windows. When this occurs, `process.command_line`, `process.args_count` and `process.args` may be incorrect, leading to false positives.
* Due to an issue in macOS, {{elastic-defend}} would sometimes send network events without `user.name` populated. {{elastic-defend}} will now identify these events and populate `user.name` if necessary.

## 9.1.1 [elastic-security-9.1.1-release-notes]

### Features and enhancements [elastic-security-9.1.1-features-enhancements]

* Improves the reliability of {{elastic-defend}} Kafka connections.

### Fixes [elastic-security-9.1.1-fixes]
* Fixes a bug by moving the `scheduleNow` call to the privileged monitoring engine initialization step, ensuring the task is only scheduled after the engine is fully created and ready [#230263]({{kib-pull}}230263).
* Fixes a bug where the base version API route cache was not properly invalidated after rule import [#228475]({{kib-pull}}228475).
* Fixes an issue in {{elastic-defend}} performance metrics that resulted in `endpoint_uptime_percent` always being 0 for behavioral rules.

## 9.1.0 [elastic-security-9.1.0-release-notes]

### Features and enhancements [elastic-security-9.1.0-features-enhancements]

* Adds an option to update the `kibana.alert.workflow_status` field for alerts associated with attack discoveries [#225029]({{kib-pull}}225029).
* The rule execution gaps functionality is now generally available [#224657]({{kib-pull}}224657).
* Adds the Security Entity Analytics privileged user monitoring feature [#224638]({{kib-pull}}224638).
* Adds the ability to bulk fill gaps [#224585]({{kib-pull}}224585).
* Automatic migration is now generally available [#224544]({{kib-pull}}224544).
* Adds a name field to the automatic migration UI [#223860]({{kib-pull}}223860).
* Adds the ability to bulk set up and delete alert suppression [#223090]({{kib-pull}}223090).
* Adds a human-readable incremental ID to cases, making referencing cases easier [#222874]({{kib-pull}}222874).
* Adds the ability to change rule migration execution settings when re-processing a migration [#222542]({{kib-pull}}222542).
* Adds `runscript` response action support for Microsoft Defender for Endpoint–enrolled hosts [#222377]({{kib-pull}}222377).
* Updates automatic migration API schema [#219597]({{kib-pull}}219597).
* Adds `siemV3` role migration to support the new Security **Global Artifact Management** privilege [#219566]({{kib-pull}}219566).
* Adds automatic saving of attack discoveries, with search and filter capabilities [#218906]({{kib-pull}}218906).
* Adds the ability to edit highlighted fields in the alert details flyout [#216740]({{kib-pull}}216740).
* Adds API endpoints for the Entity Analytics privileged user monitoring feature [#215663]({{kib-pull}}215663).
* Adds the onboarding flow for the Asset Inventory feature [#212315]({{kib-pull}}212315).
* Adds the XSOAR connector [#212049]({{kib-pull}}212049).
* Adds a custom script selector for choosing scripts to execute when using the `runscript` response action [#204965]({{kib-pull}}204965).
* Updates {{elastic-sec}} Labs Knowledge Base content [#227125]({{kib-pull}}227125).
* Bumps default Gemini model [#225917]({{kib-pull}}225917).
* Groups vulnerabilities by resource and cloud account using IDs instead of names [#225492]({{kib-pull}}225492).
* Adds prompt tiles to the Security AI Assistant [#224981]({{kib-pull}}224981).
* Adds support for collapsible sections in integrations READMEs [#223916]({{kib-pull}}223916).
* Adds advanced policy settings in {{elastic-defend}} to enable collection of file origin information for File, Process, and DLL (ImageLoad) events [#223882]({{kib-pull}}223882), [#222030]({{kib-pull}}222030).
* Adds the `ecs@mappings` component to the transform destination index template [#223878]({{kib-pull}}223878).
* Adds the ability to revert a customized prebuilt rule to its original version [#223301]({{kib-pull}}223301).
* Displays which fields are customized for prebuilt rules [#225939]({{kib-pull}}225939).
* Adds an {{elastic-defend}} advanced policy setting that allows you to enable or disable the Microsoft-Windows-Security-Auditing ETW provider for security events collection [#222197]({{kib-pull}}222197).
* Updates the risk severity color map to match the new design [#222061]({{kib-pull}}222061).
* Updates the asset criticality status color map to match the new design [#222024]({{kib-pull}}222024).
* Updates the highlighted fields button styling in the alert details flyout [#221862]({{kib-pull}}221862).
* Adds support for content connectors in {{elastic-sec}} and {{observability}} [#221856]({{kib-pull}}221856).
* Expands CVE ID search to all search parameters, not just names [#221099]({{kib-pull}}221099).
* Improves alert searching and filtering by including additional ECS data stream fields [#220447]({{kib-pull}}220447).
* Updates default model IDs for Amazon Bedrock and OpenAI connectors [#220146]({{kib-pull}}220146).
* Adds support for PKI (certificate-based) authentication for the OpenAI **Other** connector providers [#219984]({{kib-pull}}219984).
* Adds pinning and settings to the **Table** tab in the alert and event details flyouts [#218686]({{kib-pull}}218686).
* Updates the data view selector in the event analyzer [#218183]({{kib-pull}}218183).
* Updates the data view selector in the global header [#216685]({{kib-pull}}216685).
* Updates UI handling for multiple CVEs and package fields [#216411]({{kib-pull}}216411).
* Adds the Security AI prompts integration [#216106]({{kib-pull}}216106).
* Adds support for grouping multi-value fields in Cloud Security [#215913]({{kib-pull}}215913).
* Limits unassigned notes to a maximum of 100 per document instead of globally [#214922]({{kib-pull}}214922).
* Updates the Detection rule monitoring dashboard to include rule gaps histogram [#214694]({{kib-pull}}214694).
* Adds support for multiple CVEs and improves vulnerability data grid, flyout, and contextual flyout UI [#213039]({{kib-pull}}213039).
* Adds support for the `MV_EXPAND` command for the {{esql}} rule type [#212675]({{kib-pull}}212675).
* Adds support for partial results for the {{esql}} rule type [#223198]({{kib-pull}}223198).
* Updates the data view selector in Timelines [#210585]({{kib-pull}}210585).
* Adds `unassigned` as an asset criticality level for bulk uploads [#208884]({{kib-pull}}208884).
* Enables `isolate` and `release` response actions from the event details flyout [#206857]({{kib-pull}}206857).
* Standardizes action triggers in alerts KPI visualizations [#206340]({{kib-pull}}206340).
* Introduces space-awareness capabilities for {{elastic-defend}} and other {{elastic-sec}}-specific {{fleet}} features.
* Adds {{elastic-defend}} process event monitoring for `ptrace` and `memfd` activity on Linux (kernel 5.10+) using eBPF.
* Adds support for DNS events on macOS. Events can be controlled from the {{elastic-defend}} policy using the **DNS events** checkbox.
* Adds TCC (Transparency Consent and Control) events to {{elastic-defend}} on macOS. Events are generated every time the TCC database is altered.
* Adds `parent.command_line` to {{elastic-defend}} process events on macOS to keep in line with Linux and Windows.
* Reduces {{elastic-defend}} CPU usage for ETW events, API events, and behavioral protections. In some cases, this may be a significant reduction.
* {{elastic-defend}}: Changes the security events source from the Event Log provider to Event Tracing for Windows (Microsoft-Windows-Security Auditing) provider and enriches the events with additional data.
* Adds {{elastic-defend}} support for Elliptic Curve certificates and TLS output settings, including `supported_protocols`, `cipher_suites`, and `curve_types`.
* Reduces {{elastic-defend}} CPU and memory usage for behavioral protections.
* Reduces {{elastic-defend}} CPU when processing events from the System process, such as IIS network events.
* Improves {{elastic-defend}} logging of fatal exceptions.
* Improves {{elastic-defend}} call site analysis logic.

### Fixes [elastic-security-9.1.0-fixes]

* Fixes a bug where data wasn't fetched by the vulnerability expandable flyout in preview mode [#227262]({{kib-pull}}227262).
* Fixes a bug where Timelines and investigations did not consistently use the default Security data view [#226314]({{kib-pull}}226314).
* Fixes a bug where opening an alert deeplink didn't correctly load filters on the **Alerts** page [#225650]({{kib-pull}}225650).
* Updates entity links to open in a flyout instead of leaving the current page [#225381]({{kib-pull}}225381).
* Adds a title to the rule gap histogram in the Detection rule monitoring dashboard [#225274]({{kib-pull}}225274).
* Fixes URL query handling for the asset inventory flyout [#225199]({{kib-pull}}225199).
* Fixes a bug where pressing Escape with an alert details flyout open from a Timeline closed the Timeline instead of the flyout [#224352]({{kib-pull}}224352).
* Fixes a bug where comma-separated `process.args` values didn't wrap properly in the alert details flyout's **Overview** tab [#223544]({{kib-pull}}223544).
* Fixes wrapping for threat indicator match event renderer [#223164]({{kib-pull}}223164).
* Fixes a z-index issue in the {{esql}} query editor within Timeline [#222841]({{kib-pull}}222841).
* Fixes incorrect content displaying after tab switching in the integrations section on the **Get started** page [#222271]({{kib-pull}}222271).
* Fixes the exception flyout to show the correct "Edit rule exception" title and button label when editing an exception item [#222248]({{kib-pull}}222248).
* Retrieves active integrations from the installed integrations API [#218988]({{kib-pull}}218988).
* Updates tooltips in the gap fills table [#218926]({{kib-pull}}218926).
* Fixes AI Assistant prompt updates so UI changes reflect only successful updates [#217058]({{kib-pull}}217058).
* Fixes error callout placement on the **Engine Status** tab of the **Entity Store** page [#216228]({{kib-pull}}216228).
* Fixes alert severity ordering to display from highest severity to lowest [#215813]({{kib-pull}}215813).
* Generalizes and consolidates custom {{fleet}} onboarding logic [#215561]({{kib-pull}}215561).
* Fixes an alert grouping re-render issue that caused infinite rendering loops when selecting a group [#215086]({{kib-pull}}215086).
* Fixes a bug in the alert details flyout's **Table** tab where fields displayed duplicate hover actions [#212316]({{kib-pull}}212316).
* Refactors conversation pagination for the Security AI Assistant [#211831]({{kib-pull}}211831).
* Fixes a bug in {{elastic-defend}} where the `fqdn` feature flag wasn't being persisted across system or endpoint restarts.
* Fixes a crash in the {{elastic-defend}} scan response action and suppresses the end-user popup when running background malware scans.
* Fixes an unbounded kernel non-paged memory growth issue in the {{elastic-defend}} kernel driver during extremely high event load situations on Windows. Systems affected by this issue would slow down or become unresponsive until the triggering event load (such as network activity) subsided [#88](https://github.com/elastic/endpoint/issues/88).
* Fixes a memory growth bug in {{elastic-defend}} on Linux when both **Collect session data** and **Capture terminal output** are enabled.
* Fixes a bug in {{elastic-defend}} where Linux network events would have source and destination byte counts swapped.
* Fixes an issue where {{elastic-defend}} may incorrectly set the artifact channel in policy responses, and adds `manifest_type` to policy responses.

## 9.0.8 [elastic-security-9.0.8-release-notes]

### Features and enhancements [elastic-security-9.0.8-features-enhancements]
* Adds an {{elastic-defend}} option to remediate orphaned state by attempting to start Elastic Agent service.

### Fixes [elastic-security-9.0.8-fixes]
* Removes `null` in confirmation dialog when bulk editing index patterns for rules [#236572]({{kib-pull}}236572).
* Fixes the URL passed to detection rule actions via the `{{context.results_link}}` placeholder [#236067]({{kib-pull}}236067).
* Adds support in {{elastic-defend}} for installing eBPF probes on Linux endpoints when taskstats is compiled out of the kernel.
* Fixes an issue in {{elastic-defend}} where Linux network events could have source and destination bytes swapped.
* Removes `.process.thread.capabilities.permitted` and `.process.thread.capabilities.effective` from Linux network events in {{elastic-defend}}.
* Fixes an issue in {{elastic-defend}} where host isolation could auto-release incorrectly. Host isolation now only releases when {{elastic-endpoint}} becomes orphaned. Intermittent {{elastic-agent}} connectivity changes no longer alter the host isolation state.
* Improves the reliability of local {{elastic-defend}} administrative shell commands. In rare cases, a command could fail to execute due to issue with interprocess communication.
* Fixes an issue where {{elastic-defend}} would incorrectly calculate throughput capacity when sending documents to output.  This may have limited event throughput on extremely busy endpoints.
* Fixes an issue in {{elastic-defend}} installation logging where only the first character of install paths (usually 'C') would be logged.

## 9.0.7 [elastic-security-9.0.7-release-notes]

### Fixes [elastic-security-9.0.7-fixes]
* Prevents users without appropriate privileges from deleting notes [#233948]({{kib-pull}}233948).
* Fixes a bug that prevented the **MITRE ATT&CK** section from appearing in the alert details flyout [#233805]({{kib-pull}}233805).
* Updates {{kib}} MITRE ATT&CK data to v17.1 [#231375]({{kib-pull}}231375).
* Fixes a bug where Linux capabilities were included in {{elastic-endpoint}} network events despite being disabled.
* Makes the delivery of {{elastic-endpoint}} command line commands more robust. In rare cases, commands could previously fail due to interprocess communication issues.

## 9.0.6 [elastic-security-9.0.6-release-notes]

### Features and enhancements [elastic-security-9.0.6-features-enhancements]
* Improves the reliability of {{elastic-defend}}'s connection to its kernel driver. This should reduce the instances of temporary `DEGRADED` policy statuses at boot due to `connect_kernel` failures.
* Improves {{elastic-defend}} malware scan queue efficiency by not blocking scan requests when an oplock for the file being scanned cannot be acquired.
* To help identify which parts of `elastic-endpoint.exe` are using a significant amount of CPU, {{elastic-defend}} on Windows can now include CPU profiling data in diagnostics. To request CPU profiling data using the command line, refer to [{{agent}} command reference](/reference/fleet/agent-command-reference.md#_options). To request CPU profiling data using {{kib}}, check the **Collect additional CPU metrics** box when requesting {{agent}} diagnostics.
* Enriches {{elastic-defend}} macOS network connect events with `network.direction`. Possible values are `ingress` and `egress`.

### Fixes [elastic-security-9.0.6-fixes]
* Prevents the {{esql}} form from locking in read-only mode in the rule upgrade flyout [#231699]({{kib-pull}}231699).
* Fixes a bug in {{elastic-defend}} where the `fqdn` feature flag was not being persisted across system/endpoint restarts.
* Fix a race condition in {{elastic-defend}} that occasionally resulted in corrupted process command lines on Windows. This could cause incorrect values for `process.command_line`, `process.args_count` and `process.args`, leading to false positives.
* Fixes a bug in {{elastic-defend}} where Linux endpoints would report `process.executable` as a relative, instead of absolute, path.

## 9.0.5 [elastic-security-9.0.5-release-notes]

### Features and enhancements [elastic-security-9.0.5-features-enhancements]
* Adds the `detection_rule_upgrade_status` object to snapshot telemetry schema [#223086]({{kib-pull}}223086).
* Reduces {{elastic-defend}} CPU when processing events from the System process on Windows.
* Allows {{elastic-defend}} to automatically recover in some situations when it loses connectivity with {{agent}}.
* Shortens the time it takes {{elastic-defend}} to recover from a `DEGRADED` status caused by communication issues with {{agent}}.
* Due to an issue in macOS, {{elastic-defend}} would sometimes send network events without `user.name` populated. {{elastic-defend}} will now identify these events and populate `user.name` if necessary.
* Reduces {{elastic-defend}} CPU usage for ETW events, API events, and Behavioral Protections. In some cases, this may be a significant reduction.


### Fixes [elastic-security-9.0.5-fixes]
* Fixes a bug where Security AI Assistant settings landed on the wrong page for users on the Basic license  [#229163]({{kib-pull}}229163).
* Fixes an issue in {{elastic-defend}} performance metrics that resulted in `endpoint_uptime_percent` always being 0 for behavioral rules.
* Fixes an issue in {{elastic-defend}} that could result in a crash if a {{ls}} output configuration is specified containing a certificate that cannot not be parsed.

## 9.0.4 [elastic-security-9.0.4-release-notes]

### Features and enhancements [elastic-security-9.0.4-features-enhancements]
* Adds the `elastic_customized_total`, `elastic_noncustomized_total`, and `is_customized` fields to snapshot telemetry schema [#222370]({{kib-pull}}222370).
* Improves logging of fatal exceptions in {{elastic-defend}}.

### Fixes [elastic-security-9.0.4-fixes]
* Fixes differences between risk scoring preview and persisted risk scores [#226456]({{kib-pull}}226456).
* Updates a placeholder and validation message in the **Related Integrations** section of the rule upgrade flyout [#225775]({{kib-pull}}225775).
* Excludes {{ml}} rules from installation and upgrade checks for users with Basic or Essentials licenses [#224676]({{kib-pull}}224676).
* Allows using days as a time unit in rule schedules, fixing an issue where durations normalized to days were incorrectly displayed as 0 seconds [#224083]({{kib-pull}}224083).
* Fixes a bug where unmodified prebuilt rules installed before v8.18 didn't appear in the **Upgrade** table when the **Unmodified** filter was selected [#227859]({{kib-pull}}227859).
* Improves UI copy for the "bulk update with conflicts" modal [#227803]({{kib-pull}}227803).
* Strips `originId` from connectors before rule import to ensure correct ID regeneration and prevent errors when migrating connector references on rules [#223454]({{kib-pull}}223454).
* Fixes an issue that prevented the AI Assistant Knowledge Base settings UI from displaying [#225033]({{kib-pull}}225033).
* Fixes a bug in {{elastic-defend}} where Linux network events would fail to load if IPv6 is not supported by the system.
* Fixes an issue in {{elastic-defend}} that may result in bugchecks (BSODs) on Windows systems with a very high volume of network connections.
* Fixes an issue where {{elastic-defend}} may incorrectly set the artifact channel in policy responses, and adds `manifest_type` to policy responses.

## 9.0.3 [elastic-security-9.0.3-release-notes]

### Features and enhancements [elastic-security-9.0.3-features-enhancements]
* Adds `dns` event collection for macOS for {{elastic-defend}} [#223566]({{kib-pull}}223566).
* Adds pricing information about Elastic Managed LLM in AI Assistant and Attack Discovery tours and callouts [#221566]({{kib-pull}}221566).
* Adds support for DNS events on macOS. Events can be controlled from the policy using the **DNS events** checkbox.

### Fixes [elastic-security-9.0.3-fixes]
* Fixes a bug where OSS models didn’t work when streaming was ON [#224129]({{kib-pull}}224129).
* Fixes a bug where cell actions didn’t work when opening a Timeline from specific rules [#223306]({{kib-pull}}223306).
* Fixes an issue where the entity risk score feature stopped persisting risk score documents [#221937]({{kib-pull}}221937).
* Fixes a bug where the **Rules**, **Alerts**, and **Fleet** pages would stall in air-gapped environments by ensuring API requests are sent even when offline [#220510]({{kib-pull}}220510).
* Ensures the Amazon Bedrock connector respects the action proxy configuration [#224130]({{kib-pull}}224130).
* Ensures the OpenAI connector respects the action proxy configuration for all sub-actions [#219617]({{kib-pull}}219617).

## 9.0.2 [elastic-security-9.0.2-release-notes]

### Features and enhancements [elastic-security-9.0.2-features-enhancements]
There are no new features or enhancements.

### Fixes [elastic-security-9.0.2-fixes]
* Fixes a bug that caused an error message to appear when you changed entity asset criticality from the entity flyout [#219858]({{kib-pull}}219858)
* Removes the technical preview badge from the alert suppression fields for event correlation rules
* Fixes a bug in {{elastic-defend}} 8.16.0 where {{elastic-endpoint}} would incorrectly report some files as being `.NET`

## 9.0.1 [elastic-security-9.0.1-release-notes]

### Features and enhancements [elastic-security-9.0.1-features-enhancements]
There are no new features or enhancements.

### Fixes [elastic-security-9.0.1-fixes]
* Fixes a bug that caused installed prebuilt detection rules to upgrade to their latest available versions when you installed a new {{elastic-defend}} integration or {{agent}} policy [#217959]({{kib-pull}}217959)
* Prevents {{esql}} rules from timing out if the rule query takes longer than five minutes to complete [#216667]({{kib-pull}}216667)
* Fixes a bug that prevented you form scrolling in modals [#218697]({{kib-pull}}218697)

## 9.0.0 [elastic-security-900-release-notes]

::::{NOTE}
All features introduced in 8.18.0 are also available in 9.0.0.
::::

### Features and enhancements [elastic-security-900-features-enhancements]
* Enables Automatic Import to accept CEL log samples [#206491]({{kib-pull}}206491)
* Enhances Automatic Import by including setup and troubleshooting documentation for each input type that's selected in the readme [#206477]({{kib-pull}}206477)
* Adds the ability to continue to the Entity Analytics dashboard when there is no data [#201363]({{kib-pull}}201363)
* Modifies the privilege-checking behavior during rule execution. Now, only read privileges of extant indices are checked during rule execution [#177658]({{kib-pull}}177658)


### Fixes [elastic-security-900-fixes]
* Fixes a bug that caused the Entity Analytics Dashboard refresh button to break risk score tables [#215472]({{kib-pull}}215472)
* Fixes AI Assistant `apiConfig` set by Security getting started page [#213971]({{kib-pull}}213971)
* Limits the length of `transformID` to 36 characters [#213405]({{kib-pull}}213405)
* Ensures that table actions use standard colors [#207743]({{kib-pull}}207743)
* Fixes a bug with the **Save and continue** button on a {{fleet}} form [#211563]({{kib-pull}}211563)

