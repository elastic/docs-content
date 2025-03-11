---
applies_to:
  deployment:
    ece: ga
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-tls-version.html
---

# Configure the TLS version [ece-configure-tls-version]

Elastic Cloud Enterprise 2.4.0 and later defaults to minimum TLS version 1.2 with a modern set of cipher suites.

|     |     |     |
| --- | --- | --- |
| **Elastic Cloud Enterprise version** | **Default minimum TLS version** | **Default allowed cipher suites** |
| 2.4.0 and later | TLS 1.2 | `ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256` |
| 2.3.1 and earlier | TLS 1.0 | `CDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:ECDHE-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA` |

You can bring back the legacy behavior by running the following script. Note that this requires a proxy restart.

1. On a host that holds the director role:

    ```sh
    docker run \
    -v ~/.found-shell:/elastic_cloud_apps/shell/.found-shell \
    --env SHELL_ZK_AUTH=$(docker exec -it frc-directors-director bash -c 'echo -n $FOUND_ZK_READWRITE') $(docker inspect -f '{{ range .HostConfig.ExtraHosts }} --add-host {{.}} {{ end }}' frc-directors-director)  \
    --env FOUND_SCRIPT=setIntermediateTls.sc \
    --rm -it \
    $(docker inspect -f '{{ .Config.Image }}' frc-directors-director) \
    /elastic_cloud_apps/shell/run-shell.sh
    ```

2. On all of the proxy hosts:

    ```sh
    docker rm -f frc-proxies-proxyv2
    ```


To reset back to the default behavior of using TLSv1.2 and a modern cipher suite, you can run the following code.

1. On a host that holds the director role:

    ```sh
    docker run \
    -v ~/.found-shell:/elastic_cloud_apps/shell/.found-shell \
    --env SHELL_ZK_AUTH=$(docker exec -it frc-directors-director bash -c 'echo -n $FOUND_ZK_READWRITE') $(docker inspect -f '{{ range .HostConfig.ExtraHosts }} --add-host {{.}} {{ end }}' frc-directors-director)  \
    --env FOUND_SCRIPT=resetToDefaultTls.sc \
    --rm -it \
    $(docker inspect -f '{{ .Config.Image }}' frc-directors-director) \
    /elastic_cloud_apps/shell/run-shell.sh
    ```

2. On all of the proxy hosts:

    ```sh
    docker rm -f frc-proxies-proxyv2
    ```


