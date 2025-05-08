---
navigation_title: "Breaking changes"
---

# {{fleet}} and {{agent}} breaking changes [fleet-elastic-agent-breaking-changes]
Breaking changes can impact your Elastic applications, potentially disrupting normal operations. Before you upgrade, carefully review the {{fleet}} and {{agent}} breaking changes and take the necessary steps to mitigate any issues. To learn how to upgrade, check [Upgrade](/deploy-manage/upgrade.md).

% ## Next version [fleet-elastic-agent-nextversion-breaking-changes]

% ::::{dropdown} Title of breaking change
% Description of the breaking change.
% For more information, check [PR #](PR link).

% **Impact**<br> Impact of the breaking change.

% **Action**<br> Steps for mitigating deprecation impact.
% ::::

## 9.0.1 [fleet-elastic-agent-9.0.1-breaking-changes]

::::{dropdown} Disabled the `process` scraper of the `hostmetrics` receiver in the Elastic Distribution of OTel Collector

**Impact**<br>
This scraper collects metrics for all available processes of a host without an easy way to limit this to only report top N process for example. This results in quite big amount of timeseries. Since this is not quite critical for any of the available UIs or dashboards we decide to disable it temporarily until we find a better solution. Users that specifically need these metrics can also enable it back manually.

For more information, check [#198434]({{agent-pull}}7894).
::::

## 9.0.0 [fleet-elastic-agent-900-breaking-changes]

::::{dropdown} Removed deprecated epm Fleet APIs
Removed `GET/POST/DELETE /epm/packages/:pkgkey` APIs in favor of the `GET/POST/DELETE /epm/packages/:pkgName/:pkgVersion`.

**Impact**<br>
* Removed `experimental` query parameter in `GET /epm/packages` and `GET /epm/categories`
* Removed `response` in response in `* /epm/packages*` and `GET /epm/categories`
* Removed `savedObject` in `/epm/packages` response in favor of `installationInfo`

For more information, check [#198434]({{kib-pull}}198434).
::::

::::{dropdown} Removed deprecated Fleet APIs for agents endpoints
Removed the following API endpoints:

* `POST /service-tokens` in favor of `POST /service_tokens`
* `GET /agent-status` in favor `GET /agent_status`
* `PUT /agents/:agentid/reassign` in favor of `POST /agents/:agentid/reassign`

Removed deprecated parameters or responses:

* Removed `total` from `GET /agent_status` response
* Removed `list` from `GET /agents` response

For more information, check [#198313]({{kib-pull}}198313).
::::

::::{dropdown} Removed cloud defend support for {{agent}}
Support for `cloud-defend` (Defend for Containers) has been removed. The package has been removed from the {{agent}} packaging scripts and template Kubernetes files.

For more information, check [#5481]({{agent-pull}}5481).
::::

::::{dropdown} Removed username and password default values for {{agent}}
The default values for `username` and `password` have been removed for when {{agent}} is running in container mode. The {{es}} `api_key` can now be set in that mode using the `ELASTICSEARCH_API_KEY` environment variable.

For more information, check [#5536]({{agent-pull}}5536).
::::

::::{dropdown} Changed Ubuntu-based Docker images for {{agent}}
The default Ubuntu-based Docker images used for {{agent}} have been changed to UBI-minimal-based images, to reduce the overall footprint of the agent Docker images and to improve compliance with enterprise standards.

For more information, check [#6427]({{agent-pull}}6427).
::::

::::{dropdown} Removed --path.install flag declaration from {{agent}} paths command
The deprecated `--path.install` flag declaration has been removed from the {{agent}} `paths` command and its use removed from the `container` and `enroll` commands.

For more information, check [#6461]({{agent-pull}}6461) and [#2489]({{agent-pull}}2489).
::::

::::{dropdown} Changed the default {{agent}} installation and upgrade
The default {{agent}} installation and ugprade have been changed to include only the `agentbeat`, `endpoint-security` and `pf-host-agent` components. Additional components can be included using flags.

For more information, check [#6542]({{agent-pull}}6542).
::::

::::{dropdown} Removed deprecated settings API endpoints in Fleet
* `GET/DELETE/POST enrollment-api-keys`: removed in favor of `GET/DELETE/POST enrollment_api_keys`
* Removed `list` property from `GET enrollment_api_keys` response in favor of `items`
* `GET/POST /settings`: `fleet_server_hosts` was removed from the response and body

For more information, check [#198799]({{kib-pull}}198799).
::::

::::{dropdown} Removed deprecated settings API endpoints in Fleet
* `GET/DELETE/POST enrollment-api-keys`: removed in favor of `GET/DELETE/POST enrollment_api_keys`
* Removed `list` property from `GET enrollment_api_keys` response in favor of `items`
* `GET/POST /settings`: `fleet_server_hosts` was removed from the response and body

For more information, check [#198799]({{kib-pull}}198799).
::::

::::{dropdown} Removed deprecated topics property for kafka output in favor of the topic property
Removed deprecated property `topics` from output APIs in response and requests (`(GET|POST|PUT) /api/fleet/outputs`) in favor of the `topic` property.

For more information, check [#199226]({{kib-pull}}199226).
::::

::::{dropdown} Limit pagination size to 100 when retrieving full policy or withAgentCount in Fleet
In addition to the new pagination limit size of 100, retrieving agent policies without agent count is now the new default behavior, and a new query parameter `withAgentCount` was added to retrieve the agent count.

For more information, check [#196887]({{kib-pull}}196887).
::::