---
navigation_title: With your private Docker registry
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-offline-with-registry.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Air-gapped install with a private Docker registry [ece-install-offline-with-registry]

Installing ECE on multiple hosts with your own registry server is simpler, because you do not have to load the Docker images on each host.

1. Set up your private Docker registry. To learn more, check [Deploy a registry server](https://docs.docker.com/registry/deploying/).

    ::::{tip}
    As part of the ECE [high availability](ece-ha.md) strategy, it’s a good idea to make sure that your Docker registry server is available to all ECE allocators, so that it can continue to be accessed in the event of a network partition or zone outage. Allocators attempting to start instances requiring Docker images that have not yet been pulled from a custom Docker registry will fail to start if the registry is unavailable.
    ::::

2. On an internet-connected host that has Docker installed, download the [Available Docker Images](ece-install-offline-images.md) and push them to your private Docker registry. Note that for ECE version 4.0, if you want to use {{stack}} version 9.0 in your deployments, you need to download and make available both the version 8.x and version 9.x Docker images.

    ```sh subs=true
    docker pull docker.elastic.co/cloud-enterprise/elastic-cloud-enterprise:{{version.ece}}
    docker pull docker.elastic.co/cloud-release/elasticsearch-cloud-ess:8.18.0
    docker pull docker.elastic.co/cloud-release/kibana-cloud:8.18.0
    docker pull docker.elastic.co/cloud-release/elastic-agent-cloud:8.18.0
    docker pull docker.elastic.co/cloud-release/enterprise-search-cloud:8.18.0
    docker pull docker.elastic.co/cloud-release/elasticsearch-cloud-ess:9.0.0
    docker pull docker.elastic.co/cloud-release/kibana-cloud:9.0.0
    docker pull docker.elastic.co/cloud-release/elastic-agent-cloud:9.0.0
    ```

    For example, for {{ece}} {{version.ece}} and the {{stack}} versions it shipped with, you need:

    * {{ece}} {{version.ece}}
    * {{es}} 9.0.0, {{kib}} 9.0.0, APM 9.0.0

    :::{important}
       Enterprise Search is not available in versions 9.0+.
    :::

3. Tag the Docker images with your private registry URL by replacing `REGISTRY` with your actual registry address, for example `my.private.repo:5000`:

    ```sh subs=true
    docker tag docker.elastic.co/cloud-enterprise/elastic-cloud-enterprise:{{version.ece}} REGISTRY/cloud-enterprise/elastic-cloud-enterprise:{{version.ece}}
    docker tag docker.elastic.co/cloud-release/elasticsearch-cloud-ess:8.18.0 REGISTRY/cloud-release/elasticsearch-cloud-ess:8.18.0
    docker tag docker.elastic.co/cloud-release/kibana-cloud:8.18.0 REGISTRY/cloud-release/kibana-cloud:8.18.0
    docker tag docker.elastic.co/cloud-release/elastic-agent-cloud:8.18.0 REGISTRY/cloud-release/elastic-agent-cloud:8.18.0
    docker tag docker.elastic.co/cloud-release/enterprise-search-cloud:8.18.0 REGISTRY/cloud-release/enterprise-search-cloud:8.18.0
    docker tag docker.elastic.co/cloud-release/elasticsearch-cloud-ess:9.0.0 REGISTRY/cloud-release/elasticsearch-cloud-ess:9.0.0
    docker tag docker.elastic.co/cloud-release/kibana-cloud:9.0.0 REGISTRY/cloud-release/kibana-cloud:9.0.0
    docker tag docker.elastic.co/cloud-release/elastic-agent-cloud:9.0.0 REGISTRY/cloud-release/elastic-agent-cloud:9.0.0
    ```

4. Push the Docker images to your private Docker registry, using the same tags from the previous step. Replace `REGISTRY` with your actual registry URL, for example `my.private.repo:5000`:

    ```sh subs=true
    docker push REGISTRY/cloud-enterprise/elastic-cloud-enterprise:{{version.ece}}
    docker push REGISTRY/cloud-release/elasticsearch-cloud-ess:8.18.0
    docker push REGISTRY/cloud-release/kibana-cloud:8.18.0
    docker push REGISTRY/cloud-release/elastic-agent-cloud:8.18.0
    docker push REGISTRY/cloud-release/enterprise-search-cloud:8.18.0
    docker push REGISTRY/cloud-release/elasticsearch-cloud-ess:9.0.0
    docker push REGISTRY/cloud-release/kibana-cloud:9.0.0
    docker push REGISTRY/cloud-release/elastic-agent-cloud:9.0.0
    ```

5. On an internet-connected host, download the installation script:

    ```sh
    curl -L -O https://download.elastic.co/cloud/elastic-cloud-enterprise.sh
    ```

6. Copy the installation script to each host where you plan to install {{ece}} or make it available on your network.

7. Invoke the installation script on each host with the `--docker-registry REGISTRY` parameter, replacing `REGISTRY` with your actual registry URL (for example `my.private.repo:5000`):

   ::::{note}
   Refer to [](./install-ece-procedures.md) for more details on the parameters to pass to the installation script depending on the size of your installation.
   ::::

    1. On the first host:

        ```sh
        bash elastic-cloud-enterprise.sh install
          --docker-registry REGISTRY
        ```

    2. On additional hosts, include the `--coordinator-host HOST_IP` and `--roles-token 'TOKEN'` parameters provided to you when you installed on the first host, along with the `--docker-registry REGISTRY` parameter:

        ```sh
        bash elastic-cloud-enterprise.sh install
          --coordinator-host HOST_IP
          --roles-token 'TOKEN'
          --docker-registry REGISTRY
        ```

   Once the installation is complete, refer to [](./log-into-cloud-ui.md) to access Cloud UI.
