---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-agent-server-compatibility.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# APM agent compatibility [apm-agent-server-compatibility]

The chart below outlines the compatibility between different versions of Elastic APM agents and extensions with the APM integration.

## APM AWS Lambda extension [_apm_aws_lambda_extension]

| {{apm-agent}} version | APM integration version |
| --- | --- |
| `1.x` | ≥ `8.2` |

## Go agent [_go_agent]

| {{apm-agent}} version | APM integration version |
| --- | --- |
| `1.x` | ≥ `6.5` |
| `2.x` | ≥ `6.5` |

## iOS agent [_ios_agent]

| {{apm-agent}} version | APM integration version |
| --- | --- |
| `1.x` | ≥ `8.12` |

## Java agent [_java_agent]

| {{apm-agent}} version | APM integration version |
| --- | --- |
| `1.x` | ≥ `6.5` |

::::{note}
Java agent < 1.43.0 not fully compatible with APM Server >= 8.11.0. For more information, check [Elastic APM known issues](apm-server://release-notes/known-issues.md).

::::

## .NET agent [_net_agent]

| {{apm-agent}} version | APM integration version |
| --- | --- |
| `1.x` | ≥ `6.5` |

## Node.js agent [_node_js_agent]

| {{apm-agent}} version | APM integration version |
| --- | --- |
| `3.x` | ≥ `6.6` |

## PHP agent [_php_agent]

| {{apm-agent}} version | APM integration version |
| --- | --- |
| `1.x` | ≥ `7.0` |

## Python agent [_python_agent]

| {{apm-agent}} version | APM integration version |
| --- | --- |
| `6.x` | ≥ `6.6` |

## Ruby agent [_ruby_agent]

| {{apm-agent}} version | APM integration version |
| --- | --- |
| `3.x` | ≥ `6.5` |
| `4.x` | ≥ `6.5` |

## JavaScript RUM agent [_javascript_rum_agent]

| {{apm-agent}} version | APM integration version |
| --- | --- |
| `4.x` | ≥ `6.5` |
| `5.x` | ≥ `7.0` |

