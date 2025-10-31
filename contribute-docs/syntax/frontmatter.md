# Frontmatter

Every Markdown file referenced in the TOC may optionally define a frontmatter block.
Frontmatter is YAML-formatted metadata about a page, at the beginning of each file
and wrapped by `---` lines.

In the frontmatter block, you can define the following fields:

```yaml
---
navigation_title: This is the navigation title <1>
navigation_tooltip: This is a tooltip shown on hover <2>
description: This is a description of the page <3>
applies_to: <4>
  serverless: all
products: <5>
  - id: apm-agent
  - id: edot-sdk
sub: <6>
  key: value
---
```

1. [`navigation_title`](#navigation-title)
2. [`navigation_tooltip`](#navigation-tooltip)
3. [`description`](#description)
4. [`applies_to`](#applies-to)
5. [`products`](#products)
6. [`sub`](#subs)

## Navigation Title

See [](./titles.md)

## Navigation Tooltip

Use the `navigation_tooltip` frontmatter to set custom tooltip text that appears when hovering over navigation items.

The tooltip is displayed with a 500ms delay when hovering over navigation links in the sidebar and dropdown menus.
It's positioned dynamically relative to the viewport to avoid overflow issues.

If you don't set a `navigation_tooltip`, it will automatically fall back to the `description` field.
This provides helpful context for users browsing the navigation without requiring additional configuration.

The `navigation_tooltip` frontmatter is a string. Keep it concise (recommended 50-100 characters) for best readability.

Example:

```yaml
---
navigation_title: Quick Start
navigation_tooltip: Learn how to set up and configure your first application in 5 minutes
---
```

## Description

Use the `description` frontmatter to set the description meta tag for a page.
This helps search engines and social media.
It also sets the `og:description` and `twitter:description` meta tags.

The `description` frontmatter is a string, recommended to be around 150 characters. If you don't set a `description`,
it will be generated from the first few paragraphs of the page until it reaches 150 characters.

## Applies to

See [](./applies.md)

## Products

The products frontmatter is a list of products that the page relates to.
This is used for the "Products" filter in the Search UI.

The products frontmatter is a list of objects, each object has an `id` field.

| Product ID                                  | Product Name                                  |
|---------------------------------------------|-----------------------------------------------|
| `apm`                                       | APM                                           |
| `apm-agent`                                 | APM Agent                                     |
| `auditbeat`                                 | Auditbeat                                     |
| `beats`                                     | Beats                                         |
| `cloud-control-ecctl`                       | Elastic Cloud Control ECCTL                   |
| `cloud-enterprise`                          | Elastic Cloud Enterprise                      |
| `cloud-hosted`                              | Elastic Cloud Hosted                          |
| `cloud-kubernetes`                          | Elastic Cloud Kubernetes                      |
| `cloud-serverless`                          | Elastic Cloud Serverless                      |
| `cloud-terraform`                           | Elastic Cloud Terraform                       |
| `ecs`                                       | Elastic Common Schema (ECS)                   |
| `ecs-logging`                               | ECS Logging                                   |
| `edot-cf`                                   | EDOT Cloud Forwarder                          |
| `edot-sdk`                                  | Elastic Distribution of OpenTelemetry SDK     |
| `edot-collector`                            | Elastic Distribution of OpenTelemetry Collector |
| `elastic-agent`                             | Elastic Agent                                 |
| `elastic-serverless-forwarder`              | Elastic Serverless Forwarder                  |
| `elastic-stack`                             | Elastic Stack                                 |
| `elasticsearch`                             | Elasticsearch                                 |
| `elasticsearch-client`                      | Elasticsearch Client                          |
| `filebeat`                                  | Filebeat                                      |
| `fleet`                                     | Fleet                                         |
| `heartbeat`                                 | Heartbeat                                     |
| `integrations`                              | Integrations                                  |
| `kibana`                                    | Kibana                                        |
| `logstash`                                  | Logstash                                      |
| `machine-learning`                          | Machine Learning                              |
| `metricbeat`                                | Metricbeat                                    |
| `observability`                             | Elastic Observability                         |
| `packetbeat`                                | Packetbeat                                    |
| `painless`                                  | Painless                                      |
| `search-ui`                                 | Search UI                                     |
| `security`                                  | Elastic Security                              |
| `winlogbeat`                                | Winlogbeat                                    |

## Subs

Use the `sub` field to define local substitutions. Refer to [Substitutions](substitutions.md) for more information.