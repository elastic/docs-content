---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/endpoint-event-capture.html
  - https://www.elastic.co/guide/en/serverless/current/security-endpoint-event-capture.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Event capture and {{elastic-defend}} [endpoint-event-capture]

{{elastic-defend}} collects selective data on system activities in order to detect and prevent as many threats as possible, while balancing storage and performance overhead. To that end, {{elastic-defend}} isn’t designed to provide a complete capture of all system events. The event data that {{elastic-defend}} generates might be aggregated, truncated, or deduplicated as needed to optimize threat detection and prevention.

You can supplement {{elastic-defend}}'s protection capabilities with additional [Elastic integrations](https://docs.elastic.co/en/integrations) and tools that provide more visibility and historical data. Consult the following sections to learn what {{elastic-defend}} collects for specific system events and how to expand data collection.


## Network port creation and deletion [_network_port_creation_and_deletion]

{{elastic-defend}} tracks TCP connections. If a port is created but no traffic flows, no events are generated.

For complete capture of network port creation and deletion, consider capturing Windows event ID 5158 using the [Custom Windows Event Logs](https://docs.elastic.co/en/integrations/winlog) integration.


## Network in/out connections [_network_inout_connections]

{{elastic-defend}} tracks TCP connections, which don’t include network in/out connections.

For complete network capture, consider deploying {{packetbeat}} using the [Network Packet Capture](https://docs.elastic.co/en/integrations/network_traffic) integration.


## User behavior [_user_behavior]

{{elastic-defend}} collects a selected set of user security events to support threat detection and prevention. It doesn't capture every user event, and the events it collects vary by operating system.

On Windows, {{elastic-defend}} collects the following events from the Windows Security event log and stores them in the `logs-endpoint.events.security-*` data stream. Windows records these events only when the corresponding audit policy is enabled on the host.

| Windows event ID | Description |
| --- | --- |
| 4624 | An account was successfully logged on. |
| 4625 | An account failed to log on. |
| 4634 | An account was logged off. |
| 4648 | A logon was attempted using explicit credentials. |
| 4672 | Special privileges were assigned to a new logon. |
| 4720 {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | A user account was created. |
| 4800 | The workstation was locked. |
| 4801 | The workstation was unlocked. |
| 5382 {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | Vault credentials were read. |

{{elastic-defend}} doesn't collect other user-related events, such as user account deletion or modification. To collect these events, use the [Custom Windows Event Logs](integration-docs://reference/winlog/index.md) integration.


## System service registration, deletion, and modification [_system_service_registration_deletion_and_modification]

{{elastic-defend}} only captures system service security events required by its behavioral protection engine.

On Windows, {{elastic-defend}} collects the following event from the Windows Security event log and stores it in the `logs-endpoint.events.security-*` data stream. Windows records this event only when the corresponding audit policy is enabled on the host.

| Windows event ID | Description |
| --- | --- |
| 4697 {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | A service was installed in the system. |

Service creation and modification can also be detected in registry activity, for which {{elastic-defend}} has internal rules such as [Registry or File Modification from Suspicious Memory](https://github.com/elastic/protections-artifacts/blob/6d54ae289b290b1d42a7717569483f6ce907200a/behavior/rules/persistence_registry_or_file_modification_from_suspicious_memory.toml).

For complete capture of all or specific Windows security events, consider the [Custom Windows Event Logs](integration-docs://reference/winlog/index.md) integration.


## Scheduled task creation and modification [_scheduled_task_creation_and_modification]

{{elastic-defend}} only captures scheduled task security events required by its behavioral protection engine.

On Windows, {{elastic-defend}} collects the following events from the Windows Security event log and stores them in the `logs-endpoint.events.security-*` data stream. Windows records these events only when the corresponding audit policy is enabled on the host.

| Windows event ID | Description |
| --- | --- |
| 4698 {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | A scheduled task was created. |
| 4702 {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | A scheduled task was updated. |

For complete capture of all or specific Windows security events, consider the [Custom Windows Event Logs](integration-docs://reference/winlog/index.md) integration.


## Windows API calls [_windows_api_calls]

On Windows, {{elastic-defend}} monitors calls to sensitive Windows APIs that malware commonly abuses, and stores selected calls as API events in the `logs-endpoint.events.api-*` data stream. The name of the called API is stored in the `process.Ext.api.name` field.

{{elastic-defend}} doesn't generate an event for every call to a monitored API. Events are generated only under certain conditions. Also, some API events aren't sent to {{es}} by default. To send these events to {{es}}, set the [`windows.advanced.events.api_verbose`](/reference/security/defend-advanced-settings.md) advanced policy setting to `true`.

:::{dropdown} Monitored Windows APIs
* `AmsiScanBuffer`
* `connect`
* `CreateProcessAsUserA` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `CreateProcessAsUserW` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `CreateProcessWithLogonW` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `CreateProcessWithTokenW` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `DeviceIoControl`
* `GetAsyncKeyState`
* `ImpersonateLoggedOnUser` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `ImpersonateNamedPipeClient` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `INetFwRules::Add` {applies_to}`stack: ga 9.2+` {applies_to}`serverless: ga`
* `InternetOpenUrl` {applies_to}`stack: ga 9.3+` {applies_to}`serverless: ga`
* `IoCreateDevice`
* `IWbemServices` methods (WMI operations)
* `IWbemServices::PutInstance` for WMI permanent event subscription creation
* `ldap_search` {applies_to}`stack: ga 9.2+` {applies_to}`serverless: ga`
* `MapViewOfFile`
* `MapViewOfFile2`
* `NtCreateProcess` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `NtCreateProcessEx` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `NtCreateUserProcess` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `NtFsControlFile` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `NtQueueApcThread`
* `NtSetInformationThread` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `NtSuspendProcess`
* `OpenProcess`
* `OpenThread`
* `QueueUserAPC`
* `ReadProcessMemory`
* `RegisterRawInputDevices`
* `SetThreadContext`
* `SetThreadToken` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `SetWindowsHookEx`
* `SuspendThread`
* `TpAllocWork` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `TpCallbackStart` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
* `VirtualAlloc`
* `VirtualAllocEx`
* `VirtualProtect`
* `VirtualProtectEx`
* `WinHttpOpenRequest` {applies_to}`stack: ga 9.3+` {applies_to}`serverless: ga`
* `Wow64SetThreadContext`
* `WriteProcessMemory`
:::

For some API events, `process.Ext.api.name` might contain the API that called the monitored API, rather than the monitored API itself.


## Kernel driver registration, deletion, and queries [_kernel_driver_registration_deletion_and_queries]

{{elastic-defend}} scans every driver as it is loaded, but it doesn’t generate an event each time.

Drivers are registered in the system as system services. You can capture this with Windows event ID 4697 using the [Custom Windows Event Logs](https://docs.elastic.co/en/integrations/winlog) integration.

Also consider capturing Windows event ID 6 using {{winlogbeat}}'s [Sysmon module](beats://reference/winlogbeat/winlogbeat-module-sysmon.md).


## System configuration file creation, modification, and deletion [_system_configuration_file_creation_modification_and_deletion]

{{elastic-defend}} tracks creation, modification, and deletion of all files on the system. However, as mentioned above, the data might be aggregated, truncated, or deduplicated to provide only what’s required for threat detection and prevention.

