---
navigation_title: "Elastic Security"
---

# {{elastic-sec}} deprecations [elastic-security-deprecations]
Over time, certain Elastic functionality becomes outdated and is replaced or removed. To help with the transition, Elastic deprecates functionality for a period before removal, giving you time to update your applications. 

Review the deprecated functionality for {{elastic-sec}}. While deprecations have no immediate impact, we strongly encourage you update your implementation after you upgrade.

To learn how to upgrade, check out [Upgrade](/deploy-manage/upgrade.md).

% ## Next version
% **Release date:** Month day, year

% ::::{dropdown} Deprecation title
% Description of the deprecation.
% For more information, check [PR #](PR link).
% **Impact**<br> Impact of deprecation. 
% **Action**<br> Steps for mitigating deprecation impact.
% ::::

% ## 9.0.0 [elastic-security-900-deprecations]
% **Release date:** April 2, 2025

::::{dropdown} Renames the `integration-assistant` plugin
Renames the `integration-assistant` plugin to `automatic-import` to match the associated feature.
For more information, check ({{kibana-pull}}207325[#207325]).
::::

::::{dropdown} Removes legacy risk engine
Removes all legacy risk engine code and features.
For more information, check ({{kibana-pull}}201810[#201810]).
::::

::::{dropdown} Removes {{elastic-defend}} API endoints
Removes deprecated API endpoints for {{elastic-defend}}.
For more information, check ({{kibana-pull}}199598[#199598]).
::::

::::{dropdown} Deprecates SIEM signals migration APIs
Deprecates the SIEM signals migration APIs.
For more information, check ({{kibana-pull}}202662[#202662]).
::::