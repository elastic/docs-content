---
navigation_title: Search UI
mapped_pages:
  - https://www.elastic.co/guide/en/search-ui/current/overview.html
  - https://www.elastic.co/guide/en/search-ui/current/index.html
applies_to:
  stack:
  serverless:
products:
  - id: search-ui
---

# What is Search UI? [overview]

Search UI is a JavaScript library from [Elastic](https://www.elastic.co/). It helps you create modern and customizable search experiences. You can use it with Elasticsearch or other search APIs. It helps developers build complete search interfaces quickly, with minimal boilerplate.

As a headless library, Search UI separates logic from presentation. You can use it with React, vanilla JavaScript, or any front-end framework. You can use built-in React components for quick development. Or, you can create your own from the ground up.

Search UI supports advanced capabilities like customizable query behavior, smart URL handling (capturing filters, paging, and queries in the URL), and flexible backend integration through connectors. It works seamlessly with Elasticsearch and also supports custom backends via custom connectors.

:::{important}
Enterprise Search is not available in {{stack}} 9.0+.
:::

## Get started
* [Reference documentation](search-ui://reference/index.md): API docs, tutorials, and usage guides
    * [Quickstart tutorials](search-ui://reference/tutorials.md)
    * [Ecommerce examples](search-ui://reference/ecommerce.md)
    * [Basic usage](search-ui://reference/basic-usage.md)
    * [API reference](search-ui://reference/api-reference.md)
* [GitHub repository](https://github.com/elastic/search-ui): Source code, examples, and issue tracking

## Live demos [overview-live-demos]

### Connectors [overview-connectors]

- [Elasticsearch](https://codesandbox.io/s/github/elastic/search-ui/tree/main/examples/sandbox?from-embed=&initialpath=/elasticsearch&file=/src/pages/elasticsearch/index.js)
- [Elastic Site Search (Swiftype)](https://codesandbox.io/s/github/elastic/search-ui/tree/main/examples/sandbox?from-embed=&initialpath=/site-search&file=/src/pages/site-search/index.js)

### Examples [overview-examples]

- [Search as you type](https://codesandbox.io/s/github/elastic/search-ui/tree/main/examples/sandbox?from-embed=&initialpath=/search-as-you-type&file=/src/pages/search-as-you-type/index.js)
- [Search bar in header](https://codesandbox.io/s/github/elastic/search-ui/tree/main/examples/sandbox?from-embed=&initialpath=/search-bar-in-header&file=/src/pages/search-bar-in-header/index.js)
- [Customizing Styles and Components](https://codesandbox.io/s/github/elastic/search-ui/tree/main/examples/sandbox?from-embed=&initialpath=/customizing-styles-and-html&file=/src/pages/customizing-styles-and-html/index.js)
