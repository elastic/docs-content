---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/system-config.html
---

# Important System configuration [system-config]

Ideally, {{es}} should run alone on a server and use all of the resources available to it. In order to do so, you need to configure your operating system to allow the user running {{es}} to access more resources than allowed by default.

The following settings **must** be considered before going to production:

* [Configure system settings](setting-system-settings.md)
* [Disable swapping](setup-configuration-memory.md)
* [Increase file descriptors](file-descriptors.md)
* [Ensure sufficient virtual memory](vm-max-map-count.md)
* [Ensure sufficient threads](max-number-of-threads.md)
* [JVM DNS cache settings](networkaddress-cache-ttl.md)
* [Temporary directory not mounted with `noexec`](executable-jna-tmpdir.md)
* [TCP retransmission timeout](system-config-tcpretries.md)


## Development mode vs production mode [dev-vs-prod] 

By default, {{es}} assumes that you are working in development mode. If any of the above settings are not configured correctly, a warning will be written to the log file, but you will be able to start and run your {{es}} node.

As soon as you configure a network setting like `network.host`, {{es}} assumes that you are moving to production and will upgrade the above warnings to exceptions. These exceptions will prevent your {{es}} node from starting. This is an important safety measure to ensure that you will not lose data because of a malconfigured server.









