---
applies_to:
  deployment:
    ece: ga
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-allow-x509-sha1.html
---

# Allow x509 Certificates Signed with SHA-1 [ece-allow-x509-sha1]

{{ece}} 3.5.0 and later defaults to rejecting x509 certificates signed with the SHA-1 hash function. This does not apply to self-signed root certificates. Practical attacks against SHA-1 have been demonstrated since 2017 and publicly trusted Certificate Authorities have not issues SHA-1 certificates since 2015.

You can temporarily bring back the legacy behavior by running the following script. Note that this requires a proxy restart, and support for x509 SHA-1 certificates will be entirely removed in a future release.

1. On a host that holds the director role:

    ```sh
    docker run \
    -v ~/.found-shell:/elastic_cloud_apps/shell/.found-shell \
    --env SHELL_ZK_AUTH=$(docker exec -it frc-directors-director bash -c 'echo -n $FOUND_ZK_READWRITE') $(docker inspect -f '{{ range .HostConfig.ExtraHosts }} --add-host {{.}} {{ end }}' frc-directors-director)  \
    --env FOUND_SCRIPT=allowX509Sha1Certs.sc \
    --rm -it \
    $(docker inspect -f '{{ .Config.Image }}' frc-directors-director) \
    /elastic_cloud_apps/shell/run-shell.sh
    ```

2. On all the proxy hosts:

    ```sh
    docker rm -f frc-proxies-proxyv2
    ```


To reset back to the default behavior of rejected x509 certificates signed with the SHA-1 hash function, you can run the following code.

1. On a host that holds the director role:

    ```sh
    docker run \
    -v ~/.found-shell:/elastic_cloud_apps/shell/.found-shell \
    --env SHELL_ZK_AUTH=$(docker exec -it frc-directors-director bash -c 'echo -n $FOUND_ZK_READWRITE') $(docker inspect -f '{{ range .HostConfig.ExtraHosts }} --add-host {{.}} {{ end }}' frc-directors-director)  \
    --env FOUND_SCRIPT=rejectX509Sha1Certs.sc \
    --rm -it \
    $(docker inspect -f '{{ .Config.Image }}' frc-directors-director) \
    /elastic_cloud_apps/shell/run-shell.sh
    ```

2. On all the proxy hosts:

    ```sh
    docker rm -f frc-proxies-proxyv2
    ```


