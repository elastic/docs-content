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

% Release notes include only features, enhancements, and fixes. Add breaking changes, deprecations, and known issues to the applicable release notes sections.

% ## version.next [elastic-security-X.X.X-notes]

% ### Features and enhancements [elastic-security-X.X.X-features-enhancements]
% *

% ### Fixes [elastic-security-X.X.X-fixes]

% *

## 9.0.2 [elastic-security-9.0.2-release-notes]

### Features and enhancements [elastic-security-9.0.2-features-enhancements]
There are no new features or enhancements.

### Fixes [elastic-security-9.0.2-fixes]
* Fixes a bug that caused an error message to appear when you changed entity asset criticality from the entity flyout [#219858]({{kib-pull}}219858)
* Fixes a bug in {{elastic-defend}} 8.16.0 where {{elastic-endpoint}} would incorrectly report some files as being `.NET`.

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

