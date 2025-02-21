---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/configure-text-analysis.html
applies_to:
  stack: ga
  serverless: ga
---

# Configure text analysis [configure-text-analysis]

By default, {{es}} uses the [`standard` analyzer](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analysis-standard-analyzer.md) for all text analysis. The `standard` analyzer gives you out-of-the-box support for most natural languages and use cases. If you chose to use the `standard` analyzer as-is, no further configuration is needed.

If the standard analyzer does not fit your needs, review and test {{es}}'s other built-in [built-in analyzers](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analyzer-reference.md). Built-in analyzers don’t require configuration, but some support options that can be used to adjust their behavior. For example, you can configure the `standard` analyzer with a list of custom stop words to remove.

If no built-in analyzer fits your needs, you can test and create a custom analyzer. Custom analyzers involve selecting and combining different [analyzer components](anatomy-of-an-analyzer.md), giving you greater control over the process.

* [Test an analyzer](test-an-analyzer.md)
* [Configuring built-in analyzers](configuring-built-in-analyzers.md)
* [Create a custom analyzer](create-custom-analyzer.md)
* [Specify an analyzer](specify-an-analyzer.md)





