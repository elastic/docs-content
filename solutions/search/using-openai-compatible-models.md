---
applies_to:
  stack: ga
  serverless: ga
navigation_title: Using OpenAI compatible models
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Using OpenAI compatible models with the {{infer-cap}} API

{{es}} enables you to use LLMs through the {{infer}} API, supporting providers such as Amazon Bedrock, Cohere, Google AI, HuggingFace, OpenAI, and more, as a service.
It also allows you to use models deployed in your local environment that have an OpenAI compatible API.

This page shows you how to connect local models to {{es}} using Ollama.

[Ollama](https://ollama.com/) enables you to download and run LLM models on your own infrastructure.
For a list of available models compatible with Ollama, refer to this [page](https://ollama.com/library).

Using Ollama ensures that your interactions remain private, as the models run on your infrastructure.

## Overview

In this tutorial, you learn how to:

* download and run Ollama,
* use ngrok to expose your local web server hosting Ollama over the internet
* connect your local LLM to Playground

## Download and run Ollama

1. [Download Ollama](https://ollama.com/download).
2. Install Ollama using the downloaded file.
Enable the command line tool for Ollama during installation.
3. Choose a model from the [list of supported LLMs](https://ollama.com/library).
This tutorial uses `llama 3.2`.
4. Run the following command:
   ```shell
   ollama pull llama3.2
   ```

### Test the installed model

After installation, test the model.

1. Run `ollama run llama3.2` and ask a question, for example, "Are you working?"
If the model is installed successfully, you receive a valid response.
2. When the model is running, an API endpoint is enabled by default on port `11434`.
To test it, make a request to the API using the following command:
   ```shell
    curl http://localhost:11434/api/generate -d '{
   "model": "llama3.2",
   "prompt": "What is the capital of France?"
   }'
   ```
  
   Refer to the API [documentation](https://github.com/ollama/ollama/blob/main/docs/api.md) to learn more.
   The API returns a response similar to this:
   ```json
   {"model":"llama3.2","created_at":"2025-03-26T10:07:05.500614Z","response":"The","done":false}
   {"model":"llama3.2","created_at":"2025-03-26T10:07:05.519131Z","response":" capital","done":false}
   {"model":"llama3.2","created_at":"2025-03-26T10:07:05.537432Z","response":" of","done":false}
   {"model":"llama3.2","created_at":"2025-03-26T10:07:05.556016Z","response":" France","done":false}
   {"model":"llama3.2","created_at":"2025-03-26T10:07:05.574815Z","response":" is","done":false}
   {"model":"llama3.2","created_at":"2025-03-26T10:07:05.592967Z","response":" Paris","done":false}
   {"model":"llama3.2","created_at":"2025-03-26T10:07:05.611558Z","response":".","done":false}
   {"model":"llama3.2","created_at":"2025-03-26T10:07:05.630715Z","response":"","done":true,"done_reason":"stop","context":[128006,9125,128007,271,38766,1303,33025,2696,25,6790,220,2366,18,271,128009,128006,882,128007,271,3923,374,279,6864,315,9822,30,128009,128006,78191,128007,271,791,6864,315,9822,374,12366,13],"total_duration":2232589542,"load_duration":1052276792,"prompt_eval_count":32,"prompt_eval_duration":1048833625,"eval_count":8,"eval_duration":130808916}
   ```

## Expose the endpoint using ngrok

Since the created endpoint only works locally, it cannot be accessed from external services (for example, your Elastic Cloud instance).
[ngrok](https://ngrok.com/) enables you to expose a local port with a public URL.

::::{warning}
Exposing a local endpoint to the internet can introduce security risks. Anyone with the public URL may be able to send requests to your service. Avoid exposing sensitive data or functionality, and consider using authentication or access restrictions to limit who can interact with the endpoint.
::::

1. Create an ngrok account and follow the [official setup guide](https://dashboard.ngrok.com/get-started/setup).
2. After installing and configuring the ngrok agent, expose the Ollama port by running:
   ```shell
   ngrok http 11434 --host-header="localhost:11434"
   ```
   The command returns a public link that works as long as ngrok and the Ollama server are running locally:
   ```shell
   Session Status                online                                                                                                                                                                              
   Account                       xxxx@yourEmailProvider.com (Plan: Free)                                                                                                                                             
   Version                       3.18.4                                                                                                                                                                              
   Region                        United States (us)                                                                                                                                                                  
   Latency                       561ms                                                                                                                                                                               
   Web Interface                 http://127.0.0.1:4040                                                                                                                                                               
   Forwarding                    https://your-ngrok-endpoint.ngrok-free.app -> http://localhost:11434                                                                                                                   
   
   
   Connections                   ttl     opn     rt1     rt5     p50     p90                                                                                                                                         
                                 0       0       0.00    0.00    0.00    0.00
   ```

3. Copy the ngrok-generated URL from the `Forwarding` line.
4. Test the endpoint again using the new URL:
   ```shell
    curl https://your-ngrok-endpoint.ngrok-free.app/api/generate -d '{
   "model": "llama3.2",
   "prompt": "What is the capital of France?"
   }'
   ```
   The response should be similar to the previous one.

## Connecting the local LLM to Playground

:::{include} ../_snippets/connect-local-llm-to-playground.md
:::

## Using the local LLM with the {{infer}} API

:::{include} ../_snippets/use-local-llm-inference-api.md
:::

## Further reading

* [Using Ollama with the {{infer}} API](https://www.elastic.co/search-labs/blog/ollama-with-inference-api#expose-endpoint-to-the-internet-using-ngrok): A more comprehensive, end-to-end guide to using Ollama with {{es}}.
