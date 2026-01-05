---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/d4c-policy-guide.html
applies_to:
  stack: beta 9.3
  serverless:
    security: beta
---

# Container workload protection policies [d4c-policy-guide]

To unlock the full functionality of the Defend for Containers (D4C) integration, you’ll need to understand its policy syntax. This enables you to construct policies that precisely allow expected container behaviors and prevent unexpected behaviors—thereby hardening your container workloads' security posture.

D4C integration policies consist of *selectors* and *responses*. Each policy must contain at least one selector and one response. Currently, the system supports two types of selectors and responses: `file` and `process`. Selectors define which system operations to match and can include multiple conditions (grouped using a logical `AND`) to precisely select events. Responses define which actions to take when a system operation matches the conditions specified in an associated selector.

The default policy described on this page provides an example that’s useful for understanding D4C policies in general. Following the description, you’ll find a comprehensive glossary of selector conditions, response fields, and actions.


## Default policies: [d4c-default-policies]

The default D4C integration policy includes two selector-response pairs. It is designed to implement core container workload protection capabilities:

* **Threat Detection:** The first selector-response pair is designed to stream process telemetry data to your {{es}} cluster so {{elastic-sec}} can evaluate it to detect threats. Both the selector and response are named `allProcesses`. The selector selects all fork and exec events. The associated response specifies that selected events should be logged.
* **Drift Detection & Prevention:** The second selector-response pair is designed to create alerts when container drift is detected. Both the selector and response are named `executableChanges`. The selector selects all `createExecutable` and `modifyExecutable` events. The associated response specifies that the selected events should create alerts, which will be sent to your {{es}} cluster. You can modify the response to block drift operations by setting it to block.

:::{image} /solutions/images/security-d4c-policy-editor.png
:alt: The defend for containers policy editor with the default policies
:::


## Selectors [d4c-selectors-glossary]

A selector requires a name and at least one operation. It will select all events of the specified operation types, unless you also include *conditions* to narrow down the selection. Some conditions are available for both `file` and `process` selectors, while others only available for one type of selector.


### Common conditions [_common_conditions]

These conditions are available for both `file` and `process` selectors.

| Name | Description |
| --- | --- |
| containerImageFullName | A list of full container image names to match on. For example: `docker.io/nginx`. |
| containerImageName | A list of container image names to match on. For example: `nginx`. |
| containerImageTag | A list of container image tags to match on. For example: `latest`. |
| kubernetesClusterId | A list of Kubernetes cluster IDs to match on. For consistency with KSPM, the `kube-system` namespace’s UID is used as a cluster ID. |
| kubernetesClusterName | A list of Kubernetes cluster names to match on. |
| kubernetesNamespace | A list of Kubernetes namespaces to match on. |
| kubernetesPodName | A list of Kubernetes pod names to match on. Trailing wildcards supported. |
| kubernetesPodLabel | A list of resource labels. Trailing wildcards supported (value only), for example: `key1:val*`. |


### File-selector conditions [_file_selector_conditions]

These conditions are available only for `file` selectors.

| Name | Description |
| --- | --- |
| operation | The list of system operations to match on. Options include `createExecutable`, `modifyExecutable`, `createFile`, `modifyFile`, `deleteFile`. |
| ignoreVolumeMounts | If set, ignores file operations on *all* volume mounts. |
| ignoreVolumeFiles | If set, ignores operations on file mounts only. For example: mounted files, `configMaps`, and secrets. |
| targetFilePath | A list of file paths to include. Paths are absolute and wildcards are supported. The `*` wildcard matches any sequence of characters within a single directory, while the `**` wildcard matches any sequence of characters across multiple directories and subdirectories. |

::::{note}
In order to ensure precise targeting of file integrity monitoring operations, a `TargetFilePath` is required whenever the `deleteFile`, `modifyFile`, or `createFile` operations are used within a selector.
::::



### Process-selector conditions [_process_selector_conditions]

These conditions are available only for `process` selectors.

| Name | Description |
| --- | --- |
| operation | The list of system operations to match on. Options include `fork` and `exec`. |
| processExecutable | A list of executables (full path included) to match on. For example: `/usr/bin/cat`. Wildcard support is same as targetFilePath above. |
| processName | A list of process names (executable basename) to match on. For example: `bash`, `vi`, `cat`. |
| sessionLeaderInteractive | If set to `true`, will only match on interactive sessions (defined as sessions with a controlling TTY). |


### Response fields [_response_fields]

A policy can include one or more responses. Each response is comprised of the following fields:

| Field | Description |
| --- | --- |
| match | An array of one or more selectors of the same type (`file` or `process`). |
| exclude | Optional. An array of one or more selectors to use as exclusions to everything in `match`. |
| actions | An array of actions to perform when at least one `match` selector matches and none of the `exclude` selectors match. Options include `log`, `alert`, and `block`. |


### Response actions [_response_actions]

D4C responses can include the following actions:

| Action | Description |
| --- | --- |
| log | Sends events to the `logs-cloud_defend.file-*` data stream for file responses, and the `logs-cloud_defend.process-*` data stream for process responses. |
| alert | Writes events (file or process) to the logs-cloud_defend.alerts-* data stream. |
| block | Prevents the system operation from proceeding. This blocking action happens prior to the execution of the event. It is required that the alert action be set if block is enabled.<br><br>**Note:** Currently, block is only supported on file operations.<br> |