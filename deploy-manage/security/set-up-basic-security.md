---
navigation_title: Set up transport TLS
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup.html
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
---

% Scope: TLS certificates setup / multi-node cluster / manual configuration
% original title: Set up basic security for the {{stack}}
# Set up transport TLS [security-basic-setup]

Configuring TLS between nodes is the basic security setup to prevent unauthorized nodes from accessing to your {{es}} cluster, and it's required by multi-node clusters. [Production mode](../deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode) clusters will not start if you do not enable TLS.

This document focuses on the **manual configuration** of TLS for [{{es}} transport protocol](./secure-cluster-communications.md#encrypt-internode-communication) in self-managed environments. Use this approach if you want to provide your own TLS certificates, generate them with Elastic’s tools, or have full control over the configuration. Alternatively, {{es}} can [automatically generate and configure HTTPS certificates](./self-auto-setup.md) for you.

::::{note}
For other deployment types, such as {{ech}}, {{ece}}, or {{eck}}, refer to [](./secure-cluster-communications.md).
::::

In this guide, you will learn how to:

* [Generate a Certificate Authority (CA) and a server certificate using the `elasticsearch-certutil` tool](#generate-certificates).
* [Configure your {{es}} nodes to use the generated certificate for the transport layer](#encrypt-internode-communication).

Refer to [Transport TLS/SSL settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#transport-tls-ssl-settings) for the complete list of available settings in {{es}}.

## Considerations for using an external CA

You might choose to use an external CA to generate transport certificates for node-to-node connections.

Transport connections between {{es}} nodes are security-critical and you must protect them carefully. Malicious actors who can observe or interfere with unencrypted node-to-node transport traffic can read or modify cluster data. A malicious actor who can establish a transport connection might be able to invoke system-internal APIs, including APIs that read or modify cluster data.

Carefully review [](/deploy-manage/security/self-tls-considerations.md) to ensure that the certificates that you provide meet the security requirements for transport connections.

## Generate the certificate authority [generate-certificates]

You can add as many nodes as you want in a cluster but they must be able to communicate with each other. The communication between nodes in a cluster is handled by the transport module. To secure your cluster, you must ensure that internode communications are encrypted and verified, which is achieved with mutual TLS.

In a secured cluster, {{es}} nodes use certificates to identify themselves when communicating with other nodes.

The cluster must validate the authenticity of these certificates. The recommended approach is to trust a specific certificate authority (CA). When nodes are added to your cluster they must use a certificate signed by the same CA.

For the transport layer, we recommend using a separate, dedicated CA instead of an existing, possibly shared CA so that node membership is tightly controlled. Use the `elasticsearch-certutil` tool to generate a CA for your cluster.

1. Before starting {{es}}, use the `elasticsearch-certutil` tool on any single node to generate a CA for your cluster.

    ```shell
    ./bin/elasticsearch-certutil ca
    ```

    1. When prompted, accept the default file name, which is `elastic-stack-ca.p12`. This file contains the public certificate for your CA and the private key used to sign certificates for each node.
    2. Enter a password for your CA. You can choose to leave the password blank if you’re not deploying to a production environment.

2. On any single node, generate a certificate and private key for the nodes in your cluster. You include the `elastic-stack-ca.p12` output file that you generated in the previous step.

    ```shell
    ./bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12
    ```

    `--ca <ca_file>`
    :   Name of the CA file used to sign your certificates. The default file name from the `elasticsearch-certutil` tool is `elastic-stack-ca.p12`.

        1. Enter the password for your CA, or press **Enter** if you did not configure one in the previous step.
        2. Create a password for the certificate and accept the default file name.

            The output file is a keystore named `elastic-certificates.p12`. This file contains a node certificate, node key, and CA certificate.

3. On **every** node in your cluster, copy the `elastic-certificates.p12` file to the `$ES_PATH_CONF` directory.


## Encrypt internode communications with TLS [encrypt-internode-communication]

The transport networking layer is used for internal communication between nodes in a cluster. When security features are enabled, you must use TLS to ensure that communication between the nodes is encrypted.

Now that you’ve generated a certificate authority and certificates, you’ll update your cluster to use these files.

::::{note}
{{es}} monitors all files such as certificates, keys, keystores, or truststores that are configured as values of TLS-related node settings. If you update any of these files, such as when your hostnames change or your certificates are due to expire, {{es}} reloads them. The files are polled for changes at a frequency determined by the global {{es}} `resource.reload.interval.high` setting, which defaults to 5 seconds.
::::


Complete the following steps **for each node in your cluster**. To join the same cluster, all nodes must share the same `cluster.name` value.

1. Open the `$ES_PATH_CONF/elasticsearch.yml` file and make the following changes:

    1. Add the [`cluster-name`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-name) setting and enter a name for your cluster:

        ```yaml
        cluster.name: my-cluster
        ```

    2. Add the [`node.name`](../deploy/self-managed/important-settings-configuration.md#node-name) setting and enter a name for the node. The node name defaults to the hostname of the machine when {{es}} starts.

        ```yaml
        node.name: node-1
        ```

    3. Add the following settings to enable internode communication and provide access to the node’s certificate.

        Because you are using the same `elastic-certificates.p12` file on every node in your cluster, set the verification mode to `certificate`:

        ```yaml
        xpack.security.transport.ssl.enabled: true
        xpack.security.transport.ssl.verification_mode: certificate <1>
        xpack.security.transport.ssl.client_authentication: required
        xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
        xpack.security.transport.ssl.truststore.path: elastic-certificates.p12
        ```

        1. If you want to use hostname verification, set the verification mode to `full`. You should generate a different certificate for each host that matches the DNS or IP address. See the `xpack.security.transport.ssl.verification_mode` parameter in [TLS settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#transport-tls-ssl-settings).

2. If you entered a password when creating the node certificate, run the following commands to store the password in the {{es}} keystore:

    ```shell
    ./bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password
    ```

    ```shell
    ./bin/elasticsearch-keystore add xpack.security.transport.ssl.truststore.secure_password
    ```

3. Complete the previous steps for each node in your cluster.
4. On **every** node in your cluster, start {{es}}. The method for [starting](../maintenance/start-stop-services/start-stop-elasticsearch.md) and [stopping](../maintenance/start-stop-services/start-stop-elasticsearch.md) {{es}} varies depending on how you installed it.

    For example, if you installed {{es}} with an archive distribution (`tar.gz` or `.zip`), you can enter `Ctrl+C` on the command line to stop {{es}}.

    ::::{warning}
    You must perform a full cluster restart. Nodes that are configured to use TLS for transport cannot communicate with nodes that use unencrypted transport connection (and vice-versa).
    ::::


## What’s next? [encrypting-internode-whatsnext]

Congratulations! You’ve encrypted communications between the nodes in your cluster and can pass the [TLS bootstrap check](../deploy/self-managed/bootstrap-checks.md#bootstrap-checks-tls).

To add another layer of security, [set up HTTP TLS](./set-up-basic-security-plus-https.md) to encrypt client communications with both {{es}} and {{kib}}.

For other tasks related with TLS encryption in self-managed deployments, refer to [](./self-tls.md).
