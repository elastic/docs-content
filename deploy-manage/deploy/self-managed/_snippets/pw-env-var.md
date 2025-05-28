We recommend storing the `elastic` password as an environment variable in your shell. For example:

```sh subs=true
{{export}} ELASTIC_PASSWORD="your_password"
```

If you have password-protected the {{es}} keystore, you will be prompted to enter the keystore’s password. See [Secure settings](/deploy-manage/security/secure-settings.md) for more details.

To learn how to reset this password, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-sm.md).
