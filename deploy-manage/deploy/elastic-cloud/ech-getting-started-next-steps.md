---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-getting-started-next-steps.html
---

# Next steps [ech-getting-started-next-steps]

Now that you have provisioned your first deployment, you’re ready to index data into the deployment and explore the advanced capabilities of Elasticsearch Add-On for Heroku.


## Index data [ech-ingest-data] 

It’s why you’re here right? You’re looking to solve an issue or improve your experience with your data.

There are several ways to ingest data into the deployment:

* Use the sample data available from the Kibana home page in versions 6.4.0 and later, without loading your own data. There are multiple data sets available and you can add them with one click.
* Got existing Elasticsearch data? Consider your [migration options](../../../manage-data/migrate.md).


## Increase security [ech-increase-security] 

You might want to add more layers of security to your deployment, such as:

* Add more users to the deployment with third-party authentication providers and services like [SAML](../../users-roles/cluster-or-deployment-auth/saml.md), [OpenID Connect](../../users-roles/cluster-or-deployment-auth/openid-connect.md), or [Kerberos](../../users-roles/cluster-or-deployment-auth/kerberos.md).
* Do not use clients that only support HTTP to connect to Elastic Cloud. If you need to do so, you should use a reverse proxy setup.
* Create [traffic filters](../../security/traffic-filtering.md) and apply them to your deployments.
* If needed, you can [reset](../../users-roles/cluster-or-deployment-auth/built-in-users.md) the `elastic` password.


## Scale or adjust your deployment [echscale_or_adjust_your_deployment] 

You might find that you need a larger deployment for the workload. Or maybe you want to upgrade the Elasticsearch version for the latest features. Perhaps you’d like to add some plugins, enable APM, or machine learning. All of this can be done after provisioning by [changing your deployment configuration](cloud-hosted.md).

