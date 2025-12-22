---
navigation_title: Breaking changes
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
* `PATCH /api/detection_engine/rules/_bulk_update has been replaced by `POST /api/detection_engine/rules/_bulk_action`
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