You can use your locally installed LLM with the {{infer}} API.

Create the {{infer}} endpoint for a `chat_completion` task type with the `openai` service with the following request:

```console
PUT _inference/chat_completion/llama-completion
{
    "service": "openai",
    "service_settings": {
        "api_key": "ignored", <1>
        "model_id": "llama3.2", <2>
        "url": "https://your-ngrok-endpoint.ngrok-free.app/v1/chat/completions" <3>
    }
}
```

1. The `api_key` parameter is required for the `openai` service and must be set, but the specific value is not important for the local AI service.
2. The model name.
3. The ngrok-generated URL with the chat completion endpoint (`v1/chat/completions`).

Verify if the {{infer}} endpoint working correctly:

```console
POST _inference/chat_completion/llama-completion/_stream
{
    "model": "llama3.2",
    "messages": [
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    "temperature": 0.7,
    "max_completion_tokens": 300
}
```

The request results in a response similar to this:

```console-result
event: message
data: {
  "id" : "chatcmpl-416",
  "choices" : [
    {
      "delta" : {
        "content" : "The",
        "role" : "assistant"
      },
      "index" : 0
    }
  ],
  "model" : "llama3.2",
  "object" : "chat.completion.chunk"
}
(...)
```
