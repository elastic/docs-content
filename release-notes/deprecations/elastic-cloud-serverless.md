---
navigation_title: "Elastic Cloud Serverless"
---

# Elastic Cloud Serverless deprecations [elastic-cloud-serverless-deprecations]
Review the deprecated functionality for Elastic Cloud Serverless. While deprecations have no immediate impact, we strongly encourage you update your implementation after you upgrade.

To learn how to upgrade, check out <uprade docs>.

For serverless API deprecations, check [APIs Changelog](https://www.elastic.co/docs/api/changes).

% ## Next release date Month Day, Year [elastic-cloud-serverless-releasedate-deprecations]
% Description of the deprecation and steps to update implementation.
% For more information, check [PR #](PR link).

## January 27, 2025 [elastic-cloud-serverless-01272025-deprecations]
* Deprecates a subset of Elastic Security Serverless endpoint management APIs. For more information, check [#206903](https://github.com/elastic/kibana/pull/206903).

## January 13, 2025 [elastic-cloud-serverless-01132025-deprecations]
* Remove all legacy risk engine code and features. For more information, check [#201810](https://github.com/elastic/kibana/pull/201810).

## January 6, 2025 [elastic-cloud-serverless-01062025-deprecations]
* Disables Elastic Observability Serverless log stream and settings pages. For more information, check [#203996](https://github.com/elastic/kibana/pull/203996). 
* Removes Logs Explorer in Elastic Observability Serverless. For more information, check [#203685](https://github.com/elastic/kibana/pull/203685).

## December 16, 2024 [elastic-cloud-serverless-12162024-deprecations]
* Deprecates the `discover:searchFieldsFromSource` setting. For more information, check [#202679](https://github.com/elastic/kibana/pull/202679).
* Disables scripted field creation in the Data Views management page. For more information, check [#202250](https://github.com/elastic/kibana/pull/202250). 
* Removes all logic based on the following settings: `xpack.reporting.roles.enabled`, `xpack.reporting.roles.allow`. For more information, check [#200834](https://github.com/elastic/kibana/pull/200834). 
* Removes the legacy table from Discover. For more information, check [#201254](https://github.com/elastic/kibana/pull/201254).
* Deprecates ephemeral tasks from action and alerting plugins. For more information, check [#197421](https://github.com/elastic/kibana/pull/197421).