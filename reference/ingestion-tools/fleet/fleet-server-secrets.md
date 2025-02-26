---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-server-secrets.html
---

# Fleet Server Secrets [fleet-server-secrets]

{{fleet-server}} configuration can contain secret values. You may specify these values directly in the configuration or through secret files. You can use command line arguments to pass the values or file paths when you are running under {{agent}}, or you can use environment variables if {{agent}} is running in a container.

For examples of how to deploy secret files, refer to our [Secret files guide](/reference/ingestion-tools/fleet/secret-files-guide.md).

::::{note}
Stand-alone {{fleet-server}} is under active development.
::::



## Secret values [_secret_values]

The following secret values may be used when configuring {{fleet-server}}.

Note that the configuration fragments shown below are specified either in the UI as part of the output specification or as part of the {{fleet-server}} integration settings.

`service_token`
:   The `service_token` is used to communicate with {{es}}.

    It may be specified in the configuration directly as:

    ```yaml
    output.elasticsearch.service_token: my-service-token
    ```

    Or by a file with:

    ```yaml
    output.elasticsearch.service_token_path: /path/to/token-file
    ```

    When you are running {{fleet-server}} under {{agent}}, you can specify it with either the `--fleet-server-service-token` or the `--fleet-server-service-token-path` flag. See [{{agent}} command reference](/reference/ingestion-tools/fleet/agent-command-reference.md) for more details.

    If you are [running {{fleet-server}} under {{agent}} in a container](/reference/ingestion-tools/fleet/elastic-agent-container.md), you can use the environment variables `FLEET_SERVER_SERVICE_TOKEN` or `FLEET_SERVER_SERVICE_TOKEN_PATH`.


TLS private key
:   Use the TLS private key to encrypt communications between {{fleet-server}} and {{agent}}. See [Configure SSL/TLS for self-managed {{fleet-server}}s](/reference/ingestion-tools/fleet/secure-connections.md) for more details.

    Although it is not recommended, you may specify the private key directly in the configuration as:

    ```yaml
    inputs:
      - type: fleet-server
        ssl.key: |
          ----BEGIN CERTIFICATE----
          ....
          ----END CERTIFICATE----
    ```

    Alternatively, you can provide the path to the private key with the same attribute:

    ```yaml
    inputs:
      - type: fleet-server
        ssl.key: /path/to/cert.key
    ```

    When you are running {{fleet-server}} under {{agent}}, you can provide the private key path using with the `--fleet-server-cert-key` flag. See [{{agent}} command reference](/reference/ingestion-tools/fleet/agent-command-reference.md) for more details.

    If you are [running {{fleet-server}} under {{agent}} in a container](/reference/ingestion-tools/fleet/elastic-agent-container.md), you can use the environment variable `FLEET_SERVER_CERT_KEY` to specify the private key path.


TLS private key passphrase
:   The private key passphrase is used to decrypt an encrypted private key file.

    You can specify the passphrase as a secret file in the configuration with:

    ```yaml
    inputs:
      - type: fleet-server
        ssl.key_passphrase_path: /path/to/passphrase
    ```

    When you are running {{fleet-server}} under {{agent}}, you can provide the passphrase path using the `--fleet-server-cert-key-passphrase` flag. See [{{agent}} command reference](/reference/ingestion-tools/fleet/agent-command-reference.md) for more details.

    If you are [running {{fleet-server}} under {{agent}} in a container](/reference/ingestion-tools/fleet/elastic-agent-container.md), you can use the environment variable `FLEET_SERVER_CERT_KEY_PASSPHRASE` to specify the file path.


APM API Key
:   The APM API Key may be used to gather APM data from {{fleet-server}}.

    You can specify it directly in the instrumentation segment of the configuration:

    ```yaml
    inputs:
      - type: fleet-server
        instrumentation.api_key: my-apm-api-key
    ```

    Or by a file with:

    ```yaml
    inputs:
      - type: fleet-server
        instrumentation.api_key_file: /path/to/apmAPIKey
    ```

    You may specify the API key by value using the environment variable `ELASTIC_APM_API_KEY`.


APM secret token
:   The APM secret token may be used to gather APM data from {{fleet-server}}.

    You can specify the secret token directly in the instrumentation segment of the configuration:

    ```yaml
    inputs:
      - type: fleet-server
        instrumentation.secret_token: my-apm-secret-token
    ```

    Or by a file with:

    ```yaml
    inputs:
      - type: fleet-server
        instrumentation.secret_token_file: /path/to/apmSecretToken
    ```

    You may also specify the token by value using the environment variable `ELASTIC_APM_SECRET_TOKEN`.



