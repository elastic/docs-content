---
navigation_title: Deprecations
---

# {{serverless-full}} deprecations [elastic-cloud-serverless-deprecations]
Review the deprecated functionality for {{serverless-full}}. While deprecations have no immediate impact, we strongly encourage you update your implementation.

% ## Next release date Month Day, Year [elastic-cloud-serverless-releasedate-deprecations]
% Description of the deprecation and steps to update implementation.
% For more information, check [PR #](PR link).

## November 24, 2025 [elastic-cloud-serverless-11242025-deprecations]
* Shows a callout for deprecated, in-use ILM policies. For more information, check [#243416]({{kib-pull}}243416).

## October 13, 2025 [elastic-cloud-serverless-10132025-deprecations]
* Filters endpoint exceptions from the detection engine's execution logic. For more information, check [#233289]({{kib-pull}}233289).

## August 25, 2025 [elastic-cloud-serverless-08252025-deprecations]
* Changes the `reporting_user` role to leverage reserved {{kib}} privileges. For more information, check [#132766](https://github.com/elastic/elasticsearch/pull/132766)

## June 30, 2025 [elastic-cloud-serverless-06302025-deprecations]
* Removes Default Quick Prompts from the Security AI Assistant. For more information, check [#225536]({{kib-pull}}225536).

## June 2, 2025 [elastic-cloud-serverless-06022025-deprecations]
* Removes the `allowByValueEmbeddables` setting from the Dashboard plugin. For more information, check [#221165]({{kib-pull}}221165). 

## February 24, 2025 [elastic-cloud-serverless-02242025-deprecations]
* Deprecates the Behavioral Analytics CRUD APIs [#122960](https://github.com/elastic/elasticsearch/pull/122960)

## February 3, 2025 [elastic-cloud-serverless-02032025-deprecations]
* Renames the `integration-assistant` plugin to `automatic-import`. For more information, check [#207325]({{kib-pull}}207325).

## January 27, 2025 [elastic-cloud-serverless-01272025-deprecations]
* Deprecates a subset of Elastic Security Serverless endpoint management APIs. For more information, check [#206903]({{kib-pull}}206903).

## January 13, 2025 [elastic-cloud-serverless-01132025-deprecations]
* Removes all legacy risk engine code and features. For more information, check [#201810]({{kib-pull}}201810).

## January 6, 2025 [elastic-cloud-serverless-01062025-deprecations]
* Disables the Elastic Observability Serverless log stream and settings pages. For more information, check [#203996]({{kib-pull}}203996). 
* Removes Logs Explorer in Elastic Observability Serverless. For more information, check [#203685]({{kib-pull}}203685).

## December 16, 2024 [elastic-cloud-serverless-12162024-deprecations]
* Deprecates the `discover:searchFieldsFromSource` setting. For more information, check [#202679]({{kib-pull}}202679).
* Disables scripted field creation in the Data Views management page. For more information, check [#202250]({{kib-pull}}202250). 
* Removes all logic based on the following settings: `xpack.reporting.roles.enabled`, `xpack.reporting.roles.allow`. For more information, check  [#200834]({{kib-pull}}200834). 
* Removes the legacy table from Discover. For more information, check [#201254]({{kib-pull}}201254).
* Deprecates ephemeral tasks from action and alerting plugins. For more information, check [#197421]({{kib-pull}}197421).
