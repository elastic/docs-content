---
navigation_title: To an external cluster
applies_to:
  deployment:
    eck: ga
products:
  - id: cloud-kubernetes
---

# Connect an ECK-managed cluster to an external {{es}} cluster
(Use case missing).

This guide explains how to configure remote clusters when your ECK-managed cluster connects to a self-managed cluster, an ECE/ECH deployment, or a cluster managed by another ECK operator.

::::{include} _snippets/eck_rcs_intro.md
::::



Intro, the external / remote cluster in this case could be ECH/ECE/self-managed or even an ECK-managed cluster managed by a different operator.

When the remote cluster is not handled by the same operator, there are certain things that the operator is not capable to do, so it requires some extra steps.

(license considerations)

This guide focuses on API key based authentication as the security model, as TLS cert based authentication is deprecated in favor of API.

Steps:
1. Enable the remote cluster server on the remote (if it's ECH or ECE it's enabled by default)
2. Create an API key on the remote, get CA certificate.
3. Create the connection from the local ECK-managed Elasticsearch cluster

(note: the orchestrator does NOT help in this process at all... or would it help?)

process described here: https://github.com/elastic/cloud-on-k8s/issues/8502#issuecomment-2753674140 (for ECH)
(does it make sense to recreate N docs or try to create a single one?)
ECK to --> another ECK, self-managed, ECH, ECE.



