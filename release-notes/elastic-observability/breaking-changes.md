---
navigation_title: Breaking changes
---

# Elastic {{observability}} breaking changes [elastic-observability-breaking-changes]
Breaking changes can impact your Elastic applications, potentially disrupting normal operations. Before you upgrade, carefully review the Elastic {{observability}} breaking changes and take the necessary steps to mitigate any issues. To learn how to upgrade, check [](/deploy-manage/upgrade.md).

% ## Next version [elastic-observability-nextversion-breaking-changes]
% **Release date:** Month day, year

% ::::{dropdown} Title of breaking change 
% Description of the breaking change.
% For more information, check [PR #](PR link).

% **Impact**<br> Impact of the breaking change.

% **Action**<br> Steps for mitigating deprecation impact.
% ::::

## 9.0.1 [elastic-observability-9.0.1-breaking-changes]

There are no breaking changes in Elastic {{observability}} 9.0.1.

## 9.0.0 [elastic-observability-9.0.0-breaking-changes]

::::{dropdown} Profiling now defaults to 19Hz sampling frequency
For more information, check [#202278]({{kib-pull}}202278).
::::

::::{dropdown} Removed log stream and settings pages
The following have been removed:
* Logs Stream
* Logs settings page
* Logs stream panel in Dashboards

For more information, check [#203996]({{kib-pull}}203996).

**Action**<br>
To explore your logs, use the contextual experience in Discover.

To view log streams, use Discover sessions.

::::

