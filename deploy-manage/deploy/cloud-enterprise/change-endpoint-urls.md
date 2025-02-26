---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-administering-endpoints.html
---

# Change endpoint URLs [ece-administering-endpoints]

For applications without SSL or HTTPS protocol support, you can use a local endpoint with the HTTP protocol, which in turn connects to your Elasticsearch cluster or to Kibana either using the HTTP or the HTTPS protocol.

By default, cluster and Kibana endpoint URLs are constructed according to the following pattern, where `CLUSTER_ID` and `LOCAL_HOST_IP` are values that depend on your specific installation:

::::{admonition}
```text
http://CLUSTER_ID.LOCAL_HOST_IP.ip.es.io:9200
https://CLUSTER_ID.LOCAL_HOST_IP.ip.es.io:9243
```

::::


For example:

```sh
http://2882c82e54d4361.us-west-5.aws.found.io:9200
https://2882c82e54d4361.us-west-5.aws.found.io:9243
```

::::{tip}
To find your endpoints, select a deployment review the information on the **Elasticsearch** and **Kibana** pages.
::::


To change endpoints in the Cloud UI:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. From the **Platform** menu, select **Settings**.
3. Specify the deployment domain name value for your cluster and Kibana endpoints.
4. Select **Update Deployment endpoints**. The new endpoint becomes effective immediately.

::::{tip}
If you install Elastic Cloud Enterprise on AWS, you likely need to modify the cluster endpoint. To learn more, check [Endpoint URLs Inaccessible on AWS](../../../troubleshoot/deployments/cloud-enterprise/common-issues.md#ece-aws-private-ip).
::::


::::{tip}
If you have an App Search instance, after specifying a new deployment domain name value you need to reapply the App Search [cluster configuration](advanced-cluster-configuration.md), either with or without any changes.
::::


::::{note}
The built-in Proxy Certificate only validates against the default endpoint format described on this page. Once you change it, it is necessary to upload a new Proxy Certificate as described in [Manage security certificates](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md). For test only, clients can be configured with hostname verification disabled until the new certificate is uploaded.
::::


