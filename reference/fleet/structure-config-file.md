---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/structure-config-file.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Structure of a config file [structure-config-file]

The `elastic-agent.yml` policy file contains all of the settings that determine how {{agent}} runs. The most important and commonly used settings are described here, including input and output options, providers used for variables and conditional output, security settings, logging options, enabling of special features, and specifications for {{agent}} upgrades.

An `elastic-agent.yml` file is modular: You can combine input, output, and all other settings to enable the [{{integrations}}](integration-docs://reference/index.md) to use with {{agent}}. Refer to [Create a standalone {{agent}} policy](/reference/fleet/create-standalone-agent-policy.md) for the steps to download the settings to use as a starting point, and then refer to the following examples to learn about the available settings:

* [Config file examples](/reference/fleet/config-file-examples.md)
* [Use standalone {{agent}} to monitor nginx](/reference/fleet/example-standalone-monitor-nginx.md).


## Config file components [structure-config-file-components]

The following categories include the most common settings used to configure standalone {{agent}}. Follow each link for more detail and examples.

[Inputs](/reference/fleet/elastic-agent-input-configuration.md)
:   Specify how {{agent}} locates and processes input data.

[Providers](/reference/fleet/providers.md)
:   Specify the key-value pairs used for variable substitution and conditionals in {{agent}} output.

[Outputs](/reference/fleet/elastic-agent-output-configuration.md)
:   Specify where {{agent}} sends data.

[SSL/TLS](/reference/fleet/elastic-agent-ssl-configuration.md)
:   Configure SSL including SSL protocols and settings for certificates and keys.

[Logging](/reference/fleet/elastic-agent-standalone-logging-config.md)
:   Configure the {{agent}} logging output.

[Feature flags](/reference/fleet/elastic-agent-standalone-feature-flags.md)
:   Configure any experiemental features in {{agent}}. These are disabled by default.

[Agent download](/reference/fleet/elastic-agent-standalone-download.md)
:   Specify the location of required artifacts and other settings used for {{agent}} upgrades.

