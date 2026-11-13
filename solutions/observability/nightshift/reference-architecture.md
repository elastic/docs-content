---
navigation_title: Reference architecture
applies_to:
  serverless:
    observability: preview
description: Check which Elastic nightshift features work with your deployment, whether your data is in a Serverless project, in projects linked by cross-project search, in Elastic Cloud Hosted, or in a self-managed cluster.
products:
  - id: observability
  - id: cloud-serverless
---

# Reference architecture [nightshift-reference-architecture]

{{nightshift}} always runs in an {{obs-serverless}} project. What it can do depends on where your data lives. Use this page to check what works with your setup before you start.

{{nightshift}} has two engines that reach your data in different ways:

- **Detection** watches your data through [sources](./detection/sources.md). A source is an {{esql}} query, so detection only reads data that the project can query meaning data in the project itself, or in projects linked by [{{cps}}](/deploy-manage/cross-project-search-config.md).
- **Investigation** queries your data through {{es}} connectors. A connector can point to any {{es}} cluster that {{nightshift}} can reach over the network with an API key. Refer to [Connect your data and tools](./investigation/set-up.md).

## What works where [nightshift-reference-architecture-matrix]

| Where your data lives | Detection | Investigation | How investigations reach the data |
| --- | --- | --- | --- |
| [A single serverless project](#nightshift-reference-architecture-single) | Yes | Yes | **Local Elasticsearch** connector, created for you |
| [Serverless projects linked by {{cps}}](#nightshift-reference-architecture-cps) | Yes | Yes | **Local Elasticsearch** connector, through {{cps}} |
| [An {{ech}} deployment](#nightshift-reference-architecture-ech) | No | Yes | External {{es}} connector with an API key |
| [A self-managed cluster](#nightshift-reference-architecture-self-managed) | No | Possible, with care | External {{es}} connector to a public, secured endpoint |

For the best results, keep your data in {{serverless-short}}, either in the {{nightshift}} project or in projects linked to it. Then detection and investigation both work, and you don't manage any credentials.

## {{serverless-short}}, single project [nightshift-reference-architecture-single]

The simplest setup is having your logs, metrics, and traces in the same {{obs-serverless}} project as {{nightshift}}.

:::{image} ../../images/nightshift-ref-arch-single-project.svg
:alt: Elastic nightshift and your data in the same Serverless project. Detection and investigation both work.
:width: 100%
:::

- **Detection**: Add a source such as **All logs** and select **Enable detection**. Refer to [Choose what detection watches](./detection/sources.md).
- **Investigation**: When you enable {{nightshift}}, it creates a **Local Elasticsearch** connector for the project. You don't set up anything else.

## {{serverless-short}} with {{cps}}[nightshift-reference-architecture-cps]

Your data is spread across several Serverless projects, for example one project per team or per region, and the {{nightshift}} project is linked to them with [{{cps}}](/deploy-manage/cross-project-search-config.md).

:::{image} ../../images/nightshift-ref-arch-cps.svg
:alt: The Elastic nightshift project linked to other Serverless projects by cross-project search. Detection and investigation both work across the linked projects.
:width: 100%
:::

- **Detection**: Works across the linked projects. A source query reads the linked projects in the same way as the local one.
- **Investigation**: Works across the linked projects through the **Local Elasticsearch** connector. You don't need an External {{es}} connector for linked projects.

This is the recommended setup when your data lives in more than one place. Link the projects once, and {{nightshift}} sees all of them.

## {{ech}}[nightshift-reference-architecture-ech]

Your data is in an [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md) deployment, and {{nightshift}} runs in a separate Serverless project.

:::{image} ../../images/nightshift-ref-arch-ech.svg
:alt: Elastic nightshift in a Serverless project connects to an Elastic Cloud Hosted deployment with an External Elasticsearch connector and a read-only API key. Investigation works. Detection doesn't.
:width: 100%
:::

- **Detection**: Sources can't read data in an {{ech}} deployment.
- **Investigation**: Add an External {{es}} connector that points to the deployment's {{es}} endpoint and uses a read-only API key. Refer to [Add data](./get-started/investigations.md#nightshift-get-started-add-data) for the API key request and where to find the endpoint.

Automations start from alerts in the {{nightshift}} project. To investigate alerts that fire in the {{ech}} deployment automatically, send them to a Slack channel or to a webhook in the {{nightshift}} project. Refer to [Investigate alerts from your other tools](./use-cases/external-alerts.md).

## Self-managed cluster [nightshift-reference-architecture-self-managed]

Your data is in an {{es}} cluster that you run yourself, on premises or in your own cloud account.

:::{image} ../../images/nightshift-ref-arch-self-managed.svg
:alt: Elastic nightshift in a Serverless project connects to a self-managed cluster through a public, secured endpoint with an External Elasticsearch connector. Investigation is possible with care. Detection doesn't work.
:width: 100%
:::

- **Detection**: Sources can't read data in a self-managed cluster.
- **Investigation**: Possible, but only if {{nightshift}} can reach your cluster's {{es}} endpoint over the internet. An External {{es}} connector runs in Elastic Cloud, so it can't reach a cluster that is only on a private network. Mutual TLS (mTLS) and private connectivity, such as AWS PrivateLink, aren't supported.

:::{warning}
Exposing a cluster to the internet is a security decision for your team. If you do it, secure the endpoint before you connect it:

- Use TLS with a trusted certificate. Refer to [Secure cluster communications](/deploy-manage/security/secure-cluster-communications.md).
- Use a dedicated API key that can only read the indices that investigations need. Refer to [Elasticsearch API keys](/deploy-manage/api-keys/elasticsearch-api-keys.md).
- Restrict who can connect, for example with IP filtering or a reverse proxy in front of the cluster. Refer to [IP filtering](/deploy-manage/security/ip-filtering.md).
:::

If you can't expose the cluster, consider sending the data you want {{nightshift}} to investigate to a {{serverless-short}} project instead, for example with OpenTelemetry or {{agent}}. Refer to [Get started with {{obs-serverless}}](/solutions/observability/get-started.md).

## Next steps [nightshift-reference-architecture-next]

- [Get started](./get-started.md): Enable {{nightshift}} and connect your data
- [Connect your data and tools](./investigation/set-up.md): Set up Local and External {{es}} connectors, GitHub, and Slack
- [How detection works](./detection/index.md): Learn what detection needs from your data
- [Known issues](./known-issues.md): Check the Tech Preview limitations
