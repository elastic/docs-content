---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-kibana-plugins.html
---

# Install Kibana plugins [k8s-kibana-plugins]

You can override the {{kib}} container image to use your own image with the plugins already installed, as described in the [Create custom images](create-custom-images.md). You should run an `optimize` step as part of the build, otherwise it needs to run at startup which requires additional time and resources.

This is a Dockerfile example:

```
FROM docker.elastic.co/kibana/kibana:8.16.1
RUN /usr/share/kibana/bin/kibana-plugin install $PLUGIN_URL
RUN /usr/share/kibana/bin/kibana --optimize
```

