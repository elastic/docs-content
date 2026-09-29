If you need {{ece}} containers to make outbound connections over IPv6, enable dual-stack networking on the Docker default bridge **before** you install ECE.

1. Ensure IPv6 forwarding is enabled on the host. If you have not already set it with the other kernel parameters, add:

    ```text
    net.ipv6.conf.all.forwarding=1
    ```

    Then apply the setting:

    ```sh
    sudo sysctl -p
    ```

2. Merge the following keys into `/etc/docker/daemon.json`. Do not replace the existing file. Instead, keep your current settings, such as `default-ulimits`, `bip`, or `data-root`, and add these keys at the top level:

    ```json
    {
      "ipv6": true,
      "fixed-cidr-v6": "fd00:10:89::/64",
      "ip6tables": true
    }
    ```

    ::::{note}
    Choose a Unique Local Address (ULA) IPv6 subnet that does not overlap with other networks in your environment. The `fixed-cidr-v6` value is local to each host, so the same subnet can be reused across ECE hosts.
    ::::

3. Reload and restart Docker so the daemon picks up the changes:

    ```sh
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    ```

4. Verify that the default bridge has an IPv6 subnet:

    ```sh
    docker network inspect bridge --format '{{json .IPAM.Config}}'
    ```

    The output should include an IPv6 subnet such as `fd00:10:89::/64`.

5. Run a short-lived container and test IPv6 egress:

    ```sh
    docker run --rm curlimages/curl:latest \
        -6 -s -o /dev/null -w "%{http_code}\n" https://ipv6.google.com
    ```

    A response of `200` confirms that containers can reach IPv6 endpoints.
