# AI Assistant Knowledge Base [ai-assistant-knowledge-base]

AI Assistant’s Knowledge Base feature enables AI Assistant to recall specific documents and other specified information. This information, which can include everything from the location of your datacenters to the latest threat research, provides additional context that can improve the quality of AI Assistant’s responses to your queries. This topic describes how to enable and add information to Knowledge Base.

::::{note}
When you upgrade from {{elastic-sec}} version 8.15 to a newer version, information previously stored by AI Assistant will be lost.
::::


::::{admonition} Requirements
* To use Knowledge Base, you need the `Elastic AI Assistant: All` privilege. To edit global Knowledge Base entries (information that will affect the AI Assistant experience for other users in the {{kib}} space), you need the `Allow Changes to Global Entries` privilege.
* You must [enable machine learning](../../../solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md) with a minimum ML node size of 4 GB.

::::



## Role-based access control (RBAC) for Knowledge Base [knowledge-base-rbac]

The `Elastic AI Assistant: All` role privilege allows you to use AI Assistant and access its settings. It has two sub-privileges, `Field Selection and Anonymization`, which allows you to customize which alert fields are sent to AI Assistant and Attack Discovery, and Knowledge Base, which allows you to edit and create new Knowledge Base entries.

:::{image} ../../../images/serverless-knowledge-base-rbac.png
:alt: Knowledge Base's RBAC settings
:::


## Enable Knowledge Base [enable-knowledge-base]

There are two ways to enable Knowledge Base.

::::{note}
You must individually enable Knowledge Base for each {{kib}} space where you want to use it.
::::



### Option 1: Enable Knowledge Base from an AI Assistant conversation [_option_1_enable_knowledge_base_from_an_ai_assistant_conversation]

Open a conversation with AI Assistant, select a large language model, then click **Setup Knowledge Base**. If the button doesn’t appear, Knowledge Base is already enabled.

:::{image} ../../../images/serverless-knowledge-base-assistant-setup-button.png
:alt: An AI Assistant conversation showing the Setup Knowledge Base button
:::

Knowledge Base setup may take several minutes. It will continue in the background if you close the conversation. After setup is complete, you can access Knowledge Base settings from AI Assistant’s conversation settings menu (access the conversation settings menu by clicking the three dots button next to the model selection dropdown).

:::{image} ../../../images/serverless-knowledge-base-assistant-menu-dropdown.png
:alt: AI Assistant's dropdown menu with the Knowledge Base option highlighted
:::


### Option 2: Enable Knowledge Base from the Security AI settings [_option_2_enable_knowledge_base_from_the_security_ai_settings]

1. To open Security AI settings, use the [global search field](../../../get-started/the-stack.md#kibana-navigation-search) to find "AI Assistant for Security."
2. On the **Knowledge Base** tab, click **Setup Knowledge Base**. If the button doesn’t appear, Knowledge Base is already enabled.

:::{image} ../../../images/serverless-knowledge-base-assistant-settings-kb-tab.png
:alt: AI Assistant's settings menu open to the Knowledge Base tab
:::


## Knowledge Base for alerts [rag-for-alerts]

When Knowledge Base is enabled, AI Assistant receives `open` or `acknowledged` alerts from your environment from the last 24 hours. It uses these as context for each of your prompts. This enables it to answer questions about multiple alerts in your environment rather than just about individual alerts you choose to send it. It receives alerts ordered by risk score, then by the most recently generated. Building block alerts are excluded.

To enable Knowledge Base for alerts:

1. Ensure that Knowledge Base is [enabled](../../../solutions/security/ai/ai-assistant-knowledge-base.md#enable-knowledge-base).
2. Use the slider on the Security AI settings' **Knowledge Base** tab to select the number of alerts to send to AI Assistant. Click **Save**.

::::{note}
Including a large number of alerts may cause your request to exceed the maximum token length of your third-party generative AI provider. If this happens, try selecting a lower number of alerts to send.
::::



## Add knowledge [knowledge-base-add-knowledge]

To view all Knowledge Base entries, go to the Security AI settings and select the **Knowledge Base** tab. You can add individual documents or entire indices containing multiple documents. Each entry in the Knowledge Base (a document or index) has a **Sharing** setting of `private` or `global`. Private entries apply to the current user only and do not affect other users in the {{kib}} space, whereas global entries affect all users. Each entry can also have a `Required knowledge` setting, which means it will be included as context for every message sent to AI Assistant.

::::{note}
When you enable Knowledge Base, it comes pre-populated with articles from [Elastic Security Labs](https://www.elastic.co/security-labs), current through September 30, 2024, which allows AI Assistant to leverage Elastic’s security research during your conversations. This enables it to answer questions such as, “Are there any new tactics used against Windows hosts that I should be aware of when investigating my alerts?”
::::



### Add an individual document [knowledge-base-add-knowledge-document]

Add an individual document to Knowledge Base when you want AI Assistant to remember a specific piece of information.

1. To open Security AI settings, use the [global search field](../../../get-started/the-stack.md#kibana-navigation-search) to find "AI Assistant for Security." Select the **Knowledge Base** tab.
2. Click **New → Document** and give it a name.
3. Under **Sharing**, select whether this knowledge should be **Global** or **Private**.
4. Write the knowledge AI Assistant should remember in the **Markdown text** field.
5. In the **Markdown text** field, enter the information you want AI Assistant to remember.
6. If it should be **Required knowledge**, select the option. Otherwise, leave it blank. Alternatively, you can simply send a message to AI Assistant that instructs it to "Remember" the information. For example, "Remember that I changed my password today, October 24, 2024", or "Remember we always use the Threat Hunting Timeline template when investigating potential threats". Entries created in this way are private to you. By default, they are not required knowledge, but you can make them required by instructing AI Assistant to "Always remember", for example "Always remember to address me as madam", or "Always remember that our primary data center is located in Austin, Texas".

Refer to the following video for an example of adding a document to Knowledge Base from the settings menu.

::::{admonition}
<script type="text/javascript" async src="https://play.vidyard.com/embed/v4.js"></script>
<img
  style="width: 100%; margin: auto; display: block;"
  class="vidyard-player-embed"
  src="https://play.vidyard.com/rQsTujEfikpx3vv1vrbfde.jpg"
  data-uuid="rQsTujEfikpx3vv1vrbfde"
  data-v="4"
  data-type="inline"
/>
</br>
::::



### Add an index [knowledge-base-add-knowledge-index]

Add an index as a knowledge source when you want new information added to that index to automatically inform AI Assistant’s responses. Common security examples include asset inventories, network configuration information, on-call matrices, threat intelligence reports, and vulnerability scans.

::::{important}
Indices added to Knowledge Base must have at least one field mapped as [semantic text](https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-text.html).
::::


1. To open Security AI settings, use the [global search field](../../../get-started/the-stack.md#kibana-navigation-search) to find "AI Assistant for Security." Select the **Knowledge Base** tab.
2. Click **New → Index**.
3. Name the knowledge source.
4. Under **Sharing**, select whether this knowledge should be **Global** or **Private**.
5. Under **Index**, enter the name of the index you want to use as a knowledge source.
6. Under **Field**, enter the names of one or more semantic text fields within the index.
7. Under **Data Description**, describe when this information should be used by AI Assistant.
8. Under **Query Instruction**, describe how AI Assistant should query this index to retrieve relevant information.
9. Under **Output Fields**, list the fields which should be sent to AI Assistant. If none are listed, all fields will be sent.

:::{image} ../../../images/serverless-knowledge-base-add-index-config.png
:alt: Knowledge base's Edit index entry menu
:::

Refer to the following video for an example of adding an index to Knowledge Base.

::::{admonition}
<script type="text/javascript" async src="https://play.vidyard.com/embed/v4.js"></script>
<img
  style="width: 100%; margin: auto; display: block;"
  class="vidyard-player-embed"
  src="https://play.vidyard.com/Q5CjXMN4R2GYLGLUy5P177.jpg"
  data-uuid="Q5CjXMN4R2GYLGLUy5P177"
  data-v="4"
  data-type="inline"
/>
</br>
::::
