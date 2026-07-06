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

This guide explains how to prepare a SUSE Linux Enterprise Server (SLES) host for an {{ece}} (ECE) installation. It covers the operating system configuration required before you install ECE, including Docker installation, XFS quota configuration, and other host-specific settings.

SLES hosts use `zypper` to install Docker and require manual XFS quota setup because XFS is not the default filesystem on SLES. The steps on this page target SLES 15 SP4.

::::{warning}
SLES 12 SP5 reached general support end of life on **October 31, 2024**. Use SLES 15 or later for new {{ece}} installations, and migrate existing SLES 12 SP5 hosts.
::::

* [Prerequisites](#ece-configure-host-suse-prerequisites)
* [Prepare the user account for ECE](#ece-prepare-user-sles)
* [Install Docker](#ece-install-docker-sles12)
* [Set up XFS quotas](#ece-xfs-setup-sles12)
* [Prepare the data directories](#ece-prepare-data-directories-sles)
* [Update the system configuration](#ece-update-config-sles)
* [Configure the Docker daemon options](#ece-configure-docker-daemon-sles12)
* [Verify the host configuration](#ece-verify-host-config-sles)
* [Next steps](#ece-configure-host-suse-next-steps)

## Prerequisites [ece-configure-host-suse-prerequisites]

Before you begin:

- Identify a supported SLES and Docker version combination in the [Support matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise). Substitute the example versions in this guide with the versions listed there.

- Verify that required traffic is allowed. Check the [Networking prerequisites](ece-networking-prereq.md) for a list of ports that need to be open. The technical configuration depends on the underlying infrastructure.

- Review the [Users and permissions prerequisites](ece-users-permissions.md) for ECE. The commands in this guide assume that you are logged in as the non-root user that will install and run ECE. We recommend using a dedicated `elastic` user account. If it does not already exist, you can create it in the next section.

- If you use one user to prepare the host and another to install ECE, replace `$USER` with the name of the ECE user in the applicable commands throughout this guide.

## Prepare the user account for ECE [ece-prepare-user-sles]

Follow these steps to configure the user account according to the [Users and permissions prerequisites](ece-users-permissions.md) for a SLES host.

1. Set up the OS groups and add your user.

    1. Create the `elastic` and `docker` groups if they don't already exist:

        ```sh
        sudo groupadd elastic
        sudo groupadd docker
        ```

    1. (Optional) Create a dedicated user for ECE:

        If the user you are currently logged in as is not the user that will install and run ECE, create a dedicated user. The following example creates the recommended `elastic` user:

        ```sh
        sudo useradd -m -g elastic -G docker elastic
        ```

        ::::{note}
        If you create a dedicated user, we recommend granting it `sudo` privileges and then logging in or switching to that user before continuing. This allows `$USER` to automatically resolve to the user that will install and run ECE.

        Alternatively, you can continue using a different account with `sudo` privileges, and replace `$USER` with the name of the user that will install and run ECE in the remaining commands in this guide.
        ::::

    1. Add the user to both groups:

        ```sh
        sudo usermod -aG elastic,docker $USER
        ```

1. Verify that the user that will run ECE has a UID and GID of at least 1000:

    ```sh
    id $USER
    ```

    The output should show a `uid` and `gid` value of `1000` or higher.

1. Verify that the user's primary group is `elastic`:

    ```sh
    id -gn $USER
    ```

    If the command doesn't return `elastic`, find the `elastic` group GID:

    ```sh
    grep elastic /etc/group
    ```

    Then set the user's primary group to `elastic`:

    ```sh
    sudo usermod -g <elastic_group_gid> $USER
    ```

## Install Docker on SLES [ece-install-docker-sles12]

::::{include} /deploy-manage/deploy/_snippets/ece-supported-combinations.md
::::

1. Remove Docker and any previously installed Podman packages:

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

1. Ensure Docker is stopped before continuing. Docker is started later after the daemon configuration is updated:

    ```sh
    sudo systemctl stop docker
    ```

## Set up XFS quotas [ece-xfs-setup-sles12]

{{ece}} relies on XFS project quotas to manage disk space for {{es}} data directories. These quotas limit the amount of disk space available to each {{es}} cluster node based on the RAM-to-disk ratio defined by its [instance configuration](deployment-templates.md#ece-getting-started-instance-configurations). For example, the default `data.default` instance configuration uses a 1:32 ratio, allowing 32 GB of disk space for every 1 GB of RAM assigned to a cluster node.

To use disk quotas, the file system mounted at `/mnt/data` must be an XFS file system with project quotas enabled. This guide creates a dedicated XFS file system for `/mnt/data`, which is the recommended configuration. If `/mnt/data` already resides on an XFS file system with project quotas enabled, you can skip the file system creation steps.

::::{note}
You can use LVM, `mdadm`, or a combination of the two for block device management. However, their configuration is outside the scope of this guide and is not covered by ECE support.
::::

::::{important}
You must use XFS and have quotas enabled on all allocators. Otherwise, disk usage won't display correctly.
::::

**Example:** Set up XFS on a single, pre-partitioned block device named `/dev/xvdg1`. Replace `/dev/xvdg1` in the following example with the corresponding device on your host.

1. Format the partition:

    ```sh
    sudo mkfs.xfs /dev/xvdg1
    ```

1. Add an entry to the `/etc/fstab` file for the new XFS volume. The default filesystem path used by ECE is `/mnt/data`.

    ```sh
    /dev/xvdg1	/mnt/data	xfs	defaults,pquota,prjquota,x-systemd.automount  0 0
    ```

## Prepare the data directories [ece-prepare-data-directories-sles]

Prepare the data directories used by {{ece}} and Docker. These steps create the `/mnt/data` and `/mnt/data/docker` directories, mount an XFS file system if applicable, and apply the required ownership and permissions.

1. Create the `/mnt/data` directory if it doesn't already exist:

    ```sh
    sudo install -o $USER -g elastic -d -m 700 /mnt/data
    ```

1. If you configured a dedicated XFS file system in [Set up XFS quotas](#ece-xfs-setup-sles12):

    1. Mount the file system configured in `/etc/fstab`:

        ```sh
        sudo mount -a
        ```

    1. Set the ownership and permissions for `/mnt/data`:

        Mounting the XFS file system for the first time replaces the original mount point. Reapply the required ownership and permissions to the mounted file system.

        ```sh
        sudo chown $USER:elastic /mnt/data
        sudo chmod 700 /mnt/data
        ```

1. Create the `/mnt/data/docker` directory for Docker storage:

    ```sh
    sudo install -o $USER -g elastic -d -m 700 /mnt/data/docker
    ```

## Configure system settings [ece-update-config-sles]

1. Stop the `nscd` service and prevent it from starting automatically. This service can interfere with Elastic services.

    ```sh
    sudo systemctl stop nscd
    sudo systemctl disable nscd
    ```

1. Enable cgroup accounting for memory and swap space:

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

1. Optional: Tune additional network kernel parameters for production workloads. Create a `70-cloudenterprise.conf` file in `/etc/sysctl.d/` and include these settings:

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

    Apply the settings:

    ```sh
    sudo sysctl --system
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

## Configure the Docker daemon [ece-configure-docker-daemon-sles12]

1. Edit `/etc/docker/daemon.json` to make sure the following configuration values are present:

    ```json
    {
      "storage-driver": "overlay2",
      "bip":"172.17.42.1/16",
      "icc": false,
      "log-driver": "json-file",
      "log-opts": { <1>
        "max-size": "500m",
        "max-file": "10"
      },
      "data-root": "/mnt/data/docker",
      "default-ulimits": { <2>
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
    1. The `max-size` and `max-file` options configure rotation for the `json-file` logs created by each container. Adjust these values to match your logging requirements.
    2. The `default-ulimits` setting increases the maximum number of open file descriptors available to Docker containers.

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

1. Enable Docker to start on boot:

    ```sh
    sudo systemctl enable docker
    ```

1. Apply the updated Docker daemon configuration:

   * Reload the Docker daemon configuration:

        ```sh
        sudo systemctl daemon-reload
        ```

   * Restart the Docker service:

        ```sh
        sudo systemctl restart docker
        ```

## Verify the host configuration [ece-verify-host-config-sles]

Reboot the host and verify that the required system, storage, and Docker configuration has been applied successfully.

1. Reboot your system to ensure that all configuration changes take effect:

    ```sh
    sudo reboot
    ```

    Then log in again as your ECE user.

1. Verify that the Docker daemon started automatically:

    ```sh
    sudo systemctl status docker
    ```

    If Docker is not running, review your Docker installation and daemon configuration.

1. After rebooting, verify your Docker settings:

    ```sh
    docker info | grep Root
    ```

    If the command returns `Docker Root Dir: /mnt/data/docker`, your changes were applied successfully and persist as expected.

    If the command returns `Docker Root Dir: /var/lib/docker`, review [Configure the Docker daemon](#ece-configure-docker-daemon-sles12) to make sure the Docker settings are applied correctly. For more information, check [Custom Docker daemon options](https://docs.docker.com/engine/admin/systemd/#/custom-docker-daemon-options) in the Docker documentation.

    If the command returns a permission denied error, make sure your user is a member of the `docker` group.

1. Verify that the required kernel parameters are applied:

    ```sh
    sudo sysctl vm.max_map_count net.ipv4.ip_forward net.ipv4.tcp_retries2 vm.swappiness
    ```

    The output should include the following values:

    ```sh
    vm.max_map_count = 1048576
    net.ipv4.ip_forward = 1
    net.ipv4.tcp_retries2 = 5
    vm.swappiness = 1
    ```

1. Verify that memory cgroup accounting is enabled:

    ```sh
    cat /proc/cmdline
    ```

    Verify that the output includes the following kernel parameters:

    ```text
    cgroup_enable=memory swapaccount=1 cgroup.memory=nokmem
    ```

1. Verify the limits configured for the ECE user:

    ```sh
    sudo su - elastic -c 'ulimit -n && ulimit -l && ulimit -u' <1>
    ```
    1. Replace `elastic` with your ECE user if you are using a different user name.

    The output should show:

    ```text
    1024000
    unlimited
    unlimited
    ```

1. Verify default limits applied to Docker containers:

    ```sh
    docker run --rm alpine sh -c 'ulimit -n && ulimit -l && ulimit -u'
    ```

    The output should show:

    ```text
    1024000
    unlimited
    unlimited
    ```

1. Verify that `/mnt/data` is mounted with XFS:

    ```sh
    findmnt -no TARGET,FSTYPE,OPTIONS /mnt/data
    ```

    The output should show `/mnt/data` as an `xfs` file system with project quotas enabled.

1. Verify the ownership and permissions of the data directory:

    ```sh
    stat -c "%U:%G %a %n" /mnt/data
    ```

    The output should show that the directory is by the ECE user and the `elastic` group, and use `700` permissions.

## Next steps [ece-configure-host-suse-next-steps]

Repeat these host preparation steps for every host that you want to use with {{ece}}. After preparing and verifying all hosts, continue to [Installation procedures](install-ece-procedures.md) to install {{ece}}.
