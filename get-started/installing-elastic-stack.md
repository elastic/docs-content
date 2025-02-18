# Installing the Elastic Stack [installing-elastic-stack]

When installing the Elastic Stack, you must use the same version across the entire stack. For example, if you are using Elasticsearch 9.0.0-beta1, you install Beats 9.0.0-beta1, APM Server 9.0.0-beta1, Elasticsearch Hadoop 9.0.0-beta1, Kibana 9.0.0-beta1, and Logstash 9.0.0-beta1.

If you’re upgrading an existing installation, see [Upgrading the Elastic Stack](../deploy-manage/upgrade/deployment-or-cluster.md) for information about how to ensure compatibility with 9.0.0-beta1.

For an example of installing and configuring the {{stack}}, you can try out our [Tutorial 1: Installing a self-managed {{stack}}](../deploy-manage/deploy/self-managed/installing-elasticsearch.md). After that, you can also learn how to secure your installation for production following the steps in [Tutorial 2: Securing a self-managed {{stack}}](../deploy-manage/security/secure-your-cluster-deployment.md).


## Network requirements [network-requirements] 

To install the Elastic Stack on-premises, these ports need to be open for each component.

| Default port  | Component |
| ------------- | ------------- |
| 5044 | {{agent}} → {{ls}}<br>{{beats}} → {{ls}} |
| 5601 | {{kib}}<br>{{agent}} → {{fleet}}<br>{{fleet-server}} → {{fleet}} |
| 8220 | {{agent}} → {{fleet-server}}<br>APM Server |
| 9200-9300 | {{es}} REST API |
| 9300-9400 | {{es}} node transport and communication |
| 9600-9700 | {{ls}} REST API |

Each Elastic integration has its own ports and dependencies. Verify these ports and dependencies before installation. Refer to [{{integrations}}](https://docs.elastic.co/en/integrations).

For more information on supported network configurations, refer to [{{es}} Ingest Architectures](https://www.elastic.co/guide/en/ingest/current).


## Installation order [install-order-elastic-stack] 

Install the Elastic Stack products you want to use in the following order:

1. [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)
2. [Kibana](https://www.elastic.co/guide/en/kibana/current/install.html) 
3. [Logstash](https://www.elastic.co/guide/en/logstash/current/installing-logstash.html)
4. [Elastic Agent](https://www.elastic.co/guide/en/fleet/current/elastic-agent-installation.html) or [Beats](https://www.elastic.co/guide/en/beats/libbeat/current/getting-started.html)
5. [APM](https://www.elastic.co/guide/en/apm/guide/current/apm-quick-start.html)
6. [Elasticsearch Hadoop](https://www.elastic.co/guide/en/elasticsearch/hadoop/current/install.html)

Installing in this order ensures that the components each product depends on are in place.


## Installing on {{ecloud}} [install-elastic-stack-for-elastic-cloud] 

Installing on {{ecloud}} is easy: a single click creates an {{es}} cluster configured to the size you want, with or without high availability. The subscription features are always installed, so you automatically have the ability to secure and monitor your cluster. {{kib}} is enabled automatically, and a number of popular plugins are readily available.

Some {{ecloud}} features can be used only with a specific subscription. For more information, refer to [https://www.elastic.co/pricing/](https://www.elastic.co/pricing/).



