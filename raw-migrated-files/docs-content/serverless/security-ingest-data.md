---
navigation_title: "Ingest data"
---

# Ingest data to Elastic Security [security-ingest-data]


To ingest data, you can use:

* The [{{agent}}](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html) with the **{{elastic-defend}}** integration, which protects your hosts and sends logs, metrics, and endpoint security data to {{elastic-sec}}. See [Install Elastic Defend](../../../solutions/security/configure-elastic-defend/install-elastic-defend.md).
* The {{agent}} with other integrations, which are available in the [Elastic Package Registry (EPR)](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html#package-registry-intro). To install an integration that works with {{elastic-sec}}, select **Add integrations** in the toolbar on most pages. On the **Integrations** page, select the **Security** category filter, then select an integration to view the installation instructions. For more information on integrations, refer to [{{integrations}}](https://docs.elastic.co/en/integrations).
* **{{beats}}** shippers installed for each system you want to monitor.
* The {{agent}} to send data from Splunk to {{elastic-sec}}. See [Get started with data from Splunk](../../../solutions/observability/get-started/add-data-from-splunk.md).
* Third-party collectors configured to ship ECS-compliant data. [{{elastic-sec}} ECS field reference](https://www.elastic.co/guide/en/serverless/current/security-siem-field-reference.html) provides a list of ECS fields used in {{elastic-sec}}.

::::{important}
If you use a third-party collector to ship data to {{elastic-sec}}, you must map its fields to the [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current). Additionally, you must add its index to the {{elastic-sec}} indices (update the **`securitySolution:defaultIndex`** [advanced setting](../../../solutions/security/get-started/configure-advanced-settings.md#update-sec-indices)).

{{elastic-sec}} uses the [`host.name`](https://www.elastic.co/guide/en/ecs/current/ecs-host.html) ECS field as the primary key for identifying hosts.

::::


The {{agent}} with the [{{elastic-defend}} integration](https://www.elastic.co/products/endpoint-security) ships these data sources:

* Process - Linux, macOS, Windows
* Network - Linux, macOS, Windows
* File - Linux, macOS, Windows
* DNS - Windows
* Registry - Windows
* DLL and Driver Load - Windows
* Security - Windows


## Install {{beats}} shippers [install-beats]

To add hosts and populate {{elastic-sec}} with network security events, you need to install and configure Beats on the hosts from which you want to ingest security events:

* [{{filebeat}}](https://www.elastic.co/products/beats/filebeat) for forwarding and centralizing logs and files
* [{{auditbeat}}](https://www.elastic.co/products/beats/auditbeat) for collecting security events
* [{{winlogbeat}}](https://www.elastic.co/products/beats/winlogbeat) for centralizing Windows event logs
* [{{packetbeat}}](https://www.elastic.co/products/beats/packetbeat) for analyzing network activity

You can install {{beats}} using the UI guide or directly from the command line.


### Install {{beats}} using the UI guide [security-ingest-data-install-beats-using-the-ui-guide]

When you add integrations that use {{beats}}, you’re guided through the {{beats}} installation process. To begin, go to the **Integrations** page (select **Add integrations** in the toolbar on most pages), and then follow the links for the types of data you want to collect.

::::{tip}
On the Integrations page, you can select the **Beats only** filter to only view integrations using Beats.

::::



### Download and install {{beats}} from the command line [security-ingest-data-download-and-install-beats-from-the-command-line]

To install {{beats}}, see these installation guides:

* [{{filebeat}} quick start](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation-configuration.html)
* [{{auditbeat}} quick start](https://www.elastic.co/guide/en/beats/auditbeat/current/auditbeat-installation-configuration.html)
* [{{winlogbeat}} quick start](https://www.elastic.co/guide/en/beats/winlogbeat/current/winlogbeat-installation-configuration.html)
* [{{packetbeat}} quick start](https://www.elastic.co/guide/en/beats/packetbeat/current/packetbeat-installation-configuration.html)


### Enable modules and configuration options [enable-beat-modules]

No matter how you installed {{beats}}, you need to enable modules in {{auditbeat}} and {{filebeat}} to populate {{elastic-sec}} with data.

::::{tip}
For a full list of security-related beat modules, [click here](https://www.elastic.co/integrations?solution=security).

::::


To populate **Hosts** data, enable these modules:

* [Auditbeat system module  - Linux, macOS, Windows](https://www.elastic.co/guide/en/beats/auditbeat/current/auditbeat-module-system.html):

    * packages
    * processes
    * logins
    * sockets
    * users and groups

* [Auditbeat auditd module - Linux kernel audit events](https://www.elastic.co/guide/en/beats/auditbeat/current/auditbeat-module-auditd.html)
* [Auditbeat file integrity module - Linux, macOS, Windows](https://www.elastic.co/guide/en/beats/auditbeat/current/auditbeat-module-file_integrity.html)
* [Filebeat system module - Linux system logs](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-system.html)
* [Filebeat Santa module  - macOS security events](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-santa.html)
* [Winlogbeat - Windows event logs](https://www.elastic.co/guide/en/beats/winlogbeat/current/_winlogbeat_overview.html)

To populate **Network** data, enable Packetbeat protocols and Filebeat modules:

* [{{packetbeat}}](https://www.elastic.co/guide/en/beats/packetbeat/current/packetbeat-overview.html)

    * [DNS](https://www.elastic.co/guide/en/beats/packetbeat/current/packetbeat-dns-options.html)
    * [TLS](https://www.elastic.co/guide/en/beats/packetbeat/current/configuration-tls.html)
    * [Other supported protocols](https://www.elastic.co/guide/en/beats/packetbeat/current/configuration-protocols.html)

* [{{filebeat}}](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-overview.html)

    * [Zeek NMS module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-zeek.html)
    * [Suricata IDS module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-suricata.html)
    * [Iptables/Ubiquiti module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-iptables.html)
    * [CoreDNS module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-coredns.html)
    * [Envoy proxy module (Kubernetes)](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-envoyproxy.html)
    * [Palo Alto Networks firewall module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-panw.html)
    * [Cisco ASA firewall module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-cisco.html)
    * [AWS module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-aws.html)
    * [CEF module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-cef.html)
    * [Google Cloud module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-googlecloud.html)
    * [NetFlow module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-netflow.html)
