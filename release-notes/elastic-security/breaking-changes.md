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

## 9.6.0 [elastic-security-960-breaking-changes]

::::{dropdown} Elastic Defend and endpoint management APIs enforce request limits
Requests to the {{elastic-defend}} and endpoint management APIs now enforce maximum string lengths and array sizes:

- **{{elastic-defend}} artifacts:** Blocklist, trusted device, and basic-mode trusted application entry values, including signer `subject_name` values, are limited to 4,096 characters. Trusted application advanced-mode entry `field` values and event filter entry `field` values are limited to 1,024 characters.
- **Response actions APIs:** For all `POST /api/endpoint/action/*` requests, `comment` is limited to 30,000 characters, `endpoint_ids` to 250 items, and `alert_ids` and `case_ids` to 50 items each. Each ID in these arrays is limited to 256 characters. Command parameters are also limited, for example `parameters.command` for `execute` (8,192 characters), `parameters.path` for `scan` and `get_file` (4,096), inline `parameters.raw` for `run_script` (65,536), and `parameters.process_name` for `kill_process` (1,024). For `GET /api/endpoint/action`, `agentIds` is limited to 250 items, `userIds` and `withOutputs` to 50 items each, and `startDate` and `endDate` to 64 characters. Each `agentIds`, `userIds`, and `withOutputs` value is limited to 256 characters.
- **Scripts library API:** `name` must be 1 to 256 characters. `description`, `instructions`, and `example` are limited to 10,000 characters, and `pathToExecutable` to 4,096 characters. For `PATCH` requests, `version` must be 1 to 256 characters.
- **Endpoint metadata, policy response, and protection updates note APIs:** `kuery` is limited to 30,000 characters, and IDs such as `id`, `agentId`, and `package_policy_id` to 256 characters. The protection updates note `note` field is limited to 10,000 characters.
- **Response actions in detection rules:** When you create, update, preview, or import a rule, Osquery `query` values and ECS mapping `value` entries are limited to 30,000 characters, and ECS mapping `field` values to 2,000 characters. The `pack_id` and `saved_query_id` values, and the query `id`, `version`, and `platform` values, are limited to 256 characters. For {{elastic-defend}} response actions, `comment` is limited to 30,000 characters, `scriptId` to 256 characters, and `scriptInput` to 8,192 characters.

**Impact**<br> Requests that exceed these limits, or that send an empty `name` or `version` to the scripts library API, are rejected with a validation error. Creating, updating, previewing, or importing a detection rule with response action parameters that exceed these limits fails validation. After you upgrade, existing detection rules whose response action parameters exceed these limits fail when they run, even if you don't edit them.

**Action**<br> Before you upgrade, make sure scripts, integrations, and rule import files that call these APIs keep values within these limits, and update existing detection rules whose response action parameters exceed them.

For more information, check [#274803]({{kib-pull}}274803), [#274987]({{kib-pull}}274987), [#275710]({{kib-pull}}275710), [#275711]({{kib-pull}}275711), and [#275716]({{kib-pull}}275716).
::::

::::{dropdown} Workflows: Run workflow sends documents in one format from every entry point
When you run a workflow from the alerts table, the row actions menu, or the alert details flyout, {{elastic-sec}} now sends document IDs, and {{kib}} fetches each document. Workflows receive every document with dotted field paths and array values, for example `'host.name': ['h1']`. Previously, **Run workflow** from the legacy alert details flyout sent the raw `_source`, with nested objects and single values, for example `host: { name: 'h1' }`. Runtime fields that are defined only on a {{data-source}} aren't included.

**Impact**<br> Workflows that read fields in the nested `_source` format from the legacy alert details flyout can resolve those fields as `undefined`.

**Action**<br> Update workflows that read document fields from the trigger event to use dotted field paths with array values, such as `event.documents[0]['host.name'][0]`.

For more information, check [#292144]({{kib-pull}}292144).
::::

::::{dropdown} Cases: Legacy response action attachments use the `security.endpoint` format
Case attachments of the legacy `actions` type are now returned as external reference attachments of type `security.endpoint`. This applies to existing and new attachments in Cases API responses, case user actions, and Cases workflow step outputs. Stored attachments aren't modified, and the `user` and `alert` attachment types are unchanged.

**Impact**<br> Scripts, integrations, and workflows that read `actions` attachments from the Cases API or Cases workflow steps no longer receive the `actions` type.

**Action**<br> Update code that parses `actions` attachments to read response action attachments as external reference attachments of type `security.endpoint`.

For more information, check [#287729]({{kib-pull}}287729).
::::

## 9.4.0 [elastic-security-940-breaking-changes]

::::{dropdown} Osquery: Scheduled query results no longer populate action_id
Starting in 9.4, Osquery scheduled-pack result documents correlate using stable UUIDs (`pack_id` and `schedule_id`) instead of the name-derived `action_id`. `action_id` is no longer populated for scheduled results; it remains populated for live queries. This applies when using the Osquery Manager integration v1.23.0 or later.

**Impact**<br> Any dashboard, saved search, detection rule, or ingest pipeline that groups or filters scheduled Osquery results by `action_id` returns no data after upgrading to 9.4 or later — including the default dashboards bundled with the Osquery Manager integration. Live query results are unaffected. No data is lost: the underlying result data remains fully queryable through the new fields.

**Action**<br> Update any custom (user-authored) dashboards, saved searches, detection rules, and ingest pipelines that reference `action_id` for scheduled results to use `schedule_id` or `pack_id` instead. 

For more information, check [#271572]({{kib-pull}}271572).
::::

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