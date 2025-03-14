---
navigation_title: "Agent download"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-standalone-download.html
---

# Configure download settings for standalone {{agent}} upgrades [elastic-agent-standalone-download]


The `agent.download` section of the elastic-agent.yml config file contains settings for where to download and store artifacts used for {{agent}} upgrades.

$$$elastic-agent-standalone-download-settings$$$

| Setting | Description |
| --- | --- |
| $$$agent.download.sourceURI$$$<br>`sourceURI`<br> | (string) Path to the location of artifacts used during {{agent}} upgrade.<br> |
| $$$agent.download.target_directory$$$<br>`target_directory`<br> | (string) Path to the directory where download artifacts are stored.<br> |
| $$$agent.download.timeout$$$<br>`timeout`<br> | (string) The HTTP request timeout in seconds for the download package attempt.<br> |
| $$$agent.download.install_path$$$<br>`install_path`<br> | (string) The location of installed packages and programs, as well as program specifications.<br> |
| $$$agent.download.retry_sleep_init_duration$$$<br>`retry_sleep_init_duration`<br> | (string) The duration in seconds to sleep for before the first retry attempt.<br> |

