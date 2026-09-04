---
navigation_title: Air-gapped environments
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/air-gapped.html
applies_to:
  deployment:
    ece: ga
    self: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Run {{agents}} in an air-gapped environment [air-gapped]

When running {{agent}}s in a restricted or closed network, you need to take extra steps to make sure:

* {{kib}} is able to reach the {{package-registry}} to download package metadata and content.
* {{agent}}s are able to download binaries during upgrades from the {{artifact-registry}}.

The {{package-registry}} must therefore be accessible from {{kib}} through an HTTP Proxy or self-hosted.

The {{artifact-registry}} must therefore be accessible from {{kib}} through an HTTP Proxy or self-hosted.

::::{tip}
See the {{elastic-sec}} Solution documentation for air-gapped [offline endpoints](/solutions/security/configure-elastic-defend/configure-offline-endpoints-air-gapped-environments.md).

::::

When upgrading all the components in an air-gapped environment, it is recommended that you upgrade in the following order:

1. Upgrade the {{package-registry}}.
2. Upgrade the {{stack}} including {{kib}}.
3. Upgrade the {{artifact-registry}} and ensure the latest {{agent}} binaries are available.
4. Upgrade the on-premise {{fleet-server}}.
5. In {{fleet}}, issue an upgrade for all the {{agent}}s.


## Enable air-gapped mode for {{fleet}} [air-gapped-mode-flag]

Set the following property in {{kib}} to enable air-gapped mode in {{fleet}}. This allows {{fleet}} to intelligently skip certain requests or operations that shouldn’t be attempted in air-gapped environments.

```yaml
xpack.fleet.isAirGapped: true
```


## Configure {{agents}} to download a PGP/GPG key from {{fleet-server}} [air-gapped-pgp-fleet]

Starting from version 8.9.0, when {{agent}} tries to perform an upgrade, it first verifies the binary signature with the key bundled in the agent. This process has a backup mechanism that will use the key coming from `https://artifacts.elastic.co/GPG-KEY-elastic-agent` instead of the one it already has.

In an air-gapped environment, an {{agent}} which doesn’t have access to a PGP/GPG key from `https://artifacts.elastic.co/GPG-KEY-elastic-agent` would fail to be upgraded. For versions 8.9.0 to 8.10.3, you can resolve this problem following the steps described in the associated [known issue](https://www.elastic.co/guide/en/fleet/8.9/release-notes-8.9.0.html#known-issues-8.9.0) documentation.

Starting in version 8.10.4, you can resolve this problem by configuring {{agents}} to download the PGP/GPG key from {{fleet-server}}.

Starting in version 8.10.4, {{agent}} will:

1. Verify the binary signature with the key bundled in the agent.
2. If the verification doesn’t pass, the agent will download the PGP/GPG key from `https://artifacts.elastic.co/GPG-KEY-elastic-agent` and verify it.
3. If that verification doesn’t pass, the agent will download the PGP/GPG key from {{fleet-server}} and verify it.
4. If that verification doesn’t pass, the upgrade is blocked.

By default, {{fleet-server}} serves {{agents}} with the key located in `FLEETSERVER_BINARY_DIR/elastic-agent-upgrade-keys/default.pgp`. The key is served through the {{fleet-server}} endpoint `GET /api/agents/upgrades/{{major}}.{minor}.{{patch}}/pgp-public-key`.

If there isn’t a `default.pgp` key in the `FLEETSERVER_BINARY_DIR/elastic-agent-upgrade-keys/default.pgp` directory, {{fleet-server}} instead will attempt to retrieve a PGP/GPG key from the URL that you can specify with the `server.pgp.upstream_url` setting.

You can prevent {{fleet}} from downloading the PGP/GPG key from `server.pgp.upstream_url` by manually downloading it from `https://artifacts.elastic.co/GPG-KEY-elastic-agent` and storing it at  `FLEETSERVER_BINARY_DIR/elastic-agent-upgrade-keys/default.pgp`.

To set a custom URL for {{fleet-server}} to access a PGP/GPG key and make it available to {{agents}}:

1. In {{kib}}, go to **Management > {{fleet}} > Agent policies**.
2. Select a policy for the agents that you want to upgrade.
3. On the policy page, in the **Actions** menu for the {{fleet-server}} integration, select **Edit integration**.
4. In the {{fleet-server}} settings section expand **Change defaults** and **Advanced options**.
5. In the **Custom fleet-server configurations** field, add the setting `server.pgp.upstream_url` with the full URL where the PGP/GPG key can be accessed. For example:

```yaml
server.pgp.upstream_url: <http://my-web-server:8080/default.pgp>
```

The setting `server.pgp.upstream_url` must point to a web server hosting the PGP/GPG key, which must be reachable by the host where {{fleet-server}} is installed.

Note that:

* `server.pgp.upstream_url` may be specified as an `http` endpoint (instead of `https`).
* For an `https` endpoint, the CA for {{fleet-server}} to connect to `server.pgp.upstream_url` must be trusted by {{fleet-server}} using the `--certificate-authorities` setting that is used globally for {{agent}}.


## Use a proxy server to access the {{package-registry}} [air-gapped-proxy-server]

By default {{kib}} downloads package metadata and content from the public {{package-registry}} at [epr.elastic.co](https://epr.elastic.co/).

If you can route traffic to the public endpoint of the {{package-registry}} through a network gateway, set the following property in {{kib}} to use a proxy server:

```yaml
xpack.fleet.registryProxyUrl: your-nat-gateway.corp.net
```

For more information, refer to [Using a proxy server with {{agent}} and {{fleet}}](/reference/fleet/fleet-agent-proxy-support.md).


### Allow network access to the public {{package-registry}} [air-gapped-network-access-epr]

If you need to configure firewall rules to allow network access to [epr.elastic.co](https://epr.elastic.co/), allowlist the domain rather than specific IP addresses whenever possible, as IP addresses might change without notice.

If allowlisting the domain is not an option, these are the current IP addresses used for the {{package-registry}}:

* **IPv4**: `34.120.127.130`
* **IPv6**: `2600:1901:0:1d7::`

You can verify the current IP addresses using DNS lookup tools like `nslookup` or `dig`.


## Host your own {{package-registry}} [air-gapped-diy-epr]

::::{note}
The {{package-registry}} packages include signatures used in [package verification](/reference/fleet/package-signatures.md). By default, {{fleet}} uses the Elastic public GPG key to verify package signatures. If you ever need to change this GPG key, use the `xpack.fleet.packageVerification.gpgKeyPath` setting in [`kibana.yml`](/deploy-manage/stack-settings.md). For more information, refer to [{{fleet}} settings](kibana://reference/configuration-reference/fleet-settings.md).
::::

If routing traffic through a proxy server is not an option, you can host your own {{package-registry}}.

If using {{eck}}, you can follow the instructions in [Deploy {{package-registry}} on {{eck}}](/deploy-manage/deploy/cloud-on-k8s/package-registry.md).

The {{package-registry}} can be deployed and hosted onsite using one of the available Docker images. These docker images include the {{package-registry}} and a selection of packages.

There are different distributions available:

* {{version.stack}} (recommended): *docker.elastic.co/package-registry/distribution:{{version.stack}}* - Selection of packages from the production repository released with {{stack}} {{version.stack}}.
* lite-{{version.stack}}: *docker.elastic.co/package-registry/distribution:lite-{{version.stack}}* - Subset of the most commonly used packages from the production repository released with {{stack}} {{version.stack}}. This image is a good candidate to start using {{fleet}} in air-gapped environments.
* production: *docker.elastic.co/package-registry/distribution:production* - Packages available in the production registry ([https://epr.elastic.co](https://epr.elastic.co)). This image is updated every time a new version of a package gets published.
* lite: *docker.elastic.co/package-registry/distribution:lite* - Subset of the most commonly used packages available in the production registry ([https://epr.elastic.co](https://epr.elastic.co)). This image is updated every time a new version of a package gets published.


To update the distribution image, re-pull the image and then restart the docker container.

Every distribution contains packages that can be used by different versions of the {{stack}}. The {{package-registry}} API exposes a {{kib}} version constraint that allows for filtering packages that are compatible with a particular version.

::::{note}
These steps use the standard Docker CLI, but you can create a Kubernetes manifest based on this information. These images can also be used with other container runtimes compatible with Docker images.
::::


1. Pull the Docker image from the public Docker registry:

    ```sh subs=true
    docker pull docker.elastic.co/package-registry/distribution:{{version.stack}}
    ```

2. Save the Docker image locally:

    ```sh subs=true
    docker save -o package-registry-{{version.stack}}.tar docker.elastic.co/package-registry/distribution:{{version.stack}}
    ```

    ::::{tip}
    Check the image size to ensure that you have enough disk space.
    ::::

3. Transfer the image to the air-gapped environment and load it:

    ```sh subs=true
    docker load -i package-registry-{{version.stack}}.tar
    ```

4. Run the {{package-registry}}:

    ```sh subs=true
    docker run -it -p 8080:8080 docker.elastic.co/package-registry/distribution:{{version.stack}}
    ```

5. (Optional) You can monitor the health of your {{package-registry}} with requests to the root path:

    ```sh subs=true
    docker run -it -p 8080:8080 \
        --health-cmd "curl -f -L http://127.0.0.1:8080/health" \
        docker.elastic.co/package-registry/distribution:{{version.stack}}
    ```

    You can use the `/health` or `/health?ready=true` API endpoints to check if EPR is ready to serve requests.
    When either endpoint returns a `200` HTTP status code, the service is ready to handle requests.


### Connect {{kib}} to your hosted {{package-registry}} [air-gapped-diy-epr-kibana]

Use the `xpack.fleet.registryUrl` property in the {{kib}} config to set the URL of your hosted package registry. For example:

```yaml
xpack.fleet.registryUrl: "http://package-registry.corp.net:8080"
```


### TLS configuration of the {{package-registry}} [air-gapped-tls]

You can configure the {{package-registry}} to listen on a secure HTTPS port using TLS.

For example, given a key and a certificate pair available in `/etc/ssl`, you can start the {{package-registry}} listening on the 443 port using the following command:

```sh subs=true
docker run -it -p 443:443 \
  -v /etc/ssl/package-registry.key:/etc/ssl/package-registry.key:ro \
  -v /etc/ssl/package-registry.crt:/etc/ssl/package-registry.crt:ro \
  -e EPR_ADDRESS=0.0.0.0:443 \
  -e EPR_TLS_KEY=/etc/ssl/package-registry.key \
  -e EPR_TLS_CERT=/etc/ssl/package-registry.crt \
  docker.elastic.co/package-registry/distribution:{{version.stack}}
```

The {{package-registry}} supports TLS versions from 1.0 to 1.3. The minimum version accepted can be configured with `EPR_TLS_MIN_VERSION`, it defaults to 1.0. If you want to restrict the supported versions from 1.2 to 1.3, you can use `EPR_TLS_MIN_VERSION=1.2`.


### Using custom CA certificates [_using_custom_ca_certificates]

If you are using self-signed certificates or certificates issued by a custom Certificate Authority (CA), you need to set the file path to your CA in the `NODE_EXTRA_CA_CERTS` environment variable in the {{kib}} startup files.

```text
NODE_EXTRA_CA_CERTS="/etc/kibana/certs/ca-cert.pem"
```


## Host your own artifact registry for binary downloads [host-artifact-registry]

{{agent}}s must be able to access the {{artifact-registry}} to download binaries during upgrades. By default {{agent}}s download artifacts from `https://artifacts.elastic.co/downloads/`. Refer to the available [script and Nginx config](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry).

To make binaries available in an air-gapped environment, you can host your own custom artifact registry, and then configure {{agent}}s to download binaries from it.

1. Create a custom artifact registry in a location accessible to your {{agent}}s:

    1. Download the latest release artifacts from the public {{artifact-registry}} at `https://artifacts.elastic.co/downloads/`. The required artifacts depend on which integrations you’re using and which operating systems your {{agent}}s run on. Make sure to also download the corresponding `.sha512` and PGP signature (`.asc`) files for each binary, as these are used for file integrity validation during installation and upgrade.

        To generate the full set of `curl` commands for all supported architectures and package types, save the following script and run it with your stack version as the argument:

        ```shell
        #!/bin/sh

        VERSION="${1:-9.0.0}"

        ARCHITECTURES="linux-x86_64 linux-arm64 windows-x86_64 darwin-x86_64 darwin-aarch64"

        COMPONENTS="apm-server apm-server
        auditbeat beats/auditbeat
        elastic-agent beats/elastic-agent
        filebeat beats/filebeat
        heartbeat beats/heartbeat
        metricbeat beats/metricbeat
        osquerybeat beats/osquerybeat
        packetbeat beats/packetbeat
        cloudbeat cloudbeat
        endpoint-security endpoint-dev
        fleet-server fleet-server
        pf-host-agent prodfiler
        pf-elastic-collector prodfiler
        pf-elastic-symbolizer prodfiler"

        WINDOWS_EXCLUSIONS="apm-server osquerybeat fleet-server pf-host-agent pf-elastic-collector pf-elastic-symbolizer cloudbeat endpoint-security"
        DEB_EXCLUSIONS="fleet-server endpoint-security osquerybeat cloudbeat"
        RPM_EXCLUSIONS="fleet-server endpoint-security osquerybeat cloudbeat"
        DARWIN_EXCLUSIONS="pf-host-agent pf-elastic-symbolizer pf-elastic-collector cloudbeat apm-server"

        for ARCH in $ARCHITECTURES; do
          echo "# Architecture: $ARCH"

          echo "$COMPONENTS" | while read COMPONENT PATH; do
            SKIP=no
            case "$ARCH" in
              windows-*)
                for EXCL in $WINDOWS_EXCLUSIONS; do
                  [ "$COMPONENT" = "$EXCL" ] && SKIP=yes && break
                done
                ;;
              darwin-*)
                for EXCL in $DARWIN_EXCLUSIONS; do
                  [ "$COMPONENT" = "$EXCL" ] && SKIP=yes && break
                done
                ;;
            esac
            [ "$SKIP" = "yes" ] && continue

            BASE_URL="https://artifacts.elastic.co/downloads/${PATH}"

            case "$ARCH" in
              windows-*)
                FILE="${COMPONENT}-${VERSION}-${ARCH}.msi"
                echo "curl -O ${BASE_URL}/${FILE}"
                echo "curl -O ${BASE_URL}/${FILE}.sha512"
                echo "curl -O ${BASE_URL}/${FILE}.asc"
                ;;
              darwin-*)
                FILE="${COMPONENT}-${VERSION}-${ARCH}.tar.gz"
                echo "curl -O ${BASE_URL}/${FILE}"
                echo "curl -O ${BASE_URL}/${FILE}.sha512"
                echo "curl -O ${BASE_URL}/${FILE}.asc"
                ;;
              linux-*)
                FILE_TAR="${COMPONENT}-${VERSION}-${ARCH}.tar.gz"
                echo "curl -O ${BASE_URL}/${FILE_TAR}"
                echo "curl -O ${BASE_URL}/${FILE_TAR}.sha512"
                echo "curl -O ${BASE_URL}/${FILE_TAR}.asc"

                SKIP_DEB=no
                for EXCL in $DEB_EXCLUSIONS; do
                  [ "$COMPONENT" = "$EXCL" ] && SKIP_DEB=yes && break
                done
                [ "$SKIP_DEB" != "yes" ] && {
                  case "$ARCH" in
                    linux-x86_64) DEB_ARCH="amd64" ;;
                    linux-arm64)  DEB_ARCH="arm64" ;;
                  esac
                  FILE_DEB="${COMPONENT}-${VERSION}-${DEB_ARCH}.deb"
                  echo "curl -O ${BASE_URL}/${FILE_DEB}"
                  echo "curl -O ${BASE_URL}/${FILE_DEB}.sha512"
                  echo "curl -O ${BASE_URL}/${FILE_DEB}.asc"
                }

                SKIP_RPM=no
                for EXCL in $RPM_EXCLUSIONS; do
                  [ "$COMPONENT" = "$EXCL" ] && SKIP_RPM=yes && break
                done
                [ "$SKIP_RPM" != "yes" ] && {
                  case "$ARCH" in
                    linux-x86_64) RPM_ARCH="x86_64" ;;
                    linux-arm64)  RPM_ARCH="aarch64" ;;
                  esac
                  FILE_RPM="${COMPONENT}-${VERSION}-${RPM_ARCH}.rpm"
                  echo "curl -O ${BASE_URL}/${FILE_RPM}"
                  echo "curl -O ${BASE_URL}/${FILE_RPM}.sha512"
                  echo "curl -O ${BASE_URL}/${FILE_RPM}.asc"
                }
                ;;
            esac
          done

          echo
        done
        ```

    2. On your HTTP file server, group the artifacts into directories and sub-directories that follow the same convention used by the {{artifact-registry}}:

        ```shell
        <source_uri>/<artifact_type>/<artifact_name>-<version>-<arch>-<package_type>
        ```

        Where:

        * `<artifact_type>` is in the format `beats/elastic-agent`, `fleet-server`, `endpoint-dev`, and so on.
        * `<artifict_name>` is in the format `elastic-agent`, `endpoint-security`, or `fleet-server` and so on.
        * `arch-package-type` is in the format `linux-x86_64`, `linux-arm64`, `windows_x86_64`, `darwin_x86_64`, or darwin_aarch64`.
        * If you’re using the DEB package manager:

            * The 64bit variant has the format `<artifact_name>-<version>-amd64.deb`.
            * The aarch64 variant has the format `<artifact_name>-<version>-arm64.deb`.

        * If you’re using the RPM package manager:

            * The 64bit  variant has a format  `<artifact_name>-<version>-x86_64.rpm`.
            * The aarch64 variant has a format  `<artifact_name>-<version>-aarch64.rpm`.


    ::::{tip}
    * If you’re ever in doubt, visit the [{{agent}} download page](https://www.elastic.co/downloads/elastic-agent) to see what URL the various binaries are downloaded from.
    * Make sure you have a plan or automation in place to update your artifact registry when new versions of {{agent}} are available.

    ::::

2. Add the agent binary download location to {{fleet}} settings:

    1. Open **{{fleet}} → Settings**.
    2. Under **Agent Binary Download**, click **Add agent binary source** to add the location of your artifact registry. For more details, refer to [Agent binary download settings](/reference/fleet/fleet-settings.md#fleet-agent-binary-download-settings). If you want all {{agents}} to download binaries from this location, set it as the default.

        :::{note}
        :applies_to: stack: ga 9.4+

        To authenticate requests to your artifact registry, expand the **Authentication** section, and provide either a username and password, or an API key. Optionally, you can also add custom HTTP headers. For more details, refer to [Configure authentication for binary downloads](/reference/fleet/fleet-settings.md#agent-binary-auth).
        :::

3. If your artifact registry is not the default, edit your agent policies to override the default:

    1. Go to **{{fleet}} → Agent policies** and click the policy name to edit it.
    2. Click **Settings**.
    3. Under **Agent Binary Download**, select your artifact registry.

        When you trigger an upgrade for any {{agent}}s enrolled in the policy, the binaries are downloaded from your artifact registry instead of the public repository.


**Not using {{fleet}}?** For standalone {{agent}}s, you can set the binary download location under `agent.download.sourceURI` in the [`elastic-agent.yml`](/reference/fleet/elastic-agent-reference-yaml.md) file, or run the [`elastic-agent upgrade`](/reference/fleet/agent-command-reference.md#elastic-agent-upgrade-command) command with the `--source-uri` flag specified.
