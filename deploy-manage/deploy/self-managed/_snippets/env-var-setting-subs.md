Environment variables referenced with the `${...}` notation within the configuration file will be replaced with the value of the environment variable. For example:

```yaml
node.name:    ${HOSTNAME}
network.host: ${ES_NETWORK_HOST}
```

Values for environment variables must be simple strings. Use a comma-separated string to provide values that the component will parse as a list. For example, {{es}} will split the following string into a list of values for the `${HOSTNAME}` environment variable:

```yaml
export HOSTNAME="host1,host2"
```

By default, configuration validation will fail if an environment variable used in the config file is not present when the component starts. This behavior can be changed by using a default value for the environment variable, using the `${MY_ENV_VAR:defaultValue}` syntax.