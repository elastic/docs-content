---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-restrictions.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Restrictions and known problems [ec-restrictions]

When using {{ecloud}}, there are some limitations you should be aware of:

* [Security](#ec-restrictions-security)
* [APIs](#ec-restrictions-apis)
* [Transport client](#ec-restrictions-transport-client)
* [{{es}} and {{kib}} plugins](#ec-restrictions-plugins)
* [Watcher](#ec-restrictions-watcher)
* [Private connectivity and SSO to {{kib}} URLs](#ec-restrictions-network-security-kibana-sso)
* [PDF report generation using Alerts or Watcher webhooks](#ec-restrictions-network-security-watcher)
* [Kibana](#ec-restrictions-kibana)
* [Fleet with network security](#ec-restrictions-fleet-network-security)
* [Restoring a snapshot across deployments](#ec-snapshot-restore-enterprise-search-kibana-across-deployments)
* [Migrate Fleet-managed {{agents}} across deployments by restoring a snapshot](#ec-migrate-elastic-agent)
* [Regions and Availability Zones](#ec-regions-and-availability-zone)
* [Node count and size](#ec-node-count-size)
* [Repository analysis API is unavailable in {{ecloud}}](#ec-repository-analyis-unavailable)

For limitations related to logging and monitoring, check the [Restrictions and limitations](../../monitor/stack-monitoring/ece-ech-stack-monitoring.md#restrictions-monitoring) section of the logging and monitoring page.

% Occasionally, we also publish information about [Known problems](#ec-known-problems) with our {{ecloud}} or the {{stack}}.

To learn more about the features that are supported by {{ecloud}}, check [{{ecloud}} Subscriptions](https://www.elastic.co/cloud/elasticsearch-service/subscriptions?page=docs&placement=docs-body).


## Security [ec-restrictions-security]

* File and LDAP realms cannot be used. The Native realm is enabled, but the realm configuration itself is fixed in {{ecloud}}. Alternatively, authentication protocols such as SAML, OpenID Connect, or Kerberos can be used.
* Client certificates, such as PKI certificates, are not supported.
* IPv6 is not supported.


## APIs [ec-restrictions-apis]

The following restrictions apply when using APIs in {{ecloud}}:

{{ecloud}} API
:   The {{ecloud}} API is subject to a restriction on the volume of API requests that can be submitted per user, per second. Check [Rate limiting](cloud://reference/cloud-hosted/ec-api-rate-limiting.md) for details.

$$$ec-restrictions-apis-elasticsearch$$$

{{es}} APIs
:   The {{es}} APIs do not natively enforce rate limiting. However, all requests to the {{es}} cluster are subject to {{es}} configuration settings, such as the [network HTTP setting](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#http-settings) `http:max_content_length` which restricts the maximum size of an HTTP request body. This setting has a default value of 100MB, hence restricting API request payloads to that size. This setting is not currently configurable in {{ecloud}}. For a list of which {{es}} settings are supported on Cloud, check [Add {{es}} user settings](edit-stack-settings.md). To learn about using the {{es}} APIs in {{ecloud}}, check [Access the {{es}} API console](cloud://reference/cloud-hosted/ec-api-console.md). And, for full details about the {{es}} APIs and their endpoints, check the [{{es}} API reference documentation](elasticsearch://reference/elasticsearch/rest-apis/index.md).

$$$ec-restrictions-apis-kibana$$$

{{kib}} APIs
:   There are no rate limits restricting your use of the {{kib}} APIs. However, {{kib}} features are affected by the [{{kib}} configuration settings](kibana://reference/configuration-reference.md), not all of which are supported in {{ecloud}}. For a list of what settings are currently supported, check [Add {{kib}} user settings](edit-stack-settings.md). For all details about using the {{kib}} APIs, check the [{{kib}} API reference documentation](https://www.elastic.co/docs/api/doc/kibana/).


## Transport client [ec-restrictions-transport-client]

* The transport client is not considered thread safe in a cloud environment. We recommend that you use the Java REST client instead. This restriction relates to the fact that your deployments hosted on {{ecloud}} are behind proxies, which prevent the transport client from communicating directly with {{es}} clusters.
* The transport client is not supported over [private connections](../../security/private-connectivity.md). Use the Java REST client instead, or connect over the public internet.
% * The transport client does not work with {{es}} clusters at version 7.6 and later that are hosted on Cloud. Transport client continues to work with {{es}} clusters at version 7.5 and earlier. Note that the transport client was deprecated with version 7.0 and will be removed with 8.0.


## {{es}} and {{kib}} plugins [ec-restrictions-plugins]

* {{kib}} plugins are not supported.
* {{es}} plugins, are not enabled by default for security purposes. Reach out to support if you would like to enable {{es}} plugins support on your account.
* Some {{es}} plugins do not apply to {{ecloud}}. For example, you won’t ever need to change discovery, as {{ecloud}} handles how nodes discover one another.
% * In {{es}} 5.0 and later, site plugins are no longer supported. This change does not affect the site plugins {{ecloud}} might provide out of the box, such as Kopf or Head, since these site plugins are serviced by our proxies and not {{es}} itself.
% * In {{es}} 5.0 and later, site plugins such as Kopf and Paramedic are no longer provided. We recommend that you use our [cluster performance metrics](../../monitor/stack-monitoring.md), [X-Pack monitoring features](../../monitor/stack-monitoring.md) and Kibana’s (6.3+) [Index Management UI](/manage-data/data-store/index-basics.md#manage-indices) if you want more detailed information or perform index management actions.


## Watcher [ec-restrictions-watcher]

Watcher encryption Key Setup is not supported.

Changing the default throttle period is not possible. You can specify a throttle period per watch, however.

Watcher comes preconfigured with a directly usable email account provided by Elastic. However, this account can’t be reconfigured and is subject to some limitations. For more information on the limits of the Elastic mail server, check the [cloud email service limits](/deploy-manage/deploy/elastic-cloud/tools-apis.md#email-service-limits).

Alternatively, a custom mail server can be configured as described in [Configuring a custom mail server](../../../explore-analyze/alerts-cases/watcher/enable-watcher.md#watcher-custom-mail-server)


## Private connectivity and SSO to {{kib}} URLs [ec-restrictions-network-security-kibana-sso]

Currently you can’t use SSO to login directly from {{ecloud}} into {{kib}} endpoints that are protected by private connections. However, you can still SSO into private {{kib}} endpoints individually using the [SAML](../../users-roles/cluster-or-deployment-auth/saml.md) or [OIDC](../../users-roles/cluster-or-deployment-auth/openid-connect.md) protocol from your own identity provider, just not through the {{ecloud}} console. Stack level authentication using the {{es}} username and password should also work with `{{kibana-id}}.{vpce|privatelink|psc}.domain` URLs.


## PDF report generation using Alerts or Watcher webhooks [ec-restrictions-network-security-watcher]

* PDF report automatic generation via Alerts is not possible on {{ecloud}}.
* PDF report generation isn’t possible for deployments running on {{stack}} version 8.7.0 or before that are protected by network security. This limitation doesn’t apply to public webhooks such as Slack, PagerDuty, and email. For deployments running on {{stack}} version 8.7.1 and beyond, [PDF report automatic generation via Watcher webhook](../../../explore-analyze/report-and-share/automating-report-generation.md#use-watcher) is possible using the `xpack.notification.webhook.additional_token_enabled` configuration setting to bypass network security.


## {{kib}} [ec-restrictions-kibana]

* The maximum size of a single {{kib}} instance is 8GB. This means, {{kib}} instances can be scaled up to 8GB before they are scaled out. For example, when creating a deployment with a {{kib}} instance of size 16GB, then 2x8GB instances are created. If you face performance issues with {{kib}} PNG or PDF reports, the recommendations are to create multiple, smaller dashboards to export the data, or to use a third party browser extension for exporting the dashboard in the format you need.
* Running an external {{kib}} in parallel to {{ecloud}}’s {{kib}} instances may cause errors, for example [`Unable to decrypt attribute`](../../../explore-analyze/alerts-cases/alerts/alerting-common-issues.md#rule-cannot-decrypt-api-key), due to a mismatched [`xpack.encryptedSavedObjects.encryptionKey`](kibana://reference/configuration-reference/security-settings.md#security-encrypted-saved-objects-settings) as {{ecloud}} does not [allow users to set](edit-stack-settings.md) nor expose this value. While workarounds are possible, this is not officially supported nor generally recommended.

## Fleet with network security [ec-restrictions-fleet-network-security]

* If you are using Fleet 8.12+, using a remote {{es}} output with a target cluster that has network security enabled is not currently supported.

## Restoring a snapshot across deployments [ec-snapshot-restore-enterprise-search-kibana-across-deployments]

{{kib}} does not currently support restoring a snapshot of their indices across {{ecloud}} deployments.

* [{{kib}} uses encryption keys](/deploy-manage/security/secure-your-cluster-deployment.md) in various places, ranging from encrypting data in some areas of reporting, alerts, actions, connector tokens, ingest outputs used in Fleet and Synthetics monitoring to user sessions.
* Currently, there is not a way to retrieve the values of {{kib}} encryption keys, or set them in the target deployment before restoring a snapshot. As a result, once a snapshot is restored, {{kib}} will not be able to decrypt the data required for some features to function properly in the target deployment.
* If you have already restored a snapshot across deployments and now have broken {{kib}} saved objects in the target deployment, you will have to recreate all broken configurations and objects, or create a new setup in the target deployment instead of using snapshot restore.

A snapshot taken using the default `found-snapshots` repository can only be restored to deployments in the same region. If you need to restore snapshots across regions, create the destination deployment, connect to the [custom repository](../../tools/snapshot-and-restore/elastic-cloud-hosted.md), and then [restore from a snapshot](../../tools/snapshot-and-restore/restore-snapshot.md).

When restoring from a deployment that’s using searchable snapshots, you must not delete the snapshots in the source deployment even after they are successfully restored in the destination deployment. Refer to [Restore snapshots containing searchable snapshots indices across clusters](../../tools/snapshot-and-restore/ece-restore-snapshots-containing-searchable-snapshots-indices-across-clusters.md) for more information.


## Migrate Fleet-managed {{agents}} across deployments by restoring a snapshot [ec-migrate-elastic-agent]

There are situations where you may need or want to move your installed {{agents}} from being managed in one deployment to being managed in another deployment.

In {{ecloud}}, you can migrate your {{agents}} by taking a snapshot of your source deployment, and restoring it on a target deployment.

To make a seamless migration, after restoring from a snapshot there are some additional steps required, such as updating settings and resetting the agent policy. Check [Migrate Elastic Agents](/reference/fleet/migrate-elastic-agent.md) for details.


## Regions and Availability Zones [ec-regions-and-availability-zone]

* The AWS `us-west-1` region is limited to two availability zones for ES data nodes and one (tiebreaker only) virtual zone (as depicted by the `-z` in the AZ (`us-west-1z`). Deployment creation with three availability zones for {{es}} data nodes for hot, warm, and cold tiers is not possible. This includes scaling an existing deployment with one or two AZs to three availability zones. The virtual zone `us-west-1z` can only hold an {{es}} tiebreaker node (no data nodes). The workaround is to use a different AWS US region that allows three availability zones, or to scale existing nodes up within the two availability zones.
* The AWS `eu-central-2` region is limited to two availability zones for CPU Optimized (ARM) Hardware profile ES data node and warm/cold tier. Deployment creation with three availability zones for {{es}} data nodes for hot (for CPU Optimized (ARM) profile), warm and cold tiers is not possible. This includes scaling an existing deployment with one or two AZs to three availability zones. The workaround is to use a different AWS region that allows three availability zones, or to scale existing nodes up within the two availability zones.

## Node count and size [ec-node-count-size]
* In the {{ecloud}} console UI, the maximum configurable node count is 32.
  The total RAM for `Size per zone` is calculated by multiplying the maximum RAM size of the [instance configuration](cloud://reference/cloud-hosted/hardware.md) in use by 32. For example, for the instance configuration [`aws.es.datahot.c6gd`](cloud://reference/cloud-hosted/aws-default.md), the maximum RAM size is 60GB. Therefore, the total RAM for `Size per zone` is `60GB x 32 = 1.875TB` (displayed as `1.88TB` in the {{ecloud}} console UI).
  
  This maximum node count limitation applies to the UI and affects both the maximum `Size per zone` during manual scaling and the `Maximum size per zone` in autoscaling. This limit is in place to prevent users from inadvertently deploying excessive capacity. 
  
  This limitation does not apply when using the API for manual scaling or autoscaling. If you require additional capacity, you can use the [Elastic Cloud API](cloud://reference/cloud-hosted/ec-api-restful.md) to scale up or configure the maximum size for autoscaling, in a self-sufficient way. Refer to the [Update a deployment](cloud://reference/cloud-hosted/ec-api-deployment-crud.md#ec_update_a_deployment) example to learn how to make a deployment update request using the API.
* Apart from the maximum node count configurable in the {{ecloud}} console UI, there are other service limits based on each instance configuration. These service limits are typically greater than 32. For more details, please [contact Elastic support for assistance](/troubleshoot/index.md).

## Repository analysis API is unavailable in {{ecloud}} [ec-repository-analyis-unavailable]

* The {{es}} [Repository analysis API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-repository-analyze) is not available in {{ecloud}} due to deployments defaulting to having [operator privileges](../../users-roles/cluster-or-deployment-auth/operator-privileges.md) enabled that prevent non-operator privileged users from using it along with a number of other APIs.
