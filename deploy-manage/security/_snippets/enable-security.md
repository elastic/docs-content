{{es}} security features unlock key capabilities such as [authentication and authorization](/deploy-manage/users-roles.md), TLS encryption, and other security-related functionality described in this section. The first step in securing your deployment is to ensure that the {{es}} security features are enabled and properly configured.

For self-managed deployments, security features are automatically configured when possible. To learn about the automatic configuration process, the cases where automatic configuration might be skipped, and how to manually configure security, refer to [](/deploy-manage/security/self-setup.md).

:::{tip}
If you want to use your own TLS certificates, then you should manually configure security.
:::

Deployments managed by {{eck}}, {{ece}}, {{ech}}, as well as {{serverless-full}} projects, automatically configure security by default. This includes setting the `elastic` user password, generating TLS certificates, and configuring {{kib}} to connect to {{es}} securely. Disabling security is not supported in these deployment types.