---
description: Reference for the agent.download settings in elastic-agent.yml that control where standalone Elastic Agent downloads and stores upgrade artifacts, including sources and authentication.
navigation_title: Agent download
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-standalone-download.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Configure download settings for standalone {{agent}} upgrades [elastic-agent-standalone-download]


The `agent.download` section of the elastic-agent.yml config file contains settings for where to download and store artifacts used for {{agent}} upgrades.

$$$elastic-agent-standalone-download-settings$$$

| Setting | Description |
| --- | --- |
| $$$agent.download.sources$$$<br>`sources` {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+`<br> | (list) Ordered list of locations of artifacts used during {{agent}} upgrade. If the download from one location fails, {{agent}} tries the next one. If you set both `sources` and `sourceURI`, only `sources` is used. The `auth`, TLS, and proxy settings of the `agent.download` section apply to all locations. Default: `https://artifacts.elastic.co/downloads/`.<br> |
| $$$agent.download.sourceURI$$$<br>`sourceURI` {applies_to}`serverless: deprecated` {applies_to}`stack: deprecated 9.6+`<br> | (string) Path to the location of artifacts used during {{agent}} upgrade. Starting with version 9.6, use `sources` instead.<br> |
| $$$agent.download.target_directory$$$<br>`target_directory`<br> | (string) Path to the directory where download artifacts are stored.<br> |
| $$$agent.download.timeout$$$<br>`timeout`<br> | (string) The HTTP request timeout in seconds for the download package attempt.<br> |
| $$$agent.download.install_path$$$<br>`install_path`<br> | (string) The location of installed packages and programs, as well as program specifications.<br> |
| $$$agent.download.retry_sleep_init_duration$$$<br>`retry_sleep_init_duration`<br> | (string) The duration in seconds to sleep for before the first retry attempt.<br> |
| $$$agent.download.reserve_diskspace.enabled$$$<br>`reserve_diskspace.enabled` {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+`<br> | (bool) If `true`, {{agent}} reserves disk space for the new agent package before an upgrade, so the upgrade fails early if there isn't enough space. Set to `false` to turn off the reservation. Default: `true`.<br> |
| $$$agent.download.auth.username$$$<br>`auth.username` {applies_to}`stack: ga 9.4+`<br> | (string) Username for HTTP Basic authentication to the artifact registry. Must be set together with `auth.password`, and is mutually exclusive with `auth.api_key`.<br> |
| $$$agent.download.auth.password$$$<br>`auth.password` {applies_to}`stack: ga 9.4+`<br> | (string) Password for HTTP Basic authentication to the artifact registry. Must be set together with `auth.username`, and is mutually exclusive with `auth.api_key`.<br> |
| $$$agent.download.auth.api_key$$$<br>`auth.api_key` {applies_to}`stack: ga 9.4+`<br> | (string) API key sent in the `Authorization: ApiKey <api-key>` header. Mutually exclusive with `auth.username` and `auth.password`. If both are configured, `auth.api_key` takes precedence.<br> |
| $$$agent.download.auth.headers$$$<br>`auth.headers` {applies_to}`stack: ga 9.4+`<br> | (list) Custom HTTP headers sent to the artifact registry on every request. Each entry is an object with `key` and `value` fields.<br> |

