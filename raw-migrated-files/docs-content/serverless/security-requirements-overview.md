# {{elastic-sec}} requirements [security-requirements-overview]

The [Support Matrix](https://www.elastic.co/support/matrix) page lists officially supported operating systems, platforms, and browsers on which components such as {{beats}}, {{agent}}, {{elastic-defend}}, and {{elastic-endpoint}} have been tested.


## Space and index privileges [security-requirements-overview-space-and-index-privileges] 

Provide access to {{elastic-sec}} by assigning a user the appropriate [predefined user role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) or a [custom role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md) with specific privileges.

To use {{elastic-sec}}, your role must have at least:

* `Read` privilege for the `Security` feature in the [space](../../../solutions/security/get-started/spaces-elastic-security.md). This grants you `Read` access to all features in {{elastic-sec}} except cases. You need additional [minimum privileges](../../../solutions/security/investigate/cases-requirements.md) to use cases.
* `Read` and `view_index_metadata` privileges for all {{elastic-sec}} indices, such as `filebeat-*`, `packetbeat-*`, `logs-*`, and `endgame-*` indices.

::::{note} 
[Advanced settings](../../../solutions/security/get-started/configure-advanced-settings.md) describes how to modify {{elastic-sec}} indices.

::::


For more information about index privileges, refer to [{{es}} security privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md).


## Feature-specific requirements [security-requirements-overview-feature-specific-requirements] 

There are some additional requirements for specific features:

* [Detections requirements](../../../solutions/security/detect-and-alert/detections-requirements.md)
* [Cases requirements](../../../solutions/security/investigate/cases-requirements.md)
* [Entity risk scoring requirements](../../../solutions/security/advanced-entity-analytics/entity-risk-scoring-requirements.md)
* [{{ml-cap}} job and rule requirements](../../../solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md)
* [{{elastic-defend}} requirements](../../../solutions/security/configure-elastic-defend/elastic-defend-requirements.md)
* [Configure network map data](../../../solutions/security/explore/configure-network-map-data.md)


## Advanced configuration and UI options [security-requirements-overview-advanced-configuration-and-ui-options] 

[Advanced settings](../../../solutions/security/get-started/configure-advanced-settings.md) describes how to modify advanced settings, such as the {{elastic-sec}} indices, default time intervals used in filters, and IP reputation links.


## Third-party collectors mapped to ECS [security-requirements-overview-third-party-collectors-mapped-to-ecs] 

The [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current) defines a common set of fields to be used for storing event data in Elasticsearch. ECS helps users normalize their event data to better analyze, visualize, and correlate the data represented in their events. {{elastic-sec}} can ingest and normalize events from any ECS-compliant data source.

::::{important} 
{{elastic-sec}} requires [ECS-compliant data](https://www.elastic.co/guide/en/ecs/current). If you use third-party data collectors to ship data to {{es}}, the data must be mapped to ECS. [{{elastic-sec}} ECS field reference](https://www.elastic.co/guide/en/serverless/current/security-siem-field-reference.html) lists ECS fields used in {{elastic-sec}}.

::::


