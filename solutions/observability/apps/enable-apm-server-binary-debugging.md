---
navigation_title: "APM Server binary debugging"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-enable-apm-server-debugging.html
applies_to:
  stack:
---



# Enable APM Server binary debugging [apm-enable-apm-server-debugging]


::::{note}
Fleet-managed users should see [View {{agent}} logs](/reference/fleet/monitor-elastic-agent.md) to learn how to view logs and change the logging level of {{agent}}.
::::


By default, APM Server sends all its output to syslog. When you run APM Server in the foreground, you can use the `-e` command line flag to redirect the output to standard error instead. For example:

```sh
apm-server -e
```

The default configuration file is apm-server.yml (the location of the file varies by platform). You can use a different configuration file by specifying the `-c` flag. For example:

```sh
apm-server -e -c myapm-serverconfig.yml
```

You can increase the verbosity of debug messages by enabling one or more debug selectors. For example, to view publisher-related messages, start APM Server with the `publisher` selector:

```sh
apm-server -e -d "publisher"
```

If you want all the debugging output (fair warning, it’s quite a lot), you can use `*`, like this:

```sh
apm-server -e -d "*"
```

