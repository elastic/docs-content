---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-self-managed-running.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Step 4: Run the backend applications [profiling-self-managed-running]

The next step is to run the backend applications. To do this:

1. [Create API keys](#profiling-self-managed-create-api-keys) to authenticate the backend applications.
2. Run the application on [Linux](#profiling-self-managed-running-linux) or [Kubernetes](#profiling-self-managed-running-kubernetes).


## Create API keys [profiling-self-managed-create-api-keys]

Both the collector and symbolizer need to authenticate to Elasticsearch to process profiling data. For this, you need to create an API key for each application.

Refer to [Create an API key](/deploy-manage/api-keys/elasticsearch-api-keys.md#create-api-key) to create an API key using {{kib}}. Select a **User API key** and assign the following permissions  under **Control security privileges**:

```json
{
  "profiling": {
    "cluster": [
      "monitor"
    ],
    "indices": [
      {
        "names": [
          "profiling-*"
        ],
        "privileges": [
          "read",
          "write"
        ]
      }
    ]
  }
}
```

Store the "Encoded" version of the API keys, as you will need them to run the Universal Profiling backend. Continue to [Run on Linux](#profiling-self-managed-running-linux) or [Run on Kubernetes](#profiling-self-managed-running-kubernetes) for information on running the backend applications.


## Run on Linux [profiling-self-managed-running-linux]

Before running the backend applications on Linux, we recommend creating [configuration files](#profiling-self-managed-running-linux-configfile) to manage the applications. CLI flags are also supported, but they might result in a more complex management of the backend applications.

Install the backend applications using one of the following options:

1. [OS packages (DEB/RPM)](#profiling-self-managed-install-os-packages)
2. [OCI containers](#profiling-self-managed-running-linux-container)
3. [Binary](#profiling-self-managed-running-linux-binary): orchestrated with your configuration management system of choice (Ansible, Puppet, Chef, Salt, etc.)


## Create configuration files [profiling-self-managed-running-linux-configfile]

The configuration files are in YAML format, and are composed of two top-level sections: an "application" section, and an "output" section.

The "application" section contains the configuration for the backend applications, and the "output" section contains the configuration to connect to where the data will be read and sent to. The "application" section is named after the name of the binary. The "output" section currently supports only Elasticsearch.

The configuration files are read from the following default locations:

* Collector: `/etc/Elastic/universal-profiling/pf-elastic-collector.yml`
* Symbolizer: `/etc/Elastic/universal-profiling/pf-elastic-symbolizer.yml`

You can customize the location of the configuration files by using the `-c` flag when running the application.

For the sake of simplicity, we will use the default locations in the examples below. We also display the default application settings; you can refer to the comments in the YAML to understand how to customize them.


### Collector configuration file [profiling-self-managed-running-linux-configfile-collector]

Copy the content of the snippet below in the `/etc/Elastic/universal-profiling/pf-elastic-collector.yml` file.

Customize the content of `pf-elastic-collector.auth.secret_token` with a secret token of your choice. This token will be used by the Universal Profiling Agent to authenticate to the collector; you cannot use an empty string as a token. Adjust the `ssl` section if you want to protect the collector’s endpoint with TLS.

Customize the content of the `output.elasticsearch` section, using the Elasticsearch endpoint and [API key](#profiling-self-managed-create-api-keys) to set the `hosts` and `api_key` values, respectively. Adjust the `protocol` value and other TLS related settings as needed.

::::{dropdown} Collector configuration file
```yaml
pf-elastic-collector:
  # Defines the host and port the server is listening on.
  host: "0.0.0.0:8260"

  # Verbose log output option.
  #verbose: true

  # Configure metrics exposition. Both expvar and Prometheus formats are supported. Both can be
  # configured at the same time. By default, no metrics are exposed.
  # 'prometheus_host' can only be configured with a 'host:port' pair.
  # 'expvar_host' can be configured either with a 'host:port' pair or with a Unix Domain Socket path (with a  'unix://' prefix).
  # When host:port is used, an HTTP server is exposed. The server does not support TLS.
  # An empty value disables metrics exposition for the corresponding format.
  #metrics:
  #  prometheus_host: 'localhost:9090'
  #  expvar_host: unix:///tmp/collector-metrics.sock

  # Define the suggested upper limit of memory that pf-elastic-collector should apply. Using a lower
  # amount of memory might trigger garbage collection more often.
  #memory_limit: 500M

  # Agent authorization configuration. If no methods are defined, all requests will be allowed.
  auth:
    # Define a shared secret token for authorizing agents.
    secret_token: ""

  # Controls storage of Universal Profiling agent metrics/metadata to the customer's cluster and to a
  # cluster controlled by Elastic. By default, the full set of metrics and metadata is written to
  # an Elastic-controlled cluster, and a subset of metrics and metadata to the customer
  # cluster. These are used to monitor agent health and debug/resolve issues.
  agent_metrics:
    # Do not write Universal Profiling agent metrics/metadata to a centralized (non-customer controlled)
    # cluster. This does not affect writing metrics/metadata to the customer cluster.
    #disable: false

    # Write full set of Universal Profiling agent metrics to the customer ES cluster. If false, which
    # is the default, only a limited set of CPU usage and I/O metrics will be written.
    #write_all: false

  # Enable secure communication between pf-host-agent and pf-elastic-collector.
  ssl:
    enabled: false

    # Path to file containing the certificate for server authentication.
    # Needs to be configured when ssl is enabled.
    #certificate: ''

    # Path to file containing server certificate key.
    # Needs to be configured when ssl is enabled.
    #key: ''

    # Optional configuration options for ssl communication.

    # Passphrase for decrypting the Certificate Key.
    # It is recommended to use the provided keystore instead of entering the passphrase in plain text.
    #key_passphrase: ''

    # List of supported/valid protocol versions. By default TLS versions 1.3 is enabled.
    #supported_protocols: [TLSv1.3]

    # Configure cipher suites to be used for SSL connections.
    # Note that cipher suites are not configurable for TLS 1.3.
    #cipher_suites: []

    # Configure curve types for ECDHE based cipher suites.
    #curve_types: []

#================================ Outputs =================================

# Configure the output to use when sending the data collected by pf-elastic-collector.

#-------------------------- Elasticsearch output --------------------------
output:
  elasticsearch:
    # Array of hosts to connect to.
    # Scheme and port can be left out and will be set to the default (`http` and `9200`).
    # In case you specify an additional path, the scheme is required: `http://localhost:9200/path`.
    # IPv6 addresses should always be defined as: `https://[2001:db8::1]:9200`.
    hosts: ["localhost:9200"]

    # Set gzip compression level.
    #compression_level: 0

    # Protocol - either `http` (default) or `https`.
    protocol: "https"

    # Authentication credentials - either API key or username/password.
    #api_key: "id:api_key"

    # Optional HTTP Path.
    #path: "/elasticsearch"

    # Proxy server url.
    #proxy_url: http://proxy:3128

    # The number of times a particular Elasticsearch index operation is attempted. If
    # the indexing operation doesn't succeed after this many retries, the events are
    # dropped. The default is 3.
    #max_retries: 3

    # Enable custom SSL settings. Set to false to ignore custom SSL settings for secure communication.
    #ssl.enabled: true

    # Optional SSL configuration options. SSL is off by default, change the `protocol` option if you want to enable `https`.
    #
    # Control the verification of Elasticsearch certificates. Valid values are:
    # * full, which verifies that the provided certificate is signed by a trusted
    # authority (CA) and also verifies that the server's hostname (or IP address)
    # matches the names identified within the certificate.
    # * strict, which verifies that the provided certificate is signed by a trusted
    # authority (CA) and also verifies that the server's hostname (or IP address)
    # matches the names identified within the certificate. If the Subject Alternative
    # Name is empty, it returns an error.
    # * certificate, which verifies that the provided certificate is signed by a
    # trusted authority (CA), but does not perform any hostname verification.
    #  * none, which performs no verification of the server's certificate. This
    # mode disables many of the security benefits of SSL/TLS and should only be used
    # after very careful consideration. It is primarily intended as a temporary
    # diagnostic mechanism when attempting to resolve TLS errors; its use in
    # production environments is strongly discouraged.
    #ssl.verification_mode: full

    # List of supported/valid TLS versions. By default all TLS versions 1.0 up to
    # 1.2 are enabled.
    #ssl.supported_protocols: [TLSv1.0, TLSv1.1, TLSv1.2]

    # List of root certificates for HTTPS server verifications.
    #ssl.certificate_authorities: ["/etc/pki/root/ca.pem"]

    # Certificate for SSL client authentication.
    #ssl.certificate: "/etc/pki/client/cert.pem"

    # Client Certificate Key
    #ssl.key: "/etc/pki/client/cert.key"

    # Optional passphrase for decrypting the Certificate Key.
    # It is recommended to use the provided keystore instead of entering the passphrase in plain text.
    #ssl.key_passphrase: ''

    # Configure cipher suites to be used for SSL connections.
    #ssl.cipher_suites: []

    # Configure curve types for ECDHE based cipher suites.
    #ssl.curve_types: []

    # Configure what types of renegotiation are supported. Valid options are
    # never, once, and freely. Default is never.
    #ssl.renegotiation: never
```

::::



### Symbolizer configuration file [profiling-self-managed-running-linux-configfile-symbolizer]

Copy the content of the snippet below in the `/etc/Elastic/universal-profiling/pf-elastic-symbolizer.yml` file.

You don’t need to customize any values in the `pf-elastic-symbolizer` section. Adjust the `ssl` section if you want to protect the symbolizer’s endpoint with TLS.

Customize the content of the `output.elasticsearch` section, using the Elasticsearch endpoint and [API key](#profiling-self-managed-create-api-keys) to set the `hosts` and `api_key` values, respectively. Adjust the `protocol` value and other TLS related settings as needed.

::::{dropdown} Symbolizer configuration file
```yaml
pf-elastic-symbolizer:
  # Defines the host and port the server is listening on.
  host: "0.0.0.0:8240"

  # Endpoint for the service to connect to and query for software packages.
  # Do not set this value unless you are running a local instance of the debug symbols mirror.
  endpoint: ""

  # Verbose log output option. (default: false)
  #verbose: true

  # Configure metrics exposition. Both expvar and Prometheus formats are supported. Both can be
  # configured at the same time. By default, no metrics are exposed.
  # 'prometheus_host' can only be configured with a 'host:port' pair.
  # 'expvar_host' can be configured either with a 'host:port' pair or with a Unix Domain Socket path (with a  'unix://' prefix).
  # When host:port is used, an HTTP server is exposed. The server does not support TLS.
  # An empty value disables metrics exposition for the corresponding format.
  #metrics:
  #  prometheus_host: 'localhost:9090'
  #  expvar_host: unix:///tmp/collector-metrics.sock

  # Define the suggested upper limit of memory that pf-elastic-symbolizer should apply. Using a lower
  # amount of memory might trigger garbage collection more often. (default: 200MB)
  #memory_limit: 500M

  # Enable secure communication between symbtool and pf-elastic-symbolizer.
  ssl:
    enabled: false

    # Path to file containing the certificate for server authentication.
    # Needs to be configured when ssl is enabled.
    #certificate: ''

    # Path to file containing server certificate key.
    # Needs to be configured when ssl is enabled.
    #key: ''

    # Optional configuration options for ssl communication.

    # Passphrase for decrypting the Certificate Key.
    # It is recommended to use the provided keystore instead of entering the passphrase in plain text.
    #key_passphrase: ''

    # List of supported/valid protocol versions. By default TLS versions 1.1 up to 1.3 are enabled.
    #supported_protocols: [TLSv1.1, TLSv1.2, TLSv1.3]

    # Configure cipher suites to be used for SSL connections.
    # Note that cipher suites are not configurable for TLS 1.3.
    #cipher_suites: []

    # Configure curve types for ECDHE based cipher suites.
    #curve_types: []

#================================ Outputs =================================

# Configure the output to use when sending the data collected by pf-elastic-symbolizer.

#-------------------------- Elasticsearch output --------------------------
output:
  elasticsearch:
    # Array of hosts to connect to.
    # Scheme and port can be left out and will be set to the default (`http` and `9200`).
    # In case you specify an additional path, the scheme is required: `http://localhost:9200/path`.
    # IPv6 addresses should always be defined as: `https://[2001:db8::1]:9200`.
    hosts: ["localhost:9200"]

    # Set gzip compression level.
    #compression_level: 0

    # Protocol - either `http` (default) or `https`.
    protocol: "https"

    # Authentication credentials - either API key or username/password.
    #api_key: "id:api_key"

    # Optional HTTP Path.
    #path: "/elasticsearch"

    # Proxy server url.
    #proxy_url: http://proxy:3128

    # The number of times a particular Elasticsearch index operation is attempted. If
    # the indexing operation doesn't succeed after this many retries, the events are
    # dropped. The default is 3.
    #max_retries: 3

    # Enable custom SSL settings. Set to false to ignore custom SSL settings for secure communication.
    #ssl.enabled: true

    # Optional SSL configuration options. SSL is off by default, change the `protocol` option if you want to enable `https`.
    #
    # Control the verification of Elasticsearch certificates. Valid values are:
    # * full, which verifies that the provided certificate is signed by a trusted
    # authority (CA) and also verifies that the server's hostname (or IP address)
    # matches the names identified within the certificate.
    # * strict, which verifies that the provided certificate is signed by a trusted
    # authority (CA) and also verifies that the server's hostname (or IP address)
    # matches the names identified within the certificate. If the Subject Alternative
    # Name is empty, it returns an error.
    # * certificate, which verifies that the provided certificate is signed by a
    # trusted authority (CA), but does not perform any hostname verification.
    #  * none, which performs no verification of the server's certificate. This
    # mode disables many of the security benefits of SSL/TLS and should only be used
    # after very careful consideration. It is primarily intended as a temporary
    # diagnostic mechanism when attempting to resolve TLS errors; its use in
    # production environments is strongly discouraged.
    #ssl.verification_mode: full

    # List of supported/valid TLS versions. By default all TLS versions 1.0 up to
    # 1.2 are enabled.
    #ssl.supported_protocols: [TLSv1.0, TLSv1.1, TLSv1.2]

    # List of root certificates for HTTPS server verifications.
    #ssl.certificate_authorities: ["/etc/pki/root/ca.pem"]

    # Certificate for SSL client authentication.
    #ssl.certificate: "/etc/pki/client/cert.pem"

    # Client Certificate Key
    #ssl.key: "/etc/pki/client/cert.key"

    # Optional passphrase for decrypting the Certificate Key.
    # It is recommended to use the provided keystore instead of entering the passphrase in plain text.
    #ssl.key_passphrase: ''

    # Configure cipher suites to be used for SSL connections.
    #ssl.cipher_suites: []

    # Configure curve types for ECDHE based cipher suites.
    #ssl.curve_types: []

    # Configure what types of renegotiation are supported. Valid options are
    # never, once, and freely. Default is never.
    #ssl.renegotiation: never
```

::::



## OS packages (DEB/RPM) [profiling-self-managed-install-os-packages]

Follow these steps to install the backend using OS packages.


### DEB packages [profiling-run-backend-deb]

1. Configure the APT repository:

    ```shell
    wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
    sudo apt-get install apt-transport-https
    echo "deb https://artifacts.elastic.co/packages/9.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-9.x.list
    ```

2. Install the packages:

    ```shell
    sudo apt update
    sudo apt install -y pf-elastic-collector pf-elastic-symbolizer
    ```



### RPM packages [profiling-run-backend-rpm]

For RPM packages, configure the YUM repository and install the packages:

1. Download and install the public signing key:

    ```sh
    sudo rpm --import https://packages.elastic.co/GPG-KEY-elasticsearch
    ```

2. Create a file with a `.repo` extension (for example, `elastic.repo`) in your `/etc/yum.repos.d/` directory and add the following lines:

    ```sh
    [elastic-9.x]
    name=Elastic repository for 9.x packages
    baseurl=https://artifacts.elastic.co/packages/9.x/yum
    gpgcheck=1
    gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
    enabled=1
    autorefresh=1
    type=rpm-md
    ```

3. Install the backend services by running:

    ```sh
    sudo yum update
    sudo yum install -y pf-elastic-collector pf-elastic-symbolizer
    ```



### Run the services [_run_the_services]

After installing the packages, enable and start the systemd services:

```shell
sudo systemctl enable pf-elastic-collector
sudo systemctl start pf-elastic-collector

sudo systemctl enable pf-elastic-symbolizer
sudo systemctl start pf-elastic-symbolizer
```

Now you can check the services' logs to spot any problems:

```shell
sudo journalctl -xu pf-elastic-collector
sudo journalctl -xu pf-elastic-symbolizer
```

Refer to [Troubleshooting Universal Profiling backend](/troubleshoot/observability/troubleshoot-your-universal-profiling-agent-deployment/troubleshoot-universal-profiling-backend.md) for more information on troubleshooting possible errors in the logs.


### OCI containers [profiling-self-managed-running-linux-container]

We provide OCI images in the Elastic registry to run the backend services in containers. The images are multi-platform, so they both work on x86_64 and ARM64 architectures.

With the config file in place in your system, you can run the containers with the following commands (the example command uses Docker, but any OCI runtime will work):

1. Collector:

    ```shell
    docker run -d --name pf-elastic-collector -p 8260:8260 -v /etc/Elastic/universal-profiling/pf-elastic-collector.yml:/pf-elastic-collector.yml:ro \
      docker.elastic.co/observability/profiling-collector:{version} -c /pf-elastic-collector.yml
    ```

2. Symbolizer:

    ```shell
    docker run -d --name pf-elastic-symbolizer -p 8240:8240 -v /etc/Elastic/universal-profiling/pf-elastic-symbolizer.yml:/pf-elastic-symbolizer.yml:ro \
      docker.elastic.co/observability/profiling-symbolizer:{version} -c /pf-elastic-symbolizer.yml
    ```


With the above commands, the backend containers will serve the HTTP endpoints on the host ports 8260 and 8240, respectively. We provided the `-v` flag to mount the configuration files in the containers, and then we used the `-c` flag to tell the applications to read the configuration files from the mounted path.

Container processes will be running in the background, you can check the logs with `docker logs <container_name>`, e.g.

```shell
docker logs pf-elastic-collector
docker logs pf-elastic-symbolizer
```


### Binary [profiling-self-managed-running-linux-binary]

1. Download and unpack the binaries for your platform:

    For x86_64

    ```shell subs=true
    wget -O- "https://artifacts.elastic.co/downloads/prodfiler/pf-elastic-collector-{{version.stack}}-linux-x86_64.tar.gz" | tar xzf -
    wget -O- "https://artifacts.elastic.co/downloads/prodfiler/pf-elastic-symbolizer-{{version.stack}}-linux-x86_64.tar.gz" | tar xzf -
    ```

    For ARM64

    ```shell subs=true
    wget -O- "https://artifacts.elastic.co/downloads/prodfiler/pf-elastic-collector-{{version.stack}}-linux-arm64.tar.gz" | tar xzf -
    wget -O- "https://artifacts.elastic.co/downloads/prodfiler/pf-elastic-symbolizer-{{version.stack}}-linux-arm64.tar.gz" | tar xzf -
    ```

2. Copy the `pf-elastic-collector` and `pf-elastic-symbolizer` binaries to a directory in the machine’s `PATH`.
3. Run the backend application processes, instructing them to read the configuration files created previously.

    ```shell
    pf-elastic-collector -c /etc/Elastic/universal-profiling/pf-elastic-collector.yml
    pf-elastic-symbolizer -c /etc/Elastic/universal-profiling/pf-elastic-symbolizer.yml
    ```


If you want to customize configuration options passed to the binaries, you can use command line flags. All overrides are specified using the `-E` flag. For example, if you want to override the `host` value for the `pf-elastic-collector` application, you can use the `-E pf-elastic-collector.host` flag as follows:

```shell
pf-elastic-collector -c /etc/Elastic/universal-profiling/pf-elastic-collector.yml -E pf-elastic-collector.host=0.0.0.0:8844
```

In the previous example, we configured the collector to listen on all network interfaces on port 8844, instead of the 8260 value contained in the YAML configuration file.

You can use the `-E` flag to override any values contained in the configuration files, as lng as you specify the full YAML path on the command line flag. We recommend sticking with the configuration files for simpler orchestration.

The same configuration overrides and recommendations apply to the `pf-elastic-symbolizer` binary.


## Run on Kubernetes [profiling-self-managed-running-kubernetes]

We provide [Helm](https://helm.io) charts to deploy the backend services on Kubernetes.

To install the backend services, you need to add the Elastic Helm repository to your Helm installation and then install the charts.

We recommend creating a `values.yaml` file defining the Kubernetes-specific options of the chart. If you want to stick with the default values provided by the chart, you don’t need to create a `values.yaml` file for each chart. For the applications' configuration, you can reuse the configuration files detailed in ["Create configuration files"](#profiling-self-managed-running-linux-configfile) and pass them to Helm as a values file (using the `--values` of `-f` flags), or copy them in the `values.yaml` file.

In the example below we don’t apply any modifications to the Kubernetes configs, so we will use the default values provided by the chart.

1. Install and update the Elastic Helm registry:

    ```shell
    helm repo add elastic https://helm.elastic.co
    helm repo update elastic
    ```

2. Install the charts (we are using the `universal-profiling` namespace, but you can customize at will):

    ```shell
    helm install --create-namespace -n universal-profiling collector elastic/profiling-collector -f /etc/Elastic/universal-profiling/pf-elastic-collector.yml
    helm install --create-namespace -n universal-profiling symbolizer elastic/profiling-symbolizer -f /etc/Elastic/universal-profiling/pf-elastic-symbolizer.yml
    ```

3. Check the pods are running and read their logs, by following the steps listed in the output of the `helm install` commands.

::::{note}
In the previous examples, we used the charts' default values to configure Kubernetes resources. These **do not** include the creation of an `Ingress` resource. If you want to expose the services to an Universal Profiling Agent and symbtool deployment outside the Kubernetes cluster, you need to set up the `ingress` section of each chart.
::::


Continue to [Step 5: Next steps](step-5-next-steps.md).
