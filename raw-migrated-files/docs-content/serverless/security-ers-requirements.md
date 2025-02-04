# Entity risk scoring requirements [security-ers-requirements]

To use entity risk scoring and asset criticality, you need the appropriate user roles. These features require the Security Analytics Complete [project feature](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).

This page covers the requirements for using the entity risk scoring and asset criticality features, as well as their known limitations.


## Entity risk scoring [security-ers-requirements-entity-risk-scoring]


### User roles [security-ers-requirements-user-roles]

To turn on the risk scoring engine, you need either the appropriate [predefined Security user role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) or a [custom role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md) with the right privileges:

**Predefined roles**

* Platform engineer
* Detections admin
* Admin

**Custom role privileges**

| Cluster | Index | {{kib}} |
| --- | --- | --- |
| * `manage_index_templates`<br>* `manage_transform`<br> | `all` privilege for `risk-score.risk-score-*` | **Read** for the **Security** feature |


### Known limitations [security-ers-requirements-known-limitations]

* The risk scoring engine uses an internal user role to score all hosts and users. After you turn on the risk scoring engine, all alerts in the project will contribute to host and user risk scores.
* You cannot customize alert data views or risk weights associated with alerts and asset criticality levels.


## Asset criticality [security-ers-requirements-asset-criticality]


### User roles [security-ers-requirements-user-roles-1]

To use asset criticality, you need either the appropriate [predefined Security user role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) or a [custom role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md) with the right privileges:

**Predefined roles**

| Action | Predefined role |
| --- | --- |
| View asset criticality | * Viewer<br>* Tier 1 analyst<br> |
| View, assign, change, or unassign asset criticality | * Editor<br>* Tier 2 analyst<br>* Tier 3 analyst<br>* Threat intelligence analyst<br>* Rule author<br>* SOC manager<br>* Endpoint operations analyst<br>* Platform engineer<br>* Detections admin<br>* Endpoint policy manager<br> |

**Custom role privileges**

Custom roles need the following privileges for the `.asset-criticality.asset-criticality-<space-id>` index:

| Action | Index privilege |
| --- | --- |
| View asset criticality | `read` |
| View, assign, or change asset criticality | `read` and `write` |
| Unassign asset criticality | `delete` |
