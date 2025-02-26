---
navigation_title: "Elastic Security"
---

# Elastic Security breaking changes [elastic-security-breaking-changes]
Before you upgrade, carefully review the Elastic Security breaking changes and take the necessary steps to mitigate any issues. 

To learn how to upgrade, check out <uprade docs>.

% ## Next version [elastic-security-nextversion-breaking-changes]
% **Release date:** Month day, year

% ::::{dropdown} Title of breaking change 
% Description of the breaking change.
% For more information, check [PR #](PR link).
% **Impact**<br> Impact of the breaking change.
% **Action**<br> Steps for mitigating deprecation impact.
% ::::

## 9.0.0 [elastic-security-900-breaking-changes]
**Release date:** March 25, 2025

::::{dropdown} Removed legacy security rules bulk endpoints
* `POST /api/detection_engine/rules/_bulk_create` has been replaced by `POST /api/detection_engine/rules/_import`
* `PUT /api/detection_engine/rules/_bulk_update` has been replaced by `POST /api/detection_engine/rules/_bulk_action`
* `PATCH /api/detection_engine/rules/_bulk_update has been replaced by `POST /api/detection_engine/rules/_bulk_action`
* `DELETE /api/detection_engine/rules/_bulk_delete` has been replaced by `POST /api/detection_engine/rules/_bulk_action`
* `POST api/detection_engine/rules/_bulk_delete` has been replaced by `POST /api/detection_engine/rules/_bulk_action`

These changes were introduced in [#197422](https://github.com/elastic/kibana/pull/197422).

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

::::{dropdown} Remove deprecated endpoint management endpoints
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