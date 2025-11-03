Create a connector using the public URL from ngrok.

1. In Kibana, go to **Playground** from the left navigation menu, and select the {icon}`wrench` button in the **Large Language Model (LLM)** tile to connect an LLM.
2. Select **OpenAI** on the fly-out.
3. Provide a name for the connector.
4. Under **Connector settings**, select **Other (OpenAI Compatible Service)** as the OpenAI provider.
5. Paste the ngrok-generated URL into the **URL** field and add the `v1/chat/completions` endpoint. For example: https://your-ngrok-endpoint.ngrok-free.app/v1/chat/completions
6. Specify the default model, for example, `llama3.2`.
7. Provide any random string for the API key (it will not be used for requests).
8. **Save**.
   :::{image} /solutions/images/elasticsearch-openai-compatible-connector.png
   :alt: Configuring an LLM connector in Playground
   :screenshot:
   :::
9. Click **Add data sources** and connect your index.

You can now use Playground with the LLM running locally.
