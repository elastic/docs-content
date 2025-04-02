---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html
applies_to:
  stack:
  serverless:
---

# Text analysis during search [analysis]

*Text analysis* is the process of converting unstructured text, like the body of an email or a product description, into a structured format that’s [optimized for search](../full-text.md).


## When to configure text analysis [when-to-configure-analysis]

{{es}} performs text analysis when indexing or searching [`text`](elasticsearch://reference/elasticsearch/mapping-reference/text.md) fields.

If your index doesn’t contain `text` fields, no further setup is needed; you can skip the pages in this section.

However, if you use `text` fields or your text searches aren’t returning results as expected, configuring text analysis can often help. You should also look into analysis configuration if you’re using {{es}} to:

* Build a search engine
* Mine unstructured data
* Fine-tune search for a specific language
* Perform lexicographic or linguistic research


## Learn more [analysis-toc]

Learn more about text analysis in the **Manage Data** section of the documentation:

* [Overview](../../../manage-data/data-store/text-analysis.md)
* [Concepts](../../../manage-data/data-store/text-analysis/concepts.md)
* [*Configure text analysis*](../../../manage-data/data-store/text-analysis/configure-text-analysis.md)
* [*Built-in analyzer reference*](elasticsearch://reference/text-analysis/analyzer-reference.md)
* [*Tokenizer reference*](elasticsearch://reference/text-analysis/tokenizer-reference.md)
* [*Token filter reference*](elasticsearch://reference/text-analysis/token-filter-reference.md)
* [*Character filters reference*](elasticsearch://reference/text-analysis/character-filter-reference.md)
* [*Normalizers*](elasticsearch://reference/text-analysis/normalizers.md)

