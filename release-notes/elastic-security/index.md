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

## 9.5.0 [elastic-security-9.5.0-release-notes]

### Features and enhancements [elastic-security-9.5.0-features-enhancements]

* Adds Discover, Agents, and Workflows links to the {{elastic-sec}} classic view [#269683]({{kib-pull}}269683).
* Moves the {{agent-builder}} navigation link to the top of the {{elastic-sec}} navigation [#271532]({{kib-pull}}271532).
* Makes detection rule changes history generally available. A **History** entry in the rule actions menu opens a dedicated changes-history page with an infinite-scroll timeline of recorded rule changes and a JSON diff between revisions [#278052]({{kib-pull}}278052), [#269617]({{kib-pull}}269617), [#270091]({{kib-pull}}270091).
* Adds the ability to restore a detection rule to a previous state captured in its changes history [#274605]({{kib-pull}}274605).
* Improves prebuilt rule installation performance, making installation of all prebuilt rules approximately 5x faster [#275523]({{kib-pull}}275523).
* Updates MITRE ATT&CK mappings to `v19.1` [#278547]({{kib-pull}}278547).
* Surfaces rules with unsupported MITRE ATT&CK mappings on the coverage overview and rule edit pages after a mappings version update, so you can review and update them [#274793]({{kib-pull}}274793).
* Migrates the prebuilt `packetbeat_dns_tunneling_ea` and `packetbeat_rare_dns_question_ea` {{ml}} jobs to the `security_network` module [#268267]({{kib-pull}}268267).
* Adds `security.enableRule` and `security.disableRule` workflow steps for bulk enabling or disabling detection rules by rule IDs or query [#275187]({{kib-pull}}275187).
* Enables the **Close all alerts that match this exception** checkbox when creating an exception from a runtime field defined on the rule's source index [#270219]({{kib-pull}}270219).
* Adds a warning callout and confirmation modal to the rule exceptions form when entering escaped characters (such as `\*` or `\?`) with the `matches` operator, indicating they might have intended wildcards instead [#268397]({{kib-pull}}268397).
* Enables the advanced setting that turns on the new flyout system in {{elastic-sec}} [#279300]({{kib-pull}}279300).
* Enables search in the **JSON** tab of the Security Solution alert flyout, matching the behavior of the Discover document flyout [#263875]({{kib-pull}}263875).
* Adds an action in the correlations section of the alert details flyout to open a related attack as a preview (legacy expandable flyout) or as a child panel (new flyout system) [#279306]({{kib-pull}}279306).
* Adds an **Add to chat** bulk action to the alerts table, letting analysts send up to 100 selected alerts to the {{agent-builder}} chat for triage [#270904]({{kib-pull}}270904).
* Adds an **Export to CSV** button to the alerts table that exports the currently filtered alerts and links to the reporting page (requires the reporting capability) [#263895]({{kib-pull}}263895).
* Adds an alert analysis managed workflow that gathers context around an alert, sends it to an LLM, and writes the result to alert notes and tags, optionally auto-closing high-confidence false positives. Includes a configuration UI in the rules section and requires an Enterprise license [#269743]({{kib-pull}}269743), [#276788]({{kib-pull}}276788).
* Updates the alert **Run workflow** panel to include managed workflows, such as the alert analysis workflow [#276555]({{kib-pull}}276555).
* Shortens the tags written by the alert analysis workflow and adds a configurable `securitySolution:alertAnalysisWorkflowTagPrefix` setting (default `alert-analysis`) [#276547]({{kib-pull}}276547).
* Adds bulk enable, disable, and delete actions for Attack Discovery schedules, backed by new public bulk schedule APIs [#267549]({{kib-pull}}267549).
* Integrates Attack Discovery 2.0 workflow-based generation with alerting-framework scheduling and registers {{agent-builder}} skills for editing and troubleshooting workflows [#260816]({{kib-pull}}260816), [#260811]({{kib-pull}}260811).
* Improves the AI Value Report empty state: first-time users with no attack discoveries see a laid-out sample report preview, while returning users with no data in the selected range see a prompt to adjust the time range [#265091]({{kib-pull}}265091).
* Improves the copy for the Microsoft Sentinel rules upload step in Automatic Migration [#276242]({{kib-pull}}276242).
* Improves Automatic Migration dashboard migration accuracy by sampling index records before query translation, enabling the LLM to generate {{esql}} queries with correct field names and values from the first attempt [#261927]({{kib-pull}}261927).
* Improves Automatic Migration lookup translation by giving lookup resources (such as Microsoft Sentinel watchlists) field metadata, so generated {{esql}} can produce more accurate `LOOKUP JOIN` clauses [#275845]({{kib-pull}}275845).
* Adds Microsoft Sentinel watchlist upload support to SIEM rule migrations, validating and ingesting watchlist ARM exports as lookup resources [#269726]({{kib-pull}}269726).
* Changes the default chat experience in {{elastic-sec}} and Elastic {{observability}} contexts to AI Agent. A one-time announcement explains the change and allows you to return to the classic AI Assistant from **GenAI Settings**. The dismissal state is remembered per space [#260570]({{kib-pull}}260570).
* Redesigns the {{agent-builder}} announcement modal into three layouts based on whether the user has prior AI Assistant history and whether they can revert the space-level chat experience [#264995]({{kib-pull}}264995).
* Updates the {{agent-builder}} announcement modal so that clicking **Revert** immediately switches all space users back to AI Assistant [#267906]({{kib-pull}}267906).
* Removes the **Switch to AI Agent** confirmation modal; switching to AI Agent now takes effect immediately [#264839]({{kib-pull}}264839).
* Adds request and response examples and standardized descriptions to the {{elastic-sec}} AI Assistant and Elastic Assistant OpenAPI specifications, and fixes several schema inaccuracies (no runtime API behavior change) [#263322]({{kib-pull}}263322).
* Adds a `recommend-prebuilt-rules` {{agent-builder}} skill that recommends which Elastic prebuilt detection rules to install and answers questions about the installable rule catalog [#269559]({{kib-pull}}269559).
* Adds a `find-security-rules` {{agent-builder}} skill for discovering, filtering, sorting, and counting detection rules using natural-language queries [#269089]({{kib-pull}}269089).
* Adds an `alert-triage` {{agent-builder}} skill that ranks the open alert queue by combining base risk, MITRE tactic, entity risk, and asset criticality to highlight what to focus on [#273439]({{kib-pull}}273439).
* Adds a `pci-compliance` {{agent-builder}} skill with tools for PCI DSS v4.0.1 scope discovery, compliance checks, reporting, and field mapping [#256060]({{kib-pull}}256060).
* Adds support for attaching Timelines to cases, including a timelines table for selecting a Timeline to attach (behind the `xpack.cases.attachments.enabled` feature flag) [#272768]({{kib-pull}}272768), [#271353]({{kib-pull}}271353).
* Persists the entity AI summary to the entity metadata index so it is no longer regenerated each time the entity details flyout is opened. A callout prompts regeneration when the entity's risk score drifts from the snapshot [#276038]({{kib-pull}}276038).
* Adds an Anomalies section to the entity details flyout and details tab for host and user entities, showing a 30-day anomaly overview by MITRE ATT&CK tactic and detailed, filterable anomaly records, with actions including **Add to Timeline**, **View in Discover**, and opening the **Single Metric Viewer** in {{ml}} [#273139]({{kib-pull}}273139), [#275118]({{kib-pull}}275118).
* Adds an `entityStore.updateAssetCriticality` workflow step that updates an entity's asset criticality and triggers a risk score recalculation [#276092]({{kib-pull}}276092).
* Adds `entityStore.entityAssetCriticalityUpdated` and `entityStore.entityRiskScoreChanged` workflow triggers that fire when an entity's asset criticality is set or cleared, or when its risk score changes [#275670]({{kib-pull}}275670).
* Updates Entity Store APIs to reject unknown keys in request bodies, query parameters, and path parameters with a `400 Bad Request` instead of silently ignoring them [#273098]({{kib-pull}}273098).
* Adds recurrence-based scheduling to Osquery packs. Pack authors can run a pack on a **Daily** or **Custom** schedule, with an optional start date, stop-after date, and splay, and can override the schedule per query [#275896]({{kib-pull}}275896), [#271865]({{kib-pull}}271865), [#270639]({{kib-pull}}270639), [#269730]({{kib-pull}}269730).
* Adds the ability to export Osquery query results as CSV, JSON, or NDJSON files directly from the query results page [#275597]({{kib-pull}}275597), [#267800]({{kib-pull}}267800), [#266582]({{kib-pull}}266582), [#265995]({{kib-pull}}265995).
* Adds an {{elastic-defend}} advanced policy setting for Windows that lets you disable enrichment of DLL Search Order Hijacking detection events [#272068]({{kib-pull}}272068).
* Adds a new `canceled` response action status, shown in the response action history and console, with support across response action types including Microsoft Defender for Endpoint [#271357]({{kib-pull}}271357).
* Raises the default file size limit for the `upload` response action to 500 MB and effectively removes the maximum, configurable via `xpack.securitySolution.maxUploadResponseActionFileBytes` [#275850]({{kib-pull}}275850).
* Adds a warning callout to the **Endpoint exceptions**, **Trusted applications**, and **Event filters** forms when users enter unnecessarily escaped characters [#268477]({{kib-pull}}268477).
* Adds an **AND** button to the trusted devices form, allowing multiple conditions per trusted device entry, with a duplicate-field warning [#268011]({{kib-pull}}268011).
* Enables the automatic troubleshooting skill for {{agent-builder}}, so endpoint troubleshooting uses the skill instead of the {{elastic-sec}} AI Assistant-backed Defend Insights APIs [#273865]({{kib-pull}}273865).
* Adds more data to kernel module load events for {{elastic-defend}} on Linux.
* Adds support for the `cancel` response action in {{elastic-defend}}.
* Adds hardware breakpoint detection to shellcode thread alerts in {{elastic-defend}}. Hardware breakpoints on the creator thread are detected via kernel-mode inspection, improving the reliability of `process.thread.Ext.hardware_breakpoint_set` reporting.
* Adds AI-agent process attribution with process descendant enrichment to {{elastic-defend}}.
* Adds support for running PowerShell scripts via the `runscript` response action in {{elastic-defend}} on Windows.
* Adds experimental macOS 27 support to {{elastic-defend}}.
* Adds collection of additional Windows security events in {{elastic-defend}}: Service Installation (`4697`), Scheduled Task Creation (`4698`), Scheduled Task Updated (`4702`), User Account Created (`4720`), and Vault Credentials Were Read (`5382`).
* Adds detection of DLL masquerading via potential search order hijacking in {{elastic-defend}} on Windows. `dll.Ext.defense_evasions` is now populated with `DLL Hijack: Masquerading` when a DLL that shares a name with a known Windows system DLL (such as one from System32 or SysWOW64) is loaded from an unexpected directory.
* Adds persistence of original Windows security audit policies in {{elastic-defend}}, so they can be restored after an unclean shutdown.
* Adds the LXC container name to event telemetry for {{elastic-defend}} on Linux.


### Fixes [elastic-security-9.5.0-fixes]

* Fixes the **Security** category link in the global classic side navigation, which pointed to the Value Report instead of the **Get started** page [#272155]({{kib-pull}}272155).
* Fixes an incorrect ordering of the **Launchpad** item in the classic global side navigation. The item now appears above **Manage**, consistent with {{elastic-sec}} own classic view [#268216]({{kib-pull}}268216).
* Fixes a crash when opening the rule panel flyout for a deleted rule caused by missing `severity_mapping` or `risk_score_mapping` fields [#278545]({{kib-pull}}278545).
* Fixes the integration assets accordion to display the security rule name, since security rules have no title field [#272089]({{kib-pull}}272089).
* Fixes an issue where detection engine gap errors were classified as non-user errors, which caused gap-only rule failures to count against SLO dashboards [#263244]({{kib-pull}}263244).
* Fixes a validation error when resolving a `required_fields` conflict during a prebuilt rule upgrade [#278125]({{kib-pull}}278125).
* Preserves the prebuilt rule `revision` (incremented by 1) when upgrading a rule to a different type, matching the behavior of same-type upgrades [#275627]({{kib-pull}}275627).
* Fixes an issue where {{kib}} assets from an installed integration package (such as dashboards used by prebuilt detection rules) could remain stale across a {{kib}} upgrade because {{fleet}} never overwrote existing assets on reinstall [#277953]({{kib-pull}}277953).
* Fixes an issue where deprecated prebuilt rules could reappear as installable after being deleted [#274447]({{kib-pull}}274447).
* Fixes an issue where the **Delete all** action for deprecated prebuilt rules failed when more than 100 deprecated rules existed [#271550]({{kib-pull}}271550).
* Fixes an issue in EQL rule creation where the query field did not re-validate after changing the index pattern, leaving stale errors on screen even when the query was valid for the newly selected {{data-source}} [#261027]({{kib-pull}}261027).
* Fixes orphaned {{esql}} requests left running when navigating away from the {{esql}} rule edit page [#267455]({{kib-pull}}267455).
* Fixes the AI rule creation flow to respect the `enableESQL` advanced setting. When {{esql}} is disabled, the AI rule creation option is hidden and {{esql}} rule creation is blocked in {{agent-builder}} [#267247]({{kib-pull}}267247).
* Fixes an issue where the Agent Builder sidebar did not open when navigating directly to rule creation [#262588]({{kib-pull}}262588).
* Fixes an issue where the rule editing UI rejected valid semver range version constraints (such as `^8.2.0 || ^9.0.0`) on related integrations [#274133]({{kib-pull}}274133).
* Fixes an issue where the `concurrent_searches` and `items_per_search` API fields for `threat_match` (Indicator Match) rules were reset to their defaults when the rule was saved through the UI [#276823]({{kib-pull}}276823).
* Fixes an issue with Indicator Filters in the read-only rule details UI, where incorrect backing indices caused misleading warnings to display on hover [#263657]({{kib-pull}}263657).
* Fixes an issue where pressing Escape while a Timeline modal was open on top of the alert details flyout closed both, dropping the analyst out of the investigation context [#279153]({{kib-pull}}279153).
* Fixes missing cell actions in the new attack flyout in Discover and {{elastic-sec}} [#277833]({{kib-pull}}277833).
* Fixes an error when opening a source event from the **Highlighted fields** section of the alert details flyout when the source index had been restored, and renamed, from a cold or frozen tier [#277703]({{kib-pull}}277703).
* Fixes two display bugs in the new flyout system: a host silently dropped from the **Entities** panel, and incorrect chevron display [#277083]({{kib-pull}}277083).
* Fixes an issue where the alert details flyout **Overview** tab crashed in Discover for external alert documents [#269000]({{kib-pull}}269000).
* Fixes a double border in the EASE alert summary flyout header [#268996]({{kib-pull}}268996).
* Fixes an incorrect banner shown in the Discover document flyout when Discover is embedded in a dashboard [#268249]({{kib-pull}}268249).
* Fixes an issue where the alert details flyout failed to render its header, content, and footer when Discover was embedded in a dashboard [#267321]({{kib-pull}}267321).
* Fixes alert action error toasts (assign, tag, open, close, acknowledge) so they show the full error message from {{es}} instead of a blank body [#269592]({{kib-pull}}269592).
* Fixes an issue where only the first assignee was displayed in the alert details flyout instead of all assigned users [#273801]({{kib-pull}}273801).
* Fixes a scroll-position jump in the alert details flyout **Table** tab [#273521]({{kib-pull}}273521).
* Adds the **Add to chat** action to the alerts table row actions [#273740]({{kib-pull}}273740).
* Fixes the alerts table CSV export so reports record the actual {{kib}} version instead of `7.14.0` [#272418]({{kib-pull}}272418).
* Fixes an unwanted **Read more** button on long rule descriptions in the alert details flyout [#264876]({{kib-pull}}264876).
* Fixes an issue where auto-refresh on the **Alerts** page with grouping applied caused open flyouts and dialogs to close unexpectedly [#264518]({{kib-pull}}264518).
* Fixes a Firefox scroll position jump that occurred when hovering field rows with cell actions in the **Table** tab of the alert details flyout [#262682]({{kib-pull}}262682).
* Fixes an issue where alert KPI counts were rendered with incorrect whitespace [#260803]({{kib-pull}}260803).
* Fixes a crash in index fields formatting when a field or index is named after an `Object.prototype` property such as `constructor`, `toString`, or `__proto__` [#277851]({{kib-pull}}277851).
* Fixes **Investigate in Timeline** for suppressed alerts whose exception list data was stored as a single object instead of an array [#275417]({{kib-pull}}275417).
* Fixes **Investigate in Timeline** for Indicator Match alerts by quoting and escaping KQL values that contain reserved characters, such as `:` in URLs [#271639]({{kib-pull}}271639).
* Fixes incorrect button alignment in Timeline [#268314]({{kib-pull}}268314).
* Adds examples and descriptions to the Timeline and pinned events OpenAPI specifications and fixes several spec inaccuracies [#264388]({{kib-pull}}264388).
* Fixes the analyzer alert-hits query so it honors the `securitySolution:excludeColdAndFrozenTiersInAnalyzer` setting, which previously excluded cold and frozen tiers only from other analyzer queries [#278972]({{kib-pull}}278972).
* Adds a date range picker above the **Alerts related by ancestry** table in the correlations section and bounds the underlying query to it, preventing timeouts on very large indices [#278971]({{kib-pull}}278971).
* Fixes the **Alert processing analytics** donut on the Value Report, which failed to load when many alerts were linked to attack discoveries in the report window [#277220]({{kib-pull}}277220).
* Fixes an issue where the Attack Discovery privilege check required access to internal backing indices instead of the user-facing alert aliases, causing roles with alias-only access to fail with missing-index-privilege errors [#272122]({{kib-pull}}272122).
* Fixes the **Manage license** link on the Attack Discovery page to navigate directly to **License Management** instead of the {{stack-manage-app}} landing page [#266445]({{kib-pull}}266445).
* Fixes an issue where **Add to case** actions were visible under the Attack Discovery tab when the user's Cases privilege was set to None; they are now hidden [#266127]({{kib-pull}}266127).
* Fixes an issue where integration icons in the Attack Discovery schedule form blinked while typing in input fields [#266117]({{kib-pull}}266117).
* Fixes an issue where the Attack Discovery bulk action allowed changing selected items to a status they already had [#266115]({{kib-pull}}266115).
* Fixes an issue where **View in AI Assistant** buttons and context menu items in Attack Discovery remained visible when the AI Assistant was hidden via **GenAI Settings** [#266111]({{kib-pull}}266111).
* Fixes truncated **Run** button text in the Attack Discovery page header [#266105]({{kib-pull}}266105).
* Adds a manual input dialog for workflow runs that require input, showing event and manual inputs in separate tabs [#271586]({{kib-pull}}271586).
* Fixes a layout issue in the translated rule flyout where editing the {{esql}} translation could shrink the original rule definition column [#276459]({{kib-pull}}276459).
* Fixes an issue where the Automatic Migration integrations index could bind to a non-ELSER inference endpoint, causing translated rules to show no recommended integrations [#275766]({{kib-pull}}275766).
* Fixes a sticky redirect where users routed to Automatic Migration during onboarding could no longer open **Launchpad → Get started** afterward [#273753]({{kib-pull}}273753).
* Fixes an issue where migrated Splunk dashboard panels failed to render in Lens with a "wrong data type" error because column types were incorrectly inferred as `unknown` [#270563]({{kib-pull}}270563).
* Fixes an issue where uploading a migration file containing invalid rules or dashboards could leave behind an orphaned migration record [#266359]({{kib-pull}}266359).
* Fixes migrated Splunk dashboards showing blank visualizations on initial load by removing hardcoded time fields and {{data-source}} titles from migration templates [#264102]({{kib-pull}}264102).
* Fixes an issue in the AI Assistant where selecting all conversations and then saving an edit to a single conversation deleted all conversations instead of updating only the edited one [#274033]({{kib-pull}}274033).
* Fixes an issue where attachments from one AI Assistant conversation leaked into the next [#273017]({{kib-pull}}273017).
* Fixes an issue where the {{agent-builder}} announcement modal could reappear during page navigation after being dismissed, particularly in high-latency or proxy environments [#272276]({{kib-pull}}272276).
* Fixes a duplicate "AI Assistant" section on the **Feature Settings** page by consolidating the {{elastic-sec}} AI Assistant configuration under the **Security** group, and hides the AI Assistant for Security entry when AI Assistant is not the selected chat experience [#266697]({{kib-pull}}266697).
* Removes Beta labels and badges from the AI Agent chat experience, including the chat selection card, announcement modal, advanced settings value, and Elastic {{observability}} opt-in tour [#264200]({{kib-pull}}264200).
* Suppresses the AI Agent announcement modal in automated browser sessions by checking `navigator.webdriver`, so synthetic monitors and end-to-end tests are not affected [#263785]({{kib-pull}}263785).
* Updates the copy in the AI Agent announcement modal [#263034]({{kib-pull}}263034).
* Fixes the **Threat Intelligence** page height in classic navigation, where the page did not fill the available window space [#276150]({{kib-pull}}276150).
* Fixes an issue where the **Data Quality** dashboard showed no data when {{kib}} was set to Japanese [#265782]({{kib-pull}}265782).
* Fixes the events histogram and host/network event count panels on the **Overview** dashboard, which incorrectly included alert documents in event counts, and ensures compatibility with {{ccs}} so events from remote clusters are correctly included [#265561]({{kib-pull}}265561).
* Fixes an issue where the last event ingested metric pulled from an incorrect scope and too few indices [#262346]({{kib-pull}}262346).
* Fixes entity store routing so it respects the feature flag's registered default instead of always behaving as if the flag were off [#269642]({{kib-pull}}269642).
* Fixes an issue where uninstalling the entity store could delete entity store indices and data streams while other engines were still running; they are now kept while any engine is present [#276697]({{kib-pull}}276697).
* Fixes an issue where the entity store log extraction window could grow unboundedly in lagging environments, causing {{esql}} probe cost to spiral. Adds a `maxTimeWindowSize` parameter (default: `15m`) to the install and update APIs to cap each probe's window size. Also adds an `excludedIndexPatterns` parameter that lets you exclude specific index patterns from log extraction [#268170]({{kib-pull}}268170).
* Fixes an entity store log extraction failure caused by field mapping ambiguity during single-field identity evaluation [#272344]({{kib-pull}}272344).
* Fixes an issue where detection rules failed with errors when their executing users lacked read access to entity store indices. Entity store enrichment is now silently skipped for users without entity store index access [#267787]({{kib-pull}}267787).
* Scopes watchlist index sync to the watchlist creator's credentials, requiring read access to the configured index. Watchlists created before this change show a **Sync paused** callout with a **Re-authorize** action [#270292]({{kib-pull}}270292).
* Fixes an issue where the prebuilt Privileged Users watchlist was only installed in the default space; it is now installed in custom spaces as well [#277645]({{kib-pull}}277645).
* Fixes an issue where entity maintainer tasks (risk score, watchlist, and relationship maintainers) kept running after the entity store was toggled off; they now stop when all engines stop and restart when engines are started again [#273890]({{kib-pull}}273890).
* Fixes the entities table on the **Entity Analytics** page to sort by risk score by default, showing the highest-risk entities first and placing entities without a risk score at the bottom [#272234]({{kib-pull}}272234).
* Fixes an issue on the **Entity Analytics** page where the search bar appeared blank after navigating to Discover and back, and where **Refresh** could reuse a stale query [#265926]({{kib-pull}}265926).
* Fixes an issue where the **Entity Analytics** left panel showed stale details when previewing a different entity [#265512]({{kib-pull}}265512).
* Fixes multiple rendering issues in the entity details flyout when opened in **Preview** mode from {{agent-builder}} [#267342]({{kib-pull}}267342).
* Fixes an issue where users with read-only access could see the asset criticality update dropdown in the entity details flyout. The dropdown is now correctly gated on write permissions [#269164]({{kib-pull}}269164).
* Fixes an issue where the **Top Threat Hunting Leads** section was silently hidden for users without read access to the leads index; a privileges callout now explains the missing access [#271207]({{kib-pull}}271207).
* Fixes unreachable last pages in grouped tables with more than 10,000 groups by capping pagination at the 10,000-group limit and revealing pages progressively with a **Load more** control [#277322]({{kib-pull}}277322).
* Restores the asset inventory telemetry usage collector, which had stopped reporting `asset_inventory` stats [#271944]({{kib-pull}}271944).
* Fixes an error that prevented adding the Osquery Manager integration in custom {{kib}} spaces when a global Osquery pack existed in the Default space [#278498]({{kib-pull}}278498).
* Fixes intermittent duplicate execution of scheduled Osquery packs by deduplicating concurrent {{fleet}} package-policy writes for package policies shared across multiple agent policies [#278159]({{kib-pull}}278159).
* Fixes Osquery agent selection, policy grouping, and live query dispatch for agents whose `policy_id` carries a version suffix (such as `<id>#9.5`) [#277283]({{kib-pull}}277283).
* Fixes empty **Last results**, **Docs**, and **Agents** columns on the Osquery pack details page for scheduled queries [#267894]({{kib-pull}}267894).
* Extends the query execution timeout to 24 hours [#262008]({{kib-pull}}262008).
* Fixes Endpoint metadata queries and response actions for agents whose `policy_id` carries a version suffix, so they appear in the **Endpoint list** and their response actions succeed [#277100]({{kib-pull}}277100).
* Fixes {{elastic-defend}} package policy inputs to use the package policy ID even when input IDs are supplied, which {{elastic-defend}} relies on [#271269]({{kib-pull}}271269).
* Fixes the `run_script` response action path in the OpenAPI specification (was `/api/endpoint/action/runscript`, now `/api/endpoint/action/run_script`) [#271759]({{kib-pull}}271759).
* Fixes the response console input so a space is automatically inserted after a custom argument value selector, letting you keep typing without affecting the previous argument [#262628]({{kib-pull}}262628).
* Fixes CrowdStrike `runscript` response actions to correctly display script output (stdout/stderr) in the **Response Console** and **Action History** views [#262470]({{kib-pull}}262470).
* Fixes an issue where {{elastic-defend}} could lose Tamper Protection state on startup, by rehydrating the cache from disk when a policy is applied.
* Fixes {{elastic-defend}} recovery from network event subscription failures on macOS (26.5.2), where a failed subscription was previously sticky with no retry attempts.
* Fixes an {{elastic-defend}} crash that occurred when a Kafka broker rejected an oversized document.
* Fixes {{elastic-defend}} to properly honor {{es}} `queue.*` settings sent from {{kib}}, as well as queue presets.
* Fixes validation of the `bulk_max_size` output setting in {{elastic-defend}}.
* Fixes a race condition when assigning the username of mounted USB devices in {{elastic-defend}} on Windows.
* Improves the accuracy of serial number gathering in {{elastic-defend}} on Windows.
* Fixes a rare process tracking issue in {{elastic-defend}} on macOS and Linux.
* Fixes an issue where {{elastic-defend}} on Linux did not properly read tty events on older kernels (`4.18`) with eBPF backports, such as on RHEL 8.
* Improves the reliability of fanotify event collection in {{elastic-defend}} on Ubuntu 26.04 and Linux 7.0.
* Fixes {{elastic-defend}} on Linux to no longer perform any file reads for executables matching a trusted application entry.
* Fixes {{elastic-defend}} on Windows to display the custom popup on cached denied requests in Device Control.
* Fixes {{elastic-defend}} handling of `windows.advanced.events.security.event_disabled` on Windows, so removing event IDs from the list correctly re-enables those Security events without requiring an additional policy reapply.
* Fixes a rare edge case where {{elastic-defend}} could lose Tamper Protection.
* Fixes an issue with rollback configuration in {{elastic-defend}} on Windows, where under certain runtime conditions the endpoint could get stuck in the `CONFIGURING` state for an extended period when updating a policy with rollback enabled.
* Fixes a partial-write bug so {{elastic-defend}} correctly sends data to a {{ls}} output when the kernel TCP send buffer is full, resolving premature connection failures.
* Fixes a sharing violation in the `get-file` response action in {{elastic-defend}}.


## 9.4.4 [elastic-security-9.4.4-release-notes]

### Features and enhancements [elastic-security-9.4.4-features-enhancements]

* Adds the LXC container name to event telemetry for {{elastic-defend}} on Linux.

### Fixes [elastic-security-9.4.4-fixes]

* Fixes an issue where opening the rule details flyout for a deleted rule crashed the {{security-app}} when the rule was missing `severity_mapping` or `risk_score_mapping` values [#278545]({{kib-pull}}278545).
* Fixes an issue where {{kib}} assets from an installed integration package (such as dashboards used by prebuilt detection rules) could remain stale across a {{kib}} upgrade because {{fleet}} never overwrote existing assets on reinstall [#277953]({{kib-pull}}277953).
* Fixes an issue where the **Source event** link in an alert's **Highlighted fields** section failed to open the document when its source index had been restored (for example, from a cold or frozen tier) and renamed [#277703]({{kib-pull}}277703).
* Fixes an issue where agents on version-specific policies did not appear in the Osquery agent or policy selector and could not be targeted, causing live queries to fail with a `No agents found for selection` error [#277283]({{kib-pull}}277283).
* Fixes an issue where endpoints did not appear in the **Endpoints** list and response actions failed for agents whose `policy_id` included an agent-specific policy suffix [#277100]({{kib-pull}}277100).
* Fixes an issue where saving an Indicator Match rule through the UI reset the API-only `concurrent_searches` and `items_per_search` fields to their defaults [#276823]({{kib-pull}}276823).
* Fixes an issue where attaching an entity to a conversation in {{agent-builder}} crashed when a field such as `watchlists` or `sources` contained a single value instead of an array [#276201]({{kib-pull}}276201).
* Preserves the prebuilt rule `revision` (incremented by 1) when upgrading a rule to a different rule type, matching the behavior of same-type upgrades [#275627]({{kib-pull}}275627).
* Fixes the **Investigate in Timeline** action for suppressed alerts whose rule uses exception lists, which previously failed when the exception list data was stored as a single object instead of an array [#275417]({{kib-pull}}275417).
* Fixes an issue where deprecated prebuilt rules could reappear as installable after being deleted through the deprecation callouts [#274447]({{kib-pull}}274447).
* Fixes an issue where the rule editing UI rejected valid semver range version constraints (such as `^8.2.0 || ^9.0.0`) on related integrations [#274133]({{kib-pull}}274133).
* Fixes an issue where running a workflow that requires manual input from the **Run workflow** alert action started the execution without prompting for the input, causing it to fail immediately. A manual input dialog now collects the required values before the workflow runs [#271586]({{kib-pull}}271586).
* Fixes an issue where visualizations in dashboards created by Automatic Migration did not render on initial load, requiring manual interaction to display data [#264102]({{kib-pull}}264102).
* Fixes a race condition when assigning the username of mounted USB devices in {{elastic-defend}} on Windows.
* Improves serial number gathering accuracy in {{elastic-defend}} on Windows.
* Updates the bundled `curl` library in {{elastic-defend}}, improving the stability of network operations on Linux.
* Fixes an issue in {{elastic-defend}} that could result in incomplete addresses in network event tracking.
* Fixes an issue where {{elastic-defend}} on macOS did not attempt to recover a failed subscription to network events, which previously remained stuck.
* Fixes a crash in {{elastic-defend}} when the Kafka broker rejected a document that was too large.
* Fixes an issue where {{elastic-defend}} on Windows did not display the custom popup for cached denied requests in Device Control.

## 9.4.3 [elastic-security-9.4.3-release-notes]

### Fixes [elastic-security-9.4.3-fixes]

* Fixes an issue where only the first assignee was displayed in the alert details flyout instead of all assigned users [#273801]({{kib-pull}}273801).
* Fixes a scroll-position jump in the alert details flyout **Table** tab [#273521]({{kib-pull}}273521).
* Fixes an issue where the {{agent-builder}} announcement modal could reappear during page navigation after being dismissed, particularly in high-latency or proxy environments [#272276]({{kib-pull}}272276).
* Fixes the entities table on the **Entity Analytics** page to sort by risk score by default, showing the highest-risk entities first and placing entities without a risk score at the bottom [#272234]({{kib-pull}}272234).
* Scopes watchlist index sync to the watchlist creator's credentials, requiring read access to the configured index. Watchlists created before this change show a **Sync paused** callout with a **Re-authorize** action [#270292]({{kib-pull}}270292).
* Fixes an issue where the **Delete all** action for deprecated prebuilt rules failed when more than 100 deprecated rules existed [#271550]({{kib-pull}}271550).
* Fixes an issue in {{elastic-defend}} on Linux where BPF DNS event sources could corrupt probe data.
* Fixes an issue where {{elastic-defend}} on Linux did not correctly read TTY events on older kernels (4.18) with eBPF backports, such as on RHEL 8.
* Improves {{elastic-defend}} event enrichment scalability on hosts with many long-lived processes by using a larger, self-pruning process cache.
* Fixes a rare edge case where {{elastic-defend}} could lose Tamper Protection.
* Fixes a rare process tracking issue in {{elastic-defend}} on macOS and Linux.
* Fixes a race condition when assigning the username of mounted USB devices in {{elastic-defend}} on Windows.


## 9.4.2 [elastic-security-9.4.2-release-notes]

### Features and enhancements [elastic-security-9.4.2-features-enhancements]

* Improves Automatic Migration dashboard migration accuracy by sampling index records before query translation, enabling the LLM to generate {{esql}} queries with correct field names and values from the first attempt [#261927]({{kib-pull}}261927).
* Adds a warning callout to the **Endpoint exceptions**, **Trusted applications**, and **Event filters** forms when users enter unnecessarily escaped characters [#268477]({{kib-pull}}268477).
* Adds a warning callout and confirmation modal to the rule exceptions form when entering escaped characters (such as `\*` or `\?`) with the `matches` operator, indicating they might have intended wildcards instead [#268397]({{kib-pull}}268397).
* Updates the {{agent-builder}} announcement modal so that clicking **Revert** immediately switches all space users back to AI Assistant [#267906]({{kib-pull}}267906).

### Fixes [elastic-security-9.4.2-fixes]

* Fixes an issue where users with read-only access could see the asset criticality update dropdown in the entity details flyout. The dropdown is now correctly gated on write permissions [#269164]({{kib-pull}}269164).
* Fixes an issue where the alert details flyout **Overview** tab crashed in Discover for external alert documents [#269000]({{kib-pull}}269000).
* Fixes incorrect button alignment in Timeline [#268314]({{kib-pull}}268314).
* Fixes an incorrect banner shown in the Discover document flyout when Discover is embedded in a dashboard [#268249]({{kib-pull}}268249).
* Fixes empty **Last results**, **Docs**, and **Agents** columns on the Osquery pack details page for scheduled queries [#267894]({{kib-pull}}267894).
* Fixes multiple rendering issues in the entity details flyout when opened in **Preview** mode from {{agent-builder}} [#267342]({{kib-pull}}267342).
* Fixes an issue where the alert details flyout failed to render its header, content, and footer when Discover was embedded in a dashboard [#267321]({{kib-pull}}267321).
* Fixes the AI rule creation flow to respect the `enableESQL` advanced setting. When {{esql}} is disabled, the AI rule creation option is hidden and {{esql}} rule creation is blocked in {{agent-builder}} [#267247]({{kib-pull}}267247).
* Fixes a duplicate "AI Assistant" section on the **Feature Settings** page by consolidating the {{elastic-sec}} AI Assistant configuration under the **Security** group, and hides the AI Assistant for Security entry when AI Assistant is not the selected chat experience [#266697]({{kib-pull}}266697).
* Fixes the **Manage license** link on the Attack Discovery page to navigate directly to **License Management** instead of the {{stack-manage-app}} landing page [#266445]({{kib-pull}}266445).
* Fixes an issue where **View in AI Assistant** buttons and context menu items in Attack Discovery remained visible when the AI Assistant was hidden via **GenAI Settings** [#266111]({{kib-pull}}266111).
* Fixes an issue where auto-refresh on the **Alerts** page with grouping applied caused open flyouts and dialogs to close unexpectedly [#264518]({{kib-pull}}264518).
* Fixes an issue where {{elastic-endpoint}} could get stuck in the `CONFIGURING` state when updating an {{elastic-defend}} policy with rollback enabled on Windows.
* Fixes a sharing violation in the `get-file` response action for {{elastic-defend}}.
* Improves legacy event source compatibility with newer kernel versions (6.1+ and 7.0+) in {{elastic-defend}} on Linux.
* Fixes an issue where {{elastic-defend}} on Linux could trigger unnecessary automount activity on systems using `autofs`.
* Improves `fanotify` event collection reliability in {{elastic-defend}} on Ubuntu 26.04 and Linux 7.0.

## 9.4.1 [elastic-security-9.4.1-release-notes]

### Fixes [elastic-security-9.4.1-fixes]

* Fixes an issue where detection rules failed with errors when their executing users lacked read access to entity store indices. Entity store enrichment is now silently skipped for users without entity store index access [#267787]({{kib-pull}}267787).
* Fixes an issue where the Security alert flyout failed to render its header, content, and footer when Discover was embedded in a dashboard [#267321]({{kib-pull}}267321).
* Fixes the events histogram and host/network event count panels on the **Overview** dashboard, which incorrectly included alert documents in event counts, and ensures compatibility with cross-cluster search so events from remote clusters are correctly included [#265561]({{kib-pull}}265561).
* Fixes an incorrect ordering of the **Launchpad** item in the classic global side navigation. The item now appears above **Manage**, consistent with {{elastic-sec}} own classic navigation [#268216]({{kib-pull}}268216).
* Fixes an issue where the entity store log extraction window could grow unboundedly in lagging environments, causing {{esql}} probe cost to spiral. Adds a `maxTimeWindowSize` parameter (default: `15m`) to the install and update APIs to cap each probe's window size. Also adds an `excludedIndexPatterns` parameter that lets you exclude specific index patterns from log extraction. By default, the entity store extracts entities from all data sources defined in the Default Security data view; use `excludedIndexPatterns` to skip patterns you don't want to include [#268170]({{kib-pull}}268170).
* Fixes an issue where {{elastic-defend}} failed to send data to {{ls}} output when the kernel TCP send buffer was full, causing connections to drop prematurely.
* Updates eBPF probes for {{elastic-defend}} on Linux to support 7.0 kernels.
* Fixes {{elastic-defend}} on Linux to report more accurate path names for file-less execution events.

## 9.4.0 [elastic-security-9.4.0-release-notes]

### Features and enhancements [elastic-security-9.4.0-features-enhancements]

* Reorganizes the {{elastic-sec}} classic navigation to group **Get started**, **Value Report**, and migration-related items under a **Launchpad** section [#260429]({{kib-pull}}260429).
* Adds a new **Overview** tab to the rule details page [#251662]({{kib-pull}}251662).
* Adds an improved rule execution results table to the **Execution Results** tab on the rule details page (behind the `newExecutionResultsTableEnabled` feature flag), showing execution status, timestamp, duration, gap info, and other key metrics, with sorting, pagination, and a per-execution detail flyout [#259105]({{kib-pull}}259105).
* Adds a **Rule Monitoring Overview** panel to the **Rule Monitoring** tab, showing a summary of rule execution statuses and gap fill status breakdowns [#252327]({{kib-pull}}252327).
* Adds a gap detection scope section to **Rule Settings**, allowing you to control which gap reasons (such as rule-disabled gaps) are included in gap monitoring and auto-fill. Adds reason-based filtering to the gap table and **Bulk Fill** modal [#260095]({{kib-pull}}260095).
* Adds a new `error` gap fill status for the gap auto-fill scheduler [#259130]({{kib-pull}}259130).
* Adds `matched_indices_count` and `matched_indicator_indices_count` rule execution metrics [#259938]({{kib-pull}}259938).
* Adds an `alerts_candidate_count` rule execution metric [#259917]({{kib-pull}}259917).
* Adds high-level rule execution info logging [#253992]({{kib-pull}}253992).
* Adds UI for identifying and managing deprecated prebuilt detection rules, including a dismissable callout on the rules table page and a callout on the rule details page with actions to delete or duplicate-and-delete deprecated rules [#259673]({{kib-pull}}259673).
* Updates MITRE ATT&CK mappings to `v18.1` [#246770]({{kib-pull}}246770).
* Adds new RBAC subfeatures for rules management, allowing granular control over investigation guide editing, custom highlighted fields, enabling/disabling rules, manual rule runs, and rules management settings independently of read-only rules access [#250131]({{kib-pull}}250131).
* Adds an **Exceptions** RBAC subfeature to the Rules privilege, allowing you to grant exception list management independently of rules read/write access [#245722]({{kib-pull}}245722).
* Adds a dedicated **Alerts** {{kib}} feature privilege, separating alert view and edit access from rules management. Alert read/edit can now be granted independently of rules privileges [#244637]({{kib-pull}}244637).
* Adds an Agent Builder skill for querying Security {{ml}} jobs for {{anomaly-detect}} questions [#254908]({{kib-pull}}254908).
* Automatically injects `METADATA _id` into {{esql}} detection rule queries during execution, removing the requirement for you to include it manually. A non-blocking warning is shown when automatic injection is not possible [#254703]({{kib-pull}}254703).
* Adds an Agent Builder skill for creating detection rules [#247674]({{kib-pull}}247674).
* Adds validation for Indicator Match rules' `threat_index` parameter, so rules enter a partial failure state with a warning when no matching threat indices are found, matching the behavior of the `index` parameter [#256353]({{kib-pull}}256353).
* Adds a new initialization API endpoint for the exception list index creation flow [#258891]({{kib-pull}}258891).
* Enables search in the **JSON** tab of the Security Solution alert flyout, matching the behavior of the Discover document flyout [#263875]({{kib-pull}}263875).
* Adds a callout and badge to the visual event analyzer in the alert details flyout to indicate when cold and frozen data tiers are excluded from analyzer queries [#257015]({{kib-pull}}257015).
* Adds an advanced setting to exclude cold and frozen data tiers from prevalence queries in the alert details flyout, improving load performance [#257011]({{kib-pull}}257011).
* Adds a **Run workflow** action to the alerts table for both individual alert rows and bulk selections [#252405]({{kib-pull}}252405).
* Allows you to define custom alert closing reasons in **Advanced settings** [#253127]({{kib-pull}}253127).
* Improves Attack Discovery accuracy by automatically verifying and filtering out discoveries that contain hallucinated (non-existent) alert IDs [#247965]({{kib-pull}}247965).
* Makes the Attack Discovery and Attack Discovery Schedules APIs generally available [#246788]({{kib-pull}}246788).
* Gives Automatic Migration its own dedicated **Migrations** page and navigation entry, moving the migration creation flow out of the **Get started** page [#260379]({{kib-pull}}260379).
* Adds support for importing and parsing Splunk v2 (JSON-format) dashboards in Automatic Migration [#251199]({{kib-pull}}251199), [#253970]({{kib-pull}}253970).
* Excludes QRadar building-block rules from Automatic Migration eligibility and improves the XML upload UX [#250558]({{kib-pull}}250558).
* Updates the `fast-xml-parser` package dependency to version 5.3.4 [#251644]({{kib-pull}}251644).
* Changes the default chat experience in {{elastic-sec}} and Elastic {{observability}} contexts to AI Agent. A one-time announcement explains the change and allows you to return to the classic AI Assistant from **GenAI Settings**. The dismissal state is remembered per space [#260570]({{kib-pull}}260570).
* Adds an anonymization profiles UI under **{{stack-manage-app}} → GenAI Settings → Anonymization**, with support for field rules, regex rules, and Named Entity Recognition (NER) rules, backed by the anonymization platform service foundation [#256246]({{kib-pull}}256246), [#252616]({{kib-pull}}252616).
* Adds an **Add to chat** button on the rule details, rule editing, and alert flyout rule preview pages, allowing you to attach any detection rule to AI Agent for exploration and analysis [#253043]({{kib-pull}}253043).
* Adds an option to provide a closing reason when closing a case, which is synced to the associated alerts when the alert-sync toggle is enabled [#254603]({{kib-pull}}254603).
* Adds a **Status** column and disables the **Select** button for closed cases in the **Add to existing case** modal, preventing you from adding alerts to a closed case [#260990]({{kib-pull}}260990).
* Consolidates Entity Risk Score, Asset Criticality, and Entity Store engine status management into a single **Entity Analytics** management page with tabbed navigation and a unified enable/disable toggle [#255009]({{kib-pull}}255009).
* Updates the asset criticality CSV upload UI to use the v2 upload API [#260102]({{kib-pull}}260102).
* Adds an asset criticality v2 CSV upload API [#259386]({{kib-pull}}259386).
* Adds resolution grouping as the default grouping option in the Entity Analytics data grid. Grouped entities display the target entity name, entity count, and risk score [#258892]({{kib-pull}}258892).
* Adds a manual entity resolution UI to the entity details flyout, allowing you to create and manage resolution groups that link multiple entity records representing the same real-world identity [#260162]({{kib-pull}}260162).
* Adds entity resolution CSV upload support, including a backend API and UI [#260006]({{kib-pull}}260006).
* Introduces Entity Threat Hunting on the **Entity Analytics** page, surfacing prioritized investigation leads based on behavioral observations, risk scoring, and temporal state analysis with Agent Builder integration for guided investigation. Adds the **Entity Threat Hunting** leads cards, a **See All** flyout, and a lead provenance flyout [#257610]({{kib-pull}}257610).
* Introduces the Entity Threat Hunting backend infrastructure, including the feature flag, shared types and index templates, observation module interface, Risk and Temporal State modules, behavioral observation modules, entity retrieval and enrichment, API routes, `LeadDataClient`, async lead generation, and an automated email-based entity resolution maintainer [#255272]({{kib-pull}}255272), [#256156]({{kib-pull}}256156), [#256270]({{kib-pull}}256270), [#256628]({{kib-pull}}256628), [#257046]({{kib-pull}}257046), [#257479]({{kib-pull}}257479).
* Allows user and host details flyouts to open while observed data is loading [#252657]({{kib-pull}}252657).
* Adds an Entity Analytics Agent Builder skill for answering risk score and entity risk questions [#252400]({{kib-pull}}252400).
* Adds a rich visual renderer for `security.entity` attachments in {{agent-builder}}, displaying resolved entities as cards or tables [#264985]({{kib-pull}}264985).
* Adds a `communicates_with` entity relationship maintainer for Entity Store v2, populating user entity relationship data based on cloud API and MDM activity from {{aws}} CloudTrail, Azure Sign-in Logs, Okta System Logs, and Jamf Pro [#258656]({{kib-pull}}258656).
* Adds a namespace ID filter to **Advanced settings** for filtering Entity Store entities by namespace [#247733]({{kib-pull}}247733).
* Enables showing entity relationships from the entity node context menu in the graph visualization [#252803]({{kib-pull}}252803).
* Adds support for fetching entity relationships from the Entity Graph API [#251178]({{kib-pull}}251178).
* Prepares the monitoring entity source CRUD APIs for general availability of privileged user monitoring [#246978]({{kib-pull}}246978).
* Adds reusability support for the {{gcp}} cloud connector [#253093]({{kib-pull}}253093).
* Filters the cloud connector selector to show only connectors matching both the policy's cloud provider and account type (`single-account` or `organization-account`) [#250107]({{kib-pull}}250107).
* Adds a unified Osquery **History** table that combines live and scheduled query results with cursor-based pagination, source filtering, a date range picker, and routing to scheduled execution details [#256917]({{kib-pull}}256917).
* Persists Osquery **History** page filters (search text, source filter, date range) in session storage so they are restored when navigating between tabs and detail pages within the same browser session [#260891]({{kib-pull}}260891).
* Adds URL parameter support to the Osquery **History** page, enabling deep-linking to filtered history views [#257895]({{kib-pull}}257895).
* Adds a scheduled execution details page and API for Osquery [#257118]({{kib-pull}}257118).
* Adds a unified results details table for Osquery (behind the `osqueryUnifiedDataTable` feature flag) with a KQL search bar, document detail flyout, drag-and-drop column reordering, density controls, and full-screen mode [#257627]({{kib-pull}}257627).
* Enables dynamic schema loading for Osquery: table and ECS field schemas are now fetched at runtime from the installed `osquery_manager` integration package, keeping autocomplete and ECS mapping data in sync with the installed integration version [#258833]({{kib-pull}}258833).
* Adds the ability to duplicate Osquery saved queries and packs, and adds a row action menu with **Edit**, **Duplicate**, and **Delete** actions to the saved queries and packs list tables [#252517]({{kib-pull}}252517).
* Moves Endpoint exceptions from the **Shared exception lists** and **Rules** pages to the **Endpoint Artifacts** page, separating them from rule exceptions. Adds an opt-in for per-policy Endpoint exception assignment and adds export/import functionality to all Endpoint artifacts [#260983]({{kib-pull}}260983).
* Adds the `linux.advanced.ransomware.diagnostic` advanced {{elastic-defend}} policy flag in preparation for Linux ransomware protection support [#260538]({{kib-pull}}260538).
* Adds a script library for creating and managing scripts for use with the `runscript` response action on {{elastic-defend}}-protected hosts [#258400]({{kib-pull}}258400).
* Adds `runscript` response action support to {{elastic-defend}}.
* Improves {{elastic-defend}} by automatically enabling the required Windows security audit policies, ensuring the endpoint can collect the telemetry those policies control. Disabled by default; enable using an advanced policy flag.
* Adds a `memory-dump` response action to {{elastic-defend}} on Linux.
* Adds process event tracking for `ptrace`, shared memory, `memfd`, and module-load operations to {{elastic-defend}} on Linux.
* Adds the YARA rule name to the `message` field for {{elastic-defend}} file alerts.
* Improves {{elastic-defend}} support for x64 symbol resolution on Windows on ARM64.
* Extends {{elastic-defend}} device control to Windows Portable Devices.
* Improves the reliability of {{elastic-defend}}'s malware-on-write detection.
* Improves {{elastic-defend}} behavioral protection performance by unloading rules that are fully covered by simple exception or trust entries, preventing CPU usage from evaluating events against those rules.
* Further reduces {{elastic-defend}} behavioral protection CPU usage for trusted applications.
* Adds ransomware protection to {{elastic-defend}} on macOS. Turned off by default; turn on using the `mac.ransomware.mode` advanced policy setting.



### Fixes [elastic-security-9.4.0-fixes]

* Fixes an issue where detection engine gap errors were classified as non-user errors, which caused gap-only rule failures to count against SLO dashboards [#263244]({{kib-pull}}263244).
* Fixes an issue where disabled detection rules could appear stuck in a "running" state after a {{kib}} crash [#262374]({{kib-pull}}262374).
* Extends the query execution timeout to 24 hours [#262008]({{kib-pull}}262008).
* Fixes an issue where duplicate toolbars appeared on the detection rule monitoring dashboard [#261846]({{kib-pull}}261846).
* Fixes an issue where the search bar on the **Alerts** tab of the rule details page overlapped the alerts table in full screen mode [#260315]({{kib-pull}}260315).
* Removes Endpoint List bootstrap calls from rule-related routes [#258266]({{kib-pull}}258266).
* Fixes out-of-memory crashes and {{kib}} restarts caused by the gap auto-fill scheduler creating excessively large saved objects for rules with short intervals and long gaps [#254788]({{kib-pull}}254788).
* Fixes an issue where the legacy `rules/prepackaged` endpoints returned 500 errors on Basic licenses when processing prebuilt rule packages that include {{ml}} rules [#253574]({{kib-pull}}253574).
* Improves the performance of bulk rule deletion [#253116]({{kib-pull}}253116).
* Fixes responsiveness issues on the rule details **Overview** tab [#252890]({{kib-pull}}252890).
* Fixes an issue where detection rules APIs didn't properly validate endpoint response actions [#251352]({{kib-pull}}251352).
* Removes the Technical Preview badge from the privileged access detection package [#249500]({{kib-pull}}249500).
* Improves the stability of the **Add Elastic rules** page on deployments with low RAM configurations [#248259]({{kib-pull}}248259).
* Fixes an issue where the rule summary button was enabled for users who lacked the full set of required rule privileges [#248221]({{kib-pull}}248221).
* Fixes an issue where the gap fill scheduler logs flyout did not display tooltips for status tags [#247695]({{kib-pull}}247695).
* Fixes an issue where the rule settings pop-up remained open after clicking **Save** when enabling or disabling auto gap fill [#247678]({{kib-pull}}247678).
* Fixes a display issue with filters on the **MITRE ATT&CK® coverage** page [#246794]({{kib-pull}}246794).
* Fixes a race condition in the query bar filter when the {{data-source}} was being created asynchronously [#261523]({{kib-pull}}261523).
* Fixes an issue where the required fields component showed a false positive warning [#261830]({{kib-pull}}261830).
* Fixes an issue in EQL rule creation where the query field did not re-validate after changing the index pattern, leaving stale errors on screen even when the query was valid for the newly selected {{data-source}} [#261027]({{kib-pull}}261027).
* Fixes incorrect alert counting for indicator match detection rules when a page of source documents matches no indicators, so max-alerts warnings display correctly [#259199]({{kib-pull}}259199).
* Fixes an issue where {{esql}} rule execution did not apply data tier exclusion filters to the source document enrichment query, potentially querying excluded cold and frozen tiers [#255341]({{kib-pull}}255341).
* Fixes EQL sequence document merging to treat dot notation and nested notation as equivalent [#254830]({{kib-pull}}254830).
* Adds integration test coverage for {{esql}} rule execution logic [#252936]({{kib-pull}}252936).
* Fixes an accessibility issue with the ARIA announcement in the **Add exception list** dialog [#250624]({{kib-pull}}250624).
* Fixes an issue where the `os_types` field was not saved when creating an exception list [#250279]({{kib-pull}}250279).
* Fixes an issue where backslashes were removed when typed in exception field values [#250117]({{kib-pull}}250117).
* Fixes an issue where shared exception list entries showed the list ID instead of the list name [#249778]({{kib-pull}}249778).
* Updates the icon that is shown when alert suppression is not available because of insufficient license [#247964]({{kib-pull}}247964).
* Truncates long text in the **Value** column in the value list modal [#246679]({{kib-pull}}246679).
* Removes Beta labels and badges from the AI Agent chat experience, including the chat selection card, announcement modal, advanced settings value, and Elastic {{observability}} opt-in tour [#264200]({{kib-pull}}264200).
* Suppresses the AI Agent announcement modal in automated browser sessions by checking `navigator.webdriver`, so synthetic monitors and end-to-end tests are not affected [#263785]({{kib-pull}}263785).
* Updates the copy in the AI Agent announcement modal [#263034]({{kib-pull}}263034).
* Fixes an issue where the Agent Builder sidebar did not open when navigating directly to rule creation [#262588]({{kib-pull}}262588).
* Removes the AI Assistant prefill behavior to ensure compatibility with Claude Sonnet 4.6 and Opus 4.6 [#255740]({{kib-pull}}255740).
* Enables the `defaultModel` setting for the Azure OpenAI connector to support APIM endpoints [#253577]({{kib-pull}}253577).
* Adds a `region` field to the Amazon Bedrock connector [#252960]({{kib-pull}}252960), [#252956]({{kib-pull}}252956).
* Fixes accessibility issues in the Security AI Assistant confirm delete modal [#251962]({{kib-pull}}251962).
* Adds optional field indicators to the OpenAI connector configuration [#251857]({{kib-pull}}251857).
* Fixes an accessibility issue with a missing label in the Security AI Assistant flyout [#251656]({{kib-pull}}251656).
* Fixes the `spaceId` handling in Agent Builder security tools [#251513]({{kib-pull}}251513).
* Fixes an issue in the Security AI Assistant where the **Add connector** button was incorrectly grayed out for users with permission to create connectors [#250921]({{kib-pull}}250921).
* Fixes an issue where the Security AI Assistant chat completion API didn't use an associated conversation's system prompt [#248020]({{kib-pull}}248020).
* Replaces a deprecated icon in the UI [#251930]({{kib-pull}}251930).
* Fixes a Firefox scroll position jump that occurred when hovering field rows with cell actions in the **Table** tab of the alert details flyout [#262682]({{kib-pull}}262682).
* Fixes an issue where alert KPI counts were rendered with incorrect whitespace [#260803]({{kib-pull}}260803).
* Fixes an issue where the alert details flyout persisted after navigating away from {{elastic-sec}} [#256001]({{kib-pull}}256001).
* Fixes an issue where alert flyout section expansion state in local storage did not honor all saved values [#251999]({{kib-pull}}251999).
* Fixes an issue where the **Threat intelligence** section in the alert details flyout didn't display multiple values [#245449]({{kib-pull}}245449).
* Fixes a denial-of-service risk in Timeline bulk export by validating the number of Timeline IDs (up to 1,000), deduplicating IDs, and bounding enrichment work [#260265]({{kib-pull}}260265).
* Fixes an issue where Timeline bulk deletion did not work correctly [#260206]({{kib-pull}}260206).
* Fixes an issue where notes not associated with a saved Timeline could appear on the **Notes** tab while investigating in Timeline, including for draft Timelines [#259658]({{kib-pull}}259658).
* Adds support for timestamp overrides to Timeline at the {{data-source}} level, allowing Timeline to use the {{data-source}}'s configured timestamp field instead of `@timestamp` [#251827]({{kib-pull}}251827).
* Fixes an issue where the **Comprehensive File Timeline** template filters combined with OR logic instead of AND [#251242]({{kib-pull}}251242).
* Fixes an issue where delete actions on notes were not restricted for read-only users and improves the related error message [#247617]({{kib-pull}}247617).
* Fixes an issue where deleting a note in the Timelines table did not update the UI [#249777]({{kib-pull}}249777).
* Fixes incorrect pagination display in the **Notes** tab that showed "1-0 of 0" when no notes existed [#248481]({{kib-pull}}248481).
* Fixes notes filtering logic to correctly show notes attached to alerts, events, and timelines [#248110]({{kib-pull}}248110).
* Fixes an issue where the `createdBy` field in the notes filter didn't use exact matching [#247351]({{kib-pull}}247351).
* Fixes an issue where the visual event analyzer preview could fetch data with incorrect indices before the {{data-source}} was fully loaded [#255400]({{kib-pull}}255400).
* Fixes an issue where visual event analyzer queries could return cached results for incorrect indices [#255396]({{kib-pull}}255396).
* Fixes an issue where the visual event analyzer did not display in the alert details flyout in certain {{data-source}} configurations [#255182]({{kib-pull}}255182).
* Fixes an issue where the visual event analyzer rendered before the {{data-source}} was ready [#245712]({{kib-pull}}245712).
* Fixes an issue where Attack Discovery schedules failed to run due to internal Elastic Managed LLM connector changes [#249891]({{kib-pull}}249891).
* Fixes an issue where tabs were visible for generic attack groups in Attack Discovery [#248444]({{kib-pull}}248444).
* Fixes an issue where Attack Discovery incorrectly classified the "Security AI Anonymization settings configured to not allow any fields" message as a system error instead of a user error [#248439]({{kib-pull}}248439).
* Changes the placement of **Migrations** and **Inventory** items in the {{elastic-sec}} navigation menu [#247002]({{kib-pull}}247002).
* Improves Automatic Migration performance by reducing the number of {{es}} calls when updating field mappings [#252431]({{kib-pull}}252431).
* Fixes an Automatic Migration issue where failed rules appeared in non-failed status filters [#252263]({{kib-pull}}252263).
* Fixes the **Get started** page visibility for users with read-only privileges for rules [#247355]({{kib-pull}}247355).
* Fixes an issue where the last event ingested metric pulled from an incorrect scope and too few indices [#262346]({{kib-pull}}262346).
* Fixes Entity Store install API parameter validation [#252366]({{kib-pull}}252366).
* Fixes an issue where the privileged user monitoring table didn't refresh alert data when the time range changed [#250618]({{kib-pull}}250618).
* Fixes an issue where index updates failed due to an invalid API payload [#250758]({{kib-pull}}250758).
* Fixes an issue where the CSV export in Entity Analytics displayed an incorrect user count [#249032]({{kib-pull}}249032).
* Fixes an issue where entity user and host names were not escaped in URLs, which resulted in invalid URLs [#247707]({{kib-pull}}247707).
* Fixes an issue where special characters in {{esql}} queries for risk scoring were not handled correctly [#247060]({{kib-pull}}247060).
* Fixes an issue where the **Entity summary** section in the entity details flyout showed incorrect vulnerabilities data [#246889]({{kib-pull}}246889).
* Updates Active Directory matchers to use SID-based privileged groups for privileged user monitoring [#246763]({{kib-pull}}246763).
* Fixes an issue where Monaco editor autocomplete suggestions appeared behind modals and flyouts in the Osquery editor [#259558]({{kib-pull}}259558).
* Fixes an issue where prebuilt Osquery packs displayed a numeric user ID instead of a username in the **Created by** column on ECH deployments [#261115]({{kib-pull}}261115).
* Adds {{ccs-cap}} ({{ccs-init}}) support to Osquery search queries [#260518]({{kib-pull}}260518).
* Standardizes and persists the rows-per-page preference across Osquery tabs [#253499]({{kib-pull}}253499).
* Fixes URL parameter handling in the Osquery history page [#250469]({{kib-pull}}250469).
* Fixes CrowdStrike `runscript` response actions to correctly display script output (stdout/stderr) in the **Response Console** and **Action History** views [#262470]({{kib-pull}}262470).
* Returns an error when you submit a malware scan job while malware protection is not enabled [#255597]({{kib-pull}}255597).
* Fixes a memory leak in {{elastic-defend}} related to path normalization, introduced in 9.3.0.
* Fixes a bug in {{elastic-defend}} that could delay uninstall by up to 30 seconds in some configurations.
* Improves {{elastic-defend}} on Linux to detect and report when the service fails to start.
* Fixes a {{elastic-defend}} Kafka output issue by handling transient or invalid metadata responses with fallback to broker-selected partitioning, preventing a divide-by-zero error.
* Updates {{elastic-defend}} Linux BPF probes to support kernels with lazy preemption enabled.
* Fixes an issue where {{elastic-defend}} did not correctly honor the `ignored_filesystems` setting when a filesystem was detected.
* Fixes an issue that would cause hotfix builds of {{elastic-defend}} to incorrectly report their version in Windows Security Center.
* Fixes a bug in version 9.3.0 of {{elastic-defend}} that resulted in the Windows Security Center status page showing an error.
* Fixes an issue where `user.name` and `group.name` fields were missing from {{elastic-defend}} events in some LDAP environments.
* Fixes an issue where {{elastic-defend}} on Windows could log a warning about "Quarantine directory failed validation due to ACL or file attribute change" for empty removable media drives such as optical drives.
* Fixes an issue in {{elastic-defend}} that could cause the system to lock up for up to several minutes during {{elastic-defend}} uninstallation or upgrade.

## 9.3.8 [elastic-security-9.3.8-release-notes]

### Features and enhancements [elastic-security-9.3.8-features-enhancements]

* Adds the LXC container name to event telemetry for {{elastic-defend}} on Linux.

### Fixes [elastic-security-9.3.8-fixes]

* Fixes an issue where opening the rule details flyout for a deleted rule crashed the {{security-app}} when the rule was missing `severity_mapping` or `risk_score_mapping` values [#278545]({{kib-pull}}278545).
* Fixes an issue where {{kib}} assets from an installed integration package (such as dashboards used by prebuilt detection rules) could remain stale across a {{kib}} upgrade because {{fleet}} never overwrote existing assets on reinstall [#277953]({{kib-pull}}277953).
* Fixes a crash in index fields formatting when a field or index was named using a reserved JavaScript object property (such as `constructor` or `__proto__`) [#277851]({{kib-pull}}277851).
* Fixes an issue where the **Source event** link in an alert's **Highlighted fields** section failed to open the document when its source index had been restored (for example, from a cold or frozen tier) and renamed [#277703]({{kib-pull}}277703).
* Preserves the prebuilt rule `revision` (incremented by 1) when upgrading a rule to a different rule type, matching the behavior of same-type upgrades [#275627]({{kib-pull}}275627).
* Updates the bundled `curl` library in {{elastic-defend}}, improving the stability of network operations on Linux.
* Fixes an issue where {{elastic-defend}} on macOS did not attempt to recover a failed subscription to network events, which previously remained stuck.
* Fixes a crash in {{elastic-defend}} when the Kafka broker rejected a document that was too large.
* Fixes an issue in {{elastic-defend}} that could result in incomplete addresses in network event tracking.

## 9.3.7 [elastic-security-9.3.7-release-notes]

### Fixes [elastic-security-9.3.7-fixes]
* Fixes an issue where the rule editing UI rejected valid semver range version constraints (such as `^8.2.0 || ^9.0.0`) on related integrations [#274133]({{kib-pull}}274133).
* Fixes an issue in the AI Assistant where selecting all conversations and then saving an edit to a single conversation deleted all conversations instead of updating only the edited one [#274033]({{kib-pull}}274033).
* Fixes `bulk_max_size` output setting validation in {{elastic-defend}}.

## 9.3.6 [elastic-security-9.3.6-release-notes]

### Fixes [elastic-security-9.3.6-fixes]

* Fixes a scroll-position jump in the alert details flyout **Table** tab [#273521]({{kib-pull}}273521).
* Fixes alert action error toasts (assign, tag, open, close, acknowledge) so they show the full error message from {{es}} instead of a blank body [#269592]({{kib-pull}}269592).
* Improves {{elastic-defend}} event enrichment scalability on hosts with many long-lived processes by using a larger, self-pruning process cache.
* Fixes a rare process tracking issue in {{elastic-defend}} on macOS and Linux.

## 9.3.5 [elastic-security-9.3.5-release-notes]

### Fixes [elastic-security-9.3.5-fixes]

* Fixes incorrect button alignment in Timeline [#268314]({{kib-pull}}268314).
* Fixes an issue where the **Data Quality** dashboard showed no data when {{kib}} was set to Japanese [#265782]({{kib-pull}}265782).
* Fixes an issue where auto-refresh on the **Alerts** page with grouping applied caused open flyouts and dialogs to close unexpectedly [#264518]({{kib-pull}}264518).
* Fixes a denial-of-service risk in Timeline bulk export by validating the number of Timeline IDs (up to 1,000), deduplicating IDs, and bounding enrichment work [#260265]({{kib-pull}}260265).
* Fixes an issue where {{elastic-defend}} failed to send data to {{ls}} output when the kernel TCP send buffer was full, causing connections to drop prematurely.
* Updates eBPF probes for {{elastic-defend}} on Linux to support 7.0 kernels.
* Fixes {{elastic-defend}} on Linux to report more accurate path names for file-less execution events.
* Fixes an issue where {{elastic-endpoint}} could get stuck in the `CONFIGURING` state when updating an {{elastic-defend}} policy with rollback enabled on Windows.
* Fixes a sharing violation in the `get-file` response action for {{elastic-defend}}.
* Fixes an issue where {{elastic-defend}} did not display end user notifications for device control events.
* Improves legacy event source compatibility with newer kernel versions (6.1+ and 7.0+) in {{elastic-defend}} on Linux.
* Fixes an issue where {{elastic-defend}} on Linux could trigger unnecessary automount activity on systems using `autofs`.
* Improves `fanotify` event collection reliability in {{elastic-defend}} on Ubuntu 26.04 and Linux 7.0.
* Fixes an edge case where {{elastic-defend}} could lose tamper protection.


## 9.3.4 [elastic-security-9.3.4-release-notes]

### Features and enhancements [elastic-security-9.3.4-features-enhancements]

* Enables search in the **JSON** tab of the alert details flyout, matching the search experience available in the Discover document flyout [#263875]({{kib-pull}}263875).

### Fixes [elastic-security-9.3.4-fixes]

* Fixes an issue with Indicator Filters in the read-only rule details UI, where incorrect backing indices caused misleading warnings to display on hover [#263657]({{kib-pull}}263657).
* Fixes a Firefox-specific issue where the **Table** tab in the document details flyout jumped to the bottom when hovering over field rows with cell actions [#262682]({{kib-pull}}262682).
* Fixes CrowdStrike `runscript` response actions to correctly display script output (`stdout`/`stderr`) in the **Response Console** and **Action History** views [#262470]({{kib-pull}}262470).
* Extends the Osquery live query execution timeout maximum from 15 minutes to 24 hours [#262008]({{kib-pull}}262008).
* Fixes an issue where the required fields component displayed false-positive warnings for subfields of `flattened` type {{es}} fields, even when the rule's required fields were correctly configured [#261830]({{kib-pull}}261830).
* Fixes prebuilt Osquery packs displaying numeric user IDs instead of `elastic` in the **Created By** column [#261115]({{kib-pull}}261115).
* Fixes EQL rule creation so the query field re-validates after changing the index pattern, clearing stale errors when the query is valid for the newly selected data view [#261027]({{kib-pull}}261027).
* Fixes a layout issue where alert KPI panels overflowed their containers, causing excess whitespace on the **Alerts** and **Attacks** pages [#260803]({{kib-pull}}260803).
* Fixes a denial-of-service risk in Timeline bulk export by validating the number of Timeline IDs (up to 1,000), deduplicating IDs, and bounding enrichment work [#260265]({{kib-pull}}260265).
* Fixes a memory leak related to path normalization in {{elastic-defend}} that was introduced in 9.3.0.
* Fixes an {{elastic-defend}} Kafka output issue by falling back to broker-selected partitioning when transient or invalid metadata responses are received.
* Fixes a bug in {{elastic-defend}} that could delay uninstall by 30 seconds in some configurations.
* Ensures {{elastic-defend}} detects when the Linux service fails to start during installation and reports the error to {{agent}}.


## 9.3.3 [elastic-security-9.3.3-release-notes]

### Fixes [elastic-security-9.3.3-fixes]

* Fixes an issue where the search bar on the **Alerts** tab of the rule details page overlapped the alerts table in full screen mode [#260315]({{kib-pull}}260315).
* Fixes a denial-of-service risk in Timeline bulk export by validating the number of Timeline IDs (up to 1,000), deduplicating IDs, and bounding enrichment work [#260265]({{kib-pull}}260265).
* Fixes an issue where notes not associated with a saved Timeline could appear on the **Notes** tab while investigating in Timeline, including for draft Timelines [#259658]({{kib-pull}}259658).
* Fixes incorrect alert counting for indicator match detection rules when a page of source documents matches no indicators, so max-alerts warnings display correctly [#259199]({{kib-pull}}259199).
* Ensures {{elastic-defend}} honors `ignored_filesystems` when a filesystem appears in both monitored and ignored configuration lists.
* Fixes missing `user.name` and `group.name` fields in {{elastic-defend}} events in some LDAP environments.
* Returns an error when you submit a malware scan job while malware protection is not enabled for {{elastic-defend}}.


## 9.3.2 [elastic-security-9.3.2-release-notes]

### Features and enhancements [elastic-security-9.3.2-features-enhancements]

* Adds a callout and badge to the visual event analyzer in the alert details flyout to indicate when cold and frozen data tiers are excluded from analyzer queries [#257015]({{kib-pull}}257015).
* Adds an advanced setting to exclude cold and frozen data tiers from prevalence queries in the alert details flyout, improving load performance [#257011]({{kib-pull}}257011).
* Improves the reliability of {{elastic-defend}}'s malware-on-write detection.

### Fixes [elastic-security-9.3.2-fixes]

* Fixes an issue where the alert details flyout persisted after navigating away from {{elastic-sec}} [#256001]({{kib-pull}}256001).
* Fixes an issue where the visual event analyzer preview could fetch data with incorrect indices before the {{data-source}} was fully loaded [#255400]({{kib-pull}}255400).
* Fixes an issue where visual event analyzer queries could return cached results for incorrect indices [#255396]({{kib-pull}}255396).
* Fixes an issue where {{esql}} rule execution did not apply data tier exclusion filters to the source document enrichment query, potentially querying excluded cold and frozen tiers [#255341]({{kib-pull}}255341).
* Fixes an issue where the visual event analyzer did not display in the alert details flyout in certain {{data-source}} configurations [#255182]({{kib-pull}}255182).
* Fixes out-of-memory crashes and {{kib}} restarts caused by the gap auto-fill scheduler creating excessively large saved objects for rules with short intervals and long gaps [#254788]({{kib-pull}}254788).
* Fixes an issue where the legacy `rules/prepackaged` endpoints returned 500 errors on Basic licenses when processing prebuilt rule packages that include {{ml}} rules [#253574]({{kib-pull}}253574).
* Adds support for timestamp overrides to Timeline at the {{data-source}} level, allowing Timeline to use the {{data-source}}'s configured timestamp field instead of `@timestamp` [#251827]({{kib-pull}}251827).
* Fixes an issue that would cause hotfix builds of {{elastic-defend}} to incorrectly report their version in Windows Security Center. 
* Improves {{elastic-defend}} Linux trusted application handling by using Quark's trusted PID queue APIs for more consistent trusted PID synchronization.


## 9.3.1 [elastic-security-9.3.1-release-notes]

### Features and enhancements [elastic-security-9.3.1-features-enhancements]
* Allows user and host details flyouts to open while observed data is loading [#252657]({{kib-pull}}252657).
* Adds a new **Overview** tab to the rule details page [#251662]({{kib-pull}}251662).
* Adds a `region` field to the Amazon Bedrock connector [#252960]({{kib-pull}}252960), [#252956]({{kib-pull}}252956).
* Improves Automatic Migration performance by reducing the number of {{es}} calls when updating field mappings [#252431]({{kib-pull}}252431).
* Updates the `fast-xml-parser` package dependency to version 5.3.4 [#251644]({{kib-pull}}251644).

### Fixes [elastic-security-9.3.1-fixes]
* Improves the performance of bulk rule deletion [#253116]({{kib-pull}}253116).
* Fixes an Automatic Migration issue where failed rules appeared in non-failed status filters [#252263]({{kib-pull}}252263).
* Fixes accessibility issues in the Security AI Assistant confirm delete modal [#251962]({{kib-pull}}251962).
* Replaces a deprecated icon in the UI [#251930]({{kib-pull}}251930).
* Adds optional field indicators to the OpenAI connector configuration [#251857]({{kib-pull}}251857).
* Fixes an accessibility issue with a missing label in the Security AI Assistant flyout [#251656]({{kib-pull}}251656).
* Fixes the `spaceId` handling in Agent Builder security tools [#251513]({{kib-pull}}251513).
* Fixes an issue where detection rules APIs didn't properly validate endpoint response actions [#251352]({{kib-pull}}251352).
* Fixes an issue in the Security AI Assistant where the **Add connector** button was incorrectly grayed out for users with permission to create connectors [#250921]({{kib-pull}}250921).
* Fixes an issue where the privileged user monitoring table didn't refresh alert data when the time range changed [#250618]({{kib-pull}}250618).
* Fixes a DNS parsing bug in Linux versions of {{elastic-defend}} that could result in crashes.
* Fixes a bug in version 9.3.0 of {{elastic-defend}} that resulted in the Windows Security Center status page showing an error.


## 9.3.0 [elastic-security-9.3.0-release-notes]

### Features and enhancements [elastic-security-9.3.0-features-enhancements]

* Adds a new **Workflows** action to detection rules, allowing you to trigger workflows when a detection rule generates an alert. Refer to [](/explore-analyze/workflows.md) and [](/explore-analyze/workflows/triggers/alert-triggers.md) for more details.
* Adds a new **Rules, Alerts, and Exceptions** feature privilege that controls access to detection rules, alerts, and rule exceptions [#239634]({{kib-pull}}239634).
* Updates MITRE ATT&CK mappings to `v18.1` [#246770]({{kib-pull}}246770).
* Adds the gap auto-fill scheduler UI and API for detection rules [#244719]({{kib-pull}}244719).
* Adds a **Gap fill status** column and filter to the Rules table on the **Rule Monitoring** tab [#242595]({{kib-pull}}242595).
* Enables the **Value report** page in {{stack}} [#243511]({{kib-pull}}243511).
* Makes the Attack Discovery and Attack Discovery Schedules APIs generally available [#246788]({{kib-pull}}246788).
* Improves Attack Discovery prompts [#241346]({{kib-pull}}241346).
* Allows you to migrate QRadar rules to Elastic using Automatic Migration [#244924]({{kib-pull}}244924).
* Allows you to opt in to the new Agent Builder chat experience [#246089]({{kib-pull}}246089), [#243574]({{kib-pull}}243574), [#245259]({{kib-pull}}245259), [#242598]({{kib-pull}}242598), [#245205]({{kib-pull}}245205), [#246193]({{kib-pull}}246193), [#246403]({{kib-pull}}246403).
* Improves the alert details flyout by saving the selected threat intelligence time to local storage [#243571]({{kib-pull}}243571).
* Improves the alert details flyout by saving the selected prevalence time to local storage [#243543]({{kib-pull}}243543).
* Displays Session View in full height [#245888]({{kib-pull}}245888).
* Displays the visual event analyzer in full height [#245857]({{kib-pull}}245857).
* Persists the visual event analyzer's data view selection in local storage [#245002]({{kib-pull}}245002).
* Updates graph visualization to use Elastic Common Schema (ECS) entity fields for actor and target identification [#243711]({{kib-pull}}243711).
* Improves the graph investigation feature by introducing new popover components for displaying additional node details [#236906]({{kib-pull}}236906).
* Prepares the monitoring entity source CRUD APIs for general availability of privileged user monitoring [#246978]({{kib-pull}}246978).
* Introduces the **Entity summary** section in the entity details flyout [#245532]({{kib-pull}}245532).
* Adds Cloud Connector usage statistics collection for the CSPM and Asset Discovery integrations [#236992]({{kib-pull}}236992),[#240272]({{kib-pull}}240272).
* Improves the reliability of Cloud Security Posture (CSP) data by automatically upgrading outdated Misconfiguration and Vulnerabilities data views to the correct versions [#238547]({{kib-pull}}238547).
* Fixes Cloud Security Posture regressions to ensure AWS, GCP, and Azure cloud providers are all supported [#242592]({{kib-pull}}242592).
* Upgrades the Osquery schema to v5.19.0 and the ECS schema to v9.2.0 [#246005]({{kib-pull}}246005).
* For Osquery live queries, improves {{agent}} selection by evaluating the Osquery component's health status rather than the overall {{agent}} status. This allows you to run queries on {{agents}} where the Osquery integration is functional even when other {{agent}} components are degraded [#239304]({{kib-pull}}239304).
* Allows you to submit live Osquery queries to more than 10,000 {{agents}} [#239536]({{kib-pull}}239536).
* Allows you to load Osquery live query action results for queries that targeted many {{agents}}, which previously failed when the request URL grew too large [#239527]({{kib-pull}}239527).
* Improves the performance of the Osquery **Status** tab when displaying results for queries with more than 10,000 {{agents}} [#240082]({{kib-pull}}240082).
* Adds a file download relative URI to response actions that provide file output [#237713]({{kib-pull}}237713).
* Adds a free-text input option to the `runscript` response action for providing input to the selected script [#239436]({{kib-pull}}239436).
* Displays `runscript` response action output for Microsoft Defender for Endpoint for files up to 4.5 KB [#242441]({{kib-pull}}242441).
* Adds a server configuration setting that allows you to turn off automatic installation of the Endpoint Security ({{elastic-defend}}) rule when creating an {{elastic-defend}} integration policy [#246418]({{kib-pull}}246418).
* Adds UI and API support for process descendants in trusted applications [#236318]({{kib-pull}}236318).
* Adds an `actions` command to {{elastic-defend}} to list all queued response actions or cancel an action by ID.
* Adds the `thumbprint_sha256` field to `code_signature` for process and library events in {{elastic-defend}} on Windows.
* Adds the `desktop_name` field to {{elastic-defend}} on Windows process events to assist with the detection of malicious hidden desktop activity.
* Improves {{elastic-defend}} by integrating two new Event Tracing for Windows (ETW) providers (`Microsoft-Windows-WebIO` and `Microsoft-Windows-WinINet`) to detect malicious HTTP activity.
* Moves the {{elastic-defend}} response actions internal state location. If an unsuccessful {{elastic-defend}} upgrade is rolled back to the previous version, existing pending actions are aborted early.
* Adds service-less (no systemd) install mode for {{elastic-defend}} on Linux. Enable by setting the `ELASTIC_ENDPOINT_NO_SYSTEM_SERVICES=1` environment variable during install.
* Adds the `memory-dump` response action to {{elastic-defend}} on Windows.
* Hardens {{elastic-defend}} on Windows against Bind Filter rebinding attacks.
* Adds a new event capture mode, Quark, to {{elastic-defend}} on Linux.
* Adds DNS events for {{elastic-defend}} on Linux (only supported by eBPF-based event collection).
* Removes the 100 MB file size limit for the {{elastic-defend}} `get-file` response action.
* Adds `entropy` and `header_bytes` fields to Linux file events in {{elastic-defend}}.
* Adds the `size` field to {{elastic-defend}} file events on Linux.
* Optimizes the {{elastic-defend}} kernel driver to collect file and registry access events more efficiently, improving overall system responsiveness and reducing CPU usage.
* Adds script content collection to {{elastic-defend}} on macOS. Use the `advanced.events.script_capture` setting to enable this feature and `advanced.events.script_max_size` to control the maximum size of collected content.
* Improves responsiveness on systems running {{elastic-defend}}.
* Adds an {{elastic-defend}} advanced configuration option to use multiple streams for `get-file` uploads.
* Adds an {{elastic-defend}} advanced configuration option to process multiple `get-file` action uploads in parallel.
* Improves {{elastic-defend}} Tamper Protection error logging to include current policy information when uninstall or upgrade fails due to an invalid uninstall token.
* Reduces the number of I/O operations performed by {{elastic-defend}} for file event enrichment. This reduction is more pronounced when Ransomware Protection is not in use.
* Enables {{elastic-defend}} to save response action upload progress and continue after restart.
* Improves the {{elastic-defend}} startup log to explain unsigned policy details.
* Reduces the performance impact of file copy and move operations involving Windows Offloaded Data Transfer while {{elastic-defend}} is installed.
* Adds an {{elastic-defend}} policy advanced setting to maintain a minimum amount of free disk space.
* Reduces {{elastic-defend}} CPU usage when suppressing activity from trusted applications on Windows. This might be especially noticeable in applications that are JIT-heavy like PowerShell and .NET.
* Improves {{elastic-defend}} visibility into image load events in mixed-architecture scenarios, such as during .NET library loading when the library and main executable might use different architectures. This only applies to Windows 10, version 1709 and later.
* Refactors {{elastic-defend}} Windows file scanning behavior to reduce the risk of file sharing conflicts with other applications and improve the reliability of malware-on-write and event enrichments that rely on file contents such as code signatures and imphashes.
* Improves the accuracy of thread CPU usage reported in {{elastic-defend}} metrics documents.
* Further reduces {{elastic-defend}} behavioral protection CPU usage for trusted applications.


### Fixes [elastic-security-9.3.0-fixes]
* Fixes a bug where a lack of legacy signals data would cause the Signals Migration Status API to return an error [#237552]({{kib-pull}}237552).
* Fixes an issue where the rule settings pop-up remained open after clicking **Save** when enabling or disabling auto gap fill [#247678]({{kib-pull}}247678).
* Fixes the **Get started** page visibility for users with read-only privileges for rules [#247355]({{kib-pull}}247355).
* Fixes a display issue with filters on the **MITRE ATT&CK® coverage** page [#246794]({{kib-pull}}246794).
* Limits the retrieval of gap summaries to 100 `rule_id`s [#245924]({{kib-pull}}245924).
* Fixes threshold rule logic when no "group by" fields are defined [#241022]({{kib-pull}}241022).
* Fixes an issue where alerts generated by threshold rules had non-functional source event links [#238707]({{kib-pull}}238707).
* Fixes multiple issues searching installed rules by allowing partial matches on rule name and improving special character support [#237496]({{kib-pull}}237496).
* Updates the icon that is shown when alert suppression is not available because of insufficient license [#247964]({{kib-pull}}247964).
* Truncates long text in the **Value** column in the value list modal [#246679]({{kib-pull}}246679).
* Ignores `resource_already_exists_exception` for value list creation hook [#243642]({{kib-pull}}243642).
* Fixes an infinite loop bug related to bootstrapping value list resources [#241052]({{kib-pull}}241052).
* Fixes an issue where rule exception operators could not be cleared when editing a rule exception [#236051]({{kib-pull}}236051).
* Fixes an issue where the Security AI Assistant chat completion API didn't use an associated conversation's system prompt [#248020]({{kib-pull}}248020).
* Updates the configuration validation logic for the Google Gemini connector [#245647]({{kib-pull}}245647).
* Fixes an issue with the Security AI Assistant **Regenerate** button [#241240]({{kib-pull}}241240).
* Fixes Security AI Assistant index entry form field suggestions for nested and multi-fields [#239453]({{kib-pull}}239453).
* Prioritizes connector `defaultModel` over stored conversation model [#237947]({{kib-pull}}237947).
* Fixes an issue where attack discovery schedules couldn't be created with Case as the connector type [#239748]({{kib-pull}}239748).
* Clears the rule selection on the **Translated rules** page after successfully updating an index pattern [#239245]({{kib-pull}}239245).
* Fixes an issue where users couldn't change the migration when translating rules [#238679]({{kib-pull}}238679).
* Fixes an issue where the `createdBy` field in the notes filter didn't use exact matching [#247351]({{kib-pull}}247351).
* Changes the placement of **Migrations** and **Inventory** items in the {{elastic-sec}} navigation menu [#247002]({{kib-pull}}247002).
* Fixes an issue where Timeline actions appeared in the Alerts table bulk actions menu without proper privileges [#246150]({{kib-pull}}246150).
* Fixes an issue where the visual event analyzer preview didn't use the same data view that was selected in the analyzer [#246081]({{kib-pull}}246081).
* Fixes an issue where the visual event analyzer rendered before the data view was ready [#245712]({{kib-pull}}245712).
* Fixes an issue where the **Threat intelligence** section in the alert details flyout didn't display multiple values [#245449]({{kib-pull}}245449).
* Fixes an issue where clicking a rule link from an alert flyout inside a saved Timeline also opened the Timeline [#242313]({{kib-pull}}242313).
* Fixes a UI issue when displaying {{esql}} queries in Timeline full screen mode [#242027]({{kib-pull}}242027).
* Allows saving a Timeline with an adhoc data view [#240537]({{kib-pull}}240537).
* Fixes an issue where the onboarding integrations list wasn't fetched for all pages [#239709]({{kib-pull}}239709).
* Fixes an issue where the names of the `Security solution default` and `Security solution alerts` data views were displayed incorrectly [#238354]({{kib-pull}}238354).
* Fixes an issue where the graph visualization didn't render when switching tabs or refreshing the page [#238038]({{kib-pull}}238038).
* Fixes controls on the **Alerts** page [#236756]({{kib-pull}}236756).
* Adds support for multiple values in the Indicator details flyout's **Table** tab [#236110]({{kib-pull}}236110).
* Fixes a pagination issue with the data table on the **Indicators** page [#241108]({{kib-pull}}241108).
* Fixes alert grouping in the alerts table [#237911]({{kib-pull}}237911).
* Fixes an issue where the "Top <_n_>" popover stayed open after opening the create case flyout [#242045]({{kib-pull}}242045).
* Fixes an issue where entity user and host names were not escaped in URLs, which resulted in invalid URLs [#247707]({{kib-pull}}247707).
* Fixes an issue where special characters in {{esql}} queries for risk scoring were not handled correctly [#247060]({{kib-pull}}247060).
* Fixes an issue where the **Entity summary** section in the entity details flyout showed incorrect vulnerabilities data [#246889]({{kib-pull}}246889).
* Updates Active Directory matchers to use SID-based privileged groups for privileged user monitoring [#246763]({{kib-pull}}246763).
* Fixes an issue where the **Integrations** section on the privileged user monitoring **Manage data sources** page always showed a "no data stream" warning [#246180]({{kib-pull}}246180).
* Fixed the entity risk engine custom filters so that user-supplied KQL syntax isn't double-negated [#242171]({{kib-pull}}242171).
* Fixes the entity flyout **Risk contributions** tab link [#241153]({{kib-pull}}241153).
* Fixes an issue where the entity popover showed a missing `EngineMetadata.type` error [#239661]({{kib-pull}}239661).
* Fixes an issue where the CSPM and Asset Discovery integrations failed to collect data when using agent-based deployment [#241390]({{kib-pull}}241390).
* Standardizes how to log errors [#245030]({{kib-pull}}245030).
* Adds encoding for CloudFormation URL parameters [#242365]({{kib-pull}}242365).
* Fixes a react-query key collision that occurred when two different integration lookups shared the same key [#240517]({{kib-pull}}240517).
* Sanitizes lookup names for index creation [#240228]({{kib-pull}}240228).
* Introduces a check for {{fleet}} `read` permissions before loading in the integrations data source component [#239122]({{kib-pull}}239122).
* Fixes an issue causing "missing authentication credentials" warnings in `TelemetryConfigWatcher` and `PolicyWatcher`, reducing unnecessary warning log entries in the `securitySolution` plugin [#237796]({{kib-pull}}237796).
* Fixes an issue where the response actions API (for {{elastic-defend}} agent types) didn't send actions to more than 10 agents [#243387]({{kib-pull}}243387).
* Updates response action response codes [#240420]({{kib-pull}}240420).
* Fixes endpoint artifacts spaces migration to ensure all artifacts are processed [#238740]({{kib-pull}}238740).
* Updates the datafeed of the `packetbeat_dns_tunneling` {{elastic-sec}} {{ml}} job to include runtime mappings [#249317]({{kib-pull}}249317).
* Fixes an issue where {{elastic-defend}} on Windows could log a warning about "Quarantine directory failed validation due to ACL or file attribute change" for empty removable media drives such as optical drives.
* Fixes an issue in {{elastic-defend}} that could result in delayed or missing malware-on-write alerts.
* Fixes an issue where {{elastic-defend}} upgrades and uninstallations could fail on busy systems.
* Fixes an issue in {{elastic-defend}} on Windows where Mark of the Web parsing incorrectly handled file origin information ending with a `\0`.
* Prevents unnecessary policy reloads in {{elastic-defend}} when only the overall config version changes.
* Fixes a bug where {{elastic-defend}} for Linux could fail to bootstrap with {{agent}}.
* Fixes an issue that could prevent {{elastic-defend}} from properly handling upgrades when Tamper Protection is enabled.
* Fixes an issue in {{elastic-defend}} that could cause `get-file` and `execute` response actions to start failing after many are issued with a single running instance of {{elastic-defend}}.
* Improves {{elastic-defend}} detection of file rename operations that occur on Windows over SMB.
* Fixes a bug in {{elastic-defend}} on Linux where the legacy network event source (debugfs/kprobes) would miss network events for non-blocking connect calls.
* Fixes multiple {{elastic-defend}} issues in malware protection for Linux where a deadlock could sometimes occur when containers and autofs were both active.
* For {{elastic-defend}} on Linux, reduces the occurrence of policy failures related to malware protection system deadlock avoidance.
* Improves {{elastic-defend}} on Linux to better handle fanotify events from different mount namespaces.
* Fixes a bug in {{elastic-defend}} Linux event collection where some long-running processes were not enriched.


## 9.2.8 [elastic-security-9.2.8-release-notes]

### Fixes [elastic-security-9.2.8-fixes]

* Fixes an issue where the search bar on the **Alerts** tab of the rule details page overlapped the alerts table in full screen mode [#260315]({{kib-pull}}260315).
* Fixes a denial-of-service risk in Timeline bulk export by validating the number of Timeline IDs (up to 1,000), deduplicating IDs, and bounding enrichment work [#260265]({{kib-pull}}260265).
* Fixes an issue where notes not associated with a saved Timeline could appear on the **Notes** tab while investigating in Timeline, including for draft Timelines [#259658]({{kib-pull}}259658).
* Fixes incorrect alert counting for indicator match detection rules when a page of source documents matches no indicators, so max-alerts warnings display correctly [#259199]({{kib-pull}}259199).
* Fixes an issue in {{elastic-defend}} where `ignored_filesystems` did not take effect when the same filesystem appeared in both the monitored and ignored configuration lists.

## 9.2.7 [elastic-security-9.2.7-release-notes]

### Features and enhancements [elastic-security-9.2.7-features-enhancements]
* Adds a callout and badge to the visual event analyzer in the alert details flyout to indicate when cold and frozen data tiers are excluded from analyzer queries [#257015]({{kib-pull}}257015).
* Adds an advanced setting to exclude cold and frozen data tiers from prevalence queries in the alert details flyout, improving load performance [#257011]({{kib-pull}}257011).
* Improves the reliability of {{elastic-defend}}'s malware-on-write detection.

### Fixes [elastic-security-9.2.7-fixes]
* Fixes an issue where the alert details flyout persisted after navigating away from {{elastic-sec}} [#256001]({{kib-pull}}256001).
* Fixes an issue where the visual event analyzer preview could fetch data with incorrect indices before the {{data-source}} was fully loaded [#255400]({{kib-pull}}255400).
* Fixes an issue where visual event analyzer queries could return cached results for incorrect indices [#255396]({{kib-pull}}255396).
* Fixes an issue where the visual event analyzer did not display in the alert details flyout in certain {{data-source}} configurations [#255182]({{kib-pull}}255182).
* Enables the `defaultModel` setting for the Azure OpenAI connector to support APIM endpoints [#253577]({{kib-pull}}253577).
* Fixes an issue where the legacy `rules/prepackaged` endpoints returned 500 errors on Basic licenses when processing prebuilt rule packages that include {{ml}} rules [#253574]({{kib-pull}}253574).
* Adds support for timestamp overrides to Timeline at the {{data-source}} level, allowing Timeline to use the {{data-source}}'s configured timestamp field instead of `@timestamp` [#251827]({{kib-pull}}251827).
* Fixes an issue that would cause hotfix builds of {{elastic-defend}} to incorrectly report their version in Windows Security Center.


## 9.2.6 [elastic-security-9.2.6-release-notes]

### Features and enhancements [elastic-security-9.2.6-features-enhancements]
* Adds a new **Overview** tab to the rule details page [#251662]({{kib-pull}}251662).
* Adds a `region` field to the Amazon Bedrock connector [#252960]({{kib-pull}}252960), [#252956]({{kib-pull}}252956).
* Improves Automatic Migration performance by reducing the number of {{es}} calls when updating field mappings [#252431]({{kib-pull}}252431).
* Updates the `fast-xml-parser` package dependency to version 5.3.4 [#251644]({{kib-pull}}251644).

### Fixes [elastic-security-9.2.6-fixes]
* Improves the performance of bulk rule deletion [#253116]({{kib-pull}}253116).
* Fixes accessibility issues in the Security AI Assistant confirm delete modal [#251962]({{kib-pull}}251962).
* Adds optional field indicators to the OpenAI connector configuration [#251857]({{kib-pull}}251857).
* Fixes an accessibility issue with a missing label in the Security AI Assistant flyout [#251656]({{kib-pull}}251656).
* Fixes an issue where detection rules APIs didn't properly validate endpoint response actions [#251352]({{kib-pull}}251352).
* Fixes an issue where the `os_types` field was not saved when creating an exception list [#250279]({{kib-pull}}250279).
* Fixes a DNS parsing bug in Linux versions of {{elastic-defend}} that could result in crashes.


## 9.2.5 [elastic-security-9.2.5-release-notes]

### Features and enhancements [elastic-security-9.2.5-features-enhancements]
* Further reduces {{elastic-defend}} behavioral protection CPU usage for trusted applications.

### Fixes [elastic-security-9.2.5-fixes]
* Improves the stability of the **Add Elastic rules** page on deployments with low RAM configurations [#248259]({{kib-pull}}248259).
* Fixes an issue in {{elastic-defend}} on Windows that could reduce the detection efficacy of malware-on-write.
* Fixes an issue where {{elastic-defend}} on Windows could log a warning about "Quarantine directory failed validation due to ACL or file attribute change" for empty removable media drives such as optical drives.
* Fixes an issue in {{elastic-defend}} that could cause the system to lock up for up to several minutes during {{elastic-endpoint}} uninstallation or upgrade.

## 9.2.4 [elastic-security-9.2.4-release-notes]

### Features and enhancements [elastic-security-9.2.4-features-enhancements]
* Updates MITRE ATT&CK mappings to `v18.1` [#246770]({{kib-pull}}246770).
* Adds a server configuration setting that allows you to disable the automatic installation of the Endpoint Security ({{elastic-defend}}) rule when creating an {{elastic-defend}} integration policy [#246418]({{kib-pull}}246418).
* Persists the visual event analyzer's data view selection in local storage [#245002]({{kib-pull}}245002).
* Improves responsiveness on systems running {{elastic-defend}}.
* Optimizes the {{elastic-defend}} kernel driver to collect file and registry access events more efficiently, improving overall system responsiveness and reducing CPU usage.

### Fixes [elastic-security-9.2.4-fixes]
* Fixes an issue where the Security AI Assistant chat completion API didn't use an associated conversation's system prompt [#248020]({{kib-pull}}248020).
* Fixes an issue where entity user and host names were not escaped in URLs, which resulted in invalid URLs [#247707]({{kib-pull}}247707).
* Fixes an issue where the `createdBy` field in the notes filter didn't use exact matching [#247351]({{kib-pull}}247351).
* Fixes an issue where special characters in {{esql}} queries for risk scoring were not handled correctly [#247060]({{kib-pull}}247060).
* Fixes a display issue with filters on the **MITRE ATT&CK® coverage** page [#246794]({{kib-pull}}246794).
* Fixes an issue where the **Integrations** section on the privileged user monitoring **Manage data sources** page always showed a "no data stream" warning [#246180]({{kib-pull}}246180).
* Fixes an issue where Timeline actions appeared in the Alerts table bulk actions menu without proper privileges [#246150]({{kib-pull}}246150).
* Fixes an issue where the visual event analyzer preview didn't use the same data view that was selected in the analyzer [#246081]({{kib-pull}}246081).
* Fixes an issue where the visual event analyzer rendered before the data view was ready [#245712]({{kib-pull}}245712).
* Fixes an issue where the **Threat intelligence** section in the alert details flyout didn't display multiple values [#245449]({{kib-pull}}245449).
* Fixes an issue in {{elastic-defend}} Windows on-write malware scanning that could cause sharing violations when other applications attempted to open files.
* Fixes an issue where {{elastic-defend}} upgrades and uninstallations could fail on busy systems.
* Fixes an issue in {{elastic-defend}} on Windows where Mark of the Web parsing incorrectly handled file origin information ending with a `\0`.
* For {{elastic-defend}} on Linux, reduces the occurrence of policy failures related to malware protection system deadlock avoidance.
* Fixes an issue in {{elastic-defend}} that could result in delayed or missing malware-on-write alerts.
* Fixes a bug in {{elastic-defend}} on Windows that could sometimes result in `KERNEL_AUTO_BOOST_LOCK_ACQUISITION_WITH_RAISED_IRQL` or `PAGE_FAULT_IN_NONPAGED_AREA` bugchecks when [Offloaded Data Transfer (ODX)](https://learn.microsoft.com/en-us/windows-hardware/drivers/storage/offloaded-data-transfer) was used to copy files.  This regression was introduced in {{elastic-defend}} versions 8.19.8, 9.1.8, and 9.2.2.


## 9.2.3 [elastic-security-9.2.3-release-notes]

### Features and enhancements [elastic-security-9.2.3-features-enhancements]
* Shows session view in full height [#245888]({{kib-pull}}245888).
* Shows analyzer in full height [#245857]({{kib-pull}}245857).
* Hardens {{elastic-defend}} on Windows against Bind Filter rebinding attacks.
* Adds `process.group_leader.pid` and `process.session_leader.pid` to {{elastic-defend}} MacOS process exec events.
* Improves general system responsiveness while {{elastic-defend}} is installed.
* Reduces the number of I/O operations performed by {{elastic-defend}} for file event enrichment.  This reduction is more pronounced when Ransomware Protection is not in use.

### Fixes [elastic-security-9.2.3-fixes]
* Standardizes how to log errors [#245030]({{kib-pull}}245030).
* Fixes a bug for {{elastic-defend}} on Linux, where the legacy network event source (debugfs/kprobes) would miss network events for non-blocking connect calls.

## 9.2.2 [elastic-security-9.2.2-release-notes]

### Features and enhancements [elastic-security-9.2.2-features-enhancements]
* Improves the alert details flyout by saving the selected threat intelligence time to local storage [#243571]({{kib-pull}}243571).
* Improves the alert details flyout by saving the selected prevalence time to local storage [#243543]({{kib-pull}}243543).

### Fixes [elastic-security-9.2.2-fixes]
* Fixes response actions API (for {{elastic-defend}} agent types) not sending action to more than 10 agents [#243387]({{kib-pull}}243387).
* Fixes an issue where clicking a rule link from an alert flyout inside a saved Timeline would also open the Timeline [#242313]({{kib-pull}}242313).
* Fixes an issue where the "Top <_n_>" popover stayed open after opening the create case flyout. It now closes automatically when the flyout opens [#242045]({{kib-pull}}242045).
* Fixes a UI issue when displaying {{esql}} queries in Timeline full screen mode [#242027]({{kib-pull}}242027).
* Allows saving a Timeline with an adhoc data view [#240537]({{kib-pull}}240537).
* Fixes an issue where alerts generated by threshold rules had non-functional source event links [#238707]({{kib-pull}}238707).
* Ignores `resource_already_exists_exception` for value list creation hook [#243642]({{kib-pull}}243642).
* Adds support for multiple values in the Indicator details flyout's **Table** tab [#236110]({{kib-pull}}236110).
* Prevents unnecessary policy reloads in {{elastic-defend}} when only the overall config version changes.
* Fixes a bug where {{elastic-defend}} for Linux could fail to bootstrap with {{agent}}.
* Generates already mounted events for device control.

## 9.2.1 [elastic-security-9.2.1-release-notes]

### Features and enhancements [elastic-security-9.2.1-features-enhancements]

* Improves the startup log in {{elastic-defend}} to explain the details of unsigned policy.
* Improves the accuracy of thread CPU usage reported in {{elastic-defend}} metrics documents.

### Fixes [elastic-security-9.2.1-fixes]
* Fixes an issue where the CSPM and Asset Discovery integrations failed to collect data when using agent-based deployment [#241390]({{kib-pull}}241390).
* Fixes a react-query key collision that occurred when two different integration lookups shared the same key, which could cause errors when navigating between pages [#240517]({{kib-pull}}240517).
* Fixes multiple issues searching installed rules by allowing partial matches on rule name and improving special character support [#237496]({{kib-pull}}237496).
* Fixes an {{elastic-defend}} bug in Linux event collection where some long-running processes were not enriched.
* Fixes multiple {{elastic-defend}} issues in malware protection for Linux where a deadlock could sometimes occur when containers and autofs were both active.
* Fixes an {{elastic-defend}} issue that could cause the `get-file` and `execute` response actions to fail after many were issued with a single running instance of {{elastic-defend}}
* Improves {{elastic-defend}} detection of file rename operations on Windows when performed over Server Message Block (SMB).
* Fixes an {{elastic-defend}} issue on Windows where the `code_signature.thumbprint_sha256` field was missing under process and DLL events for certain event types.


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
* Adds firewall anti-tamper plug-in to protect {{elastic-endpoint}} processes against network blocking through Windows Firewall.
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

* Fixes a bug where a lack of legacy signals data would cause the Signals Migration Status API to return an error [#237552]({{kib-pull}}237552).
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
* Fixes issues that could sometimes cause crashes of the {{elastic-defend}} user-mode process on busy Windows systems.
* Adds support in {{elastic-defend}} for installing eBPF event probes on Linux endpoints when cgroup2 is mounted in a non-standard location or not mounted at all.
* Adds support in {{elastic-defend}} for installing eBPF probes on Linux endpoints when taskstats is compiled out of the kernel.
* Fixes an issue in {{elastic-defend}} where Linux network events could have source and destination bytes swapped.
* Fixes a bug where Linux capabilities were included in {{elastic-endpoint}} network events despite being disabled.
* Fixes an issue where {{elastic-defend}} would incorrectly calculate throughput capacity when sending documents to output. This may have limited event throughput on extremely busy endpoints.
* Improves the reliability of local {{elastic-defend}} administrative shell commands. In rare cases, a command could fail to execute due to issues with interprocess communication.
* Fixes an issue in {{elastic-defend}} where host isolation could auto-release incorrectly. Host isolation now only releases when {{elastic-endpoint}} becomes orphaned. Intermittent {{agent}} connectivity changes no longer alter the host isolation state.
* Fixes a bug in {{elastic-defend}} where Linux endpoints would report `process.executable` as a relative, instead of absolute, path.
* Fixes an issue which could cause {{elastic-defend}} to improperly report success when self-healing rollback attempted to terminate a process with an active debugger on Windows.
* Fixes an issue in {{elastic-defend}} installation logging where only the first character of install paths (usually 'C') was logged.
* Fixes an issue to improve reliability of health status reporting between {{elastic-endpoint}} and {{agent}}.
* Fixes a race condition in {{elastic-defend}} that occasionally resulted in corrupted process command lines on Windows. This could cause incorrect values for `process.command_line`, `process.args_count`, and `process.args`, leading to false positives.
* Fixes an issue in {{elastic-defend}} that could result in a crash if a specified {{ls}} output configuration contained a certificate that couldn't be parsed.
* Fixes CVE-2025-37735 ([ESA-2025-23](https://discuss.elastic.co/t/elastic-defend-8-19-6-9-1-6-and-9-2-0-security-update-esa-2025-23/383272)) in {{elastic-defend}} on Windows which could allow a low-privilege attacker to delete arbitrary files on the system and potentially escalate privileges to SYSTEM. Windows 11 24H2 includes changes which make this issue harder to exploit.


## 9.1.10 [elastic-security-9.1.10-release-notes]

### Features and enhancements [elastic-security-9.1.10-features-enhancements]
* Updates MITRE ATT&CK mappings to `v18.1` [#246770]({{kib-pull}}246770).

### Fixes [elastic-security-9.1.10-fixes]
* Fixes an issue where the Security AI Assistant chat completion API didn't use an associated conversation's system prompt [#248020]({{kib-pull}}248020).
* Fixes an issue where entity user and host names were not escaped in URLs, which resulted in invalid URLs [#247707]({{kib-pull}}247707).
* Fixes an issue where the `createdBy` field in the notes filter didn't use exact matching [#247351]({{kib-pull}}247351).
* Fixes a display issue with filters on the **MITRE ATT&CK® coverage** page [#246794]({{kib-pull}}246794).
* Fixes an issue where Timeline actions appeared in the Alerts table bulk actions menu without proper privileges [#246150]({{kib-pull}}246150).
* Limits the detection rule execution gaps API for retrieving gap summaries to 100 `rule_id`s per request [#245924]({{kib-pull}}245924).
* Fixes an issue where the **Threat intelligence** section in the alert details flyout didn't display multiple values [#245449]({{kib-pull}}245449).
* Fixes an issue where {{elastic-defend}} upgrades and uninstallations could fail on busy systems.
* Fixes an issue in {{elastic-defend}} on Windows where Mark of the Web parsing incorrectly handled file origin information ending with a `\0`.
* For {{elastic-defend}} on Linux, reduces the occurrence of policy failures related to malware protection system deadlock avoidance.
* Fixes a bug in {{elastic-defend}} on Windows that could sometimes result in `KERNEL_AUTO_BOOST_LOCK_ACQUISITION_WITH_RAISED_IRQL` or `PAGE_FAULT_IN_NONPAGED_AREA` bugchecks when [Offloaded Data Transfer (ODX)](https://learn.microsoft.com/en-us/windows-hardware/drivers/storage/offloaded-data-transfer) was used to copy files.  This regression was introduced in {{elastic-defend}} versions 8.19.8, 9.1.8, and 9.2.2.


## 9.1.9 [elastic-security-9.1.9-release-notes]

### Features and enhancements [elastic-security-9.1.9-features-enhancements]
* Shows session view in full height [#245888]({{kib-pull}}245888).
* Shows analyzer in full height [#245857]({{kib-pull}}245857).
* Hardens {{elastic-defend}} on Windows against Bind Filter rebinding attacks.
* Improves general system responsiveness while {{elastic-defend}} is installed.

### Fixes [elastic-security-9.1.9-fixes]
* Standardizes how to log errors [#245030]({{kib-pull}}245030).
* Fixes an issue that could prevent {{elastic-defend}} from properly handling upgrades when Tamper Protection is enabled.
* {{elastic-defend}} no longer reloads its policy if nothing has functionally changed from the previous policy.
* For Linux {{elastic-defend}}, fixes a bug where the legacy network event source (debugfs/kprobes) would miss network events for non-blocking connect calls.

## 9.1.8 [elastic-security-9.1.8-release-notes]

### Features and enhancements [elastic-security-9.1.8-features-enhancements]
* Improves the alert details flyout by saving the selected threat intelligence time to local storage [#243571]({{kib-pull}}243571).
* Ignores `resource_already_exists_exception` for value list creation hook [#243642]({{kib-pull}}243642).

### Fixes [elastic-security-9.1.8-fixes]
* Fixes an issue where the "Top <_n_>" popover stayed open after opening the create case flyout. It now closes automatically when the new case flyout opens [#242045]({{kib-pull}}242045).
* Fixes a UI issue when displaying {{esql}} queries in Timeline full screen mode [#242027]({{kib-pull}}242027).
* Prevents unnecessary policy reloads in {{elastic-defend}} when only the overall config version changes.
* Fixes a bug where {{elastic-defend}} for Linux could fail to bootstrap with {{agent}}.


## 9.1.7 [elastic-security-9.1.7-release-notes]

### Features and enhancements [elastic-security-9.1.7-features-enhancements]
* Improves the reliability of Cloud Security Posture (CSP) data by automatically upgrading outdated Misconfiguration and Vulnerabilities data views to the correct versions [#238547]({{kib-pull}}238547).
* Adds more {{elastic-defend}} options to the {{ls}} output, allowing for finer control.
* Improves the accuracy of thread CPU usage reported in {{elastic-defend}} metrics documents.


### Fixes [elastic-security-9.1.7-fixes]
* Fixes entity flyout **Risk contributions** tab link [#241153]({{kib-pull}}241153).
* Fixes a pagination issue with the data table on the **Indicators** page [#241108]({{kib-pull}}241108).
* Fixes a react-query key collision that occurred when two different integration lookups shared the same key, which could cause errors when navigating between pages [#240517]({{kib-pull}}240517).
* Fixes multiple issues searching installed rules by allowing partial matches on rule name and improving special character support [#237496]({{kib-pull}}237496).
* Fixes an issue where rule exception operators could not be cleared when editing a rule exception [#236051]({{kib-pull}}236051).
* Fixes an {{elastic-defend}} issue on Linux by preventing unnecessary locking within malware protection to avoid invalid watchdog firings.
* Fixes issues that could sometimes cause crashes of the {{elastic-defend}} user-mode process on busy Windows systems.
* Fixes multiple {{elastic-defend}} issues in malware protection for Linux where a deadlock could sometimes occur when containers and autofs were both active.
* Fixes CVE-2025-37735 ([ESA-2025-23](https://discuss.elastic.co/t/elastic-defend-8-19-6-9-1-6-and-9-2-0-security-update-esa-2025-23/383272)) in {{elastic-defend}} on Windows which could allow a low-privilege attacker to delete arbitrary files on the system and potentially escalate privileges to SYSTEM. Windows 11 24H2 includes changes which make this issue harder to exploit.
* Fixes an {{elastic-defend}} bug in Linux event collection where some long-running processes were not enriched.
* Fixes an {{elastic-defend}} issue that could cause the `get-file` and `execute` response actions to fail after many were issued with a single running instance of {{elastic-defend}}.


## 9.1.6 [elastic-security-9.1.6-release-notes]

### Features and enhancements [elastic-security-9.1.6-features-enhancements]
* Adds the `customized_fields` and `has_base_version` fields to the `rule_source` object schema  [#234793]({{kib-pull}}234793).
* Implements CDR Data View versioning and migration logic [#238547]({{kib-pull}}238547).

### Fixes [elastic-security-9.1.6-fixes]
* Fixes {{elastic-endpoint}} artifacts spaces migration to ensure all artifacts are processed [#238740]({{kib-pull}}238740).
* Fixes an issue causing "missing authentication credentials" warnings in `TelemetryConfigWatcher` and `PolicyWatcher`, reducing unnecessary warning log entries in the `securitySolution` plugin [#237796]({{kib-pull}}237796).
* Prioritizes connector `defaultModel` over stored conversation model [#237947]({{kib-pull}}237947).


## 9.1.5 [elastic-security-9.1.5-release-notes]

### Features and enhancements [elastic-security-9.1.5-features-enhancements]
* Adds an {{elastic-defend}} option to remediate orphaned state by attempting to start Elastic Agent service.
* Increases the throughput of {{elastic-defend}} Logstash connections by increasing the maximum size it can upload at once.
* Improves reliability and accuracy of reporting of the {{elastic-defend}}'s {{es}} connection.

### Fixes [elastic-security-9.1.5-fixes]
* Fixes a bug where a lack of legacy signals data would cause the Signals Migration Status API to return an error [#237552]({{kib-pull}}237552).
* Fixes browser fields caching to use the `dataView` ID instead of the index pattern [#234381]({{kib-pull}}234381).
* Removes `null` in confirmation dialog when bulk editing index patterns for rules [#236572]({{kib-pull}}236572).
* Fixes the URL passed to detection rule actions using the `{{context.results_link}}` placeholder [#236067]({{kib-pull}}236067).
* Fixes system prompt updates from the Conversations tab in AI Assistant [#234812]({{kib-pull}}234812).
* Fixes an issue in the Highlighted fields table in the alert details flyout [#234222]({{kib-pull}}234222).
* Fixes an issue in rule exceptions to include the `matches` operator only for supported fields [#233127]({{kib-pull}}233127).
* Adds support in {{elastic-defend}} for installing eBPF event probes on Linux endpoints when cgroup2 is mounted in a non-standard location or not mounted at all.
* Adds support in {{elastic-defend}} for installing eBPF probes on Linux endpoints when taskstats is compiled out of the kernel.
* Fixes an issue in {{elastic-defend}} where Linux network events could have source and destination bytes swapped.
* Removes `.process.thread.capabilities.permitted` and `.process.thread.capabilities.effective` from Linux network events in {{elastic-defend}}.
* Fixes an issue in {{elastic-defend}} where host isolation could auto-release incorrectly. Host isolation now only releases when {{elastic-endpoint}} becomes orphaned. Intermittent {{agent}} connectivity changes no longer alter the host isolation state.
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
* Expands CVE ID search to all search parameters, not only names [#221099]({{kib-pull}}221099).
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
* Fixes the URL passed to detection rule actions using the `{{context.results_link}}` placeholder [#236067]({{kib-pull}}236067).
* Adds support in {{elastic-defend}} for installing eBPF probes on Linux endpoints when taskstats is compiled out of the kernel.
* Fixes an issue in {{elastic-defend}} where Linux network events could have source and destination bytes swapped.
* Removes `.process.thread.capabilities.permitted` and `.process.thread.capabilities.effective` from Linux network events in {{elastic-defend}}.
* Fixes an issue in {{elastic-defend}} where host isolation could auto-release incorrectly. Host isolation now only releases when {{elastic-endpoint}} becomes orphaned. Intermittent {{agent}} connectivity changes no longer alter the host isolation state.
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

