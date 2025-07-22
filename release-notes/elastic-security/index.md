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

