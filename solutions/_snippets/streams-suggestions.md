Streams groups the samples from the **Data preview** table into categories of similar messages. For each category, Streams generates suggestions by sending samples to the LLM. Suggestions are then shown in the UI.

:::{warning}
This can incur additional costs, depending on the LLM connector you are using. Typically a single iteration uses between 1000 and 5000 tokens depending on the number of identified categories and the length of the messages.
:::
