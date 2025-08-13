---
navigation_title: Connect to a local LLM
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/connect-to-local-llm.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---

# Connect to your own local LLM

This page provides instructions for setting up a connector to a large language model (LLM) of your choice using LM Studio. This allows you to use your chosen model within the {{obs-ai-assistant}}. You’ll first need to set up LM Studio, then download and deploy a model via LM studio and finally configure the connector in your Elastic deployment.

::::{note}
You do not have to set up a proxy if LM studio is configured on the same network as your Elastic deployment or locally on your machine. 

If your Elastic deployment is not on the same network, you would need to configure a reverse proxy using Nginx to authenticate with Elastic. Refer [Configure your reverse proxy](https://www.elastic.co/docs/solutions/security/ai/connect-to-own-local-llm#_configure_your_reverse_proxy) for more detailed instructions.
::::

This example uses a server hosted in GCP to configure LM Studio with the [Mistral-Nemo-Instruct-2407](https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407) model.

### Already running LM Studio? [skip-if-already-running]

If LM Studio is already installed, the server is running, and you have a model loaded (with a context window of at least 64K tokens), you can skip directly to [Configure the connector in your Elastic deployment](#configure-the-connector-in-your-elastic-deployment).

## Configure LM Studio and download a model [configure-lm-studio-and-download-a-model]

LM Studio supports the OpenAI SDK, which makes it compatible with Elastic’s OpenAI connector, allowing you to connect to any model available in the LM Studio marketplace.

As the first step, install [LM Studio](https://lmstudio.ai/).

You must launch the application using its GUI before being able to use the CLI.

::::{note}
For local/on‑prem desktop: Launch LM studio directly.
For GCP, Chrome RDP with an [X Window System](https://cloud.google.com/architecture/chrome-desktop-remote-on-compute-engine) can be used for this purpose.
For other cloud platforms: Any secure remote desktop (RDP, VNC over SSH tunnel, or X11 forwarding) works as long as you can open the LM Studio GUI once.
::::

After you’ve opened the application for the first time using the GUI, you can start the server by using `sudo lms server start` in the [CLI](https://lmstudio.ai/docs/cli/server-start).

Once you’ve launched LM Studio:

1. Go to LM Studio’s Discover window.
2. Search for an LLM (for example, `Mistral-Nemo-Instruct-2407`). Your chosen model must include `instruct` in its name in order to work with Elastic.
3. When selecting a model, models published by verified authors are recommended (indicated by the purple verification badge next to the model name).
4. After you find a model, view download options and select a recommended option (green). For best performance, select one with the thumbs-up icon that indicates good performance on your hardware.
5. Download one or more models.

::::{important}
For security reasons, before downloading a model, verify that it is from a trusted source or by a verified author. It can be helpful to review community feedback on the model (for example using a site like Hugging Face).
::::

:::{image} /solutions/images/observability-ai-assistant-lms-model-selection.png
:alt: The LM Studio model selection interface with download options
:::

This [`mistralai/mistral-nemo-instruct-2407`](https://lmstudio.ai/models/mistralai/mistral-nemo-instruct-2407) model used in this example has 12B total parameters, a 128,000 token context window, and uses GGUF [quanitization](https://huggingface.co/docs/transformers/main/en/quantization/overview). For more information about model names and format information, refer to the following table.

| Model Name | Parameter Size | Tokens/Context Window | Quantization Format |
| --- | --- | --- | --- |
| Name of model, sometimes with a version number. | LLMs are often compared by their number of parameters — higher numbers mean more powerful models. | Tokens are small chunks of input information. Tokens do not necessarily correspond to characters. You can use [Tokenizer](https://platform.openai.com/tokenizer) to see how many tokens a given prompt might contain. | Quantization reduces overall parameters and helps the model to run faster, but reduces accuracy. |
| Examples: Llama, Mistral. | The number of parameters is a measure of the size and the complexity of the model. The more parameters a model has, the more data it can process, learn from, generate, and predict. | The context window defines how much information the model can process at once. If the number of input tokens exceeds this limit, input gets truncated. | Specific formats for quantization vary, most models now support GPU rather than CPU offloading. |

::::{important}
The {{obs-ai-assistant}} requires a model with at least 64,000 token context window.
::::

## Load a model in LM Studio [load-a-model-in-lm-studio]

After downloading a model, load it in LM Studio using the GUI or LM Studio’s [CLI tool](https://lmstudio.ai/docs/cli/load).

### Option 1: Load a model using the CLI (Recommended) [option-1-load-a-model-using-the-cli-recommended]

Once you’ve downloaded a model, use the following commands in your CLI:

1. Verify LM Studio is installed: `lms`
2. Check LM Studio’s status: `lms status`
3. List all downloaded models: `lms ls`
4. Load a model: `lms load mistralai/mistral-nemo-instruct-2407 --context-length 64000`.

::::{important}
When loading a model, use the `--context-length` flag with a context window of 64,000 or higher. 
Optionally, you can set how much to offload to the GPU by using the `--gpu` flag. `--gpu max` will offload all layers to GPU.
::::

:::{image} /solutions/images/observability-ai-assistant-lms-commands.png
:alt: The CLI interface during execution of initial LM Studio commands
:::

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

Once the model is downloaded, it will appear in the "My Models" window in LM Studio.

:::{image} /solutions/images/observability-ai-assistant-lm-studio-my-models.png
:alt: My Models window in LM Studio with downloaded models
:::

1. Navigate to the Developer window.
2. Click on the "Start server" toggle on the top left. Once the server is started, you'll see the address and port of the server. The port will be defaulted to 1234.
3. Click on "Select a model to load" and pick the model `Mistral Nemo Instruct 2407` from the dropdown menu.
4. Navigate to the "Load" on the right side of the LM Studio window, to adjust the context window to 64,000. Reload the model to apply the changes.

::::{note}
To enable other devices in the same network access the server, turn on "Serve on Local Network" via Settings.
::::

:::{image} /solutions/images/obs-ai-assistant-lm-studio-load-model-gui.png
:alt: Loading a model in LM studio developer tab
:::

## Configure the connector in your Elastic deployment [configure-the-connector-in-your-elastic-deployment]

Finally, configure the connector:

1. Log in to your Elastic deployment.
2. Find the **Connectors** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Then click **Create Connector**, and select **OpenAI**. The OpenAI connector is compatible for this use case because LM Studio uses the OpenAI SDK.
3. Name your connector to help keep track of the model version you are using.
4. Under **Select an OpenAI provider**, select **Other (OpenAI Compatible Service)**.
5. Under **URL**, enter the host's IP address and port, followed by `/v1/chat/completions`. (If you have a reverse proxy set up, enter the domain name specified in your Nginx configuration file followed by `/v1/chat/completions`.)
6. Under **Default model**, enter `mistralai/mistral-nemo-instruct-2407`.
7. Under **API key**, fill in anything. (If you have a reverse proxy set up, enter the secret token specified in your Nginx configuration file.)
8. Click **Save**.

:::{image} /solutions/images/obs-ai-assistant-local-llm-connector-setup.png
:alt: The OpenAI create connector flyout
:::

Setup is now complete. You can use the model you’ve loaded in LM Studio to power Elastic’s generative AI features.

::::{note}
While local (open-weight) LLMs offer greater privacy and control, they generally do not match the raw performance and advanced reasoning capabilities of proprietary models by LLM providers mentioned in [here](/solutions/observability/observability-ai-assistant.md)
::::
