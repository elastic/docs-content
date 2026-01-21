---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/ingest-data.html
  - https://www.elastic.co/guide/en/serverless/current/security-ingest-data.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Ingest data to {{elastic-sec}} [security-ingest-data]

To ingest data, you can use:

* The [{{agent}}](/reference/fleet/index.md) with the **{{elastic-defend}}** integration, which protects your hosts and sends logs, metrics, and endpoint security data to {{elastic-sec}}. See [Install {{elastic-defend}}](/solutions/security/configure-elastic-defend/install-elastic-defend.md).
* The {{agent}} with integrations, which are available in the [Elastic Package Registry (EPR)](/reference/fleet/index.md#package-registry-intro). To install an integration that works with {{elastic-sec}}, go to the {{kib}} Home page or navigation menu and click **Add integrations**. On the Integrations page, click the **Security** category filter, then select an integration to view the installation instructions. For more information on integrations, refer to [{{integrations}}](https://docs.elastic.co/en/integrations).
* **{{beats}}** shippers installed for each system you want to monitor.
* **{{ls}}**, which dynamically ingests, transforms, and ships your data regardless of format.
* Third-party collectors configured to ship ECS-compliant data. [](/reference/security/fields-and-object-schemas/siem-field-reference.md) provides a list of ECS fields used in {{elastic-sec}}.

::::{important}
If you use a third-party collector—or some {{ls}} plugins without {{agent}} or {{beats}}—to ship data to {{elastic-sec}}, you must map its fields to the [Elastic Common Schema (ECS)](ecs://reference/index.md). Additionally, you must add its index to the {{elastic-sec}} indices (update the `securitySolution:defaultIndex` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices)).

{{elastic-sec}} uses the [`host.name`](ecs://reference/ecs-host.md) ECS field as the primary key for identifying hosts.

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


:::{image} /solutions/images/security-add-integrations.png
:alt: Shows button to add integrations
:screenshot:
:::


### Download and install {{beats}} from the command line [security-ingest-data-download-and-install-beats-from-the-command-line]

To install {{beats}}, see these installation guides:

* [{{filebeat}} quick start](beats://reference/filebeat/filebeat-installation-configuration.md)
* [{{auditbeat}} quick start](beats://reference/auditbeat/auditbeat-installation-configuration.md)
* [{{winlogbeat}} quick start](beats://reference/winlogbeat/winlogbeat-installation-configuration.md)
* [{{packetbeat}} quick start](beats://reference/packetbeat/packetbeat-installation-configuration.md)


### Enable modules and configuration options [enable-beat-modules]

No matter how you installed {{beats}}, you need to enable modules in {{auditbeat}} and {{filebeat}} to populate {{elastic-sec}} with data.

::::{tip}
For a full list of security-related beat modules, [click here](https://www.elastic.co/integrations?solution=security).
::::


To populate **Hosts** data, enable these modules:

* [Auditbeat system module  - Linux, macOS, Windows](beats://reference/auditbeat/auditbeat-module-system.md):

    * packages
    * processes
    * logins
    * sockets
    * users and groups

* [Auditbeat auditd module - Linux kernel audit events](beats://reference/auditbeat/auditbeat-module-auditd.md)
* [Auditbeat file integrity module - Linux, macOS, Windows](beats://reference/auditbeat/auditbeat-module-file_integrity.md)
* [Filebeat system module - Linux system logs](beats://reference/filebeat/filebeat-module-system.md)
* [Filebeat Santa module  - macOS security events](beats://reference/filebeat/filebeat-module-santa.md)
* [Winlogbeat - Windows event logs](beats://reference/winlogbeat/index.md)

To populate **Network** data, enable Packetbeat protocols and Filebeat modules:

* [{{packetbeat}}](beats://reference/packetbeat/index.md)

    * [DNS](beats://reference/packetbeat/packetbeat-dns-options.md)
    * [TLS](beats://reference/packetbeat/configuration-tls.md)
    * [Other supported protocols](beats://reference/packetbeat/configuration-protocols.md)

* [{{filebeat}}](beats://reference/filebeat/index.md)

    * [Zeek NMS module](beats://reference/filebeat/filebeat-module-zeek.md)
    * [Suricata IDS module](beats://reference/filebeat/filebeat-module-suricata.md)
    * [Iptables/Ubiquiti module](beats://reference/filebeat/filebeat-module-iptables.md)
    * [CoreDNS module](beats://reference/filebeat/filebeat-module-coredns.md)
    * [Envoy proxy module (Kubernetes)](beats://reference/filebeat/filebeat-module-envoyproxy.md)
    * [Palo Alto Networks firewall module](beats://reference/filebeat/filebeat-module-panw.md)
    * [Cisco ASA firewall module](beats://reference/filebeat/filebeat-module-cisco.md)
    * [AWS module](beats://reference/filebeat/filebeat-module-aws.md)
    * [CEF module](beats://reference/filebeat/filebeat-module-cef.md)
    * [Google Cloud module](beats://reference/filebeat/filebeat-module-gcp.md)
    * [NetFlow module](beats://reference/filebeat/filebeat-module-netflow.md)
