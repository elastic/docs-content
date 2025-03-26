---
applies_to:
  deployment:
    ess: ga
    ece: ga
    eck: ga
    self: ga
  serverless: ga
---

# Encrypt your deployment data

(orphan now, we should put this content somewhere)

Add another layer of security by defining custom encryption rules for your cluster's data, {{kib}} saved objects, and settings.

**In {{ecloud}}**:

{{ech}} deployments and serverless projects are already encrypted at rest by default. This includes their data, objects, and settings. For serverless projects, security is fully-managed by Elastic. For {{ech}} deployments, some settings are available for you to customize the default security measures in place:

- Instead of the default, Elastic-managed encryption, you can choose to use a [customer-managed encryption key](encrypt-deployment-with-customer-managed-encryption-key.md) from one of our supported providers' KMS to encrypt your {{ech}} deployments.
- Store sensitive settings using the [{{es}} keystore](secure-settings.md).

**In {{ece}}, {{eck}} and self-managed installations**:

There is no encryption at rest out of the box for deployments orchestrated using [{{ece}}](secure-your-elastic-cloud-enterprise-installation.md) and [{{eck}}](secure-your-eck-installation.md), and for [self-managed clusters](manually-configure-security-in-self-managed-cluster.md). You must instead configure disk-level encryption on your hosts. 

:::{note}
Configuring dm-crypt or similar technologies is outside the scope of the Elastic documentation, and issues related to disk encryption are outside the scope of support.
:::

However, some native features are available for you to protect sensitive data and objects:

- Store sensitive settings using the [{{es}} or {{kib}} keystores](secure-settings.md).
- Enable [encryption for {{kib}} saved objects](secure-saved-objects.md).
- Customize [{{kib}} session parameters](kibana-session-management.md).



