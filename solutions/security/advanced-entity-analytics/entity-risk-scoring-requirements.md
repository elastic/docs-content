---
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

# Entity risk scoring requirements

This page covers the requirements and guidelines for using the entity risk scoring, asset criticality, and entity store features, as well as their known limitations.

To use these features in {{stack}}, your role must have certain cluster, index, and {{kib}} privileges. In {{serverless-short}}, you need the appropriate user roles or a custom role with the right privileges.

In {{stack}}, these features require a [Platinum subscription](https://www.elastic.co/pricing) or higher. In {{serverless-short}}, they require the Security Analytics Complete [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).


## Entity risk scoring [_entity_risk_scoring]

To install or run the risk scoring engine, you need the following:

* In {{stack}}, you need the appropriate [privileges](#_privileges).
* In {{serverless-short}}, you need either the appropriate [predefined Security user role](#ers_roles) or a [custom role](/deploy-manage/users-roles/cloud-organization/user-roles.md) with the right [privileges](#_privileges).


### Privileges [_privileges]


| Action | Cluster Privileges | Index Privileges | Kibana Privileges |
| --- | --- | --- | --- |
| Install the risk engine | `manage_index_templates`<br> `manage_transform`<br> `manage_ingest_pipelines` | `All` for `risk-score.risk-score-*` | **Read** for the **Security** feature |
| Run the risk engine | `manage_transform` | N/A | **Read** for the **Security** feature |


### Predefined roles [ers_roles]
```yaml {applies_to}
serverless: all
```

| Action | Predefined role |
| --- | --- |
| Install the risk engine | - Platform engineer<br>- Admin |
| Run the risk engine | - Platform engineer<br>- Detections admin<br>- Admin |


### {{es}} resource guidelines [_es_resource_guidelines]
```yaml {applies_to}
stack:
```

Follow these guidelines to ensure clusters have adequate memory to handle data volume:

* With 2GB of Java Virtual Machine (JVM) heap memory, the risk scoring engine can safely process around 44 million documents, or 30 days of risk data with an ingest rate of 1000 documents per minute.
* With 1GB of JVM heap, the risk scoring engine can safely process around 20 million documents, or 30 days of risk data with an ingest rate of around 450 documents per minute.


### Known limitations [_known_limitations]

* The risk scoring engine uses an internal user role to score all hosts, users, and services, and doesn’t respect privileges applied to custom users or roles. After you turn on the risk scoring engine for a {{kib}} space, all alerts in the space will contribute to host, user, and service risk scores.
* You cannot customize alert data views or risk weights associated with alerts and asset criticality levels.


## Asset criticality [_asset_criticality]

To use asset criticality, you need the following:

* In {{stack}}, you need the appropriate [privileges](#_privileges_2) for the `.asset-criticality.asset-criticality-<space-id>` index.
* In {{serverless-short}}, you need either the appropriate [predefined Security user role](#ac_roles) or a [custom role](/deploy-manage/users-roles/cloud-organization/user-roles.md) with the right [privileges](#_privileges_2) for the `.asset-criticality.asset-criticality-<space-id>` index.

### Privileges [_privileges_2]


| Action | Index privilege |
| --- | --- |
| View asset criticality | `read` |
| View, assign, or change asset criticality | `read` and `write` |
| Unassign asset criticality | `delete` |

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
* In serverless, you need either the Admin role or a [custom role](/deploy-manage/users-roles/cloud-organization/user-roles.md) with the right [privileges](#_privileges_3).

### Privileges [_privileges_3]

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
