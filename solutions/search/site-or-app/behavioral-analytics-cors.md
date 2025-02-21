---
navigation_title: "Set up CORs"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/behavioral-analytics-cors.html
applies_to:
  stack:
  serverless:
---



# Set up CORs [behavioral-analytics-cors]


Behavioral Analytics sends events directly to the {{es}} API. This means that the browser makes requests to the {{es}} API directly. {{es}} supports [Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS), but this feature is disabled by default. Therefore the browser will block these requests.

There are two workarounds for this:

* [Enable CORS on {{es}}](#behavioral-analytics-cors-enable-cors-elasticsearch)
* [Proxy the request through a server that supports CORS](#behavioral-analytics-cors-proxy-request)


## Enable CORS on {{es}} [behavioral-analytics-cors-enable-cors-elasticsearch] 

This is the simplest option. Enable CORS on {{es}} by adding the following to your `elasticsearch.yml` file:

```yaml
http.cors.allow-origin: "*" # Only use unrestricted value for local development
# Use a specific origin value in production, like `http.cors.allow-origin: "https://<my-website-domain.example>"`
http.cors.enabled: true
http.cors.allow-credentials: true
http.cors.allow-methods: OPTIONS, POST
http.cors.allow-headers: X-Requested-With, X-Auth-Token, Content-Type, Content-Length, Authorization, Access-Control-Allow-Headers, Accept
```

On Elastic Cloud, you can do this by [editing your {{es}} user settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md#ec-add-user-settings).

1. From your deployment menu, go to the **Edit** page.
2. In the **{{es}}** section, select **Manage user settings and extensions**.
3. Update the user settings with the configuration above.
4. Select **Save changes**.


## Proxy the request through a server that supports CORS [behavioral-analytics-cors-proxy-request] 

If you are unable to enable CORS on {{es}}, you can proxy the request through a server that supports CORS. This is more complicated, but is a viable option.

