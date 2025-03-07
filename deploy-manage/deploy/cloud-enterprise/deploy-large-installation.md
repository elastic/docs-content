---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-large-cloud.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-large-onprem.html
---

# Deploy a large installation [ece-install-large]

This type of installation is recommended for deployments with significant overall search and indexing throughput. You need:

* 3 hosts with at least 64 GB RAM each for directors and coordinators (ECE management services)
* 3 hosts for allocators, each with one of the following RAM configurations:

    * 1 x 256 GB RAM
    * 2 x 128 GB RAM
    * 4 x 64 GB RAM

* 3 hosts with 16 GB RAM each for proxies
* 3 availability zones

:::{image} ../../../images/cloud-enterprise-ece-pb-9.png
:alt: A large installation with nine to twelve hosts across three availability zones
:::

## Important considerations  [ece_before_you_start_3]

Note that the large-sized Elastic Cloud Enterprise installation separates the allocator and proxy roles from the director and coordinator roles (ECE management services).

**Check the recommended JVM Heap sizes**

| Service | JVM Heap Size (Xms and Xmx) |
| --- | --- |
| `runner` | 1 GB |
| `allocator` | 4 GB |
| `zookeeper` | 24 GB |
| `director` | 1 GB |
| `constructor` | 4 GB |
| `admin-console` | 24 GB |

::::{warning}
For production environments, you must define the memory settings for each role, except for the `proxy` role, as starting from ECE 2.4 the JVM proxy was replaced with a Golang-based proxy. If you don’t set any memory setting, the default values are used, which are inadequate for production environments and can lead to performance or stability issues.
::::

## Before you start

Make sure you have completed all prerequisites and environment preparations described in the [Installation overview](./install.md), and that the hosts are configured according to [](./configure-operating-system.md).

## Installation steps [ece_installation_steps_3]

1. Install Elastic Cloud Enterprise on the first host to start a new installation with your first availability zone. This first host holds all roles to help bootstrap the rest of the installation, but you will remove some of its roles in a later step.

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --availability-zone MY_ZONE-1 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"},"zookeeper":{"xms":"24G","xmx":"24G"},"director":{"xms":"1G","xmx":"1G"},"constructor":{"xms":"4G","xmx":"4G"},"admin-console":{"xms":"24G","xmx":"24G"}}'
    ```

    After the installation completes, copy down the coordinator host IP address, user credentials, and roles token information. Keep this information safe.

2. Generate a new roles token that persists for one hour on the first host, so that other hosts can join your installation with the right role permissions in subsequent steps (referred to as `MY_TOKEN`). The new token needs to enable the director, coordinator, and proxy roles.

    ```sh
    curl -k -H 'Content-Type: application/json' -u admin:PASSWORD https://localhost:12443/api/v1/platform/configuration/security/enrollment-tokens -d '{ "persistent": false, "roles": ["director", "coordinator", "proxy"] }'
    ```

3. Install Elastic Cloud Enterprise on a second and third host, placing them into a second and a third availability zone, and assign them the `director` and `coordinator` roles. Do not assign the `allocator` or the `proxy` role, as these hosts should not handle or route any user requests. Make sure you include the coordinator host IP information from step 1 and the new roles token from step 2.

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'MY_TOKEN' --roles "director,coordinator" --availability-zone MY_ZONE-2 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"zookeeper":{"xms":"24G","xmx":"24G"},"director":{"xms":"1G","xmx":"1G"},"constructor":{"xms":"4G","xmx":"4G"},"admin-console":{"xms":"24G","xmx":"24G"}}'
    ```

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'MY_TOKEN' --roles "director,coordinator" --availability-zone MY_ZONE-3 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"zookeeper":{"xms":"24G","xmx":"24G"},"director":{"xms":"1G","xmx":"1G"},"constructor":{"xms":"4G","xmx":"4G"},"admin-console":{"xms":"24G","xmx":"24G"}}'
    ```

4. To handle the Elasticsearch and Kibana workload, install Elastic Cloud Enterprise on three or more hosts, distributing them evenly across the existing three availability zones, or on however many hosts you think you need initially, and assign them the `allocator` role. Make sure you include the coordinator host IP information and allocator roles token from step 1.

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'ALLOCATOR_TOKEN' --roles "allocator" --availability-zone MY_ZONE-1 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"}}'

    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'ALLOCATOR_TOKEN' --roles "allocator" --availability-zone MY_ZONE-2 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"}}'

    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'ALLOCATOR_TOKEN' --roles "allocator" --availability-zone MY_ZONE-3 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"}}'
    ```

5. To handle the routing of user requests to Elasticsearch, install Elastic Cloud Enterprise on a three additional hosts, distributing them evenly across the existing three availability zones, and assign them the `proxy` role. Do not assign any other roles, as these hosts should only route user requests. Make sure you include the coordinator host IP information from step 1 and the new roles token from step 2.

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'MY_TOKEN' --roles "proxy" --availability-zone MY_ZONE-1 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"}}'
    ```

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'MY_TOKEN' --roles "proxy" --availability-zone MY_ZONE-2 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"}}'
    ```

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'MY_TOKEN' --roles "proxy" --availability-zone MY_ZONE-3 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"}}'
    ```

6. [Change the deployment configuration](working-with-deployments.md) for the `admin-console-elasticsearch`, `logging-and-metrics`, and `security` clusters to use three availability zones and resize the nodes to use at least 4 GB of RAM. This change makes sure that the clusters used by the administration console are highly available and provisioned sufficiently.

7. [Log into the Cloud UI](log-into-cloud-ui.md) to provision your deployment.

Once the installation is complete, you can continue with [](./post-installation-steps.md).