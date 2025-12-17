---
applies_to:
  deployment:
    self:
navigation_title: Production settings
---

# Using the Docker images in production [docker-prod-prerequisites]

The following requirements and recommendations apply when running {{es}} in Docker in production, including some guidelines outlined in [](/deploy-manage/deploy/self-managed/important-system-configuration.md).

The following requirements and recommendations apply when running {{es}} in Docker in production.

## Set `vm.max_map_count` to `1048576` [_set_vm_max_map_count_to_1048576]

The `vm.max_map_count` kernel setting must be set to `1048576` for production use.

How you set `vm.max_map_count` depends on your platform.

:::{dropdown} Linux

To view the current value for the `vm.max_map_count` setting, run:

```sh
grep vm.max_map_count /etc/sysctl.conf
vm.max_map_count=1048576
```

To apply the setting on a live system, run:

```sh
sysctl -w vm.max_map_count=1048576
```

To permanently change the value for the `vm.max_map_count` setting, update the value in `/etc/sysctl.conf`.
:::

:::{dropdown} macOS with Docker for Mac

The `vm.max_map_count` setting must be set within the xhyve virtual machine:

1. From the command line, run:

    ```sh
    screen ~/Library/Containers/com.docker.docker/Data/vms/0/tty
    ```

2. Press enter and use `sysctl` to configure `vm.max_map_count`:

    ```sh
    sysctl -w vm.max_map_count=1048576
    ```

3. To exit the `screen` session, type `Ctrl a d`.
:::

:::{dropdown} Windows and macOS with Docker Desktop

The `vm.max_map_count` setting must be set via docker-machine:

```sh
docker-machine ssh
sudo sysctl -w vm.max_map_count=1048576
```
:::

:::{dropdown} Windows with Docker Desktop WSL 2 backend

The `vm.max_map_count` setting must be set in the "docker-desktop" WSL instance before the {{es}} container will properly start. There are several ways to do this, depending on your version of Windows and your version of WSL.

If you are on Windows 10 before version 22H2, or if you are on Windows 10 version 22H2 using the built-in version of WSL, you must either manually set it every time you restart Docker before starting your {{es}} container, or (if you do not wish to do so on every restart) you must globally set every WSL2 instance to have the `vm.max_map_count` changed. This is because these versions of WSL do not properly process the /etc/sysctl.conf file.

To manually set it every time you reboot, you must run the following commands in a command prompt or PowerShell window every time you restart Docker:

```sh
wsl -d docker-desktop -u root
sysctl -w vm.max_map_count=1048576
```

If you are on these versions of WSL and you do not want to have to run those commands every time you restart Docker, you can globally change every WSL distribution with this setting by modifying your %USERPROFILE%\.wslconfig as follows:

```text
[wsl2]
kernelCommandLine = "sysctl.vm.max_map_count=1048576"
```

This will cause all WSL2 VMs to have that setting assigned when they start.

If you are on Windows 11, or Windows 10 version 22H2 and have installed the Microsoft Store version of WSL, you can modify the /etc/sysctl.conf within the "docker-desktop" WSL distribution, perhaps with commands like this:

```sh
wsl -d docker-desktop -u root
vi /etc/sysctl.conf
```

and appending a line which reads:

```text
vm.max_map_count = 1048576
```
:::


## Configuration files must be readable by the `elasticsearch` user [_configuration_files_must_be_readable_by_the_elasticsearch_user]

By default, {{es}} runs inside the container as user `elasticsearch` using uid:gid `1000:0`.

If you are bind-mounting a local directory or file, it must be readable by the `elasticsearch` user. In addition, this user must have write access to the [config, data and log dirs](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings) ({{es}} needs write access to the `config` directory so that it can generate a keystore). A good strategy is to grant group access to gid `0` for the local directory.

::::{important}
One exception is [Openshift](https://docs.openshift.com/container-platform/3.6/creating_images/guidelines.md#openshift-specific-guidelines), which runs containers using an arbitrarily assigned user ID. Openshift presents persistent volumes with the gid set to `0`, which works without any adjustments.
::::

For example, to prepare a local directory for storing data through a bind-mount:

```sh
mkdir esdatadir
chmod g+rwx esdatadir
chgrp 0 esdatadir
```

You can also run an {{es}} container using both a custom UID and GID. You must ensure that file permissions will not prevent {{es}} from executing. You can use one of two options:

* Bind-mount the `config`, `data` and `logs` directories. If you intend to install plugins and prefer not to [create a custom Docker image](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-configure.md#_c_customized_image), you must also bind-mount the `plugins` directory.
* Pass the `--group-add 0` command line option to `docker run`. This ensures that the user under which {{es}} is running is also a member of the `root` (GID 0) group inside the container.


## Increase ulimits for nofile and nproc [_increase_ulimits_for_nofile_and_nproc]

Increased ulimits for [nofile](setting-system-settings.md) and [nproc](/deploy-manage/deploy/self-managed/bootstrap-checks.md#max-number-threads-check) must be available for the {{es}} containers. Verify the [init system](https://github.com/moby/moby/tree/ea4d1243953e6b652082305a9c3cda8656edab26/contrib/init) for the Docker daemon sets them to acceptable values.

To check the Docker daemon defaults for ulimits, run:

::::{tab-set}
:group: docker
:::{tab-item} Latest
:sync: latest
```sh subs=true
docker run --rm docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}} /bin/bash -c 'ulimit -Hn && ulimit -Sn && ulimit -Hu && ulimit -Su'
```
:::

:::{tab-item} Specific version
:sync: specific
Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
```sh subs=true
docker run --rm docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER> /bin/bash -c 'ulimit -Hn && ulimit -Sn && ulimit -Hu && ulimit -Su'
```
:::
::::

If needed, adjust them in the Daemon or override them per container. For example, when using `docker run`, set:

```sh
--ulimit nofile=65535:65535
```


## Disable swapping [_disable_swapping]

Swapping needs to be disabled for performance and node stability. For information about ways to do this, see [Disable swapping](setup-configuration-memory.md).

If you opt for the `bootstrap.memory_lock: true` approach, you also need to define the `memlock: true` ulimit in the [Docker Daemon](https://docs.docker.com/engine/reference/commandline/dockerd/#default-ulimits), or explicitly set for the container as shown in the  [sample compose file](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-compose.md). When using `docker run`, you can specify:

```sh
-e "bootstrap.memory_lock=true" --ulimit memlock=-1:-1
```


## Randomize published ports [_randomize_published_ports]

The image [exposes](https://docs.docker.com/engine/reference/builder/#/expose) TCP ports 9200 and 9300. For production clusters, randomizing the published ports with `--publish-all` is recommended, unless you are pinning one container per host.


## Manually set the heap size [docker-set-heap-size]

By default, {{es}} automatically sizes JVM heap based on a nodes’s [roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles) and the total memory available to the node’s container. We recommend this default sizing for most production environments. If needed, you can override default sizing by manually setting JVM heap size.

To manually set the heap size in production, bind mount a [JVM options](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-options) file under `/usr/share/elasticsearch/config/jvm.options.d` that includes your desired [heap size](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-heap-size) settings.

For testing, you can also manually set the heap size using the `ES_JAVA_OPTS` environment variable. For example, to use 1GB, use the following command.

::::{tab-set}
:group: docker
:::{tab-item} Latest
:sync: latest
```sh subs=true
docker run -e ES_JAVA_OPTS="-Xms1g -Xmx1g" -e ENROLLMENT_TOKEN="<token>" --name es01 -p 9200:9200 --net elastic -it docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
```
:::

:::{tab-item} Specific version
:sync: specific
Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
```sh subs=true
docker run -e ES_JAVA_OPTS="-Xms1g -Xmx1g" -e ENROLLMENT_TOKEN="<token>" --name es01 -p 9200:9200 --net elastic -it docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER>
```
:::
::::

The `ES_JAVA_OPTS` variable overrides all other JVM options. We do not recommend using `ES_JAVA_OPTS` in production.


## Pin deployments to a specific image version [_pin_deployments_to_a_specific_image_version]

Pin your deployments to a specific version of the {{es}} Docker image. For example:

::::{tab-set}
:group: docker
:::{tab-item} Latest
:sync: latest
```sh subs=true
docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
```
:::

:::{tab-item} Specific version
:sync: specific
Replace `<SPECIFIC.VERSION.NUMBER>`  with the version of the Docker image you downloaded.
```sh subs=true
docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER>
```
:::
::::


## Always bind data volumes [_always_bind_data_volumes]

You should use a volume bound to `/usr/share/elasticsearch/data` for the following reasons:

1. The data of your {{es}} node won’t be lost if the container is deleted.
2. {{es}} is I/O sensitive and the Docker storage driver is not ideal for fast I/O.
3. It allows the use of advanced [Docker volume plugins](https://docs.docker.com/engine/extend/plugins/#volume-plugins).


## Avoid using `loop-lvm` mode [_avoid_using_loop_lvm_mode]

If you are using the devicemapper storage driver, do not use the default `loop-lvm` mode. Configure docker-engine to use [direct-lvm](https://docs.docker.com/engine/userguide/storagedriver/device-mapper-driver/#configure-docker-with-devicemapper).


## Centralize your logs [_centralize_your_logs]

Consider centralizing your logs by using a different [logging driver](https://docs.docker.com/engine/admin/logging/overview/). Also note that the default json-file logging driver is not ideally suited for production use.
