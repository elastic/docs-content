---
navigation_title: Query AI Indices with LangChain
description: Connect a LangChain agent to Context Engine through the Agent Builder MCP server or the Context Engine APIs, so it can retrieve Knowledge Indicators from your AI Indices.
applies_to:
  stack: preview 9.6
  serverless: preview
products:
  - id: kibana
---

# Query AI Indices from LangChain

:::{important}
This page is currently hidden from the documentation navigation. It is intended for testing and review while the feature is under development.
:::

A LangChain agent can retrieve Knowledge Indicators (KIs) from Context Engine using read-only tools.

You can connect a LangChain agent to Context Engine in two ways:

- Use the **[Agent Builder Model Context Protocol (MCP) server](/explore-analyze/ai-features/agent-builder/mcp-server.md)** to load the built-in Context Engine retrieval tools.
- Use the **Context Engine APIs** to wrap the available retrieval operations as LangChain tools in your application.

This guide covers both routes. Examples on this page use Python, but the same approach works in [LangChain.js](https://reference.langchain.com/javascript/langchain).

## Requirements

* An {{stack}} deployment with an Enterprise license, or an {{serverless-full}} project.
* The `contextEngine:enabled` advanced setting turned on in the space you want to query. This setting is per space, and the APIs return `404` in any space where it's off.
* At least one AI Index containing Knowledge Indicators (KIs). See [Create an AI Index](quickstart.md#2.-create-an-ai-index) if you don't have one yet.
* An API key whose privileges cover both Kibana and Elasticsearch. [Step 1](#step-1-create-credentials) walks through this.
* Python 3.10 or later, with `langchain` installed. The skill option in [Step 3](#step-3-create-the-agent) adds `deepagents`, which needs 3.11 or later.

## How retrieval works

Context Engine uses a discovery-first retrieval flow:

1. List the AI Indices available to the agent.
2. Describe the relevant AI Index to identify its query target, fields, and available Knowledge Indicators.
3. Query the AI Index using the information returned by the describe operation.

Describing the AI Index before querying it prevents the agent from guessing the query target or field names.

Both connection routes run the same three operations, against one Kibana space, as the owner of the API key. An agent only ever sees the AI Indices that key is allowed to read.

## Step 0: Connect to Context Engine

Choose a connection route.

::::{tab-set}
:group: ce-transport
:::{tab-item} MCP server
:sync: mcp

1. Create credentials with the Agent Builder, Context Engine, and Elasticsearch privileges required for MCP access.
2. Connect to the Agent Builder MCP endpoint.
3. Load the Context Engine tools.
:::
:::{tab-item} Context Engine APIs
:sync: api

1. Create credentials with the Context Engine and Elasticsearch privileges required for API access.
2. Configure the Context Engine API client.
3. Wrap the retrieval operations as LangChain tools.
:::
::::

## Step 1: Create credentials

Your credential needs privileges in both Kibana and Elasticsearch. The MCP route additionally needs Agent Builder **Read**, which is what makes the tools visible.

1. In Kibana, go to **Stack Management → API Keys** and click `Create API key` 
2. Leave **Control security privileges** off and define a role with the following privileges:

    ::::::{tab-set}
    :group: ce-transport
    :::::{tab-item} MCP server
    :sync: mcp

    * **Index privileges**: `read` and `view_index_metadata` on `ai-index-*`.
    * **Kibana privileges**, in the space you want to query: **Agent Builder** at **Read**, and **Context Engine** at **Read**.

    ::::{dropdown} Example of a concrete definition
    ```json
    {
      "contextEngineRole": {
        "cluster": [],
        "indices": [
          {
            "names": [
              "ai-index-*"
            ],
            "privileges": [
              "read",
              "view_index_metadata"
            ],
            "field_security": {
              "grant": [
                "*"
              ],
              "except": []
            },
            "allow_restricted_indices": false
          }
        ],
        "applications": [
          {
            "application": "kibana-.kibana",
            "privileges": [
              "feature_agentBuilder.read",
              "feature_contextEngine.read"
            ],
            "resources": [
              "*"
            ]
          }
        ],
        "run_as": [],
        "metadata": {},
        "transient_metadata": {
          "enabled": true
        }
      }
    }
    ```
    ::::
    :::::
    :::::{tab-item} API
    :sync: api

    * **Index privileges**: `read` and `view_index_metadata` on `ai-index-*`.
    * **Kibana privileges**, in the space you want to query: **Context Engine** at **Read**.

    ::::{dropdown} Example of a concrete definition
    ```json
    {
      "contextEngineRole": {
        "cluster": [],
        "indices": [
          {
            "names": [
              "ai-index-*"
            ],
            "privileges": [
              "read",
              "view_index_metadata"
            ],
            "field_security": {
              "grant": [
                "*"
              ],
              "except": []
            },
            "allow_restricted_indices": false
          }
        ],
        "applications": [
          {
            "application": "kibana-.kibana",
            "privileges": [
              "feature_contextEngine.read"
            ],
            "resources": [
              "*"
            ]
          }
        ],
        "run_as": [],
        "metadata": {},
        "transient_metadata": {
          "enabled": true
        }
      }
    }
    ```
    ::::
    :::::
    ::::::

3. Copy the `encoded` value and export it, along with your Kibana URL:

    ```shell
    export KIBANA_URL="https://my-deployment.kb.us-east-1.aws.elastic.cloud"
    export KIBANA_API_KEY="VnVhQ2ZHY0JDZGJrU..."
    ```

This example also uses an OpenRouter key to reach the model:

```shell
export OPENROUTER_API_KEY="sk-..."
```

## Step 2: Set up Context Engine tools

Choose how to make the retrieval tools available to LangChain:

::::{tab-set}
:group: ce-transport
:::{tab-item} MCP server
:sync: mcp
The MCP endpoint takes a single `Authorization` header. It's exempt from Kibana's XSRF check, so no `kbn-xsrf` header is needed.

```py
import os

from langchain_mcp_adapters.client import MultiServerMCPClient

CONTEXT_ENGINE_TOOLS = {   <1>
    "platform_context_engine_list_ai_indices",
    "platform_context_engine_describe_ai_index",
    "platform_context_engine_query_ai_indices",
}


async def main() -> None:
    kibana = os.environ["KIBANA_URL"].rstrip("/")
    space = os.environ.get("KIBANA_SPACE")   <2>
    base = f"{kibana}/s/{space}" if space else kibana

    client = MultiServerMCPClient(
        {
            "kibana": {
                "transport": "streamable_http",   <3>
                "url": f"{base}/api/agent_builder/mcp",   <4>
                "headers": {"Authorization": f"ApiKey {os.environ['KIBANA_API_KEY']}"},   <5>
            }
        }
    )

    all_tools = await client.get_tools()
    tools = [t for t in all_tools if t.name in CONTEXT_ENGINE_TOOLS]   <6>
```

1. The three Context Engine tool names to filter from the MCP server's full tool list.
2. Set `KIBANA_SPACE` to target a non-default space; leave unset for the default space.
3. The transport type required by `langchain-mcp-adapters` for the Kibana MCP endpoint.
4. Agent Builder serves the MCP endpoint at `/api/agent_builder/mcp`.
5. The MCP server accepts `Authorization` only; no `kbn-xsrf` header is needed.
6. Narrow the server's full tool list to the three Context Engine tools.
:::
:::{tab-item} API
:sync: api
Each tool wraps one endpoint. The docstrings are the only instructions the model gets about how and when to call them, so they carry the ordering and the constraints.

Every request needs these headers:

| Header                | Value                  | Notes                                                                                                           |
|:----------------------|:-----------------------|:----------------------------------------------------------------------------------------------------------------|
| `Authorization`       | `ApiKey <encoded key>` | The `encoded` value returned when you create the key.                                                           |
| `elastic-api-version` | `2023-10-31`           | Required on all three endpoints. Without it the request fails with `400`.                                       |
| `kbn-xsrf`            | `true`                 | Required for the `POST` request on self-managed and {{ech}} deployments. Harmless elsewhere, so always send it. |

```py
import os

import httpx
from langchain.tools import tool

kibana = os.environ["KIBANA_URL"].rstrip("/")
space = os.environ.get("KIBANA_SPACE")   <1>
base = f"{kibana}/s/{space}" if space else kibana

client = httpx.Client(
    base_url=f"{base}/api/context_engine",
    headers={
        "Authorization": f"ApiKey {os.environ['KIBANA_API_KEY']}",
        "elastic-api-version": "2023-10-31",   <2>
        "kbn-xsrf": "true",   <3>
        "Content-Type": "application/json",
    },
    timeout=60,
)


@tool
def list_ai_indices() -> list[dict]:
    """List the AI Indices available in this space, with the ES|QL target to query each
    one against. Call this first, before describing or querying anything."""
    response = client.get("/ai_index")
    response.raise_for_status()
    return [
        {
            "id": entry["id"],
            "esql_target": entry["dest"]["value"],   <4>
            "description": entry.get("description"),
        }
        for entry in response.json()["ai_indices"]
    ]


@tool
def describe_ai_index(ai_index_id: str) -> str:
    """Describe one AI Index: the ES|QL target to put after FROM, every field it exposes
    and which are semantic, the knowledge indicator types and tags it holds, and example
    queries. Always call this before writing a query against an index."""
    response = client.get(f"/ai_index/{ai_index_id}/_describe")
    response.raise_for_status()
    return response.json()["response"]


@tool
def query_ai_indices(query: str, params: dict | None = None, limit: int = 20) -> dict:
    """Run an ES|QL query against one or more AI Indices and return {columns, values}.
    Build the query from the output of describe_ai_index: use its FROM target and its
    field names verbatim. Pass user input as named parameters in params rather than
    writing it into the query string. Do not add any space, tenant, or permissions
    condition to the query."""
    body = {"query": query, "limit": limit}
    if params:
        body["params"] = params
    response = client.post("/ai_index/_query", json=body)
    response.raise_for_status()
    return response.json()
```

1. Set `KIBANA_SPACE` to target a non-default space; leave unset for the default space.
2. Required on all three endpoints. Without it the request fails with `400`.
3. Required for `POST` on self-managed and {{ech}} deployments. Harmless elsewhere.
4. The API response nests the {{esql}} target under `dest.value`; the example surfaces it as `esql_target` for clarity.
:::
::::

Each entry the list operation returns gives the agent:

* `id`, to pass to the describe operation.
* `esql_target`, the exact string to put after `FROM`. Use it verbatim: it differs from the ID (`sales-knowledge` becomes `ai-index-idx-sales-knowledge`) and can be a wildcard or a data stream.
* `description` and `managed`, to choose between entries.

The list omits an AI Index when your credential can't read its backing index. It does include an AI Index that's registered but still empty.

## Step 3: Create the agent

The agent needs a model, the tools from Step 2, and instructions telling it to follow the list, describe, query flow. You can supply those instructions two ways:

* **System instructions**: a prompt string in your script. Everything stays in one file, which suits a single application.
* **A skill**: a `SKILL.md` file loaded from a shared repository such as [elastic/agent-skills](https://github.com/elastic/agent-skills). One copy serves every agent that loads it, and the agent reads the full instructions only when it judges them relevant.

:::::{tab-set}
:group: ce-transport
::::{tab-item} MCP server
:sync: mcp

**With system instructions**

```py
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """\
You have access to Elastic Context Engine knowledge through three tools.

To answer a question from that knowledge:
1. Call platform_context_engine_list_ai_indices to see what is available.
2. Call platform_context_engine_describe_ai_index on the index you pick.
3. Call platform_context_engine_query_ai_indices with ES|QL built from that description.

Never guess an index ID, an ES|QL target, or a field name — the describe output gives you
all three. Never add a space or permissions condition to a query; the server applies one.
Answer from the rows you get back and cite the Knowledge Indicator titles.
"""

async def main() -> None:   <1>
    # ...MCP client and tools from Step 2...
    llm = ChatOpenAI(
        model="anthropic/claude-sonnet-4-6",
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        openai_api_base="https://openrouter.ai/api/v1",   <2>
    )
    agent = create_agent(llm, tools)
```

1. `main` is a coroutine function: it must be declared `async def` and run with `asyncio.run(main())`, as in [Step 4](#step-4-ask-a-question).
2. This example routes through OpenRouter. Replace `openai_api_base` and the corresponding API key to use a different LLM provider.

**With a skill**

`SkillsMiddleware` applies progressive disclosure: at startup it reads each skill's frontmatter and puts only the `name` and `description` into the system prompt. The agent reads the full `SKILL.md` with `read_file` when it decides the skill applies, then pulls in supporting files only as the instructions call for them. The tool-calling rules stay out of the context window until they're needed.

Replace the `SYSTEM_PROMPT` constant and the `create_agent` call with the following. Skills come from the `deepagents` package, which needs Python 3.11 or later.

```py
from urllib.request import urlopen

from deepagents.backends import StateBackend
from deepagents.backends.utils import create_file_data
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware
from langgraph.checkpoint.memory import InMemorySaver

SKILL_URL = (
    "https://raw.githubusercontent.com/elastic/agent-skills"
    "/main/skills/kibana/kibana-context-engine/SKILL.md"
)   <1>

async def main() -> None:
    # ...MCP client and tools from Step 2...
    with urlopen(SKILL_URL) as response:
        skill = response.read().decode()   <2>

    backend = StateBackend()
    skill_files = {
        "/skills/kibana-context-engine/SKILL.md": create_file_data(skill),   <3>
    }

    agent = create_agent(
        llm,
        tools,
        middleware=[
            FilesystemMiddleware(backend=backend),   <4>
            SkillsMiddleware(backend=backend, sources=["/skills/"]),   <5>
        ],
        checkpointer=InMemorySaver(),   <6>
    )
```

1. The raw URL of the skill file. Any `SKILL.md` works here.
2. Fetches the skill once, at startup.
3. Seeds the agent's virtual filesystem. The directory name under `/skills/` identifies the skill.
4. Gives the agent the `read_file` tool that the read stage depends on. Without it the agent can see each skill's description but can't open the instructions.
5. Scans `/skills/` and puts every skill it finds into the system prompt, name and description only.
6. `StateBackend` holds the skill files in the graph's state, scoped to a single thread, so skills need a `checkpointer` for that state to be stored against. Swap `InMemorySaver` for a durable `checkpointer` to keep a thread beyond the life of the process.
::::
::::{tab-item} API
:sync: api

**With system instructions**

```py
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """\
You have access to Elastic Context Engine knowledge through three tools.

To answer a question from that knowledge:
1. Call list_ai_indices to see what is available.
2. Call describe_ai_index on the index you pick.
3. Call query_ai_indices with ES|QL built from that description.

Never guess an index ID, an ES|QL target, or a field name — the describe output gives you
all three. Never add a space or permissions condition to a query; the server applies one.
Answer from the rows you get back and cite the knowledge indicator titles.
"""

def main() -> None:
    llm = ChatOpenAI(
        model="anthropic/claude-sonnet-4-6",
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        openai_api_base="https://openrouter.ai/api/v1",   <1>
    )
    agent = create_agent(llm, [list_ai_indices, describe_ai_index, query_ai_indices])
```

1. This example routes through OpenRouter. Replace `openai_api_base` and the corresponding API key to use a different LLM provider.

**With a skill**

`SkillsMiddleware` applies progressive disclosure: at startup it reads each skill's frontmatter and puts only the `name` and `description` into the system prompt. The agent reads the full `SKILL.md` with `read_file` when it decides the skill applies, then pulls in supporting files only as the instructions call for them. The tool-calling rules stay out of the context window until they're needed.


Replace the `SYSTEM_PROMPT` constant and the `create_agent` call with the following. Skills come from the `deepagents` package, which needs Python 3.11 or later.

```py
from urllib.request import urlopen

from deepagents.backends import StateBackend
from deepagents.backends.utils import create_file_data
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware
from langgraph.checkpoint.memory import InMemorySaver

SKILL_URL = (
    "https://raw.githubusercontent.com/elastic/agent-skills"
    "/main/skills/kibana/kibana-context-engine/SKILL.md"
)   <1>


def main() -> None:
    with urlopen(SKILL_URL) as response:
        skill = response.read().decode()   <2>

    backend = StateBackend()
    skill_files = {
        "/skills/kibana-context-engine/SKILL.md": create_file_data(skill),   <3>
    }

    agent = create_agent(
        llm,
        [list_ai_indices, describe_ai_index, query_ai_indices],
        middleware=[
            FilesystemMiddleware(backend=backend),   <4>
            SkillsMiddleware(backend=backend, sources=["/skills/"]),   <5>
        ],
        checkpointer=InMemorySaver(),   <6>
    )
```

1. The raw URL of the skill file. Any `SKILL.md` works here.
2. Fetches the skill once, at startup.
3. Seeds the agent's virtual filesystem. The directory name under `/skills/` identifies the skill.
4. Gives the agent the `read_file` tool that the read stage depends on. Without it the agent can see each skill's description but can't open the instructions.
5. Scans `/skills/` and puts every skill it finds into the system prompt, name and description only.
6. `StateBackend` holds the skill files in the graph's state, scoped to a single thread, so skills need a `checkpointer` for that state to be stored against. Swap `InMemorySaver` for a durable `checkpointer` to keep a thread beyond the life of the process.
::::
:::::

## Step 4: Ask a question

Invoke the agent with a question that the Knowledge Indicators in your AI Index can answer. The below question is just an example for illustration purposes.

::::{tab-set}
:group: ce-transport
:::{tab-item} MCP server
:sync: mcp

**With system instructions**

```py
async def main() -> None:
    # ...agent from Step 3...
    result = await agent.ainvoke(
        {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "What is our refund policy for annual plans?"},
            ]
        }
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
```

**With a skill**

```py
async def main() -> None:
    # ...agent from Step 3...
    result = await agent.ainvoke(
        {
            "messages": [
                {"role": "user", "content": "What is our refund policy for annual plans?"},
            ],
            "files": skill_files,
        },
        config={"configurable": {"thread_id": "1"}},
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
```
:::
:::{tab-item} API
:sync: api

**With system instructions**

```py
def main() -> None:
    # ...agent from Step 3...
    result = agent.invoke(
        {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "What is our refund policy for annual plans?"},
            ]
        }
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
```

**With a skill**

```py
def main() -> None:
    # ...agent from Step 3...
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "What is our refund policy for annual plans?"},
            ],
            "files": skill_files,
        },
        config={"configurable": {"thread_id": "1"}},
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
```
:::
::::

A successful run shows the agent working through the retrieval flow in order. Check that:

* It called the list tool and got back at least one AI Index.
* It called the describe tool on the index it selected.
* Its query used the target and field names returned by `describe`, not invented ones.
* The answer draws on Knowledge Indicator content, and names the indicators it used.

If the agent answers without calling the tools, or queries a target that describe never returned, the instructions aren't reaching it. Check that the system message is attached, or that the skill loaded, before looking at privileges. To see the calls it made, inspect `result["messages"]` rather than only the final entry.

## Query a different space

Set `KIBANA_SPACE` to the space ID before creating the client, so requests go to `/s/{space_id}/api/context_engine`. The API key needs the Context Engine feature privilege in that space, and `contextEngine:enabled` has to be on there.

To read from several spaces in one agent, build one client per space and register a separate set of tools for each.

## Troubleshooting

| Symptom | Cause | Resolution |
| :---- | :---- | :---- |
| `400 Please specify a version via elastic-api-version header` | The version header is missing. | Send `elastic-api-version: 2023-10-31` on every request. |
| `400 Request must contain a kbn-xsrf header` | A `POST` without the header, on a deployment that requires it. | Send `kbn-xsrf: true`. |
| `403` on every endpoint | The API key lacks the Kibana **Context Engine** feature privilege. | Add it to the role. Elasticsearch index privileges alone aren't enough. |
| `403` on query or describe only | Missing Elasticsearch privileges on the backing indices. | Grant `read` and `view_index_metadata` on `ai-index-*`. |
| `404` on every endpoint | `contextEngine:enabled` is off in the space the URL points at. | Turn it on in that space's advanced settings. |
| An AI Index you expect isn't listed | No `read` on its backing index, or every document in it belongs to another space. | Check the key's index privileges and which space the URL targets. |
| `Unknown index` from a query, for an ID that *was* listed | The AI Index is registered but its backing index doesn't exist yet. | Expected for a registration with no data. Pick another index. |
| A query returns no rows, but the index has data | Either the request is scoped to the wrong space, or the query carries its own space condition. | Point the request at the right space, and remove any space condition from the query. |
| Describe returns a block with no `Knowledge item types` or `Tags` section | The counts need `read` on the backing indices, and need `type` and `tags` mapped as aggregatable keywords. | Expected degradation. The rest of the block is still usable. |
| An error saying the response is too large | The result exceeds the 20 MB cap. | Drop large fields with `KEEP`, lower `limit`, or aggregate with `STATS`. |

## Appendix

Here are the full end-to-end Python scripts using the system prompt option from [Step 3](#step-3-create-the-agent).

:::{dropdown} demo_mcp.py
```py
import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

CONTEXT_ENGINE_TOOLS = {
    "platform_context_engine_list_ai_indices",
    "platform_context_engine_describe_ai_index",
    "platform_context_engine_query_ai_indices",
}

SYSTEM_PROMPT = """\
You have access to Elastic Context Engine knowledge through three tools.

To answer a question from that knowledge:
1. Call platform_context_engine_list_ai_indices to see what is available.
2. Call platform_context_engine_describe_ai_index on the index you pick.
3. Call platform_context_engine_query_ai_indices with ES|QL built from that description.

Never guess an index ID, an ES|QL target, or a field name — the describe output gives you
all three. Never add a space or permissions condition to a query; the server applies one.
Answer from the rows you get back and cite the Knowledge Indicator titles.
"""


async def main() -> None:
    kibana = os.environ["KIBANA_URL"].rstrip("/")
    space = os.environ.get("KIBANA_SPACE")
    base = f"{kibana}/s/{space}" if space else kibana

    client = MultiServerMCPClient(
        {
            "kibana": {
                "transport": "streamable_http",
                "url": f"{base}/api/agent_builder/mcp",
                "headers": {"Authorization": f"ApiKey {os.environ['KIBANA_API_KEY']}"},
            }
        }
    )

    all_tools = await client.get_tools()
    tools = [t for t in all_tools if t.name in CONTEXT_ENGINE_TOOLS]

    llm = ChatOpenAI(
        model="anthropic/claude-sonnet-4-6",
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        openai_api_base="https://openrouter.ai/api/v1",
    )
    agent = create_agent(llm, tools)

    result = await agent.ainvoke(
        {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "What is our refund policy for annual plans?"},
            ]
        }
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
```
:::

:::{dropdown} demo_api.py
```py
import os

import httpx
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """\
You have access to Elastic Context Engine knowledge through three tools.

To answer a question from that knowledge:
1. Call list_ai_indices to see what is available.
2. Call describe_ai_index on the index you pick.
3. Call query_ai_indices with ES|QL built from that description.

Never guess an index ID, an ES|QL target, or a field name — the describe output gives you
all three. Never add a space or permissions condition to a query; the server applies one.
Answer from the rows you get back and cite the Knowledge Indicator titles.
"""

_kibana = os.environ["KIBANA_URL"].rstrip("/")
_space = os.environ.get("KIBANA_SPACE")
_base = f"{_kibana}/s/{_space}" if _space else _kibana

client = httpx.Client(
    base_url=f"{_base}/api/context_engine",
    headers={
        "Authorization": f"ApiKey {os.environ['KIBANA_API_KEY']}",
        "elastic-api-version": "2023-10-31",
        "kbn-xsrf": "true",
        "Content-Type": "application/json",
    },
    timeout=60,
)


@tool
def list_ai_indices() -> list[dict]:
    """List the AI Indices available in this space, with the ES|QL target to query each
    one against. Call this first, before describing or querying anything."""
    response = client.get("/ai_index")
    response.raise_for_status()
    return [
        {
            "id": entry["id"],
            "esql_target": entry["dest"]["value"],
            "description": entry.get("description"),
        }
        for entry in response.json()["ai_indices"]
    ]


@tool
def describe_ai_index(ai_index_id: str) -> str:
    """Describe one AI Index: the ES|QL target to put after FROM, every field it exposes
    and which are semantic, the knowledge indicator types and tags it holds, and example
    queries. Always call this before writing a query against an index."""
    response = client.get(f"/ai_index/{ai_index_id}/_describe")
    response.raise_for_status()
    return response.json()["response"]


@tool
def query_ai_indices(query: str, params: dict | None = None, limit: int = 20) -> dict:
    """Run an ES|QL query against one or more AI Indices and return {columns, values}.
    Build the query from the output of describe_ai_index: use its FROM target and its
    field names verbatim. Pass user input as named parameters in params rather than
    writing it into the query string. Do not add any space, tenant, or permissions
    condition to the query."""
    body = {"query": query, "limit": limit}
    if params:
        body["params"] = params
    response = client.post("/ai_index/_query", json=body)
    response.raise_for_status()
    return response.json()


def main() -> None:
    llm = ChatOpenAI(
        model="anthropic/claude-sonnet-4-6",
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        openai_api_base="https://openrouter.ai/api/v1",
    )
    agent = create_agent(llm, [list_ai_indices, describe_ai_index, query_ai_indices])

    result = agent.invoke(
        {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "What is our refund policy for annual plans?"},
            ]
        }
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
```
:::

Additionally, take a look at the same two scripts using the skill option from [Step 3](#step-3-create-the-agent):

:::{dropdown} demo_mcp_skill.py
```py
import asyncio
import os
from urllib.request import urlopen

from deepagents.backends import StateBackend
from deepagents.backends.utils import create_file_data
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

CONTEXT_ENGINE_TOOLS = {
    "platform_context_engine_list_ai_indices",
    "platform_context_engine_describe_ai_index",
    "platform_context_engine_query_ai_indices",
}

SKILL_URL = (
    "https://raw.githubusercontent.com/elastic/agent-skills"
    "/main/skills/kibana/kibana-context-engine/SKILL.md"
)


async def main() -> None:
    kibana = os.environ["KIBANA_URL"].rstrip("/")
    space = os.environ.get("KIBANA_SPACE")
    base = f"{kibana}/s/{space}" if space else kibana

    client = MultiServerMCPClient(
        {
            "kibana": {
                "transport": "streamable_http",
                "url": f"{base}/api/agent_builder/mcp",
                "headers": {"Authorization": f"ApiKey {os.environ['KIBANA_API_KEY']}"},
            }
        }
    )

    all_tools = await client.get_tools()
    tools = [t for t in all_tools if t.name in CONTEXT_ENGINE_TOOLS]

    with urlopen(SKILL_URL) as response:
        skill = response.read().decode()

    backend = StateBackend()
    skill_files = {
        "/skills/kibana-context-engine/SKILL.md": create_file_data(skill),
    }

    llm = ChatOpenAI(
        model="anthropic/claude-sonnet-4-6",
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        openai_api_base="https://openrouter.ai/api/v1",
    )
    agent = create_agent(
        llm,
        tools,
        middleware=[
            FilesystemMiddleware(backend=backend),
            SkillsMiddleware(backend=backend, sources=["/skills/"]),
        ],
        checkpointer=InMemorySaver(),
    )

    result = await agent.ainvoke(
        {
            "messages": [
                {"role": "user", "content": "What is our refund policy for annual plans?"},
            ],
            "files": skill_files,
        },
        config={"configurable": {"thread_id": "1"}},
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
```
:::

:::{dropdown} demo_api_skill.py
```py
import os
from urllib.request import urlopen

import httpx
from deepagents.backends import StateBackend
from deepagents.backends.utils import create_file_data
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

SKILL_URL = (
    "https://raw.githubusercontent.com/elastic/agent-skills"
    "/main/skills/kibana/kibana-context-engine/SKILL.md"
)

_kibana = os.environ["KIBANA_URL"].rstrip("/")
_space = os.environ.get("KIBANA_SPACE")
_base = f"{_kibana}/s/{_space}" if _space else _kibana

client = httpx.Client(
    base_url=f"{_base}/api/context_engine",
    headers={
        "Authorization": f"ApiKey {os.environ['KIBANA_API_KEY']}",
        "elastic-api-version": "2023-10-31",
        "kbn-xsrf": "true",
        "Content-Type": "application/json",
    },
    timeout=60,
)


@tool
def list_ai_indices() -> list[dict]:
    """List the AI Indices available in this space, with the ES|QL target to query each
    one against. Call this first, before describing or querying anything."""
    response = client.get("/ai_index")
    response.raise_for_status()
    return [
        {
            "id": entry["id"],
            "esql_target": entry["dest"]["value"],
            "description": entry.get("description"),
        }
        for entry in response.json()["ai_indices"]
    ]


@tool
def describe_ai_index(ai_index_id: str) -> str:
    """Describe one AI Index: the ES|QL target to put after FROM, every field it exposes
    and which are semantic, the knowledge indicator types and tags it holds, and example
    queries. Always call this before writing a query against an index."""
    response = client.get(f"/ai_index/{ai_index_id}/_describe")
    response.raise_for_status()
    return response.json()["response"]


@tool
def query_ai_indices(query: str, params: dict | None = None, limit: int = 20) -> dict:
    """Run an ES|QL query against one or more AI Indices and return {columns, values}.
    Build the query from the output of describe_ai_index: use its FROM target and its
    field names verbatim. Pass user input as named parameters in params rather than
    writing it into the query string. Do not add any space, tenant, or permissions
    condition to the query."""
    body = {"query": query, "limit": limit}
    if params:
        body["params"] = params
    response = client.post("/ai_index/_query", json=body)
    response.raise_for_status()
    return response.json()


def main() -> None:
    with urlopen(SKILL_URL) as response:
        skill = response.read().decode()

    backend = StateBackend()
    skill_files = {
        "/skills/kibana-context-engine/SKILL.md": create_file_data(skill),
    }

    llm = ChatOpenAI(
        model="anthropic/claude-sonnet-4-6",
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        openai_api_base="https://openrouter.ai/api/v1",
    )
    agent = create_agent(
        llm,
        [list_ai_indices, describe_ai_index, query_ai_indices],
        middleware=[
            FilesystemMiddleware(backend=backend),
            SkillsMiddleware(backend=backend, sources=["/skills/"]),
        ],
        checkpointer=InMemorySaver(),
    )

    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "What is our refund policy for annual plans?"},
            ],
            "files": skill_files,
        },
        config={"configurable": {"thread_id": "1"}},
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
```
:::

Here's an example of a `pyproject.toml` with the dependencies for the above scripts:

```toml
[dependency-groups]
dev = [
    "deepagents>=0.7",  # needed if choosing skills over system prompts; raises floor to Python 3.11
    "langchain>=1.4.0",
    "langchain-mcp-adapters>=0.3.2",  # needed if choosing the MCP connection route
    "langchain-openai>=1.6.2",  # only needed for this example or if you want to use OpenAI or OpenRouter LLMs
]
```
