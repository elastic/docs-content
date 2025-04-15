---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-restore-across-clusters.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-restore-across-clusters.html
applies_to:
  deployment:
    ess:
    ece:
---

# Restore a snapshot across clusters [ece-restore-across-clusters]

Snapshots can be restored to either the same {{es}} cluster or to another cluster. If you are restoring all indices to another cluster, you can [clone](/deploy-manage/tools/snapshot-and-restore/ece-restore-snapshots-into-new-deployment.md) a cluster.

::::{note}
Users created using the X-Pack security features or using Shield are not included when you restore across clusters, only data from {{es}} indices is restored. If you do want to create a cloned cluster with the same users as your old cluster, you need to recreate the users manually on the new cluster.
::::


Restoring to another cluster is useful for scenarios where isolating activities on a separate cluster is beneficial, such as:

Performing ad hoc analytics
:   For most logging and metrics use cases, it is cost prohibitive to have all the data in memory, even if it would provide the best performance for aggregations. Cloning the relevant data to an ad hoc analytics cluster that can be discarded after use is a cost effective way to experiment with your data, without risk to existing clusters used for production.

Enabling your developers
:   Realistic test data is crucial for uncovering unexpected errors early in the development cycle. What can be more realistic than actual data from a production cluster? Giving your developers access to real production data is a great way to break down silos.

Testing mapping changes
:   Mapping changes almost always require reindexing. Unless your data volume is trivial, reindexing requires time and tweaking the parameters to achieve the best reindexing performance usually takes a little trial and error. While this use case could also be handled by running the scan and scroll query directly against the source cluster, a long lived scroll has the side effect of blocking merges even if the scan query is very light weight.

Integration testing
:   Test your application against a real live {{es}} cluster with actual data. If you automate this, you could also aggregate performance metrics from the tests and use those metrics to detect if a change in your application has introduced a performance degradation.

In **{{ech}}**, a cluster is eligible as a destination for a snapshot restore if it meets these criteria:

- The cluster is in the same region. For example, a snapshot taken in `eu-west-1` cannot be restored to `us-east-1` at this point. If you need to restore snapshots across regions, create the destination deployment, connect to the [custom repository](/deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md#ess-repo-types), and then [restore from a snapshot](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md).
- The destination cluster is able to read the indices. You can generally restore to your {{es}} cluster snapshots of indices created back to the previous major version, but see the [version matrix](../snapshot-and-restore.md#snapshot-restore-version-compatibility) for all the details.

The list of available snapshots can be found in the found-snapshots repository.

In **{{ece}}**, a cluster is eligible as a destination for a snapshot restore if it meets these criteria:

- The destination cluster is able to read the indices. You can generally restore to your {{es}} cluster snapshots of indices created back to the previous major version, but see the [version matrix](../snapshot-and-restore.md#snapshot-restore-version-compatibility) for all the details.

To restore built-in snapshots across clusters, there are two options:

* [Restore snapshot into a new deployment](ece-restore-snapshots-into-new-deployment.md)
* [Restore snapshot into an existing deployment](ece-restore-snapshots-into-existing-deployment.md)

When restoring snapshots across clusters on {{ech}} or {{ece}}, the platform creates a new repository called `\_clone_{{clusterIdPrefix}}`, which persists until manually deleted. If the repository is still in use, for example by mounted searchable snapshots, it can’t be removed.

::::{warning}
When restoring from a deployment that’s using searchable snapshots, refer to [Restore snapshots containing searchable snapshots indices across clusters](ece-restore-snapshots-containing-searchable-snapshots-indices-across-clusters.md).
::::
