---
navigation_title: Breaking changes
products:
  - id: observability
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
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

## 9.6.0 [elastic-observability-9.6.0-breaking-changes]

::::{dropdown} Removes deprecated Significant Events public APIs
**Details**<br> The deprecated, experimental Significant Events public APIs are removed:

* `GET /api/streams/{name}/queries`
* `PUT /api/streams/{name}/queries/{queryId}`
* `DELETE /api/streams/{name}/queries/{queryId}`
* `POST /api/streams/{name}/queries/_bulk`
* `GET /api/streams/{name}/significant_events`

The Workflows step that wrapped `GET /api/streams/{name}/significant_events` is also removed.

For more information, check [#290828]({{kib-pull}}290828).

**Impact**<br> Requests to the removed endpoints return a `404` error.

**Action**<br> There is no public replacement. Remove calls to these endpoints, and remove `kibana.streams.getSignificantEvents`, from scripts, integrations, and workflows.
::::

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

