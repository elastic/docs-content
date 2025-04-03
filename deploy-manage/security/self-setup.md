---
navigation_title: "Self-managed security setup"
applies_to:
  deployment:
    self: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/manually-configure-security.html
  - https://www.elastic.co/guide/en/elastic-stack/current/install-stack-demo-secure.html
---

% scope: initial security setup in self-managed deployments, following the automatic or manual (minimal, basic, https) procedures
# Set up security in self-managed deployments

This section explains how to perform the initial security setup for self-managed deployments, including configuring TLS certificates to secure {{es}} and {{kib}} endpoints, setting passwords for built-in users, and generating enrollment tokens to connect {{kib}} or additional {{es}} nodes to the cluster.

Self-managed deployments support two approaches for the initial setup: automatic and manual. Note that securing {{kib}} always requires some manual configuration.

For guidance on configuring additional security features, refer to [](./secure-your-cluster-deployment.md).

## Automatic configuration [automatic-configuration]

Since version 8.0, {{es}} automatically enables security features on first startup when the node is not part of an existing cluster and none of the [incompatible settings](./self-auto-setup.md#stack-existing-settings-detected) have been explicitly configured.

The automatic configuration:

* Generates TLS certificates for the [transport and HTTP layers](./secure-cluster-communications.md#communication-channels)
* Applies TLS configuration settings to `elasticsearch.yml`
* Sets a password for the `elastic` superuser
* Creates an enrollment token to securely connect {{kib}} to {{es}}

This automatic setup is the quickest way to get started and ensures your cluster is protected by default.

::::{warning}
The automatic configuration does not enable TLS on the {{kib}} HTTP endpoint. To encrypt browser traffic to {{kib}}, follow the steps in [](./set-up-basic-security-plus-https.md#encrypt-kibana-browser).
::::

Refer to [Automatic security setup](./self-auto-setup.md) for details about the full procedure, including [cases where it may be skipped](./self-auto-setup.md#stack-skip-auto-configuration).

## Manual configuration [manual-configuration]

If you’re securing an existing unsecured cluster, or prefer to use your own TLS certificates, follow the manual approach. It involves enabling different layers of protection in sequence, depending on your cluster architecture and security requirements.

1. **[Set up minimal security](set-up-minimal-security.md)**: Enables password-based authentication for built-in users and configures {{kib}} to connect using credentials. Suitable for single-node clusters, but not sufficient for production or multi-node clusters.

2. **[Configure transport TLS](./set-up-basic-security.md)**: Required for multi-node clusters running in [production mode](../deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode). Secures communication between nodes and prevents unauthorized nodes from joining the cluster.

3. **[Configure HTTP TLS](set-up-basic-security-plus-https.md)**: Secures all client communications over HTTPS, including traffic between {{kib}} and {{es}}, and between browsers and {{kib}}. Recommended for all clusters, even single-node setups.

Each step builds on the previous one. For production environments, it’s strongly recommended to complete all three.

For additional TLS configuration options, refer to [](./self-tls.md).

## Kibana security configuration

Refer to [](./using-kibana-with-security.md) to learn how to implement the following security best practices for {{kib}}:

* Set an encryption key for client sessions
* Use secure HTTP headers
* Require a Content Security Policy (CSP)