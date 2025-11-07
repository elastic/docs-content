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

This example was tested using a GCP server configured as follows:

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
  3. Create a new token with at least `read` permissions. Copy it to a secure location.
2. Create an OpenAI-compatible secret token. You will need a secret token to authenticate communication between {{ecloud}} and your Nginx reverse proxy. Generate a strong, random string and save it in a secure location. You will need it both when configuring Nginx and when configuring the Elastic connector.

## Step 2: Run your LLM with a vLLM container

To pull and run your chosen vLLM image:

1. Connect to your server via SSH.
2. Run the vLLM Docker Container: Execute the following command in your terminal. This command will start the vLLM server, download the model, and expose it on port 8000.