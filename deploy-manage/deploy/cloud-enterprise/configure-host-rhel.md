---
navigation_title: RHEL
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-hosts-rhel-centos-cloud.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-hosts-rhel-centos-onprem.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Configure a RHEL host [ece-configure-hosts-rhel-centos]

The following instructions show you how to prepare your hosts on Red Hat Enterprise Linux 8 (RHEL 8), 9 (RHEL 9), and Rocky Linux 8 and 9.

* [Prerequisites](#ece-prerequisites-rhel8)
* [Install Podman and configure the host](#ece-configure-hosts-rhel8-podman)

## Prerequisites [ece-prerequisites-rhel8]

Follow your internal guidelines to create a RHEL 8 (the version must be >= 8.5), RHEL 9, Rocky Linux 8, or Rocky Linux 9 server or VM in your environment.

Verify that required traffic is allowed. Check the [Networking prerequisites](ece-networking-prereq.md) for a list of ports that need to be open. The technical configuration depends on the underlying infrastructure.

**Example:** For AWS, allowing traffic between hosts is implemented using security groups.

::::{include} /deploy-manage/deploy/_snippets/ece-supported-combinations.md
::::

## Install Podman and configure the host [ece-configure-hosts-rhel8-podman]

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
    vm.max_map_count=262144
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

29. Restart the podman service by running this command:

    ```sh
    sudo systemctl daemon-reload
    sudo systemctl restart podman
    ```

30. Reboot the RHEL host.

    ```sh
    sudo reboot
    ```
