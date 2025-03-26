---
navigation_title: Configure security in a self-managed cluster
applies_to:
  deployment:
    self: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/manually-configure-security.html
---

# Configure security in a self-managed cluster [manually-configure-security]

:::{note}
This page describes important aspects to consider and common end-to-end scenarios for securing your self-managed {{stack}}. For a more granular view of the available security options for your clusters and nodes, refer to [](secure-your-cluster-deployment.md).
:::

Security needs vary depending on whether you’re developing locally on your laptop or securing all communications in a production environment. Regardless of where you’re deploying the {{stack}} ("ELK"), running a secure cluster is incredibly important to protect your data. That’s why security is [enabled and configured by default](../deploy/self-managed/installing-elasticsearch.md) since {{es}} 8.0.

## Security principles

### Run {{es}} with security enabled [security-run-with-security]

Never run an {{es}} cluster without security enabled. This principle cannot be overstated. Running {{es}} without security leaves your cluster exposed to anyone who can send network traffic to {{es}}, permitting these individuals to download, modify, or delete any data in your cluster. [Start the {{stack}} with security enabled](/deploy-manage/security/security-certificates-keys.md) or [manually configure security](/deploy-manage/security/manually-configure-security-in-self-managed-cluster.md) to prevent unauthorized access to your clusters and ensure that internode communication is secure.

### Run {{es}} with a dedicated non-root user [security-not-root-user]

Never try to run {{es}} as the `root` user, which would invalidate any defense strategy and permit a malicious user to do **anything** on your server. You must create a dedicated, unprivileged user to run {{es}}. By default, the `rpm`, `deb`, `docker`, and Windows packages of {{es}} contain an `elasticsearch` user with this scope.

### Protect {{es}} from public internet traffic [security-protect-cluster-traffic]

Even with security enabled, never expose {{es}} to public internet traffic. Using an application to sanitize requests to {{es}} still poses risks, such as a malicious user writing [`_search`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-search) requests that could overwhelm an {{es}} cluster and bring it down. Keep {{es}} as isolated as possible, preferably behind a firewall and a VPN. Any internet-facing applications should run pre-canned aggregations, or not run aggregations at all.

### Implement role based access control [security-create-appropriate-users]

[Define roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) for your users and [assign appropriate privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md) to ensure that users have access only to the resources that they need. This process determines whether the user behind an incoming request is allowed to run that request.

## Common security scenarios

:::{image} /deploy-manage/images/elasticsearch-reference-elastic-security-overview.png
:alt: Elastic Security layers
:::

### Minimal security ({{es}} Development) [security-minimal-overview]

::::{important}
The minimal security scenario is not sufficient for [production mode](../deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode) clusters. If your cluster has multiple nodes, you must enable minimal security and then [configure Transport Layer Security (TLS)](secure-cluster-communications.md) between nodes.
::::

If you’ve been working with {{es}} and want to enable security on your existing, unsecured cluster, start here. You’ll set passwords for the built-in users to prevent unauthorized access to your local cluster, and also configure password authentication for {{kib}}.

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
