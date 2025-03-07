---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html
navigation_title: "Self-managed"
applies_to:
  deployment:
    self:
---

# Manage snapshot repositories in self-managed deployments [snapshots-register-repository]

This guide shows you how to register a snapshot repository on a self-managed deployment. A snapshot repository is an off-cluster storage location for your snapshots. You must register a repository before you can take or restore snapshots.

In this guide, you’ll learn how to:

* Register a snapshot repository
* Verify that a repository is functional
* Clean up a repository to remove unneeded files

## Prerequisites [snapshot-repo-prereqs]

* To use {{kib}}'s **Snapshot and Restore** feature, you must have the following permissions:

    * [Cluster privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-cluster): `monitor`, `manage_slm`, `cluster:admin/snapshot`, and `cluster:admin/repository`
    * [Index privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices): `all` on the `monitor` index

* To register a snapshot repository, the cluster’s global metadata must be writeable. Ensure there aren’t any [cluster blocks](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-read-only) that prevent write access.

## Considerations [snapshot-repo-considerations]

When registering a snapshot repository, keep the following in mind:

* Each snapshot repository is separate and independent. {{es}} doesn’t share data between repositories.
* Clusters should only register a particular snapshot repository bucket once. If you register the same snapshot repository with multiple clusters, only one cluster should have write access to the repository. On other clusters, register the repository as read-only.
* This prevents multiple clusters from writing to the repository at the same time and corrupting the repository’s contents. It also prevents {{es}} from caching the repository’s contents, which means that changes made by other clusters will become visible straight away.
* When upgrading {{es}} to a newer version you can continue to use the same repository you were using before the upgrade. If the repository is accessed by multiple clusters, they should all have the same version. Once a repository has been modified by a particular version of {{es}}, it may not work correctly when accessed by older versions. However, you will be able to recover from a failed upgrade by restoring a snapshot taken before the upgrade into a cluster running the pre-upgrade version, even if you have taken more snapshots during or after the upgrade.

## Manage snapshot repositories [manage-snapshot-repos]

You can register and manage snapshot repositories in two ways:

* {{kib}}'s **Snapshot and Restore** feature
* {{es}}'s [snapshot repository management APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-snapshot)

To manage repositories in {{kib}}, go to the main menu and click **Stack Management** > **Snapshot and Restore*** > ***Repositories**. To register a snapshot repository, click **Register repository**.

You can also register a repository using the [Create snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create-repository).

## Self-managed repository types [self-managed-repo-types]

If you manage your own {{es}} cluster, you can use the following built-in snapshot repository types:

* [Azure](azure-repository.md)
* [Google Cloud Storage](google-cloud-storage-repository.md)
* [AWS S3](s3-repository.md)
* [Shared file system](shared-file-system-repository.md)
* [Read-only URL](read-only-url-repository.md)
* [Source-only](source-only-repository.md)

$$$snapshots-repository-plugins$$$
Other repository types are available through official plugins:

* [Hadoop Distributed File System (HDFS)](elasticsearch://reference/elasticsearch-plugins/repository-hdfs.md)

You can also use alternative storage implementations with these repository types, as long as the alternative implementation is fully compatible. For instance, [MinIO](https://minio.io) provides an alternative implementation of the AWS S3 API and you can use MinIO with the [`s3` repository type](s3-repository.md).

Note that some storage systems claim to be compatible with these repository types without emulating their behaviour in full. {{es}} requires full compatibility. In particular the alternative implementation must support the same set of API endpoints, return the same errors in case of failures, and offer equivalent consistency guarantees and performance even when accessed concurrently by multiple nodes. Incompatible error codes, consistency or performance may be particularly hard to track down since errors, consistency failures, and performance issues are usually rare and hard to reproduce.

You can perform some basic checks of the suitability of your storage system using the [Repository analysis](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-repository-analyze) API. If this API does not complete successfully, or indicates poor performance, then your storage system is not fully compatible and is therefore unsuitable for use as a snapshot repository. You will need to work with the supplier of your storage system to address any incompatibilities you encounter.

## Verify a repository [snapshots-repository-verification]

When you register a snapshot repository, {{es}} automatically verifies that the repository is available and functional on all master and data nodes.

To disable this verification, set the [create snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create-repository)'s `verify` query parameter to `false`. You can’t disable repository verification in {{kib}}.

```console
PUT _snapshot/my_unverified_backup?verify=false
{
  "type": "fs",
  "settings": {
    "location": "my_unverified_backup_location"
  }
}
```
%  TEST[setup:setup-repository]
%  TEST[s/my_unverified_backup_location/my_repository/]

If wanted, you can manually run the repository verification check. To verify a repository in {{kib}}, go to the **Repositories** list page and click the name of a repository. Then click **Verify repository**. You can also use the [verify snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-verify-repository).

```console
POST _snapshot/my_unverified_backup/_verify
```
%  TEST[continued]
%  TEST[s/my_unverified_backup_location/my_repository/]

If successful, the request returns a list of nodes used to verify the repository. If verification fails, the request returns an error.

You can test a repository more thoroughly using the [repository analysis API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-repository-analyze).


## Clean up a repository [snapshots-repository-cleanup]

Repositories can over time accumulate data that is not referenced by any existing snapshot. This is a result of the data safety guarantees the snapshot functionality provides in failure scenarios during snapshot creation and the decentralized nature of the snapshot creation process. This unreferenced data does in no way negatively impact the performance or safety of a snapshot repository but leads to higher than necessary storage use. To remove this unreferenced data, you can run a cleanup operation on the repository. This will trigger a complete accounting of the repository’s contents and delete any unreferenced data.

To run the repository cleanup operation in {{kib}}, go to the **Repositories** list page and click the name of a repository. Then click **Clean up repository**.

You can also use the [clean up snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-cleanup-repository).

```console
POST _snapshot/my_repository/_cleanup
```
%  TEST[setup:setup-snapshots]

The API returns:

```console-result
{
  "results": {
    "deleted_bytes": 20,
    "deleted_blobs": 5
  }
}
```
%  TESTRESPONSE[s/"deleted_bytes": 20/"deleted_bytes": $body.results.deleted_bytes/]
%  TESTRESPONSE[s/"deleted_blobs": 5/"deleted_blobs": $body.results.deleted_bytes/]

Depending on the concrete repository implementation the numbers shown for bytes free as well as the number of blobs removed will either be an approximation or an exact result. Any non-zero value for the number of blobs removed implies that unreferenced blobs were found and subsequently cleaned up.

Please note that most of the cleanup operations executed by this endpoint are automatically executed when deleting any snapshot from a repository. If you regularly delete snapshots, you will in most cases not get any or only minor space savings from using this functionality and should lower your frequency of invoking it accordingly.

## Back up a repository [snapshots-repository-backup]

You may wish to make an independent backup of your repository, for instance so that you have an archive copy of its contents that you can use to recreate the repository in its current state at a later date.

You must ensure that {{es}} does not write to the repository while you are taking the backup of its contents. If {{es}} writes any data to the repository during the backup then the contents of the backup may not be consistent and it may not be possible to recover any data from it in future. Prevent writes to the repository by unregistering the repository from the cluster which has write access to it.

Alternatively, if your repository supports it, you may take an atomic snapshot of the underlying filesystem and then take a backup of this filesystem snapshot. It is very important that the filesystem snapshot is taken atomically.

::::{warning}
Do not rely on repository backups that were taken by methods other than the one described in this section. If you use another method to make a copy of your repository contents then the resulting copy may capture an inconsistent view of your data. Restoring a repository from such a copy may fail, reporting errors, or may succeed having silently lost some of your data.
::::


::::{warning}
Do not use filesystem snapshots of individual nodes as a backup mechanism. You must use the {{es}} snapshot and restore feature to copy the cluster contents to a separate repository. Then, if desired, you can take a filesystem snapshot of this repository.
::::


When restoring a repository from a backup, you must not register the repository with {{es}} until the repository contents are fully restored. If you alter the contents of a repository while it is registered with {{es}} then the repository may become unreadable or may silently lose some of its contents. After restoring a repository from a backup, use the [Verify repository integrity](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-repository-verify-integrity) API to verify its integrity before you start to use the repository.
