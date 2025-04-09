---
navigation_title: "Deprecations"
---

# Elastic {{observability}} deprecations [elastic-observability-deprecations]
Over time, certain Elastic functionality becomes outdated and is replaced or removed. To help with the transition, Elastic deprecates functionality for a period before removal, giving you time to update your applications. 

Review the deprecated functionality for Elastic {{observability}}. While deprecations have no immediate impact, we strongly encourage you update your implementation after you upgrade. To learn how to upgrade, check out [Upgrade](/deploy-manage/upgrade.md).

% ## Next version
% **Release date:** Month day, year

% ::::{dropdown} Deprecation title
% Description of the deprecation.
% For more information, check [PR #](PR link).
% **Impact**<br> Impact of deprecation. 
% **Action**<br> Steps for mitigating deprecation impact.
% ::::

% ## 9.0.0 [elastic-observability-900-deprecations]
% **Release date:** April 2, 2025

% ::::{dropdown} Deprecation title
% Description of the deprecation.
% For more information, check [PR #](PR link).
% **Impact**<br> Impact of deprecation. 
% **Action**<br> Steps for mitigating deprecation impact.
% ::::

::::{dropdown} Removed Logs Explorer
Logs Explorer has been removed. 

For more information, check [#203685]({{kib-pull}}203685).

**Action**<br>
Use the improved logs exploration experience in Discover.
::::

::::{dropdown} Removed GA feature flags for host and container views
The `observability:enableInfrastructureHostsView` and `enableInfrastructureContainerAssetView` feature flags have been removed for host and container views.

For more information, check [#197684]({{kib-pull}}197684).

::::