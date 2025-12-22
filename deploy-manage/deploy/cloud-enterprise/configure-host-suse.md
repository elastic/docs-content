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

The following instructions explain how to prepare your hosts on SUSE Linux Enterprise Server 12 SP5 (SLES 12) or 15 (SLES 15).

* [Install Docker](#ece-install-docker-sles12)
* [Set up XFS quotas](#ece-xfs-setup-sles12)
* [Update the configurations settings](#ece-update-config-sles)
* [Configure the Docker daemon options](#ece-configure-docker-daemon-sles12)

If you want to install {{ece}} (ECE) on your own hosts, the steps for preparing your hosts can take a bit of time. There are two ways you can approach this:

* **Think like a minimalist**: [Install the correct version of Docker](#ece-install-docker-sles12) on hosts that meet the [prerequisites](prepare-environment.md) for ECE, then skip ahead and [install ECE](install.md#install-ece). Be aware that some checks during the installation can fail with this approach, which will mean doing further host preparation work before retrying the installation.
* **Cover your bases**: If you want to make absolutely sure that your installation of {{ece}} can succeed on hosts that meet the [prerequisites](prepare-environment.md), or if any of the checks during the installation failed previously, run through the full preparation steps in this section and then and [install ECE](install.md#install-ece). You’ll do a bit more work now, but life will be simpler later on.

Regardless of which approach you take, the steps in this section need to be performed on every host that you want to use with ECE.

## Install Docker on SLES [ece-install-docker-sles12]

::::{include} /deploy-manage/deploy/_snippets/ece-supported-combinations.md
::::


1. Remove Docker and previously installed podman packages (if previously installed).

    ```sh
    sudo zypper remove -y docker docker-ce podman podman-remote
    ```

2. Update packages to the latest available versions

    ```sh
    sudo zypper refresh
    sudo zypper update -y
    ```

3. Install Docker and other required packages:

    * For SLES 12:

        ```sh
        sudo zypper install -y docker=24.0.7_ce-98.109.3
        ```

    * For SLES 15:

        ```sh
        sudo zypper install -y curl device-mapper lvm2 net-tools docker=24.0.7_ce-150000.198.2 net-tools
        ```

4. Disable nscd, as it interferes with Elastic’s services:

    ```sh
    sudo systemctl stop nscd
    sudo systemctl disable nscd
    ```



## Set up OS groups and user [ece_set_up_os_groups_and_user]

1. If they don’t already exist, create the following OS groups:

    ```sh
     sudo groupadd elastic
     sudo groupadd docker
    ```

2. Add the user to these groups:

    ```sh
     sudo usermod -aG elastic,docker $USER
    ```



## Set up XFS quotas [ece-xfs-setup-sles12]

XFS is required to support disk space quotas for {{es}} data directories. Some Linux distributions such as RHEL and Rocky Linux already provide XFS as the default file system. On SLES 12 and 15, you need to set up an XFS file system and have quotas enabled.

Disk space quotas set a limit on the amount of disk space an {{es}} cluster node can use. Currently, quotas are calculated by a static ratio of 1:32, which means that for every 1 GB of RAM a cluster is given, a cluster node is allowed to consume 32 GB of disk space.

::::{note}
Using LVM, `mdadm`, or a combination of the two for block device management is possible, but the configuration is not covered here, nor is it provided as part of supporting ECE.
::::


::::{important}
You must use XFS and have quotas enabled on all allocators, otherwise disk usage won’t display correctly.
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

3. Configure kernel parameters

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
        sudo service network restart
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

5. NOTE: This step is optional if the Docker registry doesn’t require authentication.

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

2. The user installing ECE must have a User ID (UID) and Group ID (GID) of 1000 or higher. Make sure that the GID matches the ID of the `elastic`` group created earlier (likely to be 1000). You can set this using the following command:

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

    1. Ensure settings in /etc/sysctl.d/*.conf are applied on boot

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
