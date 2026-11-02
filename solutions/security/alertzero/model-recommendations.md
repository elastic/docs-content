---
description: "Choose the AI models that AlertZero uses in a space."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Choose AI models for {{alertzero}} [alertzero-model-recommendations]

Choose the AI models that {{alertzero}} uses in a space.

% PLACEHOLDER. Keep this page hidden in solutions/toc.yml until engineering settles how to choose AlertZero models.
% Once it has content, link here from the AI model sentence in Set up AlertZero (Start the Workers) and from the Models setting on each Worker page. The Worker pages in elastic/docs-content#9118 already have comments that wait for this page.
% For the steps to pick a model, link to explore-analyze/ai-features/manage-access-to-ai-assistant.md#feature-settings instead of repeating them. For what each row means, link to the glossary entries, such as glossary.md#alertzero-glossary-efficient-models.
%
% What Kibana 9.6 and decision D49 in elastic/project-alertzero say (checked 2026-11-01):
% - Models are chosen by kind of call, once per space, in Feature Settings. The navigation label is "Feature Settings", and the page heading and the Worker card link say "Feature settings".
% - Workers have no model setting of their own. A per-Worker override is post-MVP.
% - The AlertZero group has four rows, all technical preview, and they don't fall back to the cluster-wide default model. Source is x-pack/solutions/security/plugins/alertzero/server/inference_features.ts.
%   - Efficient models are for quick, lightweight calls that run often. Kibana suggests Claude Haiku 4.5, Gemini 3.5 Flash Lite, and GPT-5.6 Luna.
%   - Balanced models are for calls where accuracy matters but that run often or loop over many tool steps. Kibana suggests Claude Sonnet 5, GPT-5.6 Terra, and Gemini 3.6 Flash.
%   - Frontier models are for single-pass work where output quality matters most. Kibana suggests Claude Opus 5, GPT-5.6 Sol, and Claude Sonnet 5.
%   - Cyber domain models is optional and holds OpenAI Daybreak models, which need prompt templates. A model saved there replaces the tier model for Attack Discovery, alert triage, the false-positive judge, and the Hunt Watch.
%
% Still open:
% - Which tier alert triage uses. The Balanced models description says it covers triaging alerts, but the AlertZero prompt-template README says alert triage uses Efficient models.
% - James's review of the model list and how the tiers map to Workers, still owed as of the Sep 22 engineering weekly.
% - D49 in the project repo still uses the old tier names (Fast, Reasoning, Agentic). Use the names Kibana 9.6 ships.
