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
This guide shows you how to run an OpenAI-compatible large language model with [vLLM](https://docs.vllm.ai/en/latest/) and connect it to Elastic. The setup runs inside Docker or Podman, is served through an Nginx reverse proxy, and does not require any outbound network access. This makes it a safe option for air-gapped environments or deployments with strict network controls.

The steps below show one example configuration, but you can use any model supported by vLLM, including private and gated models on Hugging Face.

## Step 1: Configure your host server

To support this use case, you need a powerful server. For example, we tested a server with the following specifications:

* Operating system: Ubuntu 24.10
* Machine type: a2-ultragpu-2g
* vCPU: 24 (12 cores)
* Architecture: x86/64
* CPU Platform: Intel Cascade Lake
* Memory: 340GB
* Accelerator: 2 x NVIDIA A100 80GB GPUs

Set up your server then install all necessary GPU drivers.

## Step 2: Generate auth tokens

:::::{stepper}

::::{step} Create a Hugging Face user token
1. (Optional) If you plan to use a gated model (such as Llama 3.1) or a private model, create a [Hugging Face user access token](https://huggingface.co/docs/hub/en/security-tokens).
  1. Log in to your Hugging Face account.
  2. Navigate to **Settings > Access Tokens**.
  3. Create a new token with at least `read` permissions. Save it in a secure location.
::::

::::{step} Create an OpenAI-compatible secret token
2. Generate a strong, random string and save it in a secure location. You need the secret token to authenticate communication between Elastic and your reverse proxy.
::::

:::::



## Step 3: Run your vLLM container

To pull and run your chosen vLLM image:

1. Connect to your server using SSH.
2. Run the following terminal command to start the vLLM server, download the model, and expose it on port 8000:

```bash
docker run \
  --name [YOUR_MODEL_ID] \ <1>
  --gpus all \ <2>
  -v /root/.cache/huggingface:/root/.cache/huggingface \ <3>
  --env HUGGING_FACE_HUB_TOKEN=xxxx \ <4>
  --env VLLM_API_KEY=xxxx \ <5>
  -p 8000:8000 \ <6>
  --ipc=host \ <7>
  vllm/vllm-openai:v0.9.1 \ <8>
  --model mistralai/[YOUR_MODEL_ID] \ <9>
  --tool-call-parser mistral \ <10>
  --tokenizer-mode mistral \ <11>
  --config-format mistral \ <12>
  --load-format mistral \ <13>
  --enable-auto-tool-choice \ <14>
  --gpu-memory-utilization 0.90 \ <15>
  --tensor-parallel-size 2 <16>
```
1. Defines a name for the container.
2. Exposes all available GPUs to the container.
3. Sets the Hugging Face cache directory (optional if used with `HUGGING_FACE_HUB_TOKEN`).
4. Sets the environment variable for your Hugging Face token (only required for gated models).
5. vLLM API key used for authentication between {{ecloud}} and vLLM.
6. Maps port 8000 on the host to port 8000 in the container.
7. Enables sharing memory between host and container.
8. Specifies the official vLLM OpenAI-compatible image, version 0.9.1. This is the version of vLLM we recommend.
9. ID of the Hugging Face model you wish to serve.
10. Mistral-specific tool call parser. Refer to the Hugging Face model card for recommended values.
11. Mistral-specific tokenizer mode. Refer to the Hugging Face model card for recommended values.
12. Mistral-specific configuration format. Refer to the Hugging Face model card for recommended values.
13. Mistral-specific load format. Refer to the Hugging Face model card for recommended values.
14. Enables automatic function calling.
15. Limits max GPU used by vLLM (may vary depending on the machine resources available).
16. This value should match the number of available GPUs (in this case, 2). This is critical for performance on multi-GPU systems.

3. Verify the container's status by running the `docker ps -a` command. The output should show the value you specified for the `--name` parameter.

## Step 4: Expose the API with a reverse proxy

Using a reverse proxy improves stability for this use case. This example uses Nginx, which supports monitoring by means of Elastic's native Nginx integration. The example Nginx configuration forwards traffic to the vLLM container and uses a secret token for authentication.

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

## Step 5: Configure the connector in your Elastic deployment

Finally, create the connector within your Elastic deployment to link it to your vLLM instance.

1. In {{kib}}, navigate to the **Connectors** page, click **Create Connector**, and select **OpenAI**.
2. Give the connector a descriptive name, such as `vLLM - Mistral Small 3.2`.
3. In **Connector settings**, configure the following:
  * For **Select an OpenAI provider**, select **Other (OpenAI Compatible Service)**.
  * For **URL**, enter your server's public URL followed by `/v1/chat/completions`.
4. For **Default Model**, enter `mistralai/[YOUR_MODEL_ID]`.
5. For **Authentication**, configure the following:
  * For **API key**, enter the secret token you created in Step 1 and specified in your Nginx configuration file.
  * If your chosen model supports tool use, then turn on **Enable native function calling**.
6. Click **Save**
7. To enable the connector to work with AI Assistant for Security, add the following to your `config/kibana.yml` file:
  ```
  feature_flags.overrides:  
       securitySolution.inferenceChatModelDisabled: true  
  ```
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
To run a different model: s
* Stop the current container and run a new one with an updated `--model` parameter.
* Update your {{kib}} connector's **Default model** parameter to match the new model ID.
:::