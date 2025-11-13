---
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Connect to your own LLM using vLLM (air gapped environments)
This page provides an example of how to connect to a self-hosted, open-source large language model (LLM) using the [vLLM inference engine](https://docs.vllm.ai/en/latest/) running in a Docker or Podman container. 

Using this approach, you can power elastic's AI features with an LLM of your choice deployed and managed on infrastructure you control without granting external network access, which is particularly useful for air-gapped environments and organizations with strict network security policies. 

## Requirements

* Docker or Podman.
* Necessary GPU drivers.

## Server used in this example

This example uses a GCP server configured as follows:

* Operating system: Ubuntu 24.10
* Machine type: a2-ultragpu-2g
* vCPU: 24 (12 cores)
* Architecture: x86/64
* CPU Platform: Intel Cascade Lake
* Memory: 340GB
* Accelerator: 2 x NVIDIA A100 80GB GPUs
* Reverse Proxy: Nginx

## Outline
The process involves four main steps:

1. Configure your host server with the necessary GPU resources.
2. Run the desired model in a vLLM container.
3. Use a reverse proxy like Nginx to securely expose the endpoint to {{ecloud}}.
4. Configure the OpenAI connector in your Elastic deployment.

## Step 1: Configure your host server

1. (Optional) If you plan to use a gated model (such as Llama 3.1) or a private model, create a [Hugging Face user access token](https://huggingface.co/docs/hub/en/security-tokens).
  1. Log in to your Hugging Face account.
  2. Navigate to **Settings > Access Tokens**.
  3. Create a new token with at least `read` permissions. Save it in a secure location.
2. Create an OpenAI-compatible secret token. Generate a strong, random string and save it in a secure location. You need the secret token to authenticate communication between {{ecloud}} and your Nginx reverse proxy.
3. Install any necessary GPU drivers. 

## Step 2: Run your vLLM container

To pull and run your chosen vLLM image:

1. Connect to your server using SSH.
2. Run the following terminal command to start the vLLM server, download the model, and expose it on port 8000:

```bash
docker run --name Mistral-Small-3.2-24B --gpus all \
-v /root/.cache/huggingface:/root/.cache/huggingface \
--env HUGGING_FACE_HUB_TOKEN=xxxx \
--env VLLM_API_KEY=xxxx \
-p 8000:8000 \
--ipc=host \
vllm/vllm-openai:v0.9.1 \
--model mistralai/Mistral-Small-3.2-24B-Instruct-2506 \
--tool-call-parser mistral \
--tokenizer-mode mistral \
--config-format mistral \
--load-format mistral \
--enable-auto-tool-choice \
--gpu-memory-utilization 0.90 \
--tensor-parallel-size 2
```

For an explanation of each of the command's parameters, refer to the following list:

```
`--gpus all`: Exposes all available GPUs to the container.
`--name`: Defines a name for the container.
`-v /root/.cache/huggingface:/root/.cache/huggingface`: Hugging Face cache directory (optional if used with `HUGGING_FACE_HUB_TOKEN`).
`-e HUGGING_FACE_HUB_TOKEN`: Sets the environment variable for your Hugging Face token (only required for gated models).
`--env VLLM_API_KEY`: vLLM API Key used for authentication between {{ecloud}} and vLLM.
`-p 8000:8000`: Maps port 8000 on the host to port 8000 in the container.
`–ipc=host`: Enables sharing memory between host and container.
`vllm/vllm-openai:v0.9.1`: Specifies the official vLLM OpenAI-compatible image, version 0.9.1. This is the version of vLLM we recommend.
`--model`: ID of the Hugging Face model you wish to serve. In this example it represents the `Mistral-Small-3.2-24B` model.
`--tool-call-parser mistral \`, `--tokenizer-mode mistral \`, `--config-format mistral \`, and `--load-format mistral`: Mistral specific parameters, refer to the Hugging Face model card for recommended values.
`-enable-auto-tool-choice`: Enables automatic function calling.
`--gpu-memory-utilization 0.90`: Limits max GPU used by vLLM (may vary depending on the machine resources available).
`--tensor-parallel-size 2`: This value should match the number of available GPUs (in this case, 2). This is critical for performance on multi-GPU systems. 
```


3. Verify the container's status by running the `docker ps -a` command. The output should show the value you specified for the `--name` parameter.

## Step 3: Expose the API with a reverse proxy

This example uses Nginx to create a reverse proxy. This improves stability and enables monitoring by means of Elastic's native Nginx integration. The following example configuration forwards traffic to the vLLM container and uses a secret token for authentication.

1. Install Nginx on your server.
2. Create a configuration file, for example at `/etc/nginx/sites-available/default`. Give it the following content:

```
server {
    listen 80;
    server_name <yourdomainname.com>;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name <yourdomainname.com>;

    ssl_certificate /etc/letsencrypt/live/<yourdomainname.com>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<yourdomainname.com>/privkey.pem;

    location / {
        if ($http_authorization != "Bearer <secret token>") {
            return 401;
        }
        proxy_pass http://localhost:8000/;
    }
}
```

3. Enable and restart Nginx to apply the configuration.

:::{note}
For quick testing, you can use [ngrok](https://ngrok.com/) as an alternative to Nginx, but it is not recommended for production use.
:::

## Step 4: Configure the connector in your elastic deployment

Finally, create the connector within your Elastic deployment to link it to your vLLM instance.

1. Log in to {{kib}}.
2. Navigate to the **Connectors** page, click **Create Connector**, and select **OpenAI**.
3. Give the connector a descriptive name, such as `vLLM - Mistral Small 3.2`.
4. In **Connector settings**, configure the following:
  * For **Select an OpenAI provider**, select **Other (OpenAI Compatible Service)**.
  * For **URL**, enter your server's public URL followed by `/v1/chat/completions`.
5. For **Default Model**, enter `mistralai/Mistral-Small-3.2-24B-Instruct-2506` or the model ID you used during setup.
6. For **Authentication**, configure the following:
  * For **API key**, enter the secret token you created in Step 1 and specified in your Nginx configuration file.
  * If your chosen model supports tool use, then turn on **Enable native function calling**.
7. Click **Save**
8. Finally, open the **AI Assistant for Security** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). 
  * On the **Conversations** tab, turn off **Streaming**.
  * If your model supports tool use, then on the **System prompts** page, create a new system prompt with a variation of the following prompt, to prevent your model from returning tool calls in AI Assistant conversations:
  
  ```
  You are a model running under OpenAI-compatible tool calling mode.
  
  Rules:
  1. When you want to invoke a tool, never describe the call in text.
  2. Always return the invocation in the `tool_calls` field.
  3. The `content` field must remain empty for any assistant message that performs a tool call.
  4. Only use tool calls defined in the "tools" parameter.
  ```

Setup is now complete. The model served by your vLLM container can now power Elastic's generative AI features.


:::{note}
To run a different model, stop the current container and run a new one with an updated `--model` parameter.
:::