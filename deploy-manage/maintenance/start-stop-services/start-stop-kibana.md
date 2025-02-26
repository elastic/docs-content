---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/start-stop.html
applies_to:
  deployment:
     self:
---

# Start and stop Kibana [start-stop]

The method for starting and stopping {{kib}} varies depending on how you installed it.  If a password protected keystore is used, the environment variable `KBN_KEYSTORE_PASSPHRASE_FILE` can be used to point to a file containing the password, the environment variable `KEYSTORE_PASSWORD` can be defined, or you will be prompted to enter to enter the password on startup,

## Archive packages (`.tar.gz`) [start-start-targz]

If you installed {{kib}} on Linux or Darwin with a `.tar.gz` package, you can start and stop {{kib}} from the command line.

### Run {{kib}} from the command line [run-kibana-from-command-line]

Kibana can be started from the command line as follows:

```sh
./bin/kibana
```

By default, Kibana runs in the foreground, prints its logs to the standard output (`stdout`), and can be stopped by pressing **Ctrl-C**.

If this is the first time you’re starting {{kib}}, this command generates a unique link in your terminal to enroll your {{kib}} instance with {{es}}.

1. In your terminal, click the generated link to open {{kib}} in your browser.
2. In your browser, paste the enrollment token that was generated in the terminal when you started {{es}}, and then click the button to connect your {{kib}} instance with {{es}}.
3. Log in to {{kib}} as the `elastic` user with the password that was generated when you started {{es}}.

::::{note} 
If you need to reset the password for the `elastic` user or other built-in users, run the [`elasticsearch-reset-password`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/reset-password.md) tool. To generate new enrollment tokens for {{kib}} or {{es}} nodes, run the [`elasticsearch-create-enrollment-token`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool. These tools are available in the {{es}} `bin` directory.

::::

## Archive packages (`.zip`) [start-stop-zip]

If you installed {{kib}} on Windows with a `.zip` package, you can stop and start {{kib}} from the command line.

### Run {{kib}} from the command line [_run_kib_from_the_command_line_2]

Kibana can be started from the command line as follows:

```sh
.\bin\kibana.bat
```

By default, Kibana runs in the foreground, prints its logs to `STDOUT`, and can be stopped by pressing **Ctrl-C**.

If this is the first time you’re starting {{kib}}, this command generates a unique link in your terminal to enroll your {{kib}} instance with {{es}}.

1. In your terminal, click the generated link to open {{kib}} in your browser.
2. In your browser, paste the enrollment token that was generated in the terminal when you started {{es}}, and then click the button to connect your {{kib}} instance with {{es}}.
3. Log in to {{kib}} as the `elastic` user with the password that was generated when you started {{es}}.

::::{note} 
If you need to reset the password for the `elastic` user or other built-in users, run the [`elasticsearch-reset-password`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/reset-password.md) tool. To generate new enrollment tokens for {{kib}} or {{es}} nodes, run the [`elasticsearch-create-enrollment-token`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool. These tools are available in the {{es}} `bin` directory.

::::

## Debian and RPM packages [start-stop-deb-rpm]

### Run {{kib}} with `systemd` [_run_kib_with_systemd]

To configure {{kib}} to start automatically when the system starts, run the following commands:

```sh
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable kibana.service
```

{{kib}} can be started and stopped as follows:

```sh
sudo systemctl start kibana.service
sudo systemctl stop kibana.service
```

These commands provide no feedback as to whether {{kib}} was started successfully or not. Log information can be accessed via `journalctl -u kibana.service`.