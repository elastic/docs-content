---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-files.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/secure-cluster.html
  - https://www.elastic.co/guide/en/kibana/current/xpack-security.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-securing-stack.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-securing-ece.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-security.html
  - https://www.elastic.co/guide/en/kibana/current/using-kibana-with-security.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/es-security-principles.html
  - https://www.elastic.co/guide/en/cloud/current/ec-faq-technical.html
applies_to:
  deployment: all
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: cloud-kubernetes
  - id: cloud-enterprise
  - id: cloud-hosted
  - id: cloud-serverless
---

# Security

An Elastic implementation comprises many moving parts: {{es}} nodes forming the cluster, {{kib}} instances, additional stack components such as Logstash and Beats, and various clients and integrations, all communicating with your cluster.

To keep your data secured, Elastic offers security features that prevent bad actors from tampering with your data, and encrypt communications to, from, and within your cluster. Regardless of your deployment type, Elastic sets up certain security features for you automatically.

The availability and configurability of security features vary by deployment type. On every page, you'll see deployment type indicators that show which content applies to specific deployment types. Focus on sections tagged with your deployment type and look for subsections specifically addressing your deployment model. You can also review a [comparison table](#comparison-table) showing feature availability and configurability by deployment type.

:::{include} /deploy-manage/security/_snippets/complete-security.md
:::

## Managed security in {{ecloud}} [managed-security-in-elastic-cloud]
```yaml {applies_to}
deployment:
  ess: all
serverless: all
```

:::{include} /deploy-manage/_snippets/ecloud-security.md
:::

::::{note}
Serverless projects are fully managed and secured by Elastic, and do not have any configurable Security features at the project level.
::::

## Securing your orchestrator
```yaml {applies_to}
deployment:
  ece: all
  eck: all
```

When running {{stack}} applications on {{ece}} or {{eck}}, you must also secure the [orchestration layer](/deploy-manage/deploy.md#who-manages-the-infrastructure) responsible for deploying and managing your Elastic products.

Learn about securing the following components:

* [An {{ece}} installation](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation.md)
* [An {{eck}} operator](/deploy-manage/security/secure-your-eck-installation.md)

:::{tip}
Elastic secures your [{{ecloud}}](/deploy-manage/deploy/elastic-cloud.md) orchestrator for you.
:::

## Cluster or deployment security features
```yaml {applies_to}
deployment:
  ece: all
  eck: all
  ess: all
  self: all
```

You can configure the following aspects of your Elastic cluster or deployment to maintain and enhance security:

### Initial security setup

:::{include} /deploy-manage/security/_snippets/enable-security.md
:::

### Communication and network security

:::{include} /deploy-manage/security/_snippets/cluster-communication-network.md
:::

### Data security

:::{include} /deploy-manage/security/_snippets/cluster-data.md
:::

### User session security

:::{include} /deploy-manage/security/_snippets/cluster-user-session.md
:::

### Security event audit logging

:::{include} /deploy-manage/security/_snippets/audit-logging.md
:::


% missing: fips mode, manual config

% we need to refine this table, but the idea is awesome IMO
### Security features by deployment type [comparison-table]

:::{include} /deploy-manage/security/_snippets/cluster-comparison.md
:::

## Securing other {{stack}} components

The {{es}} security features enable you to secure your {{es}} cluster. However, for a complete security strategy, you must secure other applications in the {{stack}}, as well as communications between {{es}} and other {{stack}} components.

[Review security topics for other {{stack}} components](/deploy-manage/security/secure-clients-integrations.md).

## Securing clients and integrations

If you use HTTP clients or integrations to communicate with {{es}}, then you also need to [secure communications between the clients or integrations and {{es}}](/deploy-manage/security/httprest-clients-security.md).

## Security limitations

There are security limitations that apply to the usage of some {{es}} features or resources. Depending on your organization's security requirements, you might want to restrict, adjust, or find workaround or alternatives for some of these features and resources.

[Review {{es}} security limitations](/deploy-manage/security/limitations.md).