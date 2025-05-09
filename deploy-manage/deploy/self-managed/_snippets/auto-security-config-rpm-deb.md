When you start {{es}} for the first time, it automatically performs the following security setup:

* Generates [TLS certificates](#stack-security-certificates) for the [transport and HTTP layers](/deploy-manage/security/secure-cluster-communications.md#communication-channels)
* Applies TLS configuration settings to [`elasticsearch.yml`](/deploy-manage/stack-settings.md)
* Creates an enrollment token to securely connect {{kib}} to {{es}}

You can then start {{kib}} and enter the enrollment token, which is valid for 30 minutes. This token automatically applies the security settings from your {{es}} cluster, authenticates to {{es}} with the built-in `kibana` service account, and writes the security configuration to [`kibana.yml`](/deploy-manage/stack-settings.md).

::::{note}
There are [some cases](/deploy-manage/security/self-auto-setup.md#stack-skip-auto-configuration) where security can’t be configured automatically because the node startup process detects that the node is already part of a cluster, or that security is already configured or explicitly disabled.
::::