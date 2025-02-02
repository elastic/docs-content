---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-perform-host-maintenance.html
---

# Perform ECE hosts maintenance [ece-perform-host-maintenance]

These steps show how you can safely perform maintenance on hosts in your ECE installation. Host maintenance refers to actions that are not part of taking care of Elastic Cloud Enterprise itself and that you might need to perform for a number of different reasons, including:

* To apply urgent operating system patches or hot fixes
* To perform regularly scheduled software or hardware upgrades
* To enable new features, such as encryption of data at rest
* To meet updated installation prerequisites

You can perform these maintenance actions on the hosts in your ECE installation using one of these methods:

* [By disabling the Docker daemon (nondestructive)](#ece-perform-host-maintenance-docker-disable)
* [By deleting the host (destructive)](#ece-perform-host-maintenance-delete-runner)
* [By shutting down the host (less destructive)](#ece-perform-host-maintenance-delete-runner)

Which method you choose depends on how invasive your host maintenance needs to be. If your host maintenance could affect ECE, use the destructive method that first deletes the host from your installation. These methods include a step that moves any hosted Elasticsearch clusters and Kibana instances off the affected hosts and are generally considered safe, provided that your ECE installation still has sufficient resources available to operate after the host has been removed.


## By disabling the Docker daemon [ece-perform-host-maintenance-docker-disable] 

This method lets you perform maintenance actions on hosts without first removing the associated host from your Elastic Cloud Enterprise installation. It works by disabling the Docker daemon. The host remains a part of your ECE installation throughout these steps but will be offline and the resources it provides will not be available.

To perform host maintenance:

1. Recommended: If the host holds the allocator role and you have enough spare capacity:

    1. [Enable maintenance mode](enable-maintenance-mode.md) on the allocator.
    2. [Move all nodes off the allocator](move-nodes-instances-from-allocators.md) and to other allocators in your installation. Moving all nodes lets you retain the same level of redundancy for highly available Elasticsearch clusters and ensures that other clusters without high availability remain available.

    ::::{important} 
    Skipping Step 1 will affect the availability of clusters with nodes on the allocator.
    ::::

2. Disable the Docker daemon:

    ```sh
    sudo systemctl disable docker
    sudo systemctl disable docker.socket
    ```

3. Reboot the host:

    ```sh
    sudo reboot
    ```

4. Perform your maintenance on the host, such as patching the operating system.
5. Enable the Docker daemon:

    ```sh
    sudo systemctl enable docker
    sudo systemctl enable docker.socket
    ```

6. Reboot the host again:

    ```sh
    sudo reboot
    ```

7. If you enabled maintenance mode in Step 1: Take the allocator out of maintenance mode.
8. Optional for allocators: ECE will start using the allocator again as you create new or change existing clusters, but it will not automatically redistribute nodes to an allocator after it becomes available. If you want to move nodes back to the same allocator after host maintenance, you need to manually [move the nodes](move-nodes-instances-from-allocators.md) and specify the allocator as a target.
9. Verify that all ECE services and deployments are back up by checking that the host shows a green status in the Cloud UI.

After the host shows a green status in the Cloud UI, it is fully functional again and can be used as before.


## By deleting the host (destructive) [ece-perform-host-maintenance-delete-runner] 

This method lets you perform potentially destructive maintenance actions on hosts. It works by deleting the associated host, which removes the host from your Elastic Cloud Enterprise installation. To add the host to your ECE installation again after host maintenance is complete, you must reinstall ECE.

To perform host maintenance:

1. If the host holds the allocator role:

    1. [Enable maintenance mode](enable-maintenance-mode.md) on the allocator.
    2. [Move all nodes off the allocator](move-nodes-instances-from-allocators.md) and to other allocators in your installation. Moving all nodes lets you retain the same level of redundancy for highly available clusters and ensures that other clusters without high availability remain available.

    ::::{important} 
    Do not skip this step or you will affect the availability of clusters with nodes on the allocator. You are in the process of removing the host from your installation and whatever ECE artifacts are stored on it will be lost.
    ::::

2. [Delete the host from your ECE installation](delete-ece-hosts.md).
3. Perform the maintenance on your host, such as enabling encryption of data at rest.
4. [Reinstall ECE on the host as if it were a new host and assign the same roles as before](../../deploy/cloud-enterprise/install-ece-on-additional-hosts.md).
5. Optional for allocators: ECE will start using the allocator again as you create new or change existing clusters, but it will not automatically redistribute nodes to an allocator after it becomes available. If you want to move nodes back to the same allocator after host maintenance, you need to manually [move the nodes](move-nodes-instances-from-allocators.md) and specify the allocator as a target.

After the host shows a green status in the Cloud UI, the host is part of your ECE installation again and can be used as before.


## By shutting down the host (less destructive) [ece-perform-host-maintenance-shutdown-host] 

This method lets you perform potentially destructive maintenance actions on hosts. It works by temporarily shutting down an ECE host, e.g. for data center moves or planned power outages. It is offered as an non-guaranteed and less destructive alternative to fully [deleting a host](#ece-perform-host-maintenance-delete-runner) from your ECE installation.

To shut down the host:

1. Disable traffic from load balancers.
2. Shut down all allocators:

    1. [Enable maintenance mode](enable-maintenance-mode.md) on the allocator.
    2. [Move all nodes off the allocator](move-nodes-instances-from-allocators.md) and to other allocators in your installation. Moving all nodes lets you retain the same level of redundancy for highly available clusters and ensures that other clusters without high availability remain available.

    ::::{important} 
    Do not skip this step or you will affect the availability of clusters with nodes on the allocator. You are in the process of removing the host from your installation and whatever ECE artifacts are stored on it will be lost.
    ::::

3. Shut down all non-director hosts.
4. Shut down directors.

After performing maintenance, start up the host:

1. Start all directors.
2. Verify that there is a healthy Zookeeper quorum (at least one `zk_server_state leader`, and `zk_followers` + `zk_synced_followers` should match the number of Zookeeper followers):

    ```sh
    docker exec frc-zookeeper-servers-zookeeper sh -c 'for i in $(seq 2191 2199); do echo "$(hostname) port is $i" && echo mntr | nc localhost ${i}; done'
    ```

3. Start all remaining hosts.
4. Re-enable traffic from load balancers.

