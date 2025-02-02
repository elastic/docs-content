---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-getting-started-post-installation.html
---

# Post-installation steps [ece-getting-started-post-installation]

After your Elastic Cloud Enterprise installation is up, some additional steps might be required:

* Add your own load balancer. Load balancers are user supplied and we do not currently provide configuration steps for you.
* [Add more capacity](../../maintenance/ece/scale-out-installation.md) to your Elastic Cloud Enterprise installation, [resize your deployment](resize-deployment.md), [upgrade to a newer Elasticsearch version](../../upgrade/deployment-or-cluster.md), and [add some plugins](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-add-plugins.html).
* [Configure ECE system deployments](system-deployments-configuration.md) to ensure a highly available and resilient setup.
* [Configure ECE for deployment templates](configure-deployment-templates.md) to indicate what kind of hardware you have available for Elastic Stack deployments.
* [Install your security certificates](../../security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md) to enable TLS/SSL authentication for secure connections over HTTPS.
* [Add a snapshot repository](../../tools/snapshot-and-restore/cloud-enterprise.md) to enable regular backups of your Elasticsearch clusters.
* [Add more platform users](../../users-roles/cloud-enterprise-orchestrator/manage-users-roles.md) with role-based access control.
* Consider enabling encryption-at-rest (EAR) on your hosts.
* [Set up traffic filters](../../security/traffic-filtering.md) to restrict traffic to your deployment to only trusted IP addresses or VPCs.
* Learn how to work around host maintenance or a host failure by [moving nodes off of an allocator](../../maintenance/ece/move-nodes-instances-from-allocators.md).
* If you received a license from Elastic, [manage the licenses](../../license/manage-your-license-in-ece.md) for your Elastic Cloud Enterprise installation.

::::{warning} 
During installation, the system generates secrets that are placed into the `/mnt/data/elastic/bootstrap-state/bootstrap-secrets.json` secrets file, unless you passed in a different path with the --host-storage-path parameter. Keep the information in the `bootstrap-secrets.json` file secure by removing it from its default location and placing it into a secure storage location.
::::


