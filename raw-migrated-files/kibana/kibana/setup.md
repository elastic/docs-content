# Set up [setup]

This section includes information on how to setup Kibana and get it running, including:

* Downloading
* Installing
* Starting
* Configuring
* Upgrading


## Supported platforms [supported-platforms] 

Packages of Kibana are provided for and tested against Linux, Darwin, and Windows. Since Kibana runs on Node.js, we include the necessary Node.js binaries for these platforms. Running Kibana against a separately maintained version of Node.js is not supported.

To support certain older Linux platforms (most notably CentOS7/RHEL7), {{kib}} for Linux ships with a custom build of Node.js with glibc 2.17 support. For details, see [Custom builds of Node.js](https://www.elastic.co/guide/en/kibana/current/upgrading-nodejs.html#custom-nodejs-builds).


## Elasticsearch version [elasticsearch-version] 

Kibana should be configured to run against an Elasticsearch node of the same version. This is the officially supported configuration.

Running different major version releases of Kibana and Elasticsearch (e.g. Kibana 5.x and Elasticsearch 2.x) is not supported, nor is running a minor version of Kibana that is newer than the version of Elasticsearch (e.g. Kibana 5.1 and Elasticsearch 5.0).

Running a minor version of Elasticsearch that is higher than Kibana will generally work in order to facilitate an upgrade process where Elasticsearch is upgraded first (e.g. Kibana 5.0 and Elasticsearch 5.1). In this configuration, a warning will be logged on Kibana server startup, so it’s only meant to be temporary until Kibana is upgraded to the same version as Elasticsearch.

Running different patch version releases of Kibana and Elasticsearch (e.g. Kibana 5.0.0 and Elasticsearch 5.0.1) is generally supported, though we encourage users to run the same versions of Kibana and Elasticsearch down to the patch version.

