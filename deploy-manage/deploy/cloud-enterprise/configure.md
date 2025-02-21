---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-ece.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-administering-ece.html
---

# Configure ECE [ece-configuring-ece]

⚠️ **This page is a work in progress.** ⚠️

Now that you have Elastic Cloud Enterprise up and running, take a look at some of the additional features that you can configure:

* [System deployment configuration](system-deployments-configuration.md) - Best practices for ECE system deployments to ensure a highly available and resilient setup.
* [Configure deployment templates](configure-deployment-templates.md) - Make the most out of deployment templates by configuring ECE for your hardware and creating custom deployment templates.
* [Manage snapshot repositories](../../tools/snapshot-and-restore/cloud-enterprise.md) - To back up your Elasticsearch clusters automatically, you need to configure a snapshot repository.
* [Manage licenses](../../license/manage-your-license-in-ece.md) - Keep Elastic Cloud Enterprise current with a valid license.
* [Change endpoint URLs](change-endpoint-urls.md) - Set where Elasticsearch and Kibana can be accessed from.
* [Configure allocator affinity](configure-allocator-affinity.md) - Determine how ECE distributes your Elastic Stack deployments across allocators.
* [Change allocator disconnect timeout](change-allocator-disconnect-timeout.md) - Configure how long ECE waits before considering allocators to be disconnected.
* [Migrate ECE on Podman hosts to SELinux in enforcing mode](migrate-ece-on-podman-hosts-to-selinux-enforce.md) - Migrate ECE to SELinux in `enforcing` mode using Podman.

## Administering your installation [ece-administering-ece]

Now that you have Elastic Cloud Enterprise up and running, take a look at the things you can do to keep your installation humming along, from adding more capacity to dealing with hosts that require maintenance or have failed. They are all presented in the [](../../maintenance.md) section.

* [Scale Out Your Installation](../../../deploy-manage/maintenance/ece/scale-out-installation.md) - Need to add more capacity? Here’s how.
* [Assign Roles to Hosts](../../../deploy-manage/deploy/cloud-enterprise/assign-roles-to-hosts.md) - Make sure new hosts can be used for their intended purpose after you install ECE on them.
* [Enable Maintenance Mode](../../../deploy-manage/maintenance/ece/enable-maintenance-mode.md) - Perform administrative actions on allocators safely by putting them into maintenance mode first.
* [Move Nodes From Allocators](../../../deploy-manage/maintenance/ece/move-nodes-instances-from-allocators.md) - Moves all Elasticsearch clusters and Kibana instances to another allocator, so that the allocator is no longer used for handling user requests.
* [Delete Hosts](../../../deploy-manage/maintenance/ece/delete-ece-hosts.md) - Remove a host from your ECE installation, either because it is no longer needed or because it is faulty.
* [Perform Host Maintenance](../../../deploy-manage/maintenance/ece/perform-ece-hosts-maintenance.md) - Apply operating system patches and other maintenance to hosts safely without removing them from your ECE installation.
* [Manage Elastic Stack Versions](../../../deploy-manage/deploy/cloud-enterprise/manage-elastic-stack-versions.md) - View, add, or update versions of the Elastic Stack that are available on your ECE installation.
* [Upgrade Your Installation](../../../deploy-manage/upgrade/orchestrator/upgrade-cloud-enterprise.md) - A new version of Elastic Cloud Enterprise is available and you want to upgrade. Here’s how.


