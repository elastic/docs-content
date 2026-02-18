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


By default, {{elastic-defend}} monitors specific Linux file system types that Elastic has tested for compatibility. If your network includes nonstandard, proprietary, or otherwise unrecognized Linux file systems, you can configure the integration policy to extend monitoring and protections to those additional file systems. You can also have {{elastic-defend}} ignore unrecognized file system types if they don’t require monitoring or cause unexpected problems.

::::{warning}
Ignoring file systems can create gaps in your security coverage. Use additional security layers for any file systems ignored by {{elastic-defend}}.
::::


To monitor or ignore additional file systems, configure the following advanced settings related to **fanotify**, a Linux feature that monitors file system events. Find **Policies** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), click a policy’s name, then scroll down and select **Show advanced settings**.

::::{note}
Even when configured to monitor all file systems (`ignore_unknown_filesystems` is `false`), {{elastic-defend}} will still ignore specific file systems that Elastic has internally identified as incompatible. The following settings apply to any *other* file systems.
::::


$$$ignore-unknown-filesystems$$$

`linux.advanced.fanotify.ignore_unknown_filesystems`
:   Determines whether to ignore unrecognized file systems. Enter one of the following:

    * `true`: (Default) Monitor only Elastic-tested file systems, and ignore all others. You can still monitor or ignore specific file systems with `monitored_filesystems` and `ignored_filesystems`, respectively.
    * `false`: Monitor all file systems. You can still ignore specific file systems with `ignored_filesystems`.

    ::::{note}
    In {{stack}}, if you’ve upgraded from 8.3 or earlier, this value will be `false` for backwards compatibility. If you don’t need to monitor additional file systems, it’s recommended to change `ignore_unknown_filesystems` to `true` after upgrading.
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
:   Specifies additional file systems to ignore. Enter a comma-separated list of [file system names](/solutions/security/configure-elastic-defend/configure-linux-file-system-monitoring.md#find-file-system-names) as they appear in `/proc/filesystems` (for example: `ext4,tmpfs`).

    Entries in this setting override entries in `monitored_filesystems`.


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
