---
applies_to:
  deployment:
    self: ga
    eck: all
    ece: all
    ess: all
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/manually-configure-security.html
---

# Secure your cluster or deployment

It's important to protect your {{es}} cluster and the data it contains. Implementing a defense in depth strategy provides multiple layers of security to help safeguard your system.

:::{include} /deploy-manage/security/_snippets/complete-security.md
:::

:::{important}
* Never run an {{es}} cluster without security enabled. This principle cannot be overstated. Running {{es}} without security leaves your cluster exposed to anyone who can send network traffic to {{es}}, permitting these individuals to download, modify, or delete any data in your cluster.
* Never try to run {{es}} as the `root` user, which would invalidate any defense strategy and permit a malicious user to do **anything** on your server. You must create a dedicated, unprivileged user to run {{es}}. By default, the `rpm`, `deb`, `docker`, and Windows packages of {{es}} contain an `elasticsearch` user with this scope.
::: 

:::{tip}
You must secure [other {{stack}} components](/deploy-manage/security/secure-clients-integrations.md), as well as [client and integration communications](/deploy-manage/security/httprest-clients-security.md), separately.
:::

You can configure the following aspects of your Elastic cluster or deployment to maintain and enhance security:

## Enable and set up security [manually-configure-security]

The first step in securing your deployment is ensuring that the {{es}} security feature is enabled and properly set up. {{es}} security provides authentication, authorization, TLS encryption, and other capabilities described in this section.

::::{note}
Deployments managed by {{eck}}, {{ece}}, {{ech}}, and {{serverless-short}} automatically configure security by default. This includes setting the `elastic` user password, generating TLS certificates, and configuring {{kib}} to connect to {{es}} securely. Disabling security is not supported in these deployment types.
::::

In self-managed clusters, security is [enabled and configured by default](./security-certificates-keys.md) since {{es}} 8.0, but some additional setup steps are still required. Follow the guide to complete the configuration and understand how the automatic setup works.

If the automatic setup is skipped, or if you prefer full control, you can [configure security manually](./self-setup.md#manual-configuration).

For an overview of both approaches, refer to [Security configuration for self-managed deployments](./self-setup.md).
 
## Communication and network security

:::{include} /deploy-manage/security/_snippets/cluster-communication-network.md
:::

## Data security

:::{include} /deploy-manage/security/_snippets/cluster-data.md
:::
 
## User session security

:::{include} /deploy-manage/security/_snippets/cluster-user-session.md
:::

## Security event audit logging

:::{include} /deploy-manage/security/_snippets/audit-logging.md
:::

## FIPS 140-2 compliant mode
```{applies_to}
deployment:
  self:
  eck:
```

The Federal Information Processing Standard (FIPS) Publication 140-2, (FIPS PUB 140-2), titled "Security Requirements for Cryptographic Modules" is a U.S. government computer security standard used to approve cryptographic modules. You can run a self-managed cluster or {{eck}} cluster in FIPS-compliant mode:

* [Self-managed](/deploy-manage/security/fips-140-2.md)
* [ECK](/deploy-manage/deploy/cloud-on-k8s/deploy-fips-compatible-version-of-eck.md)

% we need to refine this table, but the idea is awesome IMO

## Security features by deployment type [comparison-table]

:::{include} /deploy-manage/security/_snippets/cluster-comparison.md
:::

## Old content

### Common security scenarios

:::{image} /deploy-manage/images/elasticsearch-reference-elastic-security-overview.png
:alt: Elastic Security layers
:::

#### Minimal security ({{es}} Development) [security-minimal-overview]

::::{important}
The minimal security scenario is not sufficient for [production mode](../deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode) clusters. If your cluster has multiple nodes, you must enable minimal security and then [configure Transport Layer Security (TLS)](secure-cluster-communications.md) between nodes.
::::

If you’ve been working with {{es}} and want to enable security on your existing, unsecured cluster, start here. You’ll set passwords for the built-in users to prevent unauthorized access to your local cluster, and also configure password authentication for {{kib}}.

[Set up minimal security](set-up-minimal-security.md)

#### Basic security ({{es}} + {{kib}}) [security-basic-overview]

This scenario configures TLS for communication between nodes. This security layer requires that nodes verify security certificates, which prevents unauthorized nodes from joining your {{es}} cluster.

Your external HTTP traffic between {{es}} and {{kib}} won’t be encrypted, but internode communication will be secured.

[Set up basic security](secure-cluster-communications.md)

#### Basic security plus secured HTTPS traffic ({{stack}}) [security-basic-https-overview]

This scenario builds on the one for basic security and secures all HTTP traffic with TLS. In addition to configuring TLS on the transport interface of your {{es}} cluster, you configure TLS on the HTTP interface for both {{es}} and {{kib}}.

::::{note}
If you need mutual (bidirectional) TLS on the HTTP layer, then you’ll need to configure mutual authenticated encryption.
::::

You then configure {{kib}} and Beats to communicate with {{es}} using TLS so that all communications are encrypted. This level of security is strong, and ensures that any communications in and out of your cluster are secure.

[Set up basic security plus HTTPS traffic](secure-cluster-communications.md)

### Network access

Control which systems can access your Elastic deployments and clusters through traffic filtering and network controls:

- **IP traffic filtering**: Restrict access based on IP addresses or CIDR ranges.
- **Private link filters**: Secure connectivity through AWS PrivateLink, Azure Private Link, or GCP Private Service Connect.
- **Static IPs**: Use static IP addresses for predictable firewall rules.
- **Remote cluster access**: Secure cross-cluster operations.

Refer to [](traffic-filtering.md).


### Cluster communication

- **HTTP and HTTPs**
- **TLS certificates and keys**


### Data, objects and settings security

- **Bring your own encryption key**: Use your own encryption key instead of the default encryption at rest provided by Elastic.
- **{{es}} and {{kib}} keystores**: Secure sensitive settings using keystores
- **{{kib}} saved objects**: Customize the encryption for {{kib}} objects such as dashboards.
- **{{kib}} session management**: Customize {{kib}} session expiration settings.

Refer to [](data-security.md).

### User roles

[Define roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) for your users and [assign appropriate privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md) to ensure that users have access only to the resources that they need. This process determines whether the user behind an incoming request is allowed to run that request.
