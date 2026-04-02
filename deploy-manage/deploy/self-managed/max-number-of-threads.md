---
navigation_title: Increase max number of threads
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/max-number-of-threads.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Increase the maximum number of threads [max-number-of-threads]

{{es}} uses a number of thread pools for different types of operations. It is important that it is able to create new threads whenever needed. Make sure that the number of threads that the {{es}} user can create is at least `4096`.

To apply this limit, use the [system settings configuration methods](setting-system-settings.md) for your install type. For example, using `ulimit` and editing `/etc/security/limits.conf` for `.tar.gz` archives, or through `systemd` overrides when you need to change defaults on package-based installations.

The package distributions when run as services under `systemd` will configure the number of threads for the {{es}} process automatically. No additional configuration is required.


