---
navigation_title: EIS for self-managed clusters
applies_to:
  stack: ga 9.3
  deployment:
    self: ga
    ece: ga
    eck: ga
---

# EIS for self-managed clusters

Elastic {{infer-cap}} Service (EIS) for self-managed clusters is available through [Cloud Connect](/deploy-manage/cloud-connect.md), which enables you to use {{ecloud}} services in your self-managed cluster without having to install and maintain their infrastructure yourself. This allows you to use AI-powered features like [AI Assistant](/explore-analyze/ai-features/ai-chat-experiences/ai-assistant.md), [Search Playground](/explore-analyze/query-filter/tools/playground.md) and [semantic search](/solutions/search/semantic-search/semantic-search-semantic-text.md#semantic-text-index-mapping) without deploying and managing {{ml}} nodes.

## Prerequisites

Before you can use EIS with your self-managed cluster, ensure you meet the following requirements:

* Your cluster is running {{es}} 9.3 or later
* Your self-managed cluster is on an [Enterprise self-managed license](https://www.elastic.co/subscriptions) or an [active self-managed trial](https://cloud.elastic.co/registration)
* You have an {{ecloud}} account with either an [active Cloud Trial](https://cloud.elastic.co/registration) or [billing information configured](/deploy-manage/cloud-organization/billing/add-billing-details.md)

## Set up EIS with Cloud Connect

To set up EIS for your self-managed cluster with Cloud Connect:

::::::{stepper}
:::::{step} Open Cloud Connect
In your self-managed cluster, navigate to the **Cloud Connect** page using the [search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/cloud-connect-eis.png
:screenshot:
:alt: Screenshot showing Cloud Connect page
:::

:::::

:::::{step} Get your Cloud Connect API key
Sign up or log in to {{ecloud}} and get the Cloud Connect API key:

- If you already have an {{ecloud}} account, click **Log in**.
- If you don’t have an account yet, click **Sign up** and follow the prompts to create your account and start a free trial.
:::::

:::::{step} Connect EIS
Copy the Cloud Connect API key, paste it into your self-managed cluster's Cloud Connect page, then click **Connect**.

:::::

:::::{step} Enable Elastic Inference Service
On the **Cloud connected services** page, click **Connect** for Elastic {{infer}} Service.

:::{image} /explore-analyze/images/eis-cloud-connect-connect-ui.png
:screenshot:
:alt: Screenshot showing Cloud Connect and EIS 
:::

:::::

:::::{step} Verify with a chat request
In **{{dev-tools-app}}**, run this chat request to confirm EIS is responding:

```console
POST _inference/chat_completion/.rainbow-sprinkles-elastic/_stream
{
  "messages": [
    {
      "role": "user",
      "content": "In only two digits and nothing else, what is the meaning of life?" <1>
    }
  ]
}
```
% TEST[skip]
1. A user message to drive the chat completion stream.

The response should look like this:

```text
event: message <1>
data: {
  "id" : "unified-1a499203-a497-4ba5-a292-d9cfa15d32bb",
  "choices" : [
    {
      "delta" : {
        "role" : "assistant"
      },
      "index" : 0
    }
  ],
  "model" : "rainbow-sprinkles",
  "object" : "chat.completion.chunk"
}


event: message <2>
data: {
  "id" : "unified-1a499203-a497-4ba5-a292-d9cfa15d32bb",
  "choices" : [
    {
      "delta" : {
        "content" : "42"
      },
      "index" : 0
    }
  ],
  "model" : "rainbow-sprinkles",
  "object" : "chat.completion.chunk"
}


event: message <3>
data: {
  "id" : "unified-1a499203-a497-4ba5-a292-d9cfa15d32bb",
  "choices" : [
    {
      "delta" : { },
      "finish_reason" : "stop",
      "index" : 0
    }
  ],
  "model" : "rainbow-sprinkles",
  "object" : "chat.completion.chunk"
}


event: message <4>
data: {
  "id" : "unified-1a499203-a497-4ba5-a292-d9cfa15d32bb",
  "choices" : [
    {
      "delta" : { },
      "index" : 0
    }
  ],
  "model" : "rainbow-sprinkles",
  "object" : "chat.completion.chunk",
  "usage" : {
    "completion_tokens" : 5,
    "prompt_tokens" : 22,
    "total_tokens" : 27
  }
}
```
1. The first event opens the stream and sets the assistant role.
2. The next event streams the content (`"42"`).
3. The third event signals completion with `finish_reason: "stop"`.
4. The final event includes token usage details.
:::::
::::::



## Regions and billing

For information about EIS regions and request routing, refer to the [Region and hosting](/explore-analyze/elastic-inference/eis.md#eis-regions). 

:::{note}
You may encounter different {{infer}} service URLs that appear to be region- or cloud-specific, such as `https://inference.europe-west3.gcp.svc.elastic.cloud`. These URLs are used for request routing within {{ecloud}}. Regardless of which {{infer}} service URL is configured, all EIS requests are ultimately routed to {{aws}} `us-east-1`.
:::


EIS is billed per million tokens. For details on pricing and usage tracking, refer to [Pricing](/explore-analyze/elastic-inference/eis.md#pricing) and [Monitor your token usage](/explore-analyze/elastic-inference/eis.md#monitor-your-token-usage).

