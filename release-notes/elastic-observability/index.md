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