---
applies_to:
  deployment:
    eck: all
navigation_title: ECK
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-security.html
---

# Manage TLS certificates on ECK

All {{stack}} resources deployed by the ECK operator are secured by default. The operator sets up basic authentication and TLS to encrypt network traffic to, from, and within your {{es}} cluster and {{kib}} instances.

Refer to [Communication channels](./secure-cluster-communications.md#communication-channels) for an overview about the different endpoints and traffic flows to secure.

## {{es}} transport layer configuration

:::{include} ./_snippets/eck-transport.md
:::

## {{es}} and {{kib}} HTTP configuration

:::{include} ./_snippets/eck-http.md
:::

## Certificates lifecycle

:::{include} ./_snippets/eck-lifecycle.md
:::
