---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html
applies_to:
  deployment:
    self:
---

# Configure {{es}} [settings]

{{es}} ships with good defaults and requires very little configuration. Most settings can be changed on a running cluster using the [Cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) API.

The configuration files should contain settings which are node-specific (such as `node.name` and paths), or settings which a node requires in order to be able to join a cluster, such as `cluster.name` and `network.host`.

## Available settings

For a complete list of settings that you can apply to your {{es}} cluster, refer to the [Elasticsearch configuration reference](elasticsearch://reference/elasticsearch/configuration-reference/index.md).

For a list of settings that must be configured before using your cluster in production, refer to [](/deploy-manage/deploy/self-managed/important-settings-configuration.md).


## Config files [config-files-location] 

{{es}} has three configuration files:

* `elasticsearch.yml` for configuring {{es}}
* `jvm.options` for configuring {{es}} JVM settings
* `log4j2.properties` for configuring {{es}} logging

These files are located in the config directory, whose default location depends on whether or not the installation is from an archive distribution (`tar.gz` or `zip`) or a package distribution (Debian or RPM packages).

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

The configuration format is [YAML](https://yaml.org/). Here is an example of changing the path of the data and logs directories:

```yaml
path:
    data: /var/lib/elasticsearch
    logs: /var/log/elasticsearch
```

Settings can also be flattened as follows:

```yaml
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
```

In YAML, you can format non-scalar values as sequences:

```yaml
discovery.seed_hosts:
   - 192.168.1.10:9300
   - 192.168.1.11
   - seeds.mydomain.com
```

Though less common, you can also format non-scalar values as arrays:

```yaml
discovery.seed_hosts: ["192.168.1.10:9300", "192.168.1.11", "seeds.mydomain.com"]
```


## Environment variable substitution [_environment_variable_substitution] 

Environment variables referenced with the `${...}` notation within the configuration file will be replaced with the value of the environment variable. For example:

```yaml
node.name:    ${HOSTNAME}
network.host: ${ES_NETWORK_HOST}
```

Values for environment variables must be simple strings. Use a comma-separated string to provide values that {{es}} will parse as a list. For example, {{es}} will split the following string into a list of values for the `${HOSTNAME}` environment variable:

```yaml
export HOSTNAME="host1,host2"
```

## Cluster and node setting types [cluster-setting-types] 

Cluster and node settings can be categorized based on how they are configured:

### Dynamic [dynamic-cluster-setting]

You can configure and update dynamic settings on a running cluster using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). You can also configure dynamic settings locally on an unstarted or shut down node using `elasticsearch.yml`.

Updates made using the cluster update settings API can be *persistent*, which apply across cluster restarts, or *transient*, which reset after a cluster restart. You can also reset transient or persistent settings by assigning them a `null` value using the API.

If you configure the same setting using multiple methods, {{es}} applies the settings in following order of precedence:

1. Transient setting
2. Persistent setting
3. `elasticsearch.yml` setting
4. Default setting value

For example, you can apply a transient setting to override a persistent setting or `elasticsearch.yml` setting. However, a change to an `elasticsearch.yml` setting will not override a defined transient or persistent setting.

Use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) to configure dynamic cluster settings. Only use `elasticsearch.yml` for static cluster settings and node settings. The API doesn’t require a restart and ensures a setting’s value is the same on all nodes.

::::{warning} 
We no longer recommend using transient cluster settings. Use persistent cluster settings instead. If a cluster becomes unstable, transient settings can clear unexpectedly, resulting in a potentially undesired cluster configuration.
::::


### Static [static-cluster-setting]

Static settings can only be configured on an unstarted or shut down node using `elasticsearch.yml`.

Static settings must be set on every relevant node in the cluster.

## Additional topics

Refer to the following documentation to learn how to perform key configuration tasks for {{es}}: 

* [](/deploy-manage/security.md): Learn about security features that prevent bad actors from tampering with your data, and encrypt communications to, from, and within your cluster.
* [](/deploy-manage/users-roles/cluster-or-deployment-auth.md): Set up authentication and authorization for your cluster, and learn about the underlying security technologies that {{es}} uses to authenticate and authorize requests internally and across services.
* [](/deploy-manage/api-keys.md): Authenticate and authorize programmatic access to your deployments and {{es}} resources.
* [](/deploy-manage/manage-connectors.md): Manage connection information between Elastic and third-party systems.
* [](/deploy-manage/remote-clusters.md): Enable communication between {{es}} clusters to support [cross-cluster replication](/deploy-manage/tools/cross-cluster-replication.md) and [cross-cluster search](/solutions/search/cross-cluster-search.md).
* [](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md): Learn how to add or remove nodes to change the size and capacity of your cluster.
* [](/deploy-manage/production-guidance.md): Review tips and guidance that you can use to design a production environment that matches your workloads, policies, and deployment needs.