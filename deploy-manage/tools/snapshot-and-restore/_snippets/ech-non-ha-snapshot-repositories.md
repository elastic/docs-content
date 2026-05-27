:::::{important} Snapshot repositories and single-zone deployments
If your deployment runs in a **single availability zone** (one data center), it is not highly available. Node or infrastructure failures can require you to [restore data from a snapshot](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md).

**Registered snapshot repositories are not stored in snapshots.** A restore recovers index data and, if you choose, parts of the cluster state from the snapshot. It does **not** restore which snapshot repositories were registered on the cluster. Repository registration lives in cluster metadata and must exist **before** you can run a snapshot restore.

On a single-zone deployment, that cluster metadata can be lost when nodes fail. Restore operations can then fail with repository errors—even when snapshot files still exist in storage.

**`found-snapshots` (default):** {{ech}} registers and manages this repository for you. If it is missing after an outage, you cannot recreate it yourself. Edit and save your deployment configuration (no other changes required) to trigger a deployment plan that re-registers the repository, or [contact Elastic Support](/troubleshoot/index.md#contact-us).

**Custom repositories (S3, GCS, Azure, and so on):** You must [re-register the repository](/deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md#register-snapshot-repos-ech) with the same name, type, and settings as before the failure (including credentials in the deployment keystore where applicable). Document your repository configuration outside the cluster so you can restore registration after an outage.

Verify registration before you restore:

```console
GET _snapshot/_all
```

For production workloads, use [at least two availability zones](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-ha) and configure index replicas. See [Plan for production](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-ha) and [Fault tolerance](/deploy-manage/deploy/elastic-cloud/ec-customize-deployment-components.md#ec-high-availability).
:::::
