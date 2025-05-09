---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-snapshot-repository-migration.html
applies_to:
  deployment:
    ess:
---

# Access isolation for the found-snapshots repository [ec-snapshot-repository-migration]

In {{ech}}, access isolation ensures that each deployment can access only its own snapshots, preventing accidental or unauthorized access to backups from other deployments within the same organization.

Any newly created deployment has snapshot isolation set up by default. The guides in these section apply only to older deployments created before this default was implemented, where deployments within the same region may still have access to each other’s snapshots.

If a deployment can access the snapshots of other deployments, a notification will appear in the deployments menu under **{{es}} > Snapshots**, prompting you to set up access isolation.

The process for enabling access isolation depends on your cloud provider:

* [Azure deployments](/deploy-manage/tools/snapshot-and-restore/repository-isolation-on-aws-gcp.md)
* [AWS & GCP deployments](/deploy-manage/tools/snapshot-and-restore/repository-isolation-on-azure.md)



