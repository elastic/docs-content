---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-manage-elastic-stack.html
---

# Manage Elastic Stack versions [ece-manage-elastic-stack]

Elastic Cloud Enterprise ships with a number of different versions of the Elastic Stack containing Elasticsearch and Kibana. Periodically, you might need to manage Elastic Stack versions for one of the following reasons:

* To add new versions of the Elastic Stack as they become available
* To obtain information about existing Elastic Stack versions
* To update existing versions of the Elastic Stack
* To add the Elastic Stack versions that shipped with a version of ECE that you upgraded to

New or updated versions of the Elastic Stack must be prepared to work with Elastic Cloud Enterprise and are provided as packs that you can download.

::::{important}
Elasticsearch 7.8 and later comes with Index Lifecycle Management (ILM) always enabled. Before upgrading to 7.8 or later, to avoid any unpredictable behavior it is important to configure hot-warm clusters on Elastic Cloud Enterprise with ILM rather than index curation. Check [migrate to index lifecycle management](../../../manage-data/lifecycle/index-lifecycle-management.md) for existing clusters, and [configure index management](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-index-management.html) for new clusters.
::::



## Most recent Elastic Stack packs [ece_most_recent_elastic_stack_packs]

:::{important}
Enterprise Search is not available in versions 9.0+.
:::

The following are the most recently released Elastic Stack packs for version 8.x, 7.x, and 6.x, respectively:

$$$ece-elastic-stack-stackpacks-recent$$$

| Required downloads | Minimum required ECE version |
| --- | --- |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.17.1](https://download.elastic.co/cloud-enterprise/versions/8.17.1.zip) | ECE 3.0.0<br>(+ Docker 20.10.10+ required for 8.16+) |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.27](https://download.elastic.co/cloud-enterprise/versions/7.17.27.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.23](https://download.elastic.co/cloud-enterprise/versions/6.8.23.zip) | ECE 1.1.4 |


## All available Elastic Stack packs [ece-elastic-stack-stackpacks]

Following is the full list of available packs containing Elastic Stack versions. Note that Enterprise Search was introduced with ECE 2.6.0 and requires that version or higher.

::::{dropdown} **Expand to view the full list**
| Required downloads | Minimum required ECE version |
| --- | --- |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.17.1](https://download.elastic.co/cloud-enterprise/versions/8.17.1.zip) | ECE 3.0.0<br>(+ docker 20.10.10+ required for 8.16+) |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.17.0](https://download.elastic.co/cloud-enterprise/versions/8.17.0.zip) | ECE 3.0.0<br>(+ docker 20.10.10+ required for 8.16+) |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.16.3](https://download.elastic.co/cloud-enterprise/versions/8.16.3.zip) | ECE 3.0.0<br>(+ Docker 20.10.10+ required for 8.16+) |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.16.2](https://download.elastic.co/cloud-enterprise/versions/8.16.2.zip) | ECE 3.0.0<br>(+ Docker 20.10.10+ required for 8.16+) |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.16.1](https://download.elastic.co/cloud-enterprise/versions/8.16.1.zip) | ECE 3.0.0<br>(+ Docker 20.10.10+ required for 8.16+) |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.16.0](https://download.elastic.co/cloud-enterprise/versions/8.16.0.zip) | ECE 3.0.0<br>(+ Docker 20.10.10+ required for 8.16+) |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.15.5](https://download.elastic.co/cloud-enterprise/versions/8.15.5.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.15.4](https://download.elastic.co/cloud-enterprise/versions/8.15.4.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.15.3](https://download.elastic.co/cloud-enterprise/versions/8.15.3.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.15.2](https://download.elastic.co/cloud-enterprise/versions/8.15.2.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.15.1](https://download.elastic.co/cloud-enterprise/versions/8.15.1.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.15.0](https://download.elastic.co/cloud-enterprise/versions/8.15.0.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.14.3](https://download.elastic.co/cloud-enterprise/versions/8.14.3.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.14.2](https://download.elastic.co/cloud-enterprise/versions/8.14.2.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.14.1](https://download.elastic.co/cloud-enterprise/versions/8.14.1.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.14.0](https://download.elastic.co/cloud-enterprise/versions/8.14.0.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.13.4](https://download.elastic.co/cloud-enterprise/versions/8.13.4.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.13.3](https://download.elastic.co/cloud-enterprise/versions/8.13.3.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.13.2](https://download.elastic.co/cloud-enterprise/versions/8.13.2.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.13.1](https://download.elastic.co/cloud-enterprise/versions/8.13.1.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.13.0](https://download.elastic.co/cloud-enterprise/versions/8.13.0.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.12.2](https://download.elastic.co/cloud-enterprise/versions/8.12.2.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.12.1](https://download.elastic.co/cloud-enterprise/versions/8.12.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.12.0](https://download.elastic.co/cloud-enterprise/versions/8.12.0.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.11.4](https://download.elastic.co/cloud-enterprise/versions/8.11.4.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.11.3](https://download.elastic.co/cloud-enterprise/versions/8.11.3.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.11.2](https://download.elastic.co/cloud-enterprise/versions/8.11.2.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.11.1](https://download.elastic.co/cloud-enterprise/versions/8.11.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.11.0](https://download.elastic.co/cloud-enterprise/versions/8.11.0.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.10.4](https://download.elastic.co/cloud-enterprise/versions/8.10.4.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.10.3](https://download.elastic.co/cloud-enterprise/versions/8.10.3.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.10.2](https://download.elastic.co/cloud-enterprise/versions/8.10.2.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.10.1](https://download.elastic.co/cloud-enterprise/versions/8.10.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.10.0](https://download.elastic.co/cloud-enterprise/versions/8.10.0.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.9.2](https://download.elastic.co/cloud-enterprise/versions/8.9.2.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.9.1](https://download.elastic.co/cloud-enterprise/versions/8.9.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.9.0](https://download.elastic.co/cloud-enterprise/versions/8.9.0.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.8.2](https://download.elastic.co/cloud-enterprise/versions/8.8.2.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.8.1](https://download.elastic.co/cloud-enterprise/versions/8.8.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.8.0](https://download.elastic.co/cloud-enterprise/versions/8.8.0.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.7.1](https://download.elastic.co/cloud-enterprise/versions/8.7.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.7.0](https://download.elastic.co/cloud-enterprise/versions/8.7.0.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.6.2](https://download.elastic.co/cloud-enterprise/versions/8.6.2.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.6.1](https://download.elastic.co/cloud-enterprise/versions/8.6.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.6.0](https://download.elastic.co/cloud-enterprise/versions/8.6.0.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.5.3](https://download.elastic.co/cloud-enterprise/versions/8.5.3.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.5.2](https://download.elastic.co/cloud-enterprise/versions/8.5.2.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.5.1](https://download.elastic.co/cloud-enterprise/versions/8.5.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.5.0](https://download.elastic.co/cloud-enterprise/versions/8.5.0.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.4.3](https://download.elastic.co/cloud-enterprise/versions/8.4.3.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.4.2](https://download.elastic.co/cloud-enterprise/versions/8.4.2.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.4.1](https://download.elastic.co/cloud-enterprise/versions/8.4.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.4.0](https://download.elastic.co/cloud-enterprise/versions/8.4.0.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.3.3](https://download.elastic.co/cloud-enterprise/versions/8.3.3.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.3.2](https://download.elastic.co/cloud-enterprise/versions/8.3.2.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.3.1](https://download.elastic.co/cloud-enterprise/versions/8.3.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.3.0](https://download.elastic.co/cloud-enterprise/versions/8.3.0.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.2.3](https://download.elastic.co/cloud-enterprise/versions/8.2.3.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.2.2](https://download.elastic.co/cloud-enterprise/versions/8.2.2.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.2.1](https://download.elastic.co/cloud-enterprise/versions/8.2.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.2.0](https://download.elastic.co/cloud-enterprise/versions/8.2.0.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.1.3](https://download.elastic.co/cloud-enterprise/versions/8.1.3.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.1.2](https://download.elastic.co/cloud-enterprise/versions/8.1.2.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.1.1](https://download.elastic.co/cloud-enterprise/versions/8.1.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.1.0](https://download.elastic.co/cloud-enterprise/versions/8.1.0.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.0.1](https://download.elastic.co/cloud-enterprise/versions/8.0.1.zip) | ECE 3.0.0 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 8.0.0](https://download.elastic.co/cloud-enterprise/versions/8.0.0.zip) | ECE 3.0.0 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.27](https://download.elastic.co/cloud-enterprise/versions/7.17.27.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.26](https://download.elastic.co/cloud-enterprise/versions/7.17.26.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.25](https://download.elastic.co/cloud-enterprise/versions/7.17.25.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.24](https://download.elastic.co/cloud-enterprise/versions/7.17.24.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.23](https://download.elastic.co/cloud-enterprise/versions/7.17.23.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.22](https://download.elastic.co/cloud-enterprise/versions/7.17.22.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.21](https://download.elastic.co/cloud-enterprise/versions/7.17.21.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.20](https://download.elastic.co/cloud-enterprise/versions/7.17.20.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.19](https://download.elastic.co/cloud-enterprise/versions/7.17.19.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.18](https://download.elastic.co/cloud-enterprise/versions/7.17.18.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.17](https://download.elastic.co/cloud-enterprise/versions/7.17.17.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.16](https://download.elastic.co/cloud-enterprise/versions/7.17.16.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.15](https://download.elastic.co/cloud-enterprise/versions/7.17.15.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.14](https://download.elastic.co/cloud-enterprise/versions/7.17.14.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.13](https://download.elastic.co/cloud-enterprise/versions/7.17.13.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.12](https://download.elastic.co/cloud-enterprise/versions/7.17.12.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.11](https://download.elastic.co/cloud-enterprise/versions/7.17.11.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.10](https://download.elastic.co/cloud-enterprise/versions/7.17.10.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.9](https://download.elastic.co/cloud-enterprise/versions/7.17.9.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.8](https://download.elastic.co/cloud-enterprise/versions/7.17.8.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.7](https://download.elastic.co/cloud-enterprise/versions/7.17.7.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.6](https://download.elastic.co/cloud-enterprise/versions/7.17.6.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.5](https://download.elastic.co/cloud-enterprise/versions/7.17.5.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.4](https://download.elastic.co/cloud-enterprise/versions/7.17.4.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.3](https://download.elastic.co/cloud-enterprise/versions/7.17.3.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.2](https://download.elastic.co/cloud-enterprise/versions/7.17.2.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.1](https://download.elastic.co/cloud-enterprise/versions/7.17.1.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.17.0](https://download.elastic.co/cloud-enterprise/versions/7.17.0.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.16.3](https://download.elastic.co/cloud-enterprise/versions/7.16.3.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.16.2](https://download.elastic.co/cloud-enterprise/versions/7.16.2.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.16.1](https://download.elastic.co/cloud-enterprise/versions/7.16.1.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.16.0](https://download.elastic.co/cloud-enterprise/versions/7.16.0.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.15.2](https://download.elastic.co/cloud-enterprise/versions/7.15.2.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.15.1](https://download.elastic.co/cloud-enterprise/versions/7.15.1.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.15.0](https://download.elastic.co/cloud-enterprise/versions/7.15.0.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.14.2](https://download.elastic.co/cloud-enterprise/versions/7.14.2.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.14.1](https://download.elastic.co/cloud-enterprise/versions/7.14.1.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.14.0](https://download.elastic.co/cloud-enterprise/versions/7.14.0.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.13.4](https://download.elastic.co/cloud-enterprise/versions/7.13.4.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.13.3](https://download.elastic.co/cloud-enterprise/versions/7.13.3.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.13.2](https://download.elastic.co/cloud-enterprise/versions/7.13.2.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.13.1](https://download.elastic.co/cloud-enterprise/versions/7.13.1.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.13.0](https://download.elastic.co/cloud-enterprise/versions/7.13.0.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.12.1](https://download.elastic.co/cloud-enterprise/versions/7.12.1.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.12.0](https://download.elastic.co/cloud-enterprise/versions/7.12.0.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.11.2](https://download.elastic.co/cloud-enterprise/versions/7.11.2.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.11.1](https://download.elastic.co/cloud-enterprise/versions/7.11.1.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.11.0](https://download.elastic.co/cloud-enterprise/versions/7.11.0.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.10.2](https://download.elastic.co/cloud-enterprise/versions/7.10.2.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.10.1](https://download.elastic.co/cloud-enterprise/versions/7.10.1.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.10.0](https://download.elastic.co/cloud-enterprise/versions/7.10.0.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.9.3](https://download.elastic.co/cloud-enterprise/versions/7.9.3.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.9.2](https://download.elastic.co/cloud-enterprise/versions/7.9.2.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.9.1](https://download.elastic.co/cloud-enterprise/versions/7.9.1.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.9.0](https://download.elastic.co/cloud-enterprise/versions/7.9.0.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.8.1](https://download.elastic.co/cloud-enterprise/versions/7.8.1.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.8.0](https://download.elastic.co/cloud-enterprise/versions/7.8.0.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.7.1](https://download.elastic.co/cloud-enterprise/versions/7.7.1.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and Enterprise Search stack pack: 7.7.0](https://download.elastic.co/cloud-enterprise/versions/7.7.0.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and App Search stack pack: 7.6.2](https://download.elastic.co/cloud-enterprise/versions/7.6.2.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and App Search stack pack: 7.6.1](https://download.elastic.co/cloud-enterprise/versions/7.6.1.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and App Search stack pack: 7.6.0](https://download.elastic.co/cloud-enterprise/versions/7.6.0.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and App Search stack pack: 7.5.2](https://download.elastic.co/cloud-enterprise/versions/7.5.2.zip) | ECE 2.2.2 |
| [ Elasticsearch, Kibana, APM, and App Search stack pack: 7.5.1](https://download.elastic.co/cloud-enterprise/versions/7.5.1.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and App Search stack pack: 7.5.0](https://download.elastic.co/cloud-enterprise/versions/7.5.0.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and App Search stack pack: 7.4.2](https://download.elastic.co/cloud-enterprise/versions/7.4.2.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and App Search stack pack: 7.4.1](https://download.elastic.co/cloud-enterprise/versions/7.4.1.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, APM, and App Search stack pack: 7.4.0](https://download.elastic.co/cloud-enterprise/versions/7.4.0.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, and APM stack pack: 7.3.2](https://download.elastic.co/cloud-enterprise/versions/7.3.2.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, and APM stack pack: 7.3.1](https://download.elastic.co/cloud-enterprise/versions/7.3.1.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, and APM stack pack: 7.3.0](https://download.elastic.co/cloud-enterprise/versions/7.3.0.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, and APM stack pack: 7.2.1](https://download.elastic.co/cloud-enterprise/versions/7.2.1.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, and APM stack pack: 7.2.0](https://download.elastic.co/cloud-enterprise/versions/7.2.0.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, and APM stack pack: 7.1.1](https://download.elastic.co/cloud-enterprise/versions/7.1.1.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, and APM stack pack: 7.1.0](https://download.elastic.co/cloud-enterprise/versions/7.1.0.zip) | ECE 2.2.2 |
| [Elasticsearch, Kibana, and APM stack pack: 7.0.1](https://download.elastic.co/cloud-enterprise/versions/7.0.1.zip) | ECE 2.2.0 |
| [Elasticsearch, Kibana, and APM stack pack: 7.0.0](https://download.elastic.co/cloud-enterprise/versions/7.0.0.zip) | ECE 2.2.0 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.23](https://download.elastic.co/cloud-enterprise/versions/6.8.23.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.22](https://download.elastic.co/cloud-enterprise/versions/6.8.22.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.21](https://download.elastic.co/cloud-enterprise/versions/6.8.21.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.20](https://download.elastic.co/cloud-enterprise/versions/6.8.20.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.19](https://download.elastic.co/cloud-enterprise/versions/6.8.19.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.18](https://download.elastic.co/cloud-enterprise/versions/6.8.18.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.17](https://download.elastic.co/cloud-enterprise/versions/6.8.17.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.16](https://download.elastic.co/cloud-enterprise/versions/6.8.16.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.15](https://download.elastic.co/cloud-enterprise/versions/6.8.15.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.14](https://download.elastic.co/cloud-enterprise/versions/6.8.14.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.13](https://download.elastic.co/cloud-enterprise/versions/6.8.13.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.12](https://download.elastic.co/cloud-enterprise/versions/6.8.12.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.11](https://download.elastic.co/cloud-enterprise/versions/6.8.11.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.10](https://download.elastic.co/cloud-enterprise/versions/6.8.10.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.9](https://download.elastic.co/cloud-enterprise/versions/6.8.9.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.8](https://download.elastic.co/cloud-enterprise/versions/6.8.8.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.7](https://download.elastic.co/cloud-enterprise/versions/6.8.7.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.6](https://download.elastic.co/cloud-enterprise/versions/6.8.6.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.5](https://download.elastic.co/cloud-enterprise/versions/6.8.5.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.4](https://download.elastic.co/cloud-enterprise/versions/6.8.4.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.3](https://download.elastic.co/cloud-enterprise/versions/6.8.3.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.2](https://download.elastic.co/cloud-enterprise/versions/6.8.2.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.1](https://download.elastic.co/cloud-enterprise/versions/6.8.1.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.8.0](https://download.elastic.co/cloud-enterprise/versions/6.8.0.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.7.2](https://download.elastic.co/cloud-enterprise/versions/6.7.2.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.7.1](https://download.elastic.co/cloud-enterprise/versions/6.7.1.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.7.0](https://download.elastic.co/cloud-enterprise/versions/6.7.0.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.6.2](https://download.elastic.co/cloud-enterprise/versions/6.6.2.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.6.1](https://download.elastic.co/cloud-enterprise/versions/6.6.1.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.6.0](https://download.elastic.co/cloud-enterprise/versions/6.6.0.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.5.4](https://download.elastic.co/cloud-enterprise/versions/6.5.4.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.5.3](https://download.elastic.co/cloud-enterprise/versions/6.5.3.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.5.2](https://download.elastic.co/cloud-enterprise/versions/6.5.2.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.5.1](https://download.elastic.co/cloud-enterprise/versions/6.5.1.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.5.0](https://download.elastic.co/cloud-enterprise/versions/6.5.0.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.4.3](https://download.elastic.co/cloud-enterprise/versions/6.4.3.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.4.2](https://download.elastic.co/cloud-enterprise/versions/6.4.2.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.4.1](https://download.elastic.co/cloud-enterprise/versions/6.4.1.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.4.0](https://download.elastic.co/cloud-enterprise/versions/6.4.0.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.3.2](https://download.elastic.co/cloud-enterprise/versions/6.3.2.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.3.1](https://download.elastic.co/cloud-enterprise/versions/6.3.1.zip) | ECE 1.1.4 |
| [Elasticsearch, Kibana, and APM stack pack: 6.3.0](https://download.elastic.co/cloud-enterprise/versions/6.3.0.zip) | ECE 1.1.4 |
| [Elasticsearch and Kibana stack pack: 6.2.4](https://download.elastic.co/cloud-enterprise/versions/6.2.4.zip) | ECE 1.1.2 |
| [Elasticsearch and Kibana stack pack: 6.2.3](https://download.elastic.co/cloud-enterprise/versions/6.2.3.zip) | ECE 1.1.2 |
| [Elasticsearch and Kibana stack pack: 6.2.2](https://download.elastic.co/cloud-enterprise/versions/6.2.2.zip) | ECE 1.1.2 |
| [Elasticsearch and Kibana stack pack: 6.1.4](https://download.elastic.co/cloud-enterprise/versions/6.1.4.zip) | ECE 1.1.2 |
| [Elasticsearch and Kibana stack pack: 6.1.3](https://download.elastic.co/cloud-enterprise/versions/6.1.3.zip) | ECE 1.1.2 |
| [Elasticsearch and Kibana stack pack: 6.0.1](https://download.elastic.co/cloud-enterprise/versions/6.0.1.zip) | ECE 1.1.2 |
| [Elasticsearch and Kibana stack pack: 6.0.0](https://download.elastic.co/cloud-enterprise/versions/6.0.0.zip) | ECE 1.1.0 |
| [Elasticsearch and Kibana stack pack: 5.6.16](https://download.elastic.co/cloud-enterprise/versions/5.6.16.zip) | ECE 1.1.0 |
| [Elasticsearch and Kibana stack pack: 2.4.6](https://download.elastic.co/cloud-enterprise/versions/2.4.6.zip) | ECE 1.0.0 |
| [Elasticsearch and Kibana stack pack: 2.4.5](https://download.elastic.co/cloud-enterprise/versions/2.4.5.zip) | ECE 1.0.0 |

::::


::::{tip}
For *offline* or *air-gapped* installations, additional steps are required to add Elastic Stack packs, as these packs do not contain any Docker images. After downloading a stack pack, you also need to pull and load the Docker images that match the Elastic Stack version. To learn more about what Docker images you need and about pulling and loading Docker images, check [Install ECE offline](air-gapped-install.md).
::::



## Before you begin [ece_before_you_begin_10]

The examples shown all use HTTPS over port 12443, which requires that you have [a TLS certificate configured](../../security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md). Alternatively, you can specify the `-k` option to turn off certificate verification, as shown in our examples, or use HTTP over port 12400.


## Get Elastic Stack information [ece_get_elastic_stack_information]

You can obtain information about existing Elastic Stack versions that are available in your installation through the Cloud UI or through the command line.

To obtain information about available Elastic Stack versions through the Cloud UI:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. From the **Platform** menu, select **Elastic Stack**.
3. Select the version that you want.

    The available Elastic Stack versions are shown. More detailed information about Docker images, plugins, and related Kibana versions are also available for each Elasticsearch version.


To obtain information about available Elastic Stack versions through the command line:

```sh
curl -X GET -u USER:PASSWORD https://COORDINATOR_HOST:12443/api/v1/stack/versions
```

For example (output abridged for brevity):

```
curl -X GET -u admin:4Z52y8Gq7PrxMDy47ipJPSh4ozBMynOGa9HWxcy2D3j https://10.56.12.153:12443/api/v1/stack/versions
{
  "stacks": [
    {
      "version": "2.4.5",
      "template": {
        "template_version": "",
        "hashes": []
      },
      "elasticsearch": {
        "docker_image": "docker.elastic.co/cloud-enterprise/elasticsearch:2.4.5-0",
        "plugins": [
          "graph",
          "analysis-icu",
          "analysis-kuromoji",
          "analysis-smartcn",
          "analysis-stempel",
          "analysis-phonetic",
          "watcher",
          "mapper-attachments",
          "delete-by-query"
        ],
        "default_plugins": [
          "found-elasticsearch",
          "cloud-aws",
          "found-license-plugin",
          "shield",
          "marvel-agent"
        ...
        ]
      }
    },
    {
      "version": "5.2.2",
      "template": {
        "template_version": "",
        "hashes": []
      },
      "elasticsearch": {
        "docker_image": "docker.elastic.co/cloud-enterprise/elasticsearch:5.2.2-0",
        "plugins": [
          "analysis-icu",
          "analysis-kuromoji",
          "analysis-smartcn",
          "analysis-stempel",
          "analysis-phonetic",
          "mapper-attachments",
          "ingest-attachment",
          "ingest-geoip",
          "ingest-user-agent"
        ],
        "default_plugins": [
          "repository-s3",
          "found-elasticsearch",
          "x-pack"
        ...
        ]
      }
    }
  ]
}
```
You can also query for a specific version with a URI such as `https://COORDINATOR_HOST:12443/api/v1/stack/versions/5.3.2`, for example.


## Add Elastic Stack packs [ece-manage-elastic-stack-add]

You can add new Elastic Stack packs to your installation through the Cloud UI, through the Elastic Cloud Enterprise installation script, or through the RESTful API.

To add a new Elastic Stack pack from the Cloud UI:

1. Download the [Elastic Stack version]() that you want.
2. [Log into the Cloud UI](log-into-cloud-ui.md).
3. From the **Platform** menu, select **Elastic Stack**.
4. Select **Upload Elastic Stack pack**.
5. Select a .zip file that contains an Elastic Stack pack and upload it.

    After the stack pack has been uploaded successfully, the new version appears in the list of Elastic Stack versions and can be used when you create or change a deployment.


To add a new Elastic Stack pack through the Elastic Cloud Enterprise installation script from the command line:

1. Log into a host running Elastic Cloud Enterprise.
2. Add the Elastic Stack pack with the `add-stack-version` action:

    ```sh
    ./elastic-cloud-enterprise.sh add-stack-version \
        --user USER --pass PASSWORD \
        --version X.Y.Z <1>
    ```

    1. A supported Elastic Stack version, such as `8.12.2`


    For example:

    ```sh
    bash elastic-cloud-enterprise.sh add-stack-version \
        --user admin --pass pGX5DwKzVAAIeCIpTwwAkCuJDu0ASdFP33UmYpfogfF \
        --version 8.12.2
    ```


To add a new Elastic Stack pack through the RESTful API from the command line:

1. Download the pack on an internet-connected host from Elastic and make it available locally.
2. Add the Elastic Stack pack with the following API call:

    ```sh
    curl -X POST -u USER:PASSWORD https://COORDINATOR_HOST:12443/api/v1/stack/versions \
        -H 'content-type: application/zip' \
        --data-binary "@PATH/STACK_PACK_FILE" <1>
    ```

    1. The local path and the new Elastic Stack pack .zip file


    For example:

    ```sh
    curl -X POST -u admin:pGX5DwKzVAAIeCIpTwwAkCuJDu0ASdFP33UmYpfogfF https://10.56.12.153:12443/api/v1/stack/versions \
        -H 'content-type: application/zip' \
        --data-binary "@/Users/iuriitceretian/Documents/stacks/5.4.0.zip"
    ```



## Update Elastic Stack packs [ece_update_elastic_stack_packs]

Updating an Elastic Stack pack might become necessary if an Elastic Stack version has been updated with security fixes, for example. You can update an existing Elastic Stack version through the Cloud UI or through the command line.

Updated versions of Elasticsearch and Kibana are used when you create new Elasticsearch clusters, but they are not automatically applied to already running clusters. To update existing Elasticsearch clusters and Kibana after an updated Elastic Stack pack has been added, you need to [change the deployment configuration](working-with-deployments.md).

To update Elastic Stack packs through the Cloud UI:

1. Download the [Elastic Stack version](#ece-elastic-stack-stackpacks) that you want.
2. [Log into the Cloud UI](log-into-cloud-ui.md).
3. From the **Platform** menu, select **Elastic Stack**.
4. Delete the old pack you want to replace.
5. Select **Upload Elastic Stack pack**.
6. Select a ZIP file that contains an Elastic Stack pack and upload it.

    After the stack pack has been uploaded successfully, the updated Elastic Stack version replaces the existing one.


To update Elastic Stack packs through the RESTful API from the command line:

1. Download an updated pack on an internet-connected host from Elastic and make it available locally.
2. Update the Elastic Stack pack with the following API call:

    ```sh
    curl -X PUT -u USER:PASSWORD https://COORDINATOR_HOST:12443/api/v1/stack/versions/VERSION \ <1>
        -H 'content-type: application/zip' \
        --data-binary "@PATH/STACK_PACK_FILE" <2>
    ```

    1. The version being updated
    2. The local path and the updated Elastic Stack pack .zip file


    For example:

    ```sh
    curl -X PUT -u admin:pGX5DwKzVAAIeCIpTwAAkCuJDu0ASdFP33UmYpfogfF https://10.58.12.153:12443/api/v1/stack/versions/6.4.0 \
        -H 'content-type: application/zip' \
        --data-binary "@/Users/johnsmith/Documents/stacks/6.4.0.zip"
    ```
