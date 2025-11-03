---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/assistant-connect-to-bedrock.html
  - https://www.elastic.co/guide/en/serverless/current/security-connect-to-bedrock.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Connect to Amazon Bedrock

This page provides step-by-step instructions for setting up an Amazon Bedrock connector for the first time. This connector type enables you to leverage large language models (LLMs) within {{kib}}. You’ll first need to configure AWS, then configure the connector in {{kib}}.

::::{note}
All models in Amazon Bedrock's `Claude` model group are supported.
::::



## Configure AWS [_configure_aws]


### Configure an IAM policy [_configure_an_iam_policy]

First, configure an IAM policy with the necessary permissions:

1. Log into the AWS console and search for Identity and Access Management (IAM).
2. From the **IAM** menu, select **Policies** → **Create policy**.
3. To provide the necessary permissions, paste the following JSON into the **Specify permissions** menu.

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream"
                ],
                "Resource": "*"
            }
        ]
    }
    ```

    ::::{note}
    These are the minimum required permissions. IAM policies with additional permissions are also supported.
    ::::

4. Click **Next**. Name your policy.

The following video demonstrates these steps (click to watch).

[![azure-openai-configure-model-video](https://play.vidyard.com/ek6NpHaj6u4keZyEjPWXcT.jpg)](https://videos.elastic.co/watch/ek6NpHaj6u4keZyEjPWXcT?)



### Configure an IAM User [_configure_an_iam_user]

Next, assign the policy you just created to a new user:

1. Return to the **IAM** menu. Select **Users** from the navigation menu, then click **Create User**.
2. Name the user, then click **Next**.
3. Select **Attach policies directly**.
4. In the **Permissions policies** field, search for the policy you created earlier, select it, and click **Next**.
5. Review the configuration then click **Create user**.

The following video demonstrates these steps (click to watch).

[![bedrock-iam-video](https://play.vidyard.com/5BQb2P818SMddRo6gA79hd.jpg)](https://videos.elastic.co/watch/5BQb2P818SMddRo6gA79hd?)



### Create an access key [_create_an_access_key]

Create the access keys that will authenticate your Elastic connector:

1. Return to the **IAM** menu. Select **Users** from the navigation menu.
2. Search for the user you just created, and click its name.
3. Go to the **Security credentials** tab.
4. Under **Access keys**, click **Create access key**.
5. Select **Third-party service**, check the box under **Confirmation**, click **Next**, then click **Create access key**.
6. Click **Download .csv file** to download the key. Store it securely.

The following video demonstrates these steps (click to watch).

[![bedrock-accesskey-video](https://play.vidyard.com/8oXgP1fbaQCqjWUgncF9at.jpg)](https://videos.elastic.co/watch/8oXgP1fbaQCqjWUgncF9at?)



## Configure the Amazon Bedrock connector [_configure_the_amazon_bedrock_connector]

Finally, configure the connector in {{kib}}:

1. Log in to {{kib}}.
2. Find the **Connectors** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Then click **Create Connector**, and select **Amazon Bedrock**.
3. Name your connector.
4. (Optional) Configure the Amazon Bedrock connector to use a different AWS region where Anthropic models are supported by editing the **URL** field, for example by changing `us-east-1` to `eu-central-1`.
5. (Optional) Add one of the following strings if you want to use a model other than the default. Note that these URLs should have a prefix of `us.` or `eu.`, depending on your region, for example `us.anthropic.claude-3-5-sonnet-20240620-v1:0` or `eu.anthropic.claude-3-5-sonnet-20240620-v1:0`.

    * Sonnet 3.5: `us.anthropic.claude-3-5-sonnet-20240620-v1:0` or `eu.anthropic.claude-3-5-sonnet-20240620-v1:0`
    * Sonnet 3.5 v2: `us.anthropic.claude-3-5-sonnet-20241022-v2:0` or `eu.anthropic.claude-3-5-sonnet-20241022-v2:0`
    * Sonnet 3.7: `us.anthropic.claude-3-7-sonnet-20250219-v1:0` or `eu.anthropic.claude-3-7-sonnet-20250219-v1:0`
    * Haiku 3.5: `us.anthropic.claude-3-5-haiku-20241022-v1:0` or `eu.anthropic.claude-3-5-haiku-20241022-v1:0`
    * Opus: `us.anthropic.claude-3-opus-20240229-v1:0` or `eu.anthropic.claude-3-opus-20240229-v1:0`

6. Enter the **Access Key** and **Secret** that you generated earlier, then click **Save**.

    Your LLM connector is now configured. For more information on using Elastic AI Assistant, refer to [AI Assistant](/solutions/security/ai/ai-assistant.md).


::::{important}
If you’re using [provisioned throughput](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html), your ARN becomes the model ID, and the connector settings **URL** value must be [encoded](https://www.urlencoder.org/) to work. For example, if the non-encoded ARN is `arn:aws:bedrock:us-east-2:123456789102:provisioned-model/3Ztr7hbzmkrqy1`, the encoded ARN would be `arn%3Aaws%3Abedrock%3Aus-east-2%3A123456789102%3Aprovisioned-model%2F3Ztr7hbzmkrqy1`.
::::


The following video demonstrates these steps (click to watch).

[![bedrock-configure-model-video](https://play.vidyard.com/QJe4RcTJbp6S6m9CkReEXs.jpg)](https://videos.elastic.co/watch/QJe4RcTJbp6S6m9CkReEXs?)
