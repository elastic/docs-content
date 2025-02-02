---
navigation_title: "Configure data volume"
---

# Configure data volume for {{elastic-endpoint}} [endpoint-data-volume]


{{elastic-endpoint}}, the installed component that performs {{elastic-defend}}'s threat monitoring and prevention, is optimized to reduce data volume and CPU usage. You can disable or modify some of these optimizations by reconfiguring the following [advanced settings](../../../solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#adv-policy-settings) in the {{elastic-defend}} integration policy.

::::{important} 
Modifying these advanced settings from their defaults will increase the volume of data that {{elastic-endpoint}} processes and ingests, and increase {{elastic-endpoint}}'s CPU usage. Make sure you’re aware of how these changes will affect your storage capabilities and performance.
::::


Each setting has several OS-specific variants, represented by `[linux|mac|windows]` in the names listed below. Use the variant relevant to your hosts' operating system (for example, `windows.advanced.events.deduplicate_network_events` to configure network event deduplication for Windows hosts).


## Network event deduplication [network-event-deduplication] 

[8.15] When repeated network connections are detected from the same process, {{elastic-endpoint}} will not produce network events for subsequent connections. To disable or reduce deduplication of network events, use these advanced settings:

`[linux|mac|windows].advanced.events.deduplicate_network_events`
:   Enter `false` to completely disable network event deduplication. Default: `true`

`[linux|mac|windows].advanced.events.deduplicate_network_events_below_bytes`
:   Enter a transfer size threshold (in bytes) for events you want to deduplicate. Connections below the threshold are deduplicated, and connections above it are not deduplicated. This allows you to suppress repeated connections for smaller data transfers but always generate events for larger transfers. Default: `1048576` (1MB)


## Data in `host.*` fields [host-fields] 

[8.18] {{elastic-endpoint}} includes only a small subset of the data in the `host.*` fieldset in event documents. Full `host.*` information is still included in documents written to the `metrics-*` index pattern and in {{elastic-endpoint}} alerts. To override this behavior and include all `host.*` data for events, use this advanced setting:

`[linux|mac|windows].advanced.set_extended_host_information`
:   Enter `true` to include all `host.*` event data. Default: `false`

::::{note} 
Users should take note of how a lack of some `host.*` information may affect their [event filters](../../../solutions/security/manage-elastic-defend/event-filters.md) or [Endpoint alert exceptions](../../../solutions/security/detect-and-alert/add-manage-exceptions.md#endpoint-rule-exceptions).
::::



## Merged process and network events [merged-process-network] 

[8.18] {{elastic-endpoint}} merges process `create`/`terminate` events (Windows) and `fork`/`exec`/`end` events (macOS/Linux) when possible. This means short-lived processes only generate a single event containing the details from when the process terminated. {{elastic-endpoint}} also merges network `connection/termination` events (Windows/macOS/Linux) when possible for short-lived connections. To disable this behavior, use these advanced settings:

`[linux|mac|windows].advanced.events.aggregate_process`
:   Enter `false` to disable merging of process events. Default: `true`

`[linux|mac|windows].advanced.events.aggregate_network`
:   Enter `false` to disable merging of network events. Default: `true`

::::{note} 
Merged events can affect the results of [event filters](../../../solutions/security/manage-elastic-defend/event-filters.md). Notably, for merged events, `event.action` is an array containing all actions merged into the single event, such as `event.action=[fork, exec, end]`. In that example, if your event filter omits all fork events (`event.action : fork`), it will also filter out all merged events that include a `fork` action. To prevent such issues, you’ll need to modify your event filters accordingly, or set the `[linux|mac|windows].advanced.events.aggregate_process` and `[linux|mac|windows].advanced.events.aggregate_network` advanced settings to `false` to prevent {{elastic-endpoint}} from merging events.
::::



## MD5 and SHA-1 hashes [md5-sha1-hashes] 

[8.18] {{elastic-endpoint}} does not report MD5 and SHA-1 hashes in event data by default. These will still be reported if any [trusted applications](../../../solutions/security/manage-elastic-defend/trusted-applications.md), [blocklist entries](../../../solutions/security/manage-elastic-defend/blocklist.md), [event filters](../../../solutions/security/manage-elastic-defend/event-filters.md), or [Endpoint exceptions](../../../solutions/security/detect-and-alert/add-manage-exceptions.md#endpoint-rule-exceptions) require them. To include these hashes in all event data, use these advanced settings:

`[linux|mac|windows].advanced.events.hash.md5`
:   Enter `true` to compute and include MD5 hashes for processes and libraries in events. Default: `false`

`[linux|mac|windows].advanced.events.hash.sha1`
:   Enter `true` to compute and include SHA-1 hashes for processes and libraries in events. Default: `false`

`[linux|mac|windows].advanced.alerts.hash.md5`
:   Enter `true` to compute and include MD5 hashes for processes and libraries in alerts. Default: `false`

`[linux|mac|windows].advanced.alerts.hash.sha1`
:   Enter `true` to compute and include SHA-1 hashes for processes and libraries in alerts. Default: `false`

