# Set up {{es}} [setup]

This section includes information on how to setup Elasticsearch and get it running, including:

* Downloading
* Installing
* Starting
* Configuring


## Supported platforms [supported-platforms]

The matrix of officially supported operating systems and JVMs is available here: [Support Matrix](https://elastic.co/support/matrix). Elasticsearch is tested on the listed platforms, but it is possible that it will work on other platforms too.


## Use dedicated hosts [dedicated-host]

In production, we recommend you run {{es}} on a dedicated host or as a primary service. Several {{es}} features, such as automatic JVM heap sizing, assume it’s the only resource-intensive application on the host or container. For example, you might run {{metricbeat}} alongside {{es}} for cluster statistics, but a resource-heavy {{ls}} deployment should be on its own host.
