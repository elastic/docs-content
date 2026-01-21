---
navigation_title: Painless
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-painless.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Introduction to Painless [modules-scripting-painless]

:::{tip}
This introduction is designed for users new to Painless scripting. If you're already familiar with Painless, refer to the [Painless language specification](elasticsearch://reference/scripting-languages/painless/painless-language-specification.md) for syntax details and advanced features.
:::

Painless is a secure, performant, and flexible scripting language designed specifically for {{es}}. As the default scripting language for {{es}}, Painless lets you safely customize search behavior, data processing, and operations workflows across your {[stack]} deployments.

## What is Painless?

Painless was introduced in [{{es}} 5.0](https://www.elastic.co/blog/painless-a-new-scripting-language) as a replacement for Groovy, with improved security and performance compared to previous scripting solutions. Built on the [Java Virtual Machine (JVM)](https://docs.oracle.com/en/java/javase/24/vm/java-virtual-machine-technology-overview.html), Painless provides the familiar syntax of Java while improving the security boundaries with guardrails and a sandbox environment.

Unlike general scripting languages, Painless is purpose-built for {{es}}, enabling native performance while preventing unauthorized access to system resources. This architecture makes Painless both powerful for data manipulation and safe for production environments.

Common use cases include creating new fields based on existing data, calculating time differences between dates, extracting structured data from log messages, and implementing custom business logic in search scoring. For more examples, refer to our step-by-step [tutorials](/explore-analyze/scripting/common-script-uses.md). 

## Benefits

Painless enables scripting in various contexts throughout {{es}}, such as:

### Search enhancement

* Custom search scoring based on business requirements  
* Runtime field creation that calculates values during query execution  
* Real-time filtering and transformation without reindexing data

### Data processing

* Transform documents during indexing  
* Parse and extract structured data from unstructured fields  
* Calculate metrics and summaries from your data

### Operational automation

* Monitor data patterns and trigger alerts with Watcher solutions  
* Transform alert payloads for targeted notifications and actions

## How it works

You can write Painless scripts inline for quick operations or create reusable functions for your data operation. Here’s a sample Painless script applied to data transformation:

```java
String productTitle(String manufacturer, String productName) {
  return manufacturer + " - " + productName;
}

return productTitle("Elitelligence", "Winter jacket");
```

This script demonstrates a few facets of Painless scripting:

* **Function definition:** Custom `productTitle` function with typed parameters  
* **Data types:** String and integer parameter handling  
* **Return values:** Function returns formatted string output

Painless provides three core benefits across all scripting contexts:

* **Security:** Fine-grained allowlists that prevent access to restricted Java APIs.  
* **Performance**: Direct compilation to [bytecode](https://docs.oracle.com/javase/specs/jvms/se7/html/jvms-6.html) eliminates interpretation overhead and leverages JVM optimization.  
* **Flexibility**: Wide range of scripting syntax and contexts across {{es}}, from search scoring to data processing to operational processing.

## Where to write in Painless

You can use Painless in multiple contexts throughout {{es}}:

* [**Dev Tools Console**](/explore-analyze/query-filter/tools/console.md)**:** for interactive script development and testing  
* [**Ingest pipelines**](/manage-data/ingest/transform-enrich/ingest-pipelines.md)**:** for data transformation during indexing  
* [**Search queries**](/solutions/search.md)**:** for custom scoring and script fields  
* [**Runtime fields**](/manage-data/data-store/mapping/runtime-fields.md)**:** for dynamic field creation  
* [**Update API:**](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update) for document modification  
* [**Watcher**](/explore-analyze/alerts-cases/watcher.md)**:** for alert conditions and actions

## Start scripting

Write your first Painless script by trying out our [guide](/explore-analyze/scripting/modules-scripting-using.md) or jump into one of our [tutorials](/explore-analyze/scripting/common-script-uses.md) for real-world examples using sample data.

For complete syntax and language features, refer to the [Painless language specification](elasticsearch://reference/scripting-languages/painless/painless-language-specification.md).
