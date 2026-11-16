---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-kibana-plugins.html
description: Run Kibana on ECK with additional plugins by using a custom container image that already includes them.
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
navigation_title: "{{kib}} plugins"
---

# Install {{kib}} plugins on {{eck}} [k8s-kibana-plugins]

You can override the {{kib}} container image to use your own image with the plugins already installed, as described in [Create custom images](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md).

This is a Dockerfile example:

```

