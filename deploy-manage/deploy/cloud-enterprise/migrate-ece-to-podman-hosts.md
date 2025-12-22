---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-migrate-to-podman.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Migrate ECE to Podman hosts [ece-migrate-to-podman]

This section provides guidelines and recommendations for migrating an existing platform to a Podman-based environment. You have an existing ECE installation version >=3.0 and want to migrate all hosts to use Podman as a container runtime. The recommended approach consists of three (3) high-level steps.

**Step 1**: Upgrade ECE to version >= 3.3.0 following the [Upgrade your installation](../../upgrade/orchestrator/upgrade-cloud-enterprise.md) guidelines. Skip this step if your ECE installation is already running a version >= 3.3.0.

**Step 2**: Prepare an additional RHEL or Rocky Linux VM. We recommend using one additional VM to perform a rolling grow-and-shrink upgrade.

**Step 3**: Migrate each host one by one from Docker to Podman. This allows you to move workloads from Docker-based hosts to Podman-based ones without downtime. We highly recommend to allocate the additional Podman allocator to the same zone as the Docker allocator you want to replace. **Assuming there is sufficient capacity**, you may use existing docker-based hosts as the "new" Podman-based hosts.  To reuse a host, you will first follow the steps to [delete a host from the ECE deployment](../../maintenance/ece/delete-ece-hosts.md) followed by the steps [to remove ECE software from the host](../../uninstall/uninstall-elastic-cloud-enterprise.md). The following diagram shows the conceptual steps.

::::{note}
Using Docker or Podman as container runtime is a configuration local to the host. For example, the admin console is not aware which allocator is using Podman. Hence there is no restriction on the migration ordering of the hosts.  This applies to all host role types.
::::


:::{image} /deploy-manage/images/cloud-enterprise-podman-migration-overview-1.png
:alt: Migration Overview
:::

::::{note}
* When copy-pasting commands, verify that characters like quotes (“) are encoded correctly in the console where you copy the command to.
* Steps that run commands starting with `sudo` can be run as any sudoers user. Otherwise, the corresponding user is mentioned as part of the step description.
* Avoid customizing the host Docker path `/mnt/data/docker` when using SELinux. Otherwise the ECE installer script needs to be adjusted.
::::

1. Make sure you are running a healthy x-node ECE environment ready to be upgraded. All nodes use the Docker container runtime.
2. Upgrade to ECE 3.3.0+ following the [Upgrade your installation](../../upgrade/orchestrator/upgrade-cloud-enterprise.md) guideline. Skip this step if your existing ECE installation already runs ECE >= 3.3.0.
3. Follow your internal guidelines to add an additional vanilla RHEL (Note that the version must be >= 8.5, but <9), or Rocky Linux 8 or 9 VM to your environment.
4. Verify that required traffic from the host added in step 3 is allowed to the primary ECE VM(s). Check the [Networking prerequisites](ece-networking-prereq.md) and [Google Cloud Platform (GCP)](/deploy-manage/deploy/cloud-enterprise/prepare-environment.md) guidelines for a list of ports that need to be open. The technical configuration highly depends on the underlying infrastructure.

    **Example** For AWS, allowing traffic between hosts is implemented using security groups.

5. Identify the host you want to replace with a podman-based host and copy the associated roles.

    **Example 1** You want to migrate the Docker host `192.168.44.74` with the role `Allocator` to a podman host. Copy the role `allocator`.

    :::{image} /deploy-manage/images/cloud-enterprise-podman-migration-fetch-roles-1.png
    :alt: Migrate Allocator
    :::

    **Example 2** You want to migrate the Docker host `192.168.44.10` with the roles `Allocator`, `Controller`, `Director`, and `Proxy` to a podman host. Copy the roles `allocator`, `coordinator`, `director`, `proxy`.

    :::{image} /deploy-manage/images/cloud-enterprise-podman-migration-fetch-roles-2.png
    :alt: Migrate Allocator
    :::

    ::::{important}
    The role `Controller` in the admin console is called `coordinator` for the `elastic-cloud-enterprise.sh` script
    ::::

6. Configure the RHEL or Rocky Linux host.

1. Install the OS packages `lvm2`, `iptables`, `sysstat`, and `net-tools` by executing:

    ```sh
    sudo dnf install lvm2 iptables sysstat net-tools <1>
    ```

    1. The ECE diagnostic script requires `net-tools`.<br>


    ::::{note}
    For RHEL 9 and Rocky Linux 9, also install the `containernetworking-plugins` package using:<br>

    ```sh
    sudo dnf -y install containernetworking-plugins
    ```

    ::::

2. Remove Docker and previously installed podman packages (if previously installed).

    ```sh
    sudo dnf remove docker docker-ce podman podman-remote containerd.io
    ```

3. As a sudoers user, edit the `/etc/selinux/config` file:

    1. If you are not using SELinux, set it to permissive mode:

        ```text
        SELINUX=permissive
        ```

    2. If you are using SELinux, set it to enforcing mode:

        ::::{note}
        Avoid customizing the host Docker path `/mnt/data/docker` when using SELinux. Otherwise the ECE installer script needs to be adjusted.
        ::::


        ```text
        SELINUX=enforcing
        ```

4. Install Podman:

    * For Podman 4

        * Install the latest available version `4.*` using dnf.

            ```sh
            sudo dnf install podman-4.* podman-remote-4.*
            ```

        * To prevent automatic Podman major version updates, configure the Podman version to be locked at version `4.*` while still allowing minor and patch updates.

            ```sh
            ## Install versionlock
            sudo dnf install 'dnf-command(versionlock)'

            ## Lock major version
            sudo dnf versionlock add --raw 'podman-4.*'
            sudo dnf versionlock add --raw 'podman-remote-4.*'

            ## Verify that podman-4.* and podman-remote-4.* appear in the output
            sudo dnf versionlock list
            ```

    * For Podman 5

        * Install the latest available version `5.*` using dnf.

            :::{note}
            Podman versions `5.2.2-11` and `5.2.2-13` are affected by a known [memory leak issue](https://github.com/containers/podman/issues/25473). To avoid this bug, use a later version. Refer to the official [Support matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise) for more information.
            :::

            ```sh
            sudo dnf install podman-5.* podman-remote-5.*
            ```

        * To prevent automatic Podman major version updates, configure the Podman version to be locked at version `5.*` while still allowing minor and patch updates.

            ```sh
            ## Install versionlock
            sudo dnf install 'dnf-command(versionlock)'

            ## Lock major version
            sudo dnf versionlock add --raw 'podman-5.*'
            sudo dnf versionlock add --raw 'podman-remote-5.*'

            ## Verify that podman-5.* and podman-remote-5.* appear in the output
            sudo dnf versionlock list
            ```

5. [This step is for RHEL 9 and Rocky Linux 9 only] Switch the network stack from Netavark to CNI:

    1. If the */etc/containers/containers.conf* file does not exist, copy the */usr/share/containers/containers.conf* file to the */etc/containers/* directory (for example, using `cp /usr/share/containers/containers.conf /etc/containers/`).
    2. Open the */etc/containers/containers.conf* file. Navigate to the **network** section and make sure that the **network_backend** setting is set to `cni`.
    3. Reboot the system (`reboot`).
    4. Check that the network stack has changed to `cni`: <br>

        ```sh
        cat /etc/containers/containers.conf
        [...]
        [network]
        network_backend="cni"
        [...]
        ```

6. If podman requires a proxy in your infrastructure setup, modify the `/usr/share/containers/containers.conf` file and add the `HTTP_PROXY` and `HTTPS_PROXY` environment variables in the [engine] section. Note that multiple env variables in that configuration file exists — use the one in the [engine] section.

    Example:

    ```text
    [engine]
    env = ["HTTP_PROXY=http://<PROXY_IP>:<PROXY_PORT>", "HTTPS_PROXY=http://<PROXY_IP>:<PROXY_PORT>"]
    ```

7. Reload systemd configuration

    ```sh
    sudo systemctl daemon-reload
    ```

8. Create OS groups, if they do not exist yet

    Reference: [Users and permissions](ece-users-permissions.md)

    ```sh
    sudo groupadd elastic
    sudo groupadd podman
    ```

9. Add user `elastic` to the `podman` group

    Reference: [Users and permissions](ece-users-permissions.md)

    ```sh
    sudo useradd -g "elastic" -G "podman" elastic
    ```

10. As a sudoers user, add the following line to /etc/sudoers.d/99-ece-users

    Reference: [Users and permissions](ece-users-permissions.md)

    ```text
    elastic ALL=(ALL) NOPASSWD:ALL
    ```

11. Add the required options to the kernel boot arguments

    ```sh
    sudo /sbin/grubby --update-kernel=ALL --args='cgroup_enable=memory cgroup.memory=nokmem swapaccount=1'
    ```

12. Create the directory

    ```sh
    sudo mkdir -p /etc/systemd/system/podman.socket.d
    ```

13. As a sudoers user, create the file `/etc/systemd/system/podman.socket.d/podman.conf` with the following content. Set the correct ownership and permission.

    ::::{important}
    Both `ListenStream=` and `ListenStream=/var/run/docker.sock` parameters are required!
    ::::


    File content:

    ```text
    [Socket]
    ListenStream=
    ListenStream=/var/run/docker.sock
    SocketMode=770
    SocketUser=elastic
    SocketGroup=podman
    ```

    File ownership and permission:

    ```sh
    sudo chown root:root /etc/systemd/system/podman.socket.d/podman.conf
    sudo chmod 0644 /etc/systemd/system/podman.socket.d/podman.conf
    ```

14. As a sudoers user, create the (text) file `/usr/bin/docker` with the following content. Verify that the regular double quotes in the text file are used (ASCII code Hex 22)

    ```text
    #!/bin/bash
    podman-remote --url unix:///var/run/docker.sock "$@"
    ```

15. Set the file permissions on `/usr/bin/docker`

    ```sh
    sudo chmod 0755 /usr/bin/docker
    ```

16. As a sudoers user, add the following two lines to section `[storage]` in the file `/etc/containers/storage.conf`. Verify that those parameters are only defined once. Either remove or comment out potentially existing parameters.

    ::::{note}
    Avoid customizing the host Docker path `/mnt/data/docker` when using SELinux. Otherwise the ECE installer script needs to be adjusted.
    ::::


    ```text
    runroot = "/mnt/data/docker/runroot/"
    graphroot = "/mnt/data/docker"
    ```

17. Enable podman so that itself and running containers start automatically after a reboot

    ```sh
    sudo systemctl enable podman.service
    sudo systemctl enable podman-restart.service
    ```

18. Enable the `overlay` kernel module (check [Use the OverlayFS storage driver](https://docs.docker.com/storage/storagedriver/overlayfs-driver/)) that the Podman `overlay` storage driver uses (check [Working with the Container Storage library and tools in Red Hat Enterprise Linux](https://www.redhat.com/en/blog/working-container-storage-library-and-tools-red-hat-enterprise-linux#:~:text=Storage%20Configuration)).

    In the Docker world there are two overlay drivers, overlay and overlay2. Today most users use the overlay2 driver, so we just use that one, and called it overlay. Refer also to [Use the OverlayFS storage driver](https://docs.docker.com/storage/storagedriver/overlayfs-driver/).

    ```sh
    echo "overlay" | sudo tee -a /etc/modules-load.d/overlay.conf
    ```

19. Format the additional data partition

    ```sh
    sudo mkfs.xfs /dev/nvme1n1
    ```

20. Create the `/mnt/data/` directory used as a mount point

    ```sh
    sudo install -o elastic -g elastic -d -m 700 /mnt/data
    ```

21. As a sudoers user, modify the entry for the XFS volume in the `/etc/fstab` file to add `pquota,prjquota`. The default filesystem path used by {{ece}} is `/mnt/data`.

    ::::{note}
    Replace `/dev/nvme1n1` in the following example with the corresponding device on your host, and add this example configuration as a single line to `/etc/fstab`.
    ::::


    ```text
    /dev/nvme1n1	/mnt/data	xfs	defaults,nofail,x-systemd.automount,prjquota,pquota  0 2
    ```

22. Restart the local-fs target

    ```sh
    sudo systemctl daemon-reload
    sudo systemctl restart local-fs.target
    ```

23. Set the permissions on the newly mounted device

    ```sh
    ls /mnt/data
    sudo chown elastic:elastic /mnt/data
    ```

24. Create the `/mnt/data/docker` directory for the Docker service storage

    ::::{note}
    Avoid customizing the host Docker path `/mnt/data/docker` when using SELinux. Otherwise the ECE installer script needs to be adjusted.
    ::::


    ```sh
    sudo install -o elastic -g elastic -d -m 700 /mnt/data/docker
    ```

25. If you want to use FirewallD, ensure you meet the [networking prerequisites](ece-networking-prereq.md). Otherwise, you can disable it with:

    ```sh
    sudo systemctl disable firewalld
    ```

    ::::{note}
    If FirewallD does not exist on your VM, you can skip this step.
    ::::

26. Configure kernel parameters

    ```sh
    cat <<EOF | sudo tee -a /etc/sysctl.conf
    # Required by Elasticsearch
    vm.max_map_count=1048576
    # enable forwarding so the Docker networking works as expected
    net.ipv4.ip_forward=1
    # Decrease the maximum number of TCP retransmissions to 5 as recommended for Elasticsearch TCP retransmission timeout.
    # See /deploy-manage/deploy/self-managed/system-config-tcpretries.md
    net.ipv4.tcp_retries2=5
    # Make sure the host doesn't swap too early
    vm.swappiness=1
    EOF
    ```

27. Apply the new sysctl settings

    ```sh
    sudo sysctl -p
    sudo systemctl restart NetworkManager
    ```

28. As a sudoers user, adjust the system limits. Add the following configuration values to the `/etc/security/limits.conf` file.

    ```text
    *                soft    nofile         1024000
    *                hard    nofile         1024000
    *                soft    memlock        unlimited
    *                hard    memlock        unlimited
    elastic          soft    nofile         1024000
    elastic          hard    nofile         1024000
    elastic          soft    memlock        unlimited
    elastic          hard    memlock        unlimited
    elastic          soft    nproc          unlimited
    elastic          hard    nproc          unlimited
    root             soft    nofile         1024000
    root             hard    nofile         1024000
    root             soft    memlock        unlimited
    ```

29. NOTE: This step is optional if the Docker registry doesn’t require authentication.

    Authenticate the `elastic` user to pull images from the Docker registry you use, by creating the file `/home/elastic/.docker/config.json`. This file needs to be owned by the `elastic` user. If you are using a user name other than `elastic`, adjust the path accordingly.

    **Example**: In case you use `docker.elastic.co`, the file content looks like as follows:

    ```text
    {
     "auths": {
       "docker.elastic.co": {
         "auth": "<auth-token>"
       }
     }
    }
    ```

30. Restart the podman service by running this command:

    ```sh
    sudo systemctl daemon-reload
    sudo systemctl restart podman
    ```

31. Reboot the RHEL host

    ```sh
    sudo reboot
    ```

    1. Use the ECE installer script together with the `--podman` flag to add the additional host as a podman-based host.

        Refer to the official [Install {{ece}} on an additional host](install-ece-on-additional-hosts.md) and [Install ECE online](./install.md) documentation to adapt the command line parameters to your environment including fetching the role token.

        [JVM heap sizes](ece-jvm.md) describes recommended JVM options.

        Important while running `./elastic-cloud-enterprise.sh`

        * Make sure you use `--podman` on the podman host.
        * Make sure you use `--selinux` on the Podman host if SELinux runs in `enforcing` mode.
        * To fetch a role token following the [Generate Roles Tokens](generate-roles-tokens.md) guidelines, you need to send a JSON token to the admin console. Double check the correct format of the roles. Roles are a list of individual strings in quotes, **NOT a single string**.

            For **example 1**, the JSON object is as follows:

            ```json
            '{ "persistent": true, "roles": [ "allocator" ] }'
            ```

            For **example 2**, the JSON object is as follows:

            ```json
            '{ "persistent": true, "roles": [ "allocator","coordinator","director","proxy" ] }'
            ```

        * The ECE version of the additional host must be the same as the version used in step 2. Use `--cloud-enterprise-version VERSION_NAME` to specify the correct version.
        * To easily identify the podman allocator, apply a tag to the additional host, for example `containerengine:podman`. The podman allocator is needed as the “target allocator” when you later move instances from the Docker allocator to the podman allocator.  For example, use `--allocator-tags containerengine:podman`.
        * Make sure to apply the roles as copied in step 5 to the additional host. The value for the `--roles` flag is a single string.

            For **example 1** in step 4, use `--roles "allocator"`

            For **example 2** in step 4, use `--roles "allocator,coordinator,director,proxy"`

        * Add the new host to the same availability zone as the Docker host you want to replace. Use the `--availability-zone <zone>` flag.

    2. Login to admin console

        Verify that the new podman host has the same roles (same coloring of the hexagon) as the Docker host you want to replace.

        The following screenshot shows the state where the correct roles have been applied. Both hosts in ece-zone-1 have the same color.

        :::{image} /deploy-manage/images/cloud-enterprise-podman-migration-correct-role-1.png
        :alt: Correct role
        :::

        The following screenshot shows the state where incorrect roles have been applied. The hosts in ece-zone-1 do not have the same coloring.

        :::{image} /deploy-manage/images/cloud-enterprise-podman-migration-wrong-role-1.png
        :alt: Wrong role
        :::

    3. Put the docker-based allocator you want to replace with a podman allocator in maintenance mode by following the [Enable Maintenance Mode](../../maintenance/ece/enable-maintenance-mode.md) documentation.

        As an alternative, use the [Start maintenance mode](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-start-allocator-maintenance-mode) API.

    4. Move all instances from the Docker allocator to the podman allocator by following the [Move Nodes From Allocators](../../maintenance/ece/move-nodes-instances-from-allocators.md) documentation.

        ::::{important}
        Make sure to specify the target podman allocator using the option “Set target allocators”.
        ::::


        ::::{important}
        If you move admin console instances, you might update the URL in the browser before continuing with step 11.
        ::::


        :::{image} /deploy-manage/images/cloud-enterprise-podman-migration-move-instances-1.png
        :alt: Move instances
        :::

        As an alternative, use the [*Move clusters*](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-move-clusters) API.

        To identifying the correct target allocator, the following APIs might be helpful:

        * [*Get allocators*](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-get-allocators)
        * [*Get allocator metadata*](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-get-allocator-metadata)

            ```json
            {
              "allocator_id": "192.168.44.17",
              "zone_id": "ece-zone-1",
              "host_ip": "192.168.44.17",
              "public_hostname": "192.168.44.17",
              "capacity": {
                  "memory": {
                      "total": 26000,
                      "used": 0
                  }
              },
              "settings": {},
              "instances": [],
              "metadata": [
                  { <1>
                      "key": "containerengine",
                      "value": "podman"
                  }
              ]
            }
            ```

            1. If allocators are tagged as mentioned in step 7, the metadata section of the [*Get allocators*](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-get-allocators)  API should contain the tag.


            This information allows you to determine what allocators are running on top of podman (automated way)

    5. Remove the Docker allocator by following the [Delete Hosts](../../maintenance/ece/delete-ece-hosts.md) guidelines.

    As an alternative, use the [Delete Runner](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-delete-runner) API.

::::{note}
When using Podman, removing an image with the `--force` (`-f`) option not only deletes the image reference but also removes any containers that depend on that image. This behavior differs from Docker, where forced image removal does not automatically remove running or stopped containers. Therefore, avoid using the `--force` (`-f`) option with the `docker rmi` command.
::::
