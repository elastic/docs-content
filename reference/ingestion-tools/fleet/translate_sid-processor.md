---
navigation_title: "translate_sid"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/translate_sid-processor.html
---

# Translate SID [translate_sid-processor]


The `translate_sid` processor translates a Windows security identifier (SID) into an account name. It retrieves the name of the account associated with the SID, the first domain on which the SID is found, and the type of account. This is only available on Windows.

Every account on a network is issued a unique SID when the account is first created. Internal processes in Windows refer to an account’s SID rather than the account’s user or group name, and these values sometimes appear in logs.

If the SID is invalid (malformed) or does not map to any account on the local system or domain, the processor will return an error unless `ignore_failure` is set.


## Example [_example_35]

```yaml
  - translate_sid:
      field: winlog.event_data.MemberSid
      account_name_target: user.name
      domain_target: user.domain
      ignore_missing: true
      ignore_failure: true
```


## Configuration settings [_configuration_settings_41]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `field` | Yes |  | Source field containing a Windows security identifier (SID). |
| `account_name_target` | Yes* |  | Target field for the account name value. |
| `account_type_target` | Yes* |  | Target field for the account type value. |
| `domain_target` | Yes* |  | Target field for the domain value. |
| `ignore_missing` | No | `false` | Ignore errors when the source field is missing. |
| `ignore_failure` | No | `false` | Ignore all errors produced by the processor. |

* At least one of `account_name_target`, `account_type_target`, and `domain_target` must be configured.

