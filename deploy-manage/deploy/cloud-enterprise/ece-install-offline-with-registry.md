---
navigation_title: With your private Docker registry
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-offline-with-registry.html
---

# Air-gapped install with a private Docker registry [ece-install-offline-with-registry]

Installing ECE on multiple hosts with your own registry server is simpler, because you do not have to load the Docker images on each host.

1. Set up your private Docker registry. To learn more, check [Deploy a registry server](https://docs.docker.com/registry/deploying/).

    ::::{tip} 
    As part of the ECE [high availability](ece-ha.md) strategy, it’s a good idea to make sure that your Docker registry server is available to all ECE allocators, so that it can continue to be accessed in the event of a network partition or zone outage. Allocators attempting to start instances requiring Docker images that have not yet been pulled from a custom Docker registry will fail to start if the registry is unavailable.
    ::::

2. On an internet-connected host that has Docker installed, download the [Available Docker Images](ece-install-offline-images.md) and push them to your private Docker registry. Note that for ECE version 3.0, if you want to use Elastic Stack version 8.0 in your deployments, you need to download and make available both the version 7.x and version 8.x Docker images.

    ```sh
    docker pull docker.elastic.co/cloud-enterprise/elastic-cloud-enterprise:3.8.1
    docker pull docker.elastic.co/cloud-assets/elasticsearch:7.17.27-0
    docker pull docker.elastic.co/cloud-assets/kibana:7.17.27-0
    docker pull docker.elastic.co/cloud-assets/apm:7.17.27-0
    docker pull docker.elastic.co/cloud-assets/enterprise-search:7.17.27-0
    docker pull docker.elastic.co/cloud-release/elasticsearch-cloud-ess:8.17.1
    docker pull docker.elastic.co/cloud-release/kibana-cloud:8.17.1
    docker pull docker.elastic.co/cloud-release/elastic-agent-cloud:8.17.1
    docker pull docker.elastic.co/cloud-release/enterprise-search-cloud:8.17.1
    ```

    For example, for Elastic Cloud Enterprise 3.8.1 and the Elastic Stack versions it shipped with, you need:

    * Elastic Cloud Enterprise 3.8.1
    * Elasticsearch 8.17.1, Kibana 8.17.1, APM 8.17.1, and Enterprise Search 8.17.1

    :::{important}
       Enterprise Search is not available in versions 9.0+.
    :::

3. Tag the Docker images with your private registry URL by replacing `REGISTRY` with your actual registry address, for example `my.private.repo:5000`:

    ```sh
    docker tag docker.elastic.co/cloud-enterprise/elastic-cloud-enterprise:3.8.1 REGISTRY/cloud-enterprise/elastic-cloud-enterprise:3.8.1
    docker tag docker.elastic.co/cloud-assets/elasticsearch:7.17.27-0 REGISTRY/cloud-assets/elasticsearch:7.17.27-0
    docker tag docker.elastic.co/cloud-assets/kibana:7.17.27-0 REGISTRY/cloud-assets/kibana:7.17.27-0
    docker tag docker.elastic.co/cloud-assets/apm:7.17.27-0 REGISTRY/cloud-assets/apm:7.17.27-0
    docker tag docker.elastic.co/cloud-assets/enterprise-search:7.17.27-0 REGISTRY/cloud-assets/enterprise-search:7.17.27-0
    docker tag docker.elastic.co/cloud-release/elasticsearch-cloud-ess:8.17.1 REGISTRY/cloud-release/elasticsearch-cloud-ess:8.17.1
    docker tag docker.elastic.co/cloud-release/kibana-cloud:8.17.1 REGISTRY/cloud-release/kibana-cloud:8.17.1
    docker tag docker.elastic.co/cloud-release/elastic-agent-cloud:8.17.1 REGISTRY/cloud-release/elastic-agent-cloud:8.17.1
    docker tag docker.elastic.co/cloud-release/enterprise-search-cloud:8.17.1 REGISTRY/cloud-release/enterprise-search-cloud:8.17.1
    ```

4. Push the Docker images to your private Docker registry, using the same tags from the previous step. Replace `REGISTRY` with your actual registry URL, for example `my.private.repo:5000`:

    ```sh
    docker push REGISTRY/cloud-enterprise/elastic-cloud-enterprise:3.8.1
    docker push REGISTRY/cloud-assets/elasticsearch:7.17.27-0
    docker push REGISTRY/cloud-assets/kibana:7.17.27-0
    docker push REGISTRY/cloud-assets/apm:7.17.27-0
    docker push REGISTRY/cloud-assets/enterprise-search:7.17.27-0
    docker push REGISTRY/cloud-release/elasticsearch-cloud-ess:8.17.1
    docker push REGISTRY/cloud-release/kibana-cloud:8.17.1
    docker push REGISTRY/cloud-release/elastic-agent-cloud:8.17.1
    docker push REGISTRY/cloud-release/enterprise-search-cloud:8.17.1
    ```

5. On an internet-connected host, download the installation script:

    ```sh
    curl -L -O https://download.elastic.co/cloud/elastic-cloud-enterprise.sh
    ```

6. Copy the installation script to each host where you plan to install Elastic Cloud Enterprise or make it available on your network.

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