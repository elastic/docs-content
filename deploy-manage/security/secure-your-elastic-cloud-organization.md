---
navigation_title: "{{ecloud}}"
applies_to:
  deployment:
    ess: ga
  serverless: ga
---

# Secure your Elastic Cloud organization [ec-securing-considerations]

**This page is a work in progress.**

## TLS certificate management

TLS certificates apply security controls to network communications. They encrypt data in transit, verify the identity of connecting parties, and help prevent man-in-the-middle attacks.

For your **{{ech}}** deployments and serverless projects hosted on {{ecloud}}, TLS certificates are managed automatically.

## Network security

Control which systems can access your Elastic deployment through traffic filtering and network controls:

- **IP traffic filtering**: Restrict access based on IP addresses or CIDR ranges.
- **Private link filters**: Secure connectivity through AWS PrivateLink, Azure Private Link, or GCP Private Service Connect.
- **Static IPs**: Use static IP addresses for predictable firewall rules.


## Next step: secure your deployments and clusters

This section covered security principles and options at the environment level. You can take further measures individually for each deployment or cluster that you're running on your installation. Refer to [](secure-your-cluster-deployment.md).
