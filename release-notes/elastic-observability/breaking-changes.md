---
navigation_title: "Elastic Observability"
---

# Elastic {{observability}} breaking changes [elastic-observability-breaking-changes]
Breaking changes can impact your Elastic applications, potentially disrupting normal operations. Before you upgrade, carefully review the Elastic {{observability}} breaking changes and take the necessary steps to mitigate any issues. 

To learn how to upgrade, check [Upgrade](/deploy-manage/upgrade.md).

% ## Next version [elastic-observability-nextversion-breaking-changes]
% **Release date:** Month day, year

% ::::{dropdown} Title of breaking change 
% Description of the breaking change.
% For more information, check [PR #](PR link).
% **Impact**<br> Impact of the breaking change.
% **Action**<br> Steps for mitigating deprecation impact.
% ::::

% ## 9.0.0 [elastic-observability-900-breaking-changes]
% **Release date:** April 2, 2025

::::{dropdown} Profiling now defaults to 19Hz sampling frequency
For more information, check ({{kibana-pull}}202278[#202278]).
::::

::::{dropdown} Removed log stream and settings pages
The following have been removed:
* Logs Stream
* Logs settings page
* Logs stream panel in Dashboards

For more information, check ({{kibana-pull}}203996[#203996]).

**Action**
To explore your logs, use the contextual experience in Discover.

To view log streams, use Discover sessions.


::::

::::{dropdown} Removed Logs Explorer
Logs Explorer has been removed. 


For more information, refer to ({kibana-pull}203685[#203685]).

**Action**
Use the improved logs exploration experience in Discover.
::::