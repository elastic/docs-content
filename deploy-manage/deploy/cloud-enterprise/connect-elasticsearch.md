---
navigation_title: Connect to Elasticsearch
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-cloud-id.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-connect.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Connect to {{es}} [ece-connect]

This section explains how to connect client applications to an {{es}} deployment running on ECE. You can use the [endpoint URL](#ece-connect-endpoint) available in the deployment UI, or the [Cloud ID](#ece-cloud-id) for a simplified setup with compatible clients such as Beats and Logstash.

% TBD - not sure if this is totally accurate
% {{ece}} clusters running on ECE only support connections over **HTTP/HTTPS** through the RESTful API. Direct connections to the transport port are not supported.

To successfully connect to a deployment, you need both the connection details and valid authentication credentials for an authorized user in the target deployment. For more details on authentication and authorization mechanisms in ECE, refer to [Users and roles](../../users-roles.md#orchestrator-level).

## Connect using the endpoint URL [ece-connect-endpoint]

To connect to your {{es}} cluster, copy the **{{es}} endpoint** from the deployment page in the [Cloud UI](./log-into-cloud-ui.md).

::::{important}
Application endpoints in ECE are generated based on the domain name configured in **Platform > Settings**. To learn how to modify these endpoints, refer to [Change endpoint URLs](./change-endpoint-urls.md).
::::

Once you have the endpoint, use it in your client application. To test connectivity, you can:
* Open the endpoint in your browser and enter authentication details when prompted.
* Modify the following `curl` example to fit your environment by replacing the URL and proxy CA certificate with your own values.

  ```sh
  curl --cacert /path/to/elastic-ece-ca-cert.pem -u elastic https://<CLUSTER_ID.LOCAL_HOST_IP>.ip.es.io:9243
  {
    "name" : "instance-0000000000",
    "cluster_name" : "f76e96da2a7f4d3f8f3ee25d686b879c",
    "cluster_uuid" : "w2SXqdACQCy5AAixXRxeXg",
    "version" : {
      "number" : "8.17.3",
      "build_flavor" : "default",
      "build_type" : "docker",
      "build_hash" : "a091390de485bd4b127884f7e565c0cad59b10d2",
      "build_date" : "2025-02-28T10:07:26.089129809Z",
      "build_snapshot" : false,
      "lucene_version" : "9.12.0",
      "minimum_wire_compatibility_version" : "7.17.0",
      "minimum_index_compatibility_version" : "7.0.0"
    },
    "tagline" : "You Know, for Search"
  }
  ```

  The previous example authenticates to the cluster using the default `elastic` user. For more information on authentication and authorization in {{es}}, refer to [](../../users-roles.md).

  ::::{note}
  When connecting to {{es}}, you can use one of the following ports:
  * Port 9243 – Secure HTTPS (**recommended**).
  * Port 9200 – Plaintext HTTP (**not recommended**).
  ::::

## Connect using Cloud ID [ece-cloud-id]

The Cloud ID reduces the number of steps required to start sending data from [Beats](beats://reference/index.md) or [Logstash](logstash://reference/index.md) to your hosted {{es}} cluster on ECE, by assigning a unique ID to your cluster.

::::{note}
Connections through Cloud IDs are only supported in Beats and Logstash.
::::


Cloud IDs are available in every deployment page, as showed below:

:::{image} /deploy-manage/images/cloud-enterprise-ec-ce-cloud-id.png
:alt: The Cloud ID and `elastic` user information shown when you create a deployment
:::

Include this ID along with your user credentials (defined in `cloud.auth`) in your Beat or Logstash configuration. ECE will handle the remaining connection details, ensuring secure data transfer to your hosted cluster.

### Before you begin [ece_before_you_begin_16]

To use the Cloud ID, you need:

* A deployment with an {{es}} cluster to send data to.
* Beats or Logstash, installed locally wherever you want to send data from.
* To configure Beats or Logstash, you need:
    * The unique Cloud ID for your deployment, available from the deployment overview page.
    * A user ID and password that has permission to send data to your {{es}} cluster.

::::{important}
        In our examples, we use the `elastic` superuser that every {{es}} cluster comes with. The password for the `elastic` user is provided when you create a deployment (and can also be [reset](../../users-roles/cluster-or-deployment-auth/built-in-users.md) if you forget it). On a production system, you should adapt these examples by creating a user that can write to and access only the minimally required indices. For each Beat, review the specific feature and role table, similar to the one in [Metricbeat](beats://reference/metricbeat/feature-roles.md) documentation.
::::

### Example: Configure Beats with your Cloud ID [ece-cloud-id-beats]

The following example shows how you can send operational data from Metricbeat to a new ECE deployment by using the Cloud ID. While this example uses Metricbeat, the same approach applies to other Beats.

::::{tip}
For others, you can learn more about [getting started](beats://reference/index.md) with each Beat.
::::

To get started with Metricbeat and {{ece}}:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. [Create a new deployment](create-deployment.md) and copy down the password for the `elastic` user.
3. On the deployment overview page, copy down the Cloud ID.
4. Set up the Beat of your choice, such as [Metricbeat](beats://reference/metricbeat/metricbeat-installation-configuration.md).
5. [Configure the Beat output to send to {{ecloud}}](beats://reference/metricbeat/configure-cloud-id.md).

    ::::{note}
    Make sure you replace the values for `cloud.id` and `cloud.auth` with your own information.
    ::::

6. Open {{kib}} and explore!

Metricbeat creates a data view (formerly *index pattern*) with defined fields, searches, visualizations, and dashboards that you can start exploring in {{kib}}. Look for information related to system metrics, such as CPU usage, utilization rates for memory and disk, and details for processes.