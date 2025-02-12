---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-connect-to-ems.html
---

# Connect to Elastic Maps Service [maps-connect-to-ems]

[Elastic Maps Service (EMS)](https://www.elastic.co/elastic-maps-service) is a service that hosts tile layers and vector shapes of administrative boundaries. If you are using Kibana’s out-of-the-box settings, Maps is already configured to use EMS.

If you are on a restricted or fully air-gapped environment, you may need to configure your firewall to enable access to EMS resources. Find below details on the domains and HTTP headers used by Elastic Maps Service. Alternatively, Elastic Maps Service can be [disabled](#disable-ems) or [installed locally](#elastic-maps-server).


## Domains [_domains]

EMS requests are made to the following domains:

* Tile Service: `tiles.maps.elastic.co`
* File Service: `vector.maps.elastic.co`


## Headers [_headers]

Find below examples of the request and response headers from Kibana and a minimal `curl` request example showing the response headers sent by each service.

::::{warning}
These headers may change without further notice at anytime and are shared for reference.
::::



### EMS Tile Service [_ems_tile_service]

The EMS Tile Service provides basemaps in three different styles as the default background for Maps visualizations. The basemaps use [OpenStreetMap](https://www.openstreetmap.org/about) data following the [OpenMapTiles](https://openmaptiles.org/) schema and can be explored at [maps.elastic.co](https://maps.elastic.co).

Headers for the Tile Service JSON manifest describing the basemaps available.

:::::::{tab-set}

::::::{tab-item} Curl Example
::::{dropdown}
```bash
curl -I 'https://tiles.maps.elastic.co/v9.0/manifest?elastic_tile_service_tos=agree&my_app_name=kibana&my_app_version=9.0.0-beta1' \
-H 'User-Agent: curl/7.81.0' \
-H 'Accept: */*' \
-H 'Accept-Encoding: gzip, deflate, br'
```

Server response

```txt
HTTP/2 200
server: BaseHTTP/0.6 Python/3.11.4
date: Mon, 20 Nov 2023 15:08:46 GMT
content-type: application/json; charset=utf-8
elastic-api-version: 2023-10-31
access-control-allow-origin: *
access-control-allow-methods: GET, OPTIONS, HEAD
access-control-allow-headers: Origin, Accept, Content-Type, kbn-version, elastic-api-version
access-control-expose-headers: etag
content-encoding: gzip
vary: Accept-Encoding
x-varnish: 844076 5416505
accept-ranges: bytes
varnish-age: 85285
cache-control: private, max-age=86400
via: 1.1 varnish (Varnish/7.0), 1.1 google
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
```

::::
::::::

::::::{tab-item} Request
```txt
Host: tiles.maps.elastic.co
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://deployment-host/app/maps/map
Origin: https://deployment-host
Connection: keep-alive
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: cross-site
Pragma: no-cache
Cache-Control: no-cache
TE: trailers
```
::::::

::::::{tab-item} Response
```txt
server: BaseHTTP/0.6 Python/3.11.4
date: Mon, 20 Nov 2023 17:53:10 GMT
content-type: application/json; charset=utf-8
elastic-api-version: 2023-10-31
access-control-allow-origin: *
access-control-allow-methods: GET, OPTIONS, HEAD
access-control-allow-headers: Origin, Accept, Content-Type, kbn-version, elastic-api-version
access-control-expose-headers: etag
content-encoding: gzip
vary: Accept-Encoding
x-varnish: 8848609 1142291
accept-ranges: bytes
varnish-age: 65725
cache-control: private, max-age=86400
content-length: 341
via: 1.1 varnish (Varnish/7.0), 1.1 google
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
```
::::::

:::::::
Headers for a vector tile asset in *protobuffer* format from the Tile Service.

:::::::{tab-set}

::::::{tab-item} Curl Example
::::{dropdown}
```bash
$ curl -I 'https://tiles.maps.elastic.co/data/v3/1/1/0.pbf?elastic_tile_service_tos=agree&my_app_name=kibana&my_app_version=9.0.0-beta1' \
-H 'User-Agent: curl/7.81.0' \
-H 'Accept: */*' \
-H 'Accept-Encoding: gzip, deflate, br'
```

Server response

```txt
HTTP/2 200
content-encoding: gzip
content-length: 144075
access-control-allow-origin: *
access-control-allow-methods: GET, OPTIONS, HEAD
access-control-allow-headers: Origin, Accept, Content-Type, kbn-version, elastic-api-version
access-control-expose-headers: etag
x-varnish: 3269455 5976667
accept-ranges: bytes
varnish-age: 9045
via: 1.1 varnish (Varnish/7.0), 1.1 google
date: Mon, 20 Nov 2023 15:08:19 GMT
age: 78827
last-modified: Thu, 16 Sep 2021 17:14:41 GMT
etag: W/"232cb-zYEfNgd8rzHusLotRFzgRDSDDGA"
content-type: application/x-protobuf
vary: Accept-Encoding
cache-control: public,max-age=3600
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
```

::::
::::::

::::::{tab-item} Request
```txt
Host: tiles.maps.elastic.co
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://deployment-host/app/maps/map
Origin: https://deployment-host
Connection: keep-alive
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: cross-site
TE: trailers
```
::::::

::::::{tab-item} Response
```txt
content-encoding: gzip
content-length: 101691
access-control-allow-origin: *
access-control-allow-methods: GET, OPTIONS, HEAD
access-control-allow-headers: Origin, Accept, Content-Type, kbn-version, elastic-api-version
access-control-expose-headers: etag
x-varnish: 4698676 3660338
accept-ranges: bytes
varnish-age: 9206
via: 1.1 varnish (Varnish/7.0), 1.1 google
date: Mon, 20 Nov 2023 15:05:29 GMT
age: 75788
last-modified: Thu, 16 Sep 2021 17:14:41 GMT
etag: W/"18d3b-ot9ckSsdpH7n+yJz4BXXQp6Zs08"
content-type: application/x-protobuf
vary: Accept-Encoding
cache-control: public,max-age=3600
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
```
::::::

:::::::
Headers for an sprite image asset from the Tile Service

:::::::{tab-set}

::::::{tab-item} Curl Example
::::{dropdown}
```bash
curl -I 'https://tiles.maps.elastic.co/styles/osm-bright-desaturated/sprite.png' \
-H 'User-Agent: curl/7.81.0' \
-H 'Accept: image/avif,image/webp,*/*' \
-H 'Accept-Encoding: gzip, deflate, br'
```

Server response

```txt
HTTP/2 200
content-length: 17181
access-control-allow-origin: *
access-control-allow-methods: GET, OPTIONS, HEAD
access-control-allow-headers: Origin, Accept, Content-Type, kbn-version, elastic-api-version
access-control-expose-headers: etag
x-varnish: 8769943 4865354
accept-ranges: bytes
varnish-age: 250
via: 1.1 varnish (Varnish/7.0), 1.1 google
date: Tue, 21 Nov 2023 14:44:36 GMT
age: 592
etag: W/"431d-/dqE/W5Q3FqkHikyDQtCuQqAdlY"
content-type: image/png
cache-control: public,max-age=3600
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
```

::::
::::::

::::::{tab-item} Request
```txt
Host: tiles.maps.elastic.co
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: image/avif,image/webp,*/*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://deployment-host/app/maps/map
Origin: https://deployment-host
Connection: keep-alive
Sec-Fetch-Dest: image
Sec-Fetch-Mode: cors
Sec-Fetch-Site: cross-site
Pragma: no-cache
Cache-Control: no-cache
TE: trailers
```
::::::

::::::{tab-item} Response
```txt
content-length: 17181
access-control-allow-origin: *
access-control-allow-methods: GET, OPTIONS, HEAD
access-control-allow-headers: Origin, Accept, Content-Type, kbn-version, elastic-api-version
access-control-expose-headers: etag
x-varnish: 3530683 3764574
accept-ranges: bytes
varnish-age: 833
via: 1.1 varnish (Varnish/7.0), 1.1 google
date: Mon, 20 Nov 2023 14:44:29 GMT
age: 77048
etag: W/"431d-/dqE/W5Q3FqkHikyDQtCuQqAdlY"
content-type: image/png
cache-control: public,max-age=3600
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
```
::::::

:::::::

### EMS File Service [_ems_file_service]

EMS File Service provides the administrative boundaries used for [choropleth mapping](maps-getting-started.md#maps-add-choropleth-layer) as static assets in GeoJSON or TopoJSON formats and can be explored at [maps.elastic.co](https://maps.elastic.co).

Headers for the File Service JSON manifest that declares all the datasets available.

:::::::{tab-set}

::::::{tab-item} Curl example
::::{dropdown}
```bash
curl -I 'https://vector.maps.elastic.co/v9.0/manifest?elastic_tile_service_tos=agree&my_app_name=kibana&my_app_version=9.0.0-beta1' \
-H 'User-Agent: curl/7.81.0' \
-H 'Accept: */*' \
-H 'Accept-Encoding: gzip, deflate, br'
```

Server response

```txt
HTTP/2 200
x-guploader-uploadid: ABPtcPp_BvMdBDO5jVlutETVHmvpOachwjilw4AkIKwMrOQJ4exR9Eln4g0LkW3V_LLSEpvjYLtUtFmO0Uwr61XXUhoP_A
x-goog-generation: 1689593295246576
x-goog-metageneration: 1
x-goog-stored-content-encoding: gzip
x-goog-stored-content-length: 108029
content-encoding: gzip
x-goog-hash: crc32c=T5gVpw==
x-goog-hash: md5=6F8KWV8VTdx8FsN2iFehow==
x-goog-storage-class: MULTI_REGIONAL
accept-ranges: bytes
content-length: 108029
access-control-allow-origin: *
access-control-expose-headers: Authorization, Content-Length, Content-Type, Date, Server, Transfer-Encoding, X-GUploader-UploadID, X-Google-Trace, accept, elastic-api-version, kbn-name, kbn-version, origin
server: UploadServer
date: Tue, 21 Nov 2023 14:25:07 GMT
expires: Tue, 21 Nov 2023 15:25:07 GMT
cache-control: public, max-age=3600,no-transform
age: 2170
last-modified: Mon, 17 Jul 2023 11:28:15 GMT
etag: "e85f0a595f154ddc7c16c3768857a1a3"
content-type: application/json
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
```

::::
::::::

::::::{tab-item} Request
```txt
Host: vector.maps.elastic.co
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://deployment-host/app/maps/map
Origin: https://deployment-host
Connection: keep-alive
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: cross-site
Pragma: no-cache
Cache-Control: no-cache
```
::::::

::::::{tab-item} Response
```txt
x-guploader-uploadid: ABPtcPoUFrCmjBeebnfRxSZp44ZHsZ-_iQg7794RU1Z7Lb2cNNxXsMRkIDa5s7VBEfyehvo-_9rcm1A3HfYW8geguUxKrw
x-goog-generation: 1689593295246576
x-goog-metageneration: 1
x-goog-stored-content-encoding: gzip
x-goog-stored-content-length: 108029
content-encoding: gzip
x-goog-hash: crc32c=T5gVpw==
x-goog-hash: md5=6F8KWV8VTdx8FsN2iFehow==
x-goog-storage-class: MULTI_REGIONAL
accept-ranges: bytes
content-length: 108029
access-control-allow-origin: *
access-control-expose-headers: Authorization, Content-Length, Content-Type, Date, Server, Transfer-Encoding, X-GUploader-UploadID, X-Google-Trace, accept, elastic-api-version, kbn-name, kbn-version, origin
server: UploadServer
date: Tue, 21 Nov 2023 11:24:45 GMT
expires: Tue, 21 Nov 2023 12:24:45 GMT
cache-control: public, max-age=3600,no-transform
age: 3101
last-modified: Mon, 17 Jul 2023 11:28:15 GMT
etag: "e85f0a595f154ddc7c16c3768857a1a3"
content-type: application/json
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
X-Firefox-Spdy: h2
```
::::::

:::::::
Headers for a sample Dataset from the File Service in TopoJSON format.

:::::::{tab-set}

::::::{tab-item} Curl example
::::{dropdown}
```bash
curl -I 'https://vector.maps.elastic.co/files/world_countries_v7.topo.json?elastic_tile_service_tos=agree&my_app_name=kibana&my_app_version=9.0.0-beta1' \
-H 'User-Agent: curl/7.81.0' \
-H 'Accept: */*' \
-H 'Accept-Encoding: gzip, deflate, br'
```

Server response

```txt
HTTP/2 200
x-guploader-uploadid: ABPtcPpmMffchVgfHIr-SSC00WORo145oV-1q0asjqRvjLV_7cIgyfLRfofXV-BG7huMYABFypblcgdgXRBARhpo2c88ow
x-goog-generation: 1689593325442971
x-goog-metageneration: 1
x-goog-stored-content-encoding: gzip
x-goog-stored-content-length: 587241
content-encoding: gzip
x-goog-hash: crc32c=OcROeg==
x-goog-hash: md5=8KKIwD6wbKa3YYXTnnFcZw==
x-goog-storage-class: MULTI_REGIONAL
accept-ranges: bytes
content-length: 587241
access-control-allow-origin: *
access-control-expose-headers: Authorization, Content-Length, Content-Type, Date, Server, Transfer-Encoding, X-GUploader-UploadID, X-Google-Trace, accept, elastic-api-version, kbn-name, kbn-version, origin
server: UploadServer
date: Tue, 21 Nov 2023 14:22:16 GMT
expires: Tue, 21 Nov 2023 15:22:16 GMT
cache-control: public, max-age=3600,no-transform
age: 2202
last-modified: Mon, 17 Jul 2023 11:28:45 GMT
etag: "f0a288c03eb06ca6b76185d39e715c67"
content-type: application/json
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
```

::::
::::::

::::::{tab-item} Request
```txt
Host: vector.maps.elastic.co
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://deployment-host/app/maps/map
Origin: https://deployment-host
Connection: keep-alive
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: cross-site
Pragma: no-cache
Cache-Control: no-cache
```
::::::

::::::{tab-item} Response
```txt
x-guploader-uploadid: ABPtcPqIDSg5tyavvwwtJQa8a8iycoXOCkHBp_2YJbJJnQgb5XMD7nFwRUogg00Ou27VFIs95v7L99OMnvXR1bcb9RW-xQ
x-goog-generation: 1689593325442971
x-goog-metageneration: 1
x-goog-stored-content-encoding: gzip
x-goog-stored-content-length: 587241
content-encoding: gzip
x-goog-hash: crc32c=OcROeg==
x-goog-hash: md5=8KKIwD6wbKa3YYXTnnFcZw==
x-goog-storage-class: MULTI_REGIONAL
accept-ranges: bytes
content-length: 587241
access-control-allow-origin: *
access-control-expose-headers: Authorization, Content-Length, Content-Type, Date, Server, Transfer-Encoding, X-GUploader-UploadID, X-Google-Trace, accept, elastic-api-version, kbn-name, kbn-version, origin
server: UploadServer
date: Tue, 21 Nov 2023 12:16:01 GMT
expires: Tue, 21 Nov 2023 13:16:01 GMT
cache-control: public, max-age=3600,no-transform
age: 29
last-modified: Mon, 17 Jul 2023 11:28:45 GMT
etag: "f0a288c03eb06ca6b76185d39e715c67"
content-type: application/json
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
X-Firefox-Spdy: h2
```
::::::

:::::::

## Disable Elastic Maps Service [disable-ems]

You might experience EMS connection issues if your Kibana server or browser are on a private network or behind a firewall. If this happens, you can disable the EMS connection to avoid unnecessary EMS requests.

To disable EMS, change your [kibana.yml](../../../deploy-manage/deploy/self-managed/configure.md) file.

1. Set `map.includeElasticMapsService` to `false` to turn off the EMS connection.
2. Set `map.tilemap.url` to the URL of your tile server. This configures the default tile layer of Maps.


## Host Elastic Maps Service locally [elastic-maps-server]

::::{note}
Find more details about installing Elastic components in an air-gapped environment in the [Elastic Stack documentation](../../../deploy-manage/deploy/cloud-enterprise/air-gapped-install.md).
::::


If you cannot connect to Elastic Maps Service from the {{kib}} server or browser clients, and your cluster has the appropriate license level, you can opt to host the service on your own infrastructure.

{{hosted-ems}} is a self-managed version of Elastic Maps Service offered as a Docker image that provides both the EMS basemaps and EMS boundaries. The image is bundled with basemaps up to zoom level 8. After connecting it to your {{es}} cluster for license validation, you have the option to download and configure a more detailed basemaps database.

1. Pull the {{hosted-ems}} Docker image.

   ::::{warning}
   Version 9.0.0-beta1 of {{hosted-ems}} has not yet been released. No Docker image is currently available for this version.
   ::::


    ```bash
    docker pull docker.elastic.co/elastic-maps-service/elastic-maps-server:9.0.0-beta1
    ```

2. Optional: Install [Cosign](https://docs.sigstore.dev/system_config/installation/) for your environment. Then use Cosign to verify the {{es}} image’s signature.

    ```sh
    wget https://artifacts.elastic.co/cosign.pub
    cosign verify --key cosign.pub docker.elastic.co/elastic-maps-service/elastic-maps-server:9.0.0-beta1
    ```

    The `cosign` command prints the check results and the signature payload in JSON format:

    ```sh
    Verification for docker.elastic.co/elastic-maps-service/elastic-maps-server:9.0.0-beta1 --
    The following checks were performed on each of these signatures:
      - The cosign claims were validated
      - Existence of the claims in the transparency log was verified offline
      - The signatures were verified against the specified public key
    ```

3. Start {{hosted-ems}} and expose the default port `8080`:

    ```bash
    docker run --rm --init --publish 8080:8080 \
      docker.elastic.co/elastic-maps-service/elastic-maps-server:9.0.0-beta1
    ```

    Once {{hosted-ems}} is running, follow instructions from the webpage at `localhost:8080` to define a configuration file and optionally download a more detailed basemaps database.

   :::{image} ../../../images/kibana-elastic-maps-server-instructions.png
   :alt: Set-up instructions
   :class: screenshot
   :::



### Configuration [elastic-maps-server-configuration]

{{hosted-ems}} reads properties from a configuration file in YAML format that is validated on startup. The location of this file is provided by the `EMS_PATH_CONF` container environment variable and defaults to `/usr/src/app/server/config/elastic-maps-server.yml`. This environment variable can be changed by making use of the `-e` docker flag of the start command.

**General settings**

|     |     |
| --- | --- |
| $$$ems-host$$$`host` | Specifies the host of the backend server. To allow remote users to connect, set the value to the IP address or DNS name of the {{hosted-ems}} container. **Default: *your-hostname***. [Equivalent {{kib}} setting](../../../deploy-manage/deploy/self-managed/configure.md#server-host). |
| `port` | Specifies the port used by the backend server. Default: **`8080`**. [Equivalent {{kib}} setting](../../../deploy-manage/deploy/self-managed/configure.md#server-port). |
| `basePath` | Specify a path at which to mount the server if you are running behind a proxy. This setting cannot end in a slash (`/`). [Equivalent {{kib}} setting](../../../deploy-manage/deploy/self-managed/configure.md#server-basePath). |
| `ui` | Controls the display of the status page and the layer preview. **Default: `true`** |
| `logging.level` | Verbosity of {{hosted-ems}} logs. Valid values are `trace`, `debug`, `info`, `warn`, `error`, `fatal`, and `silent`. **Default: `info`** |
| `path.planet` | Path of the basemaps database. **Default: `/usr/src/app/data/planet.mbtiles`** |

**{{es}} connection and security settings**

|     |     |
| --- | --- |
| `elasticsearch.host` | URL of the {{es}} instance to use for license validation. |
| `elasticsearch.username` and `elasticsearch.password` | Credentials of a user with at least the `monitor` role. |
| `elasticsearch.ssl.certificateAuthorities` | Paths to one or more PEM-encoded X.509 certificate authority (CA) certificates that make up a trusted certificate chain for {{hosted-ems}}. This chain is used by {{hosted-ems}} to establish trust when connecting to your {{es}} cluster. [Equivalent {{kib}} setting](../../../deploy-manage/deploy/self-managed/configure.md#elasticsearch-ssl-certificateAuthorities). |
| `elasticsearch.ssl.certificate` and `elasticsearch.ssl.key`, and `elasticsearch.ssl.keyPassphrase` | Optional settings that provide the paths to the PEM-format SSL certificate and key files and the key password. These files are used to verify the identity of {{hosted-ems}} to {{es}} and are required when `xpack.security.http.ssl.client_authentication` in {{es}} is set to `required`. [Equivalent {{kib}} setting](../../../deploy-manage/deploy/self-managed/configure.md#elasticsearch-ssl-cert-key). |
| `elasticsearch.ssl.verificationMode` | Controls the verification of the server certificate that {{hosted-ems}} receives when making an outbound SSL/TLS connection to {{es}}. Valid values are "`full`", "`certificate`", and "`none`". Using "`full`" performs hostname verification, using "`certificate`" skips hostname verification, and using "`none`" skips verification entirely. **Default: `full`**. [Equivalent {{kib}} setting](../../../deploy-manage/deploy/self-managed/configure.md#elasticsearch-ssl-verificationMode). |

**Server security settings**

|     |     |
| --- | --- |
| `ssl.enabled` | Enables SSL/TLS for inbound connections to {{hosted-ems}}. When set to `true`, a certificate and its corresponding private key must be provided. **Default: `false`**. [Equivalent {{kib}} setting](../../../deploy-manage/deploy/self-managed/configure.md#server-ssl-enabled). |
| `ssl.certificateAuthorities` | Paths to one or more PEM-encoded X.509 certificate authority (CA) certificates that make up a trusted certificate chain for {{hosted-ems}}. This chain is used by the {{hosted-ems}} to establish trust when receiving inbound SSL/TLS connections from end users. [Equivalent {{kib}} setting](../../../deploy-manage/deploy/self-managed/configure.md#server-ssl-certificateAuthorities). |
| `ssl.key`, `ssl.certificate`, and `ssl.keyPassphrase` | Location of yor SSL key and certificate files and the password that decrypts the private key that is specified via `ssl.key`. This password is optional, as the key may not be encrypted. [Equivalent {{kib}} setting](../../../deploy-manage/deploy/self-managed/configure.md#server-ssl-cert-key). |
| `ssl.supportedProtocols` | An array of supported protocols with versions.Valid protocols: `TLSv1`, `TLSv1.1`, `TLSv1.2`. **Default: `TLSv1.1`, `TLSv1.2`**. [Equivalent {{kib}} setting](../../../deploy-manage/deploy/self-managed/configure.md#server-ssl-supportedProtocols). |
| `ssl.cipherSuites` | Details on the format, and the valid options, are available via the[OpenSSL cipher list format documentation](https://www.openssl.org/docs/man1.1.1/man1/ciphers.html#CIPHER-LIST-FORMAT).**Default: `TLS_AES_256_GCM_SHA384 TLS_CHACHA20_POLY1305_SHA256 TLS_AES_128_GCM_SHA256 ECDHE-RSA-AES128-GCM-SHA256, ECDHE-ECDSA-AES128-GCM-SHA256, ECDHE-RSA-AES256-GCM-SHA384, ECDHE-ECDSA-AES256-GCM-SHA384, DHE-RSA-AES128-GCM-SHA256, ECDHE-RSA-AES128-SHA256, DHE-RSA-AES128-SHA256, ECDHE-RSA-AES256-SHA384, DHE-RSA-AES256-SHA384, ECDHE-RSA-AES256-SHA256, DHE-RSA-AES256-SHA256, HIGH,!aNULL, !eNULL, !EXPORT, !DES, !RC4, !MD5, !PSK, !SRP, !CAMELLIA`**. [Equivalent {{kib}} setting](../../../deploy-manage/deploy/self-managed/configure.md#server-ssl-cipherSuites). |


#### Bind-mounted configuration [elastic-maps-server-bind-mount-config]

One way to configure {{hosted-ems}} is to provide `elastic-maps-server.yml` via bind-mounting. With `docker-compose`, the bind-mount can be specified like this:

```yaml
services:
  ems-server:
    image: docker.elastic.co/elastic-maps-service/elastic-maps-server:9.0.0-beta1
    volumes:
      - ./elastic-maps-server.yml:/usr/src/app/server/config/elastic-maps-server.yml
```


#### Environment variable configuration [elastic-maps-server-envvar-config]

All configuration settings can be overridden by environment variables that are named with all uppercase letters and by replacing YAML periods with underscores. For example `elasticsearch.ssl.certificate` could be overridden by the environment variable `ELASTICSEARCH_SSL_CERTIFICATE`. Boolean variables must use the `true` or `false` strings.

::::{warning}
All information that you include in environment variables is visible through the `ps` command, including sensitive information.
::::


These variables can be set with `docker-compose` like this:

```yaml
services:
  ems-server:
    image: docker.elastic.co/elastic-maps-service/elastic-maps-server:9.0.0-beta1
    environment:
      ELASTICSEARCH_HOST: http://elasticsearch.example.org
      ELASTICSEARCH_USERNAME: 'ems'
      ELASTICSEARCH_PASSWORD: 'changeme'
```


### Data [elastic-maps-server-data]

{{hosted-ems}} hosts vector layer boundaries and vector tile basemaps for the entire planet. Boundaries include world countries, global administrative regions, and specific country regions. Basemaps up to zoom level 8 are bundled in the Docker image. These basemaps are sufficient for maps and dashboards at the country level. To present maps with higher detail, follow the instructions of the front page to download and configure the appropriate basemaps database. The most detailed basemaps at zoom level 14 are good for street level maps, but require ~90GB of disk space.

:::{image} ../../../images/kibana-elastic-maps-server-basemaps.png
:alt: Basemaps download options
:class: screenshot
:::

::::{tip}
The available basemaps and boundaries can be explored from the `/maps` endpoint in a web page that is your self-managed equivalent to [https://maps.elastic.co](https://maps.elastic.co).
::::



### Kibana configuration [elastic-maps-server-kibana]

With {{hosted-ems}} running, add the `map.emsUrl` configuration key in your [kibana.yml](../../../deploy-manage/deploy/self-managed/configure.md) file pointing to the root of the service. This setting will point {{kib}} to request EMS basemaps and boundaries from {{hosted-ems}}. Typically this will be the URL to the [host and port](#ems-host) of {{hosted-ems}}. For example, `map.emsUrl: https://my-ems-server:8080`.


### Status check [elastic-maps-server-check]

{{hosted-ems}} periodically runs a status check that is exposed in three different forms:

* At the root of {{hosted-ems}}, a web page will render the status of the different services.
* A JSON representation of {{hosted-ems}} status is available at the `/status` endpoint.
* The Docker [`HEALTHCHECK`](https://docs.docker.com/engine/reference/builder/#healthcheck) instruction is run by default and will inform about the health of the service, running a process equivalent to the `/status` endpoint.

::::{important}
{{hosted-ems}} won’t respond to any data request if the license validation is not fulfilled.
::::



### Logging [elastic-maps-server-logging]

Logs are generated in [ECS JSON format](https://www.elastic.co/guide/en/ecs/{{ecs_version}}) and emitted to the standard output and to `/var/log/elastic-maps-server/elastic-maps-server.log`. The server won’t rotate the logs automatically but the `logrotate` tool is installed in the image. Mount `/dev/null` to the default log path if you want to disable the output to that file.
