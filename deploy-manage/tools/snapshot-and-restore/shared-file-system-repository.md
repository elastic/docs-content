---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-filesystem-repository.html
applies_to:
  deployment:
    self:
---

# Shared file system repository [snapshots-filesystem-repository]

::::{note}
This repository type is only available if you run {{es}} on your own hardware. See [Manage snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md) for other deployment methods.
::::


Use a shared file system repository to store snapshots on a shared file system.

To register a shared file system repository, first mount the file system to the same location on all master and data nodes. Then add the file system’s path or parent directory to the `path.repo` setting in `elasticsearch.yml` for each master and data node. For running clusters, this requires a [rolling restart](../../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling) of each node.

Supported `path.repo` values vary by platform:

:::::::{tab-set}

::::::{tab-item} Unix-like systems
Linux and macOS installations support Unix-style paths:

```yaml
path:
  repo:
    - /mount/backups
    - /mount/long_term_backups
```

After restarting each node, use {{kib}} or the [create snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create-repository) to register the repository. When registering the repository, specify the file system’s path:

```console
PUT _snapshot/my_fs_backup
{
  "type": "fs",
  "settings": {
    "location": "/mount/backups/my_fs_backup_location"
  }
}
```
%  TEST[skip:no access to path]

If you specify a relative path, {{es}} resolves the path using the first value in the `path.repo` setting.

```console
PUT _snapshot/my_fs_backup
{
  "type": "fs",
  "settings": {
    "location": "my_fs_backup_location"        <1>
  }
}
```
%  TEST[skip:no access to path]

1. The first value in the `path.repo` setting is `/mount/backups`. This relative path, `my_fs_backup_location`, resolves to `/mount/backups/my_fs_backup_location`.


Clusters should only register a particular snapshot repository bucket once. If you register the same snapshot repository with multiple clusters, only one cluster should have write access to the repository. On other clusters, register the repository as read-only.

This prevents multiple clusters from writing to the repository at the same time and corrupting the repository’s contents. It also prevents {{es}} from caching the repository’s contents, which means that changes made by other clusters will become visible straight away.

To register a file system repository as read-only using the create snapshot repository API, set the `readonly` parameter to true. Alternatively, you can register a [URL repository](read-only-url-repository.md) for the file system.

```console
PUT _snapshot/my_fs_backup
{
  "type": "fs",
  "settings": {
    "location": "my_fs_backup_location",
    "readonly": true
  }
}
```
%  TEST[skip:no access to path]
::::::

::::::{tab-item} Windows
Windows installations support both DOS and Microsoft UNC paths. Escape any backslashes in the paths. For UNC paths, provide the server and share name as a prefix.

```yaml
path:
  repo:
    - "E:\\Mount\\Backups"                      <1>
    - "\\\\MY_SERVER\\Mount\\Long_term_backups" <2>
```

1. DOS path
2. UNC path


After restarting each node, use {{kib}} or the [create snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create-repository) to register the repository. When registering the repository, specify the file system’s path:

```console
PUT _snapshot/my_fs_backup
{
  "type": "fs",
  "settings": {
    "location": "E:\\Mount\\Backups\\My_fs_backup_location"
  }
}
```
%  TEST[skip:no access to path]

If you specify a relative path, {{es}} resolves the path using the first value in the `path.repo` setting.

```console
PUT _snapshot/my_fs_backup
{
  "type": "fs",
  "settings": {
    "location": "My_fs_backup_location"        <1>
  }
}
```
%  TEST[skip:no access to path]

1. The first value in the `path.repo` setting is `E:\Mount\Backups`. This relative path, `My_fs_backup_location`, resolves to `E:\Mount\Backups\My_fs_backup_location`.


Clusters should only register a particular snapshot repository bucket once. If you register the same snapshot repository with multiple clusters, only one cluster should have write access to the repository. On other clusters, register the repository as read-only.

This prevents multiple clusters from writing to the repository at the same time and corrupting the repository’s contents. It also prevents {{es}} from caching the repository’s contents, which means that changes made by other clusters will become visible straight away.

To register a file system repository as read-only using the create snapshot repository API, set the `readonly` parameter to true. Alternatively, you can register a [URL repository](read-only-url-repository.md) for the file system.

```console
PUT _snapshot/my_fs_backup
{
  "type": "fs",
  "settings": {
    "location": "my_fs_backup_location",
    "readonly": true
  }
}
```
%  TEST[skip:no access to path]
::::::

:::::::
## Repository settings [filesystem-repository-settings]

`chunk_size`
:   (Optional, [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Maximum size of files in snapshots. In snapshots, files larger than this are broken down into chunks of this size or smaller. Defaults to `null` (unlimited file size).

`compress`
:   (Optional, Boolean) If `true`, metadata files, such as index mappings and settings, are compressed in snapshots. Data files are not compressed. Defaults to `true`.

`location`
:   (Required, string) Location of the shared filesystem used to store and retrieve snapshots. This location must be registered in the `path.repo` setting on all master and data nodes in the cluster. Unlike `path.repo`, this setting supports only a single file path.

`max_number_of_snapshots`
:   (Optional, integer) Maximum number of snapshots the repository can contain. Defaults to `Integer.MAX_VALUE`, which is `2^31-1` or `2147483647`.

`max_restore_bytes_per_sec`
:   (Optional, [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Maximum snapshot restore rate per node. Defaults to unlimited. Note that restores are also throttled through [recovery settings](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md).

`max_snapshot_bytes_per_sec`
:   (Optional, [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Maximum snapshot creation rate per node. Defaults to `40mb` per second. Note that if the [recovery settings for managed services](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md#recovery-settings-for-managed-services) are set, then it defaults to unlimited, and the rate is additionally throttled through [recovery settings](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md).

`readonly`
:   (Optional, Boolean) If `true`, the repository is read-only. The cluster can retrieve and restore snapshots from the repository but not write to the repository or create snapshots in it.

    Only a cluster with write access can create snapshots in the repository. All other clusters connected to the repository should have the `readonly` parameter set to `true`.

    If `false`, the cluster can write to the repository and create snapshots in it. Defaults to `false`.

    ::::{important}
    If you register the same snapshot repository with multiple clusters, only one cluster should have write access to the repository. Having multiple clusters write to the repository at the same time risks corrupting the contents of the repository.

    ::::



## Troubleshooting a shared file system repository [_troubleshooting_a_shared_file_system_repository]

{{es}} interacts with a shared file system repository using the file system abstraction in your operating system. This means that every {{es}} node must be able to perform operations within the repository path such as creating, opening, and renaming files, and creating and listing directories, and operations performed by one node must be visible to other nodes as soon as they complete.

Check for common misconfigurations using the [Verify snapshot repository](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-verify-repository) API and the [Repository analysis](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-repository-analyze) API. When the repository is properly configured, these APIs will complete successfully. If the verify repository or repository analysis APIs report a problem then you will be able to reproduce this problem outside {{es}} by performing similar operations on the file system directly.

If the verify repository or repository analysis APIs fail with an error indicating insufficient permissions then adjust the configuration of the repository within your operating system to give {{es}} an appropriate level of access. To reproduce such problems directly, perform the same operations as {{es}} in the same security context as the one in which {{es}} is running. For example, on Linux, use a command such as `su` to switch to the user as which {{es}} runs.

If the verify repository or repository analysis APIs fail with an error indicating that operations on one node are not immediately visible on another node then adjust the configuration of the repository within your operating system to address this problem. If your repository cannot be configured with strong enough visibility guarantees then it is not suitable for use as an {{es}} snapshot repository.

The verify repository and repository analysis APIs will also fail if the operating system returns any other kind of I/O error when accessing the repository. If this happens, address the cause of the I/O error reported by the operating system.

::::{tip}
Many NFS implementations match accounts across nodes using their *numeric* user IDs (UIDs) and group IDs (GIDs) rather than their names. It is possible for {{es}} to run under an account with the same name (often `elasticsearch`) on each node, but for these accounts to have different numeric user or group IDs. If your shared file system uses NFS then ensure that every node is running with the same numeric UID and GID, or else update your NFS configuration to account for the variance in numeric IDs across nodes.
::::



## Linearizable register implementation [repository-fs-linearizable-registers]

The linearizable register implementation for shared filesystem repositories is based around file locking. To perform a compare-and-exchange operation on a register, {{es}} first locks he underlying file and then writes the updated contents under the same lock. This ensures that the file has not changed in the meantime.


