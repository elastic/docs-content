---
navigation_title: Self-managed
applies_to:
  deployment:
    self: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/manually-configure-security.html
---

# Manually configure security in a self-managed cluster [manually-configure-security]

:::{note}
This page describes important aspects to consider and common end-to-end scenarios for securing your self-managed {{stack}}. For a more granular view of the available security options for your clusters and nodes, refer to [](secure-your-cluster-deployment.md).
:::

Security needs vary depending on whether you’re developing locally on your laptop or securing all communications in a production environment. Regardless of where you’re deploying the {{stack}} ("ELK"), running a secure cluster is incredibly important to protect your data. That’s why security is [enabled and configured by default](../deploy/self-managed/installing-elasticsearch.md) since {{es}} 8.0.

If you want to enable security on an existing, unsecured cluster, use your own Certificate Authority (CA), or would rather manually configure security, the following scenarios provide steps for configuring TLS on the transport layer, plus securing HTTPS traffic if you want it.

If you configure security manually *before* starting your {{es}} nodes, the auto-configuration process will respect your security configuration. You can adjust your TLS configuration at any time, such as [updating node certificates](updating-certificates.md).

:::{image} ../../images/elasticsearch-reference-elastic-security-overview.png
:alt: Elastic Security layers
:::

## Common security scenarios

Even with security enabled, never expose {{es}} to public internet traffic. Using an application to sanitize requests to {{es}} still poses risks, such as a malicious user writing [`_search`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-search) requests that could overwhelm an {{es}} cluster and bring it down. Keep {{es}} as isolated as possible, preferably behind a firewall and a VPN. Any internet-facing applications should run pre-canned aggregations, or not run aggregations at all.

While you absolutely shouldn’t expose {{es}} directly to the internet, you also shouldn’t expose {{es}} directly to users. Instead, use an intermediary application to make requests on behalf of users. This implementation allows you to track user behaviors, such as can submit requests, and to which specific nodes in the cluster. For example, you can implement an application that accepts a search term from a user and funnels it through a [`simple_query_string`](elasticsearch://reference/query-languages/query-dsl-simple-query-string-query.md) query.

### Minimal security ({{es}} Development) [security-minimal-overview]

If you’ve been working with {{es}} and want to enable security on your existing, unsecured cluster, start here. You’ll set passwords for the built-in users to prevent unauthorized access to your local cluster, and also configure password authentication for {{kib}}.

::::{important}
The minimal security scenario is not sufficient for [production mode](../deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode) clusters. If your cluster has multiple nodes, you must enable minimal security and then [configure Transport Layer Security (TLS)](secure-cluster-communications.md) between nodes.
::::


[Set up minimal security](set-up-minimal-security.md)


### Basic security ({{es}} + {{kib}}) [security-basic-overview]

This scenario configures TLS for communication between nodes. This security layer requires that nodes verify security certificates, which prevents unauthorized nodes from joining your {{es}} cluster.

Your external HTTP traffic between {{es}} and {{kib}} won’t be encrypted, but internode communication will be secured.

[Set up basic security](secure-cluster-communications.md)


### Basic security plus secured HTTPS traffic ({{stack}}) [security-basic-https-overview]

This scenario builds on the one for basic security and secures all HTTP traffic with TLS. In addition to configuring TLS on the transport interface of your {{es}} cluster, you configure TLS on the HTTP interface for both {{es}} and {{kib}}.

::::{note}
If you need mutual (bidirectional) TLS on the HTTP layer, then you’ll need to configure mutual authenticated encryption.
::::


You then configure {{kib}} and Beats to communicate with {{es}} using TLS so that all communications are encrypted. This level of security is strong, and ensures that any communications in and out of your cluster are secure.

[Set up basic security plus HTTPS traffic](secure-http-communications.md)









