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

{{es}} uses a [`mmapfs`](elasticsearch://reference/elasticsearch/index-settings/store.md#mmapfs) directory by default to store its indices, which relies on memory-mapped files. As a result, the default operating system limit for the maximum number of memory mappings per process (`vm.max_map_count`) must be adequately high. If this limit is too low, the node might fail to start or encounter out-of-memory errors.

:::{admonition} Verify vm.max_map_count configuration
If the operating system's default `vm.max_map_count` value is `1048576` or higher, no configuration change is necessary. If the default value is lower than `1048576`, configure the `vm.max_map_count` parameter to `1048576`.
:::


On Linux, you can increase the limits of the `vm.max_map_count` parameter by following this step as an account with `root` privileges:

```sh
sysctl -w vm.max_map_count=1048576
```

To set this value permanently, update the `vm.max_map_count` setting in `/etc/sysctl.conf`. 

To verify after rebooting, run:

```sh
sysctl vm.max_map_count
```

To reflect the change immediately, without rebooting, run:

```sh
sudo sysctl --system
```

While RPM and Debian packages attempt to configure this automatically, setting the value in `/etc/sysctl.conf` ensures that it takes precedence and that the correct value is applied, overriding any package-level defaults.


You can find out the current mmap count of a running {{es}} process using the following command, where `$PID` is the process ID of the running {{es}} process:

```sh
wc -l /proc/$PID/maps
```

