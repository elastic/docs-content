When installing {es}, security features are enabled and configured by default.

When you start {{es}} for the first time, the following security configuration occurs automatically:

* Authentication and authorization are enabled, and a password is generated for the `elastic` built-in superuser.
* Certificates and keys for TLS are generated for the transport and HTTP layer, and TLS is enabled and configured with these keys and certificates.

The password and certificate and keys are output to your terminal. You can reset the password for the `elastic` user with the [`elasticsearch-reset-password`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/reset-password.md) command.

We recommend storing the `elastic` password as an environment variable in your shell. For example:

```sh
export ELASTIC_PASSWORD="your_password"
```