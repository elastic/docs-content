---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-getting-started-post-installation.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Post-installation steps [ece-getting-started-post-installation]

After your {{ece}} installation is up, some additional steps might be required. For a complete list of configurable features in ECE, refer to [](./configure.md).

::::{tip}
To start creating {{es}} deployments directly, refer to [](./working-with-deployments.md).
::::

* Add your own [load balancer](./ece-load-balancers.md). Load balancers are user supplied and we do not currently provide configuration steps for you.

* [Add more capacity](/deploy-manage/maintenance/ece/scale-out-installation.md) to your ECE installation, [resize your deployment](./resize-deployment.md), [upgrade to a newer {{es}} version](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ece.md), and [add some plugins](./add-plugins.md).

* [Configure ECE system deployments](./system-deployments-configuration.md) to ensure a highly available and resilient setup.

* [Configure ECE for deployment templates](./configure-deployment-templates.md) to indicate what kind of hardware you have available for {{stack}} deployments.

* In production systems, add your own [Cloud UI and Proxy certificates](../../security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md) to enable secure connections over HTTPS. The proxy certificate must be a wildcard certificate signed for the needed DNS records of your domain.

  ::::{note}
  The default DNS resolution provided by Elastic is not intended for production use. Refer to [](./ece-wildcard-dns.md) for more information.

  If you intend to use [custom endpoint aliases](./enable-custom-endpoint-aliases.md) functionality, ensure you add the necessary Subject Alternative Name (SAN) entries to the proxy certificate.
  ::::

* Optionally, if you want the deployment endpoint links and Single-sign on to work with your domain name, configure it as the **deployment domain name** in the **Platform** > **Settings** section of the [Cloud UI](./log-into-cloud-ui.md). The domain name is used to generate the endpoint URLs and must align with your proxy certificate and DNS record.

  ::::{tip}
  For example, if your proxy certificate is signed for `*.elastic-cloud-enterprise.example.com` and you have a wildcard DNS register pointing `*.elastic-cloud-enterprise.example.com` to your load balancer, you should configure `elastic-cloud-enterprise.example.com` as the **deployment domain name** in Platform → Settings. Refer to [](./change-endpoint-urls.md) for more details.
  ::::

* [Add a snapshot repository](../../tools/snapshot-and-restore/cloud-enterprise.md) to enable regular backups of your {{es}} clusters.

* [Add more platform users](../../users-roles/cloud-enterprise-orchestrator/manage-users-roles.md) with role-based access control.

* Consider enabling encryption-at-rest (EAR) on your hosts.

  :::{{note}}
  Encryption-at-rest is not implemented out of the box in {{ece}}. [Learn more](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation.md#ece_encryption).
  :::

* Set up [traffic filters](/deploy-manage/security/network-security.md) to restrict traffic to your deployment to only trusted IP addresses or VPCs.

* Learn how to work around host maintenance or a host failure by [moving nodes off of an allocator](/deploy-manage/maintenance/ece/move-nodes-instances-from-allocators.md). For an overview of common ECE maintenance activities, refer to [ECE maintenance](../../maintenance/ece.md).

* If you received a license from Elastic, [manage the licenses](../../license/manage-your-license-in-ece.md) for your {{ece}} installation.

::::{warning}
During installation, the system generates secrets that are placed into the `/mnt/data/elastic/bootstrap-state/bootstrap-secrets.json` secrets file, unless you passed in a different path with the --host-storage-path parameter. Keep the information in the `bootstrap-secrets.json` file secure by removing it from its default location and placing it into a secure storage location.
::::
