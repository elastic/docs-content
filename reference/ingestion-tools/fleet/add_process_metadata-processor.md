---
navigation_title: "add_process_metadata"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_process_metadata-processor.html
---

# Add process metadata [add_process_metadata-processor]


The `add_process_metadata` processor enriches events with information from running processes, identified by their process ID (PID).


## Example [_example_11]

```yaml
  - add_process_metadata:
      match_pids: [system.process.ppid]
      target: system.process.parent
```

The fields added to the event look as follows:

```json
"process": {
  "name":  "systemd",
  "title": "/usr/lib/systemd/systemd --switched-root --system --deserialize 22",
  "exe":   "/usr/lib/systemd/systemd",
  "args":  ["/usr/lib/systemd/systemd", "--switched-root", "--system", "--deserialize", "22"],
  "pid":   1,
  "parent": {
    "pid": 0
  },
  "start_time": "2018-08-22T08:44:50.684Z",
  "owner": {
    "name": "root",
    "id": "0"
  }
},
"container": {
  "id": "b5285682fba7449c86452b89a800609440ecc88a7ba5f2d38bedfb85409b30b1"
},
```

Optionally, the process environment can be included, too:

```json
  ...
  "env": {
    "HOME":       "/",
    "TERM":       "linux",
    "BOOT_IMAGE": "/boot/vmlinuz-4.11.8-300.fc26.x86_64",
    "LANG":       "en_US.UTF-8",
  }
  ...
```


## Configuration settings [_configuration_settings_13]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `match_pids` | Yes |  | List of fields to lookup for a PID. The processor searches the list sequentially until the field is found in the current event, and the PID lookup is then applied to the value of this field. |
| `target` | No | event root | Destination prefix where the `process` object will be created. |
| `include_fields` | No |  | List of fields to add. By default, adds all available fields except `process.env`. |
| `ignore_missing` | No | `true` | Whether to ignore missing fields. If `false`, discards events that don’t contain any of the fields specified in `match_pids` and then generates an error. If `true`, missing fields are ignored. |
| `overwrite_keys` | No | `false` | Whether to overwrite existing keys. If `false` and a target field already exists, it is not, overwritten, and an error is logged. If `true`, the target field is overwritten. |
| `restricted_fields` | No | `false` | Whether to output restricted fields. If `false`, to avoid leaking sensitive data, the `process.env` field is not output. If `true`, the field will be present in the output. |
| `host_path` | No | root directory (`/`) of host | Host path where `/proc` is mounted. For different runtime configurations of Kubernetes or Docker, set the `host_path` to overwrite the default. |
| `cgroup_prefixes` | No | `/kubepods` and `/docker` | Prefix where the container ID is inside cgroup. For different runtime configurations of Kubernetes or Docker, set `cgroup_prefixes` to overwrite the defaults. |
| `cgroup_regex` | No |  | Regular expression with capture group for capturing the container ID from the cgroup path. For example:<br><br>1. `^\/.+\/.+\/.+\/([0-9a-f]{{64}}).*` matches the container ID of a cgroup like `/kubepods/besteffort/pod665fb997-575b-11ea-bfce-080027421ddf/b5285682fba7449c86452b89a800609440ecc88a7ba5f2d38bedfb85409b30b1`<br>2. `^\/.+\/.+\/.+\/docker-([0-9a-f]{{64}}).scope` matches the container ID of a cgroup like `/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod69349abe_d645_11ea_9c4c_08002709c05c.slice/docker-80d85a3a585f1575028ebe468d83093c301eda20d37d1671ff2a0be50fc0e460.scope`<br>3. `^\/.+\/.+\/.+\/crio-([0-9a-f]{{64}}).scope` matches the container ID of a cgroup like `/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod69349abe_d645_11ea_9c4c_08002709c05c.slice/crio-80d85a3a585f1575028ebe468d83093c301eda20d37d1671ff2a0be50fc0e460.scope`<br><br>If `cgroup_regex` is not set, the container ID is extracted from the cgroup file based on the `cgroup_prefixes` setting.<br> |
| `cgroup_cache_expire_time` | No | `30s` | Time in seconds before cgroup cache elements expire. To disable the cgroup cache, set this to `0`. In some container runtime technologies, like runc, the container’s process is also a process in the host kernel and will be affected by PID rollover/reuse. Set the expire time to a value that is smaller than the PIDs wrap around time to avoid the wrong container ID. |

