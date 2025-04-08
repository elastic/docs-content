---
applies_to:
  stack: 
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
navigation_title: "Error: unable to retrieve node fs stats"
# is mapped_pages needed for newly created docs?
---

# Fix unable to retrieve node fs stats error [unable-to-retrieve-node-fs-stats]

```
Error: unable to retrieve node fs stats
```

This error occurs when the Elasticsearch client (like Kibana) cannot fetch version information from one or more Elasticsearch nodes. This may happen due to network issues, incorrect configuration, or unavailable nodes. To resolve this, ensure that the nodes are up and running, check the network connectivity between the client and the nodes, and verify the configuration settings. If the issue persists, consider checking the Elasticsearch logs for more detailed error information.

## What it means

This log message typically comes from **Kibana** when it tries to connect to Elasticsearch during its startup routine. Kibana acts as a client to Elasticsearch and requires access to:

- The cluster’s host and port
- Authentication credentials (if required)
- TLS settings (if applicable)

If Kibana can’t reach the nodes listed in its configuration, it can’t determine if the versions are compatible, and it throws this error.

## Common causes

- One or more entries in `elasticsearch.hosts` are unreachable or misconfigured
- The `KBN_PATH_CONF` environment variable points to a different config file
- A firewall is blocking access between Kibana and Elasticsearch

## Configuration locations

Settings are defined in `kibana.yml`, usually located at `$KIBANA_HOME/config`. You can override its path with:

```console
KBN_PATH_CONF=/home/kibana/config ./bin/kibana
```

Relevant settings:

```yaml
elasticsearch.hosts: ["http://localhost:9200"]
elasticsearch.username: "kibana"
elasticsearch.password: "your_password"
elasticsearch.ssl.certificateAuthorities: ["path/to/ca.crt"]
```
Kibana tries every endpoint in `elasticsearch.hosts`, so even one unreachable node can cause the log. Use `https` if your cluster requires encrypted communication.

## How to resolve it

### Test connectivity

Try to connect to each host in `elasticsearch.hosts` using `curl`:

```console
curl http://es01:9200/
```

If using TLS:

```console
# Insecure test
curl -u elastic -k https://es01:9200/

# Secure test
curl -u elastic --cacert ~/certs/ca/ca.crt https://es01:9200/
```

You should see a response like:

```console-result
{
  "name" : "node01",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "fxP-R0FTRcmTl_AWs7-DiA",
  "version" : {
    "number" : "7.13.3",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "5d21bea28db1e89ecc1f66311ebdec9dc3aa7d64",
    "build_date" : "2021-07-02T12:06:10.804015202Z",
    "build_snapshot" : false,
    "lucene_version" : "8.8.2"
  },
  "tagline" : "You Know, for Search"
}
```

If all else fails, refer to your Kibana logs for more details and context.

