---
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Learn when to use each detection rule type and access detailed guides for custom query, EQL, threshold, and more.
---

# Rule type guides

{{elastic-sec}} provides several rule types for building detections. Each rule type page covers when to use it, how to write effective queries, real-world examples, and field configuration specific to that type.

Not sure which rule type fits your use case? Refer to [Select the right rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md) for a decision guide comparing all rule types.

| If you want to detect... | Rule type |
|---|---|
| A known field value, pattern, or boolean condition | [Custom query](/solutions/security/detect-and-alert/custom-query.md) |
| An ordered sequence of events or a missing event | [Event correlation (EQL)](/solutions/security/detect-and-alert/eql.md) |
| A field value count exceeding a boundary | [Threshold](/solutions/security/detect-and-alert/threshold.md) |
| Events matching a known threat indicator | [Indicator match](/solutions/security/detect-and-alert/indicator-match.md) |
| A field value appearing for the first time | [New terms](/solutions/security/detect-and-alert/new-terms.md) |
| Aggregated, transformed, or computed conditions | [{{esql}}](/solutions/security/detect-and-alert/esql.md) |
| Behavioral anomalies without a fixed pattern | [{{ml-cap}}](/solutions/security/detect-and-alert/machine-learning.md) |
