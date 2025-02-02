# Text analysis [analysis]

*Text analysis* is the process of converting unstructured text, like the body of an email or a product description, into a structured format that’s [optimized for search](../../../solutions/search/full-text.md).


## When to configure text analysis [when-to-configure-analysis] 

{{es}} performs text analysis when indexing or searching [`text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) fields.

If your index doesn’t contain `text` fields, no further setup is needed; you can skip the pages in this section.

However, if you use `text` fields or your text searches aren’t returning results as expected, configuring text analysis can often help. You should also look into analysis configuration if you’re using {{es}} to:

* Build a search engine
* Mine unstructured data
* Fine-tune search for a specific language
* Perform lexicographic or linguistic research


## In this section [analysis-toc] 

* [Overview](../../../manage-data/data-store/text-analysis.md)
* [Concepts](../../../manage-data/data-store/text-analysis/concepts.md)
* [*Configure text analysis*](../../../manage-data/data-store/text-analysis/configure-text-analysis.md)
* [*Built-in analyzer reference*](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html)
* [*Tokenizer reference*](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html)
* [*Token filter reference*](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenfilters.html)
* [*Character filters reference*](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-charfilters.html)
* [*Normalizers*](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-normalizers.html)

