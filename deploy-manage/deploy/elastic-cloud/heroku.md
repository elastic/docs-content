---
navigation_title: Heroku
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-getting-started.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-about.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-getting-started-next-steps.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-restrictions.html
applies_to:
  deployment:
    ess:
products:
  - id: cloud-hosted
---

# {{es}} Add-On for Heroku [ech-getting-started]

This documentation applies to Heroku users who want to make use of the {{es}} Add-On for Heroku that is available from the [Heroku Dashboard](https://dashboard.heroku.com/), or that can be installed from the CLI.

The add-on runs on {{ecloud}} and provides access to [Elasticsearch](https://www.elastic.co/products/elasticsearch), the open source, distributed, RESTful search engine. Many other features of the {{stack}} are also readily available to Heroku users through the [{{es}} Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body) after you install the add-on. For example, you can use {{kib}} to visualize your {{es}} data.

To learn more about what plans are available for Heroku users and their cost, refer to the [{{es}} add-on](https://elements.heroku.com/addons/foundelasticsearch) in the Elements Marketplace.

:::{warning}
The {{es}} Add-on for Heroku has several limitations that do not apply to [other {{ecloud}} sign-up methods](/deploy-manage/deploy/elastic-cloud/create-an-organization.md). To get access to all {{ecloud}} functionality, consider signing up using another method.
:::

## Limitations

Not all features of {{ecloud}} are available to Heroku users. Specifically, you cannot create additional deployments or use different deployment templates.

Generally, if a feature is shown as available in the [{{heroku}} console](https://cloud.elastic.co?page=docs&placement=docs-body), you can use it.

[{{es}} Machine Learning](/explore-analyze/machine-learning.md), [Elastic APM](/solutions/observability/apm/index.md) and [Elastic Fleet Server](/reference/fleet/index.md) are not supported by the {{es}} Add-On for Heroku.

For other restrictions that apply to all of {{ecloud}}, refer to [](/deploy-manage/deploy/elastic-cloud/restrictions-known-problems.md).

## Get started

To get started with the {{es}} Add-on for Heroku, [install the add-on](/deploy-manage/deploy/elastic-cloud/heroku-getting-started-installing.md).

After you install, you can access your deployment:

* [](/deploy-manage/deploy/elastic-cloud/heroku-getting-started-accessing.md): Access the {{ecloud}} Console for your {{es}} Add-On for Heroku deployment.
* [](/deploy-manage/deploy/elastic-cloud/heroku-working-with-elasticsearch.md): Retrieve  the {{es}} endpoint address and send requests to {{es}}.
* [](/deploy-manage/deploy/elastic-cloud/access-kibana.md): Access {{kib}}.
* [Access the API console](cloud://reference/cloud-hosted/ec-api-console.md): Access the API console to make requests without logging into your deployment.

## Heroku-specific hardware and regions

The {{es}} Add-on for Heroku in on specific AWS regions only. To learn about the supported AWS regions and hardware, refer to the following pages:

* [](/deploy-manage/deploy/elastic-cloud/heroku-reference-hardware.md)
* [](/deploy-manage/deploy/elastic-cloud/heroku-reference-regions.md)

## More about {{ech}} [ec-about]

Find more information about {{ech}} on the following pages. This information is subject to the {{es}} Add-on for Heroku [limitations](/deploy-manage/deploy/elastic-cloud/heroku.md).

* [Learn the basics of operating an {{ech}} deployment](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md)
* [](/deploy-manage/deploy/elastic-cloud/manage-deployments.md)
* [](/deploy-manage/license.md)
* [](/deploy-manage/deploy/elastic-cloud/available-stack-versions.md)
* [](/deploy-manage/cloud-organization/service-status.md)
* [Get help](/troubleshoot/index.md)

## Next steps [next-steps]

After have provisioned your first deployment, you’re ready to index data into the deployment and explore the advanced capabilities of {{heroku}}.

### Index data [ech-ingest-data]

There are several ways to ingest data into the deployment:

* Use the sample data available from the {{kib}} home page without loading your own data. There are multiple data sets available and you can add them with one click.
* Ingest your own data. [Learn more](/manage-data/ingest.md).
* Have existing {{es}} data? Consider your [migration options](../../../manage-data/migrate.md).


### Increase security [ech-increase-security]

You might want to add more layers of security to your deployment, such as:

* Add more users to the deployment with third-party authentication providers and services like [SAML](../../users-roles/cluster-or-deployment-auth/saml.md), [OpenID Connect](../../users-roles/cluster-or-deployment-auth/openid-connect.md), or [Kerberos](../../users-roles/cluster-or-deployment-auth/kerberos.md).
* Do not use clients that only support HTTP to connect to {{ecloud}}. If you need to do so, you should use a reverse proxy setup.
* Create [network security policies](/deploy-manage/security/network-security.md) and apply them to your deployments.
* If needed, you can [reset](../../users-roles/cluster-or-deployment-auth/built-in-users.md) the `elastic` password.

### Scale or adjust your deployment [echscale_or_adjust_your_deployment]

You might find that you need a larger deployment for the workload, or [upgrade the {{es}} version](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ech.md) for the latest features. All of this can be done after provisioning by [changing your deployment configuration](/deploy-manage/deploy/elastic-cloud/manage-deployments.md).