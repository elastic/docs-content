---
navigation_title: "Self-managed security setup"
applies_to:
  deployment:
    self: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup-https.html
---

# Set up security in self-managed deployments

There are two approaches to configuring security in self-managed deployments of the {{stack}}:

## Automatic configuration [automatic-configuration]

Since version 8.0, {{es}} automatically enables security features on first startup when the node is not part of an existing cluster and none of the [incompatible settings](./self-auto-setup.md#stack-existing-settings-detected) have been explicitly configured.

The automatic configuration::

* Generates TLS certificates for the transport and HTTP layers
* Applies security settings to `elasticsearch.yml`
* Sets a password for the `elastic` superuser
* Creates an enrollment token to securely connect {{kib}} to {{es}}

This automatic setup is the quickest way to get started and ensures your cluster is protected by default.

::::{note}
The automatic configuration does not enable TLS on the {{kib}} HTTP endpoint. To encrypt browser traffic to {{kib}}, follow the steps in [](./set-up-basic-security-plus-https.md#encrypt-kibana-browser).
::::

Refer to [Automatic security setup](./self-auto-setup.md) for the complete procedure, including [cases where it may be skipped](./self-auto-setup.md#stack-skip-auto-configuration).

## Manual configuration [manual-configuration]

If you’re securing an existing unsecured cluster, or prefer to use your own TLS certificates, follow the manual approach. It involves enabling different layers of protection in sequence, depending on your cluster architecture and security requirements.

* **Start with [minimal security](set-up-minimal-security.md)**: Enables password-based authentication for built-in users and configures {{kib}} to connect using credentials. Suitable for single-node clusters, but not sufficient for production or multi-node clusters.

* **Then [configure transport TLS](./set-up-basic-security.md)**: Required for multi-node clusters running in [production mode](../deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode). Secures communication between nodes and prevents unauthorized nodes from joining the cluster.

* **Finally, [configure HTTP TLS](set-up-basic-security-plus-https.md)**: Secures all client communications over HTTPS, including traffic between {{kib}} and {{es}}, and between browsers and {{kib}}. Recommended for all clusters, even single-node setups.

Each step builds on the previous one. For production environments, it’s strongly recommended to complete all three.


