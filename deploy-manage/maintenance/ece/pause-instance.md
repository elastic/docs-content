---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-maintenance-mode-pausing.html
applies_to:
  deployment:
     ece:
---

# Pause instance [ece-maintenance-mode-pausing]

If an individual instance is experiencing issues, then you can stop it by selecting **Pause instance** from its menu.

Pausing an instance immediately suspends the container without completing existing requests by running either [Docker `stop`](https://docs.docker.com/reference/cli/docker/container/stop/) or [Podman `stop`](https://docs.podman.io/en/stable/markdown/podman-stop.1.md), as applicable. The instance will then be marked as **Paused**.

You can start an instance by selecting **Resume instance** from the menu.

Pausing and resuming an instance can be helpful when an individual instance needs restarted without restarting the entire product. For example, you might restart an instance if an {{es}} node is unresponsive to the cluster due to [stuck JVM](../../../troubleshoot/elasticsearch/high-jvm-memory-pressure.md).
