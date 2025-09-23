---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-api-info.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# APM Server information API [apm-api-info]

The APM Server exposes an API endpoint to query general server information. This lightweight endpoint is useful as a server up/down health check.

## Server Information endpoint [apm-api-info-endpoint]

This is the server information endpoint:

```bash
http(s)://{hostname}:{port}/
```

Sending an `HTTP GET` request to the server information endpoint will return an HTTP 200, indicating that the server is up.

To configure authenticated access to the APM server, the instructions at [APM API key](/solutions/observability/apm/api-keys.md) or [APM Secret Token](/solutions/observability/apm/secret-token.md), must be followed to configure the correct permissions for APM access.

If an [API keys](/solutions/observability/apm/api-keys.md) or a [Secret token](/solutions/observability/apm/secret-token.md) is passed along with the `HTTP GET` request, in addition to an HTTP 200, the response payload will include some information about the APM server.

### Example: GET, without credentials [apm-api-info-example-get-without-credentials]

Example APM Server status request with GET, without credentials:

```sh
curl --verbose -X GET http://127.0.0.1:8200

*   Trying 127.0.0.1:8200...
* TCP_NODELAY set
* Connected to 127.0.0.1 (10.244.3.40) port 8200 (#0)
> GET / HTTP/1.1
> Host: 127.0.0.1:8200
> User-Agent: curl/7.68.0
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< X-Content-Type-Options: nosniff
< Date: Tue, 17 Oct 2023 22:04:05 GMT
< Content-Length: 0
<
* Connection #0 to host 127.0.0.1 left intact
```

### Example: GET, with secret token [apm-api-info-example-get-with-secret-token]

Example APM Server information request with GET, with a [Secret token](/solutions/observability/apm/secret-token.md):

```sh
curl -X GET http://127.0.0.1:8200/ \
  -H "Authorization: Bearer secret_token"

{
  "build_date": "2021-12-18T19:59:06Z",
  "build_sha": "24fe620eeff5a19e2133c940c7e5ce1ceddb1445",
  "publish_ready": true,
  "version": "9.0.0"
}
```

