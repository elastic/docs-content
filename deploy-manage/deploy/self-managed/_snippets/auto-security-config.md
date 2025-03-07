When you start {{es}} for the first time, the following security configuration occurs automatically:

* [Certificates and keys](/deploy-manage/security/security-certificates-keys.md#stack-security-certificates) for TLS are generated for the transport and HTTP layers.
* The TLS configuration settings are written to `elasticsearch.yml`.
* A password is generated for the `elastic` user.
* An enrollment token is generated for {{kib}}, which is valid for 30 minutes.

You can then start {{kib}} and enter the enrollment token. This token automatically applies the security settings from your {{es}} cluster, authenticates to {{es}} with the built-in `kibana` service account, and writes the security configuration to `kibana.yml`.

::::{note}
There are [some cases](/deploy-manage/security/security-certificates-keys.md#stack-skip-auto-configuration) where security can’t be configured automatically because the node startup process detects that the node is already part of a cluster, or that security is already configured or explicitly disabled.
::::