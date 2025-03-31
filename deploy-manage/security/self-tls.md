---
navigation_title: "Self-managed"
applies_to:
  deployment:
    self: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup-https.html
---

# Manage TLS certificates in self-managed deployments

This section provides guides for configuring TLS encryption in self-managed deployments. It covers how to create and manage TLS certificates, configure {{es}} and {{kib}} service endpoints to use them, and apply related security settings such as supported TLS versions and cipher suites.

All procedures in this section focus on manual configuration. If you prefer an automated approach, consider using the [automatic security configuration](./self-auto-setup.md) feature, which sets up TLS certificates for {{es}} HTTP and transport endpoints during initial startup.

For an overview of the endpoints that need securing in {{es}} and {{kib}}, refer to [Communication channels](./secure-cluster-communications.md#communication-channels).

* [](./set-up-basic-security.md) (**required for multi-node clusters**): Create and configure a Certificate Authority (CA) and certificates to encrypt inter-node traffic.
* [](./set-up-basic-security-plus-https.md) (**optional but recommended**): Create and configure certificates to encrypt traffic on {{es}} and {{kib}} HTTP endpoints.
* [](./kibana-es-mutual-tls.md) (**optional**): Strengthen security by requiring {{kib}} to use an additional client certificate in the communication to {{es}}.
* [](./updating-certificates.md): Renew or replace existing TLS certificates before they expire.
* [](./supported-ssltls-versions-by-jdk-version.md): Customize the list of supported SSL/TLS versions in your cluster.
* [](./enabling-cipher-suites-for-stronger-encryption.md): Enable the use of additional cipher suites, so you can use different cipher suites for your TLS communications or communications with authentication providers.

## Certificates lifecycle

In self-managed deployments, you are responsible for certificate lifecycle management, including monitoring expiration dates, renewing certificates, and redeploying them as needed. If you used Elastic tools to generate your certificates, refer to [Update TLS certificates](./updating-certificates.md) for guidance on rotating or replacing them.
