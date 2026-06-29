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

SUSE Linux Enterprise Server (SLES) hosts use `zypper` to install Docker. They also require manual setup of XFS quotas, since SLES doesn't ship XFS as the default file system. The steps on this page target SLES 15 SP4. 

Before installing, make sure to cross-check the compatible SLES version and Docker version combination against the [Support matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise). The commands shown on this page are examples. Substitute the versions you've identified in the support matrix.

::::{warning}
SLES 12 SP5 reached general support end of life on **October 31, 2024**. Use SLES 15 or later for new {{ece}} installations, and migrate existing SLES 12 SP5 hosts.
::::


* [Install Docker](#ece-install-docker-sles12)
* [Set up XFS quotas](#ece-xfs-setup-sles12)
* [Update the configurations settings](#ece-update-config-sles)
* [Configure the Docker daemon options](#ece-configure-docker-daemon-sles12)

## Install Docker on SLES [ece-install-docker-sles12]

::::{include} /deploy-manage/deploy/_snippets/ece-supported-combinations.md
::::



1. Remove Docker and any previously installed Podman packages.

    ```sh
    sudo zypper remove -y docker docker-ce podman podman-remote
    ```

1. Update packages to the latest available versions.

    ```sh
    sudo zypper refresh
    sudo zypper update -y
    ```

1. List the available Docker versions:

    ```sh
    sudo zypper search -s -t package --match-exact docker
    ```

    Note the version you want to install. Check the [Support matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise) for supported Docker versions for your OS. If the latest available version is compatible, you don't need to specify an explicit version in the next step.

1. Install Docker and other required packages on SLES 15. For example, to install Docker 25:

    ```sh
    sudo zypper install -y curl device-mapper lvm2 net-tools docker=25.0.6_ce-150000.207.1 <1>
    ```

    1. Replace `25.0.6_ce-150000.207.1` with the exact package version from the repository listing. Note that zypper does not support wildcards (for example, `docker=25.*`). To install the latest available version, specify `docker` without a version number.

    ::::{tip}
    If `zypper` reports that the requested Docker version isn't available, make sure the SUSE **Containers Module** is enabled. Refer to the [SUSE documentation](https://documentation.suse.com/) for instructions on adding the upstream Docker repository.
    ::::

## Prepare the user account for ECE

The following commands assume that you are logged in as the non-root user account that will run ECE. We recommend using a dedicated `elastic` user, but you can also use an existing non-root user account with a UID greater than 1000.

1. Set up the OS groups and add your user.

    1. Create the `elastic` and `docker` groups if they don't already exist:

        ```sh
        sudo groupadd elastic
        sudo groupadd docker
        ```

    1. Add the user to both groups:

        ```sh
        sudo usermod -aG elastic,docker $USER
        ```

    1. The user running ECE must have a UID and GID of at least 1000, and the primary GID must be set to the `elastic` group. To find the `elastic` group GID:

        ```sh
        grep elastic /etc/group
        ```

        Then set the user's primary group to `elastic`:

        ```sh
        sudo usermod -g <elastic_group_gid> $USER
        ```

1. Stop the `nscd` service and prevent it from starting automatically (it can interfere with Elastic services):

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
You must use XFS and have quotas enabled on all allocators. Otherwise, disk usage won't display correctly.
::::

**Example:** Set up XFS on a single, pre-partitioned block device named `/dev/xvdg1`. Replace `/dev/xvdg1` in the following example with the corresponding device on your host.

1. Format the partition:

    ```sh
    sudo mkfs.xfs /dev/xvdg1
    ```

1. Create the `/mnt/data/` directory as a mount point:

    ```sh
    sudo install -o $USER -g elastic -d -m 700 /mnt/data
    ```

1. Add an entry to the `/etc/fstab` file for the new XFS volume. The default filesystem path used by ECE is `/mnt/data`.

    ```sh
    /dev/xvdg1	/mnt/data	xfs	defaults,pquota,prjquota,x-systemd.automount  0 0
    ```

1. Regenerate the mount files:

    ```sh
    sudo mount -a
    ```

## Update the configurations settings [ece-update-config-sles]

1. Stop the Docker service:

    ```sh
    sudo systemctl stop docker
    ```

1. Enable cgroup accounting for memory and swap space.

    1. In the `/etc/default/grub` file, ensure the `GRUB_CMDLINE_LINUX=` variable includes these values:

        ```sh
        cgroup_enable=memory swapaccount=1 cgroup.memory=nokmem
        ```

    1. Update your Grub configuration:

        ```sh
        sudo update-bootloader
        ```

1. Configure kernel parameters:

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
    The `net.ipv4.tcp_retries2` setting applies to all TCP connections and also affects the reliability of communication with systems other than {{es}} clusters. If your clusters communicate with external systems over a low quality network, you might need to select a higher value for `net.ipv4.tcp_retries2`.
    ::::

    1. Apply the settings:

        ```sh
        sudo sysctl -p
        ```

1. Adjust the system limits by adding the following configuration values to the `/etc/security/limits.conf` file. These values are based on the {{ecloud}} hosted offering and should be used for ECE as well. If needed, make sure to replace `elastic` with your user name.

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

1. _If the Docker registry doesn't require authentication, skip this step._

    Authenticate the `elastic` user to pull images from the Docker registry you use, by creating the file `/home/elastic/.docker/config.json`. This file needs to be owned by the `elastic` user. If you are using a user name other than `elastic`, adjust the path accordingly.

    **Example**: If you use `docker.elastic.co`, the file content looks like this:

    ```text
    {
     "auths": {
       "docker.elastic.co": {
         "auth": "<auth-token>"
       }
     }
    }
    ```

1. If you did not create the mount point earlier (if you did not set up XFS), create the `/mnt/data/` directory as a mount point:

    ```sh
    sudo install -o $USER -g elastic -d -m 700 /mnt/data
    ```

1. If you [set up a new device with XFS](#ece-xfs-setup-sles12) earlier:

    1. Mount the block device (change the device name if you use a different device than `/dev/xvdg1`):

        ```sh
        sudo mount /dev/xvdg1
        ```

    1. Set the permissions on the newly mounted device:

        ```sh
        sudo chown $USER:elastic /mnt/data
        ```

1. Create the `/mnt/data/docker` directory for Docker storage:

    ```sh
    sudo install -o $USER -g elastic -d -m 700 /mnt/data/docker
    ```

## Configure the Docker daemon [ece-configure-docker-daemon-sles12]

1. Edit `/etc/docker/daemon.json`, and make sure the following configuration values are present:

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
      "data-root": "/mnt/data/docker",
      "default-ulimits": {
        "nofile": {
          "Name": "nofile",
          "Hard": 1024000,
          "Soft": 1024000
        },
        "memlock": {
          "Name": "memlock",
          "Hard": -1,
          "Soft": -1
        },
        "nproc": {
          "Name": "nproc",
          "Hard": -1,
          "Soft": -1
        }
      }
    }
    ```

    The `default-ulimits` setting increases the maximum number of open file descriptors available to Docker containers.

1. Apply the updated Docker daemon configuration:

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

1. For best results, tune your network settings. Create a `70-cloudenterprise.conf` file in `/etc/sysctl.d/` and include these settings:

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
    According to the [{{es}} networking settings](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md), {{es}} overrides TCP keepalive settings at the socket level for its own connections:
    * If system-level values exceed 300 seconds, {{es}} automatically lowers them to 300 seconds.
    * Values below 300 seconds are used as is.

    For non-{{es}} connections such as the proxy layer, consider reducing the following TCP keepalive parameters to detect stale network sessions and prevent firewalls from dropping silent connections:
    * `net.ipv4.tcp_keepalive_time`
    * `net.ipv4.tcp_keepalive_intvl`
    * `net.ipv4.tcp_keepalive_probes`
    :::


    1. (Optional) Ensure `/etc/sysctl.d/*.conf` settings are applied at startup:
    
        This workaround requires `cloud-init` and is only needed if the settings are not automatically applied after a reboot.

        ```sh
        sudo mkdir -p /var/lib/cloud/scripts/per-boot/
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

1. Reboot your system to ensure that all configuration changes take effect:

    ```sh
    sudo reboot
    ```

1. If the Docker daemon is not already running, start it:

    ```sh
    sudo systemctl start docker
    ```

1. After rebooting, verify your Docker settings:

    ```sh
    sudo docker info | grep Root
    ```

    If the command returns `Docker Root Dir: /mnt/data/docker`, your changes were applied successfully and persist as expected.

    If the command returns `Docker Root Dir: /var/lib/docker`, repeat the preceding configuration steps to make sure the Docker settings are applied correctly. For more information, check [Custom Docker daemon options](https://docs.docker.com/engine/admin/systemd/#/custom-docker-daemon-options) in the Docker documentation.

1. Repeat these steps on any other hosts that you want to use with ECE. To start installing {{ece}}, continue to the next section.
