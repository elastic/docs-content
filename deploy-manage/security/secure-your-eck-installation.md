---
navigation_title: "{{eck}}"
applies_to:
  deployment:
    eck: ga
---

# Secure your {{eck}} installation [eck-securing-considerations]

:::{warning}
**This page is a work in progress.** 
:::


## TLS certificate management

TLS certificates apply security controls to network communications. They encrypt data in transit, verify the identity of connecting parties, and help prevent man-in-the-middle attacks.

With **{{eck}}**, you manage HTTP layer certificates. The transport layer is managed by ECK.

## Network security

Control which systems can access your Elastic deployment through traffic filtering and network controls:

- **IP traffic filtering**: Restrict access based on IP addresses or CIDR ranges.

## Next step: secure your deployments and clusters

This section covered security principles and options at the environment level. You can take further measures individually for each deployment or cluster that you're running on this environment. Refer to [](secure-your-cluster-deployment.md).

