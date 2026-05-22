---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/file-descriptors.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Increase the file descriptor limit [file-descriptors]

::::{note} 
This is only relevant for Linux and macOS and can be safely ignored if running {{es}} on Windows. On Windows, that JVM uses an [API](https://msdn.microsoft.com/en-us/library/windows/desktop/aa363858(v=vs.85).aspx) limited only by available resources.
::::


{{es}} uses a lot of file descriptors or file handles. Running out of file descriptors can be disastrous and will most probably lead to data loss. Make sure to increase the limit on the number of open files descriptors for the user running {{es}} to 65,535 or higher.

Apply this limit using the [system settings configuration methods](setting-system-settings.md) for your install type. For example using `ulimit` and editing `/etc/security/limits.conf` for `.tar.gz` archives, or through `systemd` overrides when you need to change defaults on package-based installations.

On macOS, you must also pass the JVM option `-XX:-MaxFDLimit` to {{es}} in order for it to make use of the higher file descriptor limit.

RPM and Debian packages already default the maximum number of file descriptors to 65535 and do not require further configuration.

You can check the `max_file_descriptors` configured for each node using the [Nodes stats]({{es-apis}}operation/operation-nodes-stats) API, with:

```console
GET _nodes/stats/process?filter_path=**.max_file_descriptors
```
