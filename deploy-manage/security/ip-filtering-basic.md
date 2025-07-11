---
navigation_title: In ECK and Self Managed
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ip-filtering.html
applies_to:
  deployment:
    self:
    eck:
products:
  - id: elasticsearch
---

# Manage IP filtering in ECK and self-managed clusters

You can apply IP filtering to application clients, node clients, or transport clients, remote cluster clients, in addition to other nodes that are attempting to join the cluster.

If a node’s IP address is on the denylist, the {{es}} {{security-features}} allow the connection to {{es}} but it is be dropped immediately and no requests are processed.

:::{note}
{{es}} installations are not designed to be publicly accessible over the Internet. IP filtering and the other capabilities of the {{es}} {{security-features}} do not change this condition.
:::

:::{include} _snippets/eck-traffic-filtering.md
:::

## Enable IP filtering

The {{es}} {{security-features}} contain an access control feature that allows or rejects hosts, domains, or subnets. If the [{{operator-feature}}](/deploy-manage/users-roles/cluster-or-deployment-auth/operator-privileges.md) is enabled, only operator users can update these settings.

You configure IP filtering by specifying the `xpack.security.transport.filter.allow` and `xpack.security.transport.filter.deny` settings in [`elasticsearch.yml`](/deploy-manage/stack-settings.md). Allow rules take precedence over the deny rules.

:::{important}
Unless explicitly specified, `xpack.security.http.filter.*` and `xpack.security.remote_cluster.filter.*` settings default to the corresponding `xpack.security.transport.filter.*` setting’s value.
:::


```yaml
xpack.security.transport.filter.allow: "192.168.0.1"
xpack.security.transport.filter.deny: "192.168.0.0/24"
```

The `_all` keyword can be used to deny all connections that are not explicitly allowed.

```yaml
xpack.security.transport.filter.allow: [ "192.168.0.1", "192.168.0.2", "192.168.0.3", "192.168.0.4" ]
xpack.security.transport.filter.deny: _all
```

IP filtering configuration also support IPv6 addresses.

```yaml
xpack.security.transport.filter.allow: "2001:0db8:1234::/48"
xpack.security.transport.filter.deny: "1234:0db8:85a3:0000:0000:8a2e:0370:7334"
```

You can also filter by hostnames when DNS lookups are available.

```yaml
xpack.security.transport.filter.allow: localhost
xpack.security.transport.filter.deny: '*.google.com'
```


## Disable IP filtering

Disabling IP filtering can slightly improve performance under some conditions. To disable IP filtering entirely, set the value of the `xpack.security.transport.filter.enabled` setting in the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) configuration file to `false`.

```yaml
xpack.security.transport.filter.enabled: false
```

You can also disable IP filtering for the transport protocol but enable it for HTTP only.

```yaml
xpack.security.transport.filter.enabled: false
xpack.security.http.filter.enabled: true
```


## Specify TCP transport profiles

[TCP transport profiles](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#transport-profiles) enable {{es}} to bind on multiple hosts. The {{es}} {{security-features}} enable you to apply different IP filtering on different profiles.

```yaml
xpack.security.transport.filter.allow: 172.16.0.0/24
xpack.security.transport.filter.deny: _all
transport.profiles.client.xpack.security.filter.allow: 192.168.0.0/24
transport.profiles.client.xpack.security.filter.deny: _all
```

:::{note}
When you do not specify a profile, `default` is used automatically.
:::



## HTTP filtering

You may want to have different IP filtering for the transport and HTTP protocols.

```yaml
xpack.security.transport.filter.allow: localhost
xpack.security.transport.filter.deny: '*.google.com'
xpack.security.http.filter.allow: 172.16.0.0/16
xpack.security.http.filter.deny: _all
```


## Remote cluster (API key based model) filtering

If other clusters connect [using API key authentication](/deploy-manage/remote-clusters/remote-clusters-api-key.md) for {{ccs}} or {{ccr}}, you may want to have different IP filtering for the remote cluster server interface.

```yaml
xpack.security.remote_cluster.filter.allow: 192.168.1.0/8
xpack.security.remote_cluster.filter.deny: 192.168.0.0/16
xpack.security.transport.filter.allow: localhost
xpack.security.transport.filter.deny: '*.google.com'
xpack.security.http.filter.allow: 172.16.0.0/16
xpack.security.http.filter.deny: _all
```

:::{note}
Whether IP filtering for remote cluster is enabled is controlled by `xpack.security.transport.filter.enabled` as well. This means filtering for the remote cluster and transport interfaces must be enabled or disabled together. But the exact allow and deny lists can be different between them.
:::

## Dynamically update IP filter settings

In case of running in an environment with highly dynamic IP addresses like cloud based hosting, it is very hard to know the IP addresses upfront when provisioning a machine. Instead of changing the configuration file and restarting the node, you can use the Cluster Update Settings API. For example:

```console
PUT /_cluster/settings
{
  "persistent" : {
    "xpack.security.transport.filter.allow" : "172.16.0.0/24"
  }
}
```

You can also dynamically disable filtering completely:

```console
PUT /_cluster/settings
{
  "persistent" : {
    "xpack.security.transport.filter.enabled" : false
  }
}
```

:::{note}
To avoid locking yourself out of the cluster, the default bound transport address will never be denied. This means you can always SSH into a system and use curl to apply changes.
:::