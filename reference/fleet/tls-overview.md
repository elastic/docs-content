---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/tls-overview.html
products:
  - id: fleet
  - id: elastic-agent
---

# One-way and mutual TLS certifications flow [tls-overview]

This page provides an overview of the relationship between the various certificates and certificate authorities (CAs) that you configure for {{fleet-server}} and {{agent}}, using the `elastic-agent install` TLS command options.

* [Simple one-way TLS connection](#one-way-tls-connection)
* [Mutual TLS connection](#mutual-tls-connection)


## Simple one-way TLS connection [one-way-tls-connection]

The following `elastic-agent install` command configures a {{fleet-server}} with the required certificates and certificate authorities to enable one-way TLS connections between the components involved:

```shell
elastic-agent install --url=https://your-fleet-server.elastic.co:443 \
--certificate-authorities=/path/to/fleet-ca \
--fleet-server-es=https://es.elastic.com:443 \
--fleet-server-es-ca=/path/to/es-ca \
--fleet-server-cert=/path/to/fleet-cert \
--fleet-server-cert-key=/path/to/fleet-cert-key \
--fleet-server-service-token=FLEET-SERVER-SERVICE-TOKEN \
--fleet-server-policy=FLEET-SERVER-POLICY-ID \
--fleet-server-port=8220
```

You can also configure a one-way TLS connection using {{kib}}. Refer to [Configure TLS settings in the Fleet UI](#tls-ui-settings) for more information. {applies_to}`stack: ga 9.1`


{{agent}} is configured with `fleet-ca` as the certificate authority that it needs to validate certificates from {{fleet-server}}.

During the TLS connection setup, {{fleet-server}} presents its certificate `fleet-cert` to the agent and the agent (as a client) uses `fleet-ca` to validate the presented certificate.

:::{image} images/tls-overview-oneway-fs-agent.png
:alt: Diagram of one-way TLS connection between Fleet Server and Elastic Agent
:::

{{fleet-server}} also establishes a secure connection to an {{es}} cluster. In this case, {{fleet-server}} is configured with the certificate authority from the {{es}} `es-ca`. {{es}} presents its certificate, `es-cert`, and {{fleet-server}} validates the presented certificate using the certificate authority `es-ca`.

:::{image} images/tls-overview-oneway-fs-es.png
:alt: Diagram of one-way TLS connection between Fleet Server and Elasticsearch
:::


### Relationship between components in a one-way TLS connection [_relationship_between_components_in_a_one_way_tls_connection]

:::{image} images/tls-overview-oneway-all.jpg
:alt: Diagram of one-way TLS connection between components
:::


## Mutual TLS connection [mutual-tls-connection]

The following `elastic-agent install` command configures a {{fleet-server}} with the required certificates and certificate authorities to enable mutual TLS connections between the components involved:

```shell
elastic-agent install --url=https://your-fleet-server.elastic.co:443 \
--certificate-authorities=/path/to/fleet-ca,/path/to/agent-ca \
--elastic-agent-cert=/path/to/agent-cert \
--elastic-agent-cert-key=/path/to/agent-cert-key \
--elastic-agent-cert-key=/path/to/agent-cert-key-passphrase \
--fleet-server-es=https://es.elastic.com:443 \
--fleet-server-es-ca=/path/to/es-ca \
--fleet-server-es-cert=/path/to/fleet-es-cert \
--fleet-server-es-cert-key=/path/to/fleet-es-cert-key \
--fleet-server-cert=/path/to/fleet-cert \
--fleet-server-cert-key=/path/to/fleet-cert-key \
--fleet-server-client-auth=required \
--fleet-server-service-token=FLEET-SERVER-SERVICE-TOKEN \
--fleet-server-policy=FLEET-SERVER-POLICY-ID \
--fleet-server-port=8220
```

You can also configure a mutual TLS connection using {{kib}}. Refer to [Configure TLS settings in the Fleet UI](#tls-ui-settings) for more information. {applies_to}`stack: ga 9.1`


As with the [one-way TLS example](#one-way-tls-connection), {{agent}} is configured with `fleet-ca` as the certificate authority that it needs to validate certificates from the {{fleet-server}}. {{fleet-server}} presents its certificate `fleet-cert` to the agent and the agent (as a client) uses `fleet-ca` to validate the presented certificate.

To establish a mutual TLS connection, the agent presents its certificate, `agent-cert`, and {{fleet-server}} validates this certificate using the `agent-ca` that it has stored in memory.

:::{image} images/tls-overview-mutual-fs-agent.png
:alt: Diagram of mutual TLS connection between Fleet Server and Elastic Agent
:::

{{fleet-server}} can also establish a mutual TLS connection to the {{es}} cluster. In this case, {{fleet-server}} is configured with the certificate authority from the {{es}} `es-ca` and uses this to validate the certificate `es-cert` presented to it by {{es}}.

:::{image} images/tls-overview-mutual-fs-es.png
:alt: Diagram of mutual TLS connection between Fleet Server and Elasticsearch
:::

Note that you can also configure mutual TLS for {{fleet-server}} and {{agent}} [using a proxy](/reference/fleet/mutual-tls.md#mutual-tls-cloud-proxy).


### Relationship between components in a mutual TLS connection [_relationship_between_components_in_a_mutual_tls_connection]

:::{image} images/tls-overview-mutual-all.jpg
:alt: Diagram of mutual TLS connection between components
:::

## Configure TLS/mTLS settings in the Fleet UI [tls-ui-settings]
```{applies_to}
  stack: ga 9.1
```

You can configure TLS and mutual TLS (mTLS) settings for {{fleet-server}} hosts using the {{fleet}} UI instead of CLI flags. This approach simplifies certificate configuration.

To access these settings:

1. In **Kibana**, go to **Management** > **Fleet** > **Settings**.
2. Under **Fleet Server hosts**, click **Add host** or edit an existing host.
3. Expand the **SSL options** section.

### SSL options

The following table shows the available UI fields and their CLI equivalents:

| **UI Field**                                      | **CLI Flag**                          | **Purpose** |
|--------------------------------------------------|---------------------------------------|-------------|
| Client SSL Certificate                           | `--elastic-agent-cert`               | {{agent}} client certificate to use with {{fleet-server}} during mTLS authentication. |
| Client SSL Certificate key                       | `--elastic-agent-cert-key`           | {{agent}} client private key to use with {{fleet-server}} during mTLS authentication. This field uses secret storage and requires {{fleet-server}} v8.12.0 or later. You can optionally choose to store the value as plain text instead. |
| Server SSL certificate authorities (optional)    | `--certificate-authorities`          | Comma-separated list of root certificates for server verification used by {{agent}} and {{fleet-server}}. |
| SSL certificate for {{es}}                | `--fleet-server-es-cert`             | Client certificate for {{fleet-server}} to use when connecting to {{es}}. |
| SSL certificate key for {{es}}            | `--fleet-server-es-cert-key`         | Client private key for {{fleet-server}} to use when connecting to {{es}}. |
| {{es}} Certificate Authorities (optional) | `--fleet-server-es-ca`               | Path to certificate authority for {{fleet-server}} to use to communicate with {{es}}. |
| Enable client authentication                     | `--fleet-server-client-auth=required`| Requires {{agent}} to present a valid client certificate when connecting to {{fleet-server}}. |

The {{fleet}} UI doesn't currently allow editing the {{fleet-server}}’s own exposed TLS certificate (`--fleet-server-cert`, `--fleet-server-cert-key`). These are only configurable using the CLI either during the initial installation or later.

:::{warning}
Editing SSL or proxy settings for an existing {{fleet-server}} may cause agents to lose connectivity. After changing client certificate settings, you need to re-enroll the affected agents.
:::