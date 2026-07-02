---
navigation_title: Entity analytics requirements
description: Privileges, subscription tiers, roles, and limitations required to use entity risk scoring, asset criticality, and the entity store in Elastic Security.
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/ers-requirements.html
  - https://www.elastic.co/guide/en/serverless/current/security-ers-requirements.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Entity analytics requirements

This page covers the requirements and guidelines for using the entity risk scoring, asset criticality, and entity store features, as well as their known limitations.

To use these features in {{stack}}, your role must have certain cluster, index, and {{kib}} privileges. In {{serverless-short}}, you need the appropriate user roles or a custom role with the right privileges.

In {{stack}}, these features require a [Platinum subscription](https://www.elastic.co/pricing) or higher. In {{serverless-short}}, they require the Security Analytics Complete [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).

::::{note}
For the requirements to run {{anomaly-jobs}} and behavioral detection rules, refer to [Machine learning job and rule requirements](/solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md).
::::


## Entity risk scoring [_entity_risk_scoring]

To install or run risk scoring, you need the following:

* In {{stack}}, you need the appropriate [privileges](#_privileges).
* In {{serverless-short}}, you need either the appropriate [predefined Security user role](#ers_roles) or a [custom role](/deploy-manage/users-roles/cloud-organization/user-roles.md) with the right [privileges](#_privileges).


### Privileges [_privileges]


| Action | Cluster Privileges | Index Privileges | Kibana Privileges |
| --- | --- | --- | --- |
| Install risk scoring | `manage_index_templates`<br> `manage_transform`<br> `manage_ingest_pipelines` | `All` for `risk-score.risk-score-*` | **Read** for the **Security** feature |
| Run risk scoring | `manage_transform` | N/A | **Read** for the **Security** feature |
| {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Preview the risk score results | N/A | `Read` for `.alerts-security.alerts-*` | **Read** for the **Security** feature |
| {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` View alert risk contributions in entity details | N/A | N/A | **Read** for the **Security > Alerts** feature |
| {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` View the **Engine Status** tab | `manage_index_templates`<br>`manage_transform`<br>`manage_ingest_pipelines`<br>`manage_enrich` | `All` for `risk-score.risk-score-*` | **Read** for the **Security** feature |


### Predefined roles [ers_roles]
```yaml {applies_to}
serverless: all
```

| Action | Predefined role |
| --- | --- |
| Install risk scoring | - Platform engineer<br>- Admin |
| Run risk scoring | - Platform engineer<br>- Detections admin<br>- Admin |


### {{es}} resource guidelines [_es_resource_guidelines]
```yaml {applies_to}
stack:
```

Follow these guidelines to ensure clusters have adequate memory to handle data volume:

* With 2GB of Java Virtual Machine (JVM) heap memory, risk scoring can safely process around 44 million documents, or 30 days of risk data with an ingest rate of 1000 documents per minute.
* With 1GB of JVM heap, risk scoring can safely process around 20 million documents, or 30 days of risk data with an ingest rate of around 450 documents per minute.


### Known limitations [_known_limitations]

* Risk scoring uses an internal user role to score all hosts, users, and services, and doesn’t respect privileges applied to custom users or roles. After you turn on risk scoring for a {{kib}} space, all alerts in the space will contribute to host, user, and service risk scores.
* You cannot customize alert data views or risk weights associated with alerts and asset criticality levels.


## Asset criticality [_asset_criticality]

To use asset criticality, you need the following:

* In {{stack}}, you need the appropriate [privileges](#_privileges_2).
* In {{serverless-short}}, you need either the appropriate [predefined Security user role](#ac_roles) or a [custom role](/deploy-manage/users-roles/cloud-organization/user-roles.md) with the right [privileges](#_privileges_2).

### Privileges [_privileges_2]

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }

| Action | Index privilege |
| --- | --- |
| View asset criticality | `read` for `entities-latest-<space-id>` and `.entities.v2.latest.security_<space-id>-*` |
| View, assign, unassign, or change asset criticality | `read` and `write` for `entities-latest-<space-id>` and `read`, `write`, and `view_index_metadata` for `.entities.v2.latest.security_<space-id>-*` |
:::

:::{applies-item} { stack: ga 9.0-9.3 }
| Action | Index privilege |
| --- | --- |
| View asset criticality | `read` for `.asset-criticality.asset-criticality-<space-id>` |
| View, assign, or change asset criticality | `read` and `write` for `.asset-criticality.asset-criticality-<space-id>` |
| Unassign asset criticality | `delete` for `.asset-criticality.asset-criticality-<space-id>` |
:::

::::

### Predefined roles [ac_roles]
```yaml {applies_to}
serverless: all
```

| Action | Predefined role |
| --- | --- |
| View asset criticality | - Viewer<br>- Tier 1 analyst<br> |
| View, assign, change, or unassign asset criticality | - Editor<br>- Tier 2 analyst<br>- Tier 3 analyst<br>- Threat intelligence analyst<br>- Rule author<br>- SOC manager<br>- Endpoint operations analyst<br>- Platform engineer<br>- Detections admin<br>- Endpoint policy manager<br> |


## Entity store [_entity_store]

To turn on the entity store, you need the following:

* In {{stack}}, you need the appropriate [privileges](#_privileges_3).
* In {{serverless-short}}, you need either the Admin role or a [custom role](/deploy-manage/users-roles/cloud-organization/user-roles.md) with the right [privileges](#_privileges_3).

### Privileges [_privileges_3]

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }

#### Cluster

- `manage_index_templates`

#### Index

- `read` and `view_index_metadata` for `.asset-criticality.asset-criticality-*`
- `read` and `manage` for `risk-score.risk-score-*`
- `read` and `write` for `.entities.v2.latest.security_*`
- Additionally, `manage` for `.entities.v2.latest.security_*` is required to add or remove entities from a resolution group in the [Resolution](/solutions/security/advanced-entity-analytics/view-entity-details.md#resolution) section of the entity details flyout
- `read` and `view_index_metadata` for all {{elastic-sec}} indices

#### {{kib}}

**All** for the **Security** and **Saved Objects Management** features
:::

:::{applies-item} { stack: ga 9.0-9.3 }

#### Cluster

- `manage_enrich`
- `manage_index_templates`
- `manage_ingest_pipelines`
- `manage_transform`

#### Index

- `read` and `view_index_metadata` for `.asset-criticality.asset-criticality-*`
- `read` and `manage` for `risk-score.risk-score-*`
- `read` and `manage` for `.entities.v1.latest.*`
- `read` and `view_index_metadata` for all {{elastic-sec}} indices

#### {{kib}}

**All** for the **Security** and **Saved Objects Management** features
:::

::::
