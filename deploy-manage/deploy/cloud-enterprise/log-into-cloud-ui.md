---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-login.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Log into the Cloud UI [ece-login]

To access the Cloud UI in a web browser:

1. Connect to the HTTPS URL provided at the end of the installation process on your first host, replacing `FIRST_HOST` with the correct IP address or DNS hostname.

    ```sh
    https://<FIRST_HOST>:12443
    ```

    :::{note}
    Starting with ECE 3.7.0, the Cloud UI requires HTTPS on port 12443. Ensure this port is open in your network policies.
    :::

    Secure access through the HTTPS protocol is available with certificates generated during the installation of {{ece}}, but will prompt you with a warning in your browser. To avoid this warning, you can add [your own TLS/SSL security certificates](../../security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md). If you are on AWS and can't access the Cloud UI, [check if the URL points to a private IP address](../../../troubleshoot/deployments/cloud-enterprise/common-issues.md#ece-aws-private-ip).

2. Log in as user `admin` with the credentials provided.
3. On your first login, agree to the software license agreement to continue. You can opt out of sharing some basic usage statistics with Elastic. [Here is what we collect.](statistics-collected-by-cloud-enterprise.md)

The Cloud UI displays the available deployments and some important information about them. Three deployments are always shown:

* `admin-console-elasticsearch`: Backs the Cloud UI itself.
* `logging-and-metrics`: Collects logs and performance metrics for your ECE installation. You must not use this deployment to index monitoring data from your own {{es}} clusters or use it to index data from Beats and Logstash. Always create a separate, dedicated monitoring deployment for your own use.
* `security`: Stores all security-related configurations.
