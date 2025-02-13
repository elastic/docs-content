---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-restrictions.html
---

# Restrictions and known problems [ech-restrictions]

When using Elasticsearch Add-On for Heroku, there are some limitations you should be aware of:

* [Elasticsearch Add-On for Heroku](#ech-restrictions-heroku)
* [Security](#ech-restrictions-security)
* [Elasticsearch and Kibana plugins](#ech-restrictions-plugins)
* [Kibana](#ech-restrictions-kibana)
* [APM Agent central configuration with Private Link or traffic filters](#ech-restrictions-apm-traffic-filters)
* [Fleet with Private Link or traffic filters](#ech-restrictions-fleet-traffic-filters)
* [Enterprise Search in Kibana](#ech-restrictions-enterprise-search-kibana-integration-traffic-filters)
* [Restoring a snapshot across deployments](#ech-snapshot-restore-enterprise-search-kibana-across-deployments)
* [Migrate Fleet-managed {{agents}} across deployments by restoring a snapshot](#ech-migrate-elastic-agent)
* [Regions and Availability Zones](#ech-regions-and-availability-zone)
* [Known problems](#ech-known-problems)

For limitations related to logging and monitoring, check the [Restrictions and limitations](../../monitor/stack-monitoring/elastic-cloud-stack-monitoring.md) section of the logging and monitoring page.

Occasionally, we also publish information about [Known problems](#ech-known-problems) with our Elasticsearch Add-On for Heroku or the Elastic Stack.

To learn more about the features that are supported by Elasticsearch Add-On for Heroku, check [Elastic Cloud Subscriptions](https://www.elastic.co/cloud/elasticsearch-service/subscriptions?page=docs&placement=docs-body).


## Elasticsearch Add-On for Heroku [ech-restrictions-heroku]

Not all features of our Elasticsearch Service are available to Heroku users. Specifically, you cannot create additional deployments or use different deployment templates.

Generally, if a feature is shown as available in the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body), you can use it.


## Security [ech-restrictions-security]

* File and LDAP realms cannot be used. The Native realm is enabled, but the realm configuration itself is fixed in {{ecloud}}. Alternatively, authentication protocols such as SAML, OpenID Connect, or Kerberos can be used.
* Client certificates, such as PKI certificates, are not supported.
* IPv6 is not supported.


## Transport client [ech-restrictions-transport-client]

* The transport client is not considered thread safe in a cloud environment. We recommend that you use the Java REST client instead. This restriction relates to the fact that your deployments hosted on Elasticsearch Add-On for Heroku are behind proxies, which prevent the transport client from communicating directly with Elasticsearch clusters.
* The transport client is not supported over [private link connections](../../security/aws-privatelink-traffic-filters.md). Use the Java REST client instead, or connect over the public internet.
* The transport client does not work with Elasticsearch clusters at version 7.6 and later that are hosted on Cloud. Transport client continues to work with Elasticsearch clusters at version 7.5 and earlier. Note that the transport client was deprecated with version 7.0 and will be removed with 8.0.


## Elasticsearch and Kibana plugins [ech-restrictions-plugins]

* Kibana plugins are not supported.
* Elasticsearch plugins, are not enabled by default for security purposes. Please reach out to support if you would like to enable Elasticsearch plugins support on your account.
* Some Elasticsearch plugins do not apply to Elasticsearch Add-On for Heroku. For example, you won’t ever need to change discovery, as Elasticsearch Add-On for Heroku handles how nodes discover one another.
* In Elasticsearch 5.0 and later, site plugins are no longer supported. This change does not affect the site plugins Elasticsearch Add-On for Heroku might provide out of the box, such as Kopf or Head, since these site plugins are serviced by our proxies and not Elasticsearch itself.
* In Elasticsearch 5.0 and later, site plugins such as Kopf and Paramedic are no longer provided. We recommend that you use our [cluster performance metrics](../../monitor/stack-monitoring/elastic-cloud-stack-monitoring.md), [X-Pack monitoring features](../../monitor/stack-monitoring/elastic-cloud-stack-monitoring.md) and Kibana’s (6.3+) [Index Management UI](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-mgmt.html) if you want more detailed information or perform index management actions.


## Private Link and SSO to Kibana URLs [ech-restrictions-traffic-filters-kibana-sso]

Currently you can’t use SSO to login directly from {{ecloud}} into Kibana endpoints that are protected by Private Link traffic filters. However, you can still SSO into Private Link protected Kibana endpoints individually using the [SAML](../../users-roles/cluster-or-deployment-auth/saml.md) or [OIDC](../../users-roles/cluster-or-deployment-auth/openid-connect.md) protocol from your own identity provider, just not through the {{ecloud}} console. Stack level authentication using the {{es}} username and password should also work with `{{kibana-id}}.{vpce|privatelink|psc}.domain` URLs.


## PDF report generation using Alerts or Watcher webhooks [ech-restrictions-traffic-filters-watcher]

* PDF report automatic generation via Alerts is not possible on Elastic Cloud.
* PDF report generation isn’t possible for deployments running on Elastic stack version 8.7.0 or before that are protected by traffic filters. This limitation doesn’t apply to public webhooks such as Slack, PagerDuty, and email. For deployments running on Elastic stack version 8.7.1 and beyond, [PDF report automatic generation via Watcher webhook](../../../explore-analyze/report-and-share/automating-report-generation.md#use-watcher) is possible using the `xpack.notification.webhook.additional_token_enabled` configuration setting to bypass traffic filters.


## Kibana [ech-restrictions-kibana]

* The maximum size of a single {{kib}} instance is 8GB. This means, {{kib}} instances can be scaled up to 8GB before they are scaled out. For example, when creating a deployment with a {{kib}} instance of size 16GB, then 2x8GB instances are created. If you face performance issues with {{kib}} PNG or PDF reports, the recommendations are to create multiple, smaller dashboards to export the data, or to use a third party browser extension for exporting the dashboard in the format you need.
* Running an external Kibana in parallel to Elasticsearch Add-On for Heroku’s Kibana instances may cause errors, for example [`Unable to decrypt attribute`](../../../explore-analyze/alerts-cases/alerts/alerting-common-issues.md#rule-cannot-decrypt-api-key), due to a mismatched [`xpack.encryptedSavedObjects.encryptionKey`](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#security-encrypted-saved-objects-settings) as Elasticsearch Add-On for Heroku does not [allow users to set](edit-stack-settings.md) nor expose this value. While workarounds are possible, this is not officially supported nor generally recommended.


## APM Agent central configuration with PrivateLink or traffic filters [ech-restrictions-apm-traffic-filters]

If you are using APM 7.9.0 or older:

* You cannot use [APM Agent central configuration](https://www.elastic.co/guide/en/observability/current/apm-agent-configuration.html) if your deployment is secured by [traffic filters](../../security/traffic-filtering.md).
* If you access your APM deployment over [PrivateLink](../../security/aws-privatelink-traffic-filters.md), to use APM Agent central configuration you need to allow access to the APM deployment over public internet.


## Fleet with PrivateLink or traffic filters [ech-restrictions-fleet-traffic-filters]

* You cannot use Fleet 7.13.x if your deployment is secured by [traffic filters](../../security/traffic-filtering.md). Fleet 7.14.0 and later works with traffic filters (both Private Link and IP filters).
* If you are using Fleet 8.12+, using a remote {{es}} output with a target cluster that has [traffic filters](../../security/traffic-filtering.md) enabled is not currently supported.


## Enterprise Search in Kibana [ech-restrictions-enterprise-search-kibana-integration-traffic-filters]

Enterprise Search’s management interface in Kibana does not work with traffic filters with 8.3.1 and older, it will return an `Insufficient permissions` (403 Forbidden) error. In Kibana 8.3.2, 8.4.0 and higher, the Enterprise Search management interface works with traffic filters.


## Restoring a snapshot across deployments [ech-snapshot-restore-enterprise-search-kibana-across-deployments]

Kibana and Enterprise Search do not currently support restoring a snapshot of their indices across Elastic Cloud deployments.

* [Kibana uses encryption keys](https://www.elastic.co/guide/en/kibana/current/using-kibana-with-security.html#security-configure-settings) in various places, ranging from encrypting data in some areas of reporting, alerts, actions, connector tokens, ingest outputs used in Fleet and Synthetics monitoring to user sessions.
* [Enterprise Search uses encryption keys](https://www.elastic.co/guide/en/enterprise-search/current/encryption-keys.html) when storing content source synchronization credentials, API tokens and other sensitive information.
* Currently, there is not a way to retrieve the values of Kibana and Enterprise Search encryption keys, or set them in the target deployment before restoring a snapshot. As a result, once a snapshot is restored, Kibana and Enterprise Search will not be able to decrypt the data required for some Kibana and Enterprise Search features to function properly in the target deployment.
* If you have already restored a snapshot across deployments and now have broken Kibana saved objects or Enterprise Search features in the target deployment, you will have to recreate all broken configurations and objects, or create a new setup in the target deployment instead of using snapshot restore.

A snapshot taken using the default `found-snapshots` repository can only be restored to deployments in the same region. If you need to restore snapshots across regions, create the destination deployment, connect to the [custom repository](../../tools/snapshot-and-restore/elastic-cloud-hosted.md), and then [restore from a snapshot](../../tools/snapshot-and-restore/restore-snapshot.md).

When restoring from a deployment that’s using searchable snapshots, you must not delete the snapshots in the source deployment even after they are successfully restored in the destination deployment.


## Migrate Fleet-managed {{agents}} across deployments by restoring a snapshot [ech-migrate-elastic-agent]

There are situations where you may need or want to move your installed {{agents}} from being managed in one deployment to being managed in another deployment.

In {{ecloud}}, you can migrate your {{agents}} by taking a snapshot of your source deployment, and restoring it on a target deployment.

To make a seamless migration, after restoring from a snapshot there are some additional steps required, such as updating settings and resetting the agent policy. Check [Migrate Elastic Agents](https://www.elastic.co/guide/en/fleet/current/migrate-elastic-agent.html) for details.


## Regions and Availability Zones [ech-regions-and-availability-zone]

* The AWS `us-west-1` region is limited to two availability zones for ES data nodes and one (tiebreaker only) virtual zone (as depicted by the `-z` in the AZ (`us-west-1z`). Deployment creation with three availability zones for Elasticsearch data nodes for hot, warm, and cold tiers is not possible. This includes scaling an existing deployment with one or two AZs to three availability zones. The virtual zone `us-west-1z` can only hold an Elasticsearch tiebreaker node (no data nodes). The workaround is to use a different AWS US region that allows three availability zones, or to scale existing nodes up within the two availability zones.
* The AWS `eu-central-2` region is limited to two availability zones for CPU Optimized (ARM) Hardware profile ES data node and warm/cold tier. Deployment creation with three availability zones for Elasticsearch data nodes for hot (for CPU Optimized (ARM) profile), warm and cold tiers is not possible. This includes scaling an existing deployment with one or two AZs to three availability zones. The workaround is to use a different AWS region that allows three availability zones, or to scale existing nodes up within the two availability zones.


## Known problems [ech-known-problems]

* There is a known problem affecting clusters with versions 7.7.0 and 7.7.1 due to [a bug in Elasticsearch](https://github.com/elastic/elasticsearch/issues/56739). Although rare, this bug can prevent you from running plans. If this occurs we recommend that you retry the plan, and if that fails please contact support to get your plan through. Because of this bug we recommend you to upgrade to version 7.8 and higher, where the problem has already been addressed.
* A known issue can prevent direct rolling upgrades from Elasticsearch version 5.6.10 to version 6.3.0. As a workaround, we have removed version 6.3.0 from the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body) for new cluster deployments and for upgrading existing ones. If you are affected by this issue, check [Rolling upgrades from 5.6.x to 6.3.0 fails with "java.lang.IllegalStateException: commit doesn’t contain history uuid"](https://elastic.my.salesforce.com/articles/Support_Article/Rolling-upgrades-to-6-3-0-from-5-x-fails-with-java-lang-IllegalStateException-commit-doesn-t-contain-history-uuid?popup=false&id=kA0610000005JFG) in our Elastic Support Portal. If these steps do not work or you do not have access to the Support Portal, you can contact `support@elastic.co`.


## Repository Analysis API is unavailable in Elastic Cloud [ech-repository-analyis-unavailable]

* The Elasticsearch [Repository analysis API](https://www.elastic.co/guide/en/elasticsearch/reference/current/repo-analysis-api.html) is not available in {{ecloud}} due to deployments defaulting to having [operator privileges](../../users-roles/cluster-or-deployment-auth/operator-privileges.md) enabled that prevent non-operator privileged users from using it along with a number of other APIs.
