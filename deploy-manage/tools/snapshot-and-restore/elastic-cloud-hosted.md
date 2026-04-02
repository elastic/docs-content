---
navigation_title: "{{ech}}"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-custom-repository.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-custom-repository.html
applies_to:
  deployment:
    ess:
products:
  - id: cloud-hosted
---

# Manage snapshot repositories in {{ech}}

Snapshot repositories allow you to back up and restore your {{es}} data efficiently. In {{ech}}, repositories are automatically registered and managed within your deployment, ensuring data security, long-term archiving, and seamless recovery.

By default, {{ech}} takes a snapshot of all the indices in your {{es}} cluster every 30 minutes. You can set a different snapshot interval if needed for your environment. You can also take snapshots on demand, without having to wait for the next interval. Taking a snapshot on demand does not affect the retention schedule for existing snapshots; it just adds an additional snapshot to the repository. This might be helpful if you are about to make a deployment change and you don’t have a current snapshot.

Use {{kib}} to manage your snapshots. In {{kib}}, you can set up additional repositories where the snapshots are stored, other than the one currently managed by {{ech}}. You can view and delete snapshots, and configure a snapshot lifecycle management (SLM) policy to automate when snapshots are created and deleted.

Snapshots back up only open indices. If you close an index, it is not included in snapshots and you will not be able to restore the data.

A snapshot taken using the default `found-snapshots` repository can only be restored to deployments in the same region. If you need to restore snapshots across regions, create the destination deployment, connect to the custom repository, and then restore from a snapshot.

From within {{ech}}, you can restore a snapshot from a different deployment in the same region.

## Prerequisites for {{ech}}

:::{include} _snippets/restore-snapshot-common-prerequisites.md
:::

## Considerations

When working with snapshot repositories in {{ech}}, keep the following in mind:

- Each snapshot repository is separate and independent. {{es}} doesn’t share data between repositories.
- Clusters should only register a particular snapshot repository bucket once. If you register the same snapshot repository with multiple clusters, only one cluster should have write access to the repository. On other clusters, register the repository as read-only.
- This prevents multiple clusters from writing to the repository at the same time and corrupting the repository’s contents. It also prevents {{es}} from caching the repository’s contents, which means that changes made by other clusters will become visible straight away.
- When upgrading {{es}} to a newer version, you can continue to use the same repository you were using before the upgrade. If the repository is accessed by multiple clusters, they should all have the same version. Once a repository has been modified by a particular version of {{es}}, it may not work correctly when accessed by older versions. However, you will be able to recover from a failed upgrade by restoring a snapshot taken before the upgrade into a cluster running the pre-upgrade version, even if you have taken more snapshots during or after the upgrade.

## {{ech}} snapshot repository types [ess-repo-types]

[{{ech}} deployments](https://cloud.elastic.co/registration?page=docs&placement=docs-body) automatically register the [`found-snapshots`](../snapshot-and-restore.md) repository. {{ech}} uses this repository and the `cloud-snapshot-policy` to take periodic snapshots of your cluster. You can also use the `found-snapshots` repository for your own [{{slm-init}} policies](create-snapshots.md#automate-snapshots-slm) or to store searchable snapshots.

The `found-snapshots` repository is specific to each deployment. However, you can restore snapshots from another deployment’s `found-snapshots` repository if the deployments are under the same account and in the same region. See the Cloud [Snapshot and restore](../snapshot-and-restore.md) documentation to learn more.

{{ech}} deployments also support the following repository types:

* [Azure](ec-azure-snapshotting.md)
* [Google Cloud Storage](ec-gcs-snapshotting.md)
* [AWS S3](ec-aws-custom-repository.md)
* [Source-only](source-only-repository.md)

## Register a snapshot repository in {{ech}} [register-snapshot-repos-ech]

In **{{ech}}**, snapshot repositories are automatically registered for you, but you can create additional repositories if needed.

* {{kib}}'s **Snapshot and Restore** feature
* {{es}}'s [snapshot repository management APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-snapshot)

To manage repositories in {{kib}}:

1. Go to the **Snapshot and Restore** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the **Repositories** tab. 
3. To register a snapshot repository, click **Register repository**.

You can also register a repository using the [Create snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create-repository).

## Verify a repository [snapshots-repository-verification]

When you register a snapshot repository, {{es}} automatically verifies that the repository is available and functional on all master and data nodes.

To disable this verification during repository creation, set the [create snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create-repository)'s `verify` query parameter to `false`. You can’t disable repository verification in {{kib}}.

```console
PUT _snapshot/my_unverified_backup?verify=false
{
  "type": "fs",
  "settings": {
    "location": "my_unverified_backup_location"
  }
}
```

If wanted, you can manually run the repository verification check. To verify a repository in {{kib}}, go to the **Repositories** list page and click the name of a repository. Then click **Verify repository**. You can also use the [verify snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-verify-repository).

```console
POST _snapshot/my_unverified_backup/_verify
```

If successful, the request returns a list of nodes used to verify the repository. If verification fails, the request returns an error.

You can test a repository more thoroughly using the [repository analysis API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-repository-analyze).


## Clean up a repository [snapshots-repository-cleanup]

Repositories can over time accumulate data that is not referenced by any existing snapshot. This is a result of the data safety guarantees the snapshot functionality provides in failure scenarios during snapshot creation and the decentralized nature of the snapshot creation process. This unreferenced data does in no way negatively impact the performance or safety of a snapshot repository but leads to higher than necessary storage use. To remove this unreferenced data, you can run a cleanup operation on the repository. This will trigger a complete accounting of the repository’s contents and delete any unreferenced data.

To run the repository cleanup operation in {{kib}}, go to the **Repositories** list page and click the name of a repository. Then click **Clean up repository**.

You can also use the [clean up snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-cleanup-repository).

```console
POST _snapshot/my_repository/_cleanup
```

The API returns:

```console-result
{
  "results": {
    "deleted_bytes": 20,
    "deleted_blobs": 5
  }
}
```

Depending on the concrete repository implementation the numbers shown for bytes free as well as the number of blobs removed will either be an approximation or an exact result. Any non-zero value for the number of blobs removed implies that unreferenced blobs were found and subsequently cleaned up.

Note that most of the cleanup operations executed by this endpoint are automatically executed when deleting any snapshot from a repository. If you regularly delete snapshots, you will in most cases not get any or only minor space savings from using this functionality and should lower your frequency of invoking it accordingly.

## Back up a repository [snapshots-repository-backup]

You may wish to make an independent backup of your repository, for instance so that you have an archive copy of its contents that you can use to recreate the repository in its current state at a later date.

You must ensure that {{es}} does not write to the repository while you are taking the backup of its contents. If {{es}} writes any data to the repository during the backup then the contents of the backup may not be consistent and it may not be possible to recover any data from it in future. Prevent writes to the repository by unregistering the repository from the cluster which has write access to it, or by registering it with `readonly: true`.

Alternatively, if your repository supports it, you may take an atomic snapshot of the underlying filesystem and then take a backup of this filesystem snapshot. It is very important that the filesystem snapshot is taken atomically.

::::{warning}
Do not rely on repository backups that were taken by methods other than the one described in this section. If you use another method to make a copy of your repository contents then the resulting copy may capture an inconsistent view of your data. Restoring a repository from such a copy may fail, reporting errors, or may succeed having silently lost some of your data.
::::


::::{warning}
Do not use filesystem snapshots of individual nodes as a backup mechanism. You must use the {{es}} snapshot and restore feature to copy the cluster contents to a separate repository. Then, if desired, you can take a filesystem snapshot of this repository.
::::


When restoring a repository from a backup, you must not register the repository with {{es}} until the repository contents are fully restored. If you alter the contents of a repository while it is registered with {{es}} then the repository may become unreadable or may silently lose some of its contents. After restoring a repository from a backup, use the [Verify repository integrity](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-repository-verify-integrity) API to verify its integrity before you start to use the repository.

