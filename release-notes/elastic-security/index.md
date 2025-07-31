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

## 9.0.4 [elastic-security-9.0.4-release-notes]

### Features and enhancements [elastic-security-9.0.4-features-enhancements]
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

