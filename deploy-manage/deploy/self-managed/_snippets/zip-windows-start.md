Run the following command to start {{es}} from the command line:

```sh
.\bin\elasticsearch.bat
```

By default {{es}} prints its logs to the console (`STDOUT`) and to the `<cluster name>.log` file within the [logs directory](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings). {{es}} logs some information while it is starting, but after it has finished initializing it will continue to run in the foreground and won’t log anything further until something happens that is worth recording. While {{es}} is running you can interact with it through its HTTP interface which is on port `9200` by default.

To stop {{es}}, press `Ctrl-C`.