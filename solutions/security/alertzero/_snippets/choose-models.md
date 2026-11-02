{{alertzero}} has its own section in [**Feature Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md), with a row for each kind of model call its {{az-workers}} make: **{{az-efficient-models}}**, **{{az-balanced-models}}**, and **{{az-frontier-models}}**. Each row starts with its own recommended models instead of the default model, and the {{az-workers}} use the first available model in the row's list.

For the best balance of quality and cost on **{{az-frontier-models}}**, choose a model other than Claude Opus 5, such as GPT-5.6 Sol. Claude Opus 5 uses many more tokens for {{az-frontier-models}} calls, such as generating attack discoveries, so it costs more to run. To choose a different model for a row:

1. In **Feature Settings**, find the row in the **{{alertzero}}** section.
2. Select **Add a model** and choose the model you want.
3. Drag the model to the top of the list, or remove the models above it.
4. Select **Save settings**.

To make the {{az-workers}} use only the default model, turn off feature-specific assigned models.
