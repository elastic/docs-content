---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Connectivity Check
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Run the AutoOps Connectivity Check

The AutoOps Connectivity Check is a diagnostic tool designed to validate the communication paths between your on-premises environment and {{ecloud}} as well as the Agent and your {{es}} cluster. Before deploying the {{agent}}, or when troubleshooting missing metrics, this tool provides immediate feedback on your network, proxy, and authentication configurations. The check uses simple HTTP requests.

## Why use this tool?

Setting up cross-network observability by shipping {{es}} cluster metrics to {{ecloud}} involves navigating complex firewall rules, proxy configurations, and TLS requirements. This tool is offered to help you:

*   **Prevent common issues**: Confirm that your environment meets all network prerequisites before you run the agent installation command.
*   **Rapid troubleshooting**: If metrics are not appearing in your {{ecloud}} account, this script pinpoints exactly where the "data pipe" is broken—be it a firewall block, a missing proxy setting, or an authentication error.
*   **Verify security paths**: Ensure that your SSL/TLS certificates and API keys are correctly recognized by the system, avoiding "silent failures" where the agent runs but cannot communicate securely.

:::{note}
This script does not install or configure AutoOps. It only tests whether the required network and configuration are in place.
:::

It runs four checks in order:

1.  **Proxy configuration**: Detects whether proxy environment variables are set (informational only).
2.  **{{ecloud}} Connected Mode API**: Sends a request to the Cloud API. Any response means the endpoint is reachable so the agent can register.
3.  **OTel endpoint**: Sends a request to the OTel metrics endpoint. Any response means the agent can send metrics to {{ecloud}}.
4.  **{{es}} (optional)**: If you set `AUTOOPS_ES_URL`, the script calls your cluster root and the `/_license` endpoint to verify connectivity, {{es}} version (7.17.0 or higher), and that the license is active.

At the end it prints a summary (passed / failed / skipped / warnings). If any required check fails, the script tells you the agent will not function and points you to the troubleshooting guide.

## How to run the AutoOps Connectivity Check

Follow these steps to verify your environment is ready for the {{agent}}. These commands should be run from a terminal on the same host where you intend to install the agent.

### 1. Set your environment variables

The script uses environment variables to understand how to connect to your specific local {{es}} cluster and your {{ecloud}} account. Note that some variables are set by default and others are optional.

```bash
export ELASTIC_CLOUD_CONNECTED_MODE_API_URL="https://api.elastic-cloud.com"
export AUTOOPS_OTEL_URL="https://otel-auto-ops.ap-northeast-1.aws.svc.elastic.cloud"
export AUTOOPS_ES_URL="https://your-elasticsearch-host:9200"  
export AUTOOPS_ES_USERNAME="your_username" # Optional
export AUTOOPS_ES_PASSWORD="your_password" # Optional
export AUTOOPS_ES_API_KEY="your_api_key_here" # Optional
# export AUTOOPS_ES_CA="/path/to/your/ca.crt" # Optional. Uncomment if needed
# export HTTP_PROXY="http://proxy.example.com:8080" # Optional. Uncomment if needed
# export HTTPS_PROXY="http://proxy.example.com:8080" # Optional. Uncomment if needed
# export NO_PROXY="localhost,127.0.0.1" # Optional. Uncomment if needed
```

#### Variables - Required vs Optional

| Variable | Required / Optional | Description | Default or example |
|---|---|---|---|
| `ELASTIC_CLOUD_CONNECTED_MODE_API_URL` | Required | Base URL for the {{ecloud}} Connected Mode API. | Default: `https://api.elastic-cloud.com` |
| `AUTOOPS_OTEL_URL` | Required | Base URL for the OTel endpoint where the agent sends metrics as selected in the installation wizard (under storage location) | Example: `https://otel-auto-ops.ap-northeast-1.aws.svc.elastic.cloud` |
| `AUTOOPS_ES_URL` | Optional | Your {{es}} cluster URL. Set this to run the {{es}} check. | `https://my-cluster.example.com:9200` |
| `AUTOOPS_ES_USERNAME` | Optional | Username for HTTP Basic auth. Use with `AUTOOPS_ES_PASSWORD`. | Add your username (when not using API Key) |
| `AUTOOPS_ES_PASSWORD` | Optional | Password for HTTP Basic auth. Use with `AUTOOPS_ES_USERNAME`. | Add your password (when not using API Key) |
| `AUTOOPS_ES_API_KEY` | Optional | API key for auth. Use instead of username/password if you prefer. | Add your API key (when not using username/password) |
| `AUTOOPS_ES_CA` | Optional | Path to a CA certificate file if your cluster uses a custom or corporate CA. | `/path/to/ca.crt` |
| `HTTP_PROXY` / `http_proxy` | Optional | HTTP proxy URL. Script only detects; set if your environment uses a proxy. | — |
| `HTTPS_PROXY` / `https_proxy` | Optional | HTTPS proxy URL. Recommended when using HTTPS endpoints. | — |
| `NO_PROXY` / `no_proxy` | Optional | Hosts that should bypass the proxy (comma-separated). | — |

### 2. Download and run the script

Use cURL to download the latest version of the connectivity script directly from the Elastic repository and execute it:

```bash
curl -fsSL https://raw.githubusercontent.com/elastic/autoops-install/main/tools/check_connectivity.sh -o check_connectivity.sh && chmod u+x check_connectivity.sh && ./check_connectivity.sh
```

### 3. Review the results

*   **If the script ends with "Result: All checks passed"**: You are ready to install the agent! Copy the agent installation command from AutoOps installation wizard and run the command.
*   **If the script ends with "Result: FAIL"**: Review the specific error messages in the output. Common fixes include updating firewall rules for Port 443 or verifying that your `AUTOOPS_ES_URL` is reachable from this host.

#### Connectivity message reference table

The script runs through three main stages: Proxy Check, {{ecloud}} Connection, and {{es}} Cluster Check. Below is a breakdown of what the results mean and how to fix errors.

| Message Type | Description | Recommendation |
|---|---|---|
| SUCCESS | The connection to {{ecloud}} or {{es}} worked perfectly. | No action needed. You are ready for the next installation step. |
| FAIL: 'curl' required | The script cannot run because the curl tool is missing. | Install curl using your system’s package manager (e.g., `sudo apt install curl`). |
| FAIL: DNS resolution | Your computer cannot find the address for {{ecloud}}. | Check your internet connection or verify DNS settings with your IT team. |
| FAIL: Connection timeout | A firewall is likely blocking the request on Port 443. | Ask your network team to open Port 443 for outbound traffic to {{ecloud}}. |
| FAIL: SSL handshake | The secure connection was blocked, often by "SSL Inspection." | Request that your IT department allowlist the Elastic URLs to bypass inspection. |
| FAIL: 401 Unauthorized | The username, password, or API key provided is incorrect. | Double-check your credentials for typos and re-run the script. |
| FAIL: 403 Forbidden | Your account connects but lacks the required permissions. | Update the user role in Kibana to include monitor privileges. |
| FAIL: Version too low | Your {{es}} version is older than 7.17.0. | Upgrade your {{es}} cluster to version 7.17.0 or newer. |
| FAIL: License inactive | Your {{es}} license has expired or is invalid. | Renew your license or contact your Elastic Administrator. |
| WARNING: Proxy found | A proxy is set but might be blocking the specific connection. | If the connection fails, verify with IT that the proxy allows HTTPS traffic. |
| SKIPPED | The {{es}} check was skipped because no URL was set. | Set `AUTOOPS_ES_URL` if you want to test your local cluster connection. |

### Important security information

If you see **SSL certificate verification failed**, it means your system doesn't recognize the security certificate of the server. If using a private/company CA, you must point the script to your certificate file using the variable:

```bash
export AUTOOPS_ES_CA=/path/to/your/cert.pem
```

## Final Summary

*   **Passed**: The environment is ready to use AutoOps.
*   **Failed**: You must resolve the specific "FAIL" items in the table above before the agent will function.
*   **Warnings**: These provide helpful context but may not stop the agent from working.

## Troubleshooting

Running the Agent installation is not officially supported. Users who wish to install {{es}} cluster on their local machine and connect {{agent}}, may be getting an error message when trying to set the parameters: `zsh: command not found: #`.

An error may appear for the lines that start with `#`. If you want to be able to paste code blocks that contain comments without errors, you need to tell your Mac to allow "interactive comments." Run this command in your terminal before setting the variables:

```bash
setopt interactive_comments
```
