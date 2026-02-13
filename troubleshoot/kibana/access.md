---
navigation_title: Server status
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/access.html#status
applies_to:
  stack: all
products:
  - id: kibana
---

# Check {{kib}} server status [access]
% The fastest way to access {{kib}} is to use our hosted {{es}} Service. If you [installed {{kib}} on your own](../../deploy-manage/deploy/self-managed/install-kibana.md), access {{kib}} through the web application.
% 
% 
% ## Set up on cloud [_set_up_on_cloud]
% 
% There’s no faster way to get started than with {{ecloud}}:
% 
% 1. [Get a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
% 2. Log into [Elastic Cloud](https://cloud.elastic.co?page=docs&placement=docs-body).
% 3. Click **Create deployment**.
% 4. Give your deployment a name.
% 5. Click **Create deployment** and download the password for the `elastic` user.
% 
% That’s it! Now that you are up and running, it’s time to get some data into {{kib}}. {{kib}} will open as soon as your deployment is ready.
% 
% 
% ## Log on to the web application [log-on-to-the-web-application]
% 
% If you are using a self-managed deployment, access {{kib}} through the web application on port 5601.
% 
% 1. Point your web browser to the machine where you are running {{kib}} and specify the port number. For example, `localhost:5601` or `http://YOURDOMAIN.com:5601`.
% 
%     To remotely connect to {{kib}}, set [server.host](kibana://reference/configuration-reference/general-settings.md#server-host) to a non-loopback address.
% 
% 2. Log on to your account.
% 3. Go to the home page, then click **{{kib}}**.
% 4. To make the {{kib}} page your landing page, click **Make this my landing page**.
% 
% 
% ## Check the {{kib}} status [status]
% 

% cf (../../deploy-manage/deploy/self-managed/access.md#status) 

The status page displays information about the server resource usage and installed plugins. It only reports for the individual responding {{kib}} instance.

To view {{kib}}'s status, use the `status` endpoint. For example, `localhost:5601/status`.

:::{image} /troubleshoot/images/kibana-kibana-status-page-7_14_0.png
:alt: Kibana server status page
:screenshot:
:::

For JSON-formatted server status details, use the [{{kib}} current status API](https://www.elastic.co/docs/api/doc/kibana/v9/operation/operation-get-status). For example, `localhost:5601/api/status`.

## Triage {{kib}} health using the status API [access-triage]

The following steps demonstrate a typical investigative flow. It assumes the [{{kib}} current status API](https://www.elastic.co/docs/api/doc/kibana/v9/operation/operation-get-status) is saved locally as `kibana_status.json` and uses third-party tool [JQ](https://jqlang.github.io/jq/) as a JSON processor.

1. Check the overall status.

   The UI will report "Kibana status is" and then the status. You can see this in the API output by running:

   ```bash
   cat kibana_status.json | jq '{ overall: .status.overall.level }'
   ```
    
2. Check core dependencies.

    The UI will report "Plugin Status" with a list of plugins. The core plugins prefix `core`. You can check these in the API output by running the following command:

  ```bash
  cat kibana_status.json | jq -r '.status.core|{ elasticsearch: .elasticsearch.level, savedObjects: .savedObjects.level }'
  ```

    Before you review any further plugins, check that the `elasticsearch` and `savedObjects` are healthy and resolve any issues:
  
  * If the connection to {{es}} is unhealthy, refer to [](/troubleshoot/kibana/error-server-not-ready.md).
    * If the connection to Saved Objects is unhealthy, refer to [](/troubleshoot/kibana/migration-failures.md).

3. Check non-core plugins.

    The UI **Plugin Status** list reports the status of the other plugins running on the instance. Plugins can be dependent upon each other. You should first check the health of the common underlying plugins: `alerting`, `reporting`, `ruleRegistry`, `savedObjects`, `security`, and `taskManager`. 
    
    You can check these in the API output by running the following command:

    ```bash
    cat kibana_status.json | jq -rc '.status.plugins|to_entries[]|select(.key=="taskManager" or .key=="savedObjects" or .key=="security" or .key=="reporting" or .key=="ruleRegistry" or .key=="alerting") |{plugin:.key, status:.value.level, reason:.value.summary}'
    ```

    For an example of a degraded Task Manager and how that degradation cascades into other plugins, refer to [Troubleshooting Kibana health](https://www.elastic.co/blog/troubleshooting-kibana-health#check-dependencies). For more information on investigating a degraded Task Manager, refer to [](/troubleshoot/kibana/task-manager.md).

## Next steps

For a deeper troubleshooting walkthrough, refer to our Troubleshooting Kibana health [blog](https://www.elastic.co/blog/troubleshooting-kibana-health) and [video](https://www.youtube.com/watch?v=AlgGYcpGvOA&list=PL_mJOmq4zsHbQlfEMEh_30_LuV_hZp-3d&index=28).
