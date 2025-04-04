---
applies_to:
  deployment:
    eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-reserved-settings.html
---

# Settings managed by ECK [k8s-reserved-settings]

The following {{es}} settings are managed by ECK:

* `cluster.name`
* `discovery.seed_hosts`
* `discovery.seed_providers`
* `discovery.zen.minimum_master_nodes`
* `cluster.initial_master_nodes`
* `network.host`
* `network.publish_host`
* `path.data`
* `path.logs`
* `xpack.security.authc.reserved_realm.enabled`
* `xpack.security.enabled`
* `xpack.security.http.ssl.certificate`
* `xpack.security.http.ssl.enabled`
* `xpack.security.http.ssl.key`
* `xpack.security.transport.ssl.enabled`
* `xpack.security.transport.ssl.verification_mode`

The following {{es}} settings are not supported by ECK:

* `xpack.security.http.ssl.client_authentication`: `required`

::::{warning}
It is not recommended to change these ECK settings. We don’t support user-provided {{es}} configurations that use any of these settings.
::::
