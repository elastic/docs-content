---
navigation_title: Ubuntu
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-hosts-ubuntu-cloud.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-hosts-ubuntu-onprem.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Configure an Ubuntu host [ece-configure-hosts-ubuntu]

The following instructions show you how to prepare your hosts on Ubuntu.

* [Install Docker](#ece-install-docker-ubuntu)
* [Set up XFS quotas](#ece-xfs-setup-ubuntu)
* [Update the configurations settings](#ece-update-config-ubuntu)
* [Configure the Docker daemon options](#ece-configure-docker-daemon-ubuntu)


## Install Docker on Ubuntu [ece-install-docker-ubuntu]

Install a compatible Docker version on Ubuntu.

::::{include} /deploy-manage/deploy/_snippets/ece-supported-combinations.md
::::


1. Install the Docker repository dependencies:

    ```sh
    sudo apt-get install ca-certificates curl gnupg lsb-release
    ```

2. Add Docker’s official GPG key:

    ```sh
    sudo mkdir -m 0755 -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    ```

3. Add the stable Docker repository:

    ```sh
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

4. Install the correct version of the `docker-ce` package. The following is an example of installing Docker 27.0. If you decide to install a different Docker version, make sure to replace with the desired version in the commands below.

    ```sh
    sudo apt update && sudo apt install -y docker-ce=5:27.0.* docker-ce-cli=5:27.0.* containerd.io
    ```



## Set up XFS quotas [ece-xfs-setup-ubuntu]

XFS is required to support disk space quotas for {{es}} data directories. Some Linux distributions such as RHEL and Rocky Linux already provide XFS as the default file system. On Ubuntu, you need to set up an XFS file system and have quotas enabled.

Disk space quotas set a limit on the amount of disk space an {{es}} cluster node can use. Currently, quotas are calculated by a static ratio of 1:32, which means that for every 1 GB of RAM a cluster is given, a cluster node is allowed to consume 32 GB of disk space.

::::{note}
Using LVM, `mdadm`, or a combination of the two for block device management is possible, but the configuration is not covered here, and it is not supported by {{ece}}.
::::


::::{important}
You must use XFS and have quotas enabled on all allocators, otherwise disk usage won’t display correctly.
::::


**Example:** Set up XFS on a single, pre-partitioned block device named `/dev/xvdg1`.

1. Format the partition:

    ```sh
    sudo mkfs.xfs /dev/xvdg1
    ```

2. Create the `/mnt/data/` directory as a mount point:

    ```sh
    sudo install -o $USER -g $USER -d -m 700 /mnt/data
    ```

3. Add an entry to the `/etc/fstab` file for the new XFS volume. The default filesystem path used by {{ece}} is `/mnt/data`.

    ```sh
    /dev/xvdg1	/mnt/data	xfs	defaults,nofail,x-systemd.automount,prjquota,pquota  0 2
    ```

4. Regenerate the mount files:

    ```sh
    sudo systemctl daemon-reload
    sudo systemctl restart local-fs.target
    ```



## Update the configurations settings [ece-update-config-ubuntu]

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
        sudo update-grub
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
        ```

4. Adjust the system limits.

    Add the following configuration values to the `/etc/security/limits.conf` file. These values are derived from our experience with the {{ecloud}} hosted offering and should be used for {{ece}} as well.

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
    sudo install -o $USER -g $USER -d -m 700 /mnt/data
    ```

7. If you [set up a new device with XFS](#ece-xfs-setup-ubuntu) earlier:

    1. Mount the block device (change the device name if you use a different device than `/dev/xvdg1`):

        ```sh
        sudo mount /dev/xvdg1 /mnt/data
        ```

    2. Set the permissions on the newly mounted device:

        ```sh
        sudo chown $USER:$USER /mnt/data
        ```

8. Create the `/mnt/data/docker` directory for the Docker service storage:

    ```sh
    sudo install -o $USER -g $USER -d -m 700 /mnt/data/docker
    ```



## Configure the Docker daemon options [ece-configure-docker-daemon-ubuntu]

::::{tip}
Docker creates a bridge IP address that can conflict with IP addresses on your internal network. To avoid an IP address conflict, change the `--bip=172.17.42.1/16` parameter in our examples to something that you know will work. If there is no conflict, you can omit the `--bip` parameter. The `--bip` parameter is internal to the host and can be set to the same IP for each host in the cluster. More information on Docker daemon options can be found in the  [dockerd command line reference](https://docs.docker.com/engine/reference/commandline/dockerd/).
::::


::::{tip}
You can specify `--log-opt max-size` and `--log-opt max-file` to define the Docker daemon containers log rotation.
::::


1. Update `/etc/systemd/system/docker.service.d/docker.conf`. If the file path and file do not exist, create them first.

    ```ini
    [Unit]
    Description=Docker Service
    After=multi-user.target

    [Service]
    Environment="DOCKER_OPTS=-H unix:///run/docker.sock --data-root /mnt/data/docker --storage-driver=overlay2 --bip=172.17.42.1/16 --raw-logs --log-opt max-size=500m --log-opt max-file=10 --icc=false"
    ExecStart=
    ExecStart=/usr/bin/dockerd $DOCKER_OPTS
    ```

2. Apply the updated Docker daemon configuration:

    Reload the Docker daemon configuration:

    ```sh
    sudo systemctl daemon-reload
    ```

    Restart the Docker service:

    ```sh
    sudo systemctl restart docker
    ```

    Enable Docker to start on boot:

    ```sh
    sudo systemctl enable docker
    ```

3. Enable your user to communicate with the Docker subsystem by adding it to the `docker` group:

    ```sh
    sudo usermod -aG docker $USER
    ```

4. Recommended: Tune your network settings.

    Create a `70-cloudenterprise.conf` file in the `/etc/sysctl.d/` file path that includes these network settings:

    ```sh
    cat << SETTINGS | sudo tee /etc/sysctl.d/70-cloudenterprise.conf
    net.ipv4.tcp_max_syn_backlog=65536
    net.core.somaxconn=32768
    net.core.netdev_max_backlog=32768
    SETTINGS
    ```

5. Pin the Docker version to ensure that the package does not get upgraded:

    ```sh
    echo "docker-ce hold" | sudo dpkg --set-selections
    echo "docker-ce-cli hold" | sudo dpkg --set-selections
    echo "containerd.io hold" | sudo dpkg --set-selections
    ```

6. Reboot your system to ensure that all configuration changes take effect:

    ```sh
    sudo reboot
    ```

7. After rebooting, verify that your Docker settings persist as expected:

    ```sh
    sudo docker info | grep Root
    ```

    If the command returns `Docker Root Dir: /mnt/data/docker`, then your changes were applied successfully and persist as expected.

    If the command returns `Docker Root Dir: /var/lib/docker`, then you need to troubleshoot the previous configuration steps until the Docker settings are applied successfully before continuing with the installation process. For more information, check [Custom Docker daemon options](https://docs.docker.com/engine/admin/systemd/#/custom-docker-daemon-options) in the Docker documentation.

8. Repeat these steps on other hosts that you want to use with {{ece}} or follow the steps in the next section to start installing {{ece}}.
