---
navigation_title: SUSE
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-hosts-sles12-cloud.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-hosts-sles12-onprem.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Configure a SUSE host [ece-configure-hosts-sles12]

SUSE Linux Enterprise Server (SLES) hosts use `zypper` to install Docker and require XFS quotas to be set up manually, since SLES doesn't ship XFS as the default filesystem. The procedure below targets SLES 15. SLES 12 SP5 reached general support end of life in October 2024 — new {{ece}} installations should use SLES 15, and existing SLES 12 SP5 hosts should be migrated.

Always cross-check your SLES version and Docker version against the [Support matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise) before installing. The commands shown on this page are examples; substitute the versions you've selected from the support matrix.

* [Install Docker](#ece-install-docker-sles12)
* [Set up XFS quotas](#ece-xfs-setup-sles12)
* [Update the configurations settings](#ece-update-config-sles)
* [Configure the Docker daemon options](#ece-configure-docker-daemon-sles12)

## Install Docker on SLES [ece-install-docker-sles12]

::::{include} /deploy-manage/deploy/_snippets/ece-supported-combinations.md
::::

::::{warning}
SLES 12 SP5 reached general support end of life on **October 31, 2024**. New {{ece}} deployments should target SLES 15. Existing SLES 12 SP5 hosts should be migrated to a supported SLES 15 release.
::::

1. Remove Docker and any previously installed podman packages (if previously installed).

    ```sh
    sudo zypper remove -y docker docker-ce podman podman-remote
    ```

2. Update packages to the latest available versions.

    ```sh
    sudo zypper refresh
    sudo zypper update -y
    ```

3. Install Docker and other required packages on SLES 15. The following command is an example of installing Docker {{ece-docker-version}}. If you decide to install a different Docker version, replace `{{ece-docker-version}}` with the desired version from the [Support matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise).

    ```sh
    sudo zypper install -y curl device-mapper lvm2 net-tools docker={{ece-docker-version}}.*
    ```

    ::::{tip}
    If `zypper` reports that the requested Docker version isn't available, ensure that the SUSE **Containers Module** is enabled, or refer to [SUSE's documentation](https://documentation.suse.com/sles/15-SP6/html/SLES-all/cha-docker-installation.html) for adding the upstream Docker repository.
    ::::

    ::::{note}
    Installation on SLES 12 SP5 is no longer covered here because SLES 12 SP5 is past general support end of life. If you're maintaining an existing SLES 12 SP5 deployment, install the last Docker version that SUSE shipped for SLES 12 SP5 and plan a migration to SLES 15.
    ::::

4. Set up the OS groups and add your user.

    1. Create the `elastic` and `docker` groups if they don't already exist:

        ```sh
         sudo groupadd elastic
         sudo groupadd docker
        ```

    2. Add the user to both groups:

        ```sh
         sudo usermod -aG elastic,docker $USER
        ```

5. Disable nscd, as it interferes with Elastic's services:

    ```sh
    sudo systemctl stop nscd
    sudo systemctl disable nscd
    ```

## Set up XFS quotas [ece-xfs-setup-sles12]

XFS is required to support disk space quotas for {{es}} data directories. Some Linux distributions such as RHEL and Rocky Linux already provide XFS as the default file system. On SLES 15, you need to set up an XFS file system and have quotas enabled.

Disk space quotas set a limit on the amount of disk space an {{es}} cluster node can use. Currently, quotas are calculated by a static ratio of 1:32, which means that for every 1 GB of RAM a cluster is given, a cluster node is allowed to consume 32 GB of disk space.

::::{note}
Using LVM, `mdadm`, or a combination of the two for block device management is possible, but the configuration is not covered here, nor is it provided as part of supporting ECE.
::::

::::{important}
You must use XFS and have quotas enabled on all allocators, otherwise disk usage won't display correctly.
::::

**Example:** Set up XFS on a single, pre-partitioned block device named `/dev/xvdg1`. Replace `/dev/xvdg1` in the following example with the corresponding device on your host.

1. Format the partition:

    ```sh
    sudo mkfs.xfs /dev/xvdg1
    ```

2. Create the `/mnt/data/` directory as a mount point:

    ```sh
    sudo install -o $USER -g elastic -d -m 700 /mnt/data
    ```

3. Add an entry to the `/etc/fstab` file for the new XFS volume. The default filesystem path used by ECE is `/mnt/data`.

    ```sh
    /dev/xvdg1	/mnt/data	xfs	defaults,pquota,prjquota,x-systemd.automount  0 0
    ```

4. Regenerate the mount files:

    ```sh
    sudo mount -a
    ```

## Update the configurations settings [ece-update-config-sles]

1. Stop the Docker service:

    ```sh
    sudo systemctl stop docker
    ```

2. Enable cgroup accounting for memory and swap space.

    1. In the `/etc/default/grub` file, ensure that the `GRUB_CMDLINE_LINUX=` variable includes these values:

        ```sh
        cgroup_enable=memory swapaccount=1 cgroup.memory=nokmem
        ```

    2. Update your Grub configuration:

        ```sh
        sudo update-bootloader
        ```

3. Configure kernel parameters.

    ```sh
    cat <<EOF | sudo tee -a /etc/sysctl.conf
    # Required by Elasticsearch
    vm.max_map_count=1048576
    # enable forwarding so the Docker networking works as expected
    net.ipv4.ip_forward=1
    # Decrease the maximum number of TCP retransmissions to 5 as recommended for Elasticsearch TCP retransmission timeout.
    # See https://www.elastic.co/guide/en/elasticsearch/reference/current/system-config-tcpretries.html
    net.ipv4.tcp_retries2=5
    # Make sure the host doesn't swap too early
    vm.swappiness=1
    EOF
    ```

    ::::{important}
    The `net.ipv4.tcp_retries2` setting applies to all TCP connections and affects the reliability of communication with systems other than {{es}} clusters too. If your clusters communicate with external systems over a low quality network then you may need to select a higher value for `net.ipv4.tcp_retries2`.
    ::::

    1. Apply the settings:

        ```sh
        sudo sysctl -p
        ```

4. Adjust the system limits.

    Add the following configuration values to the `/etc/security/limits.conf` file. These values are derived from our experience with the {{ecloud}} hosted offering and should be used for ECE as well.

    ::::{tip}
    If you are using a user name other than `elastic`, adjust the configuration values accordingly.
    ::::


    ```sh
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

5. NOTE: This step is optional if the Docker registry doesn't require authentication.

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

6. If you did not create the mount point earlier (if you did not set up XFS), create the `/mnt/data/` directory as a mount point:

    ```sh
    sudo install -o $USER -g elastic -d -m 700 /mnt/data
    ```

7. If you [set up a new device with XFS](#ece-xfs-setup-sles12) earlier:

    1. Mount the block device (change the device name if you use a different device than `/dev/xvdg1`):

        ```sh
        sudo mount /dev/xvdg1
        ```

    2. Set the permissions on the newly mounted device:

        ```sh
        sudo chown $USER:elastic /mnt/data
        ```

8. Create the `/mnt/data/docker` directory for the Docker service storage:

    ```sh
    sudo install -o $USER -g elastic -d -m 700 /mnt/data/docker
    ```

## Configure the Docker daemon [ece-configure-docker-daemon-sles12]

1. Edit `/etc/docker/daemon.json`, and make sure that the following configuration values are present:<br>

    ```json
    {
      "storage-driver": "overlay2",
      "bip":"172.17.42.1/16",
      "icc": false,
      "log-driver": "json-file",
      "log-opts": {
        "max-size": "500m",
        "max-file": "10"
      },
      "data-root": "/mnt/data/docker"
    }
    ```

2. The user installing ECE must have a User ID (UID) and Group ID (GID) of 1000 or higher. Make sure that the GID matches the ID of the `elastic` group created earlier (likely to be 1000). You can set this using the following command:

    ```sh
    sudo usermod -g <elastic_group_gid> $USER
    ```

3. Apply the updated Docker daemon configuration:

   * Reload the Docker daemon configuration:

        ```sh
        sudo systemctl daemon-reload
        ```

   * Restart the Docker service:

        ```sh
        sudo systemctl restart docker
        ```

   * Enable Docker to start on boot:

        ```sh
        sudo systemctl enable docker
        ```

4. Recommended: Tune your network settings.

    Create a `70-cloudenterprise.conf` file in the `/etc/sysctl.d/` file path that includes these network settings:

    ```sh
    cat << SETTINGS | sudo tee /etc/sysctl.d/70-cloudenterprise.conf
    net.ipv4.tcp_max_syn_backlog=65536
    net.core.somaxconn=32768
    net.core.netdev_max_backlog=32768
    net.ipv4.tcp_keepalive_time=1800
    net.netfilter.nf_conntrack_tcp_timeout_established=7200
    net.netfilter.nf_conntrack_max=262140
    SETTINGS
    ```

    :::{note}
    According to [{{es}} networking settings](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md), {{es}} overrides TCP keepalive settings at the socket level for its own connections:
    * If system-level values exceed 300 seconds, {{es}} automatically lowers them to 300 seconds.
    * Values below 300 seconds are used as-is.

    For non-{{es}} connections such as the proxy layer, consider reducing the following TCP keepalive parameters to detect stale network sessions and prevent firewalls from dropping silent connections:
    * `net.ipv4.tcp_keepalive_time`
    * `net.ipv4.tcp_keepalive_intvl`
    * `net.ipv4.tcp_keepalive_probes`
    :::


    1. Ensure settings in /etc/sysctl.d/*.conf are applied on boot:

        ```sh
        SCRIPT_LOCATION="/var/lib/cloud/scripts/per-boot/00-load-sysctl-settings"
        sudo sh -c "cat << EOF > ${SCRIPT_LOCATION}
        #!/bin/bash

        set -x

        lsmod | grep ip_conntrack || modprobe ip_conntrack

        sysctl --system
        EOF
        "
        sudo chmod +x ${SCRIPT_LOCATION}
        ```

5. Reboot your system to ensure that all configuration changes take effect:

    ```sh
    sudo reboot
    ```

6. If the Docker daemon is not already running, start it:

    ```sh
    sudo systemctl start docker
    ```

7. After rebooting, verify that your Docker settings persist as expected:

    ```sh
    sudo docker info | grep Root
    ```

    If the command returns `Docker Root Dir: /mnt/data/docker`, then your changes were applied successfully and persist as expected.

    If the command returns `Docker Root Dir: /var/lib/docker`, then you need to troubleshoot the previous configuration steps until the Docker settings are applied successfully before continuing with the installation process. For more information, check [Custom Docker daemon options](https://docs.docker.com/engine/admin/systemd/#/custom-docker-daemon-options) in the Docker documentation.

8. Repeat these steps on other hosts that you want to use with ECE or follow the steps in the next section to start installing {{ece}}.
