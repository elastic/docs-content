---
navigation_title: Network Topology
applies_to:
  stack: preview 9.0+
  serverless: unavailable
  deployment:
    self: preview
products:
  - id: observability
---

# Network Topology [network-topology]

::::{note}
The Network Topology plugin is only supported on self-managed {{kib}}. It is _not_ compatible with {{ech}} or {{serverless-full}}.
::::

The Network Topology plugin lets you monitor SNMP-enabled network devices from a single view in {{kib}}. On this page, you'll find information on [use cases](#network-topology-use-cases), [features](#network-topology-features), and [how the plugin works](#network-topology-how-it-works).

## Use cases [network-topology-use-cases]

Use the Network Topology plugin to:

* Monitor SNMP-enabled network devices, such as routers and switches, from a single view.
* Visualize L2 and L3 topology and routing protocol state (BGP, OSPF) without a dedicated NMS.
* Identify interface issues and routing adjacency changes across sites.

## Features [network-topology-features]

The Network Topology plugin includes:

* **A reference {{ls}} pipeline** that walks the IF-MIB (interface counters and status), IP-MIB (ARP tables and IP address assignments), BRIDGE-MIB (MAC address forwarding tables), BGP4-MIB (BGP peer sessions), and OSPF-MIB (OSPF neighbor adjacencies) on each target device at a configurable poll interval. The pipeline handles poll timeouts, missing OID branches on devices that don't support a given MIB, and batching across large device inventories.
* **A `snmp-device-enrichment` ingest pipeline** that parses each device's `sysDescr` string to assign a normalized `host.type` (router, switch, firewall, access point, server) and `observer.vendor`. The pipeline recognizes common vendors out of the box (Cisco, Juniper, Arista, Fortinet, Palo Alto, HPE, Aruba) and is extensible for less common hardware.
* **An interactive topology graph** in {{kib}}'s Observability navigation that builds an adjacency graph from ARP, MAC table, BGP, and OSPF relationships and renders it as a force-directed layout you can zoom, pan, and rearrange. Clicking a device opens a flyout with its interface table, ARP neighbors, BGP peers, and OSPF adjacencies.
* **A sample data generator** and Docker Compose dev environment, so you can evaluate the plugin with a realistic multi-site network before connecting to live infrastructure.

## How it works [network-topology-how-it-works]

The Network Topology plugin renders data that {{ls}} collects from your network devices over SNMP and indexes into {{es}}:

1. {{ls}} polls SNMP-enabled devices on your network.
2. {{ls}} writes the collected data into an {{es}} data stream.
3. The `snmp-device-enrichment` ingest pipeline classifies each document by device type and vendor.
4. The Network Topology plugin reads from the data stream and displays sites, devices, and topology in {{kib}}.

## Next steps [network-topology-next-steps]

* [Tutorial: Monitor your network devices with the Network Topology plugin](/solutions/observability/infra-and-hosts/network-topology/monitor-network-devices.md)
* [Network Topology field reference](/solutions/observability/infra-and-hosts/network-topology/field-reference.md)
* [Network Topology plugin on GitHub](https://github.com/elastic/kibana-network-topology-plugin)
