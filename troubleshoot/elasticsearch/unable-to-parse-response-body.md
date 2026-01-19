---
applies_to:
  stack:
navigation_title: "Error: Unable to parse response body"
---

# Fix error: Unable to parse response body [unable-to-parse-response-body]

```console
Error: Unable to parse response body
```

This error occurs when {{es}} cannot process a response body, possibly due to incorrect formatting or syntax. To resolve this issue, make sure the response body is in the correct format (usually JSON) and that all syntax is correct.

If the error persists, start with these general steps:
- Check the {{es}} logs for more detailed error messages.
- Update {{es}} to the latest version.

If you're using the high-level Java REST client, continue to the next section.

## Java REST client

:::{warning}
The Java REST client is deprecated. Use the [Java API client](elasticsearch-java://reference/index.md) instead.
:::


This error can occur when the high-level Java REST client cannot parse the response received by the low-level {{es}} client.

The REST high-level client acts as a wrapper around the low-level client. The low-level client ultimately performs the HTTP request to the cluster. If the response returned to the high-level client is malformed or does not comply with the expected schema, the client throws the `unable to parse response body` exception.

Use the following sections to identify and fix the root cause of the error.

### Version mismatch

{{es}} does not guarantee compatibility between different major versions. Make sure the client version matches the {{es}} version. For more details, refer to the [{{es}} Java server compatibility policy](elasticsearch-java://reference/index.md#_elasticsearch_server_compatibility_policy).

### Reverse proxy with path prefix

If your cluster is behind a reverse proxy and you have set a path prefix to access it, make sure to configure the high-level client to include the path prefix so the proxy routes the request to the cluster correctly.

For example, suppose you have an Nginx reverse proxy receiving connections at `mycompany.com:80`, and the `/elasticsearch` path prefix is set to proxy connections to a cluster running in your infrastructure. The `/elasticsearch` path prefix must be configured on the client you're using to access the cluster &mdash; not just on the host (`mycompany.com`).

Use `setPathPrefix()` to set the path prefix:

```java
new RestHighLevelClient(
  RestClient.builder(
    new HttpHost("mycompany.com", 80, DEFAULT_SCHEME_NAME))
    .setPathPrefix("/elasticsearch")
);
```

For more context, refer to these Elastic community forum posts:

- [RestHighLevelClient - Accessing an elastic http endpoint behind reverse proxy](https://discuss.elastic.co/t/resthighlevelclient-accessing-an-elastic-http-endpoint-behind-reverse-proxy/117306)
- [Issue with HighLevelRestClient with the host = xyz.com:8080/elasticsearch](https://discuss.elastic.co/t/issue-with-highlevelrestclient-with-the-host-xyz-com-8080-elasticsearch/186384)

### HTTP size limit

The `unable to parse response body` error can occur when bulk indexing a large volume of data. By default, {{es}} has a maximum HTTP request body size of 100 MB. To raise this limit, increase the value of `http.max_content_length` in the {{es}} configuration file.

```yaml
http.max_content_length: 200mb
```

For an example of an HTTP size limit issue, refer to this Elastic community forum post: [Bulk indexing with java high level rest client gives error](https://discuss.elastic.co/t/bulk-indexing-with-java-high-level-rest-client-gives-error-unable-to-parse-response-body/161696)

### Kubernetes with ingress controller

If your {{es}} cluster runs on Kubernetes and is exposed through an ingress controller, check your ingress controller configuration. Misrouted or malformed responses from the controller can cause parsing errors in the client.

For an example of incorrect SSL redirection in an ingress controller, refer to this Elastic community forum post: [RestHighLevelClient - Unable to parse response body](https://discuss.elastic.co/t/resthighlevelclient-unable-to-parse-response-body/240809)

