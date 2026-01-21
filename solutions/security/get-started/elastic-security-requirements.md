---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/sec-requirements.html
  - https://www.elastic.co/guide/en/serverless/current/security-requirements-overview.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# {{elastic-sec}} requirements [security-requirements-overview]

The [Support Matrix](https://www.elastic.co/support/matrix) page lists officially supported operating systems, platforms, and browsers on which components such as {{beats}}, {{agent}}, {{elastic-defend}}, and {{elastic-endpoint}} have been tested.

## {{stack}} requirements [elastic-stack-requirements]

```yaml {applies_to}
stack:
```

{{elastic-sec}} is an inbuilt part of {{kib}}. To use {{elastic-sec}}, you only need an {{stack}} deployment (an {{es}} cluster and {{kib}}). Review the [Elastic Stack subscriptions](https://www.elastic.co/subscriptions) page to understand the required subscription plans for all features.

{{ecloud}} offers all of the features of {{es}}, {{kib}}, and {{elastic-sec}} as a hosted service available on AWS, GCP, and Azure. To get started, sign up for a [free {{ecloud}} trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).

For information about installing and managing the {{stack}} yourself, refer to [](/deploy-manage/deploy/self-managed.md).

### Node role requirements [node-role-requirements]

```yaml {applies_to}
stack:
```

To use {{elastic-sec}}, at least one node in your Elasticsearch cluster must have the [`transform` role](elasticsearch://reference/elasticsearch/configuration-reference/transforms-settings.md). Nodes are automatically given this role when they’re created, so changes are not required if default role settings remain the same. This applies to on-premise and cloud deployments.

Changes might be required if your nodes have customized roles. When updating node roles, nodes are only assigned the roles you specify, and default roles are removed. If you need to reassign the `transform` role to a node, [create a dedicated transform node](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#transform-node).


## Space and index privileges [_space_and_index_privileges]


To use {{elastic-sec}}, your role must have at least:

* `Read` privilege for the `Security` feature in the [space](/deploy-manage/manage-spaces.md). This grants you `Read` access to all features in {{elastic-sec}} except cases. You need additional [minimum privileges](/solutions/security/investigate/cases-requirements.md) to use cases.
* `Read` and `view_index_metadata` privileges for all {{elastic-sec}} indices, such as `filebeat-*`, `packetbeat-*`, `logs-*`, and `endgame-*` indices.

::::{note}
[Configure advanced settings](/solutions/security/get-started/configure-advanced-settings.md) describes how to modify {{elastic-sec}} indices.
::::


For more information about index privileges, refer to [{{es}} security privileges](elasticsearch://reference/elasticsearch/security-privileges.md).


## Feature-specific requirements [security-requirements-overview-feature-specific-requirements]

There are some additional requirements for specific features:

* [Detections requirements](/solutions/security/detect-and-alert/detections-requirements.md)
* [Cases requirements](/solutions/security/investigate/cases-requirements.md)
* [Entity risk scoring requirements](/solutions/security/advanced-entity-analytics/entity-risk-scoring-requirements.md)
* [Machine learning job and rule requirements](/solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md)
* [{{elastic-defend}} requirements](/solutions/security/configure-elastic-defend/elastic-defend-requirements.md)
* [Configure network map data](/solutions/security/explore/configure-network-map-data.md)

## Advanced configuration and UI options [security-requirements-overview-advanced-configuration-and-ui-options]

[Configure advanced settings](/solutions/security/get-started/configure-advanced-settings.md) describes how to modify advanced settings, such as the {{elastic-sec}} indices, default time intervals used in filters, and IP reputation links.


## Third-party collectors mapped to ECS [security-requirements-overview-third-party-collectors-mapped-to-ecs]

The [Elastic Common Schema (ECS)](ecs://reference/index.md) defines a common set of fields to be used for storing event data in Elasticsearch. ECS helps users normalize their event data to better analyze, visualize, and correlate the data represented in their events. {{elastic-sec}} can ingest and normalize events from any ECS-compliant data source.

::::{important}
{{elastic-sec}} requires [ECS-compliant data](ecs://reference/index.md). If you use third-party data collectors to ship data to {{es}}, the data must be mapped to ECS. [{{elastic-sec}} ECS field reference](/reference/security/fields-and-object-schemas/siem-field-reference.md) lists ECS fields used in {{elastic-sec}}.
::::

## Third-party collectors NOT mapped to ECS [security-requirements-overview-third-party-collectors-not-mapped-to-ecs]

{{elastic-sec}} does not support the use of third-party connectors that do not map data to ECS, including third-party and open source OTel collectors.

## Cross-cluster searches [security-cross-cluster-searches]

```yaml {applies_to}
stack:
```

For information on how to perform cross-cluster searches on {{elastic-sec}} indices, see:

* [Search across cluster](/explore-analyze/cross-cluster-search.md) (for self-managed {{stack}} deployments)
* [Enable cross-cluster search](/deploy-manage/remote-clusters/ec-enable-ccs.md) (for hosted deployments)

