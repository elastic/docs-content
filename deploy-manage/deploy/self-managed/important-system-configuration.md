---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/system-config.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Important system configuration [system-config]

Ideally, {{es}} should run alone on a server and use all of the resources available to it. In order to do so, you need to configure your operating system to allow the user running {{es}} to access more resources than allowed by default.

The following settings **must** be considered before going to production:

* [](setting-system-settings.md)
* [](setup-configuration-memory.md)
* [](vm-max-map-count.md)
* [](max-number-of-threads.md)
* [](file-descriptors.md) (Linux and MacOS only)
* [](executable-jna-tmpdir.md) (Linux only)
* [](system-config-tcpretries.md) (Linux only)

:::{tip}
For examples of applying the relevant settings in a Docker environment, refer to [](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-prod.md).
:::

::::{admonition} Use dedicated hosts
:::{include} _snippets/dedicated-hosts.md
:::
::::

## Bootstrap checks

{{es}} has bootstrap checks that run at startup to ensure that users have configured all important settings. 

For a list of the checks and their meaning, refer to [](/deploy-manage/deploy/self-managed/bootstrap-checks.md).

### Development mode vs. production mode [dev-vs-prod] 

By default, {{es}} assumes that you are working in development mode. If any of the above settings are not configured correctly, the relevant bootstrap check will fail and a warning will be written to the log file, but you will be able to start and run your {{es}} node.

As soon as you configure a network setting like `network.host`, {{es}} assumes that you are moving to production and will upgrade the above warnings to exceptions. These exceptions will prevent your {{es}} node from starting. This is an important safety measure to ensure that you will not lose data because of a misconfigured server.









