---
applies_to:
  deployment:
    self:
navigation_title: Single-node cluster
---

# Start a single-node cluster in Docker [docker-cli-run-dev-mode]

Use Docker commands to start a single-node {{es}} cluster for development or testing. You can then run additional Docker commands to add nodes to the test cluster or run {{kib}}.

::::{tip}
* If you just want to test {{es}} in local development, refer to [Run {{es}} locally](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md). Note that this setup is not suitable for production environments.
* This setup doesn’t run multiple {{es}} nodes or {{kib}} by default. To create a multi-node cluster with {{kib}}, use Docker Compose instead. See [Start a multi-node cluster with Docker Compose](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-compose.md).
::::


## Hardened Docker images [docker-wolfi-hardened-image]

:::{include} _snippets/wolfi.md
:::

## Start a single-node cluster [_start_a_single_node_cluster]

1. Install Docker. Visit [Get Docker](https://docs.docker.com/get-docker/) to install Docker for your environment.

    If using Docker Desktop, make sure to allocate at least 4GB of memory. You can adjust memory usage in Docker Desktop by going to **Settings > Resources**.

2. Create a new docker network.

    ```sh
    docker network create elastic
    ```

3. Pull the {{es}} Docker image.

    ::::{tab-set}
    :group: docker
    :::{tab-item} Latest
    :sync: latest
    ```sh subs=true
    docker pull docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
    ```
    :::

    :::{tab-item} Specific version
    :sync: specific
    Replace `<SPECIFIC.VERSION.NUMBER>` with the {{stack}} version number you want. For example, you can replace `<SPECIFIC.VERSION.NUMBER>` with {{version.stack.base}}. You'll use this same version number throughout this tutorial.
    ```sh subs=true
    docker pull docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER>
    ```
    :::

4. Optional: Install [Cosign](https://docs.sigstore.dev/cosign/system_config/installation/) for your environment. Then use Cosign to verify the {{es}} image’s signature.

    ::::{tab-set}
    :group: docker
    :::{tab-item} Latest
    :sync: latest
    $$$docker-verify-signature$$$

    ```sh subs=true
    wget https://artifacts.elastic.co/cosign.pub
    cosign verify --key cosign.pub docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
    ```

    The `cosign` command prints the check results and the signature payload in JSON format:

    ```sh subs=true
    Verification for docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}} --
    The following checks were performed on each of these signatures:
      - The cosign claims were validated
      - Existence of the claims in the transparency log was verified offline
      - The signatures were verified against the specified public key
    ```
    :::
    
    :::{tab-item} Specific version
    :sync: specific
    Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
    $$$docker-verify-signature$$$

    ```sh subs=true
    wget https://artifacts.elastic.co/cosign.pub
    cosign verify --key cosign.pub docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER>
    ```

    The `cosign` command prints the check results and the signature payload in JSON format:

    ```sh subs=true
    Verification for docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER> --
    The following checks were performed on each of these signatures:
      - The cosign claims were validated
      - Existence of the claims in the transparency log was verified offline
      - The signatures were verified against the specified public key
    ```
    :::
    ::::


5. Start an {{es}} container.

    ::::::{tab-set}
    :group: docker
    :::::{tab-item} Latest
    :sync: latest
    ```sh subs=true
    docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
    ```

    ::::{tip}
    Use the `-m` flag to set a memory limit for the container. This removes the need to [manually set the JVM size](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-prod.md#docker-set-heap-size).
    ::::

    {{ml-cap}} features such as [semantic search with ELSER](/solutions/search/semantic-search/semantic-search-elser-ingest-pipelines.md) require a larger container with more than 1GB of memory. If you intend to use the {{ml}} capabilities, then start the container with this command:

    ```sh subs=true
    docker run --name es01 --net elastic -p 9200:9200 -it -m 6GB -e "xpack.ml.use_auto_machine_memory_percent=true" docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
    ```

    The command prints the `elastic` user password and an enrollment token for {{kib}}.
    :::::

    :::::{tab-item} Specific version
    :sync: specific
    Use the same {{stack}} version number as the Docker image you pulled earlier and replace `<SPECIFIC.VERSION.NUMBER>` with it.
    ```sh subs=true
    docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER>
    ```

    ::::{tip}
    Use the `-m` flag to set a memory limit for the container. This removes the need to [manually set the JVM size](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-prod.md#docker-set-heap-size).
    ::::

    {{ml-cap}} features such as [semantic search with ELSER](/solutions/search/semantic-search/semantic-search-elser-ingest-pipelines.md) require a larger container with more than 1GB of memory. If you intend to use the {{ml}} capabilities, then start the container with this command:

    ```sh subs=true
    docker run --name es01 --net elastic -p 9200:9200 -it -m 6GB -e "xpack.ml.use_auto_machine_memory_percent=true" docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER>
    ```

    The command prints the `elastic` user password and an enrollment token for {{kib}}.
    :::::
    ::::::

6. Copy the generated `elastic` password and enrollment token. These credentials are only shown when you start {{es}} for the first time. You can regenerate the credentials using the following commands.

    ```sh
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
    ```

    We recommend storing the `elastic` password as an environment variable in your shell. Example:

    ```sh
    export ELASTIC_PASSWORD="your_password"
    ```

7. Copy the `http_ca.crt` SSL certificate from the container to your local machine.

    ```sh
    docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
    ```

8. Make a REST API call to {{es}} to ensure the {{es}} container is running.

    ```sh
    curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
    ```

## Add more nodes [_add_more_nodes]

1. Use an existing node to generate a enrollment token for the new node.

    ```sh
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node
    ```

    The enrollment token is valid for 30 minutes.

2. Start a new {{es}} container. Include the enrollment token as an environment variable.

    ::::{tab-set}
    :group: docker
    :::{tab-item} Latest
    :sync: latest
    ```sh subs=true
    docker run -e ENROLLMENT_TOKEN="<token>" --name es02 --net elastic -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
    ```
    :::
    :::{tab-item} Specific version
    :sync: specific
    Use the same {{stack}} version number as the Docker image you pulled earlier and replace `<SPECIFIC.VERSION.NUMBER>` with it.
    ```sh subs=true
    docker run -e ENROLLMENT_TOKEN="<token>" --name es02 --net elastic -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER>
    ```
    :::
    ::::

3. Call the [cat nodes API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes) to verify the node was added to the cluster.

    ```sh
    curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200/_cat/nodes
    ```

## Run {{kib}} [run-kibana-docker]

1. Pull the {{kib}} Docker image.

    ::::{tab-set}
    :group: docker
    :::{tab-item} Latest
    :sync: latest
    ```sh subs=true
    docker pull docker.elastic.co/kibana/kibana:{{version.stack}}
    ```
    :::
    :::{tab-item} Specific version
    :sync: specific
    Use the same {{stack}} version number as the Docker image you pulled earlier and replace `<SPECIFIC.VERSION.NUMBER>` with it.
    ```sh subs=true
    docker pull docker.elastic.co/kibana/kibana:<SPECIFIC.VERSION.NUMBER>
    ```
    :::
    ::::

2. Optional: Verify the {{kib}} image’s signature.

    ::::{tab-set}
    :group: docker
    :::{tab-item} Latest
    :sync: latest
    ```sh subs=true
    wget https://artifacts.elastic.co/cosign.pub
    cosign verify --key cosign.pub docker.elastic.co/kibana/kibana:{{version.stack}}
    ```
    :::
    :::{tab-item} Specific version
    :sync: specific
    Use the same {{stack}} version number as the Docker image you pulled earlier and replace `<SPECIFIC.VERSION.NUMBER>` with it.
    ```sh subs=true
    wget https://artifacts.elastic.co/cosign.pub
    cosign verify --key cosign.pub docker.elastic.co/kibana/kibana:<SPECIFIC.VERSION.NUMBER>
    ```
    :::
    ::::


3. Start a {{kib}} container.

    ::::{tab-set}
    :group: docker
    :::{tab-item} Latest
    :sync: latest
    ```sh subs=true
    docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:{{version.stack}}
    ```
    :::
    :::{tab-item} Specific version
    :sync: specific
    Use the same {{stack}} version number as the Docker image you pulled earlier and replace `<SPECIFIC.VERSION.NUMBER>` with it.
     ```sh subs=true
    docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:<SPECIFIC.VERSION.NUMBER>
    ```
    :::
    ::::

4. When {{kib}} starts, it outputs a unique generated link to the terminal. To access {{kib}}, open this link in a web browser.
5. In your browser, enter the enrollment token that was generated when you started {{es}}.

    To regenerate the token, run:

    ```sh
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
    ```

6. Log in to {{kib}} as the `elastic` user with the password that was generated when you started {{es}}.

    To regenerate the password, run:

    ```sh
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
    ```

## Remove containers [remove-containers-docker]

To remove the containers and their network, run:

```sh subs=true
# Remove the Elastic network
docker network rm elastic

# Remove {{es}} containers
docker rm es01
docker rm es02

# Remove the {{kib}} container
docker rm kib01
```

## Next steps [_next_steps_5]

You now have a test {{es}} environment set up. Before you start serious development or go into production with {{es}}, review the [requirements and recommendations](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-prod.md) to apply when running {{es}} in Docker in production.