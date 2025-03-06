---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/synthetics-lightweight.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-lightweight.html
---

# Configure lightweight monitors [synthetics-lightweight]

Monitor the status of network endpoints using the following lightweight checks:

* **HTTP**: Monitor your website. The HTTP monitor checks to make sure specific endpoints return the correct status code and display the correct text.
* **ICMP**: Check the availability of your hosts. The ICMP monitor uses ICMP (v4 and v6) Echo Requests to check the network reachability of the hosts you are pinging. This will tell you whether the host is available and connected to the network, but doesn’t tell you if a service on the host is running or not.
* **TCP**: Monitor the services running on your hosts. The TCP monitor checks individual ports to make sure the service is accessible and running.

Lightweight monitors can be configured using either the [Synthetics UI](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-ui) or [{{project-monitors-cap}}](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-projects).


## Synthetics UI [synthetics-lightweight-ui]

To use the UI, go to the Synthetics UI in {{kib}} or in your Observability Serverless project to create and configure monitors. For step-by-step instructions, refer to [Use the Synthetics UI](../../../solutions/observability/apps/create-monitors-in-synthetics-app.md).

:::{image} ../../../images/observability-synthetics-get-started-ui-lightweight.png
:alt: Synthetics Create monitor UI
:class: screenshot
:::


## {{project-monitors-cap}} [synthetics-lightweight-projects]

To use YAML files to create lightweight monitors in a Synthetics project, [set up the Synthetics project](../../../solutions/observability/apps/create-monitors-with-project-monitors.md) and configure monitors in YAML files in the `lightweight` directory.

In each YAML file, define a set of `monitors` to check your remote hosts. Each `monitor` item is an entry in a YAML list and begins with a dash (`-`). You can define the type of monitor to use, the hosts to check, and other optional settings.

The following example configures three monitors checking via the `http`, `icmp`, and `tcp` protocols and demonstrates how to use TCP Echo response verification:

```yaml
heartbeat.monitors:
- type: http
  name: Todos Lightweight
  id: todos-lightweight
  urls: "https://elastic.github.io/synthetics-demo/"
  schedule: '@every 1m'
- type: icmp
  id: ping-myhost
  name: My Host Ping
  hosts: "myhost"
  schedule: '@every 5m'
- type: tcp
  id: myhost-tcp-echo
  name: My Host TCP Echo
  hosts: "myhost:777"  # default TCP Echo Protocol
  check.send: "Check"
  check.receive: "Check"
  schedule: '@every 60s'
```

$$$synthetics-monitor-options$$$
There are some common monitor configuration options that are the same for all lightweight monitor types. For a complete list, refer to [Common options](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-common-options).

Each monitor type also has additional configuration options that are specific to that type. Refer to:

* [HTTP options](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-http)
* [ICMP options](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-icmp)
* [TCP options](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-tcp)

The `tcp` and `http` monitor types both support SSL/TLS and some proxy settings.


### Common options [synthetics-lightweight-common-options]

You can specify the following options when defining a synthetic monitor in any location. These options are the same for all monitors. Each monitor type has additional configuration options that are specific to that monitor type.

$$$monitor-type$$$

**`type`**
:   Type: `"http"` | `"icmp"` | `"tcp"`

    **Required**. The type of monitor to run. One of:

    * `http`: Connects via HTTP and optionally verifies that the host returns the expected response.
    * `icmp`: Uses an ICMP (v4 and v6) Echo Request to ping the configured hosts. Requires special permissions or root access.
    * `tcp`: Connects via TCP and optionally verifies the endpoint by sending and/or receiving a custom payload.


$$$monitor-id$$$

**`id`**
:   Type: [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)

    **Required**. A unique identifier for this configuration. This should not change with edits to the monitor configuration regardless of changes to any config fields.

    **Examples**:

    ```yaml
    id: uploader-service
    ```

    ```yaml
    id: http://example.net
    ```

    ::::{note}
    When querying against indexed monitor data this is the field you will be aggregating with. It appears in the exported fields as `monitor.id`.

    If you do not set an `id` explicitly, the monitor’s config will be hashed and a generated value will be used. This value will change with any options change to this monitor making aggregations over time between changes impossible. For this reason, it’s recommended that you set this manually.

    ::::


$$$monitor-name$$$

**`name`**
:   Type: [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)

    Human readable name for this monitor.

    **Examples**:

    ```yaml
    name: Uploader service
    ```

    ```yaml
    name: Example website
    ```


$$$monitor-service_name$$$

**`service.name`**
:   Type: [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)

    APM service name for this monitor. Corresponds to the `service.name` ECS field. Set this when monitoring an app that is also using APM to enable integrations between Synthetics and APM data in Kibana or your Observability Serverless project.


$$$monitor-enabled$$$

**`enabled`**
:   Type: [boolean](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-bool)

    Whether the monitor is enabled.

    **Default**: `true`

    **Example**:

    ```yaml
    enabled: false
    ```


$$$monitor-schedule$$$

**`schedule`**
:   Type: [duration](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-duration)

    **Required**. The task schedule.

    ::::{note}
    Schedules with less than 1 minute resolution will be saved to the nearest minute. For example, `@every 5s` will be changed to `@every 60s` when the monitor is pushed using the CLI.
    ::::


    **Example**: Run the task every 5 minutes from the time the monitor was started.

    ```yaml
    schedule: @every 5m
    ```


$$$monitor-timeout$$$

**`timeout`**
:   Type: [duration](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-duration)

    The total running time for each ping test. This is the total time allowed for testing the connection and exchanging data.

    **Default**: `16s`

    **Example**:

    ```yaml
    timeout: 2m
    ```


$$$monitor-tags$$$

**`tags`**
:   Type: list of [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)s

    A list of tags that will be sent with the monitor event.

    **Examples**:

    ```yaml
    tags:
      - tag one
      - tag two
    ```

    ```yaml
    tags: ["tag one", "tag two"]
    ```


$$$monitor-mode$$$

**`mode`**
:   Type: `"any"` | `"all"`

    One of two modes in which to run the monitor:

    * `any`: The monitor pings only one IP address for a hostname.
    * `all`: The monitor pings all resolvable IPs for a hostname.

    **Default**: `any`

    **Example**: If you’re using a DNS-load balancer and want to ping every IP address for the specified hostname, you should use `all`.


$$$monitor-ipv4$$$

**`ipv4`**
:   Type: [boolean](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-bool)

    Whether to ping using the ipv4 protocol if hostnames are configured.

    **Default**: `true`

    **Example**:

    ```yaml
    ipv4: false
    ```


$$$monitor-ipv6$$$

**`ipv6`**
:   Type: [boolean](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-bool)

    Whether to ping using the ipv6 protocol if hostnames are configured.

    **Default**: `true`

    **Example**:

    ```yaml
    ipv6: false
    ```


$$$monitor-alert$$$

**`alert`**
:   Enable or disable alerts on this monitor. Read more about alerts in [Alerting](../../../solutions/observability/apps/configure-synthetics-settings.md#synthetics-settings-alerting).

    **`status.enabled`** ([boolean](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-bool))
    :   Enable monitor status alerts on this monitor.

        **Default**: `true`

        **Example**:

        ```yaml
        alert.status.enabled: true
        ```


    **`tls.enabled`** ([boolean](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-bool))
    :   Enable TLS certificate alerts on this monitor.

        **Default**: `true`

        **Example**:

        ```yaml
        alert.tls.enabled: true
        ```


$$$monitor-retest_on_failure$$$

**`retest_on_failure`**
:   Type: [boolean](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-bool)

    Enable or disable retesting when a monitor fails. Default is `true`.

    By default, monitors are automatically retested if the monitor goes from "up" to "down". If the result of the retest is also "down", an error will be created, and if configured, an alert sent. Then the monitor will resume running according to the defined schedule. Using `retestOnFailure` can reduce noise related to transient problems.

    **Example**:

    ```yaml
    retest_on_failure: false
    ```


$$$monitor-locations$$$

**`locations`**
:   Type: list of [`SyntheticsLocationsType`](https://github.com/elastic/synthetics/blob/v1.3.0/src/locations/public-locations.ts#L28-L37)

    Where to deploy the monitor. You can deploy monitors in multiple locations to detect differences in availability and response times across those locations.

    To list available locations you can:

    * Run the [`elastic-synthetics locations` command](../../../solutions/observability/apps/use-synthetics-cli.md#elastic-synthetics-locations-command).
    * Find `Synthetics` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) and click **Create monitor**. Locations will be listed in *Locations*.

    **Examples**:

    ```yaml
    locations: ["japan", "india"]
    ```

    ```yaml
    locations:
      - japan
      - india
    ```

    ::::{note}
    This can also be set using [`monitor.locations` in the Synthetics project configuration file](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-monitor) or via the CLI using the [`--location` flag on `push`](../../../solutions/observability/apps/use-synthetics-cli.md#elastic-synthetics-push-command).

    The value defined via the CLI takes precedence over the value defined in the lightweight monitor configuration, and the value defined in the lightweight monitor configuration takes precedence over the value defined in the Synthetics project configuration file.

    ::::


$$$monitor-private_locations$$$

**`private_locations`**
:   Type: list of [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)s

    The [{{private-location}}s](../../../solutions/observability/apps/monitor-resources-on-private-networks.md) to which the monitors will be deployed. These {{private-location}}s refer to locations hosted and managed by you, whereas  `locations` are hosted by Elastic. You can specify a {{private-location}} using the location’s name.

    To list available {{private-location}}s you can:

    * Run the [`elastic-synthetics locations` command](../../../solutions/observability/apps/use-synthetics-cli.md#elastic-synthetics-locations-command) and specify the {{kib}} URL of the deployment. This will fetch all available private locations associated with the deployment.
    * Find `Synthetics` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) and click **Create monitor**. {{private-location}}s will be listed in *Locations*.

    **Examples**:

    ```yaml
    private_locations: ["Private Location 1", "Private Location 2"]
    ```

    ```yaml
    private_locations:
      - Private Location 1
      - Private Location 2
    ```

    ::::{note}
    This can also be set using [`monitor.privateLocations` in the Synthetics project configuration file](../../../solutions/observability/apps/configure-synthetics-projects.md#synthetics-configuration-monitor) or via the CLI using the [`--privateLocations` flag on `push`](../../../solutions/observability/apps/use-synthetics-cli.md#elastic-synthetics-push-command).

    The value defined via the CLI takes precedence over the value defined in the lightweight monitor configuration, and the value defined in the lightweight monitor configuration takes precedence over the value defined in Synthetics project configuration file.

    ::::


$$$monitor-fields$$$

**`fields`**
:   A list of key-value pairs that will be sent with each monitor event. The `fields` are appended to {{es}} documents as `labels`, and those labels are displayed in {{kib}} in the *Monitor details* panel in the [individual monitor’s *Overview* tab](../../../solutions/observability/apps/analyze-data-from-synthetic-monitors.md#synthetics-analyze-individual-monitors-overview).

    **Examples**:

    ```yaml
    fields:
      foo: bar
      team: synthetics
    ```

    ```yaml
    fields.foo: bar
    fields.team: synthetics
    ```



### HTTP options [synthetics-lightweight-http]

The options described here configure Synthetics to connect via HTTP and optionally verify that the host returns the expected response.

Valid options for HTTP monitors include [all common options](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-common-options) and the following HTTP-specific options:

$$$monitor-http-urls$$$

**`urls`**
:   Type: [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)

    **Required**. The URL to ping.


$$$monitor-http-max_redirects$$$

**`max_redirects`**
:   Type: [number](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-numbers)

    The total number of redirections Synthetics will follow.

    By default, Synthetics will not follow redirects, but will report the status of the redirect. If set to a number greater than `0`, Synthetics will follow that number of redirects.

    When this option is set to a value greater than `0`, the `monitor.ip` field will no longer be reported, as multiple DNS requests across multiple IPs may return multiple IPs. Fine-grained network timing data will also not be recorded, as with redirects that data will span multiple requests. Specifically the fields `http.rtt.content.us`, `http.rtt.response_header.us`, `http.rtt.total.us`, `http.rtt.validate.us`, `http.rtt.write_request.us` and `dns.rtt.us` will be omitted.

    **Default**: `0`


$$$monitor-http-proxy_headers$$$

**`proxy_headers`**
:   Additional headers to send to proxies during `CONNECT` requests.

$$$monitor-http-proxy_url$$$

**`proxy_url`**
:   ([string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)) The HTTP proxy URL. This setting is optional.

    **Example**:

    ```yaml
    http://proxy.mydomain.com:3128
    ```


$$$monitor-http-username$$$

**`username`**
:   Type: [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)

    The username for authenticating with the server. The credentials are passed with the request. This setting is optional.

    You need to specify credentials when your `check.response` settings require it. For example, you can check for a 403 response (`check.response.status: [403]`) without setting credentials.


$$$monitor-http-password$$$

**`password`**
:   Type: [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)

    The password for authenticating with the server. This setting is optional.


$$$monitor-http-ssl$$$

**`ssl`**
:   Type: [SSL](asciidocalypse://docs/beats/docs/reference/heartbeat/configuration-ssl.md)

    The TLS/SSL connection settings for use with the HTTPS endpoint. If you don’t specify settings, the system defaults are used.

    **Example**:

    ```yaml
    - type: http
      id: my-http-service
      name: My HTTP Service
      urls: "https://myhost:443"
      schedule: '@every 5s'
      ssl:
        certificate_authorities: ['/etc/ca.crt']
        supported_protocols: ["TLSv1.0", "TLSv1.1", "TLSv1.2"]
    ```


$$$monitor-http-headers$$$

**`headers`**
:   Type: [boolean](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-bool)

    Controls the indexing of the HTTP response headers `http.response.body.headers` field. Set `response.include_headers` to `false` to disable.

    **Default**: `true`


$$$monitor-http-response$$$

**`response`**
:   Controls the indexing of the HTTP response body contents to the `http.response.body.contents` field.

    **`include_body`** (`"on_error"` | `"never"` | `"always"`)
    :   Set `response.include_body` to one of the options listed below.

        * `on_error`: Include the body if an error is encountered during the check. This is the default.
        * `never`: Never include the body.
        * `always`: Always include the body with checks.


    **`include_body_max_bytes`** ([number](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-numbers))
    :   Set `response.include_body_max_bytes` to control the maximum size of the stored body contents.

        **Default**: `1024`


$$$monitor-http-check$$$

**`check`**
:   **`request`**
:   An optional `request` to send to the remote host. Under `check.request`, specify these options:

    **`method`**
    :   Type: `"HEAD"` | `"GET"` | `"POST"` | `"OPTIONS"`

        The HTTP method to use.


    **`headers`**
    :   Type: [HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

        A dictionary of additional HTTP headers to send. By default Synthetics will set the *User-Agent* header to identify itself.


    **`body`**
    :   Type: [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)

        Optional request body content.


**Example**: This monitor POSTs an `x-www-form-urlencoded` string to the endpoint `/demo/add`.

```yaml
check.request:
  method: POST
  headers:
    'Content-Type': 'application/x-www-form-urlencoded'
  # urlencode the body:
  body: "name=first&email=someemail%40someemailprovider.com"
```


**`response`**
:   The expected `response`.

    Under `check.response`, specify these options:

    **`status`**
    :   Type: list of [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)s

        A list of expected status codes. 4xx and 5xx codes are considered `down` by default. Other codes are considered `up`.

        **Example**:

        ```yaml
        check.response:
          status: [200, 201]
        ```


    **`headers`**
    :   Type: [HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

        The required response headers.


    **`body.positive`**
    :   Type: list of [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)s

        A list of regular expressions to match the body output. Only a single expression needs to match.

        **Example**:

        This monitor examines the response body for the strings *foo* or *Foo*:

        ```yaml
        check.response:
          status: [200, 201]
          body:
            positive:
              - foo
              - Foo
        ```


    **`body.negative`** (list of [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)s)
    :   A list of regular expressions to match the body output negatively. Return match failed if single expression matches. HTTP response bodies of up to 100MiB are supported.

        This monitor examines match successfully if there is no *bar* or *Bar* at all, examines match failed if there is *bar* or *Bar* in the response body:

        **Example**:

        ```yaml
        check.response:
          status: [200, 201]
          body:
            negative:
              - bar
              - Bar
        ```

        **Example**:

        This monitor examines match successfully only when *foo* or *Foo* in body AND no *bar* or *Bar* in body:

        ```yaml
        check.response:
          status: [200, 201]
          body:
            positive:
              - foo
              - Foo
            negative:
              - bar
              - Bar
        ```


    **`json`**
    :   A list of expressions executed against the body when parsed as JSON. Body sizes must be less than or equal to 100 MiB.

    **`description`**
    :   A description of the check.

    **`expression`**
    :   The following configuration shows how to check the response using [gval](https://github.com/PaesslerAG/gval/blob/master/README.md) expressions when the body contains JSON:

        **Example**:

        ```yaml
        check.response:
          status: [200]
          json:
            - description: check status
              expression: 'foo.bar == "myValue"'
        ```



### ICMP options [synthetics-lightweight-icmp]

The options described here configure Synthetics to use ICMP (v4 and v6) Echo Requests to check the configured hosts. On most platforms you must execute Synthetics with elevated permissions to perform ICMP pings.

On Linux, regular users may perform pings if the right file capabilities are set. Run `sudo setcap cap_net_raw+eip /path/to/heartbeat` to  grant Synthetics ping capabilities on Linux. Alternatively, you can grant ping permissions to the user being used to run Synthetics. To grant ping permissions in this way, run `sudo sysctl -w net.ipv4.ping_group_range='myuserid myuserid'`.

Other platforms may require Synthetics to run as root or administrator to execute pings.

Valid options for ICMP monitors include [all common options](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-common-options) and the following ICMP-specific options:

$$$monitor-icmp-hosts$$$

**`hosts`**
:   Type: [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)

    **Required**. The host to ping.

    **Example**:

    ```yaml
    hosts: "myhost"
    ```


$$$monitor-icmp-wait$$$

**`wait`**
:   Type: [duration](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-duration)

    The duration to wait before emitting another ICMP Echo Request if no response is received.

    **Default**: `1s`

    **Example**:

    ```yaml
    wait: 1m
    ```



### TCP options [synthetics-lightweight-tcp]

The options described here configure Synthetics to connect via TCP and optionally verify the endpoint by sending and/or receiving a custom payload.

Valid options for TCP monitors include [all common options](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-common-options) and the following TCP-specific options:

$$$monitor-tcp-hosts$$$

**`hosts`**
:   Type: [string](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-string)

    **Required**. The host to ping. The value can be:

    * **A hostname and port, such as `localhost:12345`.** Synthetics connects to the port on the specified host. If the monitor is [configured to use SSL](asciidocalypse://docs/beats/docs/reference/heartbeat/configuration-ssl.md), Synthetics establishes an SSL/TLS-based connection. Otherwise, it establishes a TCP connection.
    * **A full URL using the syntax `scheme://<host>:[port]`**, where:

        * `scheme` is one of `tcp`, `plain`, `ssl` or `tls`. If `tcp` or `plain` is specified, Synthetics establishes a TCP connection even if the monitor is configured to use SSL. If `tls` or `ssl` is specified, Synthetics establishes an SSL connection. However, if the monitor is not configured to use SSL, the system defaults are used (currently not supported on Windows).
        * `host` is the hostname.
        * `port` is the port number.


    **Examples**:

    ```yaml
    hosts: "localhost:8000"
    ```

    ```yaml
    hosts: "tcp://localhost:8000"
    ```


$$$monitor-tcp-check$$$

**`check`**
:   An optional payload string to send to the remote host and the expected answer. If no payload is specified, the endpoint is assumed to be available if the connection attempt was successful. If `send` is specified without `receive`, any response is accepted as OK. If `receive` is specified without `send`, no payload is sent, but the client expects to receive a payload in the form of a "hello message" or "banner" on connect.

    **Example**:

    ```yaml
    check.send: 'Hello World'
    check.receive: 'Hello World'
    ```

    ```yaml
    check:
      send: 'Hello World'
      receive: 'Hello World'
    ```


$$$monitor-tcp-proxy_url$$$

**`proxy_url`**
:   The URL of the SOCKS5 proxy to use when connecting to the server. The value must be a URL with a scheme of socks5://

    If the SOCKS5 proxy server requires client authentication, then a username and password can be embedded in the URL.

    When using a proxy, hostnames are resolved on the proxy server instead of on the client. You can change this behavior by setting the `proxy_use_local_resolver` option.

    **Examples**:

    A proxy URL that requires client authentication:

    ```yaml
    proxy_url: socks5://user:password@socks5-proxy:2233
    ```


$$$monitor-tcp-proxy_use_local_resolver$$$

**`proxy_use_local_resolver`**
:   Type: [boolean](../../../solutions/observability/apps/configure-lightweight-monitors.md#synthetics-lightweight-data-bool)

    A Boolean value that determines whether hostnames are resolved locally instead of being resolved on the proxy server. The default value is `false`, which means that name resolution occurs on the proxy server.

    **Default**: `false`


$$$monitor-tcp-ssl$$$

**`ssl`**
:   Type: [SSL](asciidocalypse://docs/beats/docs/reference/heartbeat/configuration-ssl.md)

    The TLS/SSL connection settings. If the monitor is [configured to use SSL](asciidocalypse://docs/beats/docs/reference/heartbeat/configuration-ssl.md), it will attempt an SSL handshake. If `check` is not configured, the monitor will only check to see if it can establish an SSL/TLS connection. This check can fail either at TCP level or during certificate validation.

    **Example**:

    ```yaml
    ssl:
      certificate_authorities: ['/etc/ca.crt']
      supported_protocols: ["TLSv1.0", "TLSv1.1", "TLSv1.2"]
    ```

    Also see [Configure SSL](asciidocalypse://docs/beats/docs/reference/heartbeat/configuration-ssl.md) for a full description of the `ssl` options.



### Data types reference [synthetics-lightweight-data-types]

Values of configuration settings are interpreted as required by Synthetics. If a value can’t be correctly interpreted as the required type - for example a string is given when a number is required - Synthetics will fail to start up.


#### Boolean [synthetics-lightweight-data-bool]

Boolean values can be either `true` or `false`. Alternative names for `true` are `yes` and `on`. Instead of `false` the values `no` and `off` can be used.

```yaml
enabled: true
disabled: false
```


#### Number [synthetics-lightweight-data-numbers]

Number values require you to enter the number *without* single or double quotes.

```yaml
integer: 123
negative: -1
float: 5.4
```

::::{note}
Some settings only support a restricted number range.
::::



#### String [synthetics-lightweight-data-string]

In [YAML](http://www.yaml.org), multiple styles of string definitions are supported: double-quoted, single-quoted, unquoted.

The double-quoted style is specified by surrounding the string with `"`. This style provides support for escaping unprintable characters using `\`, but comes at the cost of having to escape `\` and `"` characters.

The single-quoted style is specified by surrounding the string with `'`. This style supports no escaping (use `''` to quote a single quote). Only printable characters can be used when using this form.

Unquoted style requires no quotes, but does not support any escaping and can’t include any symbol that has a special meaning in YAML.

::::{note}
Single-quoted style is recommended when defining regular expressions, event format strings, windows file paths, or non-alphabetical symbolic characters.
::::



#### Duration [synthetics-lightweight-data-duration]

Durations require a numeric value with optional fraction and required unit. Valid time units are `ns`, `us`, `ms`, `s`, `m`, `h`. Sometimes features based on durations can be disabled by using zero or negative durations.

```yaml
duration1: 2.5s
duration2: 6h
duration_disabled: -1s
```


#### Regular expression [synthetics-lightweight-data-regex]

Regular expressions are special strings that are compiled into regular expressions at load time.

As regular expressions and YAML use `\` for escaping characters in strings, it’s highly recommended to use single quoted strings when defining regular expressions. When single quoted strings are used, the `\` character is not interpreted by YAML parser as an escape symbol.