---
navigation_title: "add_docker_metadata"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_docker_metadata-processor.html
---

# Add Docker metadata [add_docker_metadata-processor]


::::{tip}
Inputs that collect logs and metrics use this processor by default, so you do not need to configure it explicitly.
::::


The `add_docker_metadata` processor annotates each event with relevant metadata from Docker containers. At startup the processor detects a Docker environment and caches the metadata.

For events to be annotated with Docker metadata, the configuration must be valid, and the processor must be able to reach the Docker API.

Each event is annotated with:

* Container ID
* Name
* Image
* Labels

::::{note}
When running {{agent}} in a container, you need to provide access to Docker’s unix socket in order for the `add_docker_metadata` processor to work. You can do this by mounting the socket inside the container. For example:

`docker run -v /var/run/docker.sock:/var/run/docker.sock ...`

To avoid privilege issues, you may also need to add `--user=root` to the `docker run` flags. Because the user must be part of the Docker group in order to access `/var/run/docker.sock`, root access is required if {{agent}} is running as non-root inside the container.

If the Docker daemon is restarted, the mounted socket will become invalid, and metadata will stop working. When this happens, you can do one of the following:

* Restart {{agent}} every time Docker is restarted
* Mount the entire `/var/run` directory (instead of just the socket)

::::



## Example [_example_4]

```yaml
  - add_docker_metadata:
      host: "unix:///var/run/docker.sock"
      #match_fields: ["system.process.cgroup.id"]
      #match_pids: ["process.pid", "process.parent.pid"]
      #match_source: true
      #match_source_index: 4
      #match_short_id: true
      #cleanup_timeout: 60
      #labels.dedot: false
      # To connect to Docker over TLS you must specify a client and CA certificate.
      #ssl:
      #  certificate_authority: "/etc/pki/root/ca.pem"
      #  certificate:           "/etc/pki/client/cert.pem"
      #  key:                   "/etc/pki/client/cert.key"
```


## Configuration settings [_configuration_settings_3]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `host` | No | `unix:///var/run/docker.sock` | Docker socket (UNIX or TCP socket). |
| `ssl` | No |  | SSL configuration to use when connecting to the Docker socket. For a list ofavailable settings, refer to [SSL/TLS](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md), specificallythe settings under [Table 7, Common configuration options](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md#common-ssl-options) and [Table 8, Client configuration options](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md#client-ssl-options). |
| `match_fields` | No |  | List of fields to match a container ID. At least one of the fields most hold a container ID to get the event enriched. |
| `match_pids` | No | `["process.pid", "process.parent.pid"]` | List of fields that contain process IDs. If the process is running in Docker, the event will be enriched. |
| `match_source` | No | `true` | Whether to match the container ID from a log path present in the `log.file.path` field. |
| `match_short_id` | No | `false` | Whether to match the container short ID from a log path present in the `log.file.path` field. This setting allows you to match directory names that have the first 12 characters of the container ID. For example, `/var/log/containers/b7e3460e2b21/*.log`. |
| `match_source_index` | No | `4` | Index in the source path split by a forward slash (`/`) to find the container ID. For example, the default, `4`, matches the container ID in `/var/lib/docker/containers/<container_id>/*.log`. |
| `cleanup_timeout` | No | `60s` | Time of inactivity before container metadata is cleaned up and forgotten. |
| `labels.dedot` | No | `false` | Whether to replace dots (`.`) in labels with underscores (`_`). |

