---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/max-number-of-threads.html
navigation_title: Increase max number of threads
applies_to:
  deployment:
    self:
---

# Increase the maximum number of threads [max-number-of-threads]

{{es}} uses a number of thread pools for different types of operations. It is important that it is able to create new threads whenever needed. Make sure that the number of threads that the {{es}} user can create is at least 4096.

This can be done by setting [`ulimit -u 4096`](setting-system-settings.md#ulimit) as root before starting {{es}}, or by setting `nproc` to `4096` in [`/etc/security/limits.conf`](setting-system-settings.md#limits.conf).

The package distributions when run as services under `systemd` will configure the number of threads for the {{es}} process automatically. No additional configuration is required.

