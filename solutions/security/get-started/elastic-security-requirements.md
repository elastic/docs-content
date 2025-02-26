---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/sec-requirements.html
  - https://www.elastic.co/guide/en/serverless/current/security-requirements-overview.html
---

# Elastic Security requirements

% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/sec-requirements.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-requirements-overview.md

{{elastic-sec}} is an inbuilt part of {{kib}}. To use {{elastic-sec}}, you only need an {{stack}} deployment (an {{es}} cluster and {{kib}}).

{{ecloud}} offers all of the features of {{es}}, {{kib}}, and {{elastic-sec}} as a hosted service available on AWS, GCP, and Azure. To get started, sign up for a [free {{ecloud}} trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).

For information about installing and managing the {{stack}} yourself, see [Installing the {{stack}}](/get-started/the-stack.md).

The [Support Matrix](https://www.elastic.co/support/matrix) page lists officially supported operating systems, platforms, and browsers on which {{es}}, {{kib}}, {{beats}}, and Elastic Endpoint have been tested.


## Node role requirements [node-role-requirements] 

To use Elastic Security, at least one node in your Elasticsearch cluster must have the [`transform` role](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/transforms-settings.md). Nodes are automatically given this role when they’re created, so changes are not required if default role settings remain the same. This applies to on-premise and cloud deployments.

Changes might be required if your nodes have customized roles. When updating node roles, nodes are only assigned the roles you specify, and default roles are removed. If you need to reassign the `transform` role to a node, [create a dedicated transform node](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/node-settings.md#transform-node).


## Space and index privileges [_space_and_index_privileges] 

To use {{elastic-sec}}, your role must have at least:

* `Read` privilege for the `Security` feature in the [space](/deploy-manage/manage-spaces.md). This grants you `Read` access to all features in {{elastic-sec}} except cases. You need additional [minimum privileges](/solutions/security/investigate/cases-requirements.md) to use cases.
* `Read` and `view_index_metadata` privileges for all {{elastic-sec}} indices, such as `filebeat-*`, `packetbeat-*`, `logs-*`, and `endgame-*` indices.

::::{note} 
[*Configure advanced settings*](/solutions/security/get-started/configure-advanced-settings.md) describes how to modify {{elastic-sec}} indices.
::::


For more information about index privileges, refer to [{{es}} security privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md).


## Feature-specific requirements [_feature_specific_requirements] 

There are some additional requirements for specific features:

* [*Detections requirements*](/solutions/security/detect-and-alert/detections-requirements.md)
* [Cases requirements](/solutions/security/investigate/cases-requirements.md)
* [Entity risk scoring requirements](/solutions/security/advanced-entity-analytics/entity-risk-scoring-requirements.md)
* [Machine learning job and rule requirements](/solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md)
* [*{{elastic-defend}} requirements*](/solutions/security/configure-elastic-defend/elastic-defend-requirements.md)
* [Configure network map data](/solutions/security/explore/configure-network-map-data.md)


## License requirements [_license_requirements] 

All features are available as part of the free Basic plan **except**:

* [Alert notifications via external systems](/solutions/security/detect-and-alert/create-detection-rule.md#rule-notifications)
* [{{ml-cap}} jobs and rules](/solutions/security/advanced-entity-analytics/anomaly-detection.md)
* [Cases integration with third-party ticketing systems](/solutions/security/investigate/configure-case-settings.md#cases-ui-integrations)

[Elastic Stack subscriptions](https://www.elastic.co/subscriptions) lists the required subscription plans for all features.


## Advanced configuration and UI options [_advanced_configuration_and_ui_options] 

[*Configure advanced settings*](/solutions/security/get-started/configure-advanced-settings.md) describes how to modify advanced settings, such as the {{elastic-sec}} indices, default time intervals used in filters, and IP reputation links.


## Third-party collectors mapped to ECS [_third_party_collectors_mapped_to_ecs] 

The [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current) defines a common set of fields to be used for storing event data in Elasticsearch. ECS helps users normalize their event data to better analyze, visualize, and correlate the data represented in their events. {{elastic-sec}} can ingest and normalize events from any ECS-compliant data source.

::::{important} 
{{elastic-sec}} requires [ECS-compliant data](https://www.elastic.co/guide/en/ecs/current). If you use third-party data collectors to ship data to {{es}}, the data must be mapped to ECS. [*Elastic Security ECS field reference*](asciidocalypse://docs/docs-content/docs/reference/security/fields-and-object-schemas/siem-field-reference.md) lists ECS fields used in {{elastic-sec}}.
::::



## Cross-cluster searches [_cross_cluster_searches] 

For information on how to perform cross-cluster searches on {{elastic-sec}} indices, see:

* [Search across cluster](/solutions/search/cross-cluster-search.md) (for self-managed {{stack}} deployments)
* [Enable cross-cluster search](/deploy-manage/remote-clusters/ec-enable-ccs.md) (for hosted deployments)

