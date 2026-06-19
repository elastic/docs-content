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

::::{dropdown} Entity Analytics: Risk scores reset after upgrading to 9.4
Risk scoring is moving from name-based to ID-based scoring tied to the entity store. Historical name-based risk scores are not migrated to the new model.

**Impact**<br> After upgrading to 9.4, all existing risk scores are cleared. The entity store initializes with a 3-hour lookback, so scored entity counts will be lower immediately after upgrade and will rebuild over time. Additionally, Identity Provider (IdP) user entities may not receive risk scores initially, as alerts do not yet map directly to IdP EUIDs. Local user and host entities are unaffected.

**Action**<br> No action required to trigger the rebuild — it happens automatically. Plan for a warm-up period after upgrading before risk score dashboards return to their pre-upgrade state.

For more information, check [#258197]({{kib-pull}}258197).
::::

::::{dropdown} Entity Analytics requires additional index privileges for custom roles
**Details**<br> Starting in 9.4.0, the entity store reads entity data from a new set of indices. Roles that grant access to the Entity Analytics features must now include `read` on the following index patterns:

- `.entities.v2.latest.security_*`
- `.entities.v2.updates.security_*`
- `entities-latest-*`
- `risk-score.risk-score-*`
- `.entity_analytics.*`

The built-in Security roles have been updated to grant these privileges. Custom roles created against the `v1` index patterns (`.entities.v1.latest.security_*`) are not updated automatically.

**Impact**<br> Users assigned a custom role that does not include the index patterns above will see the **Entity Analytics** page load in a degraded state — without entity data and without the standard "insufficient privileges" message. Users assigned built-in Security roles are not affected.

**Action**<br> If you use custom roles to control access to Entity Analytics, add `read` on the following entity store and risk score index patterns to each affected role:

```yaml
- names:
    - ".entities.v2.latest.security_*"
    - "entities-latest-*"
    - "risk-score.risk-score-*"
    - ".entity_analytics.*"
  privileges:
    - read
```

For more information, check [#255800]({{kib-pull}}255800).
::::

::::{dropdown} Entity Analytics: Risk engine management APIs removed
The standalone risk engine is replaced by an entity maintainer integrated into the entity store. The following risk engine management API endpoint is removed:

* `DELETE /api/risk_score/engine/dangerously_delete_data`

**Impact**<br> Any scripts or automations using this endpoint will fail.

**Action**<br> Remove references to this endpoint. Risk scoring is now managed through the entity store lifecycle. Refer to the [Entity store API documentation]({{kib-apis}}group/endpoint-security-entity-store) for the new endpoints.
::::

::::{dropdown} Entity Analytics: Asset criticality values reset and CSV format changed after upgrading to 9.4
Asset criticality storage is moving to the entity store. Historical values from the legacy index are not migrated to the new model. Additionally, the CSV upload format has changed: headers are now required, and uploading a CSV no longer creates new entities — entities must already exist in the entity store.

**Impact**<br> Existing asset criticality assignments are not carried over after upgrading to 9.4. CSV files using the old headerless format will no longer work.

**Action**<br> Re-assign asset criticality in 9.4 using the updated CSV format or the entity flyout. Update any CSV files to include the required header row before uploading.
::::

::::{dropdown} Entity Analytics: Privileged user monitoring replaced by watchlists
Privileged user monitoring is replaced by watchlists in 9.4. Historical privileged user assignments are not migrated to the new model.

**Impact**<br> The privileged user monitoring UI and engine are removed. Existing privileged user configurations, including manual user lists and CSV uploads, are not carried over.

**Action**<br> Recreate your privileged user tracking using watchlists. The default **Privileged Users** watchlist automatically pulls in administrative users from Active Directory and Okta integrations.
% TODO: Add link to Watchlist documentation when available: [Watchlists](/solutions/security/advanced-entity-analytics/watchlists.md). See https://github.com/elastic/docs-content/pull/5994
::::

::::{dropdown} Entity Analytics: Privileged user monitoring APIs removed
All privileged user monitoring APIs are removed in 9.4.

Removed with no equivalent:
* `POST /api/entity_analytics/monitoring/users`
* `GET /api/entity_analytics/monitoring/users/list`
* `PUT /api/entity_analytics/monitoring/users/{id}`
* `DELETE /api/entity_analytics/monitoring/users/{id}`
* `POST /api/entity_analytics/monitoring/users/_csv`
* `POST /api/entity_analytics/monitoring/engine/init`
* `POST /api/entity_analytics/monitoring/engine/disable`
* `DELETE /api/entity_analytics/monitoring/engine/delete`
* `POST /api/entity_analytics/privileged_user_monitoring/pad/install`
* `GET /api/entity_analytics/privileged_user_monitoring/pad/status`

Replaced by watchlists equivalents:
* `POST .../monitoring/engine/schedule_now` → `POST /api/entity_analytics/watchlists/{watchlist_id}/sync`
* `.../monitoring/entity_source/...` → `/api/entity_analytics/watchlists/{watchlist_id}/entity_source/...`

**Impact**<br> Any scripts or automations using these endpoints will fail.

**Action**<br> Remove references to removed endpoints. For entity source management, update paths to use the watchlists-scoped equivalents. Refer to the [Entity Analytics API documentation]({{kib-apis}}/group/endpoint-security-entity-analytics-api).
::::

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

**Action**<br> Remove references to these endpoints. Refer to the [Entity store API documentation]({{kib-apis}}group/endpoint-security-entity-store) for information on new endpoints.
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

::::{dropdown} Entity Analytics: Entity identification in Explore/Entity flyout/Entity store
In 9.4, a fine-grained logical identifier has been introduced for user and host entities. In previous versions, user entities were identified by the `user.name` field and host entities were identified by the `host.name` field. This has been replaced by a priority ranking for hosts (`host.id` -> `host.name` -> `host.hostname`) and a user tiering identification which separates medium-confidence local users (i.e., a `user.name` associated with a particular `host.id`), from high-confidence IDP users found in integrations.

**Impact**<br> User and Host entities which do not provide enough information to properly identify them will not be available in the entity store. These entities will only be visible through "observed" aggregation views within the entity flyout and Explore details pages, with no Entity Analytics processing done against them, such as entity risk scoring, resolution, or watchlists. Additionally, entities which _are_ properly identified and are in the entity store will no longer have a link available to the Explore details page for that entity.
::::

::::{dropdown} Removes serializer and deserializer parameters from the Lists API
Removes the unused `serializer` and `deserializer` parameters from the Lists API endpoints.
For more information, check [#250111]({{kib-pull}}250111).

**Impact**<br> API requests that include `serializer` or `deserializer` parameters will return a deprecation warning header. The parameters are ignored.

**Action**<br> Remove any `serializer` or `deserializer` parameters from your Lists API requests.
::::

## 9.3.2 [elastic-security-932-breaking-changes]
::::{dropdown} Removes serializer and deserializer parameters from the Lists API
Removes the unused `serializer` and `deserializer` parameters from the Lists API endpoints.
For more information, check [#250111]({{kib-pull}}250111).

**Impact**<br> API requests that include `serializer` or `deserializer` parameters will return a deprecation warning header. The parameters are ignored.

**Action**<br> Remove any `serializer` or `deserializer` parameters from your Lists API requests.
::::

## 9.2.7 [elastic-security-927-breaking-changes]
::::{dropdown} Removes serializer and deserializer parameters from the Lists API
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

    * Use `POST /api/detection_engine/rules/_import` ([API documentation]({{kib-apis}}operation/operation-importrules)) to create multiple rules along with their associated entities (for example, exceptions and action connectors).
    * Alternatively, create rules individually using `POST /api/detection_engine/rules` ([API documentation]({{kib-apis}}operation/operation-createrule)).

* **For bulk updates of rules:**

    * Use `POST /api/detection_engine/rules/_bulk_action` ([API documentation]({{kib-apis}}operation/operation-performrulesbulkaction)) to update fields in multiple rules simultaneously.
    * Alternatively, update rules individually using `PUT /api/detection_engine/rules` ([API documentation]({{kib-apis}}operation/operation-updaterule)).

* **For bulk deletion of rules:**

    * Use `POST /api/detection_engine/rules/_bulk_action` ([API documentation]({{kib-apis}}operation/operation-performrulesbulkaction)) to delete multiple rules by IDs or query.
    * Alternatively, delete rules individually using `DELETE /api/detection_engine/rules` ([API documentation]({{kib-apis}}operation/operation-deleterule)).
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