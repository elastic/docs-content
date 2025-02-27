---
navigation_title: "Ingest data"
---

# Ingest data to Elastic Security [security-ingest-data]


To ingest data, you can use:

* The [{{agent}}](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/index.md) with the **{{elastic-defend}}** integration, which protects your hosts and sends logs, metrics, and endpoint security data to {{elastic-sec}}. See [Install Elastic Defend](../../../solutions/security/configure-elastic-defend/install-elastic-defend.md).
* The {{agent}} with other integrations, which are available in the [Elastic Package Registry (EPR)](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/index.md#package-registry-intro). To install an integration that works with {{elastic-sec}}, select **Add integrations** in the toolbar on most pages. On the **Integrations** page, select the **Security** category filter, then select an integration to view the installation instructions. For more information on integrations, refer to [{{integrations}}](https://docs.elastic.co/en/integrations).
* **{{beats}}** shippers installed for each system you want to monitor.
* The {{agent}} to send data from Splunk to {{elastic-sec}}. See [Get started with data from Splunk](../../../solutions/observability/get-started/add-data-from-splunk.md).
* Third-party collectors configured to ship ECS-compliant data. [{{elastic-sec}} ECS field reference](asciidocalypse://docs/docs-content/docs/reference/security/fields-and-object-schemas/siem-field-reference.md) provides a list of ECS fields used in {{elastic-sec}}.

::::{important}
If you use a third-party collector to ship data to {{elastic-sec}}, you must map its fields to the [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current). Additionally, you must add its index to the {{elastic-sec}} indices (update the **`securitySolution:defaultIndex`** [advanced setting](../../../solutions/security/get-started/configure-advanced-settings.md#update-sec-indices)).

{{elastic-sec}} uses the [`host.name`](asciidocalypse://docs/ecs/docs/reference/ecs-host.md) ECS field as the primary key for identifying hosts.

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

* [{{filebeat}} quick start](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-installation-configuration.md)
* [{{auditbeat}} quick start](asciidocalypse://docs/beats/docs/reference/auditbeat/auditbeat-installation-configuration.md)
* [{{winlogbeat}} quick start](asciidocalypse://docs/beats/docs/reference/winlogbeat/winlogbeat-installation-configuration.md)
* [{{packetbeat}} quick start](asciidocalypse://docs/beats/docs/reference/packetbeat/packetbeat-installation-configuration.md)


### Enable modules and configuration options [enable-beat-modules]

No matter how you installed {{beats}}, you need to enable modules in {{auditbeat}} and {{filebeat}} to populate {{elastic-sec}} with data.

::::{tip}
For a full list of security-related beat modules, [click here](https://www.elastic.co/integrations?solution=security).

::::


To populate **Hosts** data, enable these modules:

* [Auditbeat system module  - Linux, macOS, Windows](asciidocalypse://docs/beats/docs/reference/auditbeat/auditbeat-module-system.md):

    * packages
    * processes
    * logins
    * sockets
    * users and groups

* [Auditbeat auditd module - Linux kernel audit events](asciidocalypse://docs/beats/docs/reference/auditbeat/auditbeat-module-auditd.md)
* [Auditbeat file integrity module - Linux, macOS, Windows](asciidocalypse://docs/beats/docs/reference/auditbeat/auditbeat-module-file_integrity.md)
* [Filebeat system module - Linux system logs](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-system.md)
* [Filebeat Santa module  - macOS security events](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-santa.md)
* [Winlogbeat - Windows event logs](asciidocalypse://docs/beats/docs/reference/winlogbeat/_winlogbeat_overview.md)

To populate **Network** data, enable Packetbeat protocols and Filebeat modules:

* [{{packetbeat}}](asciidocalypse://docs/beats/docs/reference/packetbeat/packetbeat-overview.md)

    * [DNS](asciidocalypse://docs/beats/docs/reference/packetbeat/packetbeat-dns-options.md)
    * [TLS](asciidocalypse://docs/beats/docs/reference/packetbeat/configuration-tls.md)
    * [Other supported protocols](asciidocalypse://docs/beats/docs/reference/packetbeat/configuration-protocols.md)

* [{{filebeat}}](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-overview.md)

    * [Zeek NMS module](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-zeek.md)
    * [Suricata IDS module](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-suricata.md)
    * [Iptables/Ubiquiti module](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-iptables.md)
    * [CoreDNS module](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-coredns.md)
    * [Envoy proxy module (Kubernetes)](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-envoyproxy.md)
    * [Palo Alto Networks firewall module](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-panw.md)
    * [Cisco ASA firewall module](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-cisco.md)
    * [AWS module](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-aws.md)
    * [CEF module](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-cef.md)
    * [Google Cloud module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-googlecloud.html)
    * [NetFlow module](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-netflow.md)
