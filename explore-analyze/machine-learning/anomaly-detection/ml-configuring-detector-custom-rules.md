---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-configuring-detector-custom-rules.html
---

# Customizing detectors with custom rules [ml-configuring-detector-custom-rules]

[Custom rules](ml-ad-run-jobs.md#ml-ad-rules) – or *job rules* as {{kib}} refers to them – enable you to change the behavior of anomaly detectors based on domain-specific knowledge.

Custom rules describe *when* a detector should take a certain *action* instead of following its default behavior. To specify the *when* a rule uses a `scope` and `conditions`. You can think of `scope` as the categorical specification of a rule, while `conditions` are the numerical part. A rule can have a scope, one or more conditions, or a combination of scope and conditions. For the full list of specification details, see the [`custom_rules` object](https://www.elastic.co/guide/en/elasticsearch/reference/current/ml-put-job.html#put-customrules) in the create {{anomaly-jobs}} API.





