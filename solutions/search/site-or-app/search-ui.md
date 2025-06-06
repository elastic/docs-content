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

A JavaScript library for the fast development of modern, engaging search experiences with [Elastic](https://www.elastic.co/). Get up and running quickly without re-inventing the wheel.


## Features 👍 [overview-features]

* **You know, for search** - Maintained by [Elastic](https://elastic.co), the team behind Elasticsearch.
* **Speedy Implementation** - Build a complete search experience with a few lines of code.
* **Customizable** - Tune the components, markup, styles, and behaviors to your liking.
* **Smart URLs** - Searches, paging, filtering, and more, are captured in the URL for direct result linking.
* **Flexible front-end** - Not just for React. Use with any JavaScript library, even vanilla JavaScript.
* **Flexible back-end** - Use it with Elasticsearch, Elastic Enterprise Search, or any other search API.
:::{important}
Enterprise Search is not available in {{stack}} 9.0+.
:::

## Get started 🌟 
* 📘 [Reference documentation](search-ui://reference/index.md): API docs, tutorials, and usage guides
    * [Quickstart tutorials](search-ui://reference/tutorials.md)
    * [Ecommerce examples](search-ui://reference/ecommerce.md)
    * [Basic usage](search-ui://reference/basic-usage.md)
    * [API reference](search-ui://reference/api-reference.md)
* 💻 [GitHub repository](https://github.com/elastic/search-ui): Source code, examples, and issue tracking

## Use Cases 🛠️ [overview-use-cases]


### Ecommerce [overview-ecommerce]

Search UI works great in the ecommerce use-case. Check out our [ecommerce guide](search-ui://reference/ecommerce.md) that includes demo and code examples, as well as general guidance for ecommerce search.


## FAQ 🔮 [overview-faq]


### Is Search UI only for React? [overview-is-search-ui-only-for-react]

Search UI is "headless". You can use vanilla JavaScript or write support for it into any JavaScript framework.

[Read about the search-ui package](https://github.com/elastic/search-ui/tree/main/packages/search-ui) for more information, or check out the [Vue.js Example](https://github.com/elastic/vue-search-ui-demo).


### Can I use my own styles? [overview-can-i-use-my-own-styles]

You can!

Read the [Custom Styles and Layout Guide](search-ui://reference/basic-usage.md) to learn more, or check out the [Seattle Indies Expo Demo](https://github.com/elastic/seattle-indies-expo-search).


### Can I build my own Components? [overview-can-i-build-my-own-components]

Yes! Absolutely.

Check out the [Build Your Own Component Guide](search-ui://reference/guides-creating-own-components.md).


### Does Search UI only work with App Search? [overview-does-search-ui-only-work-with-app-search]

Nope! We do have two first party connectors: Site Search and App Search.

But Search UI is headless. You can use *any* Search API.

Read the [Building a custom connector](search-ui://reference/guides-building-custom-connector.md) to learn more about building your own connector for your API.


### How do I use this with Elasticsearch? [overview-how-do-i-use-this-with-elasticsearch]

Read the [Elasticsearch Connector](search-ui://reference/api-connectors-elasticsearch.md) docs.


### Where do I report issues with the Search UI? [overview-where-do-i-report-issues-with-the-search-ui]

If something is not working as expected, open an [issue](https://github.com/elastic/search-ui/issues/new).


### Where can I go to get help? [overview-where-can-i-go-to-get-help]

The Enterprise Search team at Elastic maintains this library and are happy to help. Try posting your question to the [Elastic Enterprise Search](https://discuss.elastic.co/c/enterprise-search/84) discuss forums. Be sure to mention that you’re using Search UI and also let us know what backend your using; whether it’s App Search, Site Search, Elasticsearch, or something else entirely.


## Contribute 🚀 [overview-contribute]

We welcome contributors to the project. Before you begin, a couple notes…

* Read the [Search UI Contributor’s Guide](https://github.com/elastic/search-ui/blob/main/CONTRIBUTING.md).
* Prior to opening a pull request:

    * Create an issue to [discuss the scope of your proposal](https://github.com/elastic/search-ui/issues).
    * Sign the [Contributor License Agreement](https://www.elastic.co/contributor-agreement/). We are not asking you to assign copyright to us, but to give us the right to distribute your code without restriction. We ask this of all contributors in order to assure our users of the origin and continuing existence of the code. You only need to sign the CLA once.

* Write simple code and concise documentation, when appropriate.


## License 📗 [overview-license]

[Apache-2.0](https://github.com/elastic/search-ui/blob/main/LICENSE.txt) © [Elastic](https://github.com/elastic)

Thank you to all the [contributors](https://github.com/elastic/search-ui/graphs/contributors)! 🙏 🙏
