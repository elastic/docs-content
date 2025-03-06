---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-container.html
---

# Run Elastic Agent in a container [elastic-agent-container]

You can run {{agent}} inside a container — either with {{fleet-server}} or standalone. Docker images for all versions of {{agent}} are available from the [Elastic Docker registry](https://www.docker.elastic.co/r/elastic-agent/elastic-agent). If you are running in Kubernetes, refer to [run {{agent}} on ECK](/deploy-manage/deploy/cloud-on-k8s/standalone-elastic-agent.md).

Note that running {{elastic-agent}} in a container is supported only in Linux environments. For this reason we don’t currently provide {{agent}} container images for Windows.

Considerations:

* When {{agent}} runs inside a container, it cannot be upgraded through {{fleet}} as it expects that the container itself is upgraded.
* Enrolling and running an {{agent}} is usually a two-step process. However, this doesn’t work in a container, so a special subcommand, `container`, is called. This command allows environment variables to configure all properties, and runs the `enroll` and `run` commands as a single command.


## What you need [_what_you_need]

* [Docker installed](https://docs.docker.com/get-docker/).
* {{es}} for storing and searching your data, and {{kib}} for visualizing and managing it.

   ::::{tab-set}

   :::{tab-item} {{ech}}
   To get started quickly, spin up an [{{ech}}](https://www.elastic.co/cloud/elasticsearch-service) deployment. {{ech}} is available on AWS, GCP, and Azure. [Try it out for free](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
   :::

   :::{tab-item} Self-managed
   To install and run {{es}} and {{kib}}, see [Installing the {{stack}}](/deploy-manage/deploy/self-managed/deploy-cluster.md).
   :::

   ::::

## Step 1: Pull the image [_step_1_pull_the_image]

There are two images for Elastic Agent, elastic-agent and elastic-agent-complete. The elastic-agent image contains all the binaries for running Beats, while the elastic-agent-complete image contains these binaries plus additional dependencies to run browser monitors through Elastic Synthetics. Refer to [Synthetic monitoring via Elastic Agent and Fleet](/solutions/observability/apps/get-started.md) for more information.

Run the `docker pull` command against the Elastic Docker registry:

```terminal
docker pull docker.elastic.co/elastic-agent/elastic-agent:9.0.0-beta1
```

Alternately, you can use the hardened [Wolfi](https://github.com/wolfi-dev/) image. Using Wolfi images requires Docker version 20.10.10 or later. For details about why the Wolfi images have been introduced, refer to our article [Reducing CVEs in Elastic container images](https://www.elastic.co/blog/reducing-cves-in-elastic-container-images).

```terminal
docker pull docker.elastic.co/elastic-agent/elastic-agent-wolfi:9.0.0-beta1
```

If you want to run Synthetics tests, run the docker pull command to fetch the elastic-agent-complete image:

```terminal
docker pull docker.elastic.co/elastic-agent/elastic-agent-complete:9.0.0-beta1
```
To run Synthetics tests using the hardened [Wolfi](https://github.com/wolfi-dev/) image, run:

```terminal
docker pull docker.elastic.co/elastic-agent/elastic-agent-complete-wolfi:9.0.0-beta1
```

## Step 2: Optional: Verify the image [_step_2_optional_verify_the_image]

Although it’s optional, we highly recommend verifying the signatures included with your downloaded Docker images to ensure that the images are valid.

Elastic images are signed with Cosign which is part of the [Sigstore](https://www.sigstore.dev) project. Cosign supports container signing, verification, and storage in an OCI registry. Install the appropriate Cosign application for your operating system.

Run the following commands to verify the **elastic-agent** container image signature for Elastic Agent v9.0.0-beta1:

```terminal
wget https://artifacts.elastic.co/cosign.pub <1>
cosign verify --key cosign.pub docker.elastic.co/elastic-agent/elastic-agent:9.0.0-beta1 <2>
```
1. Download the Elastic public key to verify container signature
2. Verify the container against the Elastic public key

If you’re using the elastic-agent-complete image, run the commands as follows:

```terminal
wget https://artifacts.elastic.co/cosign.pub
cosign verify --key cosign.pub docker.elastic.co/elastic-agent/elastic-agent-complete:9.0.0-beta1
```
The command prints the check results and the signature payload in JSON format, for example:

```terminal
Verification for docker.elastic.co/elastic-agent/elastic-agent-complete:9.0.0-beta1 --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The signatures were verified against the specified public key
```

## Step 3: Get aware of the Elastic Agent container command [_step_3_get_aware_of_the_elastic_agent_container_command]

The Elastic Agent container command offers a wide variety of options. To see the full list, run:

```terminal
docker run --rm docker.elastic.co/elastic-agent/elastic-agent:9.0.0-beta1 elastic-agent container -h
```

## Step 4: Run the Elastic Agent image [_step_4_run_the_elastic_agent_image]


::::{tab-set}

:::{tab-item} Elastic Cloud

```terminal
docker run \
  --env FLEET_ENROLL=1 \ <1>
  --env FLEET_URL=<fleet-server-host-url> \ <2>
  --env FLEET_ENROLLMENT_TOKEN=<enrollment-token> \ <3>
  --rm docker.elastic.co/elastic-agent/elastic-agent:9.0.0-beta1 <4>
```

1. Set to 1 to enroll the {{agent}} into {{fleet-server}}.
2. URL to enroll the {{fleet-server}} into. You can find it in {{kib}}. Select **Management → {{fleet}} → Fleet Settings**, and copy the {{fleet-server}} host URL.
3. The token to use for enrollment. Close the flyout panel and select **Enrollment tokens**. Find the Agent policy you want to enroll {{agent}} into, and display and copy the secret token. To learn how to create a policy, refer to [Create an agent policy without using the UI](/reference/ingestion-tools/fleet/create-policy-no-ui.md).
4. If you want to run **elastic-agent-complete** image, replace `elastic-agent` to `elastic-agent-complete`. Use the `elastic-agent` user instead of root to run Synthetics Browser tests. Synthetic tests cannot run under the root user. Refer to [Synthetics {{fleet}} Quickstart](/solutions/observability/apps/get-started.md) for more information.

Refer to [Environment variables](/reference/ingestion-tools/fleet/agent-environment-variables.md) for all available options.
:::

:::{tab-item} Self-managed

If you’re running a self-managed cluster and want to run your own {{fleet-server}}, run the following command, which will spin up both {{agent}} and {{fleet-server}} in a container:

```terminal
docker run \
  --env FLEET_SERVER_ENABLE=true \ <1>
  --env FLEET_SERVER_ELASTICSEARCH_HOST=<elasticsearch-host> \ <2>
  --env FLEET_SERVER_SERVICE_TOKEN=<service-token> \ <3>
  --env FLEET_SERVER_POLICY_ID=<fleet-server-policy> \ <4>
  -p 8220:8220 \ <5>
  --rm docker.elastic.co/elastic-agent/elastic-agent:9.0.0-beta1 <6>
```

1. Set to 1 to bootstrap Fleet Server on this Elastic Agent.
2. Your cluster’s {{es}} host URL.
3. The {{fleet}} service token. [Generate one in the {{fleet}} UI](/reference/ingestion-tools/fleet/fleet-enrollment-tokens.md#create-fleet-enrollment-tokens) if you don’t have one already.
4. ID of the {{fleet-server}} policy. We recommend only having one fleet-server policy. To learn how to create a policy, refer to [Create an agent policy without using the UI](/reference/ingestion-tools/fleet/create-policy-no-ui.md).
5. publish container port 8220 to host.
6. If you want to run the **elastic-agent-complete** image, replace `elastic-agent` with `elastic-agent-complete`. Use the `elastic-agent` user instead of root to run Synthetics Browser tests. Synthetic tests cannot run under the root user. Refer to [Synthetics {{fleet}} Quickstart](/solutions/observability/apps/get-started.md) for more information.

Refer to [Environment variables](/reference/ingestion-tools/fleet/agent-environment-variables.md) for all available options.
:::

::::

If you need to run {{fleet-server}} as well, adjust the `docker run` command above by adding these environment variables:

```terminal
  --env FLEET_SERVER_ENABLE=true \ <1>
  --env FLEET_SERVER_ELASTICSEARCH_HOST=<elasticsearch-host> \ <2>
  --env FLEET_SERVER_SERVICE_TOKEN=<service-token> <3>
```

1. Set to `true` to bootstrap {{fleet-server}} on this {{agent}}. This automatically forces {{fleet}} enrollment as well.
2. The Elasticsearch host for Fleet Server to communicate with, for example `http://elasticsearch:9200`.
3. Service token to use for communication with {{es}} and {{kib}}.


:::{tip}
**Running {{agent}} on a read-only file system**

If you’d like to run {{agent}} in a Docker container on a read-only file system, you can do so by specifying the `--read-only` option. {{agent}} requires a stateful directory to store application data, so with the `--read-only` option you also need to use the `--mount` option to specify a path to where that data can be stored.

For example:

```bash
docker run --rm --mount source=$(pwd)/state,destination=/state -e {STATE_PATH}=/state --read-only docker.elastic.co/elastic-agent/elastic-agent:9.0.0-beta1 <1>
```

1. Where `{STATE_PATH}` is the path to a stateful directory to mount where {{agent}} application data can be stored.

You can also add `type=tmpfs` to the mount parameter (`--mount type=tmpfs,destination=/state...`) to specify a temporary file storage location. This should be done with caution as it can cause data duplication, particularly for logs, when the container is restarted, as no state data is persisted.

:::


## Step 5: View your data in {{kib}} [_step_5_view_your_data_in_kib]

1. Launch {{kib}}:

   ::::{tab-set}

   :::{tab-item} {{ech}}
   1. [Log in](https://cloud.elastic.co/) to your {{ecloud}} account.
   2. Navigate to the {{kib}} endpoint in your deployment.
   :::

   :::{tab-item} Self-managed
   Point your browser to [http://localhost:5601](http://localhost:5601), replacing `localhost` with the name of the {{kib}} host.
   :::

   ::::

2. To check if your {{agent}} is enrolled in {{fleet}}, go to **Management → {{fleet}} → Agents**.

    :::{image} images/kibana-fleet-agents.png
    :alt: {{agent}}s {{fleet}} page
    :class: screenshot
    :::

3. To view data flowing in, go to **Analytics → Discover** and select the index `metrics-*`, or even more specific, `metrics-kubernetes.*`. If you can’t see these indexes, [create a data view](/explore-analyze/find-and-organize/data-views.md) for them.
4. To view predefined dashboards, either select **Analytics→Dashboard** or [install assets through an integration](/reference/ingestion-tools/fleet/view-integration-assets.md).


## Docker compose [_docker_compose]

You can run {{agent}} in docker-compose. The example below shows how to enroll an {{agent}}:

```yaml
version: "3"
services:
  elastic-agent:
    image: docker.elastic.co/elastic-agent/elastic-agent:9.0.0-beta1 <1>
    container_name: elastic-agent
    restart: always
    user: root                                                       <2>
    environment:
      - FLEET_ENROLLMENT_TOKEN=<enrollment-token>
      - FLEET_ENROLL=1
      - FLEET_URL=<fleet-server-url>
```

1. Switch `elastic-agent` to `elastic-agent-complete` if you intend to use the complete version. Use the `elastic-agent` user instead of root to run Synthetics Browser tests. Synthetic tests cannot run under the root user. Refer to [Synthetics {{fleet}} Quickstart](/solutions/observability/apps/get-started.md) for more information.
2. Synthetic browser monitors require this set to `elastic-agent`.


If you need to run {{fleet-server}} as well, adjust the docker-compose file above by adding these environment variables:

```yaml
      - FLEET_SERVER_ENABLE=true
      - FLEET_SERVER_ELASTICSEARCH_HOST=<elasticsearch-host>
      - FLEET_SERVER_SERVICE_TOKEN=<service-token>
```

Refer to [Environment variables](/reference/ingestion-tools/fleet/agent-environment-variables.md) for all available options.


## Logs [_logs]

Since a container supports only a single version of {{agent}}, logs and state are stored a bit differently than when running an {{agent}} outside of a container. The logs can be found under: `/usr/share/elastic-agent/state/data/logs/*`.

It’s important to note that only the logs from the {{agent}} process itself are logged to `stdout`. Subprocess logs are not. Each subprocess writes its own logs to the `default` directory inside the logs directory:

```bash
/usr/share/elastic-agent/state/data/logs/default/*
```

::::{tip}
Running into errors with {{fleet-server}}? Check the fleet-server subprocess logs for more information.
::::

## Debugging [_debugging]

A monitoring endpoint can be enabled to expose resource usage and event processing data. The endpoint is compatible with {{agent}}s running in both {{fleet}} mode and Standalone mode.

Enable the monitoring endpoint in `elastic-agent.yml` on the host where the {{agent}} is installed. A sample configuration looks like this:

```yaml
agent.monitoring:
  enabled: true <1>
  logs: true <2>
  metrics: true <3>
  http:
      enabled: true <4>
      host: localhost <5>
      port: 6791 <6>
```

1. Enable monitoring of running processes.
2. Enable log monitoring.
3. Enable metrics monitoring.
4. Expose {{agent}} metrics over HTTP. By default, sockets and named pipes are used.
5. The hostname, IP address, Unix socket, or named pipe that the HTTP endpoint will bind to. When using IP addresses, we recommend only using `localhost`.
6. The port that the HTTP endpoint will bind to.


The above configuration exposes a monitoring endpoint at `http://localhost:6791/processes`.

::::{dropdown} `http://localhost:6791/processes` output
```json
{
   "processes":[
      {
         "id":"metricbeat-default",
         "pid":"36923",
         "binary":"metricbeat",
         "source":{
            "kind":"configured",
            "outputs":[
               "default"
            ]
         }
      },
      {
         "id":"filebeat-default-monitoring",
         "pid":"36924",
         "binary":"filebeat",
         "source":{
            "kind":"internal",
            "outputs":[
               "default"
            ]
         }
      },
      {
         "id":"metricbeat-default-monitoring",
         "pid":"36925",
         "binary":"metricbeat",
         "source":{
            "kind":"internal",
            "outputs":[
               "default"
            ]
         }
      }
   ]
}
```

::::


Each process ID in the `/processes` output can be accessed for more details.

::::{dropdown} `http://localhost:6791/processes/{{process-name}}` output
```json
{
   "beat":{
      "cpu":{
         "system":{
            "ticks":537,
            "time":{
               "ms":537
            }
         },
         "total":{
            "ticks":795,
            "time":{
               "ms":796
            },
            "value":795
         },
         "user":{
            "ticks":258,
            "time":{
               "ms":259
            }
         }
      },
      "info":{
         "ephemeral_id":"eb7e8025-7496-403f-9f9a-42b20439c737",
         "uptime":{
            "ms":75332
         },
         "version":"7.14.0"
      },
      "memstats":{
         "gc_next":23920624,
         "memory_alloc":20046048,
         "memory_sys":76104712,
         "memory_total":60823368,
         "rss":83165184
      },
      "runtime":{
         "goroutines":58
      }
   },
   "libbeat":{
      "config":{
         "module":{
            "running":4,
            "starts":4,
            "stops":0
         },
         "reloads":1,
         "scans":1
      },
      "output":{
         "events":{
            "acked":0,
            "active":0,
            "batches":0,
            "dropped":0,
            "duplicates":0,
            "failed":0,
            "toomany":0,
            "total":0
         },
         "read":{
            "bytes":0,
            "errors":0
         },
         "type":"elasticsearch",
         "write":{
            "bytes":0,
            "errors":0
         }
      },
      "pipeline":{
         "clients":4,
         "events":{
            "active":231,
            "dropped":0,
            "failed":0,
            "filtered":0,
            "published":231,
            "retry":112,
            "total":231
         },
         "queue":{
            "acked":0,
            "max_events":4096
         }
      }
   },
   "metricbeat":{
      "system":{
         "cpu":{
            "events":8,
            "failures":0,
            "success":8
         },
         "filesystem":{
            "events":80,
            "failures":0,
            "success":80
         },
         "memory":{
            "events":8,
            "failures":0,
            "success":8
         },
         "network":{
            "events":135,
            "failures":0,
            "success":135
         }
      }
   },
   "system":{
      "cpu":{
         "cores":8
      },
      "load":{
         "1":2.5957,
         "15":5.415,
         "5":3.5815,
         "norm":{
            "1":0.3245,
            "15":0.6769,
            "5":0.4477
         }
      }
   }
}
```

::::


