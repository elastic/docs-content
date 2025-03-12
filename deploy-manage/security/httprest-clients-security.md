---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/http-clients.html
---

# HTTP/REST clients and security [http-clients]

The {{es}} {{security-features}} work with standard HTTP [basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) headers to authenticate users. Since Elasticsearch is stateless, this header must be sent with every request:

```shell
Authorization: Basic <TOKEN> <1>
```

1. The `<TOKEN>` is computed as `base64(USERNAME:PASSWORD)`


Alternatively, you can use [token-based authentication services](../users-roles/cluster-or-deployment-auth/token-based-authentication-services.md).


## Client examples [http-clients-examples]

This example uses `curl` without basic auth to create an index:

```shell
curl -XPUT 'localhost:9200/idx'
```

```js
{
  "error":  "AuthenticationException[Missing authentication token]",
  "status": 401
}
```

Since no user is associated with the request above, an authentication error is returned. Now we’ll use `curl` with basic auth to create an index as the `rdeniro` user:

```shell
curl --user rdeniro:taxidriver -XPUT 'localhost:9200/idx'
```

```js
{
  "acknowledged": true
}
```


## Secondary authorization [http-clients-secondary-authorization]

Some APIs support secondary authorization headers for situations where you want tasks to run with a different set of credentials. For example, you can send the following header in addition to the basic authentication header:

```shell
es-secondary-authorization: Basic <TOKEN> <1>
```

1. The `<TOKEN>` is computed as `base64(USERNAME:PASSWORD)`


The `es-secondary-authorization` header has the same syntax as the `Authorization` header. It therefore also supports the use of [token-based authentication services](../users-roles/cluster-or-deployment-auth/token-based-authentication-services.md). For example:

```shell
es-secondary-authorization: ApiKey <TOKEN> <1>
```

1. The `<TOKEN>` is computed as `base64(API key ID:API key)`



## Client libraries over HTTP [http-clients-libraries]

For more information about using {{security-features}} with the language specific clients, refer to:

* [Java](elasticsearch-java://reference/_basic_authentication.md)
* [JavaScript](elasticsearch-js://reference/connecting.md)
* [.NET](elasticsearch-net://reference/configuration.md)
* [Perl](https://metacpan.org/pod/Search::Elasticsearch::Cxn::HTTPTiny#CONFIGURATION)
* [PHP](elasticsearch-php://reference/connecting.md)
* [Python](https://elasticsearch-py.readthedocs.io/en/master/#ssl-and-authentication)
* [Ruby](https://github.com/elasticsearch/elasticsearch-ruby/tree/master/elasticsearch-transport#authentication)

