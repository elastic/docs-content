---
applies_to:
  stack: all
  serverless:
    security: all
---

# {{elastic-defend}} advanced settings

When configuring an {{elastic-defend}} integration policy, access the [**Advanced settings** section](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#adv-policy-settings) to fine-tune how the integration behaves in your environment. Use these settings to customize detection, performance, and security options based on your specific requirements.

:::{important}
Advanced settings are not recommended for most users. Use them only if you have specific configuration or security requirements. If configured incorrectly, these settings can cause unpredictable behavior.
:::

`[linux,mac,windows].advanced.agent.connection_delay`
:   Added in 7.9.0.

    *How long to wait for agent connectivity before sending first policy reply, in seconds. Default: `60`.*

    {{elastic-endpoint}} applies a cached configuration from disk immediately on start up. However, before generating a policy response document, {{elastic-endpoint}} waits to first establish a connection to {{elastic-agent}} to see if there are configuration updates. Use this setting to specify how long that delay should be. Regardless of this setting, {{elastic-endpoint}} will periodically attempt to (re)connect to {{elastic-agent}} if it isn't connected.


`[mac,windows].advanced.alerts.cloud_lookup`

:   Added in 7.12.0.

    *Check a cloud service for known false positives before generating malware alerts. Default: `true`.*

    Before blocking or alerting on malware files, {{elastic-endpoint}} reaches out to an Elastic cloud service ([https://cloud.security.elastic.co](https://cloud.security.elastic.co)) to see if the alert is a known false positive. Use this setting to disable this feature.

    ::::{note}
    Disabling cloud lookup for alerts may result in higher false positive rates.
    ::::


`[linux,mac,windows].advanced.alerts.hash.md5`
:   Added in 8.16.0.

    *Include MD5 hashes in alerts. Even if set to false, MD5 hashes will still be included if alert exceptions, trusted apps, or blocklisting require them. Default: <=8.17: true, >=8.18: false.*

    {{elastic-endpoint}} doesn't generate MD5 hashes in alerts unless alert exceptions, trusted apps, or blocklisting requires them, in which case this setting is ignored. This setting was added in 8.16 to allow users to opt out of MD5 hashing; starting with 8.18, users are opted out by default. Prior to 8.16, MD5 hashes were always included.


`[linux,mac,windows].advanced.alerts.hash.sha1`
:   Added in 8.16.0.

    *Include SHA-1 hashes in alerts. Even if set to `false`, SHA-1 hashes will still be included if alert exceptions, trusted apps, or blocklisting require them. Default: <=8.17: true, >=8.18: `false`.*

    {{elastic-endpoint}} doesn't generate SHA-1 hashes in alerts unless alert exceptions, trusted apps, or blocklisting requires them, in which case this setting is ignored. This setting was added in 8.16 to allow users to opt out of SHA-1 hashing; starting with 8.18, users are opted out by default. Prior to 8.16, SHA-1 hashes were always included.


`windows.advanced.alerts.rollback.self_healing.enabled`
:   Added in 8.4.0.

    *Enable self-healing by erasing attack artifacts when prevention alerts are triggered. Warning: data loss can occur. Default: `false`.*

    When a prevention alert is generated, {{elastic-endpoint}} can [roll back](/solutions/security/configure-elastic-defend/configure-self-healing-rollback-for-windows-endpoints.md) recent filesystem changes likely associated with the attack. Use this setting to enable the self-healing rollback feature.
    
    ::::{warning}
    This feature can cause permanent data loss.
    ::::


`windows.advanced.alerts.rollback.self_healing.process_enabled`
:   Added in 8.8.0.

    *Enable automatic removal of malware processes when a related prevention alert fires, including processes which were not directly involved in the alert. Requires `rollback.self_healing.enabled` to also be enabled. Default: `true`.*

    As an extension to the base-level self-healing rollback feature, {{elastic-endpoint}} can terminate recently spawned processes when an attack occurs. Use this setting to enable this feature.

    ::::{warning}
    This feature can cause permanent data loss.
    ::::


`windows.advanced.alerts.rollback.self_healing.registry_enabled`
:   Added in 8.8.0.

    *Enable self-healing of registry based malware artifacts when prevention alerts are triggered. Requires `rollback.self_healing.enabled` to also be enabled. Default: `true`.*

    As an extension to the base-level self-healing rollback feature, {{elastic-endpoint}} can roll back recent registry changes when an attack occurs. Use this setting to enable this feature.
    
    ::::{warning}
    This feature can cause permanent data loss.
    ::::


`[linux,mac,windows].advanced.alerts.sample_collection`
:   Added in 8.13.0.

    *Allow Elastic to collect samples of unknown malware files. Default: `true`.*

    To improve the efficacy of malware and reputation protections, Elastic collects samples of unknown malware files. Use this setting to disable the sample collection.


`[linux,mac,windows].advanced.allow_cloud_features`
:   Added in 8.18.0.

    *Explicitly define which cloud services are permitted. Valid services are `sample-collection`, `reputation-lookup`, `malware-lookup`, `artifacts-update`, `staged-artifacts-rollout`. If any comma-separated values are provided, all other services are disabled. To disallow all, use the keyword `none`. Warning: this may reduce protection efficacy and increase false positive rates. Default: all services are permitted.*

    {{elastic-endpoint}} has various features that require use of cloud services. Each of those features has an individual advanced setting that allows users to disable it. This setting provides an alternative way to disable features that need cloud services in a way that inherently disables all future cloud service features by default.

    ::::{warning}
    Disabling cloud services may reduce protection efficacy and increase false positive rates.
    ::::


`[linux,mac,windows].advanced.artifacts.global.base_url`
:   Added in 7.9.0.

    *Modify the base URL from which to download protection artifact updates. Default: `https://artifacts.security.elastic.co`.*

    Change this setting when [configuring air-gapped environments](/solutions/security/configure-elastic-defend/configure-offline-endpoints-air-gapped-environments.md) to receive protection updates.


`[linux,mac,windows].advanced.artifacts.global.ca_cert`
:   Added in 7.9.0.

    *Provide an additional PEM-encoded certificate to validate the protection artifact update SSL/TLS server. Default: none.*

    This allows specification of an additional PEM-encoded certificate for verification of the SSL/TLS server that is hosting global protection artifacts updates.


`[linux,mac,windows].advanced.artifacts.global.channel`
:   Added in 8.18.0.

    *Modify the release channel for protection artifact updates. The `default` is staged rollout, `rapid` receives candidate artifacts as soon as available, and `stable` only receives artifact updates after staged rollout has finished. Default: `default`.*

    Global protection artifact updates are publicly released in stages to ensure stability across the {{elastic-defend}} user base. Use this setting to opt specific endpoints in (such as test or lab machines) or out (such as mission-critical systems) of the staged rollout process.


`[linux,mac,windows].advanced.artifacts.global.interval`
:   Added in 7.9.0.

    *Specify the period between protection artifact update attempts, in seconds. Default: `3600`.*

    By default {{elastic-endpoint}} checks for protection artifact updates every hour. Use this setting to modify this interval.


`[linux,mac,windows].advanced.artifacts.global.manifest_relative_url`
:   Added in 7.9.0.

    *Modify the relative URL from which to download protection artifact manifests. Default: `/downloads/endpoint/manifest/artifacts-<version>.zip`.*

    Specifies the relative path appended to the base URL (`[linux,mac,windows].advanced.artifacts.global.base_url`) to form the full URL for downloading protection artifact updates. When configuring protection artifact updates in [air-gapped environments](/solutions/security/configure-elastic-defend/configure-offline-endpoints-air-gapped-environments.md), this setting typically doesn't need to be modified. If you do override it, {{elastic-endpoint}} will use the exact path you provide, without replacing `<version>` with the current version number.


`[linux,mac,windows].advanced.artifacts.global.proxy_disable`
:   Added in 8.8.0.

    *Disable the use of a proxy when downloading protection artifact updates. Default: `false`.*

    This allows you to disable the use of a proxy even if one is provided by other configuration.


`[linux,mac,windows].advanced.artifacts.global.proxy_url`
:   Added in 8.8.0.

    *Override all other proxy settings for use when downloading protection artifact updates. Default: none.*

    Use this setting to override all other configuration that defines the proxy to be used when downloading global protection artifacts.


`[linux,mac,windows].advanced.artifacts.global.public_key`
:   Added in 7.9.0.

    *Override the PEM-encoded public key used to verify the protection artifact manifest signature. Default: none.*

    Specifies the public key used to verify the signature of global protection artifacts (not the SSL connection to the server that hosts them). It is not needed for air-gapped environments that re-host artifacts.


`[linux,mac,windows].advanced.artifacts.user.ca_cert`
:   Added in 7.9.0.

    *Provide an additional PEM-encoded certificate for {{fleet}} Server SSL/TLS verification. Default: none.*

    Specifies the certificate used to verify the SSL/TLS connection to the {{fleet}} Server. We typically recommend configuring this at the {{fleet}} level, so it applies consistently across {{elastic-agent}} and all integrations, rather than setting it specifically for {{elastic-endpoint}}.


`[linux,mac,windows].advanced.artifacts.user.proxy_disable`
:   Added in 8.8.0.

    *Disable the use of a proxy when downloading user artifact updates. Default: `false`.*

    This allows you to disable the use of a proxy for reaching {{fleet}} Server even if one is provided by other configuration.


`[linux,mac,windows].advanced.artifacts.user.proxy_url`
:   Added in 8.8.0.

    *Override all other proxy settings for use when downloading user artifact updates from {{fleet}} Server. Default: none.*

    Use this setting to configure a proxy server when communicating with the {{fleet}} Server. We typically recommend [configuring proxy settings at the {{elastic-agent}} level](/reference/fleet/fleet-agent-proxy-support.md) to ensure consistent and centralized proxy handling.


`[linux,mac,windows].advanced.capture_command_line`
:   Added in 8.14.0.

    *Include the command line as part of the collected process information for all event types. Default: `false`.*

    By default, {{elastic-endpoint}} excludes command-line arguments from most `process` fieldsets to help reduce data volume. Use this setting to include them—for example, to allow {{elastic-endpoint}} alerts or rule exceptions to be based on command-line content.


`[linux,mac].advanced.capture_env_vars`
:   Added in 8.6.0 (Linux), 8.7.0 (macOS).

    *Provide a comma-separated list of up to five environment variables to capture in process create events. Default: none.*

    Use this setting to include a limited number of environment variables in process `create` events.


`[mac,windows].advanced.device_control.filter_images`
:   Added in 9.2.0.

    *Filter out file  backed images and CD-ROM volumes from consideration by device control. Default: `true`.*


`[linux,mac,windows].advanced.diagnostic.enabled`
:   Added in 7.11.0 (Windows), 7.12.0 (macOS and Linux).

    *Enable diagnostic features. Default: `true`.*

    Use this setting to disable diagnostic mode, which tests new protections and rules to ensure low false positive rates upon production release. The results of this testing are only collected if telemetry is enabled. 
    
    ::::{note}
    We recommend keeping diagnostic mode enabled to help improve product quality and ensure new protections perform effectively in your environment before they’re released.
    ::::
  

`windows.advanced.diagnostic.rollback_telemetry_enabled`
:   Added in 8.1.0.

    *Enable diagnostic self-healing features without affecting other diagnostic features. Default: `true`.*

    Use this setting to disable the diagnostic (testing) self-healing features without affecting other diagnostic functionalities.


`[linux,mac,windows].advanced.document_enrichment.fields`
:   Added in 8.11.0.

    *Provide a comma-delimited set of key=value pairs of values to add into all documents. Each key must begin with `Custom`. An example is `Custom.key=value1,Custom.key2=value2`. Default: none.*

    Use this setting to add custom key/value pairs into all {{elastic-endpoint}} documents. It works similarly to the [**Custom fields** {{elastic-agent}} policy configuration](/reference/fleet/agent-policy.md#add-custom-fields), which {{elastic-endpoint}} doesn't support.

    
`[linux,mac,windows].advanced.elasticsearch.delay`
:   Added in 7.9.0.

    *Specify the delay between sending documents to {{es}}, in seconds. Default: `120`.*

    To improve compression, {{elastic-endpoint}} pushes unsent documents to {{es}} at periodic intervals, rather than immediately after each new event is generated. Use this setting to modify that interval. Regardless of this setting, {{elastic-endpoint}} will always flush all event data immediately when an alert is generated.


`[linux,mac,windows].advanced.elasticsearch.tls.ca_cert`
:   Added in 7.9.0.

    *Provide an additional PEM-encoded certificate for {{es}} certificate authority. Default: none.*

    Use this setting to configure an additional root certificate for validating {{elastic-endpoint}}'s connection to {{es}}. We typically recommend configuring this at the {{fleet}} level.


`[linux,mac,windows].advanced.elasticsearch.tls.verify_hostname`
:   Added in 7.9.0.

    *Verify the hostname for the {{es}} SSL/TLS connection. Default: `true`.*

    Use this setting to disable TLS hostname verification for {{elastic-endpoint}}'s connection to {{es}}. We typically recommend configuring this at the [{{fleet}} level](/reference/fleet/secure-connections.md).


`[linux,mac,windows].advanced.elasticsearch.tls.verify_peer`
:   Added in 7.9.0.

    *Verify certificates for the {{es}} SSL/TLS connection. Default: `true`.*

    Use this setting to disable TLS peer verification for {{elastic-endpoint}}'s connection to {{es}}. We typically recommend configuring this at the [{{fleet}} level](/reference/fleet/secure-connections.md).


`[linux,mac,windows].advanced.event_filter.default`
:   Added in 8.3.0.

    *Download and use default event filter rules from Elastic. Default: `true`.*

    By default, {{elastic-endpoint}} doesn't generate and stream events to {{es}} for system activity known to be noisy and of limited security value, based on dynamic rules Elastic maintains. Use this setting to disable that suppression.


`[linux,mac,windows].advanced.events.aggregate_network`
:   Added in 8.18.0.

    *Reduce event volume by merging related network events into fewer aggregate events. Default: <=8.17: `false`, >=8.18: `true`.*

    {{elastic-endpoint}} [merges rapid network connect and disconnect events](/solutions/security/configure-elastic-defend/configure-data-volume-for-elastic-endpoint.md#merged-process-network) into a single event document. Use this setting to disable that behavior.


`[linux,mac,windows].advanced.events.aggregate_process`
:   Added in 8.16.0.

    *Reduce event volume by merging related process events into fewer aggregate events. Default: <=8.17: `false`, >=8.18: `true`.*

    {{elastic-endpoint}} [merges rapid process `create`/`fork`/`exec`/`end` events](/solutions/security/configure-elastic-defend/configure-data-volume-for-elastic-endpoint.md#merged-process-network) into a single event document. Use this setting to disable that behavior. This setting was made available in 8.16; starting with 8.18, this behavior is enabled by default.


`[linux,mac,windows].advanced.events.ancestry_in_all_events`
:   Added in 8.15.0.

    *Include ancestor process entity IDs in all event types; by default they are only included in alerts and process events. Default: `false`.*

    Prior to 8.15, {{elastic-endpoint}} included `process.ancestry` in all event documents. This field helps render the event analyzer more quickly and is primarily needed for process events. In 8.15, this was changed to limit data volume.


`windows.advanced.events.api`
:   Added in 8.8.0.

    *Enable ETW API events. `false` disables them even if they are needed by other features. Default: `true`.*

    Use this setting to disable API event collection, even if other {{elastic-endpoint}} features require them.
    
    :::{warning}
    Disabling API event collection may break other {{elastic-endpoint}} features.
    :::


`windows.advanced.events.api_disabled`
:   Added in 8.11.0.

    *Provide a comma-separated list of API names to selectively disable. Default: none.*

    Use this setting to disable the collection of specific API events for performance or troubleshooting purposes. API names can be found at `process.Ext.api.name` with the corresponding API events.


`windows.advanced.events.api_verbose`
:   Added in 8.11.0.

    *Send high-volume API events to {{es}}. Warning: event filtering is recommended if enabled. Default: `false`.*


`windows.advanced.events.callstacks.emit_in_events`
:   Added in 8.8.0.

    *Include callstacks in regular events whenever possible. When disabled (`false`), they are only included in events that trigger behavioral protection rules. Warning: event filtering is recommended if enabled. Default: `false`.*


`windows.advanced.events.callstacks.exclude_hotpatch_extension_pages`
:   Added in 8.15.2.

    *Exclude Windows 11 24H2 hotpatch extension pages, which resemble injected code, from callstack module stomp scanning. Default: `true`.*


`windows.advanced.events.callstacks.file`
:   Added in 8.8.0.

    *Collect callstacks during file events. Default: `true`.*


`windows.advanced.events.callstacks.image_load`
:   Added in 8.8.0.

    *Collect callstacks during image/library load events. Default: `true`.*


`windows.advanced.events.callstacks.include_network_images`
:   Added in 8.9.0.

    *Parse executables and DLLs on network shares for callstack symbols. Disable this if Endpoint hangs because of a network file system. Default: `true`.*


`windows.advanced.events.callstacks.process`
:   Added in 8.8.0.

    *Collect callstacks during process events. Default: `true`.*


`windows.advanced.events.callstacks.registry`
:   Added in 8.8.0.

    *Collect callstacks during registry events. Default: `true`.*


`windows.advanced.events.callstacks.timeout_microseconds`
:   Added in 8.12.0.

    *Alter the maximum runtime of inline callstack collection/enrichment, in microseconds. Default: `100000`.*


`windows.advanced.events.callstacks.use_hardware`
:   Added in 8.16.0.

    *Use hardware callstacks (e.g. Intel CET) if supported by the OS and CPU. Default: `true`.*


`windows.advanced.events.check_debug_registers`
:   Added in 8.11.0.

    *Check debug registers inline to detect the use of hardware breakpoints. Malware may use hardware breakpoints to forge benign-looking call stacks. Default: `true`.*


`[linux,mac,windows].advanced.events.deduplicate_network_events`
:   Added in 8.15.0.

    *Deduplicate network events based on repeated Src-IP/Dst-IP/Dst-Port/PID tuple grouping. Default: <=8.14: `false`, >=8.15: `true`.*

    To limit data volume, {{elastic-endpoint}} doesn't emit network events for [repeated connections](/solutions/security/configure-elastic-defend/configure-data-volume-for-elastic-endpoint.md#network-event-deduplication) based on the Src-IP/Dst-IP/Dst-Port/PID tuple grouping. Use this setting to disable that suppression.


`[linux,mac,windows].advanced.events.deduplicate_network_events_below_bytes`
:   Added in 8.15.0.

    *Specify a network event deduplication transfer threshold, in bytes. Events for connections exceeding the threshold will always be emitted. A value `0` disables this feature. Default: `1048576` (1MB).*

    Specify a transfer size threshold for events you want to deduplicate. Connections below the threshold are deduplicated, and connections above it are not deduplicated. This allows [network event deduplication](/solutions/security/configure-elastic-defend/configure-data-volume-for-elastic-endpoint.md#network-event-deduplication) to be applied only to low data volume connections.


`linux.advanced.events.disable_fd_kprobes`
:   Added in 8.8.0.

    *Disable file descriptor tracking kprobes to reduce Endpoint processing at the expense of missing fchdir-based working directory changes. If eBPF is used for system monitoring, this option is ignored. If file events are enabled, this option is ineffective. Default is `false`.*

    Use this setting to reduce {{elastic-endpoint}}'s CPU usage when using kprobes instead of eBPF. Enabling it causes many file paths in events to appear as relative rather than absolute.


`windows.advanced.events.disable_image_load_suppression_cache`
:   Added in 8.12.1.

    *Disable the cache system used to improve image (DLL) load performance. Only disable this if image load events are not being generated as expected. Default: `false`.*

    The image load suppression cache improves system performance by allowing {{elastic-endpoint}} to inform its kernel driver about DLLs to avoid eventing upon as they are not of interest. This feature improves system responsiveness and reduces {{elastic-endpoint}} CPU usage. Use this setting only for troubleshooting image load event issues.

`windows.advanced.events.disable_registry_write_suppression`
:   Added in 8.12.1.

    *Ignore uninteresting registry events for performance. Only modify this to troubleshoot if registry events are not functioning as expected. Default: `false`.*

    Registry write suppression improves system performance by enabling {{elastic-endpoint}} to inform its driver that certain types of registry operations are uninteresting. Once deemed uninteresting, the driver can quickly drop these events, improving system responsiveness and reducing {{elastic-endpoint}} CPU usage. Use this setting only for troubleshooting if registry events are not functioning as expected.


`linux.advanced.events.enable_caps`
:   Added in 8.14.0.

    *Include Linux process capabilities in process events written to {{es}}. Capabilities must be enabled for some SIEM detection rules. Warning: enabling this will increase data volume. Default: <=8.13: `true`, >=8.14: `false`.*

    Use this setting to enable reporting of process capabilities on Linux. {{elastic-endpoint}} began reporting these capabilities in 8.11.0, but this was disabled by default in 8.14.0 due to data volume concerns. This setting must be enabled for some SIEM detection rules, but all malicious behavior detection rules running within {{elastic-defend}} work regardless of its status.


`windows.advanced.events.enforce_registry_filters`
:   Added in 8.15.0.

    *Reduce data volume by filtering out registry events which are not relevant to behavioral protections. Default: `true`.*


`windows.advanced.events.event_on_access.file_paths`
:   Added in 8.15.0.

    *Provide a comma-separated list of additional wildcard patterns that will be monitored for read access. At most one match per pattern per process will be reported. If possible, drive letters will be converted to NT paths (e.g. `\Device\HarddiskVolume4`), but conversion will fail for per-user drives, such as network drives. Put only commas (no spaces) between entries. Wildcard matching is case-insensitive. Check Microsoft FsRtlIsNameInExpression documentation for wildcard matching rules. Default: none.*

`windows.advanced.events.event_on_access.registry_paths`
:   Added in 8.15.0.

    *Provide a comma-separated list of registry paths that will be monitored for read access. These must be NT paths (for example, `\REGISTRY\MACHINE\SOFTWARE\Microsoft\...`). At most one match per pattern per process will be reported. Only commas (no spaces) should be used between entries. Wildcard matching is case-insensitive. See Microsoft FsRtlIsNameInExpression documentation for wildcard matching rules.*


`[linux,mac,windows].advanced.events.file.max_hash_size_mb`
:   Added in 8.16.0.

    *Attempt to include `file.hash.sha256` in file events. Hashing is asynchronous, best-effort, and not guaranteed to succeed, especially on network drives. Warning: file hashing will increase Endpoint's CPU and I/O, and may adversely affect system responsiveness. Warning: Event processing will be delayed due to the time spent hashing, which will interfere with malicious behavior and ransomware protections and potentially allow threats to inflict additional damage. Set to `off` to disable this feature. Set to `0` to hash all files up to 1 GiB. Otherwise, this sets the maximum to-be-hashed file size in MiB. Default: `off`.*

    ::::{note}
    Enabling file hashing may increase CPU and IO use, decrease system responsiveness, and interfere with malicious behavior and ransomware protections.
    ::::


`windows.advanced.events.file.origin_info_collection`
:   Added in 8.19.0.

    *Include `file.origin_url`, `file.origin_referrer_url`, and `file.Ext.windows.zone_identifier` in file events. These fields show the details of file's Mark of the Web. Default: `true`.*


`[linux,mac,windows].advanced.events.hash.md5`
:   Added in 8.16.0.

    *Include MD5 hashes in processes and libraries in events. Even if set to `false`, MD5 hashes will still be included if alert exceptions, trusted apps, or blocklisting require them. Default: <=8.17: `true`, >=8.18: `false`.*

    {{elastic-endpoint}} doesn't generate MD5 hashes in events unless event filters or trusted apps require them, in which case this setting is ignored. This setting was added in 8.16 to allow users to opt out of MD5 hashing; starting with 8.18, users are opted out by default. Prior to 8.16, MD5 hashes were always included.


`[linux,mac,windows].advanced.events.hash.sha1`
:   Added in 8.16.0.

    *Include SHA-1 hashes in processes and libraries in events. Even if set to `false`, SHA-1 hashes will still be included if alert exceptions, trusted apps, or blocklisting require them. Default: <=8.17: `true`, >=8.18: `false`.*

    {{elastic-endpoint}} doesn't generate SHA-1 hashes in events unless event filters or trusted apps require them, in which case this setting is ignored. This setting was added in 8.16 to allow users to opt out of SHA-1 hashing; starting with 8.18, users are opted out by default. Prior to 8.16, SHA-1 hashes were always included.


`[linux,mac,windows].advanced.events.hash.sha256`
:   Added in 8.16.0.

    *Include SHA-256 hashes in processes and libraries in events. Even if set to `false`, SHA-256 hashes will still be included if alert exceptions, trusted apps, or blocklisting require them. Default: <=8.17: `true`, >=8.18: `false`.*

    {{elastic-endpoint}} doesn't generate SHA-256 hashes in events unless event filters or trusted apps require them, in which case this setting is ignored. This setting was added in 8.16 to allow users to opt out of SHA-256 hashing; starting with 8.18, users are opted out by default. Prior to 8.16, SHA-256 hashes were always included.


`mac.advanced.events.image_load`
:   Added in 8.11.0.

    *Enable kernel image load events. `false` disables them even if they are needed by other features. Default: `true`.*

    Use this setting to disable image load events, even if other {{elastic-endpoint}} features require them. 

    :::{warning}
    Disabling image load events may break other {{elastic-endpoint}} features.
    :::


`windows.advanced.events.image_load.origin_info_collection`
:   Added in 8.19.0.

    *Include `dll.origin_url`, `dll.origin_referrer_url`, and `dll.Ext.windows.zone_identifier` in image load events. These fields normally show where the loaded DLL was downloaded from, using information taken from the file's Mark of the Web. Default: <=9.1: `false`, >=9.2: `true`.*


`windows.advanced.events.memory_scan`
:   Added in: 8.14.0.

    *Enable an additional scan of suspicious memory regions against well-known malware signatures when malicious behavior alerts are triggered. Default: `true`.*

    Additional memory scanning of behavior alerts provides more context for responders analyzing alerts. Use this setting to disable this feature.


`[linux,mac,windows].advanced.events.process_ancestry_length`
:   Added in 8.15.0.

    *Maximum number of process ancestry entries to include in process events. Default: <=8.14: `20`, >=8.15: `5`.*

    Use this setting to control how many ancestor processes {{elastic-endpoint}} includes in the `process.ancestry` field. Prior to 8.15, this field contained the last 20 ancestor processes; starting with 8.15, it was reduced to the last 5, to limit data volume.


`windows.advanced.events.process.creation_flags`
:   Added in 8.13.0.

    *Enrich process events with process creation flags. Only use this setting to troubleshoot if process events are not functioning as expected. Default: `true`.*

    Use this setting to control whether {{elastic-endpoint}} captures process creation flags, such as `CREATE_SUSPENDED`, in process events.


`windows.advanced.events.process.origin_info_collection`
:   Added in 8.19.0.

    *Include `process.origin_url`, `process.origin_referrer_url`, and `process.Ext.windows.zone_identifier` in process events. These fields normally show where the process's executable file was downloaded from, using information taken from the file's Mark of the Web. Default: <=9.1: `false`, >=9.2: `true`.*


`windows.advanced.events.security.event_disabled`
:   Added in 9.2.0.

    *Provide a comma-separated list of security event IDs to selectively disable. An example is `4624,4800,4801`. Default: none.*


`windows.advanced.events.security.provider_etw`
:   Added in 8.19.0.

    *Enable the Microsoft-Windows-Security-Auditing ETW provider for security events collection. Default: `true`.*


`linux.advanced.fanotify.ignore_unknown_filesystems`
:   Added in 8.4.0.

    *Control if the fanotify subsystem should ignore unknown filesystems. By default only Elastic-tested filesystems are monitored. If set to `false`, all filesystems, excluding certain known-benign filesystems, will be monitored. Default: `true`.*

    Use this setting to control how {{elastic-endpoint}} handles unknown filesystems when using fanotify to monitor for malware. Filesystems that aren't monitored won't generate malware alerts. Use the `monitored_filesystems` and `ignored_filesystems` settings to more explicitly control which filesystems are monitored. When `false`, only an internally curated list of filesystems will be ignored, all others will be marked; additional filesystems can be ignored via `ignored_filesystems`. `monitored_filesystems` is ignored when `ignore_unknown_filesystems` is `false`.


`linux.advanced.fanotify.ignored_filesystems`
:   Added in 8.4.0.

    *Provide a comma-separated list of additional filesystems for the fanotify subsystem to ignore. Names should be as they appear in `/proc/filesystems`, for example `ext4,tmpfs`. Default: none.*

    Use this setting to specify filesystems that fanotify should ignore when monitoring for malware. Filesystems that aren't monitored won't generate malware alerts.


`linux.advanced.fanotify.monitored_filesystems`
:   Added in 8.4.0.

    *Provide a comma-separated list of additional filesystems for fanotify subsystem to monitor. Names should be as they appear in `/proc/filesystems`, for example `jfs,ufs,ramfs`. When `ignore_unknown_filesystems` is `false`, this option is ignored. Warning: it's recommended to avoid network backed filesystems. Default: none.*

    Use this setting to specify filesystems for fanotify to monitor for malware. Filesystems that aren't monitored won't generate malware alerts. 


`linux.advanced.fanotify.seccomp_restricted`
:   Added in 8.13.1.

    *Prevent permission checking from using the `open`/`openat` syscalls when running on kernels which require `FAN_OPEN_PERM` (older than 5.0). This will avoid potential deadlocks with other antivirus products at the cost of racy hash-based trusted application entries. Ignored when running on newer kernels. Default: `false`.*


`[linux,mac,windows].advanced.file_cache.file_object_cache_size`
:   Added in 8.12.0.

    *Control the number of file metadata cache entries stored in memory. Larger values can improve performance but increase memory usage. Default: `5000`.*

    Elastic caches information about recently read files in memory. Use this setting to control the number of recent file entries to cache.


`windows.advanced.firewall_anti_tamper`
:   Added in 9.2.0.

    *Enable firewall anti tamper prevention or detection. Tamper protetion must also be enabled. Allowed values are `prevent`, `detect`, and `off`. Default: `prevent`.*


`[linux,mac,windows].advanced.flags`
:   Added in 8.13.0 (Windows), 8.16.0 (macOS and Linux).

    *A comma-separated list of feature flags. Currently no feature flags are supported.*


`mac.advanced.harden.self_protect`
:   Added in 7.11.0.

    *Enable self-protection hardening on macOS. Default: `true`.*

    Use this setting to enable self-protection on macOS. This hardens {{elastic-endpoint}} and {{elastic-agent}} processes, files, and services against basic tampering attempts. This is distinct from [tamper protection](https://www.elastic.co/docs/solutions/security/configure-elastic-defend/prevent-elastic-agent-uninstallation).


`linux.advanced.host_isolation.allowed`
:   Added in 8.6.1.

    *Force disable host isolation. If a host is currently not isolated, it will refuse to isolate, and likewise, a host will refuse to release if it is currently isolated. Default: `true`.*

    Use this setting to control whether host isolation activity on Linux is allowed. If disabled, the host remains unisolated even when isolation is requested. Setting this to `true` will override internal detection of the system's ability to support host isolation.


`mac.advanced.image_load.capture`
:   Added in 8.11.0.

    *Collect and send image load events to {{es}}. Warning: this can lead to very high data volumes; use of event filters to drop unwanted events is strongly recommended. Default: `false`.*
    
    If malicious behavior protection is enabled, {{elastic-endpoint}} by default monitors for image load events, but doesn't emit them to {{es}} due to high data volume. Use this setting to allow those events to be emitted to {{es}}, regardless of whether malicious behavior protection is enabled.


`windows.advanced.kernel.asyncimageload`
:   Added in 7.9.0.

    *Enable kernel asynchronous image load events. `false` disables them even if they are needed by other features. Default: `true`.*

    Use this setting to disable kernel asynchronous image load events, even if other {{elastic-endpoint}} features require them.

    ::::{important}
    Disabling the monitoring of asynchronous image load events may negatively impact the functionality of other {{elastic-endpoint}} features.
    ::::


`linux.advanced.kernel.capture_mode`
:   Added in 8.2.0.

    *Control whether kprobes or eBPF are used to gather data. Options are `kprobe`, `ebpf`, or `auto`. `auto` uses eBPF if possible, otherwise it uses kprobe. Default: `auto`.*

    On Linux, {{elastic-endpoint}} can monitor system events using kprobes or eBPF. By default, {{elastic-endpoint}} automatically chooses the best option, but you can use this setting to override that behavior.


`[mac,windows].advanced.kernel.connect`
:   Added in 7.9.0.

    *Control whether to connect to the kernel driver. Warning: disabling this will break most features. Default: `true`.*

    On macOS, {{elastic-endpoint}} uses a system extension, and on Windows, a kernel driver. Use this setting to disable {{elastic-endpoint}}'s attempt to connect to those subsystems. 

    :::{warning}
    Disabling the connection will break many {{elastic-endpoint}} features.
    :::


`windows.advanced.kernel.dev_drives.harden`
:   Added in 8.16.0.

    *Apply malware protection to dev drives. Default: `false`.*


`mac.advanced.kernel.fileaccess`
:   Added in 8.11.0.

    *Enable kernel file access events. `false` disables them even if they are needed by other features. Default: `true`.*

    Use this setting to disable file access events, even if other {{elastic-endpoint}} features require them.

    :::{warning}
    Disabling file access events may break other {{elastic-endpoint}} features.
    :::


`windows.advanced.kernel.fileopen`
:   Added in 7.9.0.

    *Enable kernel file open events. `false` disables them even if they are needed by other features. Default: `true`.*

    Use this setting to disable kernel file open events, even if other {{elastic-endpoint}} features require them.

    :::{warning}
    Disabling file open events may break other {{elastic-endpoint}} features.
    :::


`[mac,windows].advanced.kernel.filewrite`
:   Added in 7.9.0.

    *Enable kernel file write events. `false` disables them even if they are needed by other features. Default: `true`.*

    Use this setting to disable kernel file write events, even if other {{elastic-endpoint}} features require them.
    
    :::{warning}
    Disabling file write events may break other {{elastic-endpoint}} features.
    :::


`windows.advanced.kernel.filewrite_sync`
:   Added in 8.14.0.

    *Process file write notifications synchronously when possible. This may improve file write and malware-on-write enrichment reliability at the cost of system responsiveness. Default: `false`.*


`windows.advanced.kernel.image_and_process_file_timestamp`
:   Added in 8.4.0.

    *Collect executable/dll timestamps for process and asynchronous image load events. Default: `true`.*


`[mac,windows].advanced.kernel.network`
:   Added in 7.9.0.

    *Enable kernel network events. `false` disables them even if they are needed by other features. Default: `true`.*

    Use this setting to disable kernel network events, even if other {{elastic-endpoint}} features require them.
    
    :::{warning}
    Disabling network events may break other {{elastic-endpoint}} features.
    :::


`mac.advanced.kernel.network_extension.enable_content_filtering`
:   Added in 8.1.0.

    *Enable the network content filter, which will enable network eventing. Warning: host isolation will fail if this is disabled. Default: `true`.*

    Use this setting to enable or disable the macOS network content filter.
    
    :::{warning}
    Disabling the network content filter will break other {{elastic-endpoint}} features.
    :::


`mac.advanced.kernel.network_extension.enable_packet_filtering`
:   Added in 8.1.0.

    *Enable the network packet filter. Warning: host isolation will fail if this is disabled. Default: `true`.*

    Use this setting to enable or disable the macOS network packet filter.
    
    :::{warning}
    Disabling the network packet filter will break other {{elastic-endpoint}} features.
    :::


`windows.advanced.kernel.network_report_loopback`
:   Added in 8.15.0.

    *Report loopback network events. Default: `true`.*

    Use this setting to control whether {{elastic-endpoint}} reports localhost and loopback network events through its kernel component.

    :::{warning}
    Disabling localhost and loopback network events will reduce some system visibility, such as inter-process communication.
    :::


`windows.advanced.kernel.ppl.harden_am_images`
:   Added in 8.9.0.

    *Apply the `windows.advanced.kernel.ppl.harden_images` mitigation to Anti-Malware PPL as well. Disable this if third-party Anti-Malware is blocked from loading DLLs over the network. If this happens, there will be Event ID 8 events in the `Microsoft-Windows-Security-Mitigations/Kernel Mode` event log. Default: `true`.*


`windows.advanced.kernel.ppl.harden_images`
:   Added in 8.9.0.

    *Mitigate attacks like PPLFault by preventing Protected Process Light (PPL) processes from loading DLLs over the network. Default: `true`.*.


`[mac,windows].advanced.kernel.process`
:   Added in 7.9.0.

    *Enable kernel process events. `false` disables them even if they are needed by other features. Default: `true`.*

    Use this setting to disable kernel process events, even if other {{elastic-endpoint}} features require them.
    
    :::{warning}
    Disabling process events may break other {{elastic-endpoint}} features.
    :::


`windows.advanced.kernel.process_handle`
:   Added in 8.1.0.

    *Enable process and thread handle events. `false` disables them even if they are needed by other features. Default: `true`.*

    Use this setting to disable process and thread handle events, even if other {{elastic-endpoint}} features require them.
    
    :::{warning}
    Disabling process and thread handle events may break other {{elastic-endpoint}} features.
    :::


`windows.advanced.kernel.registry`
:   Added in 7.9.0.

    *Enable kernel registry events. `false` disables them even if they are needed by other features. Default: `true`.*

    Use this setting to disable registry modification events, even if other {{elastic-endpoint}} features require them.
    
    :::{warning}
    Disabling registry modification events may break other {{elastic-endpoint}} features.
    :::


`windows.advanced.kernel.registryaccess`
:   Added in 7.15.0.

    *Report limited registry access (`queryvalue`, `savekey`) events. Additional paths can be monitored via `windows.advanced.events.event_on_access.registry_paths`. Default: `true`.*


`windows.advanced.kernel.syncimageload`
:   Added in 7.9.0.

    *Enable kernel sync image load events. `false` disables them even if they are needed by other features. Default: `true`.*

    Use this setting to disable synchronous image load events, even if other {{elastic-endpoint}} features require them.
    
    :::{warning}
    Disabling synchronous image load events may break other {{elastic-endpoint}} features.
    :::


`windows.advanced.logging.debugview`
:   Added in 7.11.0.

    *Write logs to the DebugView Sysinternals tool. Allowed values are `error`, `warning`, `info`, `debug`, and `trace`. Default: none.*

    Use this setting to send {{elastic-endpoint}} logs to DebugView alongside other logging targets, such as the default file-based logging.


`[linux,mac,windows].advanced.logging.file`
:   Added in 7.11.0.

    *Override the log level configured for logs that are saved to disk and streamed to {{es}}. Elastic recommends using {{fleet}} to change this logging setting in most circumstances. Allowed values are `error`, `warning`, `info`, `debug`, and `trace`. Default: {{fleet}} configuration is used.*

    Use this setting to override the {{fleet}}-controlled file-based log level log level.


`[linux,mac].advanced.logging.syslog`
:   Added in 7.11.0.

    *Write logs to syslog. Allowed values are `error`, `warning`, `info`, `debug`, and `trace`. Default: none.*

    Use this setting to send {{elastic-endpoint}} logs to syslog alongside other logging targets, such as the default file-based logging.


`[linux,mac,windows].advanced.malware.max_file_size_bytes`
:   Added in 8.16.4.

    *Control the maximum file size in bytes that should be evaluated for malware. Default: `78643200`.*

    At the cost of performance overhead, increase the maximum file size {{elastic-endpoint}} will scan for malware.


`windows.advanced.malware.networkshare`
:   Added in 8.9.0.

    *Apply malware protection to network drives. Default: `true`.*


`[linux,mac,windows].advanced.malware.quarantine`
:   Added in 7.9.0 (macOS and Windows), 7.14.0. (Linux).

    *Enable quarantining files when malware prevention is enabled. Default: `true`.*

    Disabling quarantine will prevent malicious files from running but allow further user access to the files.


`[mac,windows].advanced.malware.threshold`
:   Added in 7.11.0.

    *Control the threshold that should be used for evaluating malware. Allowed values are `normal`, `conservative`, and `aggressive`. Default: `normal`.*

    Malware protection includes a machine learning model. Use this setting to modify the aggressiveness of that model.

    Changing the threshold will affect detection efficacy and result in true and false positive and negative rates outside of the model's optimized range.


`linux.advanced.memory_protection.enable_fork_scan`
:   Added in 8.14.0.

    *Enable memory scanning on process fork events. This will have the effect of more memory regions being scanned. Default: `true`.*


`linux.advanced.memory_protection.enable_shared_dirty_scan`
:   Added in 8.14.0.

    *Instead of ignoring regions with just no `Private_Dirty` bytes, ignore regions with the combination of no `Private_Dirty` bytes, no `Shared_Dirty` bytes and is file-backed. This has the effect of scanning more memory regions because of the loosened restrictions. Default: `true`.*


`[linux,mac,windows].advanced.memory_protection.memory_scan`
:   Added in 7.15.0 (Windows), 7.16.0 (macOS and Linux).

    *Enable scanning for malicious memory regions as a part of memory protection. Default: `true`.*

    Use this setting to disable memory scanning using YARA rules, even if Memory Threat protection is enabled. On Windows, Memory Threat protection will remain effective even without this scan. On macOS and Linux, disabling this scan will effectively disable Memory Threat protection. 


`[linux,mac,windows].advanced.memory_protection.memory_scan_collect_sample`
:   Added in 7.15.0 (Windows), 7.16.0 (macOS and Linux).

    *Collect 4MB of memory surrounding detected malicious memory regions. Warning: enabling this value may significantly increase the amount of data stored in {{es}}. Default: `false`.*

    Use this setting to collect memory surrounding detected malicious regions when Memory Threat alerts are triggered by YARA rule scanning.


`windows.advanced.memory_protection.scan_on_api_event`
:   Added in 8.17.6.

    *Scan for memory threats in response to API events. Default: `true`.*


`[linux,mac,windows].advanced.memory_protection.scan_on_image_load_event`
:   Added in 8.17.6.

    *Scan for memory threats in response to image loads. Default: `true`.*


`[linux,mac,windows].advanced.memory_protection.scan_on_network_event`
:   Added in 8.17.6.

    *Scan for memory threats in response to network activity. Default: `true`.*


`windows.advanced.memory_protection.shellcode`
:   Added in 7.15.0.

    *Enable shellcode injection detection as a part of memory protection. Default: `true`.*

    Use this setting to disable scanning memory for shellcode, even if Memory Threat protection is enabled. Memory Threat protection remains effective even without this scan.


`windows.advanced.memory_protection.shellcode_collect_sample`
:   Added in 7.15.0.

    *Collect 4MB of memory surrounding detected shellcode regions. Warning: enabling this value may significantly increase the amount of data stored in {{es}}. Default: `false`.*

    Use this setting to collect memory surrounding detected shellcode regions when Memory Threat alerts are triggered by shellcode scanning.


`windows.advanced.memory_protection.shellcode_enhanced_pe_parsing`
:   Added in 7.15.0.

    *Attempt to identify and extract PE metadata from injected shellcode, including Authenticode signatures and version resource information. Default: `true`.*


`windows.advanced.memory_protection.shellcode_trampoline_detection`
:   Added in 8.1.0.

    *Enable trampoline-based shellcode injection detection as a part of memory protection. Default: `true`.*

    Use this setting to disable scanning memory for trampolines, even if Memory Threat protection is enabled. Memory Threat protection will remain effective even without this scan.


`[linux,mac,windows].advanced.network_events_exclude_local`
:   Added in 8.10.1.

    *Exclude local connections from network events. Default: `false`.*


`windows.advanced.ransomware.canary`
:   Added in 7.14.0.

    *Enable ransomware canary protection. Default: `true`.*

    Use this setting to disable ransomware detection based on canary files, even if ransomware protection is enabled. Ransomware protection will remain effective even when this ransomware detection is disabled.


`mac.advanced.ransomware.diagnostic`
:   Added in 9.2.0.

    *Enable diagnostic ransomware protection. Default: `true`.*


`windows.advanced.ransomware.dump_process`
:   Added in 8.11.0.

    *Enable the generation of a memory dump of the ransomware process. This is ignored if the canary protection is off. Default: `true`.*


`windows.advanced.ransomware.mbr`
:   Added in 7.12.0.

    *Enable ransomware MBR protection. Default: `true`.*

    Use this setting to disable ransomware detection using Master Boot Record monitoring, even if ransomware protection is enabled. Ransomware protection will remain effective even when this ransomware detection is disabled.


`[linux,mac,windows].advanced.set_extended_host_information`
:   Added in 8.16.0.

    *Include full `host.*` fieldset information in events. When `false`, only `id`, `name`, and `os` are included. Warning: `true` will increase event size. Default: <=8.17: `true`, >=8.18: `false`.*

    {{elastic-endpoint}} only includes minimal information in the host fieldset in each event. Use this setting to also include extended information from the `alerts` and `metrics-*` documents. This setting was made available in 8.16; starting with 8.18, this behavior is disabled by default. Prior to 8.16, full `host` information was always included.


`linux.advanced.tty_io.max_event_interval_seconds`
:   Added in 8.5.0.

    *The maximum amount of time (seconds) to batch terminal output in a single event. Default: `30`.*


`linux.advanced.tty_io.max_kilobytes_per_event`
:   Added in 8.5.0.

    *The maximum kilobytes of terminal output to record in a single event. Default: `512`.*


`linux.advanced.tty_io.max_kilobytes_per_process`
:   Added in 8.5.0.

    *The maximum kilobytes of terminal output to record for a single process. Default: `512`.*


`linux.advanced.utilization_limits.cpu`
:   Added in 8.3.0.

    *The percentage of the aggregate system CPU to which Endpoint is restricted. The range is `20`-`100%`. Values under `20` are ignored and trigger a policy warning. Default: `50`.*
 
    :::{important}
    Setting the limit too low will impact system performance, since {{elastic-endpoint}} pauses application loads during malware scans.
    :::


`windows.advanced.utilization_limits.resident_memory_target_mb`
:   Added in 8.12.0.

    *Control how much memory (in MB) should be kept resident in RAM. This setting affects Private Working Set but does not affect the amount of virtual memory requested from the OS (Private Bytes or Commit Charge). If plenty of unused RAM is available, Windows may give {{elastic-endpoint}} more RAM than requested to reduce unnecessary paging and improve performance. If the current {{elastic-defend}} configuration requires regularly touching more than the requested amount of memory, then the Private Working Set will be higher than requested here. The minimum value is 50. Default: `200`.*
