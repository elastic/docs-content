---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-proxy-log-fields.html
applies_to:
  deployment:
    ece: all
---

# Proxy Log Fields [ece-proxy-log-fields]

::::{note} 
These fields *are* subject to change, though the vast majority of them are generic for HTTP requests and should be relatively stable.
::::


|     |     |
| --- | --- |
| Field | Description |
| `proxy_ip` | the IP on the connection, i.e. a proxy IP if the request has been proxied |
| `request_end` | the time the request was returned in ms since unix epoch |
| `status_code` | the HTTP status returned to the client |
| `handling_instance` | the product instance name the request was forwarded to |
| `handling_server` | the allocator IP address the request was forwarded to |
| `request_length` | the length of the request body, a value of `-1` means streaming/continuing |
| `request_path` | the request path from the url |
| `instance_capacity` | the total capacity of the handling instance |
| `response_time` | the total time taken for the request in milliseconds `ms`. `response_time` includes `backend_response_time`. |
| `backend_response_time` | the total time spent processing the upstream request with the backend instance (Elasticsearch, Kibana, and so on), including the initial connection, time the component is processing the request, and time streaming the response back to the calling client. The proxy latency is `backend_response_time` - `response_time`.  `backend_response_time` minus `backend_response_body_time` indicates the time spent making the initial connection to the backend instance as well as the time for the backend instance to actually process the request. `backend_response_time` includes `backend_response_body_time`. |
| `backend_response_body_time` | the total time spent streaming the response from the backend instance to the calling client. |
| `auth_user` | the authenticated user for the request (only supported for basic authentication) |
| `capacity` | the total capacity of the handling cluster |
| `request_host` | the `Host` header from the request |
| `client_ip` | the client IP for the request (may differ from proxy ip if `X-Forwarded-For` or proxy protocol is configured) |
| `availability_zones` | the number of availablity zones supported by the target cluster |
| `response_length` | the number of bytes written in the response body |
| `connection_id` | a unique ID represented a single client connecition, multiple requests may use a single connection |
| `status_reason` | an optional reason to explain the response code - e.g. `BLOCKED_BY_TRAFFIC_FILTER` |
| `request_start` | the time the request was received in milliseconds `ms` since unix epoch |
| `request_port` | the port used for the request |
| `request_scheme` | the scheme (HTTP/HTTPS) used for the request |
| `message` | an optoinal message associated with a proxy error |
| `action` | the type of elasticsearch request (e.g. search/bulk etc) |
| `handling_cluster` | the cluster the request was forwarded to |
| `request_id` | a unique ID for each request (returned on the response as `X-Cloud-Request-Id` - can be used to correlate client requests with proxy logs) |
| `tls_version` | a code indicating the TLS version used for the request - `1.0 769`,`1.1 770`,`1.2 771`,`1.3 772` |
| `instance_count` | the number of instances in the target cluster |
| `cluster_type` | the type of cluster the request was routed to (e.g. elasticsearch, kibana, apm etc) |
| `request_method` | the HTTP method for the request |
| `backend_connection_id` | a unique ID for the upstream request to the product, the proxy maintains connection pools so this should be re-used |

