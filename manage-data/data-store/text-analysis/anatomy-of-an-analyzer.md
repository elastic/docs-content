---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer-anatomy.html
---

# Anatomy of an analyzer [analyzer-anatomy]

An *analyzer*  — whether built-in or custom — is just a package which contains three lower-level building blocks: *character filters*, *tokenizers*, and *token filters*.

The built-in [analyzers](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html) pre-package these building blocks into analyzers suitable for different languages and types of text. Elasticsearch also exposes the individual building blocks so that they can be combined to define new [`custom`](create-custom-analyzer.md) analyzers.

## Character filters [analyzer-anatomy-character-filters]

A *character filter* receives the original text as a stream of characters and can transform the stream by adding, removing, or changing characters. For instance, a character filter could be used to convert Hindu-Arabic numerals (٠‎١٢٣٤٥٦٧٨‎٩‎) into their Arabic-Latin equivalents (0123456789), or to strip HTML elements like `<b>` from the stream.

An analyzer may have **zero or more** [character filters](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-charfilters.html), which are applied in order.


## Tokenizer [analyzer-anatomy-tokenizer]

A *tokenizer* receives a stream of characters, breaks it up into individual *tokens* (usually individual words), and outputs a stream of *tokens*. For instance, a [`whitespace`](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-whitespace-tokenizer.html) tokenizer breaks text into tokens whenever it sees any whitespace. It would convert the text `"Quick brown fox!"` into the terms `[Quick, brown, fox!]`.

The tokenizer is also responsible for recording the order or *position* of each term and the start and end *character offsets* of the original word which the term represents.

An analyzer must have **exactly one** [tokenizer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html).


## Token filters [analyzer-anatomy-token-filters]

A *token filter* receives the token stream and may add, remove, or change tokens. For example, a [`lowercase`](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-lowercase-tokenfilter.html) token filter converts all tokens to lowercase, a [`stop`](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-stop-tokenfilter.html) token filter removes common words (*stop words*) like `the` from the token stream, and a [`synonym`](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-tokenfilter.html) token filter introduces synonyms into the token stream.

Token filters are not allowed to change the position or character offsets of each token.

An analyzer may have **zero or more** [token filters](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenfilters.html), which are applied in order.


