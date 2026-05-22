---
applies_to:
  stack: preview 9.0+
  serverless: unavailable
  deployment:
    self: preview
products:
  - id: observability
---

# Network Topology field reference [network-topology-fields]

This page describes every {{es}} field the [Network Topology plugin](/solutions/observability/infra-and-hosts/network-topology.md) reads or writes, its ECS compliance status, mapping type, and expected values.

## ECS status key [network-topology-fields-ecs-status]

| Badge | Meaning |
| --- | --- |
| **Core ECS** | Defined in the [{{product.ecs}}](ecs://reference/index.md) and used as specified. |
| **ECS ext.** | Uses an ECS-defined namespace but with values that extend beyond the official spec. |
| **Custom** | No ECS equivalent — SNMP-specific data for which ECS does not define field sets. |

## Base fields [network-topology-fields-base]

| Field | Type | ECS status | Description | Examples |
| --- | --- | --- | --- | --- |
| `@timestamp` | date | Core ECS | Document timestamp — when the SNMP poll was collected. | `2024-01-01T12:00:00.000Z` |

## `host.*` — Device identity [network-topology-fields-host]

ECS `host` fields identify the monitored network device.

| Field | Type | ECS status | Description | Examples |
| --- | --- | --- | --- | --- |
| `host.name` | keyword | Core ECS | Device hostname (SNMP `sysName`). | `hq-core-rtr-01` |
| `host.ip` | ip | Core ECS | Primary management IP address. | `10.1.1.2` |
| `host.mac` | keyword | Core ECS | Primary MAC address. | `aa:bb:cc:dd:ee:01` |
| `host.type` | keyword | ECS ext. | Device category — set explicitly in the {{ls}} collector config. The ingest pipeline infers it from `observer.sys_descr` as a fallback when unset. | `router`, `switch`, `firewall`, `server`, `ap`, `unknown` |

## `observer.*` — Device classification [network-topology-fields-observer]

ECS `observer` fields describe the network device as the observed system.

| Field | Type | ECS status | Description | Examples |
| --- | --- | --- | --- | --- |
| `observer.vendor` | keyword | Core ECS | Vendor name — auto-detected from `observer.sys_descr` by the ingest pipeline. | `Cisco`, `Juniper`, `Palo Alto`, `Arista`, `Fortinet`, `HPE`, `Aruba` |
| `observer.sys_descr` | text | Core ECS | Raw SNMP `sysDescr` string — the ingest pipeline uses this to populate `observer.vendor` and `host.type`. | `Cisco IOS XR Software, ASR 9000 Series Router` |
| `observer.os.full` | keyword | Core ECS | Full OS version string. | `IOS-XR 7.3.2`, `Junos 22.1R1` |

## `network.*` — Location and role metadata [network-topology-fields-network]

These fields provide hierarchical location context for the device. The ECS `network` field set covers protocol and transport data; the site, building, and role fields below extend that namespace.

| Field | Type | ECS status | Description | Examples |
| --- | --- | --- | --- | --- |
| `network.site` | keyword | ECS ext. | Site or datacenter identifier. Defaults to `Ungrouped` if absent (set by the ingest pipeline). | `HQ-DC1`, `Branch-NYC`, `Branch-CHI` |
| `network.building` | keyword | ECS ext. | Building within the site. | `Main`, `Annex`, `Tower-B` |
| `network.role` | keyword | ECS ext. | Network tier — used for topology hierarchy. Controls the vertical position of nodes in the topology map. | `core`, `distribution`, `access`, `server` |

## `interface.*` — SNMP interface metrics [network-topology-fields-interface]

No ECS field set covers SNMP interface MIB (IF-MIB, RFC 2863) data. These fields are plugin-defined under the `interface.*` namespace.

| Field | Type | ECS status | SNMP MIB OID | Description | Examples |
| --- | --- | --- | --- | --- | --- |
| `interface.name` | keyword | Custom | `ifDescr` (1.3.6.1.2.1.2.2.1.2) | Interface name. | `Gi0/0/0`, `eth0`, `xe-0/0/0` |
| `interface.speed` | long | Custom | `ifSpeed` (1.3.6.1.2.1.2.2.1.5) | Interface speed in bits/sec. | `10000000000` (10 Gbps) |
| `interface.status.admin` | keyword | Custom | `ifAdminStatus` (1.3.6.1.2.1.2.2.1.7) | Administrative status. | `up`, `down` |
| `interface.status.oper` | keyword | Custom | `ifOperStatus` (1.3.6.1.2.1.2.2.1.8) | Operational status. | `up`, `down`, `testing` |
| `interface.traffic.in.bytes` | long | Custom | `ifInOctets` (1.3.6.1.2.1.2.2.1.10) | Cumulative inbound bytes. | `125000000` |
| `interface.traffic.out.bytes` | long | Custom | `ifOutOctets` (1.3.6.1.2.1.2.2.1.16) | Cumulative outbound bytes. | `87500000` |
| `interface.errors.in` | long | Custom | `ifInErrors` (1.3.6.1.2.1.2.2.1.14) | Inbound error count. | `0` |
| `interface.errors.out` | long | Custom | `ifOutErrors` (1.3.6.1.2.1.2.2.1.20) | Outbound error count. | `0` |

::::{note}
These are cumulative counters, not rates. To compute bits/sec, take the delta between two consecutive polls in your collector or use a {{kib}} scripted field.
::::

## `arp.*` — ARP table entries [network-topology-fields-arp]

Populated from the IP-MIB `ipNetToMediaTable` (RFC 1213, OID `1.3.6.1.2.1.4.22`). Used to infer Layer 3 adjacency in the topology map.

| Field | Type | ECS status | SNMP MIB OID | Description | Examples |
| --- | --- | --- | --- | --- | --- |
| `arp.ip_addr` | ip | Custom | `ipNetToMediaNetAddress` (.4) | ARP neighbor IP address. | `10.1.1.3` |
| `arp.mac_addr` | keyword | Custom | `ipNetToMediaPhysAddress` (.2) | ARP neighbor MAC address. | `aa:bb:cc:dd:ee:02` |
| `arp.interface_index` | integer | Custom | `ipNetToMediaIfIndex` (.1) | Interface on which the ARP entry was learned. | `1` |

## `mac_table.*` — MAC forwarding table entries [network-topology-fields-mac-table]

Populated from the BRIDGE-MIB `dot1dTpFdbTable` (RFC 1493, OID `1.3.6.1.2.1.17.4.3`). Used to infer Layer 2 adjacency between switches in the topology map.

| Field | Type | ECS status | SNMP MIB OID | Description | Examples |
| --- | --- | --- | --- | --- | --- |
| `mac_table.mac_addr` | keyword | Custom | `dot1dTpFdbAddress` (.1) | MAC address in forwarding table. | `aa:bb:cc:dd:ee:05` |
| `mac_table.port_index` | integer | Custom | `dot1dTpFdbPort` (.2) | Bridge port on which this MAC was seen. | `2` |
| `mac_table.status` | keyword | Custom | `dot1dTpFdbStatus` (.3) | Entry type. | `learned`, `static`, `mgmt` |

## `ip_addr.*` — IP address table entries [network-topology-fields-ip-addr]

Populated from the IP-MIB `ipAddrTable` (RFC 1213, OID `1.3.6.1.2.1.4.20`). Used to determine which network segments (CIDRs) each device participates in.

| Field | Type | ECS status | SNMP MIB OID | Description | Examples |
| --- | --- | --- | --- | --- | --- |
| `ip_addr.address` | ip | Custom | `ipAdEntAddr` (.1) | Interface IP address — used for CIDR-based segment lookups. | `192.168.10.1` |
| `ip_addr.netmask` | keyword | Custom | `ipAdEntNetMask` (.3) | Interface subnet mask. | `255.255.255.0` |
| `ip_addr.network` | keyword | Custom | _computed_ | CIDR block derived from address and netmask — used for segment grouping. | `192.168.10.0/24` |
| `ip_addr.prefix_length` | integer | Custom | _computed_ | Prefix length derived from netmask. | `24` |
| `ip_addr.if_index` | integer | Custom | `ipAdEntIfIndex` (.2) | Interface index linking this IP to an interface row. | `3` |

::::{note}
Loopback (`127.x`), link-local (`169.254.x`), multicast (`>=224`), and unspecified (`0.x`) addresses are filtered out at collection time.
::::

## `bgp_peer.*` — BGP peer sessions [network-topology-fields-bgp-peer]

Populated from the BGP4-MIB `bgpPeerTable` (RFC 4273, OID `1.3.6.1.2.1.15.3`). Used to display BGP peering sessions and create logical overlay links on the topology map.

| Field | Type | ECS status | SNMP MIB OID | Description | Examples |
| --- | --- | --- | --- | --- | --- |
| `bgp_peer.remote_ip` | ip | Custom | `bgpPeerRemoteAddr` (.7) | BGP peer remote IP address. | `198.51.100.1` |
| `bgp_peer.remote_asn` | long | Custom | `bgpPeerRemoteAs` (.9) | Remote autonomous system number. | `3356` |
| `bgp_peer.local_asn` | long | Custom | `bgpLocalAs` (1.3.6.1.2.1.15.2) | Local autonomous system number. | `65000` |
| `bgp_peer.peer_state` | keyword | Custom | `bgpPeerState` (.2) | BGP FSM state. | `Established`, `Idle`, `Active` |
| `bgp_peer.prefixes_received` | long | Custom | _vendor-specific_ | Prefixes received from this peer (not in standard BGP4-MIB). | `920000` |
| `bgp_peer.prefixes_sent` | long | Custom | _vendor-specific_ | Prefixes advertised to this peer. | `12` |
| `bgp_peer.uptime_seconds` | long | Custom | `bgpPeerFsmEstablishedTime` (.16) | Seconds since the session was established. | `2592000` |
| `bgp_peer.in_updates` | long | Custom | `bgpPeerInUpdates` (.10) | BGP UPDATE messages received. | `45000` |
| `bgp_peer.out_updates` | long | Custom | `bgpPeerOutUpdates` (.11) | BGP UPDATE messages sent. | `1200` |

::::{note}
Prefix counts (`prefixes_received`, `prefixes_sent`) are not part of the standard BGP4-MIB. They are available in vendor-specific MIBs (for example, Cisco `CISCO-BGP4-MIB`, Juniper `jnxBgpM2PrefixCounters`) or in BGP4-MIB-V2 (draft). The {{ls}} filter sets these to `0` when unavailable.
::::

## `ospf_neighbor.*` — OSPF neighbor adjacencies [network-topology-fields-ospf-neighbor]

Populated from the OSPF-MIB `ospfNbrTable` (RFC 4750, OID `1.3.6.1.2.1.14.10`). Used to display OSPF adjacency state and create interior routing links on the topology map.

| Field | Type | ECS status | SNMP MIB OID | Description | Examples |
| --- | --- | --- | --- | --- | --- |
| `ospf_neighbor.neighbor_ip` | ip | Custom | `ospfNbrIpAddr` (.1) | OSPF neighbor IP address. | `10.1.1.2` |
| `ospf_neighbor.router_id` | ip | Custom | `ospfNbrRtrId` (.3) | Neighbor's OSPF router ID. | `10.1.1.2` |
| `ospf_neighbor.state` | keyword | Custom | `ospfNbrState` (.6) | OSPF FSM adjacency state. | `Full`, `2-Way`, `Down` |
| `ospf_neighbor.area_id` | keyword | Custom | _from OID index_ | OSPF area identifier. | `0.0.0.0` (backbone) |
| `ospf_neighbor.priority` | integer | Custom | `ospfNbrPriority` (.5) | DR election priority. | `1` |
| `ospf_neighbor.dead_timer` | integer | Custom | _configured_ | Dead interval in seconds. | `40` |
| `ospf_neighbor.retrans_count` | integer | Custom | `ospfNbrEvents` (.7) | Number of state change events. | `3` |

::::{note}
OSPF state values: `1=Down`, `2=Attempt`, `3=Init`, `4=2-Way`, `5=ExStart`, `6=Exchange`, `7=Loading`, `8=Full`. `Full` means fully adjacent (exchanged LSDBs). `2-Way` is normal for DROther routers on broadcast segments.
::::

## Document types [network-topology-fields-document-types]

A single SNMP poll cycle produces six document types per device, all indexed into the `logs-snmp.topology-default` data stream:

| Document type | Distinguishing field | Purpose |
| --- | --- | --- |
| Interface metrics | `interface.name` present | Per-interface status, speed, traffic, errors. |
| ARP entry | `arp.mac_addr` present | Layer 3 neighbor discovery. |
| MAC table entry | `mac_table.mac_addr` present | Layer 2 forwarding topology. |
| IP address entry | `ip_addr.address` present | Interface IPs and subnet membership for segment views. |
| BGP peer session | `bgp_peer.remote_ip` present | BGP peering state, AS numbers, prefix counts, uptime. |
| OSPF neighbor | `ospf_neighbor.neighbor_ip` present | OSPF adjacency state, router ID, area, priority. |

All six share the same `host.*`, `observer.*`, and `network.*` fields to identify which device the data belongs to.

## Ingest pipeline: `snmp-device-enrichment` [network-topology-fields-ingest-pipeline]

The ingest pipeline performs the following on every incoming document:

1. **Device type default** — sets `host.type = "unknown"` if the field is absent.
2. **Site default** — sets `network.site = "Ungrouped"` if the field is absent.
3. **Device type inference (fallback)** — if `host.type` is still `"unknown"`, performs a keyword match on `observer.sys_descr` to set `host.type` (router, switch, firewall, ap, server). This is a best-effort fallback; setting `host.type` explicitly in the collector config is preferred.
4. **Vendor detection** — runs a regex match on `observer.sys_descr` to set `observer.vendor`. Cisco, Juniper, Arista, Fortinet, Palo Alto, HPE, and Aruba are recognized out of the box, and you can extend the pipeline to recognize additional vendors.

The pipeline is created by the `scripts/setup_elasticsearch.sh` script in the [Network Topology plugin repository](https://github.com/elastic/kibana-network-topology-plugin).
