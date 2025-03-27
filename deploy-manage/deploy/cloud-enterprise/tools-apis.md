---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-api-console.html
---
# Tools and APIs

% What needs to be done: Write from scratch

% GitHub issue: https://github.com/elastic/docs-projects/issues/310

 ⚠️ **This page is a work in progress.** ⚠️

You can use these tools and APIs to interact with the following {{ece}} features:

* [{{ecloud}} Control (ecctl)](ecctl://reference/index.md): Wraps typical operations commonly needed by operators within a single command line tool.
* [ECE scripts](cloud://reference/cloud-enterprise/scripts.md): Use the `elastic-cloud-enterprise.sh` script to install {{ece}} or modify your installation.
* [ECE diagnostics tool](/troubleshoot/deployments/cloud-enterprise/run-ece-diagnostics-tool.md): Collect logs and metrics that you can send to Elastic Support for troubleshooting and investigation purposes.
* [Elasticsearch API console](#ece-api-console)

**API**

% ECE API links and information are still pending
* [Elastic Cloud Enterprise RESTful API](cloud://reference/cloud-enterprise/restful-api.md)

## {{es}} API Console [ece-api-console]

With the API console you can interact with a specific {{es}} deployment directly from the Cloud UI without having to authenticate again. This RESTful API access is limited to the specific cluster and works only for Elasticsearch API calls.

::::{important}
API console is intended for admin purposes. Avoid running normal workload like indexing or search requests.
::::

You can find this console in Cloud UI when selecting a specific deployment to manage. From the {{es}} menu, select **API Console**.

:::{note}
This API Console is different from the [Dev Tools Console](/explore-analyze/query-filter/tools/console.md) available in {{kib}}, from which you can call {{es}} and {{kib}} APIs. On the ECE API Console, you cannot run Kibana APIs.
:::

To learn more about what kinds of {{es}} API calls you can make from the Cloud UI, check the [Elasticsearch API Reference](elasticsearch://reference/elasticsearch/rest-apis/index.md) documentation.





