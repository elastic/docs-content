---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-monitoring-ece-access.html
applies_to:
  deployment:
    ece: all
---

# Platform monitoring deployment logs and metrics [ece-monitoring-ece-access]

On the **{{es}}** page, the following logs and metrics are available:

| Log or metric | Description |
| --- | --- |
| {{es}} logs | Detailed logs related to cluster state. |
| {{es}} metrics | Detailed metrics for CPU and memory usage, running processes, networking and file system performance, and more. |
| Proxy logs | Search and indexing requests that proxies have sent to the {{es}} cluster. |

If a {{kib}} instance exists for the deployment, the following {{kib}} logs and metrics are also available from the **{{kib}}** page:

| Log or metric | Description |
| --- | --- |
| {{kib}} logs | Detailed logs related to instance state. |
| {{kib}} metrics | Detailed metrics for CPU and memory usage, running processes, networking and file system performance, and more. |
| Proxy logs | Requests that proxies have sent to the {{kib}} instance. |

## Access logs and metrics

To access logs and metrics for your deployment:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. Depending on the logs or metrics that you want to access, click on the **Elasticsearch** or **Kibana** page.

    ::::{tip} 
    If you have a license from 2018 or earlier, you might receive a warning that your cluster license is about to expire. Don’t panic, it isn’t really. {{ece}} manages the cluster licenses so that you don’t have to. In rare cases, such as when a cluster is overloaded, it can take longer for {{ece}} to reapply the cluster license. If you have a license from 2019 and later, you’ll receive a warning only when your full platform license is about to expire, which you’ll need to renew.
    ::::

4. Select one of the links and log in with the `elastic` user of the `logging-and-metrics` deployment. If you do not know the password, you can [reset it first](../../users-roles/cluster-or-deployment-auth/built-in-users.md).

    ::::{tip} 
    The password you specify must be for the `elastic` user on the `logging-and-metrics` cluster, where the logging and metrics indices are collected. If you need to reset the password for the user, make sure you reset for the `logging-and-metrics` cluster.
    ::::


    After you select one of the links, {{kib}} opens and shows you a view of the monitoring metrics for the logs or metrics that you selected.


If you are looking for an {{es}} or {{kib}} diagnostic to share with Elastic support, go to the **Operations** page for the deployment and download the diagnostic bundle to attach to your ticket. If logs or an ECE diagnostic are requested by Elastic support, [run the ECE diagnostics tool](../../../troubleshoot/deployments/cloud-enterprise/run-ece-diagnostics-tool.md).
