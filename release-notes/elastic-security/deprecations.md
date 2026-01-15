---
navigation_title: Deprecations
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

## 9.3.0 [elastic-security-9.3.0-deprecations]
$$$elastic-security-233289$$$
::::{dropdown} Removes evaluation of Endpoint exceptions during detection rule execution
Endpoint exceptions are no longer evaluated during detection rule execution.
For more information, refer to [#233289]({{kib-pull}}233289).
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

::::{dropdown} Removes {{elastic-defend}} API endoints
Removes deprecated API endpoints for {{elastic-defend}}.
For more information, refer to [#199598]({{kib-pull}}199598).
::::

::::{dropdown} Deprecates SIEM signals migration APIs
Removes the SIEM signals migration APIs.
For more information, refer to [#202662]({{kib-pull}}202662).
::::