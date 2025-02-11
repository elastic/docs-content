---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-painless.html
---

# Painless scripting language [modules-scripting-painless]

*Painless* is a performant, secure scripting language designed specifically for {{es}}. You can use Painless to safely write inline and stored scripts anywhere scripts are supported in {{es}}.

$$$painless-features$$$
Painless provides numerous capabilities that center around the following core principles:

* **Safety**: Ensuring the security of your cluster is of utmost importance. To that end, Painless uses a fine-grained allowlist with a granularity down to the members of a class. Anything that is not part of the allowlist results in a compilation error. See the [Painless API Reference](https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-api-reference.html) for a complete list of available classes, methods, and fields per script context.
* **Performance**: Painless compiles directly into JVM bytecode to take advantage of all possible optimizations that the JVM provides. Also, Painless typically avoids features that require additional slower checks at runtime.
* **Simplicity**: Painless implements a syntax with a natural familiarity to anyone with some basic coding experience. Painless uses a subset of Java syntax with some additional improvements to enhance readability and remove boilerplate.


## Start scripting [_start_scripting]

Ready to start scripting with Painless? Learn how to [write your first script](modules-scripting-using.md).

If you’re already familiar with Painless, see the [Painless Language Specification](https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-lang-spec.html) for a detailed description of the Painless syntax and language features.
