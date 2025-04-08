---
applies_to:
  stack: 
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
navigation_title: "Error: unable to parse response body"
# is mapped_pages needed for newly created docs?
---

# Fix unable to parse response body error [unable-to-parse-response-body]

```console
Error: Unable to parse response body
```

This error occurs when Elasticsearch cannot understand the response body it received, possibly due to incorrect formatting or syntax. To resolve this, ensure that the response body is in the correct format (usually JSON) and that all syntax is correct. If the error persists, check the Elasticsearch logs for more detailed error messages. It could also be due to a bug in the Elasticsearch version you’re using, so consider updating to the latest version.

## Overview

This error is typically related to the REST High Level Client and it occurs whenever the client cannot parse the response received by Elasticsearch’s low-level client.

## What it means

The REST High Level Client acts as a wrapper around the low-level client. The latter is the one that will ultimately perform the HTTP request to the cluster. If for any reason the response returned to the High Level Client is broken or does not comply with the schema it is expecting, then it will throw the “Unable to parse response body” exception.

## Why it occurs

Below are a few scenarios where users reported receiving this error, and the likely causes:

### Version mismatch between the client and the cluster

Elastic does not guarantee that it will maintain the compatibility between different major versions. If you’re running a 6.x cluster, but your application uses a 7.x version of the High Level Client, this could be what is causing the issue, due to differences in the response schema.

You can learn more about compatibility for the High Level REST client [here](https://www.elastic.co/guide/en/elasticsearch/client/java-rest/current/java-rest-high-compatibility.html).

### The cluster is behind a reverse proxy with a path prefix

If your cluster is behind a reverse proxy and you have set a path prefix to access it, you need to make sure to correctly configure the High Level Client so it reaches and gets a response from the cluster itself, as opposed to from the reverse proxy. If your client is getting the response from the reverse proxy service this could be what is causing the “Unable to parse response body” exception.

Suppose you have an Nginx reverse proxy receiving connections at `mycompany.com:80` and you have set the `/elasticsearch` path prefix that will proxy connections to a cluster running inside your infrastructure. In this case you should make sure the path prefix is properly configured in the configuration file of the client you’re using to access the cluster, not only the host (`mycompany.com` in this case).

If you have an app that uses the High Level Client to access the cluster you can use the `setPathPrefix()` to set the path prefix, like so:

```java
new RestHighLevelClient(
  RestClient.builder(
    new HttpHost("mycompany.com", 80, DEFAULT_SCHEME_NAME))
    .setPathPrefix("/elasticsearch")
);
```

This [post](https://discuss.elastic.co/t/resthighlevelclient-accessing-an-elastic-http-endpoint-behind-reverse-proxy/117306) and [this post](https://discuss.elastic.co/t/issue-with-highlevelrestclient-with-the-host-xyz-com-8080-elasticsearch/186384) might be helpful.

### You are reaching the HTTP size limit

Some users have reported the “Unable to parse response body” error when bulk indexing a huge volume of data. This happens because Elasticsearch by default has a maximum size of HTTP request body of 100MB. You can change this by adjusting the `http.max_content_length` setting in the Elasticsearch configuration file.

```yaml
http.max_content_length: 200mb
```

This [post](https://discuss.elastic.co/t/bulk-indexing-with-java-high-level-rest-client-gives-error-unable-to-parse-response-body/161696) is an example of such a case and could be helpful if you’re facing a similar situation.

### The cluster is running on Kubernetes and its entrypoint is through an Ingress Controller

If you have your cluster running inside a Kubernetes cluster and the entrypoint for the Elasticsearch service is through an Ingress Controller, then you should double check your Ingress configuration, since it is a moving piece between your clients and your cluster.

Check out [this post](https://discuss.elastic.co/t/resthighlevelclient-unable-to-parse-response-body/240809) to see an example of misconfiguration in the Ingress Controller related to redirecting incoming connections through SSL, which was not actually configured and therefore was the root cause of the problem that ultimately caused the “Unable to parse response body” exception.

## How to resolve it

Here is a checklist to go through when trying to solve the “Unable to parse response body” error:

- Are the client (your App, a third-party tool, even an Elastic tool like Logstash) and the cluster version compatible (same major version)?
- Are you bulk indexing a huge amount of data? Try to increase the `http.max_content_length` setting in the `elasticsearch.yml` configuration file.
- Is your cluster behind a reverse proxy?
  - Make sure your client is accessing the exact path configured in your proxy that will redirect the request to the cluster.
  - Could any other configuration in the reverse proxy be causing the request to fail? Maybe you have a request rate limit or any other request policy in place in your reverse proxy service and this could be causing the request not to reach the cluster. In this case the client will receive a response from the reverse proxy itself and it will not be able to parse the response body (as it would definitely not comply with the expected schema).
- Running Elasticsearch on Kubernetes with an Ingress Controller acting as the entrypoint? Double check your Ingress configurations and make sure you can definitely reach the cluster.

