---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
---

# Create snapshots [snapshots-take-snapshot]

This guide shows you how to take snapshots of a running cluster. You can later [restore a snapshot](restore-snapshot.md) to recover or transfer its data.

In this guide, you’ll learn how to:

* Automate snapshot creation and retention with {{slm}} ({{slm-init}})
* Manually take a snapshot
* Monitor a snapshot’s progress
* Delete or cancel a snapshot
* Back up cluster configuration files

The guide also provides tips for creating dedicated cluster state snapshots and taking snapshots at different time intervals.


## Prerequisites [create-snapshot-prereqs]

* To use {{kib}}'s **Snapshot and Restore** feature, you must have the following permissions:

    * [Cluster privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-cluster): `monitor`, `manage_slm`, `cluster:admin/snapshot`, and `cluster:admin/repository`
    * [Index privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices): `all` on the `monitor` index

* You can only take a snapshot from a running cluster with an elected [master node](../../distributed-architecture/clusters-nodes-shards/node-roles.md#master-node-role).
* A snapshot repository must be [registered](self-managed.md) and available to the cluster.
* The cluster’s global metadata must be readable. To include an index in a snapshot, the index and its metadata must also be readable. Ensure there aren’t any [cluster blocks](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-read-only) or [index blocks](elasticsearch://reference/elasticsearch/index-settings/index-block.md) that prevent read access.


## Considerations [create-snapshot-considerations]

* Each snapshot must have a unique name within its repository. Attempts to create a snapshot with the same name as an existing snapshot will fail.
* Snapshots are automatically deduplicated. You can take frequent snapshots with little impact to your storage overhead.
* Each snapshot is logically independent. You can delete a snapshot without affecting other snapshots.
* Taking a snapshot can temporarily pause shard allocations. See [Snapshots and shard allocation](../snapshot-and-restore.md#snapshots-shard-allocation).
* Taking a snapshot doesn’t block indexing or other requests. However, the snapshot won’t include changes made after the snapshot process starts.
* You can take multiple snapshots at the same time. The [`snapshot.max_concurrent_operations`](elasticsearch://reference/elasticsearch/configuration-reference/snapshot-restore-settings.md#snapshot-max-concurrent-ops) cluster setting limits the maximum number of concurrent snapshot operations.
* If you include a data stream in a snapshot, the snapshot also includes the stream’s backing indices and metadata.

    You can also include only specific backing indices in a snapshot. However, the snapshot won’t include the data stream’s metadata or its other backing indices.

* A snapshot can include a data stream but exclude specific backing indices. When you restore such a data stream, it will contain only backing indices in the snapshot. If the stream’s original write index is not in the snapshot, the most recent backing index from the snapshot becomes the stream’s write index.


## Automate snapshots with {{slm-init}} [automate-snapshots-slm]

{{slm-cap}} ({{slm-init}}) is the easiest way to regularly back up a cluster. An {{slm-init}} policy automatically takes snapshots on a preset schedule. The policy can also delete snapshots based on retention rules you define.

::::{tip}
Elastic Cloud Hosted deployments automatically include the `cloud-snapshot-policy` {{slm-init}} policy. Elastic Cloud Hosted uses this policy to take periodic snapshots of your cluster. For more information, see the [Manage snapshot repositories in Elastic Cloud Hosted documentation](/deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md).
::::

### {{slm-init}} security [slm-security]

The following [cluster privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-cluster) control access to the {{slm-init}} actions when {{es}} {{security-features}} are enabled:

`manage_slm`
:   Allows a user to perform all {{slm-init}} actions, including creating and updating policies and starting and stopping {{slm-init}}.

`read_slm`
:   Allows a user to perform all read-only {{slm-init}} actions, such as getting policies and checking the {{slm-init}} status.

`cluster:admin/snapshot/*`
:   Allows a user to take and delete snapshots of any index, whether or not they have access to that index.

You can create and manage roles to assign these privileges through {{kib}} Management.

To grant the privileges necessary to create and manage {{slm-init}} policies and snapshots, you can set up a role with the `manage_slm` and `cluster:admin/snapshot/*` cluster privileges and full access to the {{slm-init}} history indices.

For example, the following request creates an `slm-admin` role:

```console
POST _security/role/slm-admin
{
  "cluster": [ "manage_slm", "cluster:admin/snapshot/*" ],
  "indices": [
    {
      "names": [ ".slm-history-*" ],
      "privileges": [ "all" ]
    }
  ]
}
```
%  TEST[skip:security is not enabled here]

To grant read-only access to {{slm-init}} policies and the snapshot history, you can set up a role with the `read_slm` cluster privilege and read access to the {{slm}} history indices.

For example, the following request creates a `slm-read-only` role:

```console
POST _security/role/slm-read-only
{
  "cluster": [ "read_slm" ],
  "indices": [
    {
      "names": [ ".slm-history-*" ],
      "privileges": [ "read" ]
    }
  ]
}
```
%  TEST[skip:security is not enabled here]


### Create an {{slm-init}} policy [create-slm-policy]

To manage {{slm-init}} in {{kib}}, go to the main menu and click **Stack Management** > **Snapshot and Restore*** > ***Policies**. To create a policy, click **Create policy**.

You can also manage {{slm-init}} using the [{{slm-init}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-slm). To create a policy, use the [create {{slm-init}} policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-put-lifecycle).

The following request creates a policy that backs up the cluster state, all data streams, and all indices daily at 1:30 a.m. UTC.

```console
PUT _slm/policy/nightly-snapshots
{
  "schedule": "0 30 1 * * ?",       <1>
  "name": "<nightly-snap-{now/d}>", <2>
  "repository": "my_repository",    <3>
  "config": {
    "indices": "*",                 <4>
    "include_global_state": true    <5>
  },
  "retention": {                    <6>
    "expire_after": "30d",
    "min_count": 5,
    "max_count": 50
  }
}
```

1. When to take snapshots, written in [Cron syntax](/explore-analyze/alerts-cases/watcher/schedule-types.md#schedule-cron).
2. Snapshot name. Supports [date math](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-date-math-index-names). To prevent naming conflicts, the policy also appends a UUID to each snapshot name.
3. [Registered snapshot repository](self-managed.md) used to store the policy’s snapshots.
4. Data streams and indices to include in the policy’s snapshots.
5. If `true`, the policy’s snapshots include the cluster state. This also includes all feature states by default. To only include specific feature states, see [Back up a specific feature state](#back-up-specific-feature-state).
6. Optional retention rules. This configuration keeps snapshots for 30 days, retaining at least 5 and no more than 50 snapshots regardless of age. See [{{slm-init}} retention](#slm-retention-task) and [Snapshot retention limits](#snapshot-retention-limits).



### Manually run an {{slm-init}} policy [manually-run-slm-policy]

You can manually run an {{slm-init}} policy to immediately create a snapshot. This is useful for testing a new policy or taking a snapshot before an upgrade. Manually running a policy doesn’t affect its snapshot schedule.

To run a policy in {{kib}}, go to the **Policies** page and click the run icon under the **Actions** column. You can also use the [execute {{slm-init}} policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-execute-lifecycle).

```console
POST _slm/policy/nightly-snapshots/_execute
```
%  TEST[skip:we can’t easily handle snapshots from docs tests]

The snapshot process runs in the background. To monitor its progress, see [Monitor a snapshot](#monitor-snapshot).


### {{slm-init}} retention [slm-retention-task]

{{slm-init}} snapshot retention is a cluster-level task that runs separately from a policy’s snapshot schedule. To control when the {{slm-init}} retention task runs, configure the [`slm.retention_schedule`](elasticsearch://reference/elasticsearch/configuration-reference/snapshot-restore-settings.md#slm-retention-schedule) cluster setting.

```console
PUT _cluster/settings
{
  "persistent" : {
    "slm.retention_schedule" : "0 30 1 * * ?"
  }
}
```

To immediately run the retention task, use the [execute {{slm-init}} retention policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-execute-retention).

```console
POST _slm/_execute_retention
```

An {{slm-init}} policy’s retention rules only apply to snapshots created using the policy. Other snapshots don’t count toward the policy’s retention limits.


### Snapshot retention limits [snapshot-retention-limits]

We recommend you include retention rules in your {{slm-init}} policy to delete snapshots you no longer need.

A snapshot repository can safely scale to thousands of snapshots. However, to manage its metadata, a large repository requires more memory on the master node. Retention rules ensure a repository’s metadata doesn’t grow to a size that could destabilize the master node.


## Manually create a snapshot [manually-create-snapshot]

To take a snapshot without an {{slm-init}} policy, use the [create snapshot API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create). The snapshot name supports [date math](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-date-math-index-names).

```console
# PUT _snapshot/my_repository/<my_snapshot_{now/d}>
PUT _snapshot/my_repository/%3Cmy_snapshot_%7Bnow%2Fd%7D%3E
```
%  TEST[s/3E/3E?wait_for_completion=true/]

Depending on its size, a snapshot can take a while to complete. By default, the create snapshot API only initiates the snapshot process, which runs in the background. To block the client until the snapshot finishes, set the `wait_for_completion` query parameter to `true`.

```console
PUT _snapshot/my_repository/my_snapshot?wait_for_completion=true
```

You can also clone an existing snapshot using [clone snapshot API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-clone).


## Monitor a snapshot [monitor-snapshot]

To monitor any currently running snapshots, use the [get snapshot API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-get) with the `_current` request path parameter.

```console
GET _snapshot/my_repository/_current
```

To get a complete breakdown of each shard participating in any currently running snapshots, use the [get snapshot status API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-get).

```console
GET _snapshot/_status
```


### Check {{slm-init}} history [check-slm-history]

To get more information about a cluster’s {{slm-init}} execution history, including stats for each {{slm-init}} policy, use the [get {{slm-init}} stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-get-stats). The API also returns information about the cluster’s snapshot retention task history.

```console
GET _slm/stats
```

To get information about a specific {{slm-init}} policy’s execution history, use the [get {{slm-init}} policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-get-lifecycle). The response includes:

* The next scheduled policy execution.
* The last time the policy successfully started the snapshot process, if applicable. A successful start doesn’t guarantee the snapshot completed.
* The last time policy execution failed, if applicable, and the associated error.

```console
GET _slm/policy/nightly-snapshots
```


## Delete or cancel a snapshot [delete-snapshot]

To delete a snapshot in {{kib}}, go to the **Snapshots** page and click the trash icon under the **Actions** column. You can also use the [delete snapshot API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-delete).

```console
DELETE _snapshot/my_repository/my_snapshot_2099.05.06
```
%  TEST[setup:setup-snapshots]

If you delete a snapshot that’s in progress, {{es}} cancels it. The snapshot process halts and deletes any files created for the snapshot. Deleting a snapshot doesn’t delete files used by other snapshots.


## Back up configuration files [back-up-config-files]

If you run {{es}} on your own hardware, we recommend that, in addition to backups, you take regular backups of the files in each node’s [`$ES_PATH_CONF` directory](../../deploy/self-managed/configure-elasticsearch.md#config-files-location) using the file backup software of your choice. Snapshots don’t back up these files. Also note that these files will differ on each node, so each node’s files should be backed up individually.

::::{important}
The `elasticsearch.keystore`, TLS keys, and [SAML](../../deploy/self-managed/configure-elasticsearch.md#ref-saml-settings), [OIDC](../../deploy/self-managed/configure-elasticsearch.md#ref-oidc-settings), and [Kerberos](../../deploy/self-managed/configure-elasticsearch.md#ref-kerberos-settings) realms private key files contain sensitive information. Consider encrypting your backups of these files.
::::



## Back up a specific feature state [back-up-specific-feature-state]

By default, a snapshot that includes the cluster state also includes all [feature states](../snapshot-and-restore.md#feature-state). Similarly, a snapshot that excludes the cluster state excludes all feature states by default.

You can also configure a snapshot to only include specific feature states, regardless of the cluster state.

To get a list of available features, use the [get features API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-features-get-features).

```console
GET _features
```

The API returns:

```console-result
{
  "features": [
    {
      "name": "tasks",
      "description": "Manages task results"
    },
    {
      "name": "kibana",
      "description": "Manages Kibana configuration and reports"
    },
    {
      "name": "security",
      "description": "Manages configuration for Security features, such as users and roles"
    },
    ...
  ]
}
```
%  TESTRESPONSE[skip:response may vary based on features in test cluster]

To include a specific feature state in a snapshot, specify the feature `name` in the `feature_states` array.

For example, the following {{slm-init}} policy only includes feature states for the {{kib}} and {{es}} security features in its snapshots.

```console
PUT _slm/policy/nightly-snapshots
{
  "schedule": "0 30 2 * * ?",
  "name": "<nightly-snap-{now/d}>",
  "repository": "my_repository",
  "config": {
    "indices": "*",
    "include_global_state": true,
    "feature_states": [
      "kibana",
      "security"
    ]
  },
  "retention": {
    "expire_after": "30d",
    "min_count": 5,
    "max_count": 50
  }
}
```

Any index or data stream that’s part of the feature state will display in a snapshot’s contents. For example, if you back up the `security` feature state, the `security-*` system indices display in the [get snapshot API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-get)'s response under both `indices` and `feature_states`.


## Dedicated cluster state snapshots [cluster-state-snapshots]

Some feature states contain sensitive data. For example, the `security` feature state includes system indices that may contain user names and encrypted password hashes. Because passwords are stored using [cryptographic hashes](../../deploy/self-managed/configure-elasticsearch.md#hashing-settings), the disclosure of a snapshot would not automatically enable a third party to authenticate as one of your users or use API keys. However, it would disclose confidential information, and if a third party can modify snapshots, they could install a back door.

To better protect this data, consider creating a dedicated repository and {{slm-init}} policy for snapshots of the cluster state. This lets you strictly limit and audit access to the repository.

For example, the following {{slm-init}} policy only backs up the cluster state. The policy stores these snapshots in a dedicated repository.

```console
PUT _slm/policy/nightly-cluster-state-snapshots
{
  "schedule": "0 30 2 * * ?",
  "name": "<nightly-cluster-state-snap-{now/d}>",
  "repository": "my_secure_repository",
  "config": {
    "include_global_state": true,                 <1>
    "indices": "-*"                               <2>
  },
  "retention": {
    "expire_after": "30d",
    "min_count": 5,
    "max_count": 50
  }
}
```

1. Includes the cluster state. This also includes all feature states by default.
2. Excludes regular data streams and indices.
%  TEST[s/my_secure_repository/my_repository/]

If you take dedicated snapshots of the cluster state, you’ll need to exclude the cluster state from your other snapshots. For example:

```console
PUT _slm/policy/nightly-snapshots
{
  "schedule": "0 30 2 * * ?",
  "name": "<nightly-snap-{now/d}>",
  "repository": "my_repository",
  "config": {
    "include_global_state": false,    <1>
    "indices": "*"                    <2>
  },
  "retention": {
    "expire_after": "30d",
    "min_count": 5,
    "max_count": 50
  }
}
```

1. Excludes the cluster state. This also excludes all feature states by default.
2. Includes all regular data streams and indices.



## Create snapshots at different time intervals [create-snapshots-different-time-intervals]

If you only use a single {{slm-init}} policy, it can be difficult to take frequent snapshots and retain snapshots with longer time intervals.

For example, a policy that takes snapshots every 30 minutes with a maximum of 100 snapshots will only keep snapshots for approximately two days. While this setup is great for backing up recent changes, it doesn’t let you restore data from a previous week or month.

To fix this, you can create multiple {{slm-init}} policies with the same snapshot repository that run on different schedules. Since a policy’s retention rules only apply to its snapshots, a policy won’t delete a snapshot created by another policy.

For example, the following {{slm-init}} policy takes hourly snapshots with a maximum of 24 snapshots. The policy keeps its snapshots for one day.

```console
PUT _slm/policy/hourly-snapshots
{
  "name": "<hourly-snapshot-{now/d}>",
  "schedule": "0 0 * * * ?",
  "repository": "my_repository",
  "config": {
    "indices": "*",
    "include_global_state": true
  },
  "retention": {
    "expire_after": "1d",
    "min_count": 1,
    "max_count": 24
  }
}
```

The following policy takes nightly snapshots in the same snapshot repository. The policy keeps its snapshots for one month.

```console
PUT _slm/policy/daily-snapshots
{
  "name": "<daily-snapshot-{now/d}>",
  "schedule": "0 45 23 * * ?",          <1>
  "repository": "my_repository",
  "config": {
    "indices": "*",
    "include_global_state": true
  },
  "retention": {
    "expire_after": "30d",
    "min_count": 1,
    "max_count": 31
  }
}
```

1. Runs at 11:45 p.m. UTC every day.


The following policy creates monthly snapshots in the same repository. The policy keeps its snapshots for one year.

```console
PUT _slm/policy/monthly-snapshots
{
  "name": "<monthly-snapshot-{now/d}>",
  "schedule": "0 56 23 1 * ?",            <1>
  "repository": "my_repository",
  "config": {
    "indices": "*",
    "include_global_state": true
  },
  "retention": {
    "expire_after": "366d",
    "min_count": 1,
    "max_count": 12
  }
}
```

1. Runs on the first of the month at 11:56 p.m. UTC.
