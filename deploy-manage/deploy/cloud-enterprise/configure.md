---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-ece.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-administering-ece.html
---

# Configure ECE [ece-configuring-ece]

Now that you have {{ece}} up and running, take a look at some of the additional features that you can configure:

## Common ECE tasks

* [Assign roles to hosts](../../../deploy-manage/deploy/cloud-enterprise/assign-roles-to-hosts.md) - Make sure new hosts can be used for their intended purpose after you install ECE on them.
* [System deployments configuration](system-deployments-configuration.md) - Best practices for ECE system deployments to ensure a highly available and resilient setup.
* [Configure deployment templates](configure-deployment-templates.md) – Define the resources, topology, hardware, and configurations that will be applied to your deployments.
* [Manage {{stack}} versions](./manage-elastic-stack-versions.md) - Upload or remove {{stack}} packs.
* [Change the ECE API URL](./change-ece-api-url.md) - Configure the HTTPS URL used to access the ECE API.
* [Change endpoint URLs](change-endpoint-urls.md) - Configure the URLs to access {{es}} and {{kib}} deployments to match your [domain name](./ece-wildcard-dns.md) and [proxy certificate](../../security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md).
* [Enable custom endpoint aliases](./enable-custom-endpoint-aliases.md) - This feature allows to use aliases in the endpoint URLs instead of cluster UUIDs.

Other sections of the documentation describe important ECE features to consider:

* [Configure ECE users and roles](../../users-roles/cloud-enterprise-orchestrator.md) - Manage authentication and authorization at ECE platform level.
* [Manage security certificates](../../security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md) - Configure Cloud UI and Proxy TLS/SSL certificates.
* [Manage licenses](../../license/manage-your-license-in-ece.md) - Keep {{ece}} current with a valid license.
* [Manage snapshot repositories](../../tools/snapshot-and-restore/cloud-enterprise.md) - To back up your {{es}} clusters automatically, you need to configure a snapshot repository.

## Advanced configuration procedures

* [Configure allocator affinity](configure-allocator-affinity.md) - Determine how ECE distributes your {{stack}} deployments across allocators.
* [Change allocator disconnect timeout](change-allocator-disconnect-timeout.md) - Configure how long ECE waits before considering allocators to be disconnected.
* [Migrate ECE to Podman hosts](./migrate-ece-to-podman-hosts.md) - If you are running a Docker based installation and you need to migrate to Podman.
* [Migrate ECE on Podman hosts to SELinux in enforcing mode](../../security/secure-your-elastic-cloud-enterprise-installation/migrate-ece-on-podman-hosts-to-selinux-enforce.md) - Migrate ECE to SELinux in `enforcing` mode using Podman.

## Maintenance activities

Refer to [ECE maintenance](../../maintenance/ece.md) for important maintenance activities, including adding capacity, applying OS patches, and addressing host failures.

* [Scale out your installation](../../../deploy-manage/maintenance/ece/scale-out-installation.md) - Need to add more capacity? Here’s how.
* [Enable maintenance mode](../../../deploy-manage/maintenance/ece/enable-maintenance-mode.md) - Perform administrative actions on allocators safely by putting them into maintenance mode first.
* [Move nodes from allocators](../../../deploy-manage/maintenance/ece/move-nodes-instances-from-allocators.md) - Moves all {{es}} clusters and {{kib}} instances to another allocator, so that the allocator is no longer used for handling user requests.
* [Perform host maintenance](../../../deploy-manage/maintenance/ece/perform-ece-hosts-maintenance.md) - Apply operating system patches and other maintenance to hosts safely without removing them from your ECE installation.
* [Delete hosts](../../../deploy-manage/maintenance/ece/delete-ece-hosts.md) - Remove a host from your ECE installation, either because it is no longer needed or because it is faulty.
