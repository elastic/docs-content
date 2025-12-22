---
applies_to:
  stack:
  deployment:
    eck:
    ess:
    ece:
    self:
navigation_title: "Error: Unable to retrieve node fs stats"
---

# Fix error: Unable to retrieve node fs stats [unable-to-retrieve-node-fs-stats]

```console
Error: unable to retrieve node fs stats
```

This error occurs when {{kib}} or another {{es}} client can't fetch version information from an {{es}} node. Without version information, the client can't confirm compatibility or proceed with requests.

Possible causes include network issues, incorrect configuration, or unavailable nodes. To diagnose, first try these general actions:

- Ensure that all nodes are up and running.
- Check the network connectivity between the client and the nodes.
- Verify configuration settings.

If the issue persists, check the {{es}} logs for details, then continue with the tips below.

## Check potential causes

This error typically appears in the {{kib}} logs during startup. Because {{kib}} acts as a client to {{es}}, it requires access to several resources:

- The cluster's host and port
- Authentication credentials, if required
- TLS settings, if applicable

If {{kib}} can't reach the configured nodes, it can't verify version compatibility and logs the `unable to retrieve` error. Check these possible access issues:

- One or more entries in `elasticsearch.hosts` are unreachable or misconfigured
- The `KBN_PATH_CONF` environment variable points to a different config file
- A firewall is blocking access between {{kib}} and {{es}}

## Configuration locations

Settings are defined in `kibana.yml`, usually located at `$KIBANA_HOME/config`. You can change the path as needed:

```bash
KBN_PATH_CONF=/home/kibana/config ./bin/kibana
```

Check the relevant settings:

```yaml
elasticsearch.hosts: ["http://localhost:9200"]
elasticsearch.username: "kibana"
elasticsearch.password: "your_password"
elasticsearch.ssl.certificateAuthorities: ["path/to/ca.crt"]
```
{{kib}} tries every endpoint in `elasticsearch.hosts`, so even one unreachable node can cause the error. Use `https` if your cluster requires encrypted communication.

### Test connectivity

Use `curl` to test the connection to each host in `elasticsearch.hosts`:

```bash
curl <ELASTICSEARCH_HOST_URL>:9200/
```

If you're using TLS, try one of the following:

```bash
# Insecure test
curl -u elastic -k https://es01:9200/

# Secure test
curl -u elastic --cacert ~/certs/ca/ca.crt https://es01:9200/
```

Example response:

```json
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

If you're still encountering issues, check the {{kib}} logs for more details and context.

