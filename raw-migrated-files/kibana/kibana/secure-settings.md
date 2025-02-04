# Secure settings [secure-settings]

Some settings are sensitive, and relying on filesystem permissions to protect their values is not sufficient. For this use case, Kibana provides a keystore, and the `kibana-keystore` tool to manage the settings in the keystore.

::::{note} 
* Run all commands as the user who runs {{kib}}.
* Any valid {{kib}} setting can be stored in the keystore securely. Unsupported, extraneous or invalid settings will cause {{kib}} to fail to start up.

::::



## Create the keystore [creating-keystore] 

To create the `kibana.keystore`, use the `create` command:

```sh
bin/kibana-keystore create
```

The file `kibana.keystore` will be created in the `config` directory defined by the environment variable `KBN_PATH_CONF`.

To create a password protected keystore use the `--password` flag.


## List settings in the keystore [list-settings] 

A list of the settings in the keystore is available with the `list` command:

```sh
bin/kibana-keystore list
```


## Add string settings [add-string-to-keystore] 

::::{note} 
Your input will be JSON-parsed to allow for object/array input configurations. To enforce string values, use "double quotes" around your input.
::::


Sensitive string settings, like authentication credentials for Elasticsearch can be added using the `add` command:

```sh
bin/kibana-keystore add the.setting.name.to.set
```

Once added to the keystore, these setting will be automatically applied to this instance of Kibana when started. For example if you do

```sh
bin/kibana-keystore add elasticsearch.username
```

you will be prompted to provide the value for elasticsearch.username. (Your input will show as asterisks.)

The tool will prompt for the value of the setting. To pass the value through stdin, use the `--stdin` flag:

```sh
cat /file/containing/setting/value | bin/kibana-keystore add the.setting.name.to.set --stdin
```


## Remove settings [remove-settings] 

To remove a setting from the keystore, use the `remove` command:

```sh
bin/kibana-keystore remove the.setting.name.to.remove
```


## Read settings [read-settings] 

To display the configured setting values, use the `show` command:

```sh
bin/kibana-keystore show setting.key
```


## Change password [change-password] 

To change the password of the keystore, use the `passwd` command:

```sh
bin/kibana-keystore passwd
```


## Has password [has-password] 

To check if the keystore is password protected, use the `has-passwd` command. An exit code of 0 will be returned if the keystore is password protected, and the command will fail otherwise.

```sh
bin/kibana-keystore has-passwd
```

