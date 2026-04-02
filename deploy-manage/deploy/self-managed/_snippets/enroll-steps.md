If this is the first time you’re starting {{kib}}, this command generates a unique link in your terminal to enroll your {{kib}} instance with {{es}}.

1. In your terminal, click the generated link to open {{kib}} in your browser.
2. In your browser, paste the enrollment token that was generated in the terminal when you started {{es}}, and then click the button to connect your {{kib}} instance with {{es}}.
3. Log in to {{kib}} as the `elastic` user with the password that was generated when you started {{es}}.

::::{note}
If you need to reset the password for the `elastic` user or other built-in users, run the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) tool. To generate new enrollment tokens for {{kib}} or {{es}} nodes, run the [`elasticsearch-create-enrollment-token`](elasticsearch://reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool. These tools are available in the {{es}} `bin` directory.
::::

:::{tip}
{{kib}} won’t enter interactive mode if it detects existing credentials for {{es}} (`elasticsearch.username` and `elasticsearch.password`) or an existing URL for `elasticsearch.hosts`.

In this case, you can enroll {{kib}} in detached mode:

Run the `kibana-setup` tool and pass the generated enrollment token with the `--enrollment-token` parameter.

```sh
bin/kibana-setup --enrollment-token <enrollment-token>
```
:::