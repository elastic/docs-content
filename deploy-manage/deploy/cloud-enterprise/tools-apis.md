---
navigation_title: Tools and APIs
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-api-console.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---
# Tools and APIs for {{ece}}

Review key resources that can be used to interact with and manage your {{ece}} installation and deployments.


## APIs

You can use the following APIs in an {{ece}} environment.

:::{tip}
Refer to [](/deploy-manage/api-keys.md) to learn how to generate API keys for your environment.
:::

### Orchestration APIs

You can use the [{{ece}} RESTful API]({{ece-apis}}) to manage both your {{stack}} deployments and the ECE platform.

Refer to [{{es}} API conventions](cloud://reference/cloud-enterprise/restful-api.md) to learn about headers and request body conventions, and view examples.

### APIs to interact with data and solution features

The following APIs allow you to interact with your {{es}} cluster, its data, and the features available to you in your {{ece}} deployments.

:::{tip}
Refer to [{{es}} API conventions](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md) to learn about headers and request body conventions, and to view examples.
:::

:::{include} /deploy-manage/deploy/_snippets/core-apis.md
:::

:::{include} /deploy-manage/deploy/_snippets/other-apis.md
:::

## Elastic CLI
```{applies_to}
deployment:
  stack: preview
```

The Elastic CLI provides a single command-line interface for {{es}} and {{kib}} APIs. Use it to interact with {{es}} and {{kib}} in {{ece}} deployments.

Refer to the [Elastic CLI documentation](cli://index.md) to install the CLI, configure a connection, and run example operations. Not all Elastic APIs are available as CLI commands.

:::{note}
The Elastic CLI doesn't support the {{ece}} API. To manage deployments at the platform level, you can use [ecctl](#ecctl).
:::

## {{es}} API Console [ece-api-console]

:::{include} /deploy-manage/deploy/_snippets/cloud-api-console.md
:::

## {{ecloud}} Control: command-line interface for {{ecloud}} [ecctl]

:::{include} /deploy-manage/deploy/_snippets/ecctl.md
:::

## Provision hosted deployments with Terraform
```{applies_to}
deployment:
  ess: ga
serverless: unavailable
```

:::{include} /deploy-manage/deploy/_snippets/tpec.md
:::

## Other tools

* [ECE scripts](cloud://reference/cloud-enterprise/scripts.md): Use these scripts to install {{ece}} or modify your installation.
* [ECE diagnostics tool](/troubleshoot/deployments/cloud-enterprise/run-ece-diagnostics-tool.md): Collect logs and metrics related to your ECE installation that you can send to Elastic Support for troubleshooting and investigation purposes.
* [{{es}} Support Diagnostic tool](/troubleshoot/elasticsearch/diagnostic.md): Captures a point-in-time snapshot of cluster statistics and most {{es}} settings for troubleshooting purposes.
