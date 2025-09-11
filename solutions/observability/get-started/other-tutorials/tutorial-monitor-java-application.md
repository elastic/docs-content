---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-java-app.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Tutorial: Monitor a Java application [monitor-java-app]

In this guide, you’ll learn how to monitor a Java application using Elastic {{observability}}: Logs, Infrastructure metrics, APM, and Uptime.

## What you’ll learn [_what_youll_learn]

You’ll learn how to:

* Create a sample Java application.
* Ingest logs using {{filebeat}} and view your logs in {{kib}}.
* Ingest metrics using the [Metricbeat Prometheus Module](beats://reference/metricbeat/metricbeat-module-prometheus.md) and view your metrics in {{kib}}.
* Instrument your application using the [Elastic APM Java agent](apm-agent-java://reference/index.md).
* Monitor your services using {{heartbeat}} and view your uptime data in {{kib}}.

## Before you begin [_before_you_begin]

Create an [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) deployment. The deployment includes an {{es}} cluster for storing and searching your data, {{kib}} for visualizing and managing your data, and an APM server. If you do not want to follow all those steps listed here and take a look at the final java code, check out the [observability-contrib GitHub repository](https://github.com/elastic/observability-contrib/tree/main/monitor-java-app) for the sample application.

## Step 1: Create a Java application [_step_1_create_a_java_application]

To create the Java application, you require OpenJDK 14 (or higher) and the [Javalin](https://javalin.io/) web framework. The application will include the main endpoint, an artificially long-running endpoint, and an endpoint that needs to poll another data source. There will also be a background job running.

1. Set up a Gradle project and create the following `build.gradle` file.

    ```gradle
    plugins {
      id 'java'
      id 'application'
    }

    repositories {
      jcenter()
    }

    dependencies {
      implementation 'io.javalin:javalin:3.10.1'

      testImplementation 'org.junit.jupiter:junit-jupiter-api:5.6.2'
      testRuntimeOnly 'org.junit.jupiter:junit-jupiter-engine:5.6.2'
    }

    application {
      mainClassName = 'de.spinscale.javalin.App'
    }

    test {
      useJUnitPlatform()
    }
    ```

2. Run the following command.

    ```bash
    echo "rootProject.name = 'javalin-app'" >> settings.gradle

    mkdir -p src/main/java/de/spinscale/javalin
    mkdir -p src/test/java/de/spinscale/javalin
    ```

3. Install the Gradle wrapper. An easy way to install Gradle is to use [sdkman](https://sdkman.io/) and run `sdk install gradle 6.5.1`. Next run `gradle wrapper` in the current directory to install the Gradle wrapper.
4. Run `./gradlew clean check`. You should see a successful build that has nothing built or compiled yet.
5. To create a Javalin server and its first endpoint (the main endpoint), create the `src/main/java/de/spinscale/javalin/App.java` file.

    ```java
    package de.spinscale.javalin;

    import io.javalin.Javalin;

    public class App {
        public static void main(String[] args) {
            Javalin app = Javalin.create().start(7000);
            app.get("/", ctx -> ctx.result("Appsolutely perfect"));
        }
    }
    ```

6. Run `./gradlew assemble`

    This command compiled the `App.class` file in the `build` directory. However, there is no way to start the server. Let’s create a jar that contains our compiled class along with all the required dependencies.

7. In the `build.gradle` file, edit `plugins` as shown here.

    ```gradle
    plugins {
      id 'com.github.johnrengelman.shadow' version '6.0.0'
      id 'application'
      id 'java'
    }
    ```

8. Run `./gradlew shadowJar`. This command creates a `build/libs/javalin-app-all.jar` file.

    The `shadowJar` plugin requires information about its main class.

9. Add the following snippet to the `build.gradle` file.

    ```gradle
    jar {
      manifest {
        attributes 'Main-Class': 'de.spinscale.javalin.App'
      }
    }
    ```

10. Rebuild the project and start the server.

    ```bash
    java -jar build/libs/javalin-app-all.jar
    ```

    Open another terminal and run `curl localhost:7000` to display an HTTP response.

11. Test the code. Placing everything into the `main()` method makes it difficult to test the code. However, a dedicated handler fixes this.

    Refactor the `App` class.

    ```java
    package de.spinscale.javalin;

    import io.javalin.Javalin;
    import io.javalin.http.Handler;

    public class App {

        public static void main(String[] args) {
            Javalin app = Javalin.create().start(7000);
            app.get("/", mainHandler());
        }

        static Handler mainHandler() {
            return ctx -> ctx.result("Appsolutely perfect");
        }
    }
    ```

    Add a Mockito and an Assertj dependency to the `build.gradle` file.

    ```gradle
    dependencies {
      implementation 'io.javalin:javalin:3.10.1'

      testImplementation 'org.mockito:mockito-core:3.5.10'
      testImplementation 'org.assertj:assertj-core:3.17.2'
      testImplementation 'org.junit.jupiter:junit-jupiter-api:5.6.2'
      testRuntimeOnly 'org.junit.jupiter:junit-jupiter-engine:5.6.2'
    }
    ```

    Create an `AppTests.java` class file in `src/test/java/de/spinscale/javalin`.

    ```java
    package de.spinscale.javalin;

    import io.javalin.http.Context;
    import org.junit.jupiter.api.Test;

    import javax.servlet.http.HttpServletRequest;
    import javax.servlet.http.HttpServletResponse;
    import java.io.IOException;
    import java.nio.charset.StandardCharsets;
    import java.util.HashMap;

    import static de.spinscale.javalin.App.mainHandler;
    import static org.assertj.core.api.Assertions.assertThat;
    import static org.mockito.Mockito.mock;

    public class AppTests {

        final HttpServletRequest req = mock(HttpServletRequest.class);
        final HttpServletResponse res = mock(HttpServletResponse.class);
        final Context ctx = new Context(req, res, new HashMap<>());

        @Test
        public void testMainHandler() throws Exception {
            mainHandler().handle(ctx);

            String response = resultStreamToString(ctx);
            assertThat(response).isEqualTo("Appsolutely perfect");
        }

        private String resultStreamToString(Context ctx) throws IOException {
            final byte[] bytes = ctx.resultStream().readAllBytes();
            return new String(bytes, StandardCharsets.UTF_8);
        }
    }
    ```

12. After the tests pass, build and package the application.

    ```bash
    ./gradlew clean check shadowJar
    ```

## Step 2: Ingest logs [_step_2_ingest_logs]

Logs can be events such as checkout, an exception, or an HTTP request. For this tutorial, let’s use log4j2 as our logging implementation.

### Add logging implementation [_add_logging_implementation]

1. Add the dependency to the `build.gradle` file.

    ```gradle
    dependencies {
      implementation 'io.javalin:javalin:3.10.1'
      implementation 'org.apache.logging.log4j:log4j-slf4j18-impl:2.13.3'

      ...
    }
    ```

2. To start logging, edit the `App.java` file and change a handler.

    ::::{note}
    The logger call must be within the lambda. Otherwise, the log message is logged only during startup.

    ::::

    ```java
    package de.spinscale.javalin;

    import io.javalin.Javalin;
    import io.javalin.http.Handler;
    import org.slf4j.Logger;
    import org.slf4j.LoggerFactory;

    public class App {

        private static final Logger logger = LoggerFactory.getLogger(App.class);

        public static void main(String[] args) {
            Javalin app = Javalin.create();
            app.get("/", mainHandler());
            app.start(7000);
        }

        static Handler mainHandler() {
            return ctx -> {
                logger.info("This is an informative logging message, user agent [{}]", ctx.userAgent());
                ctx.result("Appsolutely perfect");
            };
        }
    }
    ```

3. Create a log4j2 configuration in the `src/main/resources/log4j2.xml` file. You might need to create that directory first.

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <Configuration>
      <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
          <PatternLayout pattern="%d{HH:mm:ss.SSS} [%-5level] %logger{36} %msg%n"/>
        </Console>
      </Appenders>
      <Loggers>
        <Logger name="de.spinscale.javalin.App" level="INFO"/>
        <Root level="ERROR">
          <AppenderRef ref="Console" />
        </Root>
      </Loggers>
    </Configuration>
    ```

    By default, this logs on the `ERROR` level. For the `App` class, there is an additional configuration so that all `INFO` logs are also logged. After repackaging and restarting, the log messages are displayed in the terminal.

    ```text
    17:17:40.019 [INFO ] de.spinscale.javalin.App - This is an informative logging message, user agent [curl/7.64.1]
    ```

### Log requests [_log_requests]

Depending on the application traffic and whether it happens outside of the application, it makes sense to log each request on the application level.

1. In the `App.java` file, edit the `App` class.

    ```java
    public class App {

        private static final Logger logger = LoggerFactory.getLogger(App.class);

        public static void main(String[] args) {
            Javalin app = Javalin.create(config -> {
                config.requestLogger((ctx, executionTimeMs) -> {
                    logger.info("{} {} {} {} \"{}\" {}",
                            ctx.method(),  ctx.url(), ctx.req.getRemoteHost(),
                            ctx.res.getStatus(), ctx.userAgent(), executionTimeMs.longValue());
               });
            });
            app.get("/", mainHandler());
            app.start(7000);
        }

        static Handler mainHandler() {
            return ctx -> {
                logger.info("This is an informative logging message, user agent [{}]", ctx.userAgent());
                ctx.result("Appsolutely perfect");
            };
        }
    }
    ```

2. Rebuild and restart the application. The log messages are logged for each request.

    ```text
    10:43:50.066 [INFO ] de.spinscale.javalin.App - GET / 200 0:0:0:0:0:0:0:1 "curl/7.64.1" 7
    ```

### Create an ISO8601 timestamp [_create_an_iso8601_timestamp]

Before ingesting logs into {{ech}}, create an ISO8601 timestamp by editing the `log4j2.xml` file.

::::{note}
Creating an ISO8601 timestamp removes the need to do any calculation for timestamps when ingesting logs, as this is a unique point in time, including the timezone. Having a timezone becomes more important once you are running across data centers while trying to follow data streams.

::::

```text
<PatternLayout pattern="%d{ISO8601_OFFSET_DATE_TIME_HHCMM} [%-5level] %logger{36} %msg%n"/>
```

The log entries are ingested containing timestamps like the following.

```text
2020-07-03T14:25:40,378+02:00 [INFO ] de.spinscale.javalin.App GET / 200 0:0:0:0:0:0:0:1 "curl/7.64.1" 0
```

### Log to a file and stdout [_log_to_a_file_and_stdout]

1. To read the logging output, let’s write data into a file and to stdout. This is a new `log4j2.xml` file.

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <Configuration>
      <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
          <PatternLayout pattern="%highlight{%d{ISO8601_OFFSET_DATE_TIME_HHCMM} [%-5level] %logger{36} %msg%n}"/>
        </Console>
        <File name="JavalinAppLog" fileName="/tmp/javalin/app.log">
          <PatternLayout pattern="%d{ISO8601_OFFSET_DATE_TIME_HHCMM} [%-5level] %logger{36} %msg%n"/>
        </File>
      </Appenders>
      <Loggers>
        <Logger name="de.spinscale.javalin.App" level="INFO"/>
        <Root level="ERROR">
          <AppenderRef ref="Console" />
          <AppenderRef ref="JavalinAppLog" />
        </Root>
      </Loggers>
    </Configuration>
    ```

2. Restart the application and send a request. The logs will be sent to `/tmp/javalin/app.log`.

### Install and configure {{filebeat}} [_install_and_configure_filebeat]

To read the log file and send it to {{es}}, {{filebeat}} is required. To download and install {{filebeat}}, use the commands that work with your system:

:::::::{tab-set}

::::::{tab-item} DEB
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-{{version.stack}}-amd64.deb
sudo dpkg -i filebeat-{{version.stack}}-amd64.deb
```
::::::

::::::{tab-item} RPM
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-{{version.stack}}-x86_64.rpm
sudo rpm -vi filebeat-{{version.stack}}-x86_64.rpm
```
::::::

::::::{tab-item} MacOS
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-{{version.stack}}-darwin-x86_64.tar.gz
tar xzvf filebeat-{{version.stack}}-darwin-x86_64.tar.gz
```
::::::

::::::{tab-item} Linux
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-{{version.stack}}-linux-x86_64.tar.gz
tar xzvf filebeat-{{version.stack}}-linux-x86_64.tar.gz
```
::::::

::::::{tab-item} Windows
1. Download the [Filebeat Windows zip file](https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-{{version.stack}}-windows-x86_64.zip).

2. Extract the contents of the zip file into `C:\Program Files`.

3. Rename the `filebeat-[version]-windows-x86_64` directory to `Filebeat`.

4. Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select *Run As Administrator*).

5. From the PowerShell prompt, run the following commands to install Filebeat as a Windows service:

```shell subs=true
PS > cd 'C:\Program Files\Filebeat'
PS C:\Program Files\Filebeat> .\install-service-filebeat.ps1
```

```{note}
If script execution is disabled on your system, you need to set the execution policy for the current session to allow the script to run. For example: `PowerShell.exe -ExecutionPolicy UnRestricted -File .\install-service-filebeat.ps1`.
```
::::::

:::::::
1. Use the {{filebeat}} keystore to store [secure settings](beats://reference/filebeat/keystore.md). Let’s store the Cloud ID in the keystore.

    ::::{note}
    Substitute the Cloud ID from your deployment in the following command.  To find your Cloud ID Click on your deployment in [https://cloud.elastic.co/deployments](https://cloud.elastic.co/deployments)

    ::::

    ```bash
    ./filebeat keystore create
    echo -n "<Your Cloud ID>" | ./filebeat keystore add CLOUD_ID --stdin
    ```

    To store logs in {{es}} with minimal permissions, create an API key to send data from {{filebeat}} to {{ecloud}}.

2. Log into {{kib}} user (you can do so from the Cloud Console without typing in any permissions) and select **Management** → **{{dev-tools-app}}**. Send the following request:

    ```console
    POST /_security/api_key
    {
      "name": "filebeat_javalin-app",
      "role_descriptors": {
        "filebeat_writer": {
          "cluster": ["monitor", "read_ilm"],
          "index": [
            {
              "names": ["filebeat-*"],
              "privileges": ["view_index_metadata", "create_doc"]
            }
          ]
        }
      }
    }
    ```

    The response contains an `api_key` and an `id` field, which can be stored in the {{filebeat}} keystore in the following format: `id:api_key`.

    ```bash
    echo -n "IhrJJHMB4JmIUAPLuM35:1GbfxhkMT8COBB4JWY3pvQ" | ./filebeat keystore add ES_API_KEY --stdin
    ```

    ::::{note}
    Make sure you specify the `-n` parameter; otherwise, you will have painful debugging sessions, because of adding a newline at the end of your API key.

    ::::

    To see if both settings have been stored, run `./filebeat keystore list`.

3. To load the {{filebeat}} dashboards, use the `elastic` super user.

    ```bash
    ./filebeat setup -e -E 'cloud.id=${CLOUD_ID}' -E 'cloud.auth=elastic:YOUR_SUPER_SECRET_PASS'
    ```

    ::::{tip}
    If you prefer not to store credentials in your shell’s `.history` file, add a space at the beginning of the line. Depending on the shell configuration, these commands are not added to the history.

    ::::

4. Configure {{filebeat}}, so it knows where to read data from and where to send it to. Create a `filebeat.yml` file.

    ```yaml
    name: javalin-app-shipper

    filebeat.inputs:
    - type: log
      paths:
        - /tmp/javalin/*.log

    cloud.id: ${CLOUD_ID}
    output.elasticsearch:
      api_key: ${ES_API_KEY}
    ```

### Send data to {{es}} [_send_data_to_es]

To send data to {{es}}, start {{filebeat}}.

:::::::{tab-set}

::::::{tab-item} DEB
```sh
sudo service filebeat start
```

::::{note}
If you use an `init.d` script to start Filebeat, you can’t specify command line flags (see [Command reference](beats://reference/filebeat/command-line-options.md)). To specify flags, start Filebeat in the foreground.
::::

Also see [Filebeat and systemd](beats://reference/filebeat/running-with-systemd.md).
::::::

::::::{tab-item} RPM
```sh
sudo service filebeat start
```

::::{note}
If you use an `init.d` script to start Filebeat, you can’t specify command line flags (see [Command reference](beats://reference/filebeat/command-line-options.md)). To specify flags, start Filebeat in the foreground.
::::

Also see [Filebeat and systemd](beats://reference/filebeat/running-with-systemd.md).
::::::

::::::{tab-item} MacOS
```sh
./filebeat -e
```
::::::

::::::{tab-item} Linux
```sh
./filebeat -e
```
::::::

::::::{tab-item} Windows
```sh
PS C:\Program Files\filebeat> Start-Service filebeat
```

By default, Windows log files are stored in `C:\ProgramData\filebeat\Logs`.
::::::

:::::::
In the log output, you should see the following line.

```text
2020-07-03T15:41:56.532+0200    INFO    log/harvester.go:297    Harvester started for file: /tmp/javalin/app.log
```

Let’s create some log entries for the application. You can use a tool like [wrk](https://github.com/wg/wrk) and run the following command to send requests to the application.

```bash
wrk -t1 -c 100 -d10s http://localhost:7000
```

This command results in roughly 8,000 requests per second, and the equivalent number of log lines are also written.

## Step 3: View logs in {{kib}} [_step_3_view_logs_in_kib]

1. Log into {{kib}} and select the **Discover** app.

    There is a summary of the documents at the top, but let’s take a look at a single document.

    ![{{kib}} single document view](/solutions/images/observability-monitor-java-app-kibana-single-document.png "")

    You can see that a lot more data is indexed than just the event. There is information about the offset in the file, information about the component shipping the logs, the name of the shipper’s name in the output, and there is a `message` field containing log line contents.

    You can see there is a flaw in the request logging. If the user agent is `null`, something other than `null` is returned. Reading our logs is crucial; however, just indexing them gains us nothing.  To fix this, here is a new request logger.

    ```java
    Javalin app = Javalin.create(config -> {
        config.requestLogger((ctx, executionTimeMs) -> {
            String userAgent = ctx.userAgent() != null ? ctx.userAgent() : "-";
            logger.info("{} {} {} {} \"{}\" {}",
                    ctx.method(), ctx.req.getPathInfo(), ctx.res.getStatus(),
                    ctx.req.getRemoteHost(), userAgent, executionTimeMs.longValue());
        });
    });
    ```

    You may also want to fix this in the logging message in the main handler.

    ```java
    static Handler mainHandler() {
        return ctx -> {
            String userAgent = ctx.userAgent() != null ? ctx.userAgent() : "-";
            logger.info("This is an informative logging message, user agent [{}]", userAgent);
            ctx.result("Appsolutely perfect");
        };
    }
    ```

2. Now let’s have a look at the {{logs-app}} in {{kib}}. Select **{{observability}}** → **Logs**.

    If you want to see the streaming feature at work, run the following curl request in a loop while sleeping.

    ```bash
    while $(sleep 0.7) ; do curl localhost:7000 ; done
    ```

3. To view a continuous stream of log messages, click **Stream live**. You can also highlight specific terms, as shown here.

    ![{{kib}} Logs UI Streaming](/solutions/images/observability-monitor-java-app-kibana-streaming.png "")

    Looking at one of the documents being indexed, you can see that the log message is contained in a single field. Verify this by looking at one of those documents.

    ```console
    GET filebeat-*/_search
    {
      "size": 1
    }
    ```

    Things to note:

    * When you compare the `@timestamp` field with the timestamp of the log message, you will notice that it differs. This means that you don’t get the results you expect when filtering based on the `@timestamp` field. The current `@timestamp` field reflects the timestamp when the event was created within {{filebeat}}, not the timestamp of when the log event occurred in the application.
    * One cannot filter on specific fields like the HTTP verb, the HTTP status code, the log level or the class that generated the log message

## Step 4: Work with your logs [_step_4_work_with_your_logs]

### Structure logs [_structure_logs]

To extract more data from a single log line into several fields requires additional structuring of the logs.

Let’s take another look at a log message generated by our app.

```text
2020-07-03T15:45:01,479+02:00 [INFO ] de.spinscale.javalin.App This is an informative logging message
```

This message has four parts: `timestamp`, `log level`, `class`, and `message`. The rules of splitting are apparent as well, as most of them involve whitespace.

The good news is that all {{beats}} can process a log line before sending it to {{es}} by using [processors](beats://reference/filebeat/filtering-enhancing-data.md). If the capabilities of these processors are not enough, you can always let {{es}} do the heavy lifting by using [an ingest node](/manage-data/ingest/transform-enrich/ingest-pipelines.md). This is what many modules in {{filebeat}} do. A module in {{filebeat}} is a way to parse a specific log file format for a particular software.

Let’s try this by using a couple of processors and only a {{filebeat}} configuration.

```yaml
processors:
  - add_host_metadata: ~
  - dissect:
      tokenizer: '%{timestamp} [%{log.level}] %{log.logger} %{message_content}'
      field: "message"
      target_prefix: ""
  - timestamp:
      field: "timestamp"
      layouts:
        - '2006-01-02T15:04:05.999Z0700'
      test:
        - '2020-07-18T04:59:51.123+0200'
  - drop_fields:
      fields: [ "message", "timestamp" ]
  - rename:
      fields:
        - from: "message_content"
        - to: "message"
```

The `dissect` processor splits the log message into four parts. If you want to have the last part of the original message in the `message` field, you need to remove the old `message` field first and then rename the field. There is no in-place replacement with the dissect filter.

There is also a dedicated timestamp parsing so that the `@timestamp` field contains a parsed value. Drop the duplicated fields, but ensure that a part of the original message is still available in the `message` field.

::::{important}
The removal of parts of the original message is debatable. Keeping the original message around makes a lot of sense to me. With the above example, debugging might become problematic if parsing the timestamp does not work as expected.

::::

There is also a slight difference in the parsing of a timestamp as the go time parser only accepts dots as a separator between seconds and milliseconds. Still, our default output of the log4j2 is using a comma.

Either one can fix the timestamp in the logging output to look like one expected from {{filebeat}}. This results in the following pattern layout.

```xml
  <PatternLayout pattern="%d{yyyy-MM-dd'T'HH:mm:ss.SSSZ} [%-5level] %logger{36} %msg%n"/>
```

Fixing the timestamp parsing is another way, as you do not always have full control over your logs and change their format. Imagine using some third-party software. For now, this will be good enough.

Restart {{filebeat}} after the change, and look at what changed in an indexed JSON document by running this search (and having another log message indexed).

```console
GET filebeat-*/_search?filter_path=**._source
{
  "size": 1,
  "_source": {
    "excludes": [
      "host.ip",
      "host.mac"
    ]
  },
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ]
}
```

This returns a document like this.

```console-response
{
  "hits" : {
    "hits" : [
      {
        "_source" : {
          "input" : {
            "type" : "log"
          },
          "agent" : {
            "hostname" : "rhincodon",
            "name" : "javalin-app-shipper",
            "id" : "95705f0c-b472-4bcc-8b01-2d387c0d309b",
            "type" : "filebeat",
            "ephemeral_id" : "e4df883f-6073-4a90-a4c4-9e116704f871",
            "version" : "7.9.0"
          },
          "@timestamp" : "2020-07-03T15:11:51.925Z",
          "ecs" : {
            "version" : "1.5.0"
          },
          "log" : {
            "file" : {
              "path" : "/tmp/javalin/app.log"
            },
            "offset" : 1440,
            "level" : "ERROR",
            "logger" : "de.spinscale.javalin.App"
          },
          "host" : {
            "hostname" : "rhincodon",
            "os" : {
              "build" : "19F101",
              "kernel" : "19.5.0",
              "name" : "Mac OS X",
              "family" : "darwin",
              "version" : "10.15.5",
              "platform" : "darwin"
            },
            "name" : "javalin-app-shipper",
            "id" : "C28736BF-0EB3-5A04-BE85-C27A62C99316",
            "architecture" : "x86_64"
          },
          "message" : "This is an informative logging message, user agent [curl/7.64.1]"
        }
      }
    ]
  }
}
```

You can see that the `message` field only contains the last part of our log message. Also, there is a `log.level` and `log.logger` field.

When the log level is `INFO`, it is logged with additional space at the end. You could use a [script processor](beats://reference/filebeat/processor-script.md) and call `trim()`. However, it might be easier to fix our logging configuration to not always emit 5 characters, regardless of the log level length. You can still keep this when writing to standard out.

```xml
<File name="JavalinAppLog" fileName="/tmp/javalin/app.log">
  <PatternLayout pattern="%d{yyyy-MM-dd'T'HH:mm:ss.SSSZ} [%level] %logger{36} %msg%n"/>
</File>
```

### Parse exceptions [_parse_exceptions]

Exceptions are a special treat in the case of logging. They span multiple lines, so the old rule of one message per line does not exist in exceptions.

Add an endpoint in `App.java` that triggers an exception first and make sure it is logged by using an exception mapper.

```java
app.get("/exception", ctx -> {
    throw new IllegalArgumentException("not yet implemented");
});

app.exception(Exception.class, (e, ctx) -> {
    logger.error("Exception found", e);
    ctx.status(500).result(e.getMessage());
});
```

Calling `/exception` returns an HTTP 500 error to the client, but it leaves a stack trace in the logs like this.

```text
2020-07-06T11:27:29,491+02:00 [ERROR] de.spinscale.javalin.App Exception found
java.lang.IllegalArgumentException: not yet implemented
    at de.spinscale.javalin.App.lambda$main$2(App.java:24) ~[classes/:?]
    at io.javalin.core.security.SecurityUtil.noopAccessManager(SecurityUtil.kt:23) ~[javalin-3.10.1.jar:?]
    at io.javalin.http.JavalinServlet$addHandler$protectedHandler$1.handle(JavalinServlet.kt:119) ~[javalin-3.10.1.jar:?]
    at io.javalin.http.JavalinServlet$service$2$1.invoke(JavalinServlet.kt:45) ~[javalin-3.10.1.jar:?]
    at io.javalin.http.JavalinServlet$service$2$1.invoke(JavalinServlet.kt:24) ~[javalin-3.10.1.jar:?]

  ... goes on and on and on and own ...
```

There is one attribute that helps to parse this stack trace. It seems different compared to a regular log message. Each new line starts with whitespace, thus different from a log message beginning with the date. Let’s add this logic to our {{beats}} configuration.

```yaml
- type: log
  enabled: true
  paths:
    - /tmp/javalin/*.log
  multiline.pattern: ^20
  multiline.negate: true
  multiline.match: after
```

So the verbatim translation of the above settings says to treat everything as part of an existing message, that is not starting with `20` in a line. The `20` resembles the beginning year of your timestamps. Some users prefer to wrap the date in `[]` to make this easier to understand.

::::{note}
This introduces state into your logging. You cannot split a log file among several processors now, as every log line could still be belonging to the current event. This is not a bad thing, but again something to be aware of.

::::

After restarting {{filebeat}} and your Javalin app, trigger an exception, and you will see a long stack trace in the `message` field of your logs.

### Configure log rotation [_configure_log_rotation]

To ensure that logs don’t grow infinitely, let’s add some log rotation to your logging configuration.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration>
  <Appenders>
    <Console name="Console" target="SYSTEM_OUT">
      <PatternLayout pattern="%highlight{%d{ISO8601_OFFSET_DATE_TIME_HHCMM} [%-5level] %logger{36} %msg%n}"/>
    </Console>

    <RollingFile name="JavalinAppLogRolling" fileName="/tmp/javalin/app.log" filePattern="/tmp/javalin/%d{yyyy-MM-dd}-%i.log.gz">
      <PatternLayout pattern="%d{yyyy-MM-dd'T'HH:mm:ss.SSSZ} [%level] %logger{36} %msg%n"/>
      <Policies>
        <TimeBasedTriggeringPolicy />
        <SizeBasedTriggeringPolicy size="50 MB"/>
      </Policies>
      <DefaultRolloverStrategy max="20"/>
    </RollingFile>
  </Appenders>

  <Loggers>
    <Logger name="de.spinscale.javalin.App" level="INFO"/>
    <Root level="ERROR">
      <AppenderRef ref="Console" />
      <AppenderRef ref="JavalinAppLogRolling" />
    </Root>
  </Loggers>
</Configuration>
```

The sample added a `JavalinAppLogRolling` appender to our configuration that uses the same logging pattern as before, but rolls over if a new day starts or if the log file has reached 50 megabytes.

If a new log file is created, older log files are gzipped as well to take less space on disk. The size of 50 megabytes refers to the unpacked file size, so the potentially twenty files on disk will be much smaller each.

### Ingest node [_ingest_node]

The built-in modules are almost entirely using the [Ingest node](/manage-data/ingest/transform-enrich/ingest-pipelines.md) feature of {{es}} instead of the {{beats}} processors.

One of the most helpful parts of the ingest pipeline is the ability to debug by using the [Simulate Pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-simulate).

1. Let’s write a pipeline that is similar to our {{filebeat}} processors using the {{dev-tools-app}} panel in {{kib}}, run the following:

    ```console
    # Store the pipeline in Elasticsearch
    PUT _ingest/pipeline/javalin_pipeline
    {
      "processors": [
        {
          "dissect": {
            "field": "message",
            "pattern": "%{@timestamp} [%{log.level}] %{log.logger} %{message}"
          }
        },
        {
          "trim": {
            "field": "log.level"
          }
        },
        {
          "date": {
            "field": "@timestamp",
            "formats": [
              "ISO8601"
            ]
          }
        }
      ]
    }

    # Test the pipeline
    POST _ingest/pipeline/javalin_pipeline/_simulate
    {
      "docs": [
        {
          "_source": {
            "message": "2020-07-06T13:39:51,737+02:00 [INFO ] de.spinscale.javalin.App This is an informative logging message"
          }
        }
      ]
    }
    ```

    You can see the pipeline’s created fields in the output, which now looks like the earlier {{filebeat}} processors. As the ingest pipeline works on a document level, you still need to check for exceptions where the logs are generated and let {{filebeat}} create a single message out of that. You could even implement the log level trimming with a single processor, and date parsing was also pretty easy, as the {{es}} ISO8601 parser correctly identifies a comma instead of a dot when splitting seconds and milliseconds.

2. Now, on to the {{filebeat}} configuration. First, let’s remove all the processors, except the [add_host_metadata processor](beats://reference/filebeat/add-host-metadata.md), to add some host information like the host name and operating system.

    ```yaml
    processors:
      - add_host_metadata: ~
    ```

3. Edit the {{es}} output to ensure the pipeline will be referred to when a document is indexed from {{filebeat}}.

    ```yaml
    cloud.id: ${CLOUD_ID}
    output.elasticsearch:
      api_key: ${ES_API_KEY}
      pipeline: javalin_pipeline
    ```

4. Restart {{filebeat}} and see if logs are flowing in as expected.

### Write logs as JSON [_write_logs_as_json]

You have now learned about parsing logs in either {{beats}} or {{es}}. What if we didn’t need to think about parsing our logs and extract data manually?

Writing out logs as plain text works and is easy to read for humans. However, first writing them out as plain text, parsing them using the `dissect` processors, and then creating a JSON again sounds tedious and burns unneeded CPU cycles.

While log4j2 has a [JSONLayout](https://logging.apache.org/log4j/2.x/manual/layouts.html#JSONLayout), you can go further and use a Library called [ecs-logging-java](https://github.com/elastic/ecs-logging-java). The advantage of ECS logging is that it uses the [Elastic Common Schema](ecs://reference/index.md). ECS defines a standard set of fields used when storing event data in {{es}}, such as logs and metrics.

1. Instead of writing our logging standard, use an existing one. Let’s add the logging dependency to our Javalin application.

    ```gradle
    dependencies {
      implementation 'io.javalin:javalin:3.10.1'
      implementation 'org.apache.logging.log4j:log4j-slf4j18-impl:2.13.3'
      implementation 'co.elastic.logging:log4j2-ecs-layout:0.5.0'

      testImplementation 'org.mockito:mockito-core:3.5.10'
      testImplementation 'org.assertj:assertj-core:3.17.2'
      testImplementation 'org.junit.jupiter:junit-jupiter-api:5.6.2'
      testRuntimeOnly 'org.junit.jupiter:junit-jupiter-engine:5.6.2'
    }

    // this is needed to ensure JSON logging works as expected when building
    // a shadow jar
    shadowJar {
      transform(com.github.jengelman.gradle.plugins.shadow.transformers.Log4j2PluginsCacheFileTransformer)
    }
    ```

    The `log4j2-ecs-layout` ships with a custom `<EcsLayout>` which can be used in the logging setup for the rolling file appender

    ```xml
    <RollingFile name="JavalinAppLogRolling" fileName="/tmp/javalin/app.log" filePattern="/tmp/javalin/%d{yyyy-MM-dd}-%i.log.gz">
      <EcsLayout serviceName="my-javalin-app"/>
      <Policies>
        <TimeBasedTriggeringPolicy />
        <SizeBasedTriggeringPolicy size="50 MB"/>
      </Policies>
      <DefaultRolloverStrategy max="20"/>
    </RollingFile>
    ```

    When you restart your app, you will see pure JSON written to your log file. When you trigger an exception, you will see, that the stack trace is already within your single document. This means the {{filebeat}} configuration can become stateless and even more lightweight. Also, the ingest pipeline on the {{es}} side can be deleted again.

2. You can configure a few [more parameters](https://github.com/elastic/ecs-logging-java/tree/main/log4j2-ecs-layout) for the `EcsLayout`, but the defaults have been selected wisely. Let’s fix the {{filebeat}} configuration and remove the multiline setup along with pipeline:

    ```yaml
    filebeat.inputs:
    - type: log
      enabled: true
      paths:
        - /tmp/javalin/*.log
      json.keys_under_root: true

    name: javalin-app-shipper

    cloud.id: ${CLOUD_ID}
    output.elasticsearch:
      api_key: ${ES_API_KEY}

    # ================================= Processors =================================
    processors:
      - add_host_metadata: ~
    ```

    As you can see, just by writing out logs as JSON, our whole logging setup got a ton easier, so whenever possible, try to directly write your logs as JSON.

## Step 5: Ingest metrics [_step_5_ingest_metrics]

A metric is considered a point in time value that can change anytime. The number of current requests can change any millisecond. You could have a spike of 1000 requests, and then everything goes back to one request. This also means that these kinds of metrics may not be accurate, and you also want to pull min/max values to get some more indication. Furthermore, this implies that you need to think about the duration of those metrics as well. Do you need those once per minute or every 10 seconds?

To get a different angled view of your application, let’s ingest some metrics. In this example, we will use the [Metricbeat Prometheus Module](beats://reference/metricbeat/metricbeat-module-prometheus.md) to send data to {{es}}.

The underlying library used in our app is [micrometer.io](http://micrometer.io/), a vendor-neutral application metrics facade in combination with its [Prometheus support](http://micrometer.io/docs/registry/prometheus) to implement a pull-based model. You could use the [elastic support](http://micrometer.io/docs/registry/elastic) to achieve a push-based model. This would require users to store credential data of the {{es}} cluster in our app. This example keeps this data in the surrounding tools.

### Add metrics to the application [_add_metrics_to_the_application]

1. Add the dependencies to our `build.gradle` file.

    ```gradle
      // metrics via micrometer
      implementation 'io.micrometer:micrometer-core:1.5.4'
      implementation 'io.micrometer:micrometer-registry-prometheus:1.5.4'
      implementation 'org.apache.commons:commons-lang3:3.11'
    ```

2. Add the micrometer plugin and its corresponding import to our Javalin app.

    ```java
    ...
    import io.javalin.plugin.metrics.MicrometerPlugin;
    import io.javalin.core.security.BasicAuthCredentials;
    ...

    Javalin app = Javalin.create(config -> {
       ...
       config.registerPlugin(new MicrometerPlugin());
    );
    ```

3. Add a new metrics endpoint and ensure the `BasicAuthCredentials` class is imported as well.

    ```java
    final Micrometer micrometer = new Micrometer();
    app.get("/metrics", ctx -> {
      ctx.status(404);
      if (ctx.basicAuthCredentialsExist()) {
        final BasicAuthCredentials credentials = ctx.basicAuthCredentials();
        if ("metrics".equals(credentials.getUsername()) && "secret".equals(credentials.getPassword())) {
          ctx.status(200).result(micrometer.scrape());
        }
      }
    });
    ```

    Here, the `MicroMeter` class is a self-written class named `MicroMeter.java` that sets up a couple of metrics monitors and creates the registry for Prometheus, which provides the text-based Prometheus output.

    ```java
    package de.spinscale.javalin;

    import io.micrometer.core.instrument.Metrics;
    import io.micrometer.core.instrument.binder.jvm.JvmCompilationMetrics;
    import io.micrometer.core.instrument.binder.jvm.JvmGcMetrics;
    import io.micrometer.core.instrument.binder.jvm.JvmHeapPressureMetrics;
    import io.micrometer.core.instrument.binder.jvm.JvmMemoryMetrics;
    import io.micrometer.core.instrument.binder.jvm.JvmThreadMetrics;
    import io.micrometer.core.instrument.binder.logging.Log4j2Metrics;
    import io.micrometer.core.instrument.binder.system.FileDescriptorMetrics;
    import io.micrometer.core.instrument.binder.system.ProcessorMetrics;
    import io.micrometer.core.instrument.binder.system.UptimeMetrics;
    import io.micrometer.prometheus.PrometheusConfig;
    import io.micrometer.prometheus.PrometheusMeterRegistry;

    public class Micrometer {

        final PrometheusMeterRegistry registry = new PrometheusMeterRegistry(new PrometheusConfig() {
            @Override
            public String get(String key) {
                return null;
            }

            @Override
            public String prefix() {
                return "javalin";
            }
        });

        public Micrometer() {
            Metrics.addRegistry(registry);
            new JvmGcMetrics().bindTo(Metrics.globalRegistry);
            new JvmHeapPressureMetrics().bindTo(Metrics.globalRegistry);
            new JvmThreadMetrics().bindTo(Metrics.globalRegistry);
            new JvmCompilationMetrics().bindTo(Metrics.globalRegistry);
            new JvmMemoryMetrics().bindTo(Metrics.globalRegistry);
            new Log4j2Metrics().bindTo(Metrics.globalRegistry);
            new UptimeMetrics().bindTo(Metrics.globalRegistry);
            new FileDescriptorMetrics().bindTo(Metrics.globalRegistry);
            new ProcessorMetrics().bindTo(Metrics.globalRegistry);
        }

        public String scrape() {
            return registry.scrape();
        }
    }
    ```

4. Rebuild your app and poll the metrics endpoint.

    ```bash
    curl localhost:7000/metrics -u metrics:secret
    ```

    This returns a line based response with one metric per line. This is the standard Prometheus format.

### Install and configure {{metricbeat}} [_install_and_configure_metricbeat]

To send metrics to {{es}}, {{metricbeat}} is required. To download and install {{metricbeat}}, use the commands that work with your system:

:::::::{tab-set}

::::::{tab-item} DEB
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-{{version.stack}}-amd64.deb
sudo dpkg -i metricbeat-{{version.stack}}-amd64.deb
```
::::::

::::::{tab-item} RPM
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-{{version.stack}}-x86_64.rpm
sudo rpm -vi metricbeat-{{version.stack}}-x86_64.rpm
```
::::::

::::::{tab-item} MacOS
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-{{version.stack}}-darwin-x86_64.tar.gz
tar xzvf metricbeat-{{version.stack}}-darwin-x86_64.tar.gz
```
::::::

::::::{tab-item} Linux
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-{{version.stack}}-linux-x86_64.tar.gz
tar xzvf metricbeat-{{version.stack}}-linux-x86_64.tar.gz
```
::::::

::::::{tab-item} Windows
1. Download the [Metricbeat Windows zip file](https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-{{version.stack}}-windows-x86_64.zip).

2. Extract the contents of the zip file into `C:\Program Files`.

3. Rename the `metricbeat-[version]-windows-x86_64` directory to `Metricbeat`.

4. Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select *Run As Administrator*).

5. From the PowerShell prompt, run the following commands to install Metricbeat as a Windows service:

  ```shell subs=true
  PS > cd 'C:\Program Files\Metricbeat'
  PS C:\Program Files\Metricbeat> .\install-service-metricbeat.ps1
  ```

```{note}
If script execution is disabled on your system, you need to set the execution policy for the current session to allow the script to run. For example: `PowerShell.exe -ExecutionPolicy UnRestricted -File .\install-service-metricbeat.ps1`.
```
::::::

:::::::
1. Similar to the {{filebeat}} setup, run the initial set up of all the dashboards using the admin user, and then use an API key.

    ```console
    POST /_security/api_key
    {
      "name": "metricbeat_javalin-app",
      "role_descriptors": {
        "metricbeat_writer": {
          "cluster": ["monitor", "read_ilm"],
          "index": [
            {
              "names": ["metricbeat-*"],
              "privileges": ["view_index_metadata", "create_doc"]
            }
          ]
        }
      }
    }
    ```

2. Store the combination of `id` and `api_key` fields in the keystore.

    ```bash
    ./metricbeat keystore create
    echo -n "IhrJJHMB4JmIUAPLuM35:1GbfxhkMT8COBB4JWY3pvQ" | ./metricbeat keystore add ES_API_KEY --stdin
    echo -n "observability-javalin-app:ZXUtY2VudHJhbC0xLmF3cy5jbG91ZC5lcy5pbyQ4NDU5M2I1YmQzYTY0N2NhYjA2MWQ3NTJhZWFhNWEzYyQzYmQwMWE2OTQ2MmQ0N2ExYjdhYTkwMzI0YjJiOTMyYQ==" | ./metricbeat keystore add CLOUD_ID --stdin
    ```

    Don’t forget to do the initial setup like this.

    ```bash
    ./metricbeat setup -e -E 'cloud.id=${CLOUD_ID}' -E 'cloud.auth=elastic:YOUR_SUPER_SECRET_PASS'
    ```

3. Configure {{metricbeat}} to read our Prometheus metrics. Start with a basic `metricbeat.yaml`.

    ```yaml
    metricbeat.config.modules:
      path: ${path.config}/modules.d/*.yml
      reload.enabled: false

    name: javalin-metrics-shipper

    cloud.id: ${CLOUD_ID}
    output.elasticsearch:
      api_key: ${ES_API_KEY}

    processors:
      - add_host_metadata: ~
      - add_cloud_metadata: ~
      - add_docker_metadata: ~
      - add_kubernetes_metadata: ~
    ```

    As {{metricbeat}} supports dozens of modules, which in turn are different ways of ingesting metrics (the same applies to {{filebeat}} with different types of log files and formats), the Prometheus module needs to be enabled.

    ```bash
    ./metricbeat modules enable prometheus
    ```

    Add the Prometheus endpoint to poll in `./modules.d/prometheus.yml`:

    ```yaml
    - module: prometheus
      period: 10s
      hosts: ["localhost:7000"]
      metrics_path: /metrics
      username: "metrics"
      password: "secret"
      use_types: true
      rate_counters: true
    ```

4. To improve security, you should add the username and the password to the keystore and refer to both in the configuration.
5. Start {{metricbeat}}.

:::::::{tab-set}

::::::{tab-item} DEB
```sh
sudo service metricbeat start
```

::::{note}
If you use an `init.d` script to start Metricbeat, you can’t specify command line flags (see [Command reference](beats://reference/metricbeat/command-line-options.md)). To specify flags, start Metricbeat in the foreground.
::::

Also see [Metricbeat and systemd](beats://reference/metricbeat/running-with-systemd.md).
::::::

::::::{tab-item} RPM
```sh
sudo service metricbeat start
```

::::{note}
If you use an `init.d` script to start Metricbeat, you can’t specify command line flags (see [Command reference](beats://reference/metricbeat/command-line-options.md)). To specify flags, start Metricbeat in the foreground.
::::

Also see [Metricbeat and systemd](beats://reference/metricbeat/running-with-systemd.md).
::::::

::::::{tab-item} MacOS
```sh
sudo chown root metricbeat.yml <1>
sudo ./metricbeat -e
```

1. You’ll be running Metricbeat as root, so you need to change ownership of the configuration file, or run Metricbeat with `--strict.perms=false` specified. See [Config File Ownership and Permissions](beats://reference/libbeat/config-file-permissions.md).
::::::

::::::{tab-item} Linux
```sh
sudo chown root metricbeat.yml <1>
sudo ./metricbeat -e
```

1. You’ll be running Metricbeat as root, so you need to change ownership of the configuration file, or run Metricbeat with `--strict.perms=false` specified. See [Config File Ownership and Permissions](beats://reference/libbeat/config-file-permissions.md).
::::::

::::::{tab-item} Windows
```sh
PS C:\Program Files\metricbeat> Start-Service metricbeat
```

By default, Windows log files are stored in `C:\ProgramData\metricbeat\Logs`.

::::{note}
On Windows, statistics about system load and swap usage are currently not captured
::::
::::::

:::::::
Verify that the Prometheus events are flowing into {{es}}.

```console
GET metricbeat-*/_search?filter_path=**.prometheus,hits.total
{
  "query": {
    "term": {
      "event.module": "prometheus"
    }
  }
}
```

## Step 6: View metrics in {{kib}} [_step_6_view_metrics_in_kib]

As this is custom data from our Javalin app, there is no predefined dashboard for displaying this data.

Let’s check for the number of logging messages per log level.

```console
GET metricbeat-*/_search
{
  "query": {
    "exists": {
      "field": "prometheus.log4j2_events_total.counter"
    }
  }
}
```

Visualize the number of log messages over time, split by the log level. Since the {{stack}} 7.7, there is a new way of creating a visualization called `Lens`.

1. Log into {{kib}} and select **Visualize** → **Create Visualization**.
2. Create a line chart and select `metricbeat-*` as the source.

    The basic idea is to have a [max aggregation](elasticsearch://reference/aggregations/search-aggregations-metrics-max-aggregation.md) on the y-axis on the `prometheus.log4j2_events_total.rate` field, whereas the x-axis, is split by date using a [date_histogram aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-datehistogram-aggregation.md) on the `@timestamp` field.

    There is one more split within each date histogram bucket, split by log level, using a [terms aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-terms-aggregation.md) on the `prometheus.labels.level`, which contains the log level. Also, increase the size of the log level to six to display every log level.

    The final result looks like this.

    ![Date Histogram of the log rate per log level](/solutions/images/observability-monitor-java-app-metrics-kibana-create-visualization-log-rate.png "")

### Visualize open files over time [_visualize_open_files_over_time]

The second visualization is to be a check for the number of open files in our application.

As no one can remember all the field names, let’s again look at the metrics output again first.

```bash
curl -s localhost:7000/metrics -u metrics:secret | grep ^process
process_files_max_files 10240.0
process_cpu_usage 1.8120711232436825E-4
process_uptime_seconds 72903.726
process_start_time_seconds 1.594048883317E9
process_files_open_files 61.0
```

Let’s look at the `process_files_open_files` metric. This should be a rather static value that rarely changes. If you run an application which stores data within the JVM or opens and closes network sockets, this metric increases and decreases depending on the load. With a web application, this is rather static. Let’s figure out why there are 60 files open on our small web application.

1. Run `jps` that will contain your App in the process list.

    ```bash
    $ jps
    14224 Jps
    82437 Launcher
    82438 App
    40895
    ```

2. Use `lsof` on that process.

    ```bash
    $ lsof -p 82438
    ```

    You will see more output than just all the files being opened, as a file is also a TCP connection happening right now.

3. Add an endpoint to increase the number of open files by having long-running HTTP connections (each connection is also considered an open file as it requires a file descriptor), and then run `wrk` against it.

    ```java
    ...
    import java.util.concurrent.CompletableFuture;
    import java.util.concurrent.Executor;
    import java.util.concurrent.TimeUnit;
    ...

    public static void main(String[] args) {
    ...
        final Executor executor = CompletableFuture.delayedExecutor(20, TimeUnit.SECONDS);
        app.get("/wait", ctx -> {
            CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "done", executor);
            ctx.result(future);
        });
    ...
    ```

    Every future gets delayed by 20 seconds, which means that a single HTTP request stays open for 20 seconds.

4. Let’s run a `wrk` workload.

    ```bash
    wrk -c 100 -t 20 -d 5m http://localhost:7000/wait
    ```

    Results show that only twenty requests were sent, which makes sense given the processing time.

    Now let’s build a visualization using [Lens](/explore-analyze/dashboards.md) in {{kib}}.

    ![Lens visualization](/solutions/images/observability-monitor-java-app-metrics-kibana-create-visualization-open-files.png "")

5. Below `Add filter`, select the `metricbeat-*` index pattern. This will likely use `filebeat-*` as the default.

    The x-axis uses the `@timestamp` field - which in turn will create a `date_histogram` aggregation again. The y-axis should not be the document count, as that one will always be stable, but the maximum value of the documents in the buckets. Click on the right of the field name on the y-axis and select `Max`. This gives you a similar visualization than shown, with a peak where you ran the `wrk` command above.

6. Now let’s have a look at the {{infrastructure-app}} in {{kib}}. Select **{{observability}}** → **Infrastructure**.

    You will only see data from a single shipper. Still, the moment you are running several services and the ability to group this per Kubernetes pod or host enables you to spot hosts with elevated CPU or memory consumption.

7. Click **Metrics Explorer**, you can start exploring your data for specific hosts or the CPU usage across your nodes.

    ![Metrics UI Log Counter](/solutions/images/observability-monitor-java-app-metrics-ui-prometheus-event-counter.png "")

    This is an area chart of the total events counter the Javalin app emits. It’s rising because there is a component polling an endpoint that, in turn, produces another log message. The steeper peek was due to sending more requests. But where is the sudden drop-off coming from? A JVM restart. As those metrics are not persisted, they reset on a JVM restart. With that in mind, it’s often better to log the `rate` instead of the `counter` field.

## Step 7: Instrument the application [_step_7_instrument_the_application]

The third piece of {{observability}} is Application Performance Management (APM). An APM setup consists of an APM server which accepts the data (and is already running within our {{ecloud}} setup) and an agent delivering the data to the server.

The agent has two tasks: instrumenting the Java application to extract application performance information and sending that data to the APM Server.

One of the APM’s core ideas is the ability to follow the flow of a user session across your whole stack, regardless of whether you have dozens of microservices or a monolith answering your user requests. This implies the ability to tag a request across your entire stack.

To fully capture user activity, you need to start in the browser of the user using Real User Monitoring (RUM) down to your application, which sends a SQL query to your database.

### Data Model [_data_model]

Despite a heavily fragmented APM landscape, the terminology often is similar. The two most important terms are **Spans** and **Transactions**.

A transaction encapsulates a series of spans, which contain information about the execution of a piece of code. Let’s take a look at this screenshot from the {{kib}} Applications UI.

![A transaction with spans](/solutions/images/observability-monitor-java-app-apm-transactions.png "")

This is a Spring Boot application. The `UserProfileController.showProfile()` method is called, which is marked as the transaction. There are two spans within. First, a request is sent to {{es}} using the {{es}} REST client, and after the response is rendered using Thymeleaf. The request to {{es}} is faster than the rendering in this case.

The Java {{apm-agent}} can instrument specific frameworks automatically. Spring and Spring Boot are supported well, and the above data was created by adding the agent to the Spring Boot application; there is no configuration necessary.

There are currently agents for Go, .NET, Node, Python, Ruby, and the browser (RUM). Agents keep getting added so you may want to check the [APM agent documentation](/reference/apm-agents/index.md).

### Add the {{apm-agent}} to your code [_add_the_apm_agent_to_your_code]

You have two options to add Java agent instrumentation to your application.

First, you can add the agent via a parameter when calling the `java` binary. This way, it does not interfere with the packaging of the application. This mechanism instruments the application when starting up.

First, download the agent, you can check [for the most recent version](https://search.maven.org/search?q=g:co.elastic.apm%20AND%20a:elastic-apm-agent).

```bash
wget https://repo1.maven.org/maven2/co/elastic/apm/elastic-apm-agent/1.17.0/elastic-apm-agent-1.17.0.jar
```

Specify the agent on startup as well as the configuration parameters of where to send the APM data to. Before starting the Java application, let’s get an API key for our APM server running in {{ecloud}}.

When you check your deployment in {{ecloud}} and click on `APM` on the left, you will see the `APM Server Secret Token`, which you can use. Also you can copy the APM endpoint URL from there.

```bash
java -javaagent:/path/to/elastic-apm-agent-1.17.0.jar\
  -Delastic.apm.service_name=javalin-app \
  -Delastic.apm.application_packages=de.spinscale.javalin \
  -Delastic.apm.server_urls=$APM_ENDPOINT_URL \
  -Delastic.apm.secret_token=PqWTHGtHZS2i0ZuBol \
  -jar build/libs/javalin-app-all.jar
```

You could now go ahead and open up the Applications UI and you should see the data flowing in.

### Automatic attachment [_automatic_attachment]

If you do not want to change the startup options of your application, the standalone agent allows you to attach to running JVMs on a host.

This requires you to download the standalone jar. You can find the link on the [official docs](apm-agent-java://reference/setup-attach-cli.md).

To list your locally running java application, you can run

```bash
java -jar /path/to/apm-agent-attach-1.17.0-standalone.jar --list
```

As I usually run more than a single java app on my system, I specify the application to attach to. Also, make sure, that you have stopped your Javalin application with the agent already attached and just start a regular Javalin app without the agent configured to attach.

```bash
java -jar /tmp/apm-agent-attach-1.17.0-standalone.jar --pid 30730 \
  --config service_name=javalin-app \
  --config application_packages=de.spinscale.javalin \
  --config server_urls=$APM_ENDPOINT_URL \
  --config secret_token=PqWTHGtHZS2i0ZuBol
```

This above message will return something like this:

```text
2020-07-10 15:04:48.144  INFO Attaching the Elastic APM agent to 30730
2020-07-10 15:04:49.649  INFO Done
```

So now the agent was attached to a running application with a special configuration.

While both of the first two possibilities work, you can also use the third one: using the {{apm-agent}} as a direct dependency. This allows you to write custom spans and transactions within our application.

### Programmatic setup [_programmatic_setup]

A programmatic setup allows you to attach the agent via a line of java in your source code.

1. Add the java agent dependency.

    ```gradle
    dependencies {
      ...
      implementation 'co.elastic.apm:apm-agent-attach:1.17.0'
      ...
    }
    ```

2. Instrument the application right at the start in our `main()` method.

    ```java
    import co.elastic.apm.attach.ElasticApmAttacher;

    ...

    public static void main(String[] args) {
        ElasticApmAttacher.attach();
        ...
    }
    ```

    We did not configure any endpoint or API tokens yet. While the [documentation](apm-agent-java://reference/setup-attach-api.md#setup-attach-api-configuration) recommends using the `src/main/resources/elasticapm.properties` file, I prefer the use of environment variables, as this prevents either committing API tokens to your source or merging another repository. Mechanisms like [vault](https://www.vaultproject.io/) allow you to manage your secrets in such a way.

    For our local deployment, I usually use something like [direnv](https://direnv.net/) for local setup. `direnv` is an extension for your local shell that loads/unloads environment variables when you enter a directory, like your application. `direnv` can do quite a bit more like loading the right node/ruby version or adding a directory to your $PATH variable.

3. To enable `direnv`, you need to create a `.envrc` file with this.

    ```text
    dotenv
    ```

    This tells `direnv` to load the contents of the `.env` file as environment variables. The `.env` file should look like this:

    ```bash
    ELASTIC_APM_SERVICE_NAME=javalin-app
    ELASTIC_APM_SERVER_URLS=https://APM_ENDPOINT_URL
    ELASTIC_APM_SECRET_TOKEN=PqWTHGtHZS2i0ZuBol
    ```

    If you are not comfortable with putting sensitive data in that `.env` file, you can use tools like [envchain](https://github.com/sorah/envchain) or call arbitrary commands in the `.envrc` file like accessing Vault.

4. You can now run the java application as you did before.

    ```bash
    java -jar build/libs/javalin-app-all.jar
    ```

    If you want to run this in your IDE, you can either set the environment variables manually or search for a plugin that supports `.env` files.

    Wait a few minutes and let’s finally take a look at the Applications UI.

    ![Javalin App Applications UI](/solutions/images/observability-monitor-java-app-apm-ui-javalin-app.png "")

    As you can see, this is quite the difference to the Spring Boot application shown earlier. The different endpoints are not listed; we can see the requests per minute though including errors.

    The only transaction comes from a single servlet, which is not too helpful. Let’s try to fix this by introducing custom programmatic transactions.

### Custom transactions [_custom_transactions]

1. Add another dependency.

    ```gradle
    dependencies {
      ...
      implementation 'co.elastic.apm:apm-agent-attach:1.17.0'
      implementation 'co.elastic.apm:apm-agent-api:1.17.0'
      ...
    }
    ```

2. Fix the name of the transactions to include the HTTP method and the request path

    ```java
    app.before(ctx -> ElasticApm.currentTransaction()
      .setName(ctx.method() + " " + ctx.path()));
    ```

3. Restart your app and see data flowing in. Test a few different endpoints, especially the one that throws exceptions and the one that triggers a 404.

    ![Applications UI with correct transaction names](/solutions/images/observability-monitor-java-app-apm-ui-javalin-with-transaction-names.png "")

    This looks much better, having differences between endpoints.

4. Add another endpoint to see the power of transactions, which polls another HTTP service. You may have heard of [wttr.in](https://wttr.in/), a service to poll weather information from. Let’s implement a proxy HTTP method that forwards the request to that endpoint. Let’s use [Apache HTTP client](https://hc.apache.org/httpcomponents-client-4.5.x/quickstart.html), one of the most typical HTTP clients out there.

    ```gradle
    implementation 'org.apache.httpcomponents:fluent-hc:4.5.12'
    ```

    This is our new endpoint.

    ```java
    import org.apache.http.client.fluent.Request;

    ...

    public static void main(String[] args) {
    ...

        app.get("/weather/:city", ctx -> {
            String city = ctx.pathParam("city");
            ctx.result(Request.Get("https://wttr.in/" + city + "?format=3").execute()
                .returnContent().asBytes())
                .contentType("text/plain; charset=utf-8");
        });

    ...
    ```

5. Curl `http://localhost:7000/weather/Munich` and see a one-line response about the current weather. Let’s check the APM UI.

    In the overview, you can see that most time is spent in the HTTP client, which is not surprising.

    ![Overview](/solutions/images/observability-monitor-java-app-apm-ui-javalin-wttr-1.png "")

    Our transactions for the `/weather/Munich` now contain a span, showing how much time is spent on retrieving the weather data. Because the HTTP client is instrumented automatically, there is no need to do anything.

    ![Transaction with span](/solutions/images/observability-monitor-java-app-apm-ui-javalin-wttr-2.png "")

    If the `city` parameter if that URL is of high cardinality, this will result in a high amount of URLs mentioned instead of the generic endpoint. If you would like to prevent this, a possibility would be to use `ctx.matchedPath()` to log every call to the weather API as `GET /weather/:city`. This however requires some refactoring by removing the `app.before()` handler and replacing it with a `app.after()` handler.

    ```java
    app.after(ctx -> ElasticApm.currentTransaction().setName(ctx.method()
      + " " + ctx.endpointHandlerPath()));
    ```

### Method tracing via agent configuration [_method_tracing_via_agent_configuration]

Instead of writing code to trace methods, you can also configure the agent to do this. Let’s try to figure out if logging is a bottleneck for our application and trace the request logger statements we added earlier.

The agent can [trace methods](apm-agent-java://reference/config-core.md#config-trace-methods) based on their signature.

The interface to monitor would be the `io.javalin.http.RequestLogger` interface with the `handle` method. So let’s try `io.javalin.http.RequestLogger#handle` to identify the method to log and put this in your `.env`.

```bash
ELASTIC_APM_TRACE_METHODS="de.spinscale.javalin.Log4j2RequestLogger#handle"
```

1. Create a dedicated logger class as well to match the above trace method.

    ```java
    package de.spinscale.javalin;

    import io.javalin.http.Context;
    import io.javalin.http.RequestLogger;
    import org.jetbrains.annotations.NotNull;
    import org.slf4j.Logger;
    import org.slf4j.LoggerFactory;

    public class Log4j2RequestLogger implements RequestLogger  {

        private final Logger logger = LoggerFactory.getLogger(Log4j2RequestLogger.class);

        @Override
        public void handle(@NotNull Context ctx, @NotNull Float executionTimeMs) throws Exception {
            String userAgent = ctx.userAgent() != null ? ctx.userAgent() : "-";
            logger.info("{} {} {} {} \"{}\" {}",
                    ctx.method(), ctx.req.getPathInfo(), ctx.res.getStatus(),
                    ctx.req.getRemoteHost(), userAgent, executionTimeMs.longValue());
        }
    }
    ```

2. Fix the call in our `App` class.

    ```java
    config.requestLogger(new Log4j2RequestLogger());
    ```

3. Restart your app, and see how much time your logging takes.

    ![Logging caller trace](/solutions/images/observability-monitor-java-app-apm-ui-logging-trace.png "")

    The request logger takes roughly 400 microseconds. The whole request takes about 1.3 milliseconds. Approximately a third of the processing of our request goes into logging.

    If you are on the quest for a faster service, you may want to rethink logging. However, this logging happens after the result is written to the client, so while the total processing time increases with logging, responding to the client does not (closing the connection however might be). Also note that these tests were conducted without a proper warm-up. I assume that after appropriate JVM warm-up, you will have much faster processing of requests.

### Automatic profiling of inferred spans [_automatic_profiling_of_inferred_spans]

Once you have a bigger application with more code paths than our sample app, you can try to enable the [automatic profiling of inferred spans](apm-agent-java://reference/config-profiling.md#config-profiling-inferred-spans-enabled) by setting the following.

```bash
ELASTIC_APM_PROFILING_INFERRED_SPANS_ENABLED=true
```

This mechanism uses the [async profiler](https://github.com/jvm-profiling-tools/async-profiler) to create spans without you having to instrument anything allowing you to find bottlenecks faster.

### Log correlation [_log_correlation]

Transaction ids are automatically added to logs. You can check the generated log files that are sent to {{es}} via {{filebeat}}. An entry looks like this.

```json
{
  "@timestamp": "2020-07-13T12:03:22.491Z",
  "log.level": "INFO",
  "message": "GET / 200 0:0:0:0:0:0:0:1 \"curl/7.64.1\" 0",
  "service.name": "my-javalin-app",
  "event.dataset": "my-javalin-app.log",
  "process.thread.name": "qtp34871826-36",
  "log.logger": "de.spinscale.javalin.Log4j2RequestLogger",
  "trace.id": "ed735860ec0cd3ee3bdf80ed7ea47afb",
  "transaction.id": "8af7dff698937dc5"
}
```

Having the `trace.id` and `transaction.id` added, in the case of an error you will get an `error.id` field.

::::{important}
We have not covered the [Elastic APM OpenTracing bridge](apm-agent-java://reference/opentracing-bridge.md) or looked into the [additional metrics](apm-agent-java://reference/metrics.md) the agent provides, which allows us to take a look at things like garbage collection or the memory footprint of our application.

::::

## Step 8: Ingest Uptime data [_step_8_ingest_uptime_data]

```{applies_to}
stack: deprecated 8.15.0
```

There are some basic monitoring capabilities in our application so far. We index logs (with traces), we index metrics, and we even can look in our app to figure out single performance bottlenecks thanks to APM. However, there is still one weak spot. Everything done so far was within the application, but all the users are reaching the application from the internet.

How about checking if our users have the same experience that our APM data is suggesting to us. Imagine having a lagging load balancer fronting your app, that costs you an additional 50 milliseconds per request. That would be devastating. Or TLS negotiation being costly. Even though none of those external events is your fault, you will still be impacted by this and should try to mitigate those. This means you need to know about them first.

[Uptime](https://www.elastic.co/uptime-monitoring) not only enables you to monitor the availability of a service, but also graph latencies over time, and get notified about expiring TLS certificates.

### Setup [_setup]

To send uptime data to {{es}}, {{heartbeat}} (the polling component) is required. To download and install {{heartbeat}}, use the commands that work with your system:

:::::::{tab-set}

::::::{tab-item} DEB
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-{{version.stack}}-amd64.deb
sudo dpkg -i heartbeat-{{version.stack}}-amd64.deb
```
::::::

::::::{tab-item} RPM
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-{{version.stack}}-x86_64.rpm
sudo rpm -vi heartbeat-{{version.stack}}-x86_64.rpm
```
::::::

::::::{tab-item} MacOS
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-{{version.stack}}-darwin-x86_64.tar.gz
tar xzvf heartbeat-{{version.stack}}-darwin-x86_64.tar.gz
```
::::::

::::::{tab-item} Linux
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-{{version.stack}}-linux-x86_64.tar.gz
tar xzvf heartbeat-{{version.stack}}-linux-x86_64.tar.gz
```
::::::

::::::{tab-item} Windows
1. Download the [Heartbeat Windows zip file](https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-{{version.stack}}-windows-x86_64.zip).

2. Extract the contents of the zip file into `C:\Program Files`.

3. Rename the `heartbeat-[version]-windows-x86_64` directory to `Heartbeat`.

4. Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select *Run As Administrator*).

5. From the PowerShell prompt, run the following commands to install Heartbeat as a Windows service:

  ```shell subs=true
  PS > cd 'C:\Program Files\Heartbeat'
  PS C:\Program Files\Heartbeat> .\install-service-heartbeat.ps1
  ```

```{note}
If script execution is disabled on your system, you need to set the execution policy for the current session to allow the script to run. For example: `PowerShell.exe -ExecutionPolicy UnRestricted -File .\install-service-heartbeat.ps1`.
```
::::::

:::::::
After downloading and unpacking, we have to set up the cloud id and the password one more time.

1. We need to create another `API_KEY` as an elastic admin user in {{kib}}.

    ```console
    POST /_security/api_key
    {
      "name": "heartbeat_javalin-app",
      "role_descriptors": {
        "heartbeat_writer": {
          "cluster": ["monitor", "read_ilm"],
          "index": [
            {
              "names": ["heartbeat-*"],
              "privileges": ["view_index_metadata", "create_doc"]
            }
          ]
        }
      }
    }
    ```

2. Let’s setup the {{heartbeat}} keystore and run the setup.

    ```bash
    ./heartbeat keystore create
    echo -n "observability-javalin-app:ZXUtY2VudHJhbC0xLmF3cy5jbG91ZC5lcy5pbyQ4NDU5M2I1YmQzYTY0N2NhYjA2MWQ3NTJhZWFhNWEzYyQzYmQwMWE2OTQ2MmQ0N2ExYjdhYTkwMzI0YjJiOTMyYQ==" | ./heartbeat keystore add CLOUD_ID --stdin
    echo -n "SCdUSHMB1JmLUFPLgWAY:R3PQzBWW3faJT01wxXD6uw" | ./heartbeat keystore add ES_API_KEY --stdin

    ./heartbeat setup -e -E 'cloud.id=${CLOUD_ID}' -E 'cloud.auth=elastic:YOUR_SUPER_SECRET_PASS'
    ```

3. Add some services to monitor.

    ```yaml
    name: heartbeat-shipper

    cloud.id: ${CLOUD_ID}
    output.elasticsearch:
      api_key: ${ES_API_KEY}

    heartbeat.monitors:
      - type: http
        id: javalin-http-app
        name: "Javalin Web Application"
        urls: ["http://localhost:7000"]
        check.response.status: [200]
        schedule: '@every 15s'

      - type: http
        id: httpbin-get
        name: "httpbin GET"
        urls: ["https://httpbin.org/get"]
        check.response.status: [200]
        schedule: '@every 15s'

      - type: tcp
        id: javalin-tcp
        name: "TCP Port 7000"
        hosts: ["localhost:7000"]
        schedule: '@every 15s'

    processors:
      - add_observer_metadata:
          geo:
            name: europe-munich
            location: "48.138791, 11.583030"
    ```

4. Now start {{heartbeat}} and wait a couple of minutes to get some data.

:::::::{tab-set}

::::::{tab-item} DEB
```sh
sudo service heartbeat start
```

::::{note}
If you use an `init.d` script to start Heartbeat, you can’t specify command line flags (see [Command reference](beats://reference/heartbeat/command-line-options.md)). To specify flags, start Heartbeat in the foreground.
::::

Also see [Heartbeat and systemd](beats://reference/heartbeat/running-with-systemd.md).
::::::

::::::{tab-item} RPM
```sh
sudo service heartbeat start
```

::::{note}
If you use an `init.d` script to start Heartbeat, you can’t specify command line flags (see [Command reference](beats://reference//heartbeat/command-line-options.md)). To specify flags, start Heartbeat in the foreground.
::::

Also see [Heartbeat and systemd](beats://reference/heartbeat/running-with-systemd.md).
::::::

::::::{tab-item} MacOS
```sh
sudo chown root heartbeat.yml <1>
sudo ./heartbeat -e
```

1. You’ll be running Heartbeat as root, so you need to change ownership of the configuration file, or run Heartbeat with `--strict.perms=false` specified. See [Config File Ownership and Permissions](beats://reference/libbeat/config-file-permissions.md).
::::::

::::::{tab-item} Linux
```sh
sudo chown root heartbeat.yml <1>
sudo ./heartbeat -e
```

1. You’ll be running Heartbeat as root, so you need to change ownership of the configuration file, or run Heartbeat with `--strict.perms=false` specified. See [Config File Ownership and Permissions](beats://reference/libbeat/config-file-permissions.md).
::::::

::::::{tab-item} Windows
```sh
PS C:\Program Files\heartbeat> Start-Service heartbeat
```

By default, Windows log files are stored in `C:\ProgramData\heartbeat\Logs`.
::::::

:::::::
To view the {{uptime-app}}, select **{{observability}}** → **Uptime**. The overview looks like this.

![Uptime Overview](/solutions/images/observability-monitor-java-app-uptime-overview.png "")

You can see the list of monitors and a global overview. Let’s see the details for one of those alerts. Click **Javalin Web Application**.

You can see the execution for the last scheduled checks, but the duration for each check might be more interesting. You can see if the latency for one of your checks is going up.

The interesting part is the world map at the top. You can specify in the configuration where the check originated, which in this case was in Munich in Europe. By configuring several {{heartbeat}}s running across the world, you can compare latencies and figure out which data center you need to run your application to be next to your users.

The duration of the monitor is in the low milliseconds, as it is really fast. Check the monitor for the `httpbin.org` endpoint, and you will see a much higher duration. In this case, it is about 400 milliseconds for each request. This is not too surprising because the endpoint is not nearby, and you need to initiate a TLS connection for every request, which is costly.

Do not underestimate the importance of this kind of monitoring. Also, consider this just the beginning as the next step is to have synthetics that monitor the correct behavior of your application, for example, to ensure that your checkout process works all the time.

## What’s next? [_whats_next]

For more information about using  Elastic {{observability}}, see the [{{observability}} documentation](../what-is-elastic-observability.md).

