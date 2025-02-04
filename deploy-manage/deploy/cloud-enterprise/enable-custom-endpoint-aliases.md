---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-deployment-aliases.html
---

# Enable custom endpoint aliases [ece-configuring-deployment-aliases]

Custom endpoint aliases allow users to replace the UUID for each application with a human readable string. Platform administrators must enable this feature to allow deployment managers to create and modify aliases for their deployments.

::::{note} 
You need to update your proxy certificates to support this feature.
::::


After installing or upgrading to version 2.10 or later:

1. [Login to the Cloud UI](log-into-cloud-ui.md)
2. [Update your proxy certificate(s)](../../security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md). In addition to currently configured domains, additional SAN entries must be configured for each application-specific subdomain:

    ::::{note} 
    If you are not using wildcard certificates, you need to repeat this process for each deployment to account for specific aliases.
    ::::


    * For Elasticsearch, the certificate needs to allow for ***.es.<your-domain>**
    * For Kibana, the certificate needs to allow for ***.kb.<your-domain>**
    * For APM, the certificate needs to allow for ***.apm.<your-domain>**
    * For Enterprise Search or AppSearch, the certificate needs to allow for ***.ent.<your-domain>**
    * For Fleet, the certificate needs to allow for ***.fleet.<your-domain>**

3. In the **Platform** menu, select **Settings**.
4. Under the **Enable custom endpoint alias naming**, toggle the setting to allow platform administrators and deployment managers to choose a simplified, unique URL for the endpoint.

If you do not perform these steps, application endpoints will behave as they did in versions before 2.10.

To learn about setting up custom endpoint aliases for your deployments, check [Custom endpoint aliases](ece-regional-deployment-aliases.md).


