---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-rum-sourcemap-api.html
---

# RUM source map API [apm-rum-sourcemap-api]

::::{important} 
This endpoint is only compatible with the [APM integration for Elastic Agent](https://www.elastic.co/guide/en/apm/guide/current/index.html).
::::


A source map allows minified files to be mapped back to original source code — allowing you to maintain the speed advantage of minified code, without losing the ability to quickly and easily debug your application.

For best results, uploading source maps should become a part of your deployment procedure, and not something you only do when you see unhelpful errors. That’s because uploading source maps after errors happen won’t make old errors magically readable — errors must occur again for source mapping to occur.

The following APIs are available:

* [Create or update source map](#rum-sourcemap-post)
* [Get source maps](#rum-sourcemap-get)
* [Delete source map](#rum-sourcemap-delete)


### Max payload size [limit-sourcemap-api] 

{{kib}}'s maximum payload size is 1mb. If you attempt to upload a source map that exceeds the max payload size, you will get a `413` error.

Before uploading source maps that exceed this default, change the maximum payload size allowed by {{kib}} with the `server.maxPayload` variable.


### How to use APM APIs [use-sourcemap-api] 

::::{dropdown} Expand for required headers, privileges, and usage details
Interact with APM APIs using cURL or another API tool. All APM APIs are Kibana APIs, not Elasticsearch APIs; because of this, the Kibana dev tools console cannot be used to interact with APM APIs.

For all APM APIs, you must use a request header. Supported headers are `Authorization`, `kbn-xsrf`, and `Content-Type`.

`Authorization: ApiKey {{credentials}}`
:   Kibana supports token-based authentication with the Elasticsearch API key service. The API key returned by the  [Elasticsearch create API key API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) can be used by sending a request with an `Authorization` header that has a value of `ApiKey` followed by the `{{credentials}}`, where `{{credentials}}` is the base64 encoding of `id` and `api_key` joined by a colon.

    Alternatively, you can create a user and use their username and password to authenticate API access: `-u $USER:$PASSWORD`.

    Whether using `Authorization: ApiKey {{credentials}}`, or `-u $USER:$PASSWORD`, users interacting with APM APIs must have [sufficient privileges](applications-ui-api-user.md).


`kbn-xsrf: true`
:   By default, you must use `kbn-xsrf` for all API calls, except in the following scenarios:

    * The API endpoint uses the `GET` or `HEAD` operations
    * The path is allowed using the `server.xsrf.allowlist` setting
    * XSRF protections are disabled using the `server.xsrf.disableProtection` setting


`Content-Type: application/json`
:   Applicable only when you send a payload in the API request. {{kib}} API requests and responses use JSON. Typically, if you include the `kbn-xsrf` header, you must also include the `Content-Type` header.

::::


## Create or update source map [rum-sourcemap-post]

Create or update a source map for a specific service and version.


#### Privileges [rum-sourcemap-post-privs] 

The user accessing this endpoint requires `All` Kibana privileges for the APM and User Experience feature. For more information, see [Kibana privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).


#### Request [apm-sourcemap-post-req] 

`POST /api/apm/sourcemaps`


#### Request body [apm-sourcemap-post-req-body] 

`service_name`
:   (required, string) The name of the service that the service map should apply to.

`service_version`
:   (required, string) The version of the service that the service map should apply to.

`bundle_filepath`
:   (required, string) The absolute path of the final bundle as used in the web application.

`sourcemap`
:   (required, string or file upload) The source map. It must follow the [source map revision 3 proposal](https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k).


#### Examples [apm-sourcemap-post-example] 

The following example uploads a source map for a service named `foo` and a service version of `1.0.0`:

```bash
curl -X POST "http://localhost:5601/api/apm/sourcemaps" \
-H 'Content-Type: multipart/form-data' \
-H 'kbn-xsrf: true' \
-H 'Authorization: ApiKey ${YOUR_API_KEY}' \
-F 'service_name="foo"' \
-F 'service_version="1.0.0"' \
-F 'bundle_filepath="/test/e2e/general-usecase/bundle.js"' \
-F 'sourcemap="{\"version\":3,\"file\":\"static/js/main.chunk.js\",\"sources\":[\"fleet-source-map-client/src/index.css\",\"fleet-source-map-client/src/App.js\",\"webpack:///./src/index.css?bb0a\",\"fleet-source-map-client/src/index.js\",\"fleet-source-map-client/src/reportWebVitals.js\"],\"sourcesContent\":[\"content\"],\"mappings\":\"mapping\",\"sourceRoot\":\"\"}"' <1>
```

1. Alternatively, upload the source map as a file with `-F 'sourcemap=@path/to/source_map/bundle.js.map'`



#### Response body [apm-sourcemap-post-body] 

```js
{
  "type": "sourcemap",
  "identifier": "foo-1.0.0",
  "relative_url": "/api/fleet/artifacts/foo-1.0.0/644fd5a997d1ddd90ee131ba18e2b3d03931d89dd1fe4599143c0b3264b3e456",
  "body": "eJyFkL1OwzAUhd/Fc+MbYMuCEBIbHRjKgBgc96R16tiWr1OQqr47NwqJxEK3q/PzWccXxchnZ7E1A1SjuhjVZtF2yOxiEPlO17oWox3D3uPFeSRTjmJQARfCPeiAgGx8NTKsYdAc1T3rwaSJGcds8Sp3c1HnhfywUZ3QhMTFFGepZxqMC9oex3CS9tpk1XyozgOlmoVKuJX1DqEQZ0su7PGtLU+V/3JPKc3cL7TJ2FNDRPov4bFta3MDM4f7W69lpJjLO9qdK8bzVPhcJz3HUCQ4LbO/p5hCSC4cZPByrp/wFqOklbpefwAhzpqI",
  "created": "2021-07-09T20:47:44.812Z",
  "id": "apm:foo-1.0.0-644fd5a997d1ddd90ee131ba18e2b3d03931d89dd1fe4599143c0b3264b3e456",
  "compressionAlgorithm": "zlib",
  "decodedSha256": "644fd5a997d1ddd90ee131ba18e2b3d03931d89dd1fe4599143c0b3264b3e456",
  "decodedSize": 441,
  "encodedSha256": "024c72749c3e3dd411b103f7040ae62633558608f480bce4b108cf5b2275bd24",
  "encodedSize": 237,
  "encryptionAlgorithm": "none",
  "packageName": "apm"
}
```


## Get source maps [rum-sourcemap-get]

Returns an array of Fleet artifacts, including source map uploads.


#### Privileges [rum-sourcemap-get-privs] 

The user accessing this endpoint requires `Read` or `All` Kibana privileges for the APM and User Experience feature. For more information, see [Kibana privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).


#### Request [apm-sourcemap-get-req] 

`GET /api/apm/sourcemaps`


#### Example [apm-sourcemap-get-example] 

The following example requests all uploaded source maps:

```bash
curl -X GET "http://localhost:5601/api/apm/sourcemaps" \
-H 'Content-Type: application/json' \
-H 'kbn-xsrf: true' \
-H 'Authorization: ApiKey ${YOUR_API_KEY}'
```


#### Response body [apm-sourcemap-get-body] 

```js
{
  "artifacts": [
    {
      "type": "sourcemap",
      "identifier": "foo-1.0.0",
      "relative_url": "/api/fleet/artifacts/foo-1.0.0/644fd5a997d1ddd90ee131ba18e2b3d03931d89dd1fe4599143c0b3264b3e456",
      "body": {
        "serviceName": "foo",
        "serviceVersion": "1.0.0",
        "bundleFilepath": "/test/e2e/general-usecase/bundle.js",
        "sourceMap": {
          "version": 3,
          "file": "static/js/main.chunk.js",
          "sources": [
            "fleet-source-map-client/src/index.css",
            "fleet-source-map-client/src/App.js",
            "webpack:///./src/index.css?bb0a",
            "fleet-source-map-client/src/index.js",
            "fleet-source-map-client/src/reportWebVitals.js"
          ],
          "sourcesContent": [
            "content"
          ],
          "mappings": "mapping",
          "sourceRoot": ""
        }
      },
      "created": "2021-07-09T20:47:44.812Z",
      "id": "apm:foo-1.0.0-644fd5a997d1ddd90ee131ba18e2b3d03931d89dd1fe4599143c0b3264b3e456",
      "compressionAlgorithm": "zlib",
      "decodedSha256": "644fd5a997d1ddd90ee131ba18e2b3d03931d89dd1fe4599143c0b3264b3e456",
      "decodedSize": 441,
      "encodedSha256": "024c72749c3e3dd411b103f7040ae62633558608f480bce4b108cf5b2275bd24",
      "encodedSize": 237,
      "encryptionAlgorithm": "none",
      "packageName": "apm"
    }
  ]
}
```


## Delete source map [rum-sourcemap-delete]

Delete a previously uploaded source map.


#### Privileges [rum-sourcemap-delete-privs] 

The user accessing this endpoint requires `All` Kibana privileges for the APM and User Experience feature. For more information, see [Kibana privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).


#### Request [apm-sourcemap-delete-req] 

`DELETE /api/apm/sourcemaps/:id`


#### Example [apm-sourcemap-delete-example] 

The following example deletes a source map with an id of `apm:foo-1.0.0-644fd5a9`:

```bash
curl -X DELETE "http://localhost:5601/api/apm/sourcemaps/apm:foo-1.0.0-644fd5a9" \
-H 'Content-Type: application/json' \
-H 'kbn-xsrf: true' \
-H 'Authorization: ApiKey ${YOUR_API_KEY}'
```


#### Response body [apm-sourcemap-delete-body] 

```js
{}
```


