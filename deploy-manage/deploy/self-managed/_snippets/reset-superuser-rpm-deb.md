Because {{es}} runs with `systemd` and not in a terminal, the `elastic` superuser password is not output when {{es}} starts for the first time. Use the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) tool tool to set the password for the user:

```shell
bin/elasticsearch-reset-password -u elastic
```