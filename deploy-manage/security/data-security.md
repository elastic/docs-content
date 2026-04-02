---
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Encrypt your deployment data

{{ech}} deployments and {{serverless-full}} projects are already encrypted at rest by default. This includes their data, objects, and settings. 

For {{serverless-full}} projects, security is fully-managed by Elastic. 

For {{ech}} deployments, instead of the default, Elastic-managed encryption, you can choose to use a [customer-managed encryption key](encrypt-deployment-with-customer-managed-encryption-key.md) to encrypt your {{ech}} deployments.


:::{note}
There is no encryption at rest out of the box for deployments orchestrated using {{ece}} and {{eck}}secure-your-eck-installation.md, or for self-managed clusters. You must instead configure disk-level encryption on your hosts. 

Configuring dm-crypt or similar technologies is outside the scope of the Elastic documentation, and issues related to disk encryption are outside the scope of support.
:::


:::{tip}
As an alternative to or in addition to encryption at rest, you can also use the following features to encrypt sensitive data and objects: 

- Store sensitive settings using the [{{es}} or {{kib}} keystores](secure-settings.md).
- Enable [encryption for {{kib}} saved objects](secure-saved-objects.md).
:::