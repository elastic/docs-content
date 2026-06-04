---
navigation_title: Loop continue
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Reference for the loop.continue step, which skips to the next iteration of the innermost enclosing foreach or while loop.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Loop continue [workflows-loop-continue-step]

The `loop.continue` step skips the rest of the current iteration in the innermost enclosing [`foreach`](/explore-analyze/workflows/steps/foreach.md) or [`while`](/explore-analyze/workflows/steps/while.md) loop and moves on to the next iteration. Use it to skip items that don't meet a filter, without nesting the remaining logic inside an `if`.

## Parameters

`loop.continue` takes no parameters.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `name` | top level | string | Yes | Unique step identifier. |
| `type` | top level | string | Yes | Must be `loop.continue`. |

## Example: Skip benign alerts

```yaml
- name: process_alerts
  type: foreach
  foreach: "${{ event.alerts }}"
  steps:
    - name: filter_benign
      type: if
      condition: "foreach.item.kibana.alert.severity : low"
      steps:
        - name: next
          type: loop.continue

    - name: enrich
      type: virustotal.scanFileHash
      connector-id: "my-virustotal"
      with:
        hash: "{{ foreach.item.file.hash.sha256 }}"

    - name: record
      type: cases.addComment
      with:
        case_id: "{{ consts.case_id }}"
        comment: "Enriched: {{ foreach.item._id }} — {{ steps.enrich.output.stats.malicious }} hits"
```

Low-severity alerts are skipped; the loop moves on to the next alert without running `enrich` or `record`.

## Related

- [Flow control steps](/explore-analyze/workflows/steps/flow-control-steps.md): Overview of all flow-control types.
- [Loop break step](/explore-analyze/workflows/steps/loop-break.md): Exit the loop entirely instead of skipping to the next iteration.
- [Foreach step](/explore-analyze/workflows/steps/foreach.md) and [While step](/explore-analyze/workflows/steps/while.md): The loop types `loop.continue` can act on.
