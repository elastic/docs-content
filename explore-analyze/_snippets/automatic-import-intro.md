% Shared intro body for Automatic Import: canonical page and solution stub pages. 

Automatic Import parses, ingests, and maps data to [ECS](https://www.elastic.co/elasticsearch/common-schema) for sources that don’t yet have prebuilt Elastic integrations. It works with {{elastic-sec}}, {{observability}}, and other solutions that rely on {{agent}} and integrations. This lets you onboard custom or niche data sources without building a full integration manually.

Automatic Import uses a large language model (LLM) with specialized instructions to analyze source data and generate a custom integration.

Elastic integrations, including those created by Automatic Import, normalize data to [the Elastic Common Schema (ECS)](ecs://reference/index.md). This standardization provides consistent use across dashboards, search, alerts, and machine learning features.

Refer to [prebuilt data integrations](https://docs.elastic.co/en/integrations) for a full list of Elastic’s 400+ integrations.
