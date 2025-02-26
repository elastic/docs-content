---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/processor-syntax.html
---

# Processor syntax [processor-syntax]

Specify a list of one or more processors:

* When configuring processors in the standalone {{agent}} configuration file, put this list under the `processors` setting.
* When using the Integrations UI in {{kib}}, put this list in the **Processors** field.

Each processor begins with a dash (-) and includes the processor name, an optional [condition](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions), and configuration settings to pass to the processor:

```yaml
- <processor_name>:
    when:
      <condition>
    <settings>

- <processor_name>:
    when:
      <condition>
    <settings>
```

If a [condition](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions) is specified, it must be met in order for the processor to run. If no condition is specified, the processor always runs.

To accomplish complex conditional processing, use the if-then-else processor configuration. This configuration allows you to run multiple processors based on a single condition. For example:

```yaml
- if:
    <condition>
  then: <1>
    - <processor_name>:
        <settings>
    - <processor_name>:
        <settings>
    ...
  else: <2>
    - <processor_name>:
        <settings>
    - <processor_name>:
        <settings>
```

1. `then` must contain a single processor or a list of processors that will execute when the condition is `true`.
2. `else` is optional. It can contain a single processor or a list of processors that will execute when the condition is `false`.



## Conditions [processor-conditions]

Each condition receives a field to compare. You can specify multiple fields under the same condition by using `AND` between the fields (for example, `field1 AND field2`).

For each field, you can specify a simple field name or a nested map, for example `dns.question.name`.

Refer to the [integrations documentation](integration-docs://docs/reference/index.md) for a list of all fields created by a specific integration.

The supported conditions are:

* [`equals`](#processor-condition-equals)
* [`contains`](#processor-condition-contains)
* [`regexp`](#processor-condition-regexp)
* [`range`](#processor-condition-range)
* [`network`](#processor-condition-network)
* [`has_fields`](#processor-condition-has_fields)
* [`or`](#processor-condition-or)
* [`and`](#processor-condition-and)
* [`not`](#processor-condition-not)


### `equals` [processor-condition-equals]

With the `equals` condition, you can check if a field has a certain value. The condition accepts only an integer or string value.

For example, the following condition checks if the response code of the HTTP transaction is 200:

```yaml
equals:
  http.response.code: 200
```


### `contains` [processor-condition-contains]

The `contains` condition checks if a value is part of a field. The field can be a string or an array of strings. The condition accepts only a string value.

For example, the following condition checks if an error is part of the transaction status:

```yaml
contains:
  status: "Specific error"
```


### `regexp` [processor-condition-regexp]

The `regexp` condition checks the field against a regular expression. The condition accepts only strings.

For example, the following condition checks if the process name starts with `foo`:

```yaml
regexp:
  system.process.name: "^foo.*"
```


### `range` [processor-condition-range]

The `range` condition checks if the field is in a certain range of values. The condition supports `lt`, `lte`, `gt` and `gte`. The condition accepts only integer or float values.

For example, the following condition checks for failed HTTP transactions by comparing the `http.response.code` field with 400.

```yaml
range:
  http.response.code:
    gte: 400
```

This can also be written as:

```yaml
range:
  http.response.code.gte: 400
```

The following condition checks if the CPU usage in percentage has a value between 0.5 and 0.8.

```yaml
range:
  system.cpu.user.pct.gte: 0.5
  system.cpu.user.pct.lt: 0.8
```


### `network` [processor-condition-network]

The `network` condition checks if the field is in a certain IP network range. Both IPv4 and IPv6 addresses are supported. The network range may be specified using CIDR notation, like "192.0.2.0/24" or "2001:db8::/32", or by using one of these named ranges:

* `loopback` - Matches loopback addresses in the range of `127.0.0.0/8` or `::1/128`.
* `unicast` - Matches global unicast addresses defined in RFC 1122, RFC 4632, and RFC 4291 with the exception of the IPv4 broadcast address (`255.255.255.255`). This includes private address ranges.
* `multicast` - Matches multicast addresses.
* `interface_local_multicast` - Matches IPv6 interface-local multicast addresses.
* `link_local_unicast` - Matches link-local unicast addresses.
* `link_local_multicast` - Matches link-local multicast addresses.
* `private` - Matches private address ranges defined in RFC 1918 (IPv4) and RFC 4193 (IPv6).
* `public` - Matches addresses that are not loopback, unspecified, IPv4 broadcast, link-local unicast, link-local multicast, interface-local multicast, or private.
* `unspecified` - Matches unspecified addresses (either the IPv4 address "0.0.0.0" or the IPv6 address "::").

The following condition returns true if the `source.ip` value is within the private address space.

```yaml
network:
  source.ip: private
```

This condition returns true if the `destination.ip` value is within the IPv4 range of `192.168.1.0` - `192.168.1.255`.

```yaml
network:
  destination.ip: '192.168.1.0/24'
```

And this condition returns true when `destination.ip` is within any of the given subnets.

```yaml
network:
  destination.ip: ['192.168.1.0/24', '10.0.0.0/8', loopback]
```


### `has_fields` [processor-condition-has_fields]

The `has_fields` condition checks if all the given fields exist in the event. The condition accepts a list of string values denoting the field names.

For example, the following condition checks if the `http.response.code` field is present in the event.

```yaml
has_fields: ['http.response.code']
```


### `or` [processor-condition-or]

The `or` operator receives a list of conditions.

```yaml
or:
  - <condition1>
  - <condition2>
  - <condition3>
  ...
```

For example, to configure the condition `http.response.code = 304 OR http.response.code = 404`:

```yaml
or:
  - equals:
      http.response.code: 304
  - equals:
      http.response.code: 404
```


### `and` [processor-condition-and]

The `and` operator receives a list of conditions.

```yaml
and:
  - <condition1>
  - <condition2>
  - <condition3>
  ...
```

For example, to configure the condition `http.response.code = 200 AND status = OK`:

```yaml
and:
  - equals:
      http.response.code: 200
  - equals:
      status: OK
```

To configure a condition like `<condition1> OR <condition2> AND <condition3>`:

```yaml
or:
  - <condition1>
  - and:
    - <condition2>
    - <condition3>
```


### `not` [processor-condition-not]

The `not` operator receives the condition to negate.

```yaml
not:
  <condition>
```

For example, to configure the condition `NOT status = OK`:

```yaml
not:
  equals:
    status: OK
```
