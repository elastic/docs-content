---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/secure-logstash-connections.html
---

# Configure SSL/TLS for the Logstash output [secure-logstash-connections]

To send data from {{agent}} to {{ls}} securely, you need to configure Transport Layer Security (TLS). Using TLS ensures that your {{agent}}s send encrypted data to trusted {{ls}} servers, and that your {{ls}} servers receive data from trusted {{agent}} clients.


## Prerequisites [secure-logstash-prereqs]

* Make sure your [subscription level](https://www.elastic.co/subscriptions) supports output to {{ls}}.
* On Windows, add port 8220 for {{fleet-server}} and 5044 for {{ls}} to the inbound port rules in Windows Advanced Firewall.
* If you are connecting to a self-managed {{es}} cluster, you need the CA certificate that was used to sign the certificates for the HTTP layer of {{es}} cluster. For more information, refer to the [{{es}} security docs](/deploy-manage/deploy/self-managed/installing-elasticsearch.md).


## Generate custom certificates and private keys [generate-logstash-certs]

You can use whatever process you typically use to generate PEM-formatted certificates. The examples shown here use the `certutil` tool provided by {{es}}.

::::{tip}
The `certutil` tool is not available on {{ecloud}}, but you can still use it to generate certificates for {{agent}} to {{ls}} connections. Just [download an {{es}} package](https://www.elastic.co/downloads/elasticsearch), extract it to a local directory, and run the `elasticsearch-certutil` command. There’s no need to start {{es}}!
::::


1. Generate a certificate authority (CA). Skip this step if you want to use an existing CA.

    ```shell
    ./bin/elasticsearch-certutil ca --pem
    ```

    This command creates a zip file that contains the CA certificate and key you’ll use to sign the certificates. Extract the zip file:

    :::{image} images/ca-certs.png
    :alt: Screen capture of a folder called ca that contains two files: ca.crt and ca.key
    :::

2. Generate a client SSL certificate signed by your CA. For example:

    ```shell
    ./bin/elasticsearch-certutil cert \
      --name client \
      --ca-cert /path/to/ca/ca.crt \
      --ca-key /path/to/ca/ca.key \
      --pem
    ```

    Extract the zip file:

    :::{image} images/client-certs.png
    :alt: Screen capture of a folder called client that contains two files: client.crt and client.key
    :::

3. Generate a {{ls}} SSL certificate signed by your CA. For example:

    ```shell
    ./bin/elasticsearch-certutil cert \
      --name logstash \
      --ca-cert /path/to/ca/ca.crt \
      --ca-key /path/to/ca/ca.key \
      --dns your.host.name.here \
      --ip 192.0.2.1 \
      --pem
    ```

    Extract the zip file:

    :::{image} images/logstash-certs.png
    :alt: Screen capture of a folder called logstash that contains two files: logstash.crt and logstash.key
    :::

4. Convert the {{ls}} key to pkcs8. For example, on Linux run:

    ```shell
    openssl pkcs8 -inform PEM -in logstash.key -topk8 -nocrypt -outform PEM -out logstash.pkcs8.key
    ```


Store these files in a secure location.


## Configure the {{ls}} pipeline [configure-ls-ssl]

::::{tip}
If you’ve already created the {{ls}} `elastic-agent-pipeline.conf` pipeline and added it to `pipelines.yml`, skip to the example configurations and modify your pipeline configuration as needed.
::::


In your {{ls}} configuration directory, open the `pipelines.yml` file and add the following configuration. Replace the path to your file.

```yaml
- pipeline.id: elastic-agent-pipeline
  path.config: "/etc/path/to/elastic-agent-pipeline.conf"
```

In the `elastic-agent-pipeline.conf` file, add the pipeline configuration. Note that the configuration needed for {{ech}} is different from self-managed {{es}} clusters. If you copied the configuration shown in {{fleet}}, adjust it as needed.

{{ech}} example:

```text
input {
  elastic_agent {
    port => 5044
    ssl_enabled => true
    ssl_certificate_authorities => ["/path/to/ca.crt"]
    ssl_certificate => "/path/to/logstash.crt"
    ssl_key => "/path/to/logstash.pkcs8.key"
    ssl_client_authentication => "required"
  }
}

output {
  elasticsearch {
    cloud_id => "xxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx=" <1>
    api_key => "xxxx:xxxx" <2>
    data_stream => true
    ssl => true <3>
  }
}
```

1. Use the `cloud_id` shown on your deployment page in {{ecloud}}.
2. In {{fleet}}, you can generate this API key when you add a {{ls}} output.
3. {{ech}} uses standard publicly trusted certificates, so there’s no need specify other SSL settings here.


Self-managed {{es}} cluster example:

```text
input {
  elastic_agent {
    port => 5044
    ssl_enabled => true
    ssl_certificate_authorities => ["/path/to/ca.crt"]
    ssl_certificate => "/path/to/logstash.crt"
    ssl_key => "/path/to/logstash.pkcs8.key"
    ssl_client_authentication => "required"
  }
}

output {
  elasticsearch {
    hosts => "https://xxxx:9200"
    api_key => "xxxx:xxxx"
    data_stream => true
    ssl => true
    cacert => "/path/to/http_ca.crt" <1>
  }
}
```

1. Use the certificate that was generated for {{es}}.


To learn more about the {{ls}} configuration, refer to:

* [{{agent}} input plugin](logstash://docs/reference/plugins-inputs-elastic_agent.md)
* [{{es}} output plugin](logstash://docs/reference/plugins-outputs-elasticsearch.md)
* [Secure your connection to {{es}}](logstash://docs/reference/secure-connection.md)

When you’re done configuring the pipeline, restart {{ls}}:

```shell
bin/logstash
```


## Add a {{ls}} output to {{fleet}} [add-ls-output]

This section describes how to add a {{ls}} output and configure SSL settings in {{fleet}}. If you’re running {{agent}} standalone, refer to the [{{ls}} output](/reference/ingestion-tools/fleet/logstash-output.md) configuration docs.

1. In {{kib}}, go to **{{fleet}} > Settings**.
2. Under **Outputs**, click **Add output**. If you’ve been following the {{ls}} steps in {{fleet}}, you might already be on this page.
3. Specify a name for the output.
4. For **Type**, select **Logstash**.
5. Under **Logstash hosts**, specify the host and port your agents will use to connect to {{ls}}. Use the format `host:port`.
6. In the **Server SSL certificate authorities** field, paste in the entire contents of the `ca.crt` file you [generated earlier](#generate-logstash-certs).
7. In the **Client SSL certificate** field, paste in the entire contents of the `client.crt` file you generated earlier.
8. In the **Client SSL certificate key** field, paste in the entire contents of the `client.key` file you generated earlier.

:::{image} images/add-logstash-output.png
:alt: Screen capture of a folder called `logstash` that contains two files: logstash.crt and logstash.key
:class: screenshot
:::

When you’re done, save and apply the settings.


## Select the {{ls}} output in an agent policy [use-ls-output]

{{ls}} is now listening for events from {{agent}}, but events are not streaming into {{es}} yet. You need to select the {{ls}} output in an agent policy. You can edit an existing policy or create a new one:

1. In {{kib}}, go to **{{fleet}} > Agent policies** and either create a new agent policy or click an existing policy to edit it:

    * To change the output settings in a new policy, click **Create agent policy** and expand **Advanced options**.
    * To change the output settings in an existing policy, click the policy to edit it, then click **Settings**.

2. Set **Output for integrations** and (optionally) **Output for agent monitoring** to use the {{ls}} output you created earlier. You might need to scroll down to see these options

    :::{image} images/agent-output-settings.png
    :alt: Screen capture showing the {{ls}} output policy selected in an agent policy
    :class: screenshot
    :::

3. Save your changes.

Any {{agent}}s enrolled in the agent policy will begin sending data to {{es}} via {{ls}}. If you don’t have any installed {{agent}}s enrolled in the agent policy, do that now.

There might be a slight delay while the {{agent}}s update to the new policy and connect to {{ls}} over a secure connection.


## Test the connection [test-ls-connection]

To make sure {{ls}} is sending data, run the following command from the host where {{ls}} is running:

```shell
curl -XGET localhost:9600/_node/stats/events
```

The request should return stats on the number of events in and out. If these values are 0, check the {{agent}} logs for problems.

When data is streaming to {{es}}, go to **{{observability}}** and click **Metrics** to view metrics about your system.

