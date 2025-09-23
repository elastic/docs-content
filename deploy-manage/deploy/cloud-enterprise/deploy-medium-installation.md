---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-medium-cloud.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-medium-onprem.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Deploy a medium installation [ece-install-medium]

This type of installation is recommended for many production setups. You need:

* 3 hosts with at least 32 GB RAM each for directors and coordinators (ECE management services), and proxies
* 3 hosts with 256 GB RAM each for allocators
* 3 availability zones

:::{image} /deploy-manage/images/cloud-enterprise-ece-pb-6.png
:alt: A medium installation with nine to twelve hosts across three availability zones
:::

::::{note}
In the diagram, the Director Coordinator host in Availability zone 1, which represents the first host to be installed, has the allocator role greyed out. This host temporarily holds all roles until the other nodes are added and configured. Eventually, the allocator role will be removed from this host.
::::

## Important considerations  [ece_before_you_start_2]

* Monitor the load on proxies and make sure the volume of user requests routed by the proxies does not affect the resources available to the ECE management services.
* Note that the medium-sized {{ece}} installation separates the allocator from the director and coordinator roles (ECE management services) and the proxy roles.

**Check the recommended JVM Heap sizes**

| Service | JVM Heap Size (Xms and Xmx) |
| --- | --- |
| `runner` | 1 GB |
| `allocator` | 4 GB |
| `zookeeper` | 8 GB |
| `director` | 1 GB |
| `constructor` | 4 GB |
| `admin-console` | 8 GB |

::::{warning}
For production environments, you must define the memory settings for each role, except for the `proxy` role, as starting from ECE 2.4 the JVM proxy was replaced with a Golang-based proxy. If you don’t set any memory setting, the default values are used, which are inadequate for production environments and can lead to performance or stability issues.
::::

## Before you start

Make sure you have completed all prerequisites and environment preparations described in the [Installation overview](./install.md), and that the hosts are configured according to [](./configure-operating-system.md).

## Installation steps [ece_installation_steps_2]

1. Install {{ece}} on the first host to start a new installation with your first availability zone. This first host holds all roles to help bootstrap the rest of the installation, but you will remove some of its roles in a later step.

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --availability-zone MY_ZONE-1 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"},"zookeeper":{"xms":"8G","xmx":"8G"},"director":{"xms":"1G","xmx":"1G"},"constructor":{"xms":"4G","xmx":"4G"},"admin-console":{"xms":"8G","xmx":"8G"}}'
    ```

    After the installation completes, copy down the coordinator host IP address, user credentials, and roles token information. Keep this information safe.

2. Generate a new roles token that persists for one hour on the first host, so that other hosts can join your installation with the right role permissions in the next step (referred to as `MY_TOKEN`). The new token needs to enable the director, coordinator and proxy roles.

    ```sh
    curl -k -H 'Content-Type: application/json' -u admin:PASSWORD https://localhost:12443/api/v1/platform/configuration/security/enrollment-tokens -d '{ "persistent": false, "roles": ["director", "coordinator", "proxy"] }'
    ```

3. Install {{ece}} on a second and third host, placing them into a second and a third availability zone, and assign them the `director`, `coordinator`, and `proxy` roles. Do not assign the `allocator` role, as these hosts should not handle any user requests. Make sure you include the coordinator host IP information from step 1 and the new roles token from step 2.

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'MY_TOKEN' --roles "director,coordinator,proxy" --availability-zone MY_ZONE-2 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"zookeeper":{"xms":"8G","xmx":"8G"},"director":{"xms":"1G","xmx":"1G"},"constructor":{"xms":"4G","xmx":"4G"},"admin-console":{"xms":"8G","xmx":"8G"}}'
    ```

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'MY_TOKEN' --roles "director,coordinator,proxy" --availability-zone MY_ZONE-3 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"zookeeper":{"xms":"8G","xmx":"8G"},"director":{"xms":"1G","xmx":"1G"},"constructor":{"xms":"4G","xmx":"4G"},"admin-console":{"xms":"8G","xmx":"8G"}}'
    ```

4. To handle the {{es}} and {{kib}} workloads, install {{ece}} on a fourth, fifth, and sixth host, distributing them evenly across the existing three availability zones and assign them the `allocator` role. Make sure you include the coordinator host IP information and allocator roles token from step 1.

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'ALLOCATOR_TOKEN' --roles "allocator" --availability-zone MY_ZONE-1 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"}}'
    ```

    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'ALLOCATOR_TOKEN' --roles "allocator" --availability-zone MY_ZONE-2 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"}}'
    ```
    
    ```sh
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host HOST_IP --roles-token 'ALLOCATOR_TOKEN' --roles "allocator" --availability-zone MY_ZONE-3 --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"}}'
    ```

5. [Log into the Cloud UI](log-into-cloud-ui.md).

6. [Change the deployment configuration](/deploy-manage/deploy/cloud-enterprise/customize-deployment.md) for the `admin-console-elasticsearch`, `logging-and-metrics`, and `security` [system deployments](/deploy-manage/deploy/cloud-enterprise/system-deployments-configuration.md) to use three availability zones and resize the nodes to use at least 4 GB of RAM. This ensures the system clusters are both highly available and sufficiently provisioned.

7. [Vacate all instances from the initial host](/deploy-manage/maintenance/ece/move-nodes-instances-from-allocators.md#move-nodes-from-allocators). This host runs some {{es}} and {{kib}} instances from system deployments, which must be moved to other allocators before proceeding.

    Wait until all instances have been moved off the initial host before continuing.

8. [Remove the `allocator` role](/deploy-manage/deploy/cloud-enterprise/assign-roles-to-hosts.md) from the initial host. You cannot remove the role until all instances have been vacated.

Once the installation is complete, you can continue with [](./post-installation-steps.md).
