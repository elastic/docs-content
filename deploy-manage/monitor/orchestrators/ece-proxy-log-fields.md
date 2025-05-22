---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-proxy-log-fields.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Proxy log fields [ece-proxy-log-fields]

Proxy logs capture data for search and indexing requests that proxies have sent to the {{es}} cluster, and requests that proxies have sent to the {{kib}} instance.

::::{note} 
These fields are subject to change. However, most of these fields are generic for HTTP requests and should be relatively stable.
::::


| Field | Description |
| --- | --- |
| `proxy_ip` | The IP on the connection, i.e. a proxy IP if the request has been proxied |
| `request_end` | The time the request was returned in ms since unix epoch |
| `status_code` | The HTTP status returned to the client |
| `handling_instance` | The product instance name the request was forwarded to |
| `handling_server` | The allocator IP address the request was forwarded to |
| `request_length` | The length of the request body, a value of `-1` means streaming/continuing |
| `request_path` | The request path from the url |
| `instance_capacity` | The total capacity of the handling instance |
| `response_time` | The total time taken for the request in milliseconds `ms`. `response_time` includes `backend_response_time`. |
| `backend_response_time` | The total time spent processing the upstream request with the backend instance ({{es}}, {{kib}}, and so on), including the initial connection, time the component is processing the request, and time streaming the response back to the calling client. The proxy latency is `backend_response_time` - `response_time`.  `backend_response_time` minus `backend_response_body_time` indicates the time spent making the initial connection to the backend instance as well as the time for the backend instance to actually process the request. `backend_response_time` includes `backend_response_body_time`. |
| `backend_response_body_time` | The total time spent streaming the response from the backend instance to the calling client. |
| `auth_user` | The authenticated user for the request (only supported for basic authentication) |
| `capacity` | The total capacity of the handling cluster |
| `request_host` | The `Host` header from the request |
| `client_ip` | The client IP for the request (may differ from proxy ip if `X-Forwarded-For` or proxy protocol is configured) |
| `availability_zones` | The number of availability zones supported by the target cluster |
| `response_length` | The number of bytes written in the response body |
| `connection_id` | A unique ID represented a single client connection, multiple requests may use a single connection |
| `status_reason` | An optional reason to explain the response code - e.g. `BLOCKED_BY_TRAFFIC_FILTER` |
| `request_start` | The time the request was received in milliseconds `ms` since unix epoch |
| `request_port` | The port used for the request |
| `request_scheme` | The scheme (HTTP/HTTPS) used for the request |
| `message` | An optional message associated with a proxy error |
| `action` | The type of elasticsearch request (e.g. search/bulk etc) |
| `handling_cluster` | The cluster the request was forwarded to |
| `request_id` | A unique ID for each request (returned on the response as `X-Cloud-Request-Id` - can be used to correlate client requests with proxy logs) |
| `tls_version` | A code indicating the TLS version used for the request - `1.0 769`,`1.1 770`,`1.2 771`,`1.3 772` |
| `instance_count` | The number of instances in the target cluster |
| `cluster_type` | The type of cluster the request was routed to (e.g. {{es}}, {{kib}}, APM) |
| `request_method` | The HTTP method for the request |
| `backend_connection_id` | A unique ID for the upstream request to the product, the proxy maintains connection pools so this should be re-used |

