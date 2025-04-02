---
navigation_title: Traffic filtering
applies_to:
  deployment:
    ess: ga
    ece: ga
    eck: ga
    self: ga
  serverless: unavailable
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-traffic-filtering-deployment-configuration.html
  - https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-deployment-configuration.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-traffic-filtering-deployment-configuration.html
---

# Traffic filtering

Traffic filtering allows you to limit how your deployments and clusters can be accessed. Add another layer of security to your installation and deployments by restricting inbound traffic to only the sources that you trust.

## Traffic filtering methods

Depending on your deployment type you can use different mechanisms to restrict traffic.

::::{note}
This section covers traffic filtering at the deployment level. If you need the IP addresses used by {{ech}} to configure them in your network firewalls, refer to [](./elastic-cloud-static-ips.md).

You can also allow traffic to or from a [remote cluster](/deploy-manage/remote-clusters.md) for use with cross-cluster replication or search.
::::

| Filter type | Description | Applicable deployment types |
| --- | --- | --- |
| [IP traffic filters](ip-traffic-filtering.md) | Filter traffic using IP addresses and Classless Inter-Domain Routing (CIDR) masks.<br><br>• [In ECH or ECE](/deploy-manage/security/ip-filtering-cloud.md)<br><br>• [In ECK or self-managed](/deploy-manage/security/ip-filtering-basic.md) | ECH, ECE, ECK, and self-managed clusters |
| [Private link filters](/deploy-manage/security/private-link-traffic-filters.md) | Allow traffic between {{es}} and other resources hosted by the same cloud provider using private link services. Choose the relevant option for your region:<br><br>• AWS regions: [AWS PrivateLink](/deploy-manage/security/aws-privatelink-traffic-filters.md)<br><br>• Azure regions: [Azure Private Link](/deploy-manage/security/azure-private-link-traffic-filters.md)<br><br>• GCP regions: [GCP Private Service Connect](/deploy-manage/security/gcp-private-service-connect-traffic-filters.md) | {{ech}} only |
| [Kubernetes network policies](/deploy-manage/security/k8s-network-policies.md) | Isolate pods by restricting incoming and outgoing network connections to a trusted set of sources and destinations. | {{eck}} only |

:::{include} _snippets/eck-traffic-filtering.md
:::


## Traffic filter rules in ECE and ECH [traffic-filter-rules]
```{applies_to}
  deployment:
    ess:
    ece:
```

% could be refined further

By default, in {{ece}} and {{ech}}, all your deployments are accessible over the public internet. In {{ece}}, this assumes that your orchestrator's proxies are accessible.

Filtering *rules* are grouped into *rule sets*, which in turn are *associated* with one or more deployments to take effect. After you associate at least one traffic filter with a deployment, traffic that does not match any filtering rules for the deployment is denied.

Traffic filters apply to external traffic only. Internal traffic is managed by ECE or ECH. For example, {{kib}} can connect to {{es}}, as well as internal services which manage the deployment. Other deployments can’t connect to deployments protected by traffic filters.

Traffic filters operate on the proxy. Requests rejected by the traffic filters are not forwarded to the deployment. The proxy responds to the client with `403 Forbidden`.

Domain-based filtering rules are not allowed for Cloud traffic filtering, because the original IP is hidden behind the proxy. Only IP-based filtering rules are allowed.

Rule sets work as follows:

- You can assign multiple rule sets to a single deployment. The rule sets can be of different types. In case of multiple rule sets, traffic can match ANY of them. If none of the rule sets match, the request is rejected with `403 Forbidden`.
- Traffic filter rule sets are bound to a single region. The rule sets can be assigned only to deployments in the same region. If you want to associate a rule set with deployments in multiple regions, then you have to create the same rule set in all the regions you want to apply it to.
- You can mark a rule set as *default*. It is automatically attached to all new deployments that you create in its region. You can detach default rule sets from deployments after they are created. Note that a *default* rule set is not automatically attached to existing deployments.
- Traffic filter rule sets, when associated with a deployment, will apply to all deployment endpoints, such as {{es}}, {{kib}}, APM Server, and others.
- Any traffic filter rule set assigned to a deployment overrides the default behavior of *allow all access over the public internet endpoint; deny all access over Private Link*. The implication is that if you make a mistake putting in the traffic source (for example, specified the wrong IP address) the deployment will be effectively locked down to any of your traffic. You can use the UI to adjust or remove the rule sets.

:::{admonition} Rule limits
In {{ech}}, you can have a maximum of 1024 rule sets per organization and 128 rules in each rule set.

In {{ece}}, you can have a maximum of 512 rule sets per organization and 128 rules in each rule set.
:::

### Tips

This section offers suggestions on how to manage and analyze the impact of your traffic filters in ECH and ECE.

#### Review the rule sets associated with a deployment

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) or [Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Hosted deployments** page, select your deployment.
3. Select the **Security** tab on the left-hand side menu bar.

Traffic filter rule sets are listed under **Traffic filters**.

On this page, you can view and remove existing filters and attach new filters.

#### Identify default rule sets
To identify which rule sets are automatically applied to new deployments in your account:

1. Navigate to the traffic filters list:

    ::::{tab-set}
    :group: ech-ece

    :::{tab-item} {{ech}}
    :sync: ech
    1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
    2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.
    3. Under the **Features** tab, open the **Traffic filters** page.
    :::
    :::{tab-item} {{ece}}
    :sync: ece
    4. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
    5. From the **Platform** menu, select **Security**.
    :::
    ::::

2. Select each of the rule sets — **Include by default** is checked when this rule set is automatically applied to all new deployments in its region.

#### View rejected requests

Requests rejected by traffic filter have status code `403 Forbidden` and one of the following in the response body:

```json
{"ok":false,"message":"Forbidden"}
```

```json
{"ok":false,"message":"Forbidden due to traffic filtering. Please see the Elastic documentation on Traffic Filtering for more information."}
```

Additionally, traffic filter rejections are logged in ECE proxy logs as `status_reason: BLOCKED_BY_IP_FILTER`. Proxy logs also provide client IP in `client_ip` field.