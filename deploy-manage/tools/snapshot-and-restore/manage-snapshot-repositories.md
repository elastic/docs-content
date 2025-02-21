---
applies_to:
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
---

# Manage snapshot repositories

Snapshot repositories allow you to back up and restore your Elasticsearch data efficiently. Whether you're using [{{ech}}](#elastic-cloud-hosted), [{{ece}} (ECE)](#elastic-cloud-enterprise-ece), [{{eck}} (ECK)](#elastic-cloud-on-kubernetes-eck), or managing your own [{{es}} cluster](#self-managed), configuring a snapshot repository ensures data security, long-term archiving, and seamless migration across environments.

## Supported repository types

### Self-managed

If you manage your own Elasticsearch cluster, you can use the following built-in snapshot repository types:

* [Azure](/deploy-manage/tools/snapshot-and-restore/azure-repository.md)
* [Google Cloud Storage](/deploy-manage/tools/snapshot-and-restore/google-cloud-storage-repository.md)
* [AWS S3](/deploy-manage/tools/snapshot-and-restore/s3-repository.md)
* [Shared file system](/deploy-manage/tools/snapshot-and-restore/shared-file-system-repository.md)
* [Read-only URL](/deploy-manage/tools/snapshot-and-restore/read-only-url-repository.md)
* [Source-only](/deploy-manage/tools/snapshot-and-restore/source-only-repository.md)

Other repository types are available through official plugins:

* [Hadoop Distributed File System (HDFS)](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch-plugins/repository-hdfs.md)

### Elastic Cloud Hosted

{{ech}} deployments automatically register a repository named `found-snapshots` in {{es}} clusters. These repositories are used together with the `cloud-snapshot-policy` SLM policy to take periodic snapshots of your {{es}} clusters. You can also use the `found-snapshots` repository for your own [SLM policies](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm) or to store searchable snapshots.

The `found-snapshots` repository is specific to each deployment. However, you can restore snapshots from another deployment’s found-snapshots repository if the deployments are under the same account and in the same region. 

Elastic Cloud Hosted deployments also support the following repository types:

* [Azure](/deploy-manage/tools/snapshot-and-restore/ec-azure-snapshotting.md)
* [Google Cloud Storage](/deploy-manage/tools/snapshot-and-restore/ec-gcs-snapshotting.md)
* [AWS S3](/deploy-manage/tools/snapshot-and-restore/ec-aws-custom-repository.md)
* [Source-only](/deploy-manage/tools/snapshot-and-restore/source-only-repository.md)

For more details, refer to [Registering snapshot repositories in Elastic Cloud Hosted](/deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md).

### Elastic Cloud Enterprise (ECE)

Snapshot repositories are managed at the platform level in Elastic Cloud Enterprise (ECE) and can be associated with deployments as needed. ECE supports the creation and maintenance of multiple repositories, but each deployment can be linked to only one repository for automatic snapshots.

When a platform-level repository is associated with a deployment, the `found-snapshots` repository is added to the {{es}} cluster, and, similar to Elastic Cloud, a snapshot is taken every 30 minutes by default. The interval can be adjusted on per deployment basis.

Elastic Cloud Enterprise installations support the following Elasticsearch snapshot repository types:

* [AWS S3](/deploy-manage/tools/snapshot-and-restore/ece-aws-custom-repository.md)
* [Azure](/deploy-manage/tools/snapshot-and-restore/azure-storage-repository.md)
* [Google Cloud Storage](/deploy-manage/tools/snapshot-and-restore/google-cloud-storage-gcs-repository.md)
* [Minio](/deploy-manage/tools/snapshot-and-restore/minio-on-premise-repository.md)

:::{note}
No repository types other than those listed are supported in the Elastic Cloud Enterprise platform, even if they are supported by Elasticsearch. 
:::

For more details, refer to [Managing snapshot repositories in Elastic Cloud Enterprise](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md).

### Elastic Cloud on Kubernetes (ECK)

{{es}} clusters deployed through ECK support the same type of deployments as self-managed {{es}} clusters. ECK does not currently provide any automation or functionality to facilitate the integration of snapshot repositores within the {{es}} clusters.

For more information and examples, refer to [create automated snapshots on ECK](/deploy-manage/tools/snapshot-and-restore/cloud-on-k8s.md).