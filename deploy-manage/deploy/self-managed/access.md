---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/access.html
---

# Access [access]

The fastest way to access {{kib}} is to use our hosted {{es}} Service. If you [installed {{kib}} on your own](install-kibana.md), access {{kib}} through the web application.


## Set up on cloud [_set_up_on_cloud]

There’s no faster way to get started than with {{ecloud}}:

1. [Get a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
2. Log into [Elastic Cloud](https://cloud.elastic.co?page=docs&placement=docs-body).
3. Click **Create deployment**.
4. Give your deployment a name.
5. Click **Create deployment** and download the password for the `elastic` user.

That’s it! Now that you are up and running, it’s time to get some data into {{kib}}. {{kib}} will open as soon as your deployment is ready.


## Log on to the web application [log-on-to-the-web-application]

If you are using a self-managed deployment, access {{kib}} through the web application on port 5601.

1. Point your web browser to the machine where you are running {{kib}} and specify the port number. For example, `localhost:5601` or `http://YOURDOMAIN.com:5601`.

    To remotely connect to {{kib}}, set [server.host](configure.md#server-host) to a non-loopback address.

2. Log on to your account.
3. Go to the home page, then click **{{kib}}**.
4. To make the {{kib}} page your landing page, click **Make this my landing page**.

## Resources
* [Troubleshoot: Check {{kib}} server status](/troubleshoot/kibana/access.md)
* [Troubleshoot: Error: {{kib}} server is not ready yet](/troubleshoot/kibana/error-server-not-ready.md) 