---
navigation_title: "Environment variables"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/agent-environment-variables.html
---

# {{agent}} environment variables [agent-environment-variables]


Use environment variables to configure {{agent}} when running in a containerized environment. Variables on this page are grouped by action type:

* [Common variables](#env-common-vars)
* [Configure {{kib}}:](#env-prepare-kibana-for-fleet) prepare the {{fleet}} plugin in {kib}
* [Configure {{fleet-server}}:](#env-bootstrap-fleet-server) bootstrap {{fleet-server}} on an {agent}
* [Configure {{agent}} and {{fleet}}:](#env-enroll-agent) enroll an {agent}


## Common variables [env-common-vars]

To limit the number of environment variables that need to be set, the following common variables are available. These variables can be used across all {{agent}} actions, but have a lower precedence than action-specific environment variables.

These common variables are useful, for example, when using the same {{es}} and {{kib}} credentials to prepare the {{fleet}} plugin in {{kib}}, configure {{fleet-server}}, and enroll an {{agent}}.

| Settings | Description |
| --- | --- |
| $$$env-common-elasticsearch-host$$$<br>`ELASTICSEARCH_HOST`<br> | (string) The {{es}} host to communicate with.<br><br>**Default:** `http://elasticsearch:9200`<br> |
| $$$env-common-elasticsearch-username$$$<br>`ELASTICSEARCH_USERNAME`<br> | (string) The basic authentication username used to connect to {{kib}} and retrieve a `service_token` for {{fleet}}.<br><br>**Default:** none<br> |
| $$$env-common-elasticsearch-password$$$<br>`ELASTICSEARCH_PASSWORD`<br> | (string) The basic authentication password used to connect to {{kib}} and retrieve a `service_token` for {{fleet}}.<br><br>**Default:** none<br> |
| $$$env-common-elasticsearch-api-key$$$<br>`ELASTICSEARCH_API_KEY`<br> | (string) API key used for authenticating to Elasticsearch.<br><br>**Default:** none<br> |
| $$$env-common-elasticsearch-ca$$$<br>`ELASTICSEARCH_CA`<br> | (string) The path to a certificate authority.<br><br>By default, {{agent}} uses the list of trusted certificate authorities (CA) from the operating system where it is running. If the certificate authority that signed your node certificates is not in the host system’s trusted certificate authorities list, use this config to add the path to the `.pem` file that contains your CA’s certificate.<br><br>**Default:** `""`<br> |
| $$$env-common-kibana-host$$$<br>`KIBANA_HOST`<br> | (string) The {{kib}} host.<br><br>**Default:** `http://kibana:5601`<br> |
| $$$env=common-kibana-username$$$<br>`KIBANA_USERNAME`<br> | (string) The basic authentication username used to connect to {{kib}} to retrieve a `service_token`.<br><br>**Default:** `elastic`<br> |
| $$$env=common-kibana-password$$$<br>`KIBANA_PASSWORD`<br> | (string) The basic authentication password used to connect to {{kib}} to retrieve a `service_token`.<br><br>**Default:** `changeme`<br> |
| $$$env-common-kibana-ca$$$<br>`KIBANA_CA`<br> | (string) The path to a certificate authority.<br><br>By default, {{agent}} uses the list of trusted certificate authorities (CA) from the operating system where it is running. If the certificate authority that signed your node certificates is not in the host system’s trusted certificate authorities list, use this config to add the path to the `.pem` file that contains your CA’s certificate.<br><br>**Default:** `""`<br> |
| $$$env-common-elastic-netinfo$$$<br>`ELASTIC_NETINFO`<br> | (bool) When `false`, disables `netinfo.enabled` parameter of `add_host_metadata` processor. Setting this to `false` is recommended for large scale setups where the host.ip and host.mac fields index size increases.<br><br>By default, {{agent}} initializes the `add_host_metadata` processor. The `netinfo.enabled` parameter defines ingestion of IP addresses and MAC addresses as fields `host.ip` and `host.mac`. For more information see [add_host_metadata](/reference/ingestion-tools/fleet/add_host_metadata-processor.md)<br><br>**Default:** `"false"`<br> |


## Prepare {{kib}} for {{fleet}} [env-prepare-kibana-for-fleet]

Settings used to prepare the {{fleet}} plugin in {{kib}}.

| Settings | Description |
| --- | --- |
| $$$env-fleet-kib-kibana-fleet-host$$$<br>`KIBANA_FLEET_HOST`<br> | (string) The {{kib}} host to enable {{fleet}} on. Overrides `FLEET_HOST` when set.<br><br>**Default:** `http://kibana:5601`<br> |
| $$$env-fleet-kib-kibana-fleet-username$$$<br>`KIBANA_FLEET_USERNAME`<br> | (string) The basic authentication username used to connect to {{kib}} and retrieve a `service_token` to enable {{fleet}}. Overrides `ELASTICSEARCH_USERNAME` when set.<br><br>**Default:** `elastic`<br> |
| $$$env-fleet-kib-kibana-fleet-password$$$<br>`KIBANA_FLEET_PASSWORD`<br> | (string) The basic authentication password used to connect to {{kib}} and retrieve a `service_token` to enable {{fleet}}. Overrides `ELASTICSEARCH_PASSWORD` when set.<br><br>**Default:** `changeme`<br> |
| $$$env-fleet-kib-kibana-fleet-ca$$$<br>`KIBANA_FLEET_CA`<br> | (string) The path to a certificate authority. Overrides `KIBANA_CA` when set.<br><br>By default, {{agent}} uses the list of trusted certificate authorities (CA) from the operating system where it is running. If the certificate authority that signed your node certificates is not in the host system’s trusted certificate authorities list, use this config to add the path to the `.pem` file that contains your CA’s certificate.<br><br>**Default:** `""`<br> |


## Bootstrap {{fleet-server}} [env-bootstrap-fleet-server]

Settings used to bootstrap {{fleet-server}} on this {{agent}}. At least one {{fleet-server}} is required in a deployment.

| Settings | Description |
| --- | --- |
| $$$env-bootstrap-fleet-fleet-server-enable$$$<br>`FLEET_SERVER_ENABLE`<br> | (int) Set to `1` to bootstrap {{fleet-server}} on this {{agent}}. When set to `1`, this automatically forces {{fleet}} enrollment as well.<br><br>**Default:** none<br> |
| $$$env-bootstrap-fleet-fleet-server-elasticsearch-host$$$<br>`FLEET_SERVER_ELASTICSEARCH_HOST`<br> | (string) The {{es}} host for {{fleet-server}} to communicate with. Overrides `ELASTICSEARCH_HOST` when set.<br><br>**Default:** `http://elasticsearch:9200`<br> |
| $$$env-bootstrap-fleet-fleet-server-elasticsearch-ca$$$<br>`FLEET_SERVER_ELASTICSEARCH_CA`<br> | (string) The path to a certificate authority. Overrides `ELASTICSEARCH_CA` when set.<br><br>By default, {{agent}} uses the list of trusted certificate authorities (CA) from the operating system where it is running. If the certificate authority that signed your node certificates is not in the host system’s trusted certificate authorities list, use this config to add the path to the `.pem` file that contains your CA’s certificate.<br><br>**Default:** `""`<br> |
| $$$env-bootstrap-fleet-fleet-server-es-cert$$$<br>`FLEET_SERVER_ES_CERT`<br> | (string) The path to the mutual TLS client certificate that {{fleet-server}} will use to connect to {{es}}.<br><br>**Default:** `""`<br> |
| $$$env-bootstrap-fleet-fleet-server-es-cert-key$$$<br>`FLEET_SERVER_ES_CERT_KEY`<br> | (string) The path to the mutual TLS private key that {{fleet-server}} will use to connect to {{es}}.<br><br>**Default:** `""`<br> |
| $$$env-bootstrap-fleet-fleet-server-insecure-http$$$<br>`FLEET_SERVER_INSECURE_HTTP`<br> | (bool) When `true`, {{fleet-server}} is exposed over insecure or unverified HTTP. Setting this to `true` is not recommended.<br><br>**Default:** `false`<br> |
| $$$env-bootstrap-fleet-fleet-server-service-token$$$<br>`FLEET_SERVER_SERVICE_TOKEN`<br> | (string) Service token to use for communication with {{es}} and {{kib}} if [`KIBANA_FLEET_SETUP`](#env-prepare-kibana-for-fleet) is enabled. If the service token value and service token path are specified the value may be used for setup and the path is passed to the agent in the container.<br><br>**Default:** none<br> |
| $$$env-bootstrap-fleet-fleet-server-service-token-path$$$<br>`FLEET_SERVER_SERVICE_TOKEN_PATH`<br> | (string) The path to the service token file to use for communication with {{es}} and {{kib}} if [`KIBANA_FLEET_SETUP`](#env-prepare-kibana-for-fleet) is enabled. If the service token value and service token path are specified the value may be used for setup and the path is passed to the agent in the container.<br><br>**Default:** none<br> |
| $$$env-bootstrap-fleet-fleet-server-policy-name$$$<br>`FLEET_SERVER_POLICY_NAME`<br> | (string) The name of the policy for {{fleet-server}} to use on itself. Overrides `FLEET_TOKEN_POLICY_NAME` when set.<br><br>**Default:** none<br> |
| $$$env-bootstrap-fleet-fleet-server-policy-id$$$<br>`FLEET_SERVER_POLICY_ID`<br> | (string) The policy ID for {{fleet-server}} to use on itself.<br> |
| $$$env-bootstrap-fleet-fleet-server-host$$$<br>`FLEET_SERVER_HOST`<br> | (string) The binding host for {{fleet-server}} HTTP. Overrides the host defined in the policy.<br><br>**Default:** none<br> |
| $$$env-bootstrap-fleet-fleet-server-port$$$<br>`FLEET_SERVER_PORT`<br> | (string) The binding port for {{fleet-server}} HTTP. Overrides the port defined in the policy.<br><br>**Default:** none<br> |
| $$$env-bootstrap-fleet-fleet-server-cert$$$<br>`FLEET_SERVER_CERT`<br> | (string) The path to the certificate to use for HTTPS.<br><br>**Default:** none<br> |
| $$$env-bootstrap-fleet-fleet-server-cert-key$$$<br>`FLEET_SERVER_CERT_KEY`<br> | (string) The path to the private key for the certificate used for HTTPS.<br><br>**Default:** none<br> |
| $$$env-bootstrap-fleet-fleet-server-cert-key-passphrase$$$<br>`FLEET_SERVER_CERT_KEY_PASSPHRASE`<br> | (string) The path to the private key passphrase for an encrypted private key file.<br><br>**Default:** none<br> |
| $$$env-bootstrap-fleet-fleet-server-client-auth$$$<br>`FLEET_SERVER_CLIENT_AUTH`<br> | (string) One of `none`, `optional`, or `required`. {{fleet-server}}'s client authentication option for client mTLS connections. If `optional` or `required` is specified, client certificates are verified using CAs.<br><br>**Default:** `none`<br> |
| $$$env-bootstrap-fleet-fleet-server-es-ca-trusted-fingerprint$$$<br>`FLEET_SERVER_ELASTICSEARCH_CA_TRUSTED_FINGERPRINT`<br> | (string) The SHA-256 fingerprint (hash) of the certificate authority used to self-sign {{es}} certificates. This fingerprint is used to verify self-signed certificates presented by {{fleet-server}} and any inputs started by {{agent}} for communication. This flag is required when using self-signed certificates with {{es}}.<br><br>**Default:** `""`<br> |
| $$$env-bootstrap-fleet-fleet-daemon-timeout$$$<br>`FLEET_DAEMON_TIMEOUT`<br> | (duration) Set to indicate how long {{fleet-server}} will wait during the bootstrap process for {{elastic-agent}}.<br> |
| $$$env-bootstrap-fleet-fleet-server-timeout$$$<br>`FLEET_SERVER_TIMEOUT`<br> | (duration) Set to indicate how long {{agent}} will wait for {{fleet-server}} to check in as healthy.<br> |


## Enroll {{agent}} [env-enroll-agent]

Settings used to enroll an {{agent}} into a {{fleet-server}}.

| Settings | Description |
| --- | --- |
| $$$env-enroll-elastic-agent-cert$$$<br>`ELASTIC_AGENT_CERT`<br> | (string) The path to the mutual TLS client certificate that {{agent}} will use to connect to {{fleet-server}}.<br> |
| $$$env-enroll-elastic-agent-cert-key$$$<br>`ELASTIC_AGENT_CERT_KEY`<br> | (string) The path to the mutual TLS private key that {{agent}} will use to connect to {{fleet-server}}.<br> |
| $$$env-enroll-elastic-agent-cert-key-passphrase$$$<br>`ELASTIC_AGENT_CERT_KEY_PASSPHRASE`<br> | (string) The path to the file that contains the passphrase for the mutual TLS private key that {{agent}} will use to connect to {{fleet-server}}. The file must only contain the characters of the passphrase, no newline or extra non-printing characters.<br><br>This option is only used if the `--elastic-agent-cert-key` is encrypted and requires a passphrase to use.<br> |
| $$$env-enroll-elastic-agent-tag$$$<br>`ELASTIC_AGENT_TAGS`<br> | (string) A comma-separated list of tags to apply to {{fleet}}-managed {{agent}}s. You can use these tags to filter the list of agents in {{fleet}}.<br> |
| $$$env-enroll-fleet-enroll$$$<br>`FLEET_ENROLL`<br> | (bool) Set to `1` to enroll the {{agent}} into {{fleet-server}}.<br><br>**Default:** `false`<br> |
| $$$env-enroll-fleet-force$$$<br>`FLEET_FORCE`<br> | (bool) Set to `true` to force overwrite of the current {{agent}} configuration without prompting for confirmation. This flag is helpful when using automation software or scripted deployments.<br><br>**Default:** `false`<br> |
| $$$env-enroll-fleet-url$$$<br>`FLEET_URL`<br> | (string) URL to enroll the {{fleet-server}} into.<br><br>**Default:** `""`<br> |
| $$$env-enroll-fleet-enrollment-token$$$<br>`FLEET_ENROLLMENT_TOKEN`<br> | (string) The token to use for enrollment.<br><br>**Default:** `""`<br> |
| $$$env-enroll-fleet-token-name$$$<br>`FLEET_TOKEN_NAME`<br> | (string) The token name to use to fetch the token from {{kib}}.<br><br>**Default:** `""`<br> |
| $$$env-enroll-fleet-token-policy-name$$$<br>`FLEET_TOKEN_POLICY_NAME`<br> | (string) The token policy name to use to fetch the token from {{kib}}.<br><br>**Default:** `false`<br> |
| $$$env-enroll-fleet-ca$$$<br>`FLEET_CA`<br> | (string) The path to a certificate authority. Overrides `ELASTICSEARCH_CA` when set.<br><br>By default, {{agent}} uses the list of trusted certificate authorities (CA) from the operating system where it is running. If the certificate authority that signed your node certificates is not in the host system’s trusted certificate authorities list, use this config to add the path to the `.pem` file that contains your CA’s certificate.<br><br>**Default:** `false`<br> |
| $$$env-enroll-fleet-insecure$$$<br>`FLEET_INSECURE`<br> | (bool) When `true`, {{agent}} communicates with {{fleet-server}} over insecure or unverified HTTP. Setting this to `true` is not recommended.<br><br>**Default:** `false`<br> |
| $$$env-enroll-kibana-fleet-host$$$<br>`KIBANA_FLEET_HOST`<br> | (string) The {{kib}} host to enable {{fleet}} on. Overrides `FLEET_HOST` when set.<br><br>**Default:** `http://kibana:5601`<br> |
| $$$env-enroll-kibana-fleet-username$$$<br>`KIBANA_FLEET_USERNAME`<br> | (string) The basic authentication username used to connect to {{kib}} and retrieve a `service_token` to enable {{fleet}}. Overrides `ELASTICSEARCH_USERNAME` when set.<br><br>**Default:** `elastic`<br> |
| $$$env-enroll-kibana-fleet-password$$$<br>`KIBANA_FLEET_PASSWORD`<br> | (string) The basic authentication password used to connect to {{kib}} and retrieve a `service_token` to enable {{fleet}}. Overrides `ELASTICSEARCH_PASSWORD` when set.<br><br>**Default:** `changeme`<br> |
| $$$env-enroll-kibana-fleet-ca$$$<br>`KIBANA_FLEET_CA`<br> | (string) The path to a certificate authority. Overrides `KIBANA_CA` when set.<br><br>By default, {{agent}} uses the list of trusted certificate authorities (CA) from the operating system where it is running. If the certificate authority that signed your node certificates is not in the host system’s trusted certificate authorities list, use this config to add the path to the `.pem` file that contains your CA’s certificate.<br><br>**Default:** `""`<br> |

