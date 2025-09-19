---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-snapshot-repository-aws-gcp-migration.html
applies_to:
  deployment:
    ess:
products:
  - id: cloud-hosted
navigation_title: AWS and GCP
---

# Repository isolation on AWS and GCP [ec-snapshot-repository-aws-gcp-migration]

::::{note}
This configuration is automatic for all newly created deployments, but may be necessary for some existing deployments you have. If a deployment is not yet using an isolated snapshot repository, a notification will show up in the deployments menu under **Elasticsearch** > **Snapshots**.
::::


Deployments of your organization in the same region currently may have access to each other’s snapshots via the Elastic provided `found-snapshots` repository. For improved security between deployments, each deployment should only have access to its own snapshots.

If a deployment can still access the snapshots of other deployments, a notification will show up in the deployments menu under **Elasticsearch** > **Snapshots**. After applying the action, the notification will disappear.


## Removing a repository of another deployment [ec_removing_a_repository_of_another_deployment]

The deployment may have access to other deployments if it has been restored from a snapshot. If this is the case, the access permissions will be listed under **Elasticsearch** > **Snapshots** under the title **Snapshot repositories of other deployments**.

If you no longer need access to the snapshot of another deployment, you can remove the access. By doing this, you prevent accessing snapshots of other deployments from this deployment:

1. From your deployment menu, go to **Elasticsearch** > **Snapshots**.
2. On the **Snapshots** page, **Snapshot repositories of other deployments** shows the old repository.
3. With **Remove Access**, the snapshot repository will be removed.

::::{note}
If the repository is still in use (for example by mounted searchable snapshots), it can’t be removed. Remove any indices stored in this repository first.
::::


:::{image} /deploy-manage/images/cloud-ec-elasticsearch-snapshots-of-other-deployments-aws-gcp.png
:alt: View of the old snapshot repository in the Cloud UI
:::

