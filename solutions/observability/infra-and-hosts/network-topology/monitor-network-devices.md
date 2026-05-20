---
applies_to:
  stack: preview 9.0+
  serverless: unavailable
  deployment:
    self: preview
products:
  - id: observability
---

# Tutorial: Monitor your network devices with the Network Topology plugin [network-topology-get-started]

In this tutorial, you'll install the [Network Topology plugin](/solutions/observability/infra-and-hosts/network-topology.md) in self-managed {{kib}}, configure {{ls}} to collect SNMP data from your network devices, and explore site, device, and routing protocol state in {{kib}}.

This tutorial is for network engineers and IT operations teams who are familiar with SNMP and want to monitor their network devices with {{observability}}.

## What you'll learn [network-topology-what-youll-learn]

You'll learn how to:

1. Install and configure the Network Topology plugin in self-managed {{kib}}.
2. Configure SNMP data collection using {{ls}}.
3. Verify data is flowing into {{es}}.
4. Explore network topology, device health, and routing protocol state in {{kib}}.

## Before you begin [network-topology-before-you-begin]

You need:

* Self-managed {{kib}} and {{es}}. The Network Topology plugin is _not_ compatible with {{ech}} or {{serverless-full}}.
* Installation requires system or root level access on the node running {{kib}}.
* One or more network devices with SNMP v1, v2c, or v3 enabled.
* {{ls}} installed and able to reach your network devices.

:::{tip}
If you don't have SNMP-enabled devices to point at yet, you can evaluate the plugin against simulated data using the sample data generator and Docker Compose dev environment included in the [Network Topology plugin repository](https://github.com/elastic/kibana-network-topology-plugin).
:::

## Step 1: Install the plugin [network-topology-install-plugin]

1. Download the latest Network Topology plugin release `.zip` from [the plugin releases page on GitHub](https://github.com/elastic/kibana-network-topology-plugin/releases).
2. Unzip the plugin bundle.
3. Open the `kibana/networkTopology/kibana.json` manifest file included in the bundle.
4. Locate the `kibanaVersion` property and replace the placeholder value with your exact {{kib}} version. Save the file.
5. Re-zip the plugin bundle, preserving the `kibana/networkTopology` folder hierarchy. If the folder structure changes, installation will fail.
6. From the root of your {{kib}} install directory, run:

    ```shell
    bin/kibana-plugin install file:///absolute/path/to/networkTopology.zip
    ```

7. Restart {{kib}}.

### Troubleshooting: Plugin installs but doesn't load [network-topology-install-troubleshooting]

If `kibana-plugin install` reports success but the Network Topology plugin doesn't appear in {{kib}}, check the file permissions on the {{kib}} `plugins/` directory. The plugin files must be readable by the user that {{kib}} runs as. Correct the ownership or mode of the plugin directory and restart {{kib}}.

## Step 2: Apply the index templates and ingest pipeline [network-topology-apply-templates]

The plugin's **Setup** tab walks you through installing the `snmp-device-enrichment` ingest pipeline and the `logs-snmp.topology@template` index template. Install these before you start sending data so that the first documents are enriched and mapped correctly.

1. In {{kib}}, navigate to **Observability** → **Network Topology** and select the **Setup** tab.
2. Under **Step 1 — Install Index Template & Ingest Pipeline**, select **Open in DevTools** next to the ingest pipeline, then click the run button (**▶**) to apply it.

    ::::{note}
    Install the pipeline first because the index template references it as the default ingest pipeline.
    ::::

3. Repeat for the index template.

## Step 3: Configure SNMP data collection using {{ls}} [network-topology-configure-logstash]

The Network Topology plugin reads from an {{es}} data stream that {{ls}} populates using the SNMP input plugin.

1. Create a {{ls}} pipeline using the `logstash.conf` reference provided in the [Network Topology plugin repository](https://github.com/elastic/kibana-network-topology-plugin/blob/main/docs/collectors/logstash.conf). Edit the SNMP input to list your devices, credentials, and polling interval, and edit the {{es}} output to point at your cluster.

    ::::{note}
    For details on the fields you'll configure in this pipeline, refer to [Location and role metadata fields](/solutions/observability/infra-and-hosts/network-topology/field-reference.md#network-topology-fields-network).
    ::::

2. Start {{ls}} with your pipeline configuration. If you use [{{ls}} centralized pipeline management](logstash://reference/logstash-centralized-pipeline-management.md), you can push the pipeline directly from {{kib}} instead — no SSH access to a {{ls}} host required.

### Troubleshooting: Common SNMP input errors [network-topology-logstash-troubleshooting]

Problems with an SNMP get, walk, or table operation cause the following error in the {{ls}} log:

```text
error invoking 'walk' operation: error sending snmp walk request to target <ip>:<port>: Request timed out., ignoring. {host=<ip>:<port>, oids=[<oid array>]}
```

Check the following:

* **Wrong community string or v3 credentials** — verify the community string (v1/v2c) or username and password (v3) in your {{ls}} pipeline config are correct.
* **Incorrect target IP or port** — confirm the device IP and SNMP port are correct.
* **Device is unreachable or down** — confirm the device is up and available.

## Step 4: Verify data in {{kib}} [network-topology-verify-data]

1. In {{kib}}, navigate to **Observability** → **Network Topology**. You can also use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Confirm the page shows your configured sites and the network segments that have been discovered.

## Step 5: Explore the Network Topology plugin [network-topology-explore]

The plugin gives you the following views into your network: a site-level health summary, an interactive topology map, a per-device detail flyout, and a searchable device inventory.

### Site overview [network-topology-site-overview]

The site overview shows a grid of health cards, one per site. Each card summarizes the state of the devices in that site.

:::{image} /solutions/images/observability-network-topology-site-overview.png
:alt: Network Topology site overview showing health cards for HQ-DC1, Branch-NYC, and Branch-CHI
:screenshot:
:::

### Topology map [network-topology-topology-view]

The topology map builds an adjacency graph from the ARP, MAC forwarding table, BGP, and OSPF data the plugin has collected, and renders it as a force-directed layout. Zoom, pan, and drag nodes to lay out the view, and toggle the L2, L3, BGP, and OSPF layers to focus on a specific protocol. Link colors and styles indicate state.

:::{image} /solutions/images/observability-network-topology-topology-map.png
:alt: Network Topology map view showing a force-directed graph of devices and links for the HQ-DC1 site
:screenshot:
:::

### Device detail [network-topology-device-detail]

Click a node in the topology map to open the device flyout. The flyout shows the interface table, ARP neighbors, BGP peers, and OSPF adjacencies for the selected device.

:::{image} /solutions/images/observability-network-topology-device-flyout.png
:alt: Device flyout for hq-fw-01 showing interface table with status, speed, and traffic counters
:screenshot:
:::

### Device inventory [network-topology-device-inventory]

The device inventory is a searchable, paginated list of every device the plugin has discovered. Filter the list using KQL to answer operational questions, for example:

* Find every BGP session that isn't established.
* Find Cisco switches that have interfaces that are administratively up but operationally down.

:::{image} /solutions/images/observability-network-topology-device-inventory.png
:alt: Network Topology Devices tab showing a paginated list of devices with status, hostname, IP, type, vendor, site, and interface counts
:screenshot:
:::

## Related links [network-topology-related]

* [Network Topology overview](/solutions/observability/infra-and-hosts/network-topology.md)
* [Network Topology field reference](/solutions/observability/infra-and-hosts/network-topology/field-reference.md)
* [Network Topology plugin on GitHub](https://github.com/elastic/kibana-network-topology-plugin)
