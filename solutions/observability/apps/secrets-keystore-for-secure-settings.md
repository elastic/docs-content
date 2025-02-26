---
navigation_title: "Secrets keystore"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-keystore.html
applies_to:
  stack: all
---



# Secrets keystore for secure settings [apm-keystore]


::::{important}
The APM Server keystore only applies to the APM Server binary installation method.
::::


When you configure APM Server, you might need to specify sensitive settings, such as passwords. Rather than relying on file system permissions to protect these values, you can use the APM Server keystore to securely store secret values for use in configuration settings.

After adding a key and its secret value to the keystore, you can use the key in place of the secret value when you configure sensitive settings.

The syntax for referencing keys is identical to the syntax for environment variables:

`${KEY}`

Where KEY is the name of the key.

For example, imagine that the keystore contains a key called `ES_PWD` with the value `yourelasticsearchpassword`:

* In the configuration file, use `output.elasticsearch.password: "${ES_PWD}"`
* On the command line, use: `-E "output.elasticsearch.password=\${ES_PWD}"`

When APM Server unpacks the configuration, it resolves keys before resolving environment variables and other variables.

Notice that the APM Server keystore differs from the {{es}} keystore. Whereas the {{es}} keystore lets you store `elasticsearch.yml` values by name, the APM Server keystore lets you specify arbitrary names that you can reference in the APM Server configuration.

To create and manage keys, use the `keystore` command. See the [command reference](apm-server-command-reference.md#apm-keystore-command) for the full command syntax, including optional flags.

::::{note}
The `keystore` command must be run by the same user who will run APM Server.
::::



## Create a keystore [apm-creating-keystore]

To create a secrets keystore, use:

```sh
apm-server keystore create
```

APM Server creates the keystore in the directory defined by the `path.data` configuration setting.


## Add keys [apm-add-keys-to-keystore]

To store sensitive values, such as authentication credentials for {{es}}, use the `keystore add` command:

```sh
apm-server keystore add ES_PWD
```

When prompted, enter a value for the key.

To overwrite an existing key’s value, use the `--force` flag:

```sh
apm-server keystore add ES_PWD --force
```

To pass the value through stdin, use the `--stdin` flag. You can also use `--force`:

```sh
cat /file/containing/setting/value | apm-server keystore add ES_PWD --stdin --force
```


## List keys [apm-list-settings]

To list the keys defined in the keystore, use:

```sh
apm-server keystore list
```


## Remove keys [apm-remove-settings]

To remove a key from the keystore, use:

```sh
apm-server keystore remove ES_PWD
```

