---
applies_to:
  deployment:
    ess: ga
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-cloud-id.html
---

# Find your Cloud ID [ec-cloud-id]

The Cloud ID reduces the number of steps required to start sending data from Beats or Logstash to your hosted Elasticsearch cluster on {{ecloud}}. Because we made it easier to send data, you can start exploring visualizations in Kibana on {{ecloud}} that much more quickly.

:::{image} ../../../images/cloud-ec-ce-cloud-id-beats-logstash.png
:alt: Exploring data from Beats or Logstash in Kibana after sending it to a hosted Elasticsearch cluster
:::

The Cloud ID works by assigning a unique ID to your hosted Elasticsearch cluster on {{ecloud}}. All deployments automatically get a Cloud ID.

You include your Cloud ID along with your {{ecloud}} user credentials (defined in `cloud.auth`) when you run Beats or Logstash locally, and then let {{ecloud}} handle all of the remaining connection details to send the data to your hosted cluster on {{ecloud}} safely and securely.

:::{image} ../../../images/cloud-ec-ce-cloud-id.png
:alt: The Cloud ID and `elastic` user information shown when you create a deployment
:::


## What are Beats and Logstash? [ec_what_are_beats_and_logstash]

Not sure why you need Beats or Logstash? Here’s what they do:

* [Beats](https://www.elastic.co/products/beats) is our open source platform for single-purpose data shippers. The purpose of Beats is to help you gather data from different sources and to centralize the data by shipping it to Elasticsearch. Beats install as lightweight agents and ship data from hundreds or thousands of machines to your hosted Elasticsearch cluster on {{ecloud}}. If you want more processing muscle, Beats can also ship to Logstash for transformation and parsing before the data gets stored in Elasticsearch.
* [Logstash](https://www.elastic.co/products/logstash) is an open source, server-side data processing pipeline that ingests data from a multitude of sources simultaneously, transforms it, and then sends it to your favorite place where you stash things, here your hosted Elasticsearch cluster on {{ecloud}}. Logstash supports a variety of inputs that pull in events from a multitude of common sources — logs, metrics, web applications, data stores, and various AWS services — all in continuous, streaming fashion.


## Before you begin [ec_before_you_begin_3]

To use the Cloud ID, you need:

* A deployment with an Elasticsearch cluster to send data to.
* Beats or Logstash, installed locally wherever you want to send data from.
* To configure Beats or Logstash, you need:

    * The unique Cloud ID for your deployment, available from the deployment overview page.
    * A user ID and password that has permission to send data to your cluster.

        In our examples, we use the `elastic` superuser that every Elasticsearch cluster comes with. The password for the `elastic` user is provided when you create a deployment (and can also be [reset](../../users-roles/cluster-or-deployment-auth/built-in-users.md) if you forget it). On a production system, you should adapt these examples by creating a user that can write to and access only the minimally required indices. For each Beat, review the specific feature and role table, similar to the one in [Metricbeat](beats://reference/metricbeat/feature-roles.md) documentation.



## Configure Beats with your Cloud ID [ec-cloud-id-beats]

The following example shows how you can send operational data from Metricbeat to {{ecloud}} by using the Cloud ID. Any of the available Beats will work, but we had to pick one for this example.

::::{tip}
For others, you can learn more about [getting started](beats://reference/index.md) with each Beat.
::::


To get started with Metricbeat and {{ecloud}}:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. [Create a new deployment](create-an-elastic-cloud-hosted-deployment.md) and copy down the password for the `elastic` user.
3. On the deployment overview page, copy down the Cloud ID.
4. Set up the Beat of your choice, such as [Metricbeat version 7.17](beats://reference/metricbeat/metricbeat-installation-configuration.md).
5. [Configure the Beat output to send to Elastic Cloud](beats://reference/metricbeat/configure-cloud-id.md).

    ::::{note}
    Make sure you replace the values for `cloud.id` and `cloud.auth` with your own information.
    ::::

6. Open Kibana and explore!

Metricbeat creates a data view (formerly *index pattern*) with defined fields, searches, visualizations, and dashboards that you can start exploring in Kibana. Look for information related to system metrics, such as CPU usage, utilization rates for memory and disk, and details for processes.

