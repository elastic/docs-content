---
applies_to:
  self: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/configuring-stack-security.html
---

# Self-managed certificates and keys [configuring-stack-security]

When you start {{es}} for the first time, the following security configuration occurs automatically:

* [Certificates and keys](../deploy/self-managed/installing-elasticsearch.md#stack-security-certificates) for TLS are generated for the transport and HTTP layers.
* The TLS configuration settings are written to `elasticsearch.yml`.
* A password is generated for the `elastic` user.
* An enrollment token is generated for {{kib}}.

You can then start {{kib}} and enter the enrollment token, which is valid for 30 minutes. This token automatically applies the security settings from your {{es}} cluster, authenticates to {{es}} with the built-in `kibana` service account, and writes the security configuration to `kibana.yml`.

::::{note}
There are [some cases](/deploy-manage/security/security-certificates-keys.md#stack-skip-auto-configuration) where security can’t be configured automatically because the node startup process detects that the node is already part of a cluster, or that security is already configured or explicitly disabled.
::::



## Prerequisites [_prerequisites_12]

* [Download](https://www.elastic.co/downloads/elasticsearch) and unpack the `elasticsearch` package distribution for your environment.
* [Download](https://www.elastic.co/downloads/kibana) and unpack the `kibana` package distribution for your environment.


## Start {{es}} and enroll {{kib}} with security enabled [stack-start-with-security]

1. From the installation directory, start {{es}}.

    ```shell
    bin/elasticsearch
    ```

    The command prints the `elastic` user password and an enrollment token for {{kib}}.

2. Copy the generated `elastic` password and enrollment token. These credentials are only shown when you start {{es}} for the first time.

    ::::{note}
    If you need to reset the password for the `elastic` user or other built-in users, run the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) tool. To generate new enrollment tokens for {{kib}} or {{es}} nodes, run the [`elasticsearch-create-enrollment-token`](elasticsearch://reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool. These tools are available in the {{es}} `bin` directory.

    ::::


    We recommend storing the `elastic` password as an environment variable in your shell. Example:

    ```sh
    export ELASTIC_PASSWORD="your_password"
    ```

3. (Optional) Open a new terminal and verify that you can connect to your {{es}} cluster by making an authenticated call.

    ```shell
    curl --cacert config/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
    ```

4. From the directory where you installed {{kib}}, start {{kib}}.

    ```shell
    bin/kibana
    ```

5. Enroll {{kib}} using either interactive or detached mode.

    * **Interactive mode** (browser)

        1. In your terminal, click the generated link to open {{kib}} in your browser.
        2. In your browser, paste the enrollment token that you copied and click the button to connect your {{kib}} instance with {{es}}.

            ::::{note}
            {{kib}} won’t enter interactive mode if it detects existing credentials for {{es}} (`elasticsearch.username` and `elasticsearch.password`) or an existing URL for `elasticsearch.hosts`.

            ::::

    * **Detached mode** (non-browser)

        Run the `kibana-setup` tool and pass the generated enrollment token with the `--enrollment-token` parameter.

        ```sh
        bin/kibana-setup --enrollment-token <enrollment-token>
        ```



## Enroll additional nodes in your cluster [stack-enroll-nodes]

When {{es}} starts for the first time, the security auto-configuration process binds the HTTP layer to `0.0.0.0`, but only binds the transport layer to localhost. This intended behavior ensures that you can start a single-node cluster with security enabled by default without any additional configuration.

Before enrolling a new node, additional actions such as binding to an address other than `localhost` or satisfying bootstrap checks are typically necessary in production clusters. During that time, an auto-generated enrollment token could expire, which is why enrollment tokens aren’t generated automatically.

Additionally, only nodes on the same host can join the cluster without additional configuration. If you want nodes from another host to join your cluster, you need to set `transport.host` to a [supported value](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#network-interface-values) (such as uncommenting the suggested value of `0.0.0.0`), or an IP address that’s bound to an interface where other hosts can reach it. Refer to [transport settings](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#transport-settings) for more information.

To enroll new nodes in your cluster, create an enrollment token with the `elasticsearch-create-enrollment-token` tool on any existing node in your cluster. You can then start a new node with the `--enrollment-token` parameter so that it joins an existing cluster.

1. In a separate terminal from where {{es}} is running, navigate to the directory where you installed {{es}} and run the [`elasticsearch-create-enrollment-token`](elasticsearch://reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool to generate an enrollment token for your new nodes.

    ```sh
    bin/elasticsearch-create-enrollment-token -s node
    ```

    Copy the enrollment token, which you’ll use to enroll new nodes with your {{es}} cluster.

2. From the installation directory of your new node, start {{es}} and pass the enrollment token with the `--enrollment-token` parameter.

    ```sh
    bin/elasticsearch --enrollment-token <enrollment-token>
    ```

    {{es}} automatically generates certificates and keys in the following directory:

    ```sh
    config/certs
    ```

3. Repeat the previous step for any new nodes that you want to enroll.


## Connect clients to {{es}} [_connect_clients_to_es_5]

When you start {{es}} for the first time, TLS is configured automatically for the HTTP layer. A CA certificate is generated and stored on disk at:

```sh
/etc/elasticsearch/certs/http_ca.crt
```

The hex-encoded SHA-256 fingerprint of this certificate is also output to the terminal. Any clients that connect to {{es}}, such as the [{{es}} Clients](https://www.elastic.co/guide/en/elasticsearch/client/index.html), {{beats}}, standalone {{agent}}s, and {{ls}} must validate that they trust the certificate that {{es}} uses for HTTPS. {{fleet-server}} and {{fleet}}-managed {{agent}}s are automatically configured to trust the CA certificate. Other clients can establish trust by using either the fingerprint of the CA certificate or the CA certificate itself.

If the auto-configuration process already completed, you can still obtain the fingerprint of the security certificate. You can also copy the CA certificate to your machine and configure your client to use it.


### Use the CA fingerprint [_use_the_ca_fingerprint_5]

Copy the fingerprint value that’s output to your terminal when {{es}} starts, and configure your client to use this fingerprint to establish trust when it connects to {{es}}.

If the auto-configuration process already completed, you can still obtain the fingerprint of the security certificate by running the following command. The path is to the auto-generated CA certificate for the HTTP layer.

```sh
openssl x509 -fingerprint -sha256 -in config/certs/http_ca.crt
```

The command returns the security certificate, including the fingerprint. The `issuer` should be `{{es}} security auto-configuration HTTP CA`.

```sh
issuer= /CN={{es}} security auto-configuration HTTP CA
SHA256 Fingerprint=<fingerprint>
```


### Use the CA certificate [_use_the_ca_certificate_5]

If your library doesn’t support a method of validating the fingerprint, the auto-generated CA certificate is created in the following directory on each {{es}} node:

```sh
/etc/elasticsearch/certs/http_ca.crt
```

Copy the `http_ca.crt` file to your machine and configure your client to use this certificate to establish trust when it connects to {{es}}.


## What’s next? [_whats_next]

Congratulations! You’ve successfully started the {{stack}} with security enabled. {{es}} and {{kib}} are secured with TLS on the HTTP layer, and internode communication is encrypted. If you want to enable HTTPS for web traffic, you can [encrypt traffic between your browser and {{kib}}](set-up-basic-security-plus-https.md#encrypt-kibana-browser).


## Security certificates and keys [stack-security-certificates]

When you install {{es}}, the following certificates and keys are generated in the {{es}} configuration directory, which are used to connect a {{kib}} instance to your secured {{es}} cluster and to encrypt internode communication. The files are listed here for reference.

`http_ca.crt`
:   The CA certificate that is used to sign the certificates for the HTTP layer of this {{es}} cluster.

`http.p12`
:   Keystore that contains the key and certificate for the HTTP layer for this node.

`transport.p12`
:   Keystore that contains the key and certificate for the transport layer for all the nodes in your cluster.

`http.p12` and `transport.p12` are password-protected PKCS#12 keystores. {{es}} stores the passwords for these keystores as [secure settings](secure-settings.md). To retrieve the passwords so that you can inspect or change the keystore contents, use the [`bin/elasticsearch-keystore`](elasticsearch://reference/elasticsearch/command-line-tools/elasticsearch-keystore.md) tool.

Use the following command to retrieve the password for `http.p12`:

```sh
bin/elasticsearch-keystore show xpack.security.http.ssl.keystore.secure_password
```

Use the following command to retrieve the password for `transport.p12`:

```sh
bin/elasticsearch-keystore show xpack.security.transport.ssl.keystore.secure_password
```

Additionally, when you use the enrollment token to connect {{kib}} to a secured {{es}} cluster, the HTTP layer CA certificate is retrieved from {{es}} and stored in the {{kib}} `/data` directory. This file establishes trust between {{kib}} and the {{es}} Certificate Authority (CA) for the HTTP layer.


## Cases when security auto configuration is skipped [stack-skip-auto-configuration]

When you start {{es}} for the first time, the node startup process tries to automatically configure security for you. The process runs some checks to determine:

* If this is the first time that the node is starting
* Whether security is already configured
* If the startup process can modify the node configuration

If any of those checks fail, there’s a good indication that you [manually configured security](manually-configure-security-in-self-managed-cluster.md), or don’t want security to be configured automatically. In these cases, the node starts normally using the existing configuration.

::::{important}
If you redirect {{es}} output to a file, security autoconfiguration is skipped. Autoconfigured credentials can only be viewed on the terminal the first time you start {{es}}. If you need to redirect output to a file, start {{es}} without redirection the first time and use redirection on all subsequent starts.
::::



### Existing environment detected [stack-existing-environment-detected]

If certain directories already exist, there’s a strong indication that the node was started previously. Similarly, if certain files *don’t* exist, or we can’t read or write to specific files or directories, then we’re likely not running as the user who installed {{es}} or an administrator imposed restrictions. If any of the following environment checks are true, security isn’t configured automatically.

The {{es}} `/data` directory exists and isn’t empty
:   The existence of this directory is a strong indicator that the node was started previously, and might already be part of a cluster.

The `elasticsearch.yml` file doesn’t exist (or isn’t readable), or the `elasticsearch.keystore` isn’t readable
:   If either of these files aren’t readable, we can’t determine whether {{es}} security features are already enabled. This state can also indicate that the node startup process isn’t running as a user with sufficient privileges to modify the node configuration.

The {{es}} configuration directory isn’t writable
:   This state likely indicates that an administrator made this directory read-only, or that the user who is starting {{es}} is not the user that installed {{es}}.


### Existing settings detected [stack-existing-settings-detected]

The following settings are incompatible with security auto configuration. If any of these settings exist, the node startup process skips configuring security automatically and the node starts normally.

* [`node.roles`](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles) is set to a value where the node can’t be elected as `master`, or if the node can’t hold data
* [`xpack.security.autoconfiguration.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#general-security-settings) is set to `false`
* [`xpack.security.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#general-security-settings) has a value set
* Any of the [`xpack.security.transport.ssl.*`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#transport-tls-ssl-settings) or [`xpack.security.http.ssl.*`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#http-tls-ssl-settings) settings have a value set in the `elasticsearch.yml` configuration file or in the `elasticsearch.keystore`
* Any of the `discovery.type`, `discovery.seed_hosts`, or `cluster.initial_master_nodes` [discovery and cluster formation settings](elasticsearch://reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md) have a value set

    ::::{note}
    Exceptions are when `discovery.type` is set to `single-node`, or when `cluster.initial_master_nodes` exists but contains only the name of the current node.

    ::::


