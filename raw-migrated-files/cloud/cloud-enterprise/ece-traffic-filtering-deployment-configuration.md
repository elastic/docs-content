# Traffic Filtering [ece-traffic-filtering-deployment-configuration]

Traffic filtering is one of the security layers available in Elastic Cloud Enterprise. It allows you to limit how your deployments can be accessed. Add another layer of security to your installation and deployments by restricting inbound traffic to *only* the sources that you trust.

Elastic Cloud Enterprise supports the following traffic sources:

* [IP addresses and Classless Inter-Domain Routing (CIDR) masks](../../../deploy-manage/security/ip-traffic-filtering.md), e.g. `82.102.25.74` or `199.226.244.0/24`.
* [Remote cluster connections](../../../deploy-manage/remote-clusters/ece-enable-ccs.md), using organization and Elasticsearch cluster IDs for securing cross-cluster operations.

Filtering rules are grouped into rule sets, which in turn are associated with one or more deployments to take effect. Traffic between the instances in your deployment is automatically allowed.

Traffic filter operates on the proxy. Requests rejected by the traffic filter are not forwarded to the deployment. The proxy responds to the client with `403 Forbidden`.

::::{note}
Domain-based filtering rules are not allowed for Cloud traffic filtering, because the original IP is hidden behind the proxy. Only IP-based filtering rules are allowed.
::::


::::{note}
You can have a maximum of 1024 rule sets per organization and 128 rules in each rule set.
::::



## Before you begin [ece-traffic-filter-before-you-begin]

* Make sure your [load balancer](../../../deploy-manage/deploy/cloud-enterprise/ece-load-balancers.md) handles the `X-Forwarded-For` header appropriately for HTTP requests to prevent IP address spoofing. Make sure the proxy protocol v2 is enabled for HTTP and transport protocols (9243 and 9343).


## Terminology [ece-traffic-filter-terminology]

Traffic filter rule
:   Specifies traffic originating from an IP address or a CIDR mask.

Traffic filter rule set
:   A named set of *traffic filter rules*. It defines allowed traffic sources. Rule sets can be used across multiple deployments. Note that the rules are not in effect until the rule set is associated with a deployment.

Rule set association
:   One or more rule sets can be associated with a deployment. In such a case, the traffic sources specified in the rule sets are allowed to connect to the deployment. No other traffic source  is allowed.


## How does it work? [ece-traffic-filter-how-does-it-work]

By default, all your deployments are accessible over the public internet, assuming that your Elastic Cloud Enterprise proxies are accessible.

Once you associate at least one traffic filter with a deployment, traffic that does not match any rules (for this deployment) is denied.

::::{note}
This only applies to external traffic. Internal traffic is managed by Elastic Cloud Enterprise. For example, Kibana can connect to Elasticsearch, as well as internal services which manage the deployment. Other deployments can’t connect to deployments protected by traffic filters.
::::


You can assign multiple rule sets to a single deployment. The rule sets can be of  different types.

In case of multiple rule sets, traffic can match ANY of them. If none of the rule sets match the request is rejected with `403 Forbidden`.

You can mark a rule set as *default*. It is automatically attached to all new deployments that you create in its region. You can detach default rule sets from deployments after they are created.

::::{note}
A *default* rule set is not automatically attached to existing deployments.
::::


For more information about creating and editing rule sets and then associating them with your deployments, check [IP addresses and CIDR masks](../../../deploy-manage/security/ip-traffic-filtering.md).

::::{note}
Traffic filter rule sets when associated with a deployment will apply to all deployment endpoints, such as Elasticsearch, Kibana, APM Server, and others.
::::


::::{note}
Any traffic filter rule set assigned to a deployment overrides the default behavior of *allow all access over the public internet endpoint; deny all access over Private Link*. The implication is that if you make a mistake putting in the traffic source (for example, specified the wrong IP address) the deployment will be effectively locked down to any of your traffic. You can use the UI to adjust or remove the rule sets.
::::



## Example scenarios [ece-traffic-filter-how-does-it-work-example]

Jane creates a deployment. At this point the deployment is accessible over internet through its public endpoint, e.g. `https://fcd41689e9214319b1278325fd6af7cd.us-east-1.aws.found.io`. The deployment is protected by username+password authentication, but there’s no additional traffic source filtering.

Jane wants to allow access to the deployment from Jane’s Office.

* They create an IP rule set with office IP range give as a CIDR mask, e.g. `199.226.244.0/24`.
* They attach the rule set to the deployment.
* The deployment is accessible from the CIDR range from Jane’s Office.

Later, Jane decides to allow anyone to connect to the deployment over the public internet.

* They create the *allow all* rule set, with the CIDR mask `0.0.0.0/0`.
* They associate it with Jane’s deployment.
* Anyone with a valid username+password can now access the deployment.
* They could remove the Jane’s Office rule set — `199.226.244.0/24`. It is a subset of the *allow all*. They prefer to keep it attached anyways, in case they need to deny access from the public internet in the future.


## Deploy traffic filters [ece-traffic-filter-details]

Follow the instructions that match your use case:

* [IP addresses and Classless Inter-Domain Routing (CIDR) masks](../../../deploy-manage/security/ip-traffic-filtering.md), e.g. `82.102.25.74` or `199.226.244.0/24`.


## Troubleshooting [ece-traffic-filter-troubleshooting]

This section offers suggestions on how to troubleshoot your traffic filters. Before you start make sure you check the [Limitations and known problems](asciidocalypse://docs/cloud/docs/release-notes/cloud-enterprise/known-issues.md).


### Review the rule sets associated with a deployment [ece-review-rule-sets]

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. Select the **Security** tab on the left-hand side menu bar.
4. Traffic filter rule sets are listed under **Traffic filters**.

On this screen you can view and remove existing filters and attach new filters.


### Identify default rule sets [ece-default-rule-sets]

To identify which rule sets are automatically applied to new deployments in your account:

1. From the **Platform** menu, select **Security**.
2. You can find the list of traffic filter rule sets.
3. Select each of the rule sets — **Include by default** is checked when this rule set is automatically applied to all new deployments in its region.


### How to view rejected requests [ece-rejected-traffic-requests]

Requests rejected by traffic filter have status code `403 Forbidden` and response body `{"ok":false,"message":"Forbidden due to traffic filtering. Please see the Elastic documentation on Traffic Filtering for more information."}`.

Additionally, traffic filter rejections are logged in the proxy logs as `status_reason: BLOCKED_BY_IP_FILTER`.

Proxy logs also provide client IP in `client_ip` field.



#### Request rejected by the IP traffic filter [ece-rejected-ipfilter]

To find out why the following request was rejected, you can compare it with deployment traffic filters.

```yaml
handling_cluster: 74a1d503fc1540979fae9824f541fb5b
status_code: 403
status_reason: BLOCKED_BY_IP_FILTER
client_ip: 192.168.255.6
link_id: ""  # no value
# ...
```

:::{image} ../../../images/cloud-enterprise-ce-traffic-filter-ip-rejected-request.png
:alt: Show rejected request in the proxy logs
:class: screenshot
:::

To allow such a request to come through the traffic filter, you would register an IP traffic filter with the source IP address `192.168.255.6`, or a matching CIDR mask, e.g. `192.168.255.0/24`.



