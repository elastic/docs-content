---
navigation_title: Setup
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-setup.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Setup [transform-setup]

## Requirements overview [requirements-overview]

To use transforms, you must have:

* at least one [transform node](../../deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#transform-node-role),
* management features visible in the {{kib}} space, and
* security privileges that:
  * grant use of transforms, and
  * grant access to source and destination indices

## Security privileges [transform-privileges]

Assigning security privileges affects how users access transforms. Consider the two main categories:

* **[{{es}} API user](#transform-es-security-privileges)**: uses an {{es}} client, cURL, or {{kib}} **{{dev-tools-app}}** to access transforms through {{es}} APIs. This scenario requires {{es}} security privileges.
* **[{{kib}} user](#transform-kib-security-privileges)**: uses transforms in {{kib}}. This scenario requires {{kib}} feature privileges *and* {{es}} security privileges.

### {{es}} API user [transform-es-security-privileges]

To *manage* transforms, you must meet all of the following requirements:

* `transform_admin` built-in role or `manage_transform` cluster privileges,
* `read` and `view_index_metadata` index privileges on source indices, and
* `create_index`, `index`, `manage`, and `read` index privileges on destination indices. If a `retention_policy` is configured, `delete` index privilege is also required on the destination index.

To view only the configuration and status of transforms, you must have:

* `transform_user` built-in role or `monitor_transform` cluster privileges

For more information about {{es}} roles and privileges, refer to [Built-in roles](elasticsearch://reference/elasticsearch/roles.md) and [Security privileges](elasticsearch://reference/elasticsearch/security-privileges.md).

### {{kib}} user [transform-kib-security-privileges]

Within a {{kib}} space, for full access to transforms, you must meet all of the following requirements:

* Management features visible in the {{kib}} space, including `Data View Management` and `Stack Monitoring`,
* `monitoring_user` built-in role,
* `transform_admin` built-in role or `manage_transform` cluster privileges,
* `kibana_admin` built-in role or a custom role with `read` or `all` {{kib}} privileges for the `Data View Management` feature (dependent on whether data views already exist for your destination indices),
* data views for your source indices,
* `read` and `view_index_metadata` index privileges on source indices, and
* `create_index`, `index`, `manage`, and `read` index privileges on destination indices. Additionally, when using a `retention_policy`, `delete` index privilege is required on destination indices.
* `read_pipeline` cluster privileges, if the transform uses an ingest pipeline

Within a {{kib}} space, for read-only access to transforms, you must meet all of the following requirements:

* Management features visible in the {{kib}} space, including `Stack Monitoring`,
* `monitoring_user` built-in role,
* `transform_user` built-in role or `monitor_transform` cluster privileges,
* `kibana_admin` built-in role or a custom role with `read` {{kib}} privileges for at least one feature in the space,
* data views for your source and destination indices, and
* `read`, and `view_index_metadata` index privileges on source indices and destination indices

For more information and {{kib}} security features, see [{{kib}} role management](../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) and [{{kib}} privileges](../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

## {{kib}} spaces [transform-kib-spaces]

[Spaces](../../deploy-manage/manage-spaces.md) enable you to organize your source and destination indices and other saved objects in {{kib}} and to see only the objects that belong to your space. However, a transform is a long running task which is managed on cluster level and therefore not limited in scope to certain spaces. Space awareness can be implemented for a {{data-source}} under **Stack Management > Kibana** which allows privileges to the transform destination index.

To successfully create transforms in {{kib}}, you must be logged into a space where the source indices are visible and the `Data View Management` and `Stack Monitoring` features are visible.
