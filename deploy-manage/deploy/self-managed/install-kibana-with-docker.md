---
navigation_title: Docker
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/docker.html
products:
  - id: kibana
---



# Install {{kib}} with Docker [docker]


Docker [images for {{kib}}](https://hub.docker.com/_/kibana) are available from the Elastic Docker registry. The base image is Red Hat Universal Base Images (UBI) or Wolfi if you use [hardened Docker images](install-kibana-with-docker.md#_hardened_docker_images).

A list of all published Docker images and tags is available at [www.docker.elastic.co](https://www.docker.elastic.co). The source code is in [GitHub](https://github.com/elastic/dockerfiles/tree/master/kibana).

:::{include} _snippets/trial.md
:::

## Run {{kib}} in Docker for development [run-kibana-on-docker-for-dev]

Use Docker commands to run {{kib}} on a single-node {{es}} cluster for development or testing.

::::{tip}
This setup doesn’t run multiple {{es}} nodes by default. To create a multi-node cluster with {{kib}}, use Docker Compose instead. Refer to [Start a multi-node cluster with Docker Compose](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-compose.md) in the {{es}} documentation.
::::


## Hardened Docker images [_hardened_docker_images]

:::{include} _snippets/wolfi.md
:::

## Start a single node cluster [_start_a_single_node_cluster]

1. Install Docker. Visit [Get Docker](https://docs.docker.com/get-docker/) to install Docker for your environment.

    ::::{important}
    If using Docker Desktop, make sure to allocate at least 4GB of memory. You can adjust memory usage in Docker Desktop by going to **Settings > Resources**.
    ::::

2. Create a new Docker network for {{es}} and {{kib}}.

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
    Because {{kib}} is an {{stack}} product, you must install the same version number as the rest of your {{stack}} components. Replace `<SPECIFIC.VERSION.NUMBER>` with the version that's used across your entire stack. For example, you can use {{version.stack.base}}. You'll use this same version number throughout this tutorial.
    ```sh subs=true
    docker pull docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER>
    ```
    :::
    ::::

4. Optional: Install [Cosign](https://docs.sigstore.dev/system_config/installation/) for your environment. Then use Cosign to verify the {{es}} image’s signature.

    ::::{tab-set}
    :group: docker
    :::{tab-item} Latest
    :sync: latest
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

    ::::{tab-set}
    :group: docker
    :::{tab-item} Latest
    :sync: latest
    ```sh subs=true
    docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
    ```
    :::

    :::{tab-item} Specific version
    :sync: specific
    Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
    ```sh subs=true
    docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER>
    ```
    :::
    ::::

    ::::{tip}
    Use the `-m` flag to set a memory limit for the container. This removes the need to [manually set the JVM size](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-prod.md#docker-set-heap-size).
    ::::


    The command prints the `elastic` user password and an enrollment token for {{kib}}.

6. Copy the generated `elastic` password and enrollment token. These credentials are only shown when you start {{es}} for the first time. You can regenerate the credentials using the following commands.

    ```sh
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
    ```

7. Pull the {{kib}} Docker image.

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
    Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
    ```sh subs=true
    docker pull docker.elastic.co/kibana/kibana:<SPECIFIC.VERSION.NUMBER>
    ```
    :::
    ::::

8. Optional: Verify the {{kib}} image’s signature.

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
    Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
    ```sh subs=true
    wget https://artifacts.elastic.co/cosign.pub
    cosign verify --key cosign.pub docker.elastic.co/kibana/kibana:<SPECIFIC.VERSION.NUMBER>
    ```
    :::
    ::::

9. Start a {{kib}} container.

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
    Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
    ```sh subs=true
    docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:<SPECIFIC.VERSION.NUMBER>
    ```
    :::
    ::::

10. When {{kib}} starts, it outputs a unique generated link to the terminal. To access {{kib}}, open this link in a web browser.
11. In your browser, enter the enrollment token that was generated when you started {{es}}.

    To regenerate the token, run:

    ```sh
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
    ```

12. Log in to {{kib}} as the `elastic` user with the password that was generated when you started {{es}}.

    To regenerate the password, run:

    ```sh
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
    ```

### Remove Docker containers [_remove_docker_containers]

To remove the containers and their network, run:

```sh subs=true
# Remove the Elastic network
docker network rm elastic

# Remove the {{es}} container
docker rm es01

# Remove the {{kib}} container
docker rm kib01
```


## Configure {{kib}} on Docker [configuring-kibana-docker]

The Docker images provide several methods for configuring {{kib}}. The conventional approach is to provide a `kibana.yml` file as described in [](configure-kibana.md), but it’s also possible to use environment variables to define settings.


### Bind-mounted configuration [bind-mount-config]

One way to configure {{kib}} on Docker is to provide `kibana.yml` via bind-mounting. With `docker-compose`, the bind-mount can be specified like this:

::::{tab-set}
:group: docker-kib
:::{tab-item} Latest
:sync: latest
```yaml subs=true
version: '2'
services:
  kibana:
    image: docker.elastic.co/kibana/kibana:{{version.stack}}
    volumes:
      - ./kibana.yml:/usr/share/kibana/config/kibana.yml
```
:::

:::{tab-item} Specific version
:sync: specific
Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
```yaml subs=true
version: '2'
services:
  kibana:
    image: docker.elastic.co/kibana/kibana:<SPECIFIC.VERSION.NUMBER>
    volumes:
      - ./kibana.yml:/usr/share/kibana/config/kibana.yml
```
:::
::::


## Persist the {{kib}} keystore [_persist_the_kib_keystore]

By default, {{kib}} auto-generates a keystore file for secure settings at startup. To persist your [secure settings](/deploy-manage/security/secure-settings.md), use the `kibana-keystore` utility to bind-mount the parent directory of the keystore to the container. For example:

::::{tab-set}
:group: docker-kib
:::{tab-item} Latest
:sync: latest
```sh subs=true
docker run -it --rm -v full_path_to/config:/usr/share/kibana/config -v full_path_to/data:/usr/share/kibana/data docker.elastic.co/kibana/kibana:{{version.stack}} bin/kibana-keystore create
docker run -it --rm -v full_path_to/config:/usr/share/kibana/config -v full_path_to/data:/usr/share/kibana/data docker.elastic.co/kibana/kibana:{{version.stack}} bin/kibana-keystore add test_keystore_setting
```
:::

:::{tab-item} Specific version
:sync: specific
Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
```sh subs=true
docker run -it --rm -v full_path_to/config:/usr/share/kibana/config -v full_path_to/data:/usr/share/kibana/data docker.elastic.co/kibana/kibana:<SPECIFIC.VERSION.NUMBER> bin/kibana-keystore create
docker run -it --rm -v full_path_to/config:/usr/share/kibana/config -v full_path_to/data:/usr/share/kibana/data docker.elastic.co/kibana/kibana:<SPECIFIC.VERSION.NUMBER> bin/kibana-keystore add test_keystore_setting
```
:::
::::


### Environment variable configuration [environment-variable-config]

Under Docker, {{kib}} can be configured via environment variables. When the container starts, a helper process checks the environment for variables that can be mapped to {{kib}} command-line arguments.

For compatibility with container orchestration systems, these environment variables are written in all capitals, with underscores as word separators. The helper translates these names to valid {{kib}} setting names.

::::{warning}
All information that you include in environment variables is visible through the `ps` command, including sensitive information.
::::


Some example translations are shown here:

| Environment variable | {{kib}} setting |
| --- | --- |
| `SERVER_NAME` | `server.name` |
| `SERVER_BASEPATH` | `server.basePath`|
| `ELASTICSEARCH_HOSTS` | `elasticsearch.hosts` |

In general, any setting listed in [](configure-kibana.md) can be configured with this technique.

Supplying array options can be tricky. The following example shows the syntax for providing an array to `ELASTICSEARCH_HOSTS`.

These variables can be set with `docker-compose` like this:

::::{tab-set}
:group: docker-kib
:::{tab-item} Latest
:sync: latest
```yaml subs=true
version: '2'
services:
  kibana:
    image: docker.elastic.co/kibana/kibana:{{version.stack}}
    environment:
      SERVER_NAME: kibana.example.org
      ELASTICSEARCH_HOSTS: '["<ELASTICSEARCH_HOST_URL_01>:9200","<ELASTICSEARCH_HOST_URL_02>:9200","<ELASTICSEARCH_HOST_URL_03>:9200"]'
```
:::

:::{tab-item} Specific version
:sync: specific
Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
```yaml subs=true
version: '2'
services:
  kibana:
    image: docker.elastic.co/kibana/kibana:<SPECIFIC.VERSION.NUMBER>
    environment:
      SERVER_NAME: kibana.example.org
      ELASTICSEARCH_HOSTS: '["<ELASTICSEARCH_HOST_URL_01>:9200","<ELASTICSEARCH_HOST_URL_02>:9200","<ELASTICSEARCH_HOST_URL_03>:9200"]'
```
:::
::::

Since environment variables are translated to CLI arguments, they take precedence over settings configured in `kibana.yml`.


### Docker defaults [docker-defaults]

The following settings have different default values when using the Docker images:

`server.host`
:   `"0.0.0.0"`

`server.shutdownTimeout`
:   `"5s"`

`elasticsearch.hosts`
:   `http://elasticsearch:9200`

`monitoring.ui.container.elasticsearch.enabled`
:   `true`

These settings are defined in the default `kibana.yml`. They can be overridden with a [custom `kibana.yml`](#bind-mount-config) or using [environment variables](#environment-variable-config).

::::{important}
If replacing `kibana.yml` with a custom version, be sure to copy the defaults to the custom file if you want to retain them. If not, they will be "masked" by the new file.
::::

## Next steps

:::{include} _snippets/install-kib-next-steps.md
:::