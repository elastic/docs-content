---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Configure {{es}} [settings]

{{es}} ships with good defaults and requires very little configuration. Most settings can be changed on a running cluster using the [Cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) API.

The configuration files should contain settings which are node-specific (such as `node.name` and paths), or settings which a node requires in order to be able to join a cluster, such as `cluster.name` and `network.host`.

:::{note}
This topic describes how to configure a self-managed {{es}} cluster. Other deployment types must be configured using different steps.

To learn how to configure `elasticsearch.yml` for other deployment types, refer to [](/deploy-manage/stack-settings.md).

JVM and log4j configuration is not available in all deployment types. To learn how to configure limited JVM options in {{eck}}, refer to [](/deploy-manage/deploy/cloud-on-k8s/manage-compute-resources.md).
:::

## Available settings

For a complete list of settings that you can apply to your {{es}} cluster, refer to the [{{es}} configuration reference](elasticsearch://reference/elasticsearch/configuration-reference/index.md).

For a list of settings that must be configured before using your cluster in production, refer to [](/deploy-manage/deploy/self-managed/important-settings-configuration.md).


## Config files [config-files-location] 

{{es}} has three configuration files:

* `elasticsearch.yml` for configuring {{es}}
* `jvm.options` for configuring {{es}} [JVM settings](elasticsearch://reference/elasticsearch/jvm-settings.md)
* `log4j2.properties` for configuring [{{es}} logging](/deploy-manage/monitor/logging-configuration/elasticsearch-log4j-configuration-self-managed.md)

These files are located in the config directory, whose default location depends on whether the installation is from an archive distribution (`tar.gz` or `zip`) or a package distribution (Debian or RPM packages).

### Archive distributions

For the archive distributions, the config directory location defaults to `$ES_HOME/config`. The location of the config directory can be changed using the `ES_PATH_CONF` environment variable:

```sh
ES_PATH_CONF=/path/to/my/config ./bin/elasticsearch
```

Alternatively, you can `export` the `ES_PATH_CONF` environment variable through the command line or through your shell profile.

### Package distributions

For the package distributions, the config directory location defaults to `/etc/elasticsearch`. 

The location of the config directory can be changed by setting the `ES_PATH_CONF` environment variable, however, setting the environment variable in your shell is not sufficient. Instead, this variable is sourced from one the following locations:

* Debian: `/etc/default/elasticsearch` 
* RPM: `/etc/sysconfig/elasticsearch` 

You need to edit the `ES_PATH_CONF=/etc/elasticsearch` entry in the relevant file for your package to change the config directory location.

## Config file format [_config_file_format] 

:::{include} _snippets/config-file-format.md
:::

## Environment variable substitution [_environment_variable_substitution] 

:::{include} _snippets/env-var-setting-subs.md
:::

## Cluster and node setting types [cluster-setting-types] 

Cluster and node settings can be categorized based on how they are configured:

### Dynamic [dynamic-cluster-setting]

:::{include} _snippets/dynamic-settings.md
:::

### Static [static-cluster-setting]

:::{include} _snippets/static-settings.md
:::

## Additional topics

Refer to the following documentation to learn how to perform key configuration tasks for {{es}}: 

* [](/deploy-manage/security.md): Learn about security features that prevent bad actors from tampering with your data, and encrypt communications to, from, and within your cluster.
* [](/deploy-manage/users-roles/cluster-or-deployment-auth.md): Set up authentication and authorization for your cluster, and learn about the underlying security technologies that {{es}} uses to authenticate and authorize requests internally and across services.
* [](/deploy-manage/api-keys.md): Authenticate and authorize programmatic access to your deployments and {{es}} resources.
* [](/deploy-manage/manage-connectors.md): Manage connection information between Elastic and third-party systems.
* [](/deploy-manage/remote-clusters.md): Enable communication between {{es}} clusters to support [cross-cluster replication](/deploy-manage/tools/cross-cluster-replication.md) and [cross-cluster search](/explore-analyze/cross-cluster-search.md).
* [](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md): Learn how to add or remove nodes to change the size and capacity of your cluster.
* [](/deploy-manage/production-guidance.md): Review tips and guidance that you can use to design a production environment that matches your workloads, policies, and deployment needs.
