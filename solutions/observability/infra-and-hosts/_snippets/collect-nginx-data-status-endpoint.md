The [`nginxreceiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/nginxreceiver) OTel Collector receiver needs an endpoint that exposes NGINX status metrics.

1. Make sure the [`ngx_http_stub_status_module`](https://nginx.org/en/docs/http/ngx_http_stub_status_module.html) module is enabled.
2. In your NGINX configuration file (for example, `/etc/nginx/nginx.conf`), add or modify the `location` block in the `server { ... }` block with the following:

    ```nginx
    location = /status {
      stub_status;
    }
    ```

3. Save the configuration and restart NGINX:

    ```bash
    sudo systemctl restart nginx
    ```

4. Verify that the endpoint is active:

    ```bash
    curl http://localhost:80/status <1>
    ```
    1. Use the port number specified in the `listen` directive in the NGINX configuration.

    If the endpoint returns data, you are ready to set up {{agent}}.

For more details, refer to [Configuring NGINX for Metric Collection](https://docs.nginx.com/nginx-amplify/nginx-amplify-agent/configuring-metric-collection/#metrics-from-stub_status).
