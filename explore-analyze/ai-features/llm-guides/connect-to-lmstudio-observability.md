---
navigation_title: Connect to LM Studio for {{observability}}
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/connect-to-local-llm.html
applies_to:
  stack: ga 9.2
  serverless:
    observability: ga
products:
  - id: observability
---

# Connect to a local LLM for {{observability}} using LM Studio

:::{important}
Elastic doesn’t support the setup and configuration of local LLMs. The example provided is for reference only.
Before using a local LLM, evaluate its performance according to the [LLM performance matrix](/solutions/observability/llm-performance-matrix.md#evaluate-your-own-model).
:::

This page provides instructions for setting up a connector to a large language model (LLM) of your choice using LM Studio. This allows you to use your chosen model within the {{obs-ai-assistant}}. You’ll first need to set up LM Studio, then download and deploy a model via LM studio and finally configure the connector in your Elastic deployment.

::::{note}
If your Elastic deployment is not on the same network, you must configure an Nginx reverse proxy to authenticate with Elastic. Refer to [Configure your reverse proxy](https://www.elastic.co/docs/solutions/security/ai/connect-to-own-local-llm#_configure_your_reverse_proxy) for more detailed instructions.

You do not have to set up a proxy if LM Studio is running locally, or on the same network as your Elastic deployment.
::::

::::{note}
For information about the performance of open-source models on {{obs-ai-assistant}} tasks, refer to the [LLM performance matrix](/solutions/observability/llm-performance-matrix.md).
::::

This example uses a server hosted in GCP to configure LM Studio with the [Llama-3.3-70B-Instruct](https://huggingface.co/lmstudio-community/Llama-3.3-70B-Instruct-GGUF) model.

### Already running LM Studio? [skip-if-already-running]

If you've already installed LM Studio, the server is running, and you have a model loaded (with a context window of at least 64K tokens), skip directly to [Configure the connector in your Elastic deployment](#configure-the-connector-in-your-elastic-deployment).

## Configure LM Studio and download a model [configure-lm-studio-and-download-a-model]

LM Studio supports the OpenAI SDK, which makes it compatible with Elastic’s OpenAI connector, allowing you to connect to any model available in the LM Studio marketplace.

To get started with LM Studio:

1. Install [LM Studio](https://lmstudio.ai/).
2. You must launch the application using its GUI before being able to use the CLI. Depending on where you're deploying, use one of the following methods:
    * **Local deployments**: Launch LM Studio using the GUI.
    * **GCP deployments**: Launch using Chrome RDP with an [X Window System](https://cloud.google.com/architecture/chrome-desktop-remote-on-compute-engine).
    * **Other cloud platform deployments**: Launch using any secure remote desktop (RDP, VNC over SSH tunnel, or X11 forwarding) as long as you can open the LM Studio GUI once.
3. After you’ve opened the application for the first time using the GUI, start the server using `sudo lms server start` in the [CLI](https://lmstudio.ai/docs/cli/server-start).

Once you’ve launched LM Studio:

1. Go to LM Studio’s Discover window.
2. Search for an LLM (for example, `Llama 3.3`). Your chosen model must include `instruct` in its name (specified in download options) in order to work with Elastic.
3. We recommend you use models published by a trusted source or verified authors (indicated by the purple verification badge next to the model name).
4. After you find a model, view download options and select a recommended option (green). For best performance, select one with the thumbs-up icon that indicates good performance on your hardware.
5. Download one or more models.

::::{important}
For security reasons, before downloading a model, verify that it is from a trusted source or by a verified author. It can be helpful to review community feedback on the model (for example using a site like Hugging Face).
::::

:::{image} /solutions/images/observability-ai-assistant-lms-model-selection.png
:alt: The LM Studio model selection interface with download options
:::

Throughout this documentation, we used [`llama-3.3-70b-instruct`](https://lmstudio.ai/models/meta/llama-3.3-70b). It has 70B total parameters, a 128,000 token context window, and uses GGUF [quantization](https://huggingface.co/docs/transformers/main/en/quantization/overview). For more information about model names and format information, refer to the following table.

| Attribute | Description |
| --- | --- |
| **Model Name** | LLM model name, sometimes with a version number (e.g., Llama, Mistral). |
| **Parameter Size** | Number of parameters, which measures the size and complexity of a model (more parameters = more data it can process, learn from, generate, and predict). |
| **Tokens / Context Window** | Tokens are small chunks of input information that don't necessarily correspond to characters. Use the [Tokenizer](https://platform.openai.com/tokenizer) to estimate how many tokens a prompt contains. The context window defines how much information the model can process at once. If the number of input tokens exceeds this limit, the input is truncated. |
| **Quantization Format** | Type of quantization applied. Quantization reduces overall parameters and increases model speed, but reduces accuracy. Most models now support GPU offloading rather than CPU offloading. |

::::{important}
The {{obs-ai-assistant}} requires a model with at least a 64,000 token context window.
::::

## Load a model in LM Studio [load-a-model-in-lm-studio]

After downloading a model, load it in LM Studio using LM Studio’s [CLI tool](https://lmstudio.ai/docs/cli/load) or the GUI.

### Option 1: Load a model using the CLI (Recommended) [option-1-load-a-model-using-the-cli-recommended]

Once you’ve downloaded a model, use the following commands in your CLI:

1. Verify LM Studio is installed: `lms`
2. Check LM Studio’s status: `lms status`
3. List all downloaded models: `lms ls`
4. Load a model: `lms load llama-3.3-70b-instruct --context-length 64000 --gpu max`.

::::{important}
When loading a model, use the `--context-length` flag with a context window of 64,000 or higher.
Optionally, you can set how much to offload to the GPU by using the `--gpu` flag. `--gpu max` will offload all layers to GPU.
::::

After the model loads, you should see the message `Model loaded successfully` in the CLI.

:::{image} /solutions/images/observability-ai-assistant-model-loaded.png
:alt: The CLI message that appears after a model loads
:::

To verify which model is loaded, use the `lms ps` command.

:::{image} /solutions/images/observability-ai-assistant-lms-ps-command.png
:alt: The CLI message that appears after running lms ps
:::

If your model uses NVIDIA drivers, you can check the GPU performance with the `sudo nvidia-smi` command.

### Option 2: Load a model using the GUI [option-2-load-a-model-using-the-gui]

Once the model is downloaded, you'll find it in the **My Models** window in LM Studio.

1. Navigate to the **Developer** window.
2. Turn on the **Start server** toggle on the top left. Once the server is started, you'll see the address and port of the server. The default port is `1234`.
3. Click on **Select a model to load** and pick your model from the model dropdown.
4. Select the **Load** tab on the right side of the LM Studio GUI, and adjust the **Context Length** to 64,000. Reload the model to apply the changes.

::::{note}
To enable other devices on the same network to access the server, go to **Settings** and turn on **Serve on Local Network**.
::::

:::{image} /solutions/images/observability-ai-assistant-lm-studio-load-model-gui.png
:alt: Loading a model in LM studio developer tab
:::

## Configure the connector in your Elastic deployment [configure-the-connector-in-your-elastic-deployment]

Finally, configure the connector:

1. Log in to your Elastic deployment.
2. Find the **Connectors** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Then click **Create Connector**, and select **OpenAI**. The OpenAI connector works for this use case because LM Studio uses the OpenAI SDK.
3. Name your connector to help keep track of the model version you are using.
4. Under **Select an OpenAI provider**, select **Other (OpenAI Compatible Service)**.
5. Under **URL**, enter the host's IP address and port, followed by `/v1/chat/completions`. (If you have a reverse proxy set up, enter the domain name specified in your Nginx configuration file followed by `/v1/chat/completions`.)
6. Under **Default model**, enter `llama-3.3-70b-instruct`.
7. Under **API key**, fill in anything. (If you have a reverse proxy set up, enter the secret token specified in your Nginx configuration file.)
8. Click **Save**.

:::{image} /solutions/images/observability-ai-assistant-local-llm-connector-setup.png
:alt: The OpenAI create connector flyout
:::

Setup is now complete. You can use the model you’ve loaded in LM Studio to power Elastic’s generative AI features.

::::{note}
While local (open-weight) LLMs offer greater privacy and control, they generally do not match the raw performance and advanced reasoning capabilities of proprietary models by LLM providers mentioned in [Set up the AI Assistant](/solutions/observability/observability-ai-assistant.md#obs-ai-set-up).
::::

## Air-gapped environments

Local LLMs in air-gapped environments have specific installation and configuration instructions for deploying ELSER and configuring product documentation. Refer to the following links for more information:

- [Deploy ELSER in an air-gapped environment](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md#air-gapped-install)
- [Configure product documentation for air-gapped-environments](kibana://reference/configuration-reference/ai-assistant-settings.md#configuring-product-doc-for-airgap)