---
navigation_title: "Self-managed"
applies_to:
  deployment:
    self: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup-https.html
---

# Manage TLS certificates in self-managed deployments

This section provides guides for manually configuring and maintaining the TLS certificates required by your deployment. For an overview of the endpoints that need securing in {{es}} and {{kib}}, refer to [Communication channels](./secure-cluster-communications.md#communication-channels).

Use the following guides to manage TLS certificates:

* [Set up transport TLS](./set-up-basic-security.md): Create a CA and certificates to encrypt inter-node traffic in multi-node clusters.
* [Set up HTTP TLS](./set-up-basic-security-plus-https.md): Create and configure certificates to encrypt {{es}} and {{kib}} HTTP endpoints.
* [Mutual TLS authentication between {{kib}} and {{es}}](./kibana-es-mutual-tls.md): Strengthen security by requiring {{kib}} to use an additional client certificate in the communication to {{es}}.
* [Update TLS certificates](./updating-certificates.md): Renew or replace existing TLS certificates before they expire.

As an alternative to the manual configuration, consider the [automatic security configuration](./self-auto-setup.md) procedure, which includes automatic generation of TLS certificates for {{es}} HTTP and transport endpoints.

## Certificates maintenance and rotation

In self-managed deployments, you are responsible for certificate lifecycle management, including monitoring expiration dates, renewing certificates, and redeploying them as needed. If you used Elastic tools to generate your certificates, refer to [Update TLS certificates](./updating-certificates.md) for guidance on rotating or replacing them.
