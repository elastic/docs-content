---
navigation_title: Clients
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/index.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-clients.html
products:
  - id: cloud-serverless
---

# Elasticsearch clients [elasticsearch-clients]

{{es}} is easy to use from most popular programming languages, thanks to the wide range of official libraries and developer tools available.


## Language client overview

|  Language            | Quick install (lastest version)                      | Docs                                            | Source                                                |
|----------------------|------------------------------------------------------|-------------------------------------------------|-------------------------------------------------------|
| Python               | `pip install elasticsearch`                          | [docs](elasticsearch-py://reference/index.md)   | [repo](https://github.com/elastic/elasticsearch-py)   |
| Java                 | ([project configuration](elasticsearch-java://reference/setup/installation.md)) | [docs](elasticsearch-java://reference/index.md) | [repo](https://github.com/elastic/elasticsearch-java) |
| JavaScript / Node.js | `npm install @elastic/elasticsearch`                 | [docs](elasticsearch-js://reference/index.md)   | [repo](https://github.com/elastic/elasticsearch-js)   |
| C# / .NET            | `dotnet add package Elastic.Clients.Elasticsearch`   | [docs](elasticsearch-net://reference/index.md)  | [repo](https://github.com/elastic/elasticsearch-net)  |
| PHP                  | `composer require elasticsearch/elasticsearch`       | [docs](elasticsearch-php://reference/index.md)  | [repo](https://github.com/elastic/elasticsearch-php)  |
| Go                   | `require github.com/elastic/go-elasticsearch/v9 9.0` | [docs](go-elasticsearch://reference/index.md)   | [repo](https://github.com/elastic/go-elasticsearch)   |
| Ruby                 | `gem install elasticsearch`                          | [docs](elasticsearch-ruby://reference/index.md) | [repo](https://github.com/elastic/elasticsearch-ruby) |
| Rust (experimental)  | `cargo add elasticsearch`                            | [docs](elasticsearch-rs://reference/index.md)   | [repo](https://github.com/elastic/elasticsearch-rs)   |


## Releases and compatibility

{{es}} client libraries are released for every {{es}} server major or minor release.
Patches are released independently to allow for faster bugfixes.
This release policy does not affect compatibility; for example, version 8.13.x of the client will be compatible with versions of the server 8.13.y where y >= x.

The {{es}} clients are forward compatible, meaning that the client supports communicating with greater or equal minor versions of {{es}} without breaking.
It does not mean that the client automatically supports new features of newer {{es}} versions; that is only possible after the release of a new client version.
For example, an 8.12 client will not automatically support the new features of {{es}} 8.13; the 8.13 client version is required for that.
{{es}} language clients are only backwards compatible with default distributions and without guarantees made.

:::{note}
When upgrading {{es}} it is strongly recommended to upgrade the server first, _before_ the client.
The forward compatibility policy allows client applications to continue to work with the new server before the client itself is upgraded.
:::


## Local server development

For development and testing on a local {{es}} server, [start-local](https://github.com/elastic/start-local) is recommended:

```bash
curl -fsSL https://elastic.co/start-local | sh
```

Alternatively, learn how to [connect to your {{es}} endpoint](/solutions/elasticsearch-solution-project/search-connection-details.md) for other types of deployment.
