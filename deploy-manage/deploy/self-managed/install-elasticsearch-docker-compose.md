---
applies_to:
  deployment:
    self:
navigation_title: Multi-node cluster
---

# Start a multi-node cluster with Docker Compose [docker-compose-file]

Use Docker Compose to start a three-node {{es}} cluster with {{kib}}. Docker Compose lets you start multiple containers with a single command.

## Hardened Docker images [docker-wolfi-hardened-image]

:::{include} _snippets/wolfi.md
:::

## Configure and start the cluster [_configure_and_start_the_cluster]

1. Install Docker Compose. Visit the [Docker Compose docs](https://docs.docker.com/compose/install/) to install Docker Compose for your environment.

    If you’re using Docker Desktop, Docker Compose is installed automatically. Make sure to allocate at least 4GB of memory to Docker Desktop. You can adjust memory usage in Docker Desktop by going to **Settings > Resources**.

2. Create or navigate to an empty directory for the project.
3. Download and save the following files in the project directory:

    * [`.env`](https://github.com/elastic/elasticsearch/blob/main/docs/reference/setup/install/docker/.env)
    * [`docker-compose.yml`](https://github.com/elastic/elasticsearch/blob/main/docs/reference/setup/install/docker/docker-compose.yml)

4. In the `.env` file, specify a password for the `ELASTIC_PASSWORD` and `KIBANA_PASSWORD` variables.

    The passwords must be alphanumeric and can’t contain special characters, such as `!` or `@`. The bash script included in the `docker-compose.yml` file only works with alphanumeric characters. Example:

    ```txt
    # Password for the 'elastic' user (at least 6 characters)
    ELASTIC_PASSWORD=changeme

    # Password for the 'kibana_system' user (at least 6 characters)
    KIBANA_PASSWORD=changeme
    ...
    ```

5. Edit the `.env` file to set the `STACK_VERSION`:

    ::::{tab-set}
    :group: docker
    :::{tab-item} Latest
    :sync: latest
    Set the stack version to the current {{stack}} version. 
    ```txt subs=true
    ...
    # Version of Elastic products
    STACK_VERSION={{version.stack}}
    ...
    ```
    :::

    :::{tab-item} Specific version
    :sync: specific
    Replace `<SPECIFIC.VERSION.NUMBER>` with the {{es}} version number you want. For example, you can replace `<SPECIFIC.VERSION.NUMBER>` with {{version.stack.base}}.
    ```txt subs=true
    ...
    # Version of Elastic products
    STACK_VERSION=<SPECIFIC.VERSION.NUMBER>
    ...
    :::
    ::::

6. By default, the Docker Compose configuration exposes port `9200` on all network interfaces.

    To avoid exposing port `9200` to external hosts, set `ES_PORT` to `127.0.0.1:9200` in the `.env` file. This ensures {{es}} is only accessible from the host machine.

    ```txt
    ...
    # Port to expose Elasticsearch HTTP API to the host
    #ES_PORT=9200
    ES_PORT=127.0.0.1:9200
    ...
    ```

7. To start the cluster, run the following command from the project directory.

    ```sh
    docker-compose up -d
    ```

8. After the cluster has started, open [http://localhost:5601](http://localhost:5601) in a web browser to access {{kib}}.
9. Log in to {{kib}} as the `elastic` user using the `ELASTIC_PASSWORD` you set earlier.


## Stop and remove the cluster [_stop_and_remove_the_cluster]

To stop the cluster, run `docker-compose down`. The data in the Docker volumes is preserved and loaded when you restart the cluster with `docker-compose up`.

```sh
docker-compose down
```

To delete the network, containers, and volumes when you stop the cluster, specify the `-v` option:

```sh
docker-compose down -v
```


## Next steps [_next_steps_6]

You now have a test {{es}} environment set up. Before you start serious development or go into production with {{es}}, review the [requirements and recommendations](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-prod.md) to apply when running {{es}} in Docker in production.
