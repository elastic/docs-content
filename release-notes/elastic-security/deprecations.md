---
navigation_title: Deprecations
products:
  - id: security
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# {{elastic-sec}} deprecations [elastic-security-deprecations]
Over time, certain Elastic functionality becomes outdated and is replaced or removed. To help with the transition, Elastic deprecates functionality for a period before removal, giving you time to update your applications.

Review the deprecated functionality for {{elastic-sec}}. While deprecations have no immediate impact, we strongly encourage you update your implementation after you upgrade. To learn how to upgrade, check out [Upgrade](/deploy-manage/upgrade.md).

% ## Next version [elastic-security-X.X.X-deprecations]

% ::::{dropdown} Deprecation title
% Description of the deprecation.
% For more information, refer to [PR #](PR link).
% **Impact**<br> Impact of deprecation.
% **Action**<br> Steps for mitigating deprecation impact.
% ::::

## 9.4.0 [elastic-security-9.4.0-deprecations]

::::{dropdown} Entity Analytics: Asset Criticality APIs deprecated
The dedicated Asset Criticality APIs are deprecated in 9.4 and replaced by the Entity Store CRUD APIs.

Deprecated endpoints:
* `DELETE /api/asset_criticality`
* `POST /api/asset_criticality`
* `GET /api/asset_criticality`
* `GET /api/asset_criticality/list`

**Impact**<br> These endpoints will continue to work in 9.4 but will be removed in a future release.

**Action**<br> Migrate to the equivalent Entity Store APIs.

For more information, check [#258440]({{kib-pull}}258440).
% TODO: Add link to Entity Store API documentation when available. See https://github.com/elastic/docs-content-internal/issues/1100
::::

::::{dropdown} Removes the Threat Hunting Agent from Agent Builder
Removes the built-in Threat Hunting Agent from Agent Builder. Security AI workflows now use the Elastic AI Agent with Security skills, which is the default experience in 9.4.0.
For more information, refer to [#263996]({{kib-pull}}263996).

**Impact**<br> Conversations stored with the Threat Hunting Agent will no longer appear in the conversation list and cannot be continued from the UI. No automatic migration is planned.

::::

::::{dropdown} Deprecates Enable CCS Warning Privileges in Kibana advanced settings
Deprecates the `Enable CCS Warning Privileges` setting in {{kib}} **Advanced settings**. For more information, refer to [#252183]({{kib-pull}}252183).
::::

## 9.1.0 [elastic-security-9.1.0-deprecations]

::::{dropdown} Removes default quick prompts
Removes default quick prompts from the Security AI Assistant.
For more information, refer to [#225536]({{kib-pull}}225536).
::::

## 9.0.0 [elastic-security-900-deprecations]

::::{dropdown} Removes Defend for Containers (D4C)
Defend for Containers is no longer supported starting with {{stack}} 9.0. 
::::

::::{dropdown} Renames the integration-assistant plugin
Renames the `integration-assistant` plugin to `automatic-import` to match the associated feature.
For more information, refer to [#207325]({{kib-pull}}207325).
::::

::::{dropdown} Removes legacy risk engine
Removes all legacy risk engine code and features.
For more information, refer to [#201810]({{kib-pull}}201810).
::::

::::{dropdown} Removes {{elastic-defend}} API endpoints
Removes deprecated API endpoints for {{elastic-defend}}.
For more information, refer to [#199598]({{kib-pull}}199598).
::::

::::{dropdown} Deprecates SIEM signals migration APIs
Removes the SIEM signals migration APIs.
For more information, refer to [#202662]({{kib-pull}}202662).
::::