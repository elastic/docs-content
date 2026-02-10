---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Increase virtual memory [vm-max-map-count]

{{es}} uses a [`mmapfs`](elasticsearch://reference/elasticsearch/index-settings/store.md#mmapfs) directory by default to store its indices. The default operating system limits on mmap counts could be too low, which may result in out of memory exceptions.

:::{admonition} Verify vm.max_map_count configuration
If the operating system's default `vm.max_map_count` value is `1048576` or higher, no configuration change is necessary. If the default value is lower than `1048576`, configure the `vm.max_map_count` parameter to `1048576`.
:::


On Linux, you can increase the limits of the `vm.max_map_count` parameter by following these steps as an account with `root` privileges: 

1. Check the existing settings by searching for any existing configuration files under `/etc/sysctl.d/` that include the `vm.max_map_count` parameter:

    ```
    grep -r vm.max_map_count /etc/sysctl.d/
    ```
   
1. Update or create a configuration file:
    * If the parameter already exists in a file under `/etc/sysctl.d/`, update its value to `1048576`:
        ```sh
        sysctl -w vm.max_map_count=1048576
        ```
    * If it does not exist, create a new conf file named `/etc/sysctl.d/99-elasticsearch.conf` which includes the following:
        ```
        vm.max_map_count=1048576
        ```
1. To apply the changes without rebooting, run the following command:
    ```sh
    sudo sysctl --system
    ```


:::{note}
On systemd-based systems, the {{es}} package might install `/usr/lib/sysctl.d/elasticsearch.conf` with a lower value such as `262144`. A file with the same name under `/etc/sysctl.d/` takes precedence, so creating `/etc/sysctl.d/99-elasticsearch.conf` is a valid option to permanently set the value of `vm.max_map_count` to `1048576`. Do not edit files under `/usr/lib/sysctl.d/` directly, as they are managed by the package and may be overwritten on upgrade.
:::



To confirm the setting is active, run:

```sh
sysctl vm.max_map_count
```


You can find out the current mmap count of a running {{es}} process using the following command, where `$PID` is the process ID of the running {{es}} process:

```sh
wc -l /proc/$PID/maps
```

