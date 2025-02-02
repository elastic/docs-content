# Connect to Amazon Bedrock [assistant-connect-to-bedrock]

This page provides step-by-step instructions for setting up an Amazon Bedrock connector for the first time. This connector type enables you to leverage large language models (LLMs) within {{kib}}. You’ll first need to configure AWS, then configure the connector in {{kib}}.

::::{note}
Only Amazon Bedrock’s `Anthropic` models are supported: `Claude` and `Claude instant`.
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

The following video demonstrates these steps.

::::{admonition}
<script type="text/javascript" async src="https://play.vidyard.com/embed/v4.js"></script>
<img
  style="width: 100%; margin: auto; display: block;"
  class="vidyard-player-embed"
  src="https://play.vidyard.com/ek6NpHaj6u4keZyEjPWXcT.jpg"
  data-uuid="ek6NpHaj6u4keZyEjPWXcT"
  data-v="4"
  data-type="inline"
/>
</br>
::::



### Configure an IAM User [_configure_an_iam_user]

Next, assign the policy you just created to a new user:

1. Return to the **IAM** menu. Select **Users** from the navigation menu, then click **Create User**.
2. Name the user, then click **Next**.
3. Select **Attach policies directly**.
4. In the **Permissions policies** field, search for the policy you created earlier, select it, and click **Next**.
5. Review the configuration then click **Create user**.

The following video demonstrates these steps.

::::{admonition}
<script type="text/javascript" async src="https://play.vidyard.com/embed/v4.js"></script>
<img
  style="width: 100%; margin: auto; display: block;"
  class="vidyard-player-embed"
  src="https://play.vidyard.com/5BQb2P818SMddRo6gA79hd.jpg"
  data-uuid="5BQb2P818SMddRo6gA79hd"
  data-v="4"
  data-type="inline"
/>
</br>
::::



### Create an access key [_create_an_access_key]

Create the access keys that will authenticate your Elastic connector:

1. Return to the **IAM** menu. Select **Users** from the navigation menu.
2. Search for the user you just created, and click its name.
3. Go to the **Security credentials** tab.
4. Under **Access keys**, click **Create access key**.
5. Select **Third-party service**, check the box under **Confirmation***, click ***Next**, then click **Create access key**.
6. Click **Download .csv file** to download the key. Store it securely.

The following video demonstrates these steps.

::::{admonition}
<script type="text/javascript" async src="https://play.vidyard.com/embed/v4.js"></script>
<img
  style="width: 100%; margin: auto; display: block;"
  class="vidyard-player-embed"
  src="https://play.vidyard.com/8oXgP1fbaQCqjWUgncF9at.jpg"
  data-uuid="8oXgP1fbaQCqjWUgncF9at"
  data-v="4"
  data-type="inline"
/>
</br>
::::



### Enable model access [_enable_model_access]

Make sure the supported Amazon Bedrock LLMs are enabled:

1. Search the AWS console for Amazon Bedrock.
2. From the Amazon Bedrock page, click **Get started**.
3. Select **Model access** from the left navigation menu, then click **Manage model access**.
4. Check the boxes for **Claude** and/or **Claude Instant**, depending which model or models you plan to use.
5. Click **Save changes**.

The following video demonstrates these steps.

::::{admonition}
<script type="text/javascript" async src="https://play.vidyard.com/embed/v4.js"></script>
<img
  style="width: 100%; margin: auto; display: block;"
  class="vidyard-player-embed"
  src="https://play.vidyard.com/Z7zpHq4N9uvUxegBUMbXDj.jpg"
  data-uuid="Z7zpHq4N9uvUxegBUMbXDj"
  data-v="4"
  data-type="inline"
/>
</br>
::::



## Configure the Amazon Bedrock connector [_configure_the_amazon_bedrock_connector]

Finally, configure the connector in {{kib}}:

1. Log in to {{kib}}.
2. . Find the **Connectors** page in the navigation menu or use the [global search field](../../../get-started/the-stack.md#kibana-navigation-search). Then click **Create Connector**, and select **Amazon Bedrock**.
3. Name your connector.
4. (Optional) Configure the Amazon Bedrock connector to use a different AWS region where Anthropic models are supported by editing the **URL** field, for example by changing `us-east-1` to `eu-central-1`.
5. (Optional) Add one of the following strings if you want to use a model other than the default:

    1. For Haiku: `anthropic.claude-3-haiku-20240307-v1:0`
    2. For Sonnet: `anthropic.claude-3-sonnet-20240229-v1:0`
    3. For Opus: `anthropic.claude-3-opus-20240229-v1:0`

6. Enter the **Access Key** and **Secret** that you generated earlier, then click **Save**.

    Your LLM connector is now configured. For more information on using Elastic AI Assistant, refer to [AI Assistant](../../../solutions/security/ai/ai-assistant.md).


::::{important}
If you’re using [provisioned throughput](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.md), your ARN becomes the model ID, and the connector settings **URL** value must be [encoded](https://www.urlencoder.org/) to work. For example, if the non-encoded ARN is `arn:aws:bedrock:us-east-2:123456789102:provisioned-model/3Ztr7hbzmkrqy1`, the encoded ARN would be `arn%3Aaws%3Abedrock%3Aus-east-2%3A123456789102%3Aprovisioned-model%2F3Ztr7hbzmkrqy1`.
::::


The following video demonstrates these steps.

::::{admonition}
<script type="text/javascript" async src="https://play.vidyard.com/embed/v4.js"></script>
<img
  style="width: 100%; margin: auto; display: block;"
  class="vidyard-player-embed"
  src="https://play.vidyard.com/QJe4RcTJbp6S6m9CkReEXs.jpg"
  data-uuid="QJe4RcTJbp6S6m9CkReEXs"
  data-v="4"
  data-type="inline"
/>
</br>
::::
