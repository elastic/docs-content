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


* [ECE scripts](cloud://reference/cloud-enterprise/scripts.md): Use the `elastic-cloud-enterprise.sh` script to install {{ece}} or modify your installation.
* [ECE diagnostics tool](/troubleshoot/deployments/cloud-enterprise/run-ece-diagnostics-tool.md): Collect logs and metrics that you can send to Elastic Support for troubleshooting and investigation purposes.

**API**

% ECE API links and information are still pending
* [Elastic Cloud Enterprise RESTful API](cloud://reference/cloud-enterprise/restful-api.md)

## {{es}} API Console [ece-api-console]

With the {{es}} API console, you can interact with a specific {{es}} deployment directly from the Cloud UI without having to authenticate again. This RESTful API access is limited to the specific cluster and works only for {{es}} API calls.

You can find this console in the Cloud UI when selecting a specific deployment to manage. From the {{es}} menu, select **API Console**.

:::{note}
This API Console is different from the [Dev Tools Console](/explore-analyze/query-filter/tools/console.md) available in {{kib}}, from which you can call {{es}} and {{kib}} APIs. On the ECE API Console, you cannot run {{kib}} APIs.

This API console is intended for admin purposes. Avoid running normal workload like indexing or search requests.
:::

## Elastic Cloud Control: command-line interface for {{ecloud}}

Elastic Cloud Control (ECCTL) is the command-line interface for {{ecloud}} APIs. It wraps typical operations commonly needed by operators within a single command line tool.

ECCTL provides the following benefits: 

- Easier to use than the {{ecloud}} Console or using the RESTful API directly
- Helps you automate the deployment lifecycle
- Provides a foundation for integration with other tools

Find more details in the [ECCTL documentation](ecctl://reference/index.md).

## Provision hosted deployments with Terraform
```{applies_to}
deployment:
  ess: ga
serverless: unavailable
```

The {{ecloud}} Terraform provider allows you to provision and manage {{ech}} and {{ece}} deployments as code, and introduce DevOps-driven methodologies to manage and deploy the {{stack}} and solutions.

To get started, see the [{{ecloud}} Terraform provider documentation](https://registry.terraform.io/providers/elastic/ec/latest/docs).




