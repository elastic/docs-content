You can test that your {{es}} node is running by sending an HTTPS request to port `9200` on `localhost`:

```sh subs=true
curl --cacert {{es-conf}}{{slash}}certs{{slash}}http_ca.crt {{escape}} <1>
-u elastic:$ELASTIC_PASSWORD https://localhost:9200 <2>
```
1. `--cacert`: Path to the generated `http_ca.crt` certificate for the HTTP layer.
2. Ensure that you use `https` in your call, or the request will fail.



The call returns a response like this:

```js
{
  "name" : "Cp8oag6",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "AT69_T_DTp-1qgIJlatQqA",
  "version" : {
    "number" : "9.0.0-SNAPSHOT",
    "build_type" : "tar",
    "build_hash" : "f27399d",
    "build_flavor" : "default",
    "build_date" : "2016-03-30T09:51:41.449Z",
    "build_snapshot" : false,
    "lucene_version" : "10.0.0",
    "minimum_wire_compatibility_version" : "1.2.3",
    "minimum_index_compatibility_version" : "1.2.3"
  },
  "tagline" : "You Know, for Search"
}
```