By default, the {{es}} service doesn’t log information in the `systemd` journal. To enable `journalctl` logging, the `--quiet` option must be removed from the `ExecStart` command line in the `elasticsearch.service` file.

When `systemd` logging is enabled, the logging information are available using the `journalctl` commands:

To tail the journal:

```sh
sudo journalctl -f
```

To list journal entries for the elasticsearch service:

```sh
sudo journalctl --unit elasticsearch
```

To list journal entries for the elasticsearch service starting from a given time:

```sh
sudo journalctl --unit elasticsearch --since  "2016-10-30 18:17:16"
```

Check `man journalctl` or [https://www.freedesktop.org/software/systemd/man/journalctl.html](https://www.freedesktop.org/software/systemd/man/journalctl.md) for more command line options.