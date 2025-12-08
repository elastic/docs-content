---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/connect-to-byo-llm.html
  - https://www.elastic.co/guide/en/serverless/current/connect-to-byo-llm.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Connect to your own local LLM using LM Studio

This page provides instructions for setting up a connector to a large language model (LLM) of your choice using LM Studio. This allows you to use your chosen model within {{elastic-sec}}. You’ll first need to set up a reverse proxy to communicate with {{elastic-sec}}, then set up LM Studio on a server, and finally configure the connector in your Elastic deployment. [Learn more about the benefits of using a local LLM](https://www.elastic.co/blog/ai-assistant-locally-hosted-models).

This example uses a single server hosted in GCP to run the following components:

* LM Studio with the [Mistral-Nemo-Instruct-2407](https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407) model
* A reverse proxy using Nginx to authenticate to Elastic Cloud

:::{image} /solutions/images/security-lms-studio-arch-diagram.png
:alt: Architecture diagram for this guide
:::

::::{note}
For testing, you can use alternatives to Nginx such as [Azure Dev Tunnels](https://learn.microsoft.com/en-us/azure/developer/dev-tunnels/overview) or [Ngrok](https://ngrok.com/), but using Nginx makes it easy to collect additional telemetry and monitor its status by using Elastic’s native Nginx integration. While this example uses cloud infrastructure, it could also be replicated locally without an internet connection.
::::


::::{note}
For information about the performance of open-source models on tasks within {{elastic-sec}}, refer to the [LLM performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md).
::::



## Configure your reverse proxy [_configure_your_reverse_proxy]

::::{note}
If your Elastic instance is on the same host as LM Studio, you can skip this step. Also, check out our [blog post](https://www.elastic.co/blog/herding-llama-3-1-with-elastic-and-lm-studio) that walks through the whole process of setting up a single-host implementation.
::::


You need to set up a reverse proxy to enable communication between LM Studio and Elastic. For more complete instructions, refer to a guide such as [this one](https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-reverse-proxy-on-ubuntu-22-04).

The following is an example Nginx configuration file:

```nginx
server {
    listen                          80;
    listen                          [::]:80;
    server_name                     <yourdomainname.com>;
    server_tokens off;
    add_header x-xss-protection "1; mode=block" always;
    add_header x-frame-options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    return 301                      https://$server_name$request_uri;
}

server {

    listen                          443 ssl http2;
    listen                          [::]:443 ssl http2;
    server_name                     <yourdomainname.com>;
    server_tokens off;
    ssl_certificate                 /etc/letsencrypt/live/<yourdomainname.com>/fullchain.pem;
    ssl_certificate_key             /etc/letsencrypt/live/<yourdomainname.com>/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets on;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_prefer_server_ciphers on;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header x-xss-protection "1; mode=block" always;
    add_header x-frame-options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/<yourdomainname.com>/fullchain.pem;
    resolver 1.1.1.1;
    location / {

    if ($http_authorization != "Bearer <secret token>") {
    return 401;
}

    proxy_pass http://localhost:1234/;
   }

}
```

::::{important}
If using the example configuration file above, you must replace several values:

* Replace `<secret token>` with your actual token, and keep it safe since you’ll need it to set up the {{elastic-sec}} connector.
* Replace `<yourdomainname.com>` with your actual domain name.
* Update the `proxy_pass` value at the bottom of the configuration if you decide to change the port number in LM Studio to something other than 1234.

::::



### (Optional) Set up performance monitoring for your reverse proxy [_optional_set_up_performance_monitoring_for_your_reverse_proxy]

You can use Elastic’s [Nginx integration](https://docs.elastic.co/en/integrations/nginx) to monitor performance and populate monitoring dashboards in the {{security-app}}.


## Configure LM Studio and download a model [_configure_lm_studio_and_download_a_model]

First, install [LM Studio](https://lmstudio.ai/). LM Studio supports the OpenAI SDK, which makes it compatible with Elastic’s OpenAI connector, allowing you to connect to any model available in the LM Studio marketplace.

You must launch the application using its GUI before doing so using the CLI. For example, use Chrome RDP with an [X Window System](https://cloud.google.com/architecture/chrome-desktop-remote-on-compute-engine). After you’ve opened the application the first time using the GUI, you can start it by using `sudo lms server start` in the CLI.

Once you’ve launched LM Studio:

1. Go to LM Studio’s Search window.
2. Search for an LLM (for example, `Mistral-Nemo-Instruct-2407`). Your chosen model must include `instruct` in its name in order to work with Elastic.
3. After you find a model, view download options and select a recommended version (green). For best performance, select one with the thumbs-up icon that indicates good performance on your hardware.
4. Download one or more models.

::::{important}
For security reasons, before downloading a model, verify that it is from a trusted source. It can be helpful to review community feedback on the model (for example using a site like Hugging Face).
::::


:::{image} /solutions/images/security-lms-model-select.png
:alt: The LM Studio model selection interface
:::

In this example we used [`mistralai/Mistral-Nemo-Instruct-2407`](https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407). It has 12B total parameters, a 128,000 token context window, and uses GGUF [quanitization](https://huggingface.co/docs/transformers/main/en/quantization/overview). For more information about model names and format information, refer to the following table.

| Model Name | Parameter Size | Tokens/Context Window | Quantization Format |
| --- | --- | --- | --- |
| Name of model, sometimes with a version number. | LLMs are often compared by their number of parameters — higher numbers mean more powerful models. | Tokens are small chunks of input information. Tokens do not necessarily correspond to characters. You can use [Tokenizer](https://platform.openai.com/tokenizer) to see how many tokens a given prompt might contain. | Quantization reduces overall parameters and helps the model to run faster, but reduces accuracy. |
| Examples: Llama, Mistral, Phi-3, Falcon. | The number of parameters is a measure of the size and the complexity of the model. The more parameters a model has, the more data it can process, learn from, generate, and predict. | The context window defines how much information the model can process at once. If the number of input tokens exceeds this limit, input gets truncated. | Specific formats for quantization vary, most models now support GPU rather than CPU offloading. |


## Load a model in LM Studio [_load_a_model_in_lm_studio]

After downloading a model, load it in LM Studio using the GUI or LM Studio’s [CLI tool](https://lmstudio.ai/blog/lms).


### Option 1: load a model using the CLI (Recommended) [_option_1_load_a_model_using_the_cli_recommended]

It is a best practice to download models from the marketplace using the GUI, and then load or unload them using the CLI. The GUI allows you to search for models, whereas the CLI allows you to use `lms get` to search for models. The CLI provides a good interface for loading and unloading.

Once you’ve downloaded a model, use the following commands in your CLI:

1. Verify LM Studio is installed: `lms`
2. Check LM Studio’s status: `lms status`
3. List all downloaded models: `lms ls`
4. Load a model: `lms load`.

:::{image} /solutions/images/security-lms-cli-welcome.png
:alt: The CLI interface during execution of initial LM Studio commands
:::

After the model loads, you should see a `Model loaded successfully` message in the CLI. Select a model using the arrow and **Enter** keys.

:::{image} /solutions/images/security-lms-studio-model-loaded-msg.png
:alt: The CLI message that appears after a model loads
:::

To verify which model is loaded, use the `lms ps` command.

:::{image} /solutions/images/security-lms-ps-command.png
:alt: The CLI message that appears after running lms ps
:::

If your model uses NVIDIA drivers, you can check the GPU performance with the `sudo nvidia-smi` command.


### Option 2: load a model using the GUI [_option_2_load_a_model_using_the_gui]

Refer to the following video to see how to load a model using LM Studio’s GUI. You can change the **port** setting, which is referenced in the Nginx configuration file. Note that the **GPU offload** was set to **Max**. The following video demonstrates this process (click to watch).

[![byollm-load-model-gui-video](https://play.vidyard.com/c4AxH8d9tWMnwNp5J6bcfX.jpg)](https://videos.elastic.co/watch/c4AxH8d9tWMnwNp5J6bcfX?)


## (Optional) Collect logs using Elastic’s Custom Logs integration [_optional_collect_logs_using_elastics_custom_logs_integration]

You can monitor the performance of the host running LM Studio using Elastic’s [Custom Logs integration](https://docs.elastic.co/en/integrations/log). This can also help with troubleshooting. Note that the default path for LM Studio logs is `/tmp/lmstudio-server-log.txt`, as in the following screenshot:

:::{image} /solutions/images/security-lms-custom-logs-config.png
:alt: The configuration window for the custom logs integration
:::


## Configure the connector in your Elastic deployment [_configure_the_connector_in_your_elastic_deployment]

Finally, configure the connector:

1. Log in to your Elastic deployment.
2. Find the **Connectors** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Then click **Create Connector**, and select **OpenAI**. The OpenAI connector enables this use case because LM Studio uses the OpenAI SDK.
3. Name your connector to help keep track of the model version you are using.
4. Under **Select an OpenAI provider**, select **Other (OpenAI Compatible Service)**.
5. Under **URL**, enter the domain name specified in your Nginx configuration file, followed by `/v1/chat/completions`.
6. Under **Default model**, enter `local-model`.
7. Under **API key**, enter the secret token specified in your Nginx configuration file.
8. Click **Save**.

:::{image} /solutions/images/security-lms-edit-connector.png
:alt: The Edit connector page in the {{security-app}}
:::

Setup is now complete. You can use the model you’ve loaded in LM Studio to power Elastic’s generative AI features. You can test a variety of models as you interact with AI Assistant to see what works best without having to update your connector.

::::{note}
While local models work well for [AI Assistant](/solutions/security/ai/ai-assistant.md), we recommend you use one of [these models](/solutions/security/ai/large-language-model-performance-matrix.md) for interacting with [Attack discovery](/solutions/security/ai/attack-discovery.md). As local models become more performant over time, this is likely to change.
::::
