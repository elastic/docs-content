---
mapped_pages:
  - https://www.elastic.co/guide/en/beats/loggingplugin/current/log-driver-troubleshooting.html
---

# Elastic Logging Plugin for Docker [log-driver-troubleshooting]

You can set the debug level to capture debugging output about the Elastic Logging Plugin. To set the debug level:

1. Disable the plugin:

    ```sh
    docker plugin disable elastic/elastic-logging-plugin:9.0.0-beta1
    ```

2. Set the debug level:

    ```sh
    docker plugin set elastic/elastic-logging-plugin:9.0.0-beta1 LOG_DRIVER_LEVEL=debug
    ```

    Where valid settings for `LOG_DRIVER_LEVEL` are `debug`, `info`, `warning`, or `error`.

3. Enable the plugin:

    ```sh
    docker plugin enable elastic/elastic-logging-plugin:9.0.0-beta1
    ```


To view the logs:

On Linux, the Elastic Logging Plugin logs are written to the same location as other docker logs, typically the system journal.

On MacOS, locating the logs is more complicated. For more information, see the [Debugging on MacOS](https://github.com/elastic/beats/tree/master/x-pack/dockerlogbeat#debugging-on-macos) section in the readme file.

