# {{es}} service user requirements [elasticsearch-service-user]

{{es}} must run under an appropriate user account with specific permissions and consistent configuration across all nodes in your cluster. 
This page describes the requirements for the user account that runs the {{es}} service.

RPM and Debian packages automatically create the `elasticsearch` user and group automatically during installation. For `.tar.gz` or `.zip` installations, create the user manually before starting {{es}}.

## Don't run as root

Elastic recommends that you avoid running commands as the `root` user. Instead, create a dedicated, unprivileged user account to run the service, such as `elasticsearch` for example.

## Use consistent user and group IDs across nodes

Ensure that the `elasticsearch` user has the same *numeric* UID and GID on every node in your cluster.

This is especially important if you use NFS or another shared file system. Many NFS implementations match accounts by numeric UID and GID, not by name. 
If the `elasticsearch` account has different numeric IDs on different nodes, you might encounter permission errors when using shared file system snapshot repositories.

For more information, refer to [Troubleshooting a shared file system repository](/deploy-manage/tools/snapshot-and-restore/shared-file-system-repository.md#_troubleshooting_a_shared_file_system_repository).

## Required system resource limits

Processes running as the `elasticsearch` user must be configured with the following system resource limits: 

| Permission | Minimum value | Details |
| --- | --- | --- |
| Open file descriptors (`nofile`) | 65,535 | [File descriptors](/deploy-manage/deploy/self-managed/file-descriptors.md) |
| Max threads (`nproc`) | 4,096 | [Max number of threads](/deploy-manage/deploy/self-managed/max-number-of-threads.md) |
| Memory lock (`memlock`) | `unlimited` | [Disable swapping](/deploy-manage/deploy/self-managed/setup-configuration-memory.md) |
| Max file size (`fsize`) | `unlimited` | [Bootstrap checks](/deploy-manage/deploy/self-managed/bootstrap-checks.md) |
| Virtual memory (`as`) | `unlimited` | [Bootstrap checks](/deploy-manage/deploy/self-managed/bootstrap-checks.md) |

For instructions on configuring these, refer to [Configure system settings](/deploy-manage/deploy/self-managed/setting-system-settings.md).

## File and directory ownership and permissions

The {{es}} user must be able to read the configuration and write to data and log directories. Verify ownership and permissions after installation and before starting the service. RPM and Debian packages set correct ownership automatically.