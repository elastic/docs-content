---
navigation_title: "community_id"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/community_id-processor.html
---

# Community ID Network Flow Hash [community_id-processor]


The `community_id` processor computes a network flow hash according to the [Community ID Flow Hash specification](https://github.com/corelight/community-id-spec).

The flow hash is useful for correlating all network events related to a single flow. For example, you can filter on a community ID value and you might get back the Netflow records from multiple collectors and layer 7 protocol records from the Network Packet Capture integration.

By default the processor is configured to read the flow parameters from the appropriate Elastic Common Schema (ECS) fields. If you are processing ECS data, no parameters are required.


## Examples [_examples_5]

```yaml
  - community_id:
```

If the data does not conform to ECS, you can customize the field names that the processor reads from. You can also change the target field that the computed hash is written to. For example:

```yaml
  - community_id:
      fields:
        source_ip: my_source_ip
        source_port: my_source_port
        destination_ip: my_dest_ip
        destination_port: my_dest_port
        iana_number: my_iana_number
        transport: my_transport
        icmp_type: my_icmp_type
        icmp_code: my_icmp_code
      target: network.community_id
```

If the necessary fields are not present in the event, the processor silently continues without adding the target field.


## Configuration settings [_configuration_settings_15]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `fields` | No |  | Field names that the processor reads from:<br><br>`source_ip`<br>:   Field containing the source IP address.<br><br>`source_port`<br>:   Field containing the source port.<br><br>`destination_ip`<br>:   Field containing the destination IP address.<br><br>`destination_port`<br>:   Field containing the destination port.<br><br>`iana_number`<br>:   Field containing the IANA number. The following protocol numbers are currently supported: 1 ICMP, 2 IGMP, 6 TCP, 17 UDP, 47 GRE, 58 ICMP IPv6, 88 EIGRP, 89 OSPF, 103 PIM, and 132 SCTP.<br><br>`transport`<br>:   Field containing the transport protocol. Used only when the `iana_number` field is not present.<br><br>`icmp_type`<br>:   Field containing the ICMP type.<br><br>`icmp_code`<br>:   Field containing the ICMP code.<br> |
| `target` | No |  | Field that the computed hash is written to. |
| `seed` | No |  | Seed for the community ID hash. Must be between 0 and 65535 (inclusive). Theseed can prevent hash collisions between network domains, such as a staging andproduction network that use the same addressing scheme. This setting results ina 16-bit unsigned integer that gets incorporated into all generated hashes. |

