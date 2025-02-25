# Installing in an air-gapped environment [air-gapped-install]

Some components of the {{stack}} require additional configuration and local dependencies in order to deploy in environments without internet access. This guide gives an overview of this setup scenario and helps bridge together existing documentation for individual parts of the stack.

* [1. Self-Managed Install (Linux)](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-self-managed-linux)

    * [1.1. {{es}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elasticsearch)
    * [1.2. {{kib}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-kibana)
    * [1.3. {{beats}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-beats)
    * [1.4. {{ls}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-logstash)
    * [1.5. {{agent}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-agent)
    * [1.6. {{fleet-server}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-fleet)
    * [1.7. Elastic APM](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-apm)
    * [1.8. {{ems}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-maps-service)
    * [1.9. {{package-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-package-registry)
    * [1.10. {{artifact-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry)
    * [1.11. Elastic Endpoint Artifact Repository](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-endpoint-artifact-repository)
    * [1.12 {{ml-cap}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-machine-learning)


* [2. Kubernetes & OpenShift Install](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-kubernetes-and-openshift)

    * [2.1. Elastic Kubernetes Operator (ECK)](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-k8s-os-elastic-kubernetes-operator)
    * [2.2. Elastic Package Registry](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-k8s-os-elastic-package-registry)
    * [2.3. {{artifact-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-k8s-os-elastic-artifact-registry)
    * [2.4. Elastic Endpoint Artifact Repository](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-k8s-os-elastic-endpoint-artifact-repository)
    * [2.5. Ironbank Secure Images for Elastic](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-k8s-os-ironbank-secure-images)


* [3.0 {{ece}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-ece)

* [Appendix A - {{package-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-package-registry-example)
* [Appendix B - {{artifact-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry-example)
* [Appendix C - EPR Kubernetes Deployment](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-epr-kubernetes-example)
* [Appendix D - Agent Integration Guide](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-agent-integration-guide)

    * [D.1. Terminology](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-agent-integration-terminology)
    * [D.2. How to configure](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-agent-integration-configure)

        * [D.2.1. Using the {{kib}} UI](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-agent-integration-configure-kibana)
        * [D.2.2. Using the `kibana.yml` config file](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-agent-integration-configure-yml)
        * [D.2.3. Using the {{kib}} {{fleet}} API](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-agent-integration-configure-fleet-api)


::::{note}
If you’re working in an air-gapped environment and have a subscription level that includes Support coverage, [contact us](https://www.elastic.co/contact) if you’d like to request an offline version of the Elastic documentation.
::::



### 1. Self-Managed Install (Linux) [air-gapped-self-managed-linux]

Refer to the section for each Elastic component for air-gapped installation configuration and dependencies in a self-managed Linux environment.


#### 1.1. {{es}} [air-gapped-elasticsearch]

Air-gapped install of {{es}} may require additional steps in order to access some of the features. General install and configuration guides are available in the [{{es}} install documentation](../../../deploy-manage/deploy/self-managed/installing-elasticsearch.md).

Specifically:

* To be able to use the GeoIP processor, refer to [the GeoIP processor documentation](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/enrich-processor/geoip-processor.md#manually-update-geoip-databases) for instructions on downloading and deploying the required databases.
* Refer to [{{ml-cap}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-machine-learning) for instructions on deploying the Elastic Learned Sparse EncodeR (ELSER) natural language processing (NLP) model and other trained {{ml}} models.


#### 1.2. {{kib}} [air-gapped-kibana]

Air-gapped install of {{kib}} may require a number of additional services in the local network in order to access some of the features. General install and configuration guides are available in the [{{kib}} install documentation](../../../deploy-manage/deploy/self-managed/install-kibana.md).

Specifically:

* To be able to use {{kib}} mapping visualizations, you need to set up and configure the [Elastic Maps Service](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-maps-service).
* To be able to use {{kib}} sample data, install or update hundreds of prebuilt alert rules, and explore available data integrations, you need to set up and configure the [{{package-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-package-registry).
* To provide detection rule updates for {{endpoint-sec}} agents, you need to set up and configure the [Elastic Endpoint Artifact Repository](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-endpoint-artifact-repository).
* To access the APM integration, you need to set up and configure [Elastic APM](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-apm).
* To install and use the Elastic documentation for {{kib}} AI assistants, you need to set up and configure the [Elastic product documentation for {{kib}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-kibana-product-documentation).


#### 1.3. {{beats}} [air-gapped-beats]

Elastic {{beats}} are light-weight data shippers. They do not require any unique setup in the air-gapped scenario. To learn more, refer to the [{{beats}} documentation](asciidocalypse://docs/beats/docs/reference/index.md).


#### 1.4. {{ls}} [air-gapped-logstash]

{{ls}} is a versatile data shipping and processing application. It does not require any unique setup in the air-gapped scenario. To learn more, refer to the [{{ls}} documentation](asciidocalypse://docs/logstash/docs/reference/index.md).


#### 1.5. {{agent}} [air-gapped-elastic-agent]

Air-gapped install of {{agent}} depends on the [{{package-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-package-registry) and the [{{artifact-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry) for most use-cases. The agent itself is fairly lightweight and installs dependencies only as required by its configuration. In terms of connections to these dependencies, {{agents}} need to be able to connect to the {{artifact-registry}} directly, but {{package-registry}} connections are handled through [{{kib}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-kibana).

Additionally, if the {{agent}} {{elastic-defend}} integration is used, then access to the [Elastic Endpoint Artifact Repository](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-endpoint-artifact-repository) is necessary in order to deploy updates for some of the detection and prevention capabilities.

To learn more about install and configuration, refer to the [{{agent}} install documentation](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/install-elastic-agents.md). Make sure to check the requirements specific to running {{agents}} in an [air-gapped environment](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/air-gapped.md).

To get a better understanding of how to work with {{agent}} configuration settings and policies, refer to [Appendix D - Agent Integration Guide](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-agent-integration-guide).


#### 1.6. {{fleet-server}} [air-gapped-fleet]

{{fleet-server}} is a required middleware component for any scalable deployment of the {{agent}}. The air-gapped dependencies of {{fleet-server}} are the same as those of the [{{agent}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-agent).

To learn more about installing {{fleet-server}}, refer to the [{{fleet-server}} set up documentation](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/fleet-server.md).


#### 1.7. Elastic APM [air-gapped-elastic-apm]

Air-gapped setup of the APM server is possible in two ways:

* By setting up one of the {{agent}} deployments with an APM integration, as described in [Switch a self-installation to the APM integration](/solutions/observability/apps/switch-self-installation-to-apm-integration.md).
* Or, by installing a standalone Elastic APM Server, as described in the [APM configuration documentation](/solutions/observability/apps/configure-apm-server.md).


#### 1.8. {{ems}} [air-gapped-elastic-maps-service]

Refer to [Connect to {{ems}}](../../../explore-analyze/visualize/maps/maps-connect-to-ems.md) in the {{kib}} documentation to learn how to configure your firewall to connect to {{ems}}, host it locally, or disable it completely.


#### 1.9. {{package-registry}} [air-gapped-elastic-package-registry]

Air-gapped install of the EPR is possible using any OCI-compatible runtime like Podman (a typical choice for RHEL-like Linux systems) or Docker. Links to the official container image and usage guide is available on the [Air-gapped environments](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/air-gapped.md) page in the {{fleet}} and {{agent}} Guide.

Refer to [Appendix A - {{package-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-package-registry-example) for additional setup examples.

::::{note}
Besides setting up the EPR service, you also need to [configure {{kib}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-kibana) to use this service. If using TLS with the EPR service, it is also necessary to set up {{kib}} to trust the certificate presented by the EPR.
::::



#### 1.10. {{artifact-registry}} [air-gapped-elastic-artifact-registry]

Air-gapped install of the {{artifact-registry}} is necessary in order to enable {{agent}} deployments to perform self-upgrades and install certain components which are needed for some of the data integrations (that is, in addition to what is also retrieved from the EPR). To learn more, refer to [Host your own artifact registry for binary downloads](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/air-gapped.md#host-artifact-registry) in the {{fleet}} and {{elastic-agent}} Guide.

Refer to [Appendix B - {{artifact-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry-example) for additional setup examples.

::::{note}
When setting up own web server, such as NGINX, to function as the {{artifact-registry}}, it is recommended not to use TLS as there are, currently, no direct ways to establish certificate trust between {{agents}} and this service.
::::



#### 1.11. Elastic Endpoint Artifact Repository [air-gapped-elastic-endpoint-artifact-repository]

Air-gapped setup of this component is, essentially, identical to the setup of the [{{artifact-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry) except that different artifacts are served. To learn more, refer to [Configure offline endpoints and air-gapped environments](../../../solutions/security/configure-elastic-defend/configure-offline-endpoints-air-gapped-environments.md) in the Elastic Security guide.


#### 1.12 {{ml-cap}} [air-gapped-machine-learning]

Some {{ml}} features, like natural language processing (NLP), require you to deploy trained models. To learn about deploying {{ml}} models in an air-gapped environment, refer to:

* [Deploy ELSER in an air-gapped environment](../../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md#air-gapped-install).
* [Install trained models in an air-gapped environment with Eland](asciidocalypse://docs/eland/docs/reference/machine-learning.md#ml-nlp-pytorch-air-gapped).


#### 1.13 {{kib}} Product documentation for AI Assistants [air-gapped-kibana-product-documentation]

Detailed install and configuration instructions are available in the [{{kib}} AI Assistants settings documentation](asciidocalypse://docs/kibana/docs/reference/configuration-reference/ai-assistant-settings.md).


### 2. Kubernetes & OpenShift Install [air-gapped-kubernetes-and-openshift]

Setting up air-gapped Kubernetes or OpenShift installs of the {{stack}} has some unique concerns, but the general dependencies are the same as in the self-managed install case on a regular Linux machine.


#### 2.1. Elastic Kubernetes Operator (ECK) [air-gapped-k8s-os-elastic-kubernetes-operator]

The Elastic Kubernetes operator is an additional component in the Kubernetes OpenShift install that, essentially, does a lot of the work in installing, configuring, and updating deployments of the {{stack}}. For details, refer to the [{{eck}} install instructions](../../../deploy-manage/deploy/cloud-on-k8s/air-gapped-install.md).

The main requirements are:

* Syncing container images for ECK and all other {{stack}} components over to a locally-accessible container repository.
* Modifying the ECK helm chart configuration so that ECK is aware that it is supposed to use your offline container repository instead of the public Elastic repository.
* Optionally, disabling ECK telemetry collection in the ECK helm chart. This configuration propagates to all other Elastic components, such as {{kib}}.
* Building your custom deployment container image for the {{artifact-registry}}.
* Building your custom deployment container image for the Elastic Endpoint Artifact Repository.


#### 2.2. Elastic Package Registry [air-gapped-k8s-os-elastic-package-registry]

The container image can be downloaded from the official Elastic Docker repository, as described in the {{fleet}} and {{elastic-agent}} [air-gapped environments](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/air-gapped.md) documentation.

This container would, ideally, run as a Kubernetes deployment. Refer to [Appendix C - EPR Kubernetes Deployment](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-epr-kubernetes-example) for examples.


#### 2.3. {{artifact-registry}} [air-gapped-k8s-os-elastic-artifact-registry]

A custom container would need to be created following similar instructions to setting up a web server in the [self-managed install case](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry). For example, a container file using an NGINX base image could be used to run a build similar to the example described in [Appendix B - {{artifact-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry-example).


#### 2.4. Elastic Endpoint Artifact Repository [air-gapped-k8s-os-elastic-endpoint-artifact-repository]

Just like the {{artifact-registry}}. A custom container needs to be created following similar instructions to setting up a web server for the [self-managed install case](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry).


#### 2.5. Ironbank Secure Images for Elastic [air-gapped-k8s-os-ironbank-secure-images]

Besides the public [Elastic container repository](https://www.docker.elastic.co), most {{stack}} container images are also available in Platform One’s [Iron Bank](https://ironbank.dso.mil/repomap?vendorFilters=Elastic&page=1&sort=1).


#### 3.0 {{ece}} [air-gapped-ece]

To install {{ece}} in an air-gapped environment you’ll need to host your own [1.10. {{package-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-package-registry). Refer to the [ECE offline install instructions](/deploy-manage/deploy/cloud-enterprise/air-gapped-install.md) for details.


### Appendix A - {{package-registry}} [air-gapped-elastic-package-registry-example]

The following script generates a SystemD service file on a RHEL 8 system in order to run EPR with Podman in a production environment.

```shell
#!/usr/bin/env bash

EPR_BIND_ADDRESS="0.0.0.0"
EPR_BIND_PORT="8443"
EPR_TLS_CERT="/etc/elastic/epr/epr.pem"
EPR_TLS_KEY="/etc/elastic/epr/epr-key.pem"
EPR_IMAGE="docker.elastic.co/package-registry/distribution:9.0.0-beta1"

podman create \
  --name "elastic-epr" \
  -p "$EPR_BIND_ADDRESS:$EPR_BIND_PORT:$EPR_BIND_PORT" \
  -v "$EPR_TLS_CERT:/etc/ssl/epr.crt:ro" \
  -v "$EPR_TLS_KEY:/etc/ssl/epr.key:ro" \
  -e "EPR_ADDRESS=0.0.0.0:$EPR_BIND_PORT" \
  -e "EPR_TLS_CERT=/etc/ssl/epr.crt" \
  -e "EPR_TLS_KEY=/etc/ssl/epr.key" \
  "$EPR_IMAGE"

## creates service file in the root directory
# podman generate systemd --new --files --name elastic-epr --restart-policy always
```

The following is an example of an actual SystemD service file for an EPR, launched as a Podman service.

```shell
# container-elastic-epr.service
# autogenerated by Podman 4.1.1
# Wed Oct 19 13:12:33 UTC 2022

[Unit]
Description=Podman container-elastic-epr.service
Documentation=man:podman-generate-systemd(1)
Wants=network-online.target
After=network-online.target
RequiresMountsFor=%t/containers

[Service]
Environment=PODMAN_SYSTEMD_UNIT=%n
Restart=always
TimeoutStopSec=70
ExecStartPre=/bin/rm -f %t/%n.ctr-id
ExecStart=/usr/bin/podman run \
	--cidfile=%t/%n.ctr-id \
	--cgroups=no-conmon \
	--rm \
	--sdnotify=conmon \
	-d \
	--replace \
	--name elastic-epr \
	-p 0.0.0.0:8443:8443 \
	-v /etc/elastic/epr/epr.pem:/etc/ssl/epr.crt:ro \
	-v /etc/elastic/epr/epr-key.pem:/etc/ssl/epr.key:ro \
	-e EPR_ADDRESS=0.0.0.0:8443 \
	-e EPR_TLS_CERT=/etc/ssl/epr.crt \
	-e EPR_TLS_KEY=/etc/ssl/epr.key docker.elastic.co/package-registry/distribution:9.0.0-beta1
ExecStop=/usr/bin/podman stop --ignore --cidfile=%t/%n.ctr-id
ExecStopPost=/usr/bin/podman rm -f --ignore --cidfile=%t/%n.ctr-id
Type=notify
NotifyAccess=all

[Install]
WantedBy=default.target
```


### Appendix B - {{artifact-registry}} [air-gapped-elastic-artifact-registry-example]

The following example script downloads artifacts from the internet to be later served as a private Elastic Package Registry.

```shell
#!/usr/bin/env bash
set -o nounset -o errexit -o pipefail

STACK_VERSION=9.0.0-beta1
ARTIFACT_DOWNLOADS_BASE_URL=https://artifacts.elastic.co/downloads

DOWNLOAD_BASE_DIR=${DOWNLOAD_BASE_DIR:?"Make sure to set DOWNLOAD_BASE_DIR when running this script"}

COMMON_PACKAGE_PREFIXES="apm-server/apm-server beats/auditbeat/auditbeat beats/elastic-agent/elastic-agent beats/filebeat/filebeat beats/heartbeat/heartbeat beats/metricbeat/metricbeat beats/osquerybeat/osquerybeat beats/packetbeat/packetbeat cloudbeat/cloudbeat endpoint-dev/endpoint-security fleet-server/fleet-server"

WIN_ONLY_PACKAGE_PREFIXES="beats/winlogbeat/winlogbeat"

RPM_PACKAGES="beats/elastic-agent/elastic-agent"
DEB_PACKAGES="beats/elastic-agent/elastic-agent"

function download_packages() {
  local url_suffix="$1"
  local package_prefixes="$2"

  local _url_suffixes="$url_suffix ${url_suffix}.sha512 ${url_suffix}.asc"
  local _pkg_dir=""
  local _dl_url=""

  for _download_prefix in $package_prefixes; do
    for _pkg_url_suffix in $_url_suffixes; do
          _pkg_dir=$(dirname ${DOWNLOAD_BASE_DIR}/${_download_prefix})
          _dl_url="${ARTIFACT_DOWNLOADS_BASE_URL}/${_download_prefix}-${_pkg_url_suffix}"
          (mkdir -p $_pkg_dir && cd $_pkg_dir && curl -O "$_dl_url")
    done
  done
}

# and we download
for _os in linux windows; do
  case "$_os" in
    linux)
      PKG_URL_SUFFIX="${STACK_VERSION}-${_os}-x86_64.tar.gz"
      ;;
    windows)
      PKG_URL_SUFFIX="${STACK_VERSION}-${_os}-x86_64.zip"
      ;;
    *)
      echo "[ERROR] Something happened"
      exit 1
      ;;
  esac

  download_packages "$PKG_URL_SUFFIX" "$COMMON_PACKAGE_PREFIXES"

  if [[ "$_os" = "windows" ]]; then
    download_packages "$PKG_URL_SUFFIX" "$WIN_ONLY_PACKAGE_PREFIXES"
  fi

  if [[ "$_os" = "linux" ]]; then
    download_packages "${STACK_VERSION}-x86_64.rpm" "$RPM_PACKAGES"
    download_packages "${STACK_VERSION}-amd64.deb" "$DEB_PACKAGES"
  fi
done


## selinux tweaks
# semanage fcontext -a -t "httpd_sys_content_t" '/opt/elastic-packages(/.*)?'
# restorecon -Rv /opt/elastic-packages
```

The following is an example NGINX configuration for running a web server for the {{artifact-registry}}.

```shell
user  nginx;
worker_processes  2;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log          /var/log/nginx/access.log  main;
    sendfile            on;
    keepalive_timeout   65;

    server {
        listen                  9080 default_server;
        server_name             _;
        root                    /opt/elastic-packages;

        location / {

        }
    }

}
```


### Appendix C - EPR Kubernetes Deployment [air-gapped-epr-kubernetes-example]

The following is a sample EPR Kubernetes deployment YAML file.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: elastic-package-registry
  namespace: default
  labels:
    app: elastic-package-registry
spec:
  replicas: 1
  selector:
    matchLabels:
      app: elastic-package-registry
  template:
    metadata:
      name: elastic-package-registry
      labels:
        app: elastic-package-registry
    spec:
      containers:
        - name: epr
          image: docker.elastic.co/package-registry/distribution:9.0.0-beta1
          ports:
            - containerPort: 8080
              name: http
          livenessProbe:
            tcpSocket:
              port: 8080
            initialDelaySeconds: 20
            periodSeconds: 30
          resources:
            requests:
              cpu: 125m
              memory: 128Mi
            limits:
              cpu: 1000m
              memory: 512Mi
          env:
            - name: EPR_ADDRESS
              value: "0.0.0.0:8080"
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: elastic-package-registry
  name: elastic-package-registry
spec:
  ports:
  - port: 80
    name: http
    protocol: TCP
    targetPort: http
  selector:
    app: elastic-package-registry
```


### Appendix D - Agent Integration Guide [air-gapped-agent-integration-guide]

When configuring any integration in {{agent}}, you need to set up integration settings within whatever policy is ultimately assigned to that agent.


#### D.1. Terminology [air-gapped-agent-integration-terminology]

Note the following terms and definitions:

Integration
:   A variety of optional capabilities that can be deployed on top of the {{stack}}. Refer to [Integrations](https://www.elastic.co/integrations/) to learn more.

Agent integration
:   The integrations that require {{agent}} to run. For example, the Sample Data integration requires only {{es}} and {{kib}} and consists of dashboards, data, and related objects, but the APM integration not only has some {{es}} objects, but also needs {{agent}} to run the APM Server.

Package
:   A set of dependencies (such as dashboards, scripts, and others) for a given  integration that, typically, needs to be retrieved from the [Elastic Package Registry](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-package-registry) before an integration can be correctly installed and configured.

Agent policy
:   A configuration for the {{agent}} that may include one or more {{agent}} integrations, and configurations for each of those integrations.


#### D.2. How to configure [air-gapped-agent-integration-configure]

There are three ways to configure {{agent}} integrations:

* [D.2.1. Using the {{kib}} UI](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-agent-integration-configure-kibana)
* [D.2.2. Using the `kibana.yml` config file](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-agent-integration-configure-yml)
* [D.2.3. Using the {{kib}} {{fleet}} API](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-agent-integration-configure-fleet-api)


#### D.2.1. Using the {{kib}} UI [air-gapped-agent-integration-configure-kibana]

**Best option for:** Manual configuration and users who prefer using a UI over scripting.

**Example:** [Get started with logs and metrics](../../../solutions/observability/infra-and-hosts/get-started-with-system-metrics.md)

Agent policies and integration settings can be managed using the {{kib}} UI. For example, the following shows the configuration of logging for the System integration in an {{agent}} policy:

:::{image} ../../../images/elastic-stack-air-gapped-configure-logging.png
:alt: Configuration of a logging integration in an agent policy
:class: screenshot
:::


#### D.2.2. Using the `kibana.yml` config file [air-gapped-agent-integration-configure-yml]

**Good option for:** Declarative configuration and users who need reproducible and automated deployments.

**Example:** [Fleet settings in {{kib}}](asciidocalypse://docs/kibana/docs/reference/configuration-reference/fleet-settings.md)

::::{note}
This documentation is still under development; there may be gaps around building custom agent policies.
::::


You can have {{kib}} create {{agent}} policies on your behalf by adding appropriate configuration parameters in the `kibana.yml` settings file, these include:

`xpack.fleet.packages`
:   Takes a list of all integration package names and versions that {{kib}} should download from the {{package-registry}} (EPR). This is done because {{agents}} themselves do not directly fetch packages from the EPR.

`xpack.fleet.agentPolicies`
:   Takes a list of {{agent}} policies in the format expected by the [{{kib}} {{fleet}} HTTP API](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/fleet-api-docs.md). Refer to the setting in [Preconfiguration settings](asciidocalypse://docs/kibana/docs/reference/configuration-reference/fleet-settings.md#_preconfiguration_settings_for_advanced_use_cases) for the format. See also [D.2.3. Using the {{kib}} {{fleet}} API](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-agent-integration-configure-fleet-api).

`xpack.fleet.registryUrl`
:   Takes a URL of the {{package-registry}} that can be reached by the {{kib}} server. Enable this setting only when deploying in an air-gapped environment.

Other settings
:   You can add other, more discretionary settings for {{fleet}}, {{agents}}, & policies. Refer to [Fleet settings in {{kib}}](asciidocalypse://docs/kibana/docs/reference/configuration-reference/fleet-settings.md).


#### D.2.3. Using the {{kib}} {{fleet}} API [air-gapped-agent-integration-configure-fleet-api]

**Best option for**: Declarative configuration and users who need reproducible and automated deployments in even the trickiest of environments.

**Example:** See the following.

It is possible to use custom scripts that call the {{kib}} {{fleet}} API to create or update policies without restarting {{kib}}, and also allowing for custom error handling and update logic.

At this time, you can refer to the the [{{kib}} {{fleet}} HTTP API](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/fleet-api-docs.md) documentation, however additional resources from public code repositories should be consulted to capture the full set of configuration options available for a given integration. Specifically, many integrations have configuration options such as `inputs` and `data_streams` that are unique.

In particular, the `*.yml.hbs` templates should be consulted to determine which `vars` are available for configuring a particular integration using the {{kib}} {{fleet}} API.

* For most Integrations, refer to the README and `*.yml.hbs` files in the appropriate directory in the [elastic/integrations repository](https://github.com/elastic/integrations/tree/main/packages).
* For the APM integration, refer to the README and `*.yml.hbs` files in the [elastic/apm-server repository](https://github.com/elastic/apm-server/tree/main/apmpackage/apm/agent).

