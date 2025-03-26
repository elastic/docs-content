---
applies_to:
  deployment:
    ess: ga
  serverless: ga
mapped_urls:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-http-apis.html
  - https://www.elastic.co/guide/en/tpec/current/index.html
navigation_title: "Tools and APIs"
---

# Tools and APIs for {{ecloud}}

% What needs to be done: Write from scratch

% GitHub issue: https://github.com/elastic/docs-projects/issues/310

% Scope notes: elastic cloud control  does this work for serverless/cloud together?

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/docs-content/serverless/elasticsearch-http-apis.md
% - [ ] https://www.elastic.co/guide/en/tpec/current/index.html
%      Notes: reference only, this page wasn't migrated, but you can pull from the live URL if needed.

## REST APIs to orchestrate {{ecloud}}

The following APIs allow you to manage your {{ecloud}} organization, users, security, billing and resources.

| Deployment type | API | Tasks |
| --- | --- | --- |
| {{serverless-full}} | [{{serverless-full}} API](https://www.elastic.co/docs/api/doc/elastic-cloud-serverless) | Manage {{serverless-full}} projects. |
| {{ech}} | [{{ecloud}} API](https://www.elastic.co/docs/api/doc/cloud/) | Manage your hosted deployments and all of the resources associated with them. This includes performing deployment CRUD operations, scaling or autoscaling resources, and managing traffic filters, deployment extensions, remote clusters, and {{stack}} versions. You can also access cost data by deployment and by organization. |


## REST APIs to interact with data and solution features

The following APIs allow you to interact with your {{es}} cluster, its data, and the features available to you in your {{ech}} deployment or {{serverless-full}} project.

Note that some [restrictions](/deploy-manage/deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-apis-elasticsearch) apply when using the these APIs on {{ecloud}}.

### {{serverless-full}}

The following APIs are available for {{es-serverless}} users:

- [{{es}} {{serverless-short}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch-serverless): Use these APIs to index, manage, search, and analyze your data in {{es-serverless}}. 
  
  Learn how to [connect to your {{es-serverless}} endpoint](/solutions/search/get-started.md).
- [{{kib}} {{serverless-short}} APIs](https://www.elastic.co/docs/api/doc/serverless): Use these APIs to manage resources such as connectors, data views, and saved objects for your {{serverless-full}} project.

### {{ech}}

The following APIs are available for {{ech}} users:

- [{{es}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch/): This set of APIs allows you to interact directly with the {{es}} nodes in your deployment. You can ingest data, run search queries, check the health of your clusters, manage snapshots, and more.
- [{{kib}} APIs](https://www.elastic.co/docs/api/doc/kibana/): Many {{kib}} features can be accessed through these APIs, including {{kib}} objects, patterns, and dashboards, as well as user roles and user sessions. You can use these APIs to configure alerts and actions, and to access health details for the [{{kib}} Task Manager](/deploy-manage/distributed-architecture/kibana-tasks-management.md).

### Additional resources

Refer to [{{es}} API conventions](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md) to learn about headers and request body conventions for {{es-serverless}} and {{es}} REST APIs.

## {{ecloud}} API console
```{applies_to}
deployment:
  ess: ga
serverless: unavailable
```

With the {{es}} API console, you can interact with a specific {{es}} deployment directly from the {{ecloud}} Console without having to authenticate again. This RESTful API access is limited to the specific cluster and works only for {{es}} API calls.

You can find this console in the {{ecloud}} Console when selecting a specific deployment to manage. From the {{es}} menu, select **API Console**.

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
