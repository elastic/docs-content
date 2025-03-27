{{es}} security provides authentication, authorization, TLS encryption, and other capabilities described in this section. The first step in securing your self-managed deployment is to ensure that the {{es}} security feature is enabled and properly configured.

::::{note}
Deployments managed by {{eck}}, {{ece}}, {{ech}}, and {{serverless-short}} automatically configure security by default. This includes setting the `elastic` user password, generating TLS certificates, and configuring {{kib}} to connect to {{es}} securely. Disabling security is not supported in these deployment types.
::::

For self-managed deployments, refer to the [set up security](../self-setup.md) guide, which explains how to enable security using Elastic’s automatic configuration or by following the manual process.