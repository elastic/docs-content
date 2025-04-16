Because {{es}} runs with `systemd` and not in a terminal, the `elastic` superuser password is not output when {{es}} starts for the first time. Use the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) tool tool to set the password for the user. This only needs to be done once for the cluster, and can be done as soon as the first node is started.

```shell
bin/elasticsearch-reset-password -u elastic
```