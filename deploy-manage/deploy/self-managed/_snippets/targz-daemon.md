To run {{es}} as a daemon, specify `-d` on the command line, and record the process ID in a file using the `-p` option:

```sh
./bin/elasticsearch -d -p pid
```

If you have password-protected the {{es}} keystore, you will be prompted to enter the keystore’s password. See [Secure settings](/deploy-manage/security/secure-settings.md) for more details.

Log messages can be found in the `$ES_HOME/logs/` directory.

To shut down {{es}}, kill the process ID recorded in the `pid` file:

```sh
pkill -F pid
```

::::{note}
The {{es}} `.tar.gz` package does not include the `systemd` module. To manage {{es}} as a service, use the [Debian](/deploy-manage/deploy/self-managed/install-kibana-with-debian-package.md) or [RPM](/deploy-manage/deploy/self-managed/install-kibana-with-rpm.md) package instead.
::::