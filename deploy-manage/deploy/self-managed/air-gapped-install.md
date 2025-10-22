---
mapped_pages:
  - https://www.elastic.co/guide/en/elastic-stack/current/air-gapped-install.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-offline.html
applies_to:
  deployment:
    self:
products:
  - id: cloud-enterprise
---

# Air gapped install

Some components of the {{stack}} require additional configuration and local dependencies in order to deploy in environments without internet access. This guide gives an overview of this setup scenario and connects you to existing documentation for individual parts of the stack.

Refer to the section for each Elastic component for air-gapped installation configuration and dependencies in a self-managed Linux environment.

## {{es}} [air-gapped-elasticsearch]

Air-gapped install of {{es}} may require additional steps in order to access some of the features. General install and configuration guides are available in [](/deploy-manage/deploy/self-managed/installing-elasticsearch.md).

Specifically:

* To be able to use the GeoIP processor, refer to [the GeoIP processor documentation](elasticsearch://reference/enrich-processor/geoip-processor.md#manually-update-geoip-databases) for instructions on downloading and deploying the required databases.
* Refer to [{{ml-cap}}](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-machine-learning) for instructions on deploying the Elastic Learned Sparse EncodeR (ELSER) natural language processing (NLP) model and other trained {{ml}} models.


## {{kib}} [air-gapped-kibana]

Air-gapped install of {{kib}} may require a number of additional services in the local network in order to access some of the features. General install and configuration guides are available in the [{{kib}} install documentation](/deploy-manage/deploy/self-managed/install-kibana.md).

Specifically:

* To be able to use {{kib}} mapping visualizations, you need to set up and configure the [Elastic Maps Service](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-maps-service).
* To be able to use {{kib}} sample data, install or update hundreds of prebuilt alert rules, and explore available data integrations, you need to set up and configure the [{{package-registry}}](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-package-registry).
* To provide detection rule updates for {{endpoint-sec}} agents, you need to set up and configure the [Elastic Endpoint Artifact Repository](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-endpoint-artifact-repository).
* To access the APM integration, you need to set up and configure [Elastic APM](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-apm).
* To install and use the Elastic documentation for {{kib}} AI assistants, you need to set up and configure the [Elastic product documentation for {{kib}}](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-kibana-product-documentation).


## {{beats}} [air-gapped-beats]

Elastic {{beats}} are light-weight data shippers. They do not require any special configuration in air-gapped environments. To learn more, refer to the [{{beats}} documentation](beats://reference/index.md).


## {{ls}} [air-gapped-logstash]

{{ls}} is a versatile data shipping and processing application. It does not require any special configuration in air-gapped environments. To learn more, refer to the [{{ls}} documentation](logstash://reference/index.md).


## {{agent}} [air-gapped-elastic-agent]

Air-gapped install of {{agent}} depends on the [{{package-registry}}](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-package-registry) and the [{{artifact-registry}}](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry) for most use-cases. The agent itself is fairly lightweight and installs dependencies only as required by its configuration. In terms of connections to these dependencies, {{agents}} need to be able to connect to the {{artifact-registry}} directly, but {{package-registry}} connections are handled through [{{kib}}](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-kibana).

Additionally, if the {{agent}} {{elastic-defend}} integration is used, then access to the [Elastic Endpoint Artifact Repository](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-endpoint-artifact-repository) is necessary in order to deploy updates for some of the detection and prevention capabilities.

To learn more about install and configuration, refer to the [{{agent}} install documentation](/reference/fleet/install-elastic-agents.md). Make sure to check the requirements specific to running {{agents}} in an [air-gapped environment](/reference/fleet/air-gapped.md).


## {{fleet-server}} [air-gapped-fleet]

{{fleet-server}} is a required middleware component for any scalable deployment of the {{agent}}. The air-gapped dependencies of {{fleet-server}} are the same as those of the [{{agent}}](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-agent).

To learn more about installing {{fleet-server}}, refer to the [{{fleet-server}} set up documentation](/reference/fleet/fleet-server.md).


## Elastic APM [air-gapped-elastic-apm]

Air-gapped setup of the APM server is possible in two ways:

* By setting up one of the {{agent}} deployments with an APM integration, as described in [Switch a self-installation to the APM integration](/solutions/observability/apm/switch-self-installation-to-apm-integration.md). See [air gapped installation guidance for {{agent}}](#air-gapped-elastic-agent).
* Or, by installing a standalone Elastic APM Server, as described in the [APM configuration documentation](/solutions/observability/apm/apm-server/configure.md).


## {{ems}} [air-gapped-elastic-maps-service]

Refer to [Connect to {{ems}}](../../../explore-analyze/visualize/maps/maps-connect-to-ems.md) in the {{kib}} documentation to learn how to configure your firewall to connect to {{ems}}, host it locally, or disable it completely.


## {{package-registry}} [air-gapped-elastic-package-registry]

Air-gapped install of the EPR is possible using any OCI-compatible runtime like Podman (a typical choice for RHEL-like Linux systems) or Docker. Links to the official container image and usage guide is available on the [Air-gapped environments](/reference/fleet/air-gapped.md) page in the {{fleet}} and {{agent}} Guide.

::::{note}
Besides setting up the EPR service, you also need to [configure {{kib}}](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-kibana) to use this service. If using TLS with the EPR service, it is also necessary to set up {{kib}} to trust the certificate presented by the EPR.
::::

### Additional {{package-registry}} examples

:::::{dropdown} Script to generate a SystemD service file on a RHEL 8 system

The following script generates a SystemD service file on a RHEL 8 system in order to run EPR with Podman in a production environment.

::::{tab-set}

:::{tab-item} Latest
```sh subs=true
#!/usr/bin/env bash

EPR_BIND_ADDRESS="0.0.0.0"
EPR_BIND_PORT="8443"
EPR_TLS_CERT="/etc/elastic/epr/epr.pem"
EPR_TLS_KEY="/etc/elastic/epr/epr-key.pem"
EPR_IMAGE="docker.elastic.co/package-registry/distribution:{{version.stack}}"

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
:::

:::{tab-item} Specific version
Replace `<SPECIFIC.VERSION.NUMBER>` with the {{stack}} version number you want. For example, you can replace `<SPECIFIC.VERSION.NUMBER>` with {{version.stack.base}}.
```sh subs=true
#!/usr/bin/env bash

EPR_BIND_ADDRESS="0.0.0.0"
EPR_BIND_PORT="8443"
EPR_TLS_CERT="/etc/elastic/epr/epr.pem"
EPR_TLS_KEY="/etc/elastic/epr/epr-key.pem"
EPR_IMAGE="docker.elastic.co/package-registry/distribution:<SPECIFIC.VERSION.NUMBER>"

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
:::
::::

:::::

:::::{dropdown} SystemD service file launched as a Podman service

The following is an example of an actual SystemD service file for an EPR, launched as a Podman service.

::::{tab-set}

:::{tab-item} Latest
```ini subs=true
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
  -e EPR_TLS_KEY=/etc/ssl/epr.key docker.elastic.co/package-registry/distribution:{{version.stack}}
ExecStop=/usr/bin/podman stop --ignore --cidfile=%t/%n.ctr-id
ExecStopPost=/usr/bin/podman rm -f --ignore --cidfile=%t/%n.ctr-id
Type=notify
NotifyAccess=all

[Install]
WantedBy=default.target
```
:::

::::::{tab-item} Specific version
Replace `<SPECIFIC.VERSION.NUMBER>` with the {{stack}} version number you want. For example, you can replace `<SPECIFIC.VERSION.NUMBER>` with {{version.stack.base}}.
```ini subs=true
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
  -e EPR_TLS_KEY=/etc/ssl/epr.key docker.elastic.co/package-registry/distribution:<SPECIFIC.VERSION.NUMBER>
ExecStop=/usr/bin/podman stop --ignore --cidfile=%t/%n.ctr-id
ExecStopPost=/usr/bin/podman rm -f --ignore --cidfile=%t/%n.ctr-id
Type=notify
NotifyAccess=all

[Install]
WantedBy=default.target
```
:::
::::

:::::

## {{artifact-registry}} [air-gapped-elastic-artifact-registry]

Air-gapped install of the {{artifact-registry}} is necessary in order to enable {{agent}} deployments to perform self-upgrades and install certain components which are needed for some of the data integrations (that is, in addition to what is also retrieved from the EPR). To learn more, refer to [Host your own artifact registry for binary downloads](/reference/fleet/air-gapped.md#host-artifact-registry) in the {{fleet}} and {{elastic-agent}} Guide.

::::{note}
When setting up own web server, such as NGINX, to function as the {{artifact-registry}}, it is recommended not to use TLS as there are, currently, no direct ways to establish certificate trust between {{agents}} and this service.
::::

### Additional {{artifact-registry}} examples

:::::{dropdown} Artifact download script

The following example script downloads artifacts from the internet to be later served as a private Elastic Package Registry.

::::{tab-set}

:::{tab-item} Latest
```sh subs=true
#!/usr/bin/env bash
set -o nounset -o errexit -o pipefail

STACK_VERSION={{version.stack}}
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
:::

::::::{tab-item} Specific version
Replace `<SPECIFIC.VERSION.NUMBER>` with the {{stack}} version number you want. For example, you can replace `<SPECIFIC.VERSION.NUMBER>` with {{version.stack.base}}.
```sh subs=true
#!/usr/bin/env bash
set -o nounset -o errexit -o pipefail

STACK_VERSION=<SPECIFIC.VERSION.NUMBER>
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
:::
::::
:::::

:::{dropdown} NGINX config for private {{artifact-registry}} web server
The following is an example NGINX configuration for running a web server for the {{artifact-registry}}.

```sh
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
:::


## Elastic Endpoint Artifact Repository [air-gapped-elastic-endpoint-artifact-repository]

Air-gapped setup of this component is, essentially, identical to the setup of the [{{artifact-registry}}](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry) except that different artifacts are served. To learn more, refer to [Configure offline endpoints and air-gapped environments](../../../solutions/security/configure-elastic-defend/configure-offline-endpoints-air-gapped-environments.md) in the Elastic Security guide.


## {{ml-cap}} [air-gapped-machine-learning]

Some {{ml}} features, like natural language processing (NLP), require you to deploy trained models. To learn about deploying {{ml}} models in an air-gapped environment, refer to:

* [Deploy ELSER in an air-gapped environment](../../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md#air-gapped-install).
* [Install trained models in an air-gapped environment with Eland](eland://reference/machine-learning.md#ml-nlp-pytorch-air-gapped).


## {{kib}} Product documentation for AI Assistants [air-gapped-kibana-product-documentation]

Detailed install and configuration instructions are available in the [{{kib}} AI Assistants settings documentation](kibana://reference/configuration-reference/ai-assistant-settings.md).
