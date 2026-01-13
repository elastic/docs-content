---
navigation_title: Upgrade Elasticsearch running on Docker
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
---

# Upgrading the {{es}} version running on Docker

You update a single-node {{es}} cluster running in a Docker container by pulling a new Docker image and recreating the container using the new image and the same data volumes as the original container.

Docker images for {{es}} are available from the Elastic Docker registry. A list of all published Docker images and tags is available at [www.docker.elastic.co](https://www.docker.elastic.co). The source code is in [GitHub](https://github.com/elastic/elasticsearch/blob/master/distribution/docker).

## Prepare to upgrade [prepare-to-upgrade]

Upgrading your cluster can be disruptive. It is important that you [plan your upgrade](/deploy-manage/upgrade/plan-upgrade.md) and [take the necessary upgrade preparation steps](/deploy-manage/upgrade/prepare-to-upgrade.md).

The following is a list of typical upgrade preparation tasks and best practices:

* Always back up your data before performing an update, especially for production environments.
* Review the {{es}} release notes for the new version to be aware of any breaking changes or required actions before or after the update.
* If you're using custom plugins or configurations, ensure they are compatible with the new version and reapply them if necessary.
* If you're running a cluster, you'll need to carefully plan the upgrade process to minimize downtime and ensure cluster stability. This often involves a rolling upgrade strategy.
* When using a `docker-compose.yml` make sure to update the desired version in the configuration file or the environment variable.


## Hardened Docker images [docker-wolfi-images]

You can also use the hardened [Wolfi](https://wolfi.dev/) image for additional security. Using Wolfi images requires Docker version 20.10.10 or higher.

To use the Wolfi image, append `-wolfi` to the image tag in the Docker command.

For example:

```sh subs=true
docker pull docker.elastic.co/elasticsearch/elasticsearch-wolfi:{{version.stack}}
```

To upgrade to a different version, replace {{version.stack}} with the version you want to upgrade to.


## Upgrade {{es}} running on Docker [upgrade-process]

1. Pull the new version of the {{es}} Docker image from Elastic's Docker registry using the `docker pull` command.

    ```sh subs=true
    docker pull docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
    ```

    If you want to upgrade to a different version, replace {{version.stack}} with the version you want to upgrade to.

1. Optional: Install [Cosign](https://docs.sigstore.dev/cosign/system_config/installation/) for your environment. Then use Cosign to verify the {{es}} image’s signature.
To upgrade to a different version, replace {{version.stack}} with the version you want to upgrade to.

    ```sh subs=true
    wget https://artifacts.elastic.co/cosign.pub
    cosign verify --key cosign.pub docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
    ```

    The `cosign` command prints the check results and the signature payload:

    ```sh subs=true
    Verification for docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}} --
    The following checks were performed on each of these signatures:
      - The cosign claims were validated
      - Existence of the claims in the transparency log was verified offline
      - The signatures were verified against the specified public key
    ```

1. Stop the currently running {{es}} container. Replace `<container_name>` with the name or ID of your {{es}} container.

    ```shell
    docker stop <container_name>
    ```

1. After the container has stopped, you can remove it. If your data directory is correctly mapped to a volume outside of the container, your data is preserved. Replace `<container_name>` with the name or ID of your {{es}} container.

    :::{important}
    This example assumes that you've started the original container with the configuration and data directories stored in separate volumes.
    :::

    ```shell
    docker rm <container_name>
    ```

1. Start a new container using the new image. Use the same volume mappings and configuration settings as the old container to ensure that your data and configuration are preserved. Replace `<container_name>`, `<path_to_data_volume>`, and <path_to_config_volume> with details relevant to your setup.

    ```sh subs=true
    docker run --name <container_name> -p 9200:9200 -p 9300:9300 \
    -e "discovery.type=single-node" \
    -v <path_to_data_volume>:/usr/share/elasticsearch/data \
    -v <path_to_config_volume>:/usr/share/elasticsearch/config \
    docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
    ```

    Adjust the `-p` flags for port mappings, `-e` for environment variables, and `-v` for volume mappings as needed based on your setup.

    To upgrade to a different version, replace {{version.stack}} with the version you want to upgrade to.

1. After the new container starts, verify that {{es}} is running the new version by querying the root URL of your {{es}} instance. 

    ```sh subs=true
    curl http://localhost:9200
    docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
    ```

    In the response, check that the reported `version number` matches the {{es}} version number you upgraded to.
