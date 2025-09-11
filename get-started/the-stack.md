---
mapped_pages:
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/stack-components.html
  - https://www.elastic.co/guide/en/kibana/current/introduction.html
  - https://www.elastic.co/guide/en/kibana/current/index.html
  - https://www.elastic.co/guide/en/elastic-stack/current/installing-elastic-stack.html
  - https://www.elastic.co/guide/en/elastic-stack/current/overview.html
products:
  - id: elastic-stack
  - id: kibana
---

# The {{stack}}

Elastic's Search AI platform is built around the {{stack}}, a group of open source products and components designed for ingesting, storing, searching, analyzing, and visualizing data.

Continue reading to learn how these components work together.

### Store your data

{{es}} is the heart of the Elastic Stack, functioning as the central place to store and search your data. It stores data as **JSON documents**, which are structured data objects. These documents are organized into **indices**, which you can think of as collections of similar documents.

Elasticsearch is built to be a resilient and scalable distributed system. It runs as a **cluster** of one or more servers, called **nodes**. When you add data to an index, it's divided into pieces called **shards**, which are spread across the various nodes in the cluster. This architecture allows Elasticsearch to handle large volumes of data and ensures that your data remains available even if a node fails.

Learn more in [The {{es}} data store](/manage-data/data-store.md).

### Visualize and query your data [kibana-navigation-search]

While {{es}} stores your data, **Kibana** is the user interface where you can explore, visualize, and manage it. It provides a window into your data, allowing you to quickly gain insights and understand trends.

With Kibana, you can:

* Use **Discover** to interactively search and filter your raw data.  
* Build custom **visualizations** like charts, graphs, and metrics with tools like **Lens**, which offers a drag-and-drop experience.  
* Assemble your visualizations into interactive **dashboards** to get a comprehensive overview of your information.  
* Analyze geospatial data using the powerful **Maps** application.

At the same time, Kibana works as the user interface of all Elastic solutions, like Elastic Security and Elastic Observability, providing ways of configuring Elastic to suit your needs and offering interactive guidance.

A **query** is a question you ask about your data, and Elastic provides several powerful languages to do so. You can query data directly through the API or through the user interface in Kibana.

* **Query DSL** is a full-featured JSON-style query language that enables complex searching, filtering, and aggregations. It is the original and most powerful query language for Elasticsearch today.
* **Elasticsearch Query Language (ES|QL)** is a powerful, modern query language that uses a familiar pipe-based syntax to transform and aggregate your data at search time.  
* **Event Query Language (EQL)** is a specialized language designed to query sequences of events, which is particularly useful for security analytics and threat hunting.
* **Kibana Query Language (KQL)** is the text-based language used in the **Discover** search bar, perfect for interactive filtering and exploration.  

Learn more in [](/explore-analyze/index.md).

### Use the APIs to automate operations and management

Nearly every aspect of Elasticsearch can be configured and managed programmatically through its extensive REST APIs. This allows you to automate repetitive tasks and integrate Elastic management into your existing operational workflows. You can use the APIs to manage indices, update cluster settings, run complex queries, and configure security. 

The **Console** tool in Kibana provides an interactive way to send requests directly to the Elasticsearch API and view the responses. For secure, automated access, you can create and manage **API keys** to authenticate your scripts and applications. This API-first approach is fundamental to enabling infrastructure-as-code practices and managing your deployments at scale.

Learn more in [Elastic APIs](https://www.elastic.co/docs/api).