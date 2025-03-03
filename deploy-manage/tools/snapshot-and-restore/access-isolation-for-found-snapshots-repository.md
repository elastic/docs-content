---
applies_to:
  deployment:
    ess: 
---

# Access isolation for the found-snapshots repository [ec-snapshot-repository-migration]

In {{ech}}, [snapshots](/deploy-manage/tools/snapshot-and-restore.md) are stored in a repository. By default, deployments in the same region may have access to each other’s snapshots through the `found-snapshots` repository.

To enhance security, access isolation ensures that each deployment can only access its own snapshots. This prevents accidental or unauthorized access to backups from other deployments within the same organization.


The process for enabling access isolation depends on your cloud provider:

* [Azure deployments](/deploy-manage/tools/snapshot-and-restore/repository-isolation-on-aws-gcp.md)
* [AWS & GCP deployments](/deploy-manage/tools/snapshot-and-restore/repository-isolation-on-azure.md)



