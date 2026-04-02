{{es}} loads its configuration from the following location by default:

```sh subs=true
{{es-conf}}{{slash}}elasticsearch.yml
```

The format of this config file is explained in [](/deploy-manage/deploy/self-managed/configure-elasticsearch.md).

Any settings that can be specified in the config file can also be specified on the command line, using the `-E` syntax as follows:

```sh subs=true
.{{slash}}bin{{slash}}elasticsearch{{auto}} -Ecluster.name=my_cluster -Enode.name=node_1
```

:::{note}
Values that contain spaces must be surrounded with quotes. For instance `-Epath.logs="C:\My Logs\logs"`.
:::

:::{tip}
Typically, any cluster-wide settings (like `cluster.name`) should be added to the `elasticsearch.yml` config file, while any node-specific settings such as `node.name` could be specified on the command line.
::::