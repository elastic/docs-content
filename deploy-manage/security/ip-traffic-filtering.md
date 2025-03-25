---
applies_to:
  deployment:
    ess: ga
    ece: ga
    eck: ga
    self: ga
  serverless: unavailable
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-traffic-filtering-ip.html
  - https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-ip.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-traffic-filtering-ip.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ip-filtering.html
---

# IP traffic filtering

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):













This page covers traffic filtering by IP address or CIDR block.

Other [traffic filtering](/deploy-manage/security/traffic-filtering.md) methods are available depending on your deployment type.

:::::{tab-set}
:group: deployment-type

::::{tab-item} {{ecloud}}
:sync: cloud

Traffic filtering, by IP address or CIDR block, is one of the security layers available in {{ecloud}}. It allows you to limit how your deployments can be accessed. We have two types of filters available for filtering by IP address or CIDR block: Ingress/Inbound and Egress/Outbound (Beta, API only).

* **Ingress or inbound IP filters** - These restrict access to your deployments from a set of IP addresses or CIDR blocks. These filters are available through the {{ecloud}} Console.
* **Egress or outbound IP filters** - These restrict the set of IP addresses or CIDR blocks accessible from your deployment. These might be used to restrict access to a certain region or service. This feature is in beta and is currently only available through the [Traffic Filtering API](/deploy-manage/security/ec-traffic-filtering-through-the-api.md).

Read more about [Traffic Filtering](/deploy-manage/security/traffic-filtering.md) for the general concepts behind traffic filtering.

Follow the step described here to set up ingress or inbound IP filters through the {{ecloud}} Console.


**1. Create an IP filter rule set**

You can combine any rules into a set, so we recommend that you group rules according to what they allow, and make sure to label them accordingly. Since multiple sets can be applied to a deployment, you can be as granular in your sets as you feel is necessary.

To create a rule set:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.
3. Under the **Features** tab, open the **Traffic filters** page.
4. Select **Create filter**.
5. Select **IP filtering rule set**.
6. Create your rule set, providing a meaningful name and description.
7. Select the region for the rule set.
8. Select if this rule set should be automatically attached to new deployments.

    ::::{note} 
    Each rule set is bound to a particular region and can be only assigned to deployments in the same region.
    ::::

9. Add one or more rules using IPv4, or a range of addresses with CIDR.

    ::::{note} 
    DNS names are not supported in rules.
    ::::


The next step is to associate one or more rule-sets with your deployments.

$$$ech-associate-traffic-filter-ip-rule-set$$$

$$$ec-associate-traffic-filter-ip-rule-set$$$

**2. Associate an IP filter rule set with your deployment**

After you’ve created the rule set, you’ll need to associate IP filter rules with your deployment:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Apply filter**.
3. Choose the filter you want to apply and select **Apply filter**.

At this point, the traffic filter is active. You can remove or edit it at any time.

$$$ech-remove-association-traffic-filter-ip-rule-set$$$

$$$ec-remove-association-traffic-filter-ip-rule-set$$$

**Remove an IP filter rule set association from your deployment**

If you want to remove any traffic restrictions from a deployment or delete a rule set, you’ll need to remove any rule set associations first. To remove an association through the UI:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Remove**.


**Edit an IP filter rule set**

You can edit a rule set name or change the allowed traffic sources using IPv4, or a range of addresses with CIDR.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.
3. Under the **Features** tab, open the **Traffic filters** page.
4. Find the rule set you want to edit.
5. Select the **Edit** icon.


**Delete an IP filter rule set**

If you need to remove a rule set, you must first remove any associations with deployments.

To delete a rule set with all its rules:

1. Remove any deployment associations.
2. Under the **Features** tab, open the **Traffic filters** page.
3. Find the rule set you want to edit.
4. Select the **Delete** icon. The icon is inactive if there are deployments assigned to the rule set.



::::

::::{tab-item} {{ece}}
:sync: cloud-enterprise

Follow the step described here to set up ingress or inbound IP filters through the {{ece}} console.


**1. Create an IP filter rule set**

You can combine any rules into a set, so we recommend that you group rules according to what they allow, and make sure to label them accordingly. Since multiple sets can be applied to a deployment, you can be as granular in your sets as you feel is necessary.

To create a rule set:

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Security**.
3. Select **Create filter**.
4. Select **IP filtering rule set**.
5. Create your rule set, providing a meaningful name and description.
6. Select if this rule set should be automatically attached to new deployments.

    ::::{note} 
    Each rule set is bound to a particular region and can be only assigned to deployments in the same region.
    ::::

7. Add one or more rules using IPv4, or a range of addresses with CIDR.

    ::::{note} 
    DNS names are not supported in rules.
    ::::


The next step is to associate one or more rule-sets with your deployments.

$$$ece-associate-traffic-filter-ip-rule-set$$$

**2. Associate an IP filter rule set with your deployment**

After you’ve created the rule set, you’ll need to associate IP filter rules with your deployment:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Apply filter**.
3. Choose the filter you want to apply and select **Apply filter**.

At this point, the traffic filter is active. You can remove or edit it at any time.

$$$ece-remove-association-traffic-filter-ip-rule-set$$$

**Remove an IP filter rule set association from your deployment**

If you want to remove any traffic restrictions from a deployment or delete a rule set, you’ll need to remove any rule set associations first. To remove an association through the UI:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Remove**.


**Edit an IP filter rule set**

You can edit a rule set name or change the allowed traffic sources using IPv4, or a range of addresses with CIDR.

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Security**.
3. Find the rule set you want to edit.
4. Select the **Edit** icon.


**Delete an IP filter rule set**

If you need to remove a rule set, you must first remove any associations with deployments.

To delete a rule set with all its rules:

1. Remove any deployment associations.
2. From the **Platform** menu, select **Security**.
3. Find the rule set you want to edit.
4. Select the **Delete** icon. The icon is inactive if there are deployments assigned to the rule set.


::::


::::{tab-item} Self-managed
:sync: self-managed

You can apply IP filtering to application clients, node clients, or transport clients, remote cluster clients, in addition to other nodes that are attempting to join the cluster.

If a node’s IP address is on the denylist, the {{es}} {{security-features}} allow the connection to {{es}} but it is be dropped immediately and no requests are processed.

:::{note}
{{es}} installations are not designed to be publicly accessible over the Internet. IP Filtering and the other capabilities of the {{es}} {{security-features}} do not change this condition.
:::



**Enabling IP filtering**

The {{es}} {{security-features}} contain an access control feature that allows or rejects hosts, domains, or subnets. If the [{{operator-feature}}](/deploy-manage/users-roles/cluster-or-deployment-auth/operator-privileges.md) is enabled, only operator users can update these settings.

You configure IP filtering by specifying the `xpack.security.transport.filter.allow` and `xpack.security.transport.filter.deny` settings in `elasticsearch.yml`. Allow rules take precedence over the deny rules.

:::{important}
Unless explicitly specified, `xpack.security.http.filter.*` and `xpack.security.remote_cluster.filter.*` settings default to the corresponding `xpack.security.transport.filter.*` setting’s value.
:::


```yaml
xpack.security.transport.filter.allow: "192.168.0.1"
xpack.security.transport.filter.deny: "192.168.0.0/24"
```

The `_all` keyword can be used to deny all connections that are not explicitly allowed.

```yaml
xpack.security.transport.filter.allow: [ "192.168.0.1", "192.168.0.2", "192.168.0.3", "192.168.0.4" ]
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


**Disabling IP Filtering**

Disabling IP filtering can slightly improve performance under some conditions. To disable IP filtering entirely, set the value of the `xpack.security.transport.filter.enabled` setting in the `elasticsearch.yml` configuration file to `false`.

```yaml
xpack.security.transport.filter.enabled: false
```

You can also disable IP filtering for the transport protocol but enable it for HTTP only.

```yaml
xpack.security.transport.filter.enabled: false
xpack.security.http.filter.enabled: true
```


**Specifying TCP transport profiles**

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



**HTTP filtering**

You may want to have different IP filtering for the transport and HTTP protocols.

```yaml
xpack.security.transport.filter.allow: localhost
xpack.security.transport.filter.deny: '*.google.com'
xpack.security.http.filter.allow: 172.16.0.0/16
xpack.security.http.filter.deny: _all
```


**Remote cluster (API key based model) filtering**

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



**Dynamically updating IP filter settings**

In case of running in an environment with highly dynamic IP addresses like cloud based hosting, it is very hard to know the IP addresses upfront when provisioning a machine. Instead of changing the configuration file and restarting the node, you can use the *Cluster Update Settings API*. For example:

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
In order to avoid locking yourself out of the cluster, the default bound transport address will never be denied. This means you can always SSH into a system and use curl to apply changes.
:::


::::


:::::

