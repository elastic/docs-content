---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-large-cloud.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-large-onprem.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Deploy a large installation [ece-install-large]

This type of installation is recommended for deployments with significant overall search and indexing throughput. You need:

* 3 hosts with at least 64 GB RAM each for directors and coordinators (ECE management services)
* A minimum of 3 hosts for allocators, using one of the following configurations per availability zone:

    * 1 host with 256 GB RAM → 3 hosts total
    * 2 hosts with 128 GB RAM each → 6 hosts total
    * 4 hosts with 64 GB RAM each → 12 hosts total

* 3 hosts with 16 GB RAM each for proxies
* 3 availability zones

:::{image} /deploy-manage/images/cloud-enterprise-ece-pb-9.png
:alt: A large installation with nine to twelve hosts across three availability zones
:::

::::{note}
In the diagram, the Director Coordinator host in Availability zone 1, which represents the first host to be installed, has the allocator and proxy roles greyed out. This host temporarily holds all roles until the other nodes are added and configured. Eventually, the allocator and proxy roles will be removed from this host.
::::

## Important considerations  [ece_before_you_start_3]

Note that the large-sized {{ece}} installation separates the allocator and proxy roles from the director and coordinator roles (ECE management services).

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

1. Install {{ece}} on the first host to start a new installation with your first availability zone. This first host holds all roles to help bootstrap the rest of the installation, but you will remove some of its roles in a later step.

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --availability-zone MY_ZONE-1 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"},"zookeeper":{"xms":"24G","xmx":"24G"},"director":{"xms":"1G","xmx":"1G"},"constructor":{"xms":"4G","xmx":"4G"},"admin-console":{"xms":"24G","xmx":"24G"}}'
    ```

    After the installation completes, copy down the coordinator host IP address, user credentials, and roles token information. Keep this information safe.

2. Generate a new roles token that persists for one hour on the first host, so that other hosts can join your installation with the right role permissions in subsequent steps (referred to as `MY_TOKEN`). The new token needs to enable the director, coordinator, and proxy roles.

    ```sh
    curl -k -H 'Content-Type: application/json' -u admin:PASSWORD https://localhost:12443/api/v1/platform/configuration/security/enrollment-tokens -d '{ "persistent": false, "roles": ["director", "coordinator", "proxy"] }'
    ```

3. Install {{ece}} on a second and third host, placing them into a second and a third availability zone, and assign them the `director` and `coordinator` roles. Do not assign the `allocator` or the `proxy` role, as these hosts should not handle or route any user requests. Make sure you include the coordinator host IP information from step 1 and the new roles token from step 2.

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'MY_TOKEN' --roles "director,coordinator" --availability-zone MY_ZONE-2 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"zookeeper":{"xms":"24G","xmx":"24G"},"director":{"xms":"1G","xmx":"1G"},"constructor":{"xms":"4G","xmx":"4G"},"admin-console":{"xms":"24G","xmx":"24G"}}'
    ```

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'MY_TOKEN' --roles "director,coordinator" --availability-zone MY_ZONE-3 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"zookeeper":{"xms":"24G","xmx":"24G"},"director":{"xms":"1G","xmx":"1G"},"constructor":{"xms":"4G","xmx":"4G"},"admin-console":{"xms":"24G","xmx":"24G"}}'
    ```

4. To handle the {{es}} and {{kib}} workload, install {{ece}} on three or more hosts, distributing them evenly across the existing three availability zones, or on however many hosts you think you need initially, and assign them the `allocator` role. Make sure you include the coordinator host IP information and allocator roles token from step 1.

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'ALLOCATOR_TOKEN' --roles "allocator" --availability-zone MY_ZONE-1 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"}}'

    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'ALLOCATOR_TOKEN' --roles "allocator" --availability-zone MY_ZONE-2 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"}}'

    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'ALLOCATOR_TOKEN' --roles "allocator" --availability-zone MY_ZONE-3 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"}}'
    ```

5. To handle the routing of user requests to {{es}}, install {{ece}} on a three additional hosts, distributing them evenly across the existing three availability zones, and assign them the `proxy` role. Do not assign any other roles, as these hosts should only route user requests. Make sure you include the coordinator host IP information from step 1 and the new roles token from step 2.

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'MY_TOKEN' --roles "proxy" --availability-zone MY_ZONE-1 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"}}'
    ```

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'MY_TOKEN' --roles "proxy" --availability-zone MY_ZONE-2 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"}}'
    ```

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'MY_TOKEN' --roles "proxy" --availability-zone MY_ZONE-3 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"}}'
    ```

6. [Log into the Cloud UI](log-into-cloud-ui.md).

7. [Change the deployment configuration](/deploy-manage/deploy/cloud-enterprise/customize-deployment.md) for the `admin-console-elasticsearch`, `logging-and-metrics`, and `security` [system deployments](/deploy-manage/deploy/cloud-enterprise/system-deployments-configuration.md) to use three availability zones and resize the nodes to use at least 4 GB of RAM. This ensures the system clusters are both highly available and sufficiently provisioned.

8. [Vacate all instances from the initial host](/deploy-manage/maintenance/ece/move-nodes-instances-from-allocators.md#move-nodes-from-allocators). This host runs some {{es}} and {{kib}} instances from system deployments, which must be moved to other allocators before proceeding.

    Wait until all instances have been moved off the initial host before continuing.

9. [Remove the `allocator` and `proxy` roles](/deploy-manage/deploy/cloud-enterprise/assign-roles-to-hosts.md) from the initial host. You cannot remove the `allocator` role until all instances have been vacated.

    ::::{note}
    After removing the proxy role from the first host, the {{es}} and {{kib}} URLs shown in the Cloud UI will stop working. This happens because the **Deployment domain name** in **Platform** > **Settings** is set to the IP address of the first host, in the format `FIRST_HOST_IP.ip.es.io`. For more details, refer to [Change endpoint URLs](./change-endpoint-urls.md).

    To resolve this, follow the steps in [Post-installation steps](./post-installation-steps.md) to complete the integration between your load balancer, ECE proxies, TLS certificates, and wildcard DNS record.
    ::::

    ::::{tip}
    If you don't yet have a load balancer, TLS certificates, or a wildcard DNS record ready, you can [change the endpoint URL](./change-endpoint-urls.md) to the IP address of one of the ECE proxies, using the format `PROXY_IP.ip.es.io`. This will allow you to continue using the deployment endpoint URLs provided by the Cloud UI.
    ::::

Once the installation is complete, you can continue with [](./post-installation-steps.md).
