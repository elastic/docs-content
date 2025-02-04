# Entity risk scoring requirements [ers-requirements]

To use entity risk scoring, asset criticality, and entity store, your role must have certain cluster, index, and {{kib}} privileges. These features require a [Platinum subscription](https://www.elastic.co/pricing) or higher.

This page covers the requirements and guidelines for using the entity risk scoring, asset criticality, and entity store features, as well as their known limitations.


## Entity risk scoring [_entity_risk_scoring]


### Privileges [_privileges]

To turn on the risk scoring engine, you need the following privileges:

| Cluster | Index | {{kib}} |
| --- | --- | --- |
| * `manage_index_templates`<br>* `manage_transform`<br> | `all` privilege for `risk-score.risk-score-*` | **Read** for the **Security** feature |


### {{es}} resource guidelines [_es_resource_guidelines]

Follow these guidelines to ensure clusters have adequate memory to handle data volume:

* With 2GB of Java Virtual Machine (JVM) heap memory, the risk scoring engine can safely process around 44 million documents, or 30 days of risk data with an ingest rate of 1000 documents per minute.
* With 1GB of JVM heap, the risk scoring engine can safely process around 20 million documents, or 30 days of risk data with an ingest rate of around 450 documents per minute.


### Known limitations [_known_limitations]

The risk scoring engine uses an internal user role to score all hosts and users, and doesn’t respect privileges applied to custom users or roles. After you turn on the risk scoring engine for a {{kib}} space, all alerts in the space will contribute to host and user risk scores.


## Asset criticality [_asset_criticality]


### Privileges [_privileges_2]

To use asset criticality, you need the following privileges for the `.asset-criticality.asset-criticality-<space-id>` index:

| Action | Index privilege |
| --- | --- |
| View asset criticality | `read` |
| View, assign, or change asset criticality | `read` and `write` |
| Unassign asset criticality | `delete` |


## Entity store [_entity_store]


### Privileges [_privileges_3]

To use the entity store, you need the following privileges:

| Cluster | Index | {{kib}} |
| --- | --- | --- |
| * `manage_enrich`<br>* `manage_index_templates`<br>* `manage_ingest_pipelines`<br>* `manage_transform`<br> | * `read` and `view_index_metadata` for `.asset-criticality.asset-criticality-*`<br>* `read` and `manage` for `risk-score.risk-score-*`<br>* `read` and `manage` for `.entities.v1.latest.*`<br>* `read` and `view_index_metadata` for all {{elastic-sec}} indices<br> | **All** for the **Security** and **Saved Objects Management** features |
