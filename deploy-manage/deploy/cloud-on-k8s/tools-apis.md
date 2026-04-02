---
applies_to:
  deployment:
    eck: all
navigation_title: Tools and APIs
products:
  - id: cloud-kubernetes
---

# Tools and APIs for {{eck}}

Review key resources that can be used to interact with and manage your {{eck}} operator and deployments.

## APIs

You can use the following APIs in an {{eck}} environment.

:::{tip}
Refer to [](/deploy-manage/api-keys.md) to learn how to generate API keys for your environment.
:::

### Orchestration APIs

You can use the [{{eck}} API](cloud-on-k8s://reference/api-docs.md) to create and manage {{stack}} components using Elastic-provided [Custom Resource Definitions (CRDs)](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions).


### APIs to interact with data and solution features

The following APIs allow you to interact with your {{es}} cluster, its data, and the features available to you in your {{eck}} deployments.

:::{tip}
Refer to [{{es}} API conventions](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md) to learn about headers and request body conventions, and to view examples.
:::

:::{include} /deploy-manage/deploy/_snippets/core-apis.md
:::

:::{include} /deploy-manage/deploy/_snippets/other-apis.md
:::

## Tools

* [ECK diagnostics tool](/troubleshoot/deployments/cloud-on-k8s/run-eck-diagnostics.md): Use the `eck-diagnostics` command line tool to create a diagnostic archive to help troubleshoot issues with ECK. 