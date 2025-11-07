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

1. (Optional) If you plan to use a gated model (like Llama 3.1) or a private model, you need to create a [Hugging Face user access token](https://huggingface.co/docs/hub/en/security-tokens).
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

.**Click to expand an explanation of the command** 
[%collapsible]
=====
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
=====

