---
navigation_title: Tools and APIs
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-http-apis.html
  - https://www.elastic.co/guide/en/tpec/current/index.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-serverless
  - id: cloud-terraform
---

# Tools and APIs for {{ecloud}}

Review key resources that can be used to interact with and manage your {{ecloud}} organization, {{ech}} deployments, and {{serverless-full}} projects.

## APIs

You can use the following APIs in an {{ecloud}} environment.

:::{tip}
Refer to [](/deploy-manage/api-keys.md) to learn how to generate API keys for your environment.
:::

### Orchestration APIs

The following REST APIs allow you to manage your {{ecloud}} organization, users, security, billing and resources.

| Area | API | Tasks |
| --- | --- | --- |
| {{ecloud}} organization<br><br>{{ech}} deployments | [{{ecloud}} API](https://www.elastic.co/docs/api/doc/cloud/) | Manage your Cloud organization, members, costs, billing, and more.<br><br>Manage your hosted deployments and all of the resources associated with them, including scaling or autoscaling resources, and managing traffic filters, deployment extensions, remote clusters, and {{stack}} versions.<br><br>Refer to [{{ecloud}} RESTful API](cloud://reference/cloud-hosted/ec-api-restful.md) for usage information and examples. |
| {{serverless-full}} projects | [{{serverless-full}} API](https://www.elastic.co/docs/api/doc/elastic-cloud-serverless) | Manage {{serverless-full}} projects. |
| {{ecloud}} services | [Service Status API](https://status.elastic.co/api/) | Programmatically ingest [service status](/deploy-manage/cloud-organization/service-status.md) updates. |


### APIs to interact with data and solution features

The following APIs allow you to interact with your {{es}} cluster, its data, and the features available to you in your {{ech}} deployments and {{serverless-full}} projects. Separate APIs are used for {{ech}} and {{serverless-full}}.

Note that some [restrictions](/deploy-manage/deploy/elastic-cloud/restrictions-known-problems.md#ec-restrictions-apis-elasticsearch) apply when using the these APIs on {{ecloud}}.

:::{tip}
Refer to [{{es}} API conventions](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md) to learn about headers, request body conventions, and examples for {{es-serverless}} and {{es}} REST APIs.
:::

:::::{tab-set}
:group: serverless-hosted
::::{tab-item} {{serverless-short}}
:sync: serverless

The following APIs are available for {{es-serverless}} users:

- [{{es}} {{serverless-short}} APIs](https://www.elastic.co/docs/api/doc/elasticsearch-serverless): Use these APIs to index, manage, search, and analyze your data in {{es-serverless}}.

  Learn how to [connect to your {{es-serverless}} endpoint](/solutions/search/get-started.md).
- [{{kib}} {{serverless-short}} APIs](https://www.elastic.co/docs/api/doc/serverless): Use these APIs to manage resources such as connectors, data views, and saved objects for your {{serverless-full}} project.
::::

::::{tab-item} {{ech}}
:sync: hosted

The following APIs are available for {{ech}} users:

:::{include} /deploy-manage/deploy/_snippets/core-apis.md
:::
::::
:::::

#### APIs for optional products

:::{include} /deploy-manage/deploy/_snippets/other-apis.md
:::

## {{ecloud}} API console
```{applies_to}
deployment:
  ess: ga
serverless: unavailable
```

:::{include} /deploy-manage/deploy/_snippets/cloud-api-console.md
:::


## {{ecloud}} Control: command-line interface for {{ecloud}}
```{applies_to}
deployment:
  ess: ga
serverless: unavailable
```

:::{include} /deploy-manage/deploy/_snippets/ecctl.md
:::


## Provision deployments with Terraform
```{applies_to}
deployment:
  ess: ga
serverless: unavailable
```

:::{include} /deploy-manage/deploy/_snippets/tpec.md
:::
