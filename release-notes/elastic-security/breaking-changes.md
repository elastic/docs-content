---
navigation_title: Breaking changes
products:
  - id: security
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---
# {{elastic-sec}} breaking changes [elastic-security-breaking-changes]
Breaking changes can impact your Elastic applications, potentially disrupting normal operations. Before you upgrade, carefully review the {{elastic-sec}} breaking changes and take the necessary steps to mitigate any issues. To learn how to upgrade, check [](/deploy-manage/upgrade.md).

% ## Next version [elastic-security-X.X.X-breaking-changes]

% ::::{dropdown} Title of breaking change 
% Description of the breaking change.
% For more information, check [PR #](PR link).

% **Impact**<br> Impact of the breaking change.

% **Action**<br> Steps for mitigating deprecation impact.
% ::::

## 9.4.0 [elastic-security-940-breaking-changes]

::::{dropdown} Entity store management and CRUD APIs removed
The entity store management and CRUD APIs are removed and replaced by an updated API surface available from 9.4.
For more information, check [#264679]({{kib-pull}}264679).

Removed endpoints:
* `POST /api/entity_store/enable`
* `GET /api/entity_store/status`
* `POST /api/entity_store/engines/{entityType}/init`
* `POST /api/entity_store/engines/{entityType}/start`
* `POST /api/entity_store/engines/{entityType}/stop`
* `DELETE /api/entity_store/engines/{entityType}`
* `DELETE /api/entity_store/engines`
* `GET /api/entity_store/engines/{entityType}`
* `GET /api/entity_store/engines`
* `POST /api/entity_store/engines/apply_dataview_indices`
* `GET /api/entity_store/entities/list`
* `PUT /api/entity_store/entities/{entityType}`
* `POST /api/entity_store/entities/bulk`
* `DELETE /api/entity_store/entities/{entityType}`

**Impact**<br> Any scripts or automations using these endpoints will fail after upgrading to 9.4.

**Action**<br> Remove references to these endpoints. Refer to the Entity Store API documentation for information on new endpoints.
% TODO: Add link to Entity Store API documentation when available. See https://github.com/elastic/docs-content-internal/issues/1100
::::

::::{dropdown} Entity store index structure has changed
In 9.4, the entity store consolidates all entity types into a single index per namespace, replacing the previous model where hosts, users, and services each had their own index. For more information, check [#251089]({{kib-pull}}251089).

The old per-type index pattern (`.entities.v1.latest.security_{type}_<space-id>`) is replaced by:

* A single latest index: `.entities.v2.latest.security_<space-id>-<mapping_version>`
* A shared alias: `entities-latest-<space-id>`
* History snapshot indices: `.entities.v2.history.security_<space-id>.<YYYY-MM-DD>-<HH>`

**Impact**<br> Any direct queries, dashboards, or integrations that reference the old per-type index patterns will fail after upgrading to 9.4.

**Action**<br> Update direct index references to use the new shared alias.
::::

::::{dropdown} Removes `serializer` and `deserializer` parameters from the Lists API
Removes the unused `serializer` and `deserializer` parameters from the Lists API endpoints.
For more information, check [#250111]({{kib-pull}}250111).

**Impact**<br> API requests that include `serializer` or `deserializer` parameters will return a deprecation warning header. The parameters are ignored.

**Action**<br> Remove any `serializer` or `deserializer` parameters from your Lists API requests.
::::

## 9.3.2 [elastic-security-932-breaking-changes]
::::{dropdown} Removes `serializer` and `deserializer` parameters from the Lists API
Removes the unused `serializer` and `deserializer` parameters from the Lists API endpoints.
For more information, check [#250111]({{kib-pull}}250111).

**Impact**<br> API requests that include `serializer` or `deserializer` parameters will return a deprecation warning header. The parameters are ignored.

**Action**<br> Remove any `serializer` or `deserializer` parameters from your Lists API requests.
::::

## 9.2.7 [elastic-security-927-breaking-changes]
::::{dropdown} Removes `serializer` and `deserializer` parameters from the Lists API
Removes the unused `serializer` and `deserializer` parameters from the Lists API endpoints.
For more information, check [#250111]({{kib-pull}}250111).

**Impact**<br> API requests that include `serializer` or `deserializer` parameters will return a deprecation warning header. The parameters are ignored.

**Action**<br> Remove any `serializer` or `deserializer` parameters from your Lists API requests.
::::

## 9.2.0 [elastic-security-920-breaking-changes]
::::{dropdown} Changes invalid category for Gatekeeper

Changes `event.category` from `security` to `configuration` for Gatekeeper on macOS.

**Impact**<br> Gatekeeper events on macOS are now labeled as `event.category == configuration`.

**Action**<br> If you're deploying custom rules using `event.category == security` on macOS, change the query to `event.category == configuration`.

::::

## 9.0.7 [elastic-security-907-breaking-changes]
::::{dropdown} Changes invalid category for Gatekeeper

Changes `event.category` from `security` to `configuration` for Gatekeeper on macOS.

**Impact**<br> Gatekeeper events on macOS are now labeled as `event.category == configuration`.

**Action**<br> If you're deploying custom rules using `event.category == security` on macOS, change the query to `event.category == configuration`.

::::


## 9.0.0 [elastic-security-900-breaking-changes]

::::{dropdown} Removes legacy security rules bulk endpoints
* `POST /api/detection_engine/rules/_bulk_create` has been replaced by `POST /api/detection_engine/rules/_import`
* `PUT /api/detection_engine/rules/_bulk_update` has been replaced by `POST /api/detection_engine/rules/_bulk_action`
* `PATCH /api/detection_engine/rules/_bulk_update` has been replaced by `POST /api/detection_engine/rules/_bulk_action`
* `DELETE /api/detection_engine/rules/_bulk_delete` has been replaced by `POST /api/detection_engine/rules/_bulk_action`
* `POST api/detection_engine/rules/_bulk_delete` has been replaced by `POST /api/detection_engine/rules/_bulk_action`

These changes were introduced in [#197422]({{kib-pull}}197422).

**Impact**<br> Deprecated endpoints will fail with a 404 status code starting from version 9.0.0.

**Action**<br>

Update your implementations to use the new endpoints:

* **For bulk creation of rules:**

    * Use `POST /api/detection_engine/rules/_import` ([API documentation](https://www.elastic.co/docs/api/doc/kibana/operation/operation-importrules)) to create multiple rules along with their associated entities (for example, exceptions and action connectors).
    * Alternatively, create rules individually using `POST /api/detection_engine/rules` ([API documentation](https://www.elastic.co/docs/api/doc/kibana/operation/operation-createrule)).

* **For bulk updates of rules:**

    * Use `POST /api/detection_engine/rules/_bulk_action` ([API documentation](https://www.elastic.co/docs/api/doc/kibana/operation/operation-performrulesbulkaction)) to update fields in multiple rules simultaneously.
    * Alternatively, update rules individually using `PUT /api/detection_engine/rules` ([API documentation](https://www.elastic.co/docs/api/doc/kibana/operation/operation-updaterule)).

* **For bulk deletion of rules:**

    * Use `POST /api/detection_engine/rules/_bulk_action` ([API documentation](https://www.elastic.co/docs/api/doc/kibana/operation/operation-performrulesbulkaction)) to delete multiple rules by IDs or query.
    * Alternatively, delete rules individually using `DELETE /api/detection_engine/rules` ([API documentation](https://www.elastic.co/docs/api/doc/kibana/operation/operation-deleterule)).
::::

::::{dropdown} Removes deprecated endpoint management endpoints
* `POST /api/endpoint/isolate` has been replaced by `POST /api/endpoint/action/isolate`
* `POST /api/endpoint/unisolate` has been replaced by `POST /api/endpoint/action/unisolate`
* `GET /api/endpoint/policy/summaries` has been deprecated without replacement. Will be removed in v9.0.0
* `POST /api/endpoint/suggestions/{{suggestion_type}}` has been deprecated without replacement. Will be removed in v9.0.0
* `GET /api/endpoint/action_log/{{agent_id}}` has been deprecated without replacement. Will be removed in v9.0.0
* `GET /api/endpoint/metadata/transforms` has been deprecated without replacement. Will be removed in v9.0.0

**Impact**<br> Deprecated endpoints will fail with a 404 status code starting from version 9.0.0.

**Action**<br>

* Remove references to `GET /api/endpoint/policy/summaries` endpoint.
* Remove references to `POST /api/endpoint/suggestions/{{suggestion_type}}` endpoint.
* Remove references to `GET /api/endpoint/action_log/{{agent_id}}` endpoint.
* Remove references to `GET /api/endpoint/metadata/transforms` endpoint.
* Replace references to deprecated endpoints with the replacements listed in the breaking change details.
::::

::::{dropdown} Refactors the Timeline HTTP API endpoints
For more information, refer to [#200633]({{kib-pull}}200633).
::::

::::{dropdown} Removes deprecated {{elastic-defend}} APIs
For more information, refer to [#199598]({{kib-pull}}199598).
::::

::::{dropdown} Removes deprecated API endpoints for bulk CRUD actions on detection rules
For more information, refer to [#197422]({{kib-pull}}197422) and [#207906]({{kib-pull}}207906).
::::