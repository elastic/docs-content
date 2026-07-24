---
navigation_title: Deprecations
products:
  - id: observability
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Elastic {{observability}} deprecations [elastic-observability-deprecations]
Over time, certain Elastic functionality becomes outdated and is replaced or removed. To help with the transition, Elastic deprecates functionality for a period before removal, giving you time to update your applications.

Review the deprecated functionality for Elastic {{observability}}. While deprecations have no immediate impact, we strongly encourage you update your implementation after you upgrade. To learn how to upgrade, check out [](/deploy-manage/upgrade.md).

% ## Next version

% ::::{dropdown} Deprecation title
% Description of the deprecation.
% For more information, check [PR #](PR link).
% **Impact**<br> Impact of deprecation.
% **Action**<br> Steps for mitigating deprecation impact.
% ::::

## 9.5.0 [elastic-observability-9.5.0-deprecations]

::::{dropdown} Deprecate experimental public Significant Events APIs
The five experimental public Significant Events API endpoints (`/api/streams/{name}/queries*` and `/api/streams/{name}/significant_events`) are deprecated and will be removed in a future release. These endpoints have been superseded by internal query routes.

View [#273310]({{kib-pull}}273310).

**Impact**<br> Calls to these endpoints return a `299` deprecation warning header.

**Action**<br> Migrate to the internal stream query routes before these endpoints are removed.
::::

::::{dropdown} Mark all LLM connectors as deprecated
All LLM connectors are now marked as deprecated. Deprecation badges and warnings are displayed on affected connectors in the UI.

View [#261591]({{kib-pull}}261591).

**Impact**<br> LLM connectors continue to function but display deprecation indicators in the {{connectors-ui}}.

**Action**<br> Migrate to a supported connector type. Refer to the guidance displayed on the connector for recommended alternatives.
::::

## 9.4.0 [elastic-observability-9.4.0-deprecations]

::::{dropdown} Remove Observability Agent from Agent Builder
The Observability agent has been removed from Agent Builder, replaced by skills in the Elastic AI agent.

View [#262937]({{kib-pull}}262937).

**Impact**<br> Conversations stored with the Observability agent will no longer appear in the conversation list and cannot be continued from the UI. No automatic migration is planned.
::::

::::{dropdown} Metrics Explorer is deprecated in favor of Discover
Metrics Explorer has been deprecated in favor of an improve metrics experience in Discover.

View [#261785]({{kib-pull}}261785).
::::

## 9.0.0 [elastic-observability-9.0.0-deprecations]

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