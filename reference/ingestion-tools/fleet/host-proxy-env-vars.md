---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/host-proxy-env-vars.html
---

# Proxy Server connectivity using default host variables [host-proxy-env-vars]

Set environment variables on the host to configure default proxy settings. The {{agent}} uses host environment settings by default if no proxy settings are specified elsewhere. You can override host proxy settings later when you configure the {{agent}} and {{fleet}} settings. The following environment variables are available on the host:

| Variable | Description |
| --- | --- |
| `HTTP_PROXY` | URL of the proxy server for HTTP traffic. |
| `HTTPS_PROXY` | URL of the proxy server for HTTPS traffic. |
| `NO_PROXY` | IP addresses or domain names that should not use the proxy. Supports patterns. |

The proxy URL can be a complete URL or `host[:port]`, in which case the `http` scheme is assumed. An error is returned if the value is a different form.


## Where to set proxy environment variables [where-to-set-proxy-env-vars]

The location where you set these environment variables is platform-specific and based on the system manager you’re using. Here are some examples to get you started. For more information about setting environment variables, refer to the documentation for your operating system.

* For Windows services, set environment variables for the service in the Windows registry.

    This PowerShell command sets the `HKLM\SYSTEM\CurrentControlSet\Services\Elastic Agent\Environment` registry key, then restarts {{agent}}:

    ```yaml
    $environment = [string[]]@(
      "HTTPS_PROXY=https://proxy-hostname:proxy-port",
      "HTTP_PROXY=http://proxy-hostname:proxy-port"
      )

    Set-ItemProperty "HKLM:SYSTEM\CurrentControlSet\Services\Elastic Agent" -Name Environment -Value $environment

    Restart-Service "Elastic Agent"
    ```

* For Linux services, the location depends on the distribution you’re using. For example, you can set environment variables in:

    * `/etc/systemd/system/elastic-agent.service` for systems that use `systemd` to manage the service. To edit the file, run:

        ```shell
        sudo systemctl edit --full elastic-agent.service
        ```

        Then add the environment variables under `[Service]`

        ```shell
        [Service]

        Environment="HTTPS_PROXY=https://my.proxy:8443"
        Environment="HTTP_PROXY=http://my.proxy:8080"
        ```

    * `/etc/sysconfig/elastic-agent` for Red Hat-like distributions that don’t use `systemd`.
    * `/etc/default/elastic-agent` for Debian and Ubuntu distributions that don’t use `systemd`.

        For example:

        ```shell
        HTTPS_PROXY=https://my.proxy:8443
        HTTP_PROXY=http://my.proxy:8080
        ```


After adding environment variables, restart the service.

::::{note}
If you use a proxy server to download new agent versions from `artifacts.elastic.co` for upgrading, configure [Agent binary download settings](/reference/ingestion-tools/fleet/fleet-settings.md#fleet-agent-binary-download-settings).
::::


