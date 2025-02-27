---
navigation_title: "registered_domain"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/registered_domain-processor.html
---

# Registered Domain [registered_domain-processor]


The `registered_domain` processor reads a field containing a hostname and then writes the "registered domain" contained in the hostname to the target field. For example, given `www.google.co.uk`, the processor would output `google.co.uk`. In other words, the "registered domain" is the effective top-level domain (`co.uk`) plus one level (`google`). Optionally, the processor can store the rest of the domain, the `subdomain`, into another target field.

This processor uses the Mozilla Public Suffix list to determine the value.


## Example [_example_30]

```yaml
  - registered_domain:
      field: dns.question.name
      target_field: dns.question.registered_domain
      target_etld_field: dns.question.top_level_domain
      target_subdomain_field: dns.question.sudomain
      ignore_missing: true
      ignore_failure: true
```


## Configuration settings [_configuration_settings_35]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `field` | Yes |  | Source field containing a fully qualified domain name (FQDN). |
| `target_field` | Yes |  | Target field for the registered domain value. |
| `target_etld_field` | No |  | Target field for the effective top-level domain value. |
| `target_subdomain_field` | No |  | Target subdomain field for the subdomain value. |
| `ignore_missing` | No | `false` | Whether to ignore errors when the source field is missing. |
| `ignore_failure` | No | `false` | Whether to ignore all errors produced by the processor. |
| `id` | No |  | Identifier for this processor instance. Useful for debugging. |

