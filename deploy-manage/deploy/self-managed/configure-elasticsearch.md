---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html
---

# Configure Elasticsearch [settings]

{{es}} ships with good defaults and requires very little configuration. Most settings can be changed on a running cluster using the [Cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) API.

The configuration files should contain settings which are node-specific (such as `node.name` and paths), or settings which a node requires in order to be able to join a cluster, such as `cluster.name` and `network.host`.


## Config files location [config-files-location] 

{{es}} has three configuration files:

* `elasticsearch.yml` for configuring {{es}}
* `jvm.options` for configuring {{es}} JVM settings
* `log4j2.properties` for configuring {{es}} logging

These files are located in the config directory, whose default location depends on whether or not the installation is from an archive distribution (`tar.gz` or `zip`) or a package distribution (Debian or RPM packages).

For the archive distributions, the config directory location defaults to `$ES_HOME/config`. The location of the config directory can be changed via the `ES_PATH_CONF` environment variable as follows:

```sh
ES_PATH_CONF=/path/to/my/config ./bin/elasticsearch
```

Alternatively, you can `export` the `ES_PATH_CONF` environment variable via the command line or via your shell profile.

For the package distributions, the config directory location defaults to `/etc/elasticsearch`. The location of the config directory can also be changed via the `ES_PATH_CONF` environment variable, but note that setting this in your shell is not sufficient. Instead, this variable is sourced from `/etc/default/elasticsearch` (for the Debian package) and `/etc/sysconfig/elasticsearch` (for the RPM package). You will need to edit the `ES_PATH_CONF=/etc/elasticsearch` entry in one of these files accordingly to change the config directory location.


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

$$$dynamic-cluster-setting$$$

Dynamic
:   You can configure and update dynamic settings on a running cluster using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). You can also configure dynamic settings locally on an unstarted or shut down node using `elasticsearch.yml`.

Updates made using the cluster update settings API can be *persistent*, which apply across cluster restarts, or *transient*, which reset after a cluster restart. You can also reset transient or persistent settings by assigning them a `null` value using the API.

If you configure the same setting using multiple methods, {{es}} applies the settings in following order of precedence:

1. Transient setting
2. Persistent setting
3. `elasticsearch.yml` setting
4. Default setting value

For example, you can apply a transient setting to override a persistent setting or `elasticsearch.yml` setting. However, a change to an `elasticsearch.yml` setting will not override a defined transient or persistent setting.

::::{tip} 
If you use {{ech}}, use the [user settings](../elastic-cloud/edit-stack-settings.md) feature to configure all cluster settings. This method lets {{ech}} automatically reject unsafe settings that could break your cluster.

If you run {{es}} on your own hardware, use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) to configure dynamic cluster settings. Only use `elasticsearch.yml` for static cluster settings and node settings. The API doesn’t require a restart and ensures a setting’s value is the same on all nodes.

::::


::::{warning} 
We no longer recommend using transient cluster settings. Use persistent cluster settings instead. If a cluster becomes unstable, transient settings can clear unexpectedly, resulting in a potentially undesired cluster configuration.

::::



$$$static-cluster-setting$$$

Static
:   Static settings can only be configured on an unstarted or shut down node using `elasticsearch.yml`.

    Static settings must be set on every relevant node in the cluster.




































$$$path-settings$$$

$$$ref-saml-settings$$$

$$$ref-oidc-settings$$$

$$$ref-kerberos-settings$$$

$$$hashing-settings$$$

$$$cluster-shard-limit$$$