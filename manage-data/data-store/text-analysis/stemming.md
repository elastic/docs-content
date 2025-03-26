---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/stemming.html
applies_to:
  stack: ga
  serverless: ga
---

# Stemming [stemming]

*Stemming* is the process of reducing a word to its root form. This ensures variants of a word match during a search.

For example, `walking` and `walked` can be stemmed to the same root word: `walk`. Once stemmed, an occurrence of either word would match the other in a search.

Stemming is language-dependent but often involves removing prefixes and suffixes from words.

In some cases, the root form of a stemmed word may not be a real word. For example, `jumping` and `jumpiness` can both be stemmed to `jumpi`. While `jumpi` isn’t a real English word, it doesn’t matter for search; if all variants of a word are reduced to the same root form, they will match correctly.

## Stemmer token filters [stemmer-token-filters]

In {{es}}, stemming is handled by stemmer [token filters](anatomy-of-an-analyzer.md#analyzer-anatomy-token-filters). These token filters can be categorized based on how they stem words:

* [Algorithmic stemmers](#algorithmic-stemmers), which stem words based on a set of rules
* [Dictionary stemmers](#dictionary-stemmers), which stem words by looking them up in a dictionary

Because stemming changes tokens, we recommend using the same stemmer token filters during [index and search analysis](index-search-analysis.md).


## Algorithmic stemmers [algorithmic-stemmers]

Algorithmic stemmers apply a series of rules to each word to reduce it to its root form. For example, an algorithmic stemmer for English may remove the `-s` and `-es` suffixes from the end of plural words.

Algorithmic stemmers have a few advantages:

* They require little setup and usually work well out of the box.
* They use little memory.
* They are typically faster than [dictionary stemmers](#dictionary-stemmers).

However, most algorithmic stemmers only alter the existing text of a word. This means they may not work well with irregular words that don’t contain their root form, such as:

* `be`, `are`, and `am`
* `mouse` and `mice`
* `foot` and `feet`

The following token filters use algorithmic stemming:

* [`stemmer`](elasticsearch://reference/text-analysis/analysis-stemmer-tokenfilter.md), which provides algorithmic stemming for several languages, some with additional variants.
* [`kstem`](elasticsearch://reference/text-analysis/analysis-kstem-tokenfilter.md), a stemmer for English that combines algorithmic stemming with a built-in dictionary.
* [`porter_stem`](elasticsearch://reference/text-analysis/analysis-porterstem-tokenfilter.md), our recommended algorithmic stemmer for English.
* [`snowball`](elasticsearch://reference/text-analysis/analysis-snowball-tokenfilter.md), which uses [Snowball](https://snowballstem.org/)-based stemming rules for several languages.


## Dictionary stemmers [dictionary-stemmers]

Dictionary stemmers look up words in a provided dictionary, replacing unstemmed word variants with stemmed words from the dictionary.

In theory, dictionary stemmers are well suited for:

* Stemming irregular words
* Discerning between words that are spelled similarly but not related conceptually, such as:

    * `organ` and `organization`
    * `broker` and `broken`


In practice, algorithmic stemmers typically outperform dictionary stemmers. This is because dictionary stemmers have the following disadvantages:

* **Dictionary quality**<br> A dictionary stemmer is only as good as its dictionary. To work well, these dictionaries must include a significant number of words, be updated regularly, and change with language trends. Often, by the time a dictionary has been made available, it’s incomplete and some of its entries are already outdated.
* **Size and performance**<br> Dictionary stemmers must load all words, prefixes, and suffixes from its dictionary into memory. This can use a significant amount of RAM. Low-quality dictionaries may also be less efficient with prefix and suffix removal, which can slow the stemming process significantly.

You can use the [`hunspell`](elasticsearch://reference/text-analysis/analysis-hunspell-tokenfilter.md) token filter to perform dictionary stemming.

::::{tip}
If available, we recommend trying an algorithmic stemmer for your language before using the [`hunspell`](elasticsearch://reference/text-analysis/analysis-hunspell-tokenfilter.md) token filter.

::::



## Control stemming [control-stemming]

Sometimes stemming can produce shared root words that are spelled similarly but not related conceptually. For example, a stemmer may reduce both `skies` and `skiing` to the same root word: `ski`.

To prevent this and better control stemming, you can use the following token filters:

* [`stemmer_override`](elasticsearch://reference/text-analysis/analysis-stemmer-override-tokenfilter.md), which lets you define rules for stemming specific tokens.
* [`keyword_marker`](elasticsearch://reference/text-analysis/analysis-keyword-marker-tokenfilter.md), which marks specified tokens as keywords. Keyword tokens are not stemmed by subsequent stemmer token filters.
* [`conditional`](elasticsearch://reference/text-analysis/analysis-condition-tokenfilter.md), which can be used to mark tokens as keywords, similar to the `keyword_marker` filter.

For built-in [language analyzers](elasticsearch://reference/text-analysis/analysis-lang-analyzer.md), you also can use the [`stem_exclusion`](elasticsearch://reference/text-analysis/analysis-lang-analyzer.md#_excluding_words_from_stemming) parameter to specify a list of words that won’t be stemmed.


