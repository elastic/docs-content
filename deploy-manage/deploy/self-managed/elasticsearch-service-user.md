---
description: Requirements for the user account that runs the Elasticsearch service, including identity, kernel resource limits, and file ownership.
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
type: overview
---

# {{es}} service user requirements [elasticsearch-service-user]

{{es}} must run under an appropriate user account with specific permissions and consistent configuration across all nodes in your cluster. 
This page describes the requirements for the user account that runs the {{es}} service.

RPM and Debian packages automatically create the `elasticsearch` user and group during installation. For `.tar.gz` or `.zip` installations, create the user manually before starting {{es}}.

## Don't run as a privileged user

Elastic recommends that you avoid running commands as a privileged user:

* On Linux and macOS, do not run {{es}} as the `root` user. Instead, create a dedicated, unprivileged user account to run the service, such as `elasticsearch`.
* On Windows, do not run {{es}} as the `Administrator` user. Instead, create a dedicated, unprivileged user account to run the service.

## Use consistent user and group IDs across nodes

:::{note}
This section applies to Linux and MacOS only.
:::

Ensure that the `elasticsearch` user has the same *numeric* UID and GID on every node in your cluster.

This is especially important if you use NFS or another shared file system. Many NFS implementations match accounts by numeric UID and GID, not by name. If the `elasticsearch` account has different numeric IDs on different nodes, you might encounter permission errors when using shared file system snapshot repositories.

For more information, refer to [Troubleshooting a shared file system repository](/deploy-manage/tools/snapshot-and-restore/shared-file-system-repository.md#_troubleshooting_a_shared_file_system_repository).

## Kernel resource limits for the {{es}} process

:::{note}
This section applies to Linux and MacOS only. On Windows, the JVM manages most of these resources directly and no user-level configuration is required.
:::

{{es}} requires several kernel-level resource limits, such as open file descriptors, max threads, and memory lock, to be raised above their defaults. The kernel enforces these limits per process based on the user that spawned it, so they must be configured for the `elasticsearch` user. The [important system configuration](/deploy-manage/deploy/self-managed/important-system-configuration.md) section covers each limit and its required value.

For instructions on applying these limits using `ulimit`, `/etc/security/limits.conf`, or `systemd`, refer to [Configure system settings](/deploy-manage/deploy/self-managed/setting-system-settings.md).

## File and directory ownership and permissions

The {{es}} user must be able to read the configuration and write to data and log directories. Verify ownership and permissions after installation and before starting the service. RPM and Debian packages set correct ownership and permissions automatically.

For the default directory paths and their expected ownership, refer to the directory layout for your installation method:

* [`.tar.gz` archive on Linux or macOS](/deploy-manage/deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos.md#targz-layout)
* [`.zip` archive on Windows](/deploy-manage/deploy/self-managed/install-elasticsearch-with-zip-on-windows.md#windows-layout)
* [Debian](/deploy-manage/deploy/self-managed/install-elasticsearch-with-debian-package.md#deb-layout)
* [RPM](/deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md#rpm-layout)
* [Docker](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-prod.md#_configuration_files_must_be_readable_by_the_elasticsearch_user)