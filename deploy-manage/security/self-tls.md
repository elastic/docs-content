---
navigation_title: Self-managed
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
  - id: kibana
---

% scope: TLS encryption tasks and settings after the initial setup is completed.
# Manage TLS encryption in self-managed deployments

This section provides guidance on managing TLS certificates in self-managed deployments after the initial security setup. It covers tasks such as configuring mutual authentication, renewing certificates, and customizing supported TLS versions and cipher suites.

If you're looking to secure a new or existing cluster by setting up TLS for the first time, refer to [](./self-setup.md), which covers both the [automatic](./self-auto-setup.md) and [manual](./self-setup.md#manual-configuration) configuration procedures.

The topics in this section focus on post-setup tasks:

* [](./kibana-es-mutual-tls.md): Strengthen security by requiring {{kib}} to use a client certificate when connecting to {{es}}.
* [](./updating-certificates.md): Renew or replace existing TLS certificates before they expire.
* [](./supported-ssltls-versions-by-jdk-version.md): Customize the list of supported SSL/TLS versions in your cluster.
* [](./enabling-cipher-suites-for-stronger-encryption.md): Enable additional cipher suites for TLS communications, including those used with authentication providers.

For an overview of the endpoints that can be secured in {{es}} and {{kib}}, refer to [Communication channels](./secure-cluster-communications.md#communication-channels).

## Certificates lifecycle

In self-managed deployments, you are responsible for certificate lifecycle management, including monitoring expiration dates, renewing certificates, and redeploying them as needed. If you used Elastic tools to generate your certificates, refer to [Update TLS certificates](./updating-certificates.md) for guidance on rotating or replacing them.

## Advanced configuration references

Refer to [Transport TLS/SSL settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#transport-tls-ssl-settings) and [HTTP TLS/SSL settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#http-tls-ssl-settings) for the complete list of TLS-related settings in {{es}}.

For {{kib}}, refer to [{{kib}} general settings](kibana://reference/configuration-reference/general-settings.md), and search for all `ssl`-related settings. TLS settings for the HTTPS server are under the `server.ssl` namespace, while settings for the connection to {{es}} are under `elasticsearch.ssl`.
