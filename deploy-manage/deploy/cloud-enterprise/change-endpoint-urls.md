---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-administering-endpoints.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Change endpoint URLs [ece-administering-endpoints]

{{es}} and {{kib}} endpoint URLs are constructed using the `CLUSTER_ID` of the component ({{es}} or {{kib}}), and the domain name (`CNAME`) configured in the **Deployment Endpoints** section of the **Platform > Settings** UI.

By default, the deployments `CNAME` is set to `LOCAL_HOST_IP.ip.es.io`, where `LOCAL_HOST_IP` is the IP address of the first installed ECE host. This results in the following default endpoint URLs:

```sh
http://<CLUSTER_ID.LOCAL_HOST_IP>.ip.es.io:9200
https://<CLUSTER_ID.LOCAL_HOST_IP>.ip.es.io:9243
```

::::{important}
For security reasons, it is recommended to use **HTTPS (9243)** whenever possible.
::::

To change endpoints in the Cloud UI:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. From the **Platform** menu, select **Settings**.
3. Specify the deployment domain name (`CNAME`) value for your cluster and {{kib}} endpoints.
4. Select **Update Deployment endpoints**. The new endpoint becomes effective immediately.

To find your deployment endpoints, select a deployment and review the information on the **Elasticsearch** and **Kibana** pages.

::::{tip}
If you install {{ece}} on AWS, you likely need to modify the cluster endpoint. To learn more, check [Endpoint URLs Inaccessible on AWS](../../../troubleshoot/deployments/cloud-enterprise/common-issues.md#ece-aws-private-ip).
::::

::::{tip}
If you have an App Search instance, after specifying a new deployment domain name value you need to reapply the App Search [cluster configuration](advanced-cluster-configuration.md), either with or without any changes.
::::

::::{note}
The built-in Proxy Certificate only validates against the default endpoint format described on this page. Once you change it, it is necessary to upload a new Proxy Certificate as described in [Manage security certificates](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md). For test only, clients can be configured with hostname verification disabled until the new certificate is uploaded.
::::

::::{note}
If you do not use wildcard certificates, you must configure SAN entries for each component of the deployment (for example, {{es}} or {{kib}}) and repeat this process for every deployment. Review [Wildcard DNS record and certificates](./ece-wildcard-dns.md) for more guidance.
::::