---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-change-allocator-disconnect-timeout.html
---

# Change allocator disconnect timeout [ece-change-allocator-disconnect-timeout]

One of the responsibilities of the allocator is to monitor the health of the clusters running on it. It periodically healthcheck the instances and report their health to other components. The platform uses this information to route traffic to healthy instances and to avoid unhealthy ones. The healthstatus is stored in zookeeper.

By default, the platform will wait 10 minutes before considering a particular instance unhealthy.

While the 10 minutes timeout is long, this is based on the assumption that a short-lived zookeeper disconnect it more likely than a disconnected allocator, and that the allocator will reconnect shortly. In the meantime the workloads running on the allocator are healthy and can be accessed. This assumption may not hold for your use case, e.g., your allocators are frequently restarted.

The timeout can be changed by running the following script. Use the `TIMEOUT_MINUTES` to set a different timeout. At least 2 minutes is recommended, to avoid false positives in case of allocator container restarts.

::::{note} 
The new timeout will apply only to new instances that are added to the allocator. The existing instances will continue running on the old timeout until they are disconnected for longer that the old timeout, or migrated.
::::


To change the timeout value:

1. On a host that holds the director role:

    ```sh
    docker run \
    -v ~/.found-shell:/elastic_cloud_apps/shell/.found-shell \
    --env SHELL_ZK_AUTH=$(docker exec -it frc-directors-director bash -c 'echo -n $FOUND_ZK_READWRITE') $(docker inspect -f '{{ range .HostConfig.ExtraHosts }} --add-host {{.}} {{ end }}' frc-directors-director)  \
    --env FOUND_SCRIPT=setAllocatorTTL.sc \
    --env TIMEOUT_MINUTES=2 \
    --rm -it \
    $(docker inspect -f '{{ .Config.Image }}' frc-directors-director) \
    /elastic_cloud_apps/shell/run-shell.sh
    ```

2. On all the allocator hosts:

    ```sh
    docker rm -f frc-allocators-allocator
    ```


To reset back to the default.

1. On a host that holds the director role:

    ```sh
    docker run \
    -v ~/.found-shell:/elastic_cloud_apps/shell/.found-shell \
    --env SHELL_ZK_AUTH=$(docker exec -it frc-directors-director bash -c 'echo -n $FOUND_ZK_READWRITE') $(docker inspect -f '{{ range .HostConfig.ExtraHosts }} --add-host {{.}} {{ end }}' frc-directors-director)  \
    --env FOUND_SCRIPT=resetAllocatorTTL.sc \
    --rm -it \
    $(docker inspect -f '{{ .Config.Image }}' frc-directors-director) \
    /elastic_cloud_apps/shell/run-shell.sh
    ```

2. On all the allocator hosts:

    ```sh
    docker rm -f frc-allocators-allocator
    ```


