{{es}} security unlocks key capabilities such as [Authentication and authorization](/deploy-manage/users-roles.md), TLS encryption, and other security-related functionality described in this section. The first step in securing your deployment is to ensure that the {{es}} security feature is enabled and properly configured.

::::{note}
Deployments managed by {{eck}}, {{ece}}, {{ech}}, and {{serverless-short}} automatically configure security by default. This includes setting the `elastic` user password, generating TLS certificates, and configuring {{kib}} to connect to {{es}} securely. Disabling security is not supported in these deployment types.
::::

For self-managed deployments, [Learn how to set up security](/deploy-manage/security/self-setup.md) using Elastic’s automatic configuration or by following the manual process.