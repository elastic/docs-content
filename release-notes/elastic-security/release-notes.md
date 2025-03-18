---
navigation_title: "Elastic Security"
mapped_pages:
  - https://www.elastic.co/guide/en/security/master/release-notes-header-9.0.0.html
  - https://www.elastic.co/guide/en/security/current/release-notes.html
---
# {{elastic-sec}} release notes [elastic-security-release-notes]

Review the changes, fixes, and more in each version of {{elastic-sec}}.

To check for security updates, go to [Security announcements for the Elastic stack](https://discuss.elastic.co/c/announcements/security-announcements/31).

% Release notes include only features, enhancements, and fixes. Add breaking changes, deprecations, and known issues to the applicable release notes sections.

% ## version.next [elastic-security-next-release-notes]
% **Release date:** Month day, year

% ### Features and enhancements [elastic-security-next-features-enhancements]
% *

% ### Fixes [elastic-security-next-fixes]
% *

## 9.0.0 [elastic-security-900-release-notes]
**Release date:** April 2, 2025

### Features and enhancements [elastic-security-900-features-enhancements]
* Enables Automatic Import to accept CEL log samples [#206491]({{kib-pull}}206491)
* Applies the latest Elastic UI framework (EUI) to {{elastic-sec}} features [#204007]({{kib-pull}}204007) and [#204908]({{kib-pull}}204908)
* Adds the option to view {es} queries that run during rule execution for threshold, custom query, and {{ml}} rules [#203320]({{kib-pull}}203320)
* Enables Automatic Import to accept CEL log samples [#206491]({{kib-pull}}206491)
* Applies the latest Elastic UI framework (EUI) to {{elastic-sec}} features [#204007]({{kib-pull}}204007) and [#204908]({{kib-pull}}204908)
* Adds the option to view {{es}} queries that run during rule execution for threshold, custom query, and {{ml}} rules [#203320]({{kib-pull}}203320)
* Enhances Automatic Import by including setup and troubleshooting documentation for each input type that's selected in the readme [#206477]({{kib-pull}}206477)
* Allows users to include `closed` alerts in risk score calculations [#201909]({{kib-pull}}201909)
* Adds the ability to continue to the Entity Analytics dashboard when there is no data [#201363]({{kib-pull}}201363)
* Modifies the privilege-checking behavior during rule execution. Now, only read privileges of extant indices are checked during rule execution [#177658]({{kib-pull}}177658)


### Fixes [elastic-security-900-fixes]
* Ensures that table actions use standard colors [#207743]({{kib-pull}}207743)
* Fixes a bug with the **Save and continue** button on a {{fleet}} form [#211563]({{kib-pull}}211563)
