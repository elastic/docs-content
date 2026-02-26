---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Run the Connectivity Check
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Run the AutoOps Connectivity Check

The AutoOps Connectivity Check is a diagnostic tool that validates the communication paths between {{agent}}, your {{es}} cluster, and {{ecloud}}. Run it when going through the installation wizard to get immediate feedback on your network, proxy, and authentication configuration using HTTP requests.

Shipping metrics from your cluster to {{ecloud}} involves navigating complex firewall rules, proxy configurations, and TLS requirements. The AutoOps Connectivity Check helps you:

*   **Prevent common issues**: Confirms that your environment meets all network prerequisites before you run the agent installation command.
*   **Troubleshoot issues**: If metrics are not appearing in your {{ecloud}} account, this tool determines the cause.
*   **Verify security paths**: Checks that your SSL/TLS certificates and API keys are correct, avoiding situations where the agent runs but cannot communicate securely.

:::{important}
The AutoOps Connectivity Check does not install or configure AutoOps in your cluster. It is only a diagnostic tool that runs tests to make sure your system has all the required configuration.
:::

## How the AutoOps Connectivity Check works
The tool runs four checks in order:

1.  **Proxy configuration**: Detects whether proxy environment variables are set.
2.  **{{ecloud}} Connected Mode API**: Sends a request to the Cloud API. Any response means the endpoint is reachable so the agent can register your cluster with {{ecloud}}.
3.  **OTel endpoint**: Sends a request to the OTel metrics endpoint. Any response means the agent can send metrics to {{ecloud}}.
4.  **{{es}} (optional)**: If you set `AUTOOPS_ES_URL`, the tool calls your cluster root and the `/_license` endpoint to verify connectivity, appropriate {{es}} version, and that the license is active.

After running the checks, it prints a summary of its findings. If any required check fails, the tool tells you why and points you to the [troubleshooting guide](../autoops/cc-cloud-connect-autoops-troubleshooting.md).

## Run the AutoOps Connectivity Check

Follow these steps to run the tool and verify your environment is ready. 

:::{note}
Run the following commands from the machine where you are installing the agent.
:::

:::::{stepper}

::::{step} Set your environment variables
The tool uses environment variables to understand how to connect to your {{es}} cluster and your {{ecloud}} account. Some variables are set by default. 

Update the placeholder values in the following command and run it.

```bash
export ELASTIC_CLOUD_CONNECTED_MODE_API_URL="https://api.elastic-cloud.com"
export AUTOOPS_OTEL_URL="https://otel-auto-ops.${region}.${csp}.svc.elastic.cloud/"
export AUTOOPS_ES_URL="https://your-elasticsearch-host:9200"  
export AUTOOPS_ES_USERNAME="your_username"  ## Optional
export AUTOOPS_ES_PASSWORD="your_password"  ## Optional
export AUTOOPS_ES_API_KEY="your_api_key_here"  ## Optional
# export AUTOOPS_ES_CA="/path/to/your/ca.crt"  ## Optional. Uncomment if needed
# export HTTP_PROXY="http://proxy.example.com:8080"  ## Optional. Uncomment if needed
# export HTTPS_PROXY="http://proxy.example.com:8080"  ## Optional. Uncomment if needed
# export NO_PROXY="localhost,127.0.0.1"  ## Optional. Uncomment if needed
```
:::{tip}
You might get the following error message for lines that start with `#`:
```bash
zsh: command not found: #
```
To enable running codeblocks that contain comments, tell your computer to allow "interactive comments" with the following command:
```bash
setopt interactive_comments
```
After running this command, try setting your environment variables again.
:::

The following table describes the variables.

| Variable | Required or Optional | Description |
|---|---|---|
| `ELASTIC_CLOUD_CONNECTED_MODE_API_URL` | Required | Base URL for the {{ecloud}} Connected Mode API. This is set to `https://api.elastic-cloud.com` by default. |
| `AUTOOPS_OTEL_URL` | Required | Base URL for the OTel endpoint where the agent sends metrics. You selected this as your [storage location](../autoops/cc-connect-self-managed-to-autoops.md#storage-location) in the wizard. |
| `AUTOOPS_ES_URL` | Required | Your {{es}} cluster URL. Set this if you want to run the {{es}} check. |
| `AUTOOPS_ES_USERNAME` | Optional | Username for HTTP Basic authentication. Use with `AUTOOPS_ES_PASSWORD`. |
| `AUTOOPS_ES_PASSWORD` | Optional | Password for HTTP Basic authentication. Use with `AUTOOPS_ES_USERNAME`. |
| `AUTOOPS_ES_API_KEY` | Optional | API key for authentication. Can be used instead of `AUTOOPS_ES_PASSWORD` and `AUTOOPS_ES_USERNAME`. |
| `AUTOOPS_ES_CA` | Optional | Path to a Certificate Authority (CA) file if your cluster uses a custom or internal CA. |
| `HTTP_PROXY` / `http_proxy` | Optional | HTTP proxy URL. Set if your environment uses a proxy. |
| `HTTPS_PROXY` / `https_proxy` | Optional | HTTPS proxy URL. Recommended when using HTTPS endpoints. |
| `NO_PROXY` / `no_proxy` | Optional | Hosts that should bypass the proxy (comma-separated). |
::::

::::{step} Download and run the tool
Use curl to download the latest version of the AutoOps Connectivity Check directly from the Elastic repository and run it:

```bash
curl -fsSL https://raw.githubusercontent.com/elastic/autoops-install/main/tools/check_connectivity.sh -o check_connectivity.sh && chmod u+x check_connectivity.sh && ./check_connectivity.sh
```
::::

::::{step} View the results

After the tool has finished running all the checks, it presents one of the following messages to indicate the results. Refer to the **Action** column for next steps.

| Message type | Description | Action |
|---|---|---|
| SUCCESS | The connection to {{ecloud}} or {{es}} worked perfectly. | No action needed. Continue the steps in the installation wizard. |
| FAIL: 'curl' required | The script cannot run because the curl tool is missing. | Install curl using your system’s package manager (`sudo apt install curl`). |
| FAIL: DNS resolution | Your computer cannot find the address for {{ecloud}}. | Check your internet connection or verify DNS settings. |
| FAIL: Connection timeout | A firewall is likely blocking the request on port 443. | Open port 443 for outbound traffic to {{ecloud}}. |
| FAIL: SSL handshake | The secure connection was blocked, often by "SSL Inspection." | Allowlist the Elastic URLs to bypass inspection. |
| FAIL: 401 Unauthorized | The username, password, or API key provided is incorrect. | Double-check your credentials for typos and then re-run the tool. |
| FAIL: 403 Forbidden | Your account connects but lacks the required permissions. | Update the user role in {{kib}} to include monitor privileges. |
| FAIL: Version too low | Your {{es}} version is older than 7.17.0. | Upgrade your {{es}} cluster to version 7.17.0 or later. |
| FAIL: License inactive | Your {{es}} license has expired or is invalid. | Renew your license or contact your Elastic administrator. |
| WARNING: Proxy found | A proxy is set but might be blocking the specific connection. | If the connection fails, verify that the proxy allows HTTPS traffic. |
| SKIPPED | The {{es}} check was skipped because no URL was set. | Set `AUTOOPS_ES_URL` in Step 1 if you want to run the {{es}} check |
::::

:::{important}
If your result output shows **SSL certificate verification failed**, your system doesn't recognize the security certificate of the server. If you are using a custom or internal CA, you must point the tool to your certificate file using the following command:

```bash
export AUTOOPS_ES_CA=/path/to/your/cert.pem
```
:::

:::::
