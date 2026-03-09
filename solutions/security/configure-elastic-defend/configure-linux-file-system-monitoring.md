---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/linux-file-monitoring.html
  - https://www.elastic.co/guide/en/serverless/current/security-linux-file-monitoring.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Configure Linux file system monitoring

This page explains the advanced settings which allow you to configure which filesystems {{elastic-defend}} monitors on your Linux hosts.

By default, {{elastic-defend}} monitors specific Linux filesystem types that Elastic has tested for compatibility, and ignores all others. However, you can define more granular behavior by configuring the advanced settings related to **fanotify**, a Linux feature that monitors file system events:

* Find **Policies** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
* Click a policy’s name.
* Scroll down and select **Show advanced settings**.

From here, you can change the following settings:

:::{dropdown} View monitored file systems
{{elastic-defend}} monitors the following file systems by default:

 - ext2
 - ext3
 - ext4
 - overlay
 - tmpfs
 - vfat
 - xfs
 - btrfs 
 - zfs
:::


$$$ignore-unknown-filesystems$$$

`linux.advanced.fanotify.ignore_unknown_filesystems`
:   Determines whether to ignore unrecognized file systems. Enter one of the following:

    * `true`: (Default) Monitor only Elastic-tested file systems, and ignore all others. You can still monitor or ignore specific file systems with `monitored_filesystems` and `ignored_filesystems`.
    * `false`: Monitor all filesystems except the ignored-by-default filesystems. You can still ignore specific file systems with `ignored_filesystems`.

::::{note}
Even when `ignore_unknown_filesystems` is `false`, {{elastic-defend}} still ignores specific file systems unless they're added to `linux.advanced.fanotify.monitored_filesystems`:

:::{dropdown} View ignored-by-default file systems
{{elastic-defend}} will not monitor the following file systems unless they are individually added to `linux.advanced.fanotify.monitored_filesystems`:

 - cifs
 - lustre
 - nfs
 - nfs4
 - smbfs
 - autofs
 - binfmt_misc
 - bpf
 - cgroup
 - cgroup2
 - configfs
 - debugfs
 - devpts
 - devtmpfs
 - efivarfs
 - fuse.gvfsd-fuse
 - fuse.portal
 - fusectl
 - hugetlbfs
 - inotifyfs
 - mqueue
 - nfsd
 - nsfs
 - proc
 - pstore
 - rpc_pipefs
 - securityfs
 - selinuxfs
 - sysfs
 - tracefs
:::
::::

$$$monitored-filesystems$$$

`linux.advanced.fanotify.monitored_filesystems`
:   Specifies additional file systems to monitor. Enter a comma-separated list of [file system names](/solutions/security/configure-elastic-defend/configure-linux-file-system-monitoring.md#find-file-system-names) as they appear in `/proc/filesystems` (for example: `jfs,ufs,ramfs`).

    ::::{note}
    It’s recommended to avoid monitoring network-backed file systems.
    ::::


    This setting isn’t recognized if `ignore_unknown_filesystems` is `false`, since that would mean you’re already monitoring *all* file systems.

    Entries in this setting are overridden by entries in `ignored_filesystems`.


$$$ignored-filesystems$$$

`linux.advanced.fanotify.ignored_filesystems`
:   Specifies additional filesystems to ignore. Enter a comma-separated list of [file system names](/solutions/security/configure-elastic-defend/configure-linux-file-system-monitoring.md#find-file-system-names) as they appear in `/proc/filesystems` (for example: `ext4,tmpfs`).

    Entries in this setting override entries in `monitored_filesystems` and the `linux.advanced.fanotify.ignore_unknown_filesystems: false` setting.

::::{warning}
Ignoring filesystems can create gaps in your security coverage. Use additional security layers for ignored filesystems.
::::

## Btrfs subvolume monitoring [btrfs-subvolume-monitoring]

Btrfs (B-tree file system) is a Linux file system that supports subvolumes — independent directory trees that can be mounted separately within a single file system. Some Linux distributions mount only Btrfs subvolumes without mounting the root volume.

Due to a limitation in fanotify, {{elastic-defend}} cannot directly monitor Btrfs subvolumes. Fanotify can only monitor the root of a Btrfs file system.

If your Linux hosts use Btrfs with subvolume-only mounts, you must also mount the Btrfs root volume to enable malware protection coverage. Without the root volume mounted, {{elastic-defend}} cannot detect or prevent malware on files within those subvolumes.

## Find file system names [find-file-system-names]

This section provides a few ways to determine the file system names needed for `linux.advanced.fanotify.monitored_filesystems` and `linux.advanced.fanotify.ignored_filesystems`.

In a typical setup, when you install {{agent}}, {{filebeat}} is installed alongside {{elastic-endpoint}} and will automatically ship {{elastic-endpoint}} logs to {{es}}. {{elastic-endpoint}} will generate a log message about the file that was scanned when an event occurs.

To find the system file name:

1. Find **Hosts** in the navigation menu, or search for `Security/Explore/Hosts` by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. From the Hosts page, search for `message: "Current sync path"` to reveal the file path.
3. If you have access to the endpoint, run `findmnt -o FSTYPE -T <file path>` to return the file system. For example:

    ```shell
    > findmnt -o FSTYPE -T /etc/passwd
    FSTYPE
    ext4
    ```

    This returns the file system name as `ext4`.


Alternatively, you can also find the file system name by correlating data from two other log messages:

1. Search the logs for `message: "Current fdinfo"` to reveal the `mnt_id` value of the file path. In this example, the `mnt_id` value is `29`:

    ```shell
    pos:	12288
    flags:	02500002
    mnt_id:	29
    ino:	2367737
    ```

2. Search the logs for `message: "Current mountinfo"` to reveal the file system that corresponds to the `mnt_id` value you found in the previous step:

    ```shell
    <snip>
    29 1 8:2 / / rw,relatime shared:1 - ext4 /dev/sda2 rw,errors=remount-ro
    <snip>
    ```

    The first number, `29`, is the `mnt_id`, and the first field after the hyphen (`-`) is the file system name, `ext4`.
