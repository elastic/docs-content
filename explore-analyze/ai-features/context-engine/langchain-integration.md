---
navigation_title: LangChain Integration
description: Give a LangChain agent tools that list, describe, and query Context Engine AI indices, so it can retrieve knowledge indicators with ES|QL.
applies_to:
  stack: preview 9.6
  serverless: preview
products:
  - id: kibana
---

# Query AI indices from LangChain

:::{important}
This page is currently hidden from the documentation navigation. It is intended for testing and review while the feature is under development.
:::

A LangChain agent can retrieve knowledge from the Context Engine through three read-only tools exposed by Kibana's Model Context Protocol (MCP) server. This page shows you how to connect to the server, hand the tools to an agent, and write the ES|QL the agent runs. The same three operations are also available as plain HTTP APIs, which you can wrap as LangChain tools yourself. Use that route if you can't reach the MCP server or don't run Agent Builder.

By the end you'll have an agent that answers questions from the Knowledge Indicators stored in an AI Index, scoped to a single Kibana space and to what your credential is allowed to read.

Examples on this page use Python. The same approach works in LangChain.js.

## Requirements

* An {{stack}} deployment with an Enterprise license, or an {{serverless-full}} project.
* The `contextEngine:enabled` advanced setting turned on in the space you want to query. This setting is per space, and the APIs return `404` in any space where it's off.
* At least one AI Index containing Knowledge Indicators (KIs). See [Create an AI index](quickstart.md#2.-create-an-ai-index) if you don't have one yet.
* An API key whose privileges cover both Kibana and Elasticsearch. [Step 1](#step-1-create-an-api-key) walks through this.
* Python 3.10 or later, with `langchain` installed. [Step 4](#step-4-load-the-instructions-from-a-skill) adds `deepagents`, which needs 3.11 or later.

## How it works

Your agent reaches them through three tools, and it must call them in this order:

| Order | Tool | What it does | Backing API |
| :---: | :---: | :---: | :---: |
| 1 | `platform_context_engine_list_ai_indices` | Returns the AI Indices you can use, each with the ES|QL target to query it against | `GET /api/context_engine/ai_index` |
| 2 | `platform_context_engine_describe_ai_index` | Returns a context block for one index: its fields, its Knowledge Indicator types and tags, and example queries | `GET /api/context_engine/ai_index/{ai_index_id}/_describe` |
| 3 | `platform_context_engine_query_ai_indices` | Runs ES|QL and returns `{columns, values}` | `POST /api/context_engine/ai_index/_query` |

The order matters. Describe returns the exact `FROM` target and the real field names for that index, so an agent that skips it has to guess, and a query written from a guess either errors or silently returns nothing.

Each tool runs the same code as its backing API, as the owner of the API key, and each is scoped to one Kibana space. The space comes from either:

* MCP path: the URL the MCP server is served from: `/api/agent_builder/mcp` is the default space, and `/s/{space_id}/api/agent_builder/mcp` is the space named in the path.
* API path: request URL: `/api/...` is the default space, and `/s/{space_id}/api/...` is the space named in the path

Two differences to know about:

* MCP path needs Agent Builder enabled, and the API key needs the Agent Builder **Read** privilege as well as Context Engine **Read**.
* The `list` **tool** returns the ES|QL target as `esql_target` directly, rather than nested under `dest.value`.

If you're running via APIs, bear in mind that every request also needs these headers:

| Header | Value | Notes |
| :---- | :---- | :---- |
| `Authorization` | `ApiKey <encoded key>` | The `encoded` value returned when you create the key. |
| `elastic-api-version` | `2023-10-31` | Required on all three endpoints. Without it the request fails with `400`. |
| `kbn-xsrf` | `true` | Required for the `POST` request on self-managed and {{ech}} deployments. Harmless elsewhere, so always send it. |

## Step 1: Create an API key

Three independent checks stand between your credential and a result. The MCP server checks that you have Agent Builder **Read**, which is what makes the tools visible. Each tool then checks that you have Context Engine **Read**. Elasticsearch finally checks your privileges on the indices the query actually touches. You need all three.

1. In Kibana, go to **Stack Management → Roles** and create a role with:

    * **Index privileges**: `read` and `view_index_metadata` on `ai-index-*` and `.ai-index-*`.
    * **Kibana privileges**, in the space you want to query: the **Agent Builder** feature at **Read**, and the **Context Engine** feature at **Read**. If you're running the API route, rather than MCP tools, you only need **Context Engine Read**.

2. Assign the role to your user.

3. Go to **Stack Management → API keys** and create a key. Leave **Control security privileges** off, so the key inherits your user's privileges — including the two Kibana feature privileges.

4. Copy the `encoded` value and export it, along with your Kibana URL:

    ```shell
    export KIBANA_URL="https://my-deployment.kb.us-east-1.aws.elastic.cloud"
    export KIBANA_API_KEY="VnVhQ2ZHY0JDZGJrU..."
    ```

Alternatively, in Serverless, you can directly create an API key with the following privileges:

```json
{
  "ab_ce": {
    "cluster": [],
    "indices": [
      {
        "names": [
          "ai-index-*",
          ".ai-index-*"
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

For this demo, we also use an OpenRouter key:

```shell
export OPENROUTER_API_KEY="sk-..."
```

## Step 2: Get the appropriate tools

Choose the approach that fits your setup.

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
    """List the AI indices available in this space, with the ES|QL target to query each
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
    """Describe one AI index: the ES|QL target to put after FROM, every field it exposes
    and which are semantic, the knowledge indicator types and tags it holds, and example
    queries. Always call this before writing a query against an index."""
    response = client.get(f"/ai_index/{ai_index_id}/_describe")
    response.raise_for_status()
    return response.json()["response"]


@tool
def query_ai_indices(query: str, params: dict | None = None, limit: int = 20) -> dict:
    """Run an ES|QL query against one or more AI indices and return {columns, values}.
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
4. The API response nests the ES|QL target under `dest.value`; the example surfaces it as `esql_target` for clarity.
:::
::::

The list omits an AI Index when your credential can't read its backing index. The list does include an AI Index that's registered but still empty.

## Step 3: Give the tools to an agent

::::{tab-set}
:group: ce-transport
:::{tab-item} MCP server
:sync: mcp

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

# Add inside main(), after the tools from Step 2:
llm = ChatOpenAI(
    model="anthropic/claude-sonnet-4-6",
    openai_api_key=os.environ["OPENROUTER_API_KEY"],
    openai_api_base="https://openrouter.ai/api/v1",   <1>
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
```

1. This example routes through OpenRouter. Replace `openai_api_base` and the corresponding API key to use a different LLM provider.
:::
:::{tab-item} API
:sync: api

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

# Add after the tools from Step 2:
def main() -> None:
    llm = ChatOpenAI(
        model="anthropic/claude-sonnet-4-6",
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        openai_api_base="https://openrouter.ai/api/v1",   <1>
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

1. This example routes through OpenRouter. Replace `openai_api_base` and the corresponding API key to use a different LLM provider.
:::
::::

Each entry from the list tool gives the agent:

* `id`, to pass to describe.
* `esql_target`, the exact string to put after `FROM`. Use it verbatim: it differs from the ID (`sales-knowledge` becomes `ai-index-idx-sales-knowledge`) and can be a wildcard or a data stream.
* `description` and `managed`, to choose between entries.

## Step 4: Load the instructions from a skill

Step 3 keeps the agent's instructions in a `SYSTEM_PROMPT` string inside your script. You can load them from a **skill** instead: a `SKILL.md` file, with YAML frontmatter and Markdown instructions, kept in a shared repository such as [elastic/agent-skills](https://github.com/elastic/agent-skills). One copy then serves every agent that loads it, and editing that file updates all of them.

A skill also reaches the model differently. `SkillsMiddleware` applies progressive disclosure:

1. **Discovery**: at startup, the middleware reads each skill's frontmatter and puts only its `name` and `description` into the system prompt.
2. **Read**: when the agent judges that the skill applies, it reads the full `SKILL.md` with `read_file`.
3. **Execute**: it then follows those instructions, pulling in supporting files only as the instructions call for them.

The tool-calling rules stay out of the context window until the agent needs them, rather than riding along on every request the way a system prompt does.

:::{note}
The Context Engine skill isn't published to `elastic/agent-skills` yet. Until it is, point `SKILL_URL` at your own copy of the file.
:::

Skills come from the `deepagents` package. It needs Python 3.11 or later, a version above the 3.10 the rest of this page runs on:

```toml
[dependency-groups]
dev = [
    "deepagents>=0.7",
]
```

Then drop the `SYSTEM_PROMPT` constant and the `{"role": "system", ...}` message from Step 3, and replace the agent setup with the following.

::::{tab-set}
:group: ce-transport
:::{tab-item} MCP server
:sync: mcp

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

# Inside main(), in place of the agent setup from Step 3:
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

result = await agent.ainvoke(
    {
        "messages": [
            {"role": "user", "content": "What is our refund policy for annual plans?"},   <7>
        ],
        "files": skill_files,   <8>
    },
    config={"configurable": {"thread_id": "1"}},   <9>
)
print(result["messages"][-1].content)
```

1. The raw URL of the skill file. Any `SKILL.md` works here.
2. Fetches the skill once, at startup.
3. Seeds the agent's virtual filesystem. The directory name under `/skills/` identifies the skill.
4. Gives the agent the `read_file` tool that the **Read** stage depends on. Without it the agent can see each skill's description but can't open the instructions.
5. Scans `/skills/` and puts every skill it finds into the system prompt, name and description only.
6. `StateBackend` holds the skill files in the graph's state, scoped to a single thread, so skills need a checkpointer for that state to be stored against. Swap `InMemorySaver` for a durable checkpointer to keep a thread beyond the life of the process.
7. No system message: the skill carries the instructions now.
8. Passes the seeded filesystem into the run, so `SkillsMiddleware` can read from it.
9. Identifies the thread. Reuse it on a later call to continue the same conversation, or change it to start fresh. A fixed `"1"` suits a script that asks one question and exits; a real application generates one ID per conversation.
:::
:::{tab-item} API
:sync: api

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

    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "What is our refund policy for annual plans?"},   <7>
            ],
            "files": skill_files,   <8>
        },
        config={"configurable": {"thread_id": "1"}},   <9>
    )
    print(result["messages"][-1].content)
```

1. The raw URL of the skill file. Any `SKILL.md` works here.
2. Fetches the skill once, at startup.
3. Seeds the agent's virtual filesystem. The directory name under `/skills/` identifies the skill.
4. Gives the agent the `read_file` tool that the **Read** stage depends on. Without it the agent can see each skill's description but can't open the instructions.
5. Scans `/skills/` and puts every skill it finds into the system prompt, name and description only.
6. `StateBackend` holds the skill files in the graph's state, scoped to a single thread, so skills need a checkpointer for that state to be stored against. Swap `InMemorySaver` for a durable checkpointer to keep a thread beyond the life of the process.
7. No system message: the skill carries the instructions now.
8. Passes the seeded filesystem into the run, so `SkillsMiddleware` can read from it.
9. Identifies the thread. Reuse it on a later call to continue the same conversation, or change it to start fresh. A fixed `"1"` suits a script that asks one question and exits; a real application generates one ID per conversation.
:::
::::

To load more than one skill, seed each under its own directory in `skill_files`. `SkillsMiddleware` picks up everything under the `sources` paths you give it.

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
| An AI index you expect isn't listed | No `read` on its backing index, or every document in it belongs to another space. | Check the key's index privileges and which space the URL targets. |
| `Unknown index` from a query, for an ID that *was* listed | The AI index is registered but its backing index doesn't exist yet. | Expected for a registration with no data. Pick another index. |
| A query returns no rows, but the index has data | Either the request is scoped to the wrong space, or the query carries its own space condition. | Point the request at the right space, and remove any space condition from the query. |
| Describe returns a block with no `Knowledge item types` or `Tags` section | The counts need `read` on the backing indices, and need `type` and `tags` mapped as aggregatable keywords. | Expected degradation. The rest of the block is still usable. |
| An error saying the response is too large | The result exceeds the 20 MB cap. | Drop large fields with `KEEP`, lower `limit`, or aggregate with `STATS`. |

## Appendix

Full Python scripts

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
    """List the AI indices available in this space, with the ES|QL target to query each
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
    """Describe one AI index: the ES|QL target to put after FROM, every field it exposes
    and which are semantic, the knowledge indicator types and tags it holds, and example
    queries. Always call this before writing a query against an index."""
    response = client.get(f"/ai_index/{ai_index_id}/_describe")
    response.raise_for_status()
    return response.json()["response"]


@tool
def query_ai_indices(query: str, params: dict | None = None, limit: int = 20) -> dict:
    """Run an ES|QL query against one or more AI indices and return {columns, values}.
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

The same two scripts with [Step 4](#step-4-load-the-instructions-from-a-skill) applied, taking their instructions from a skill instead of a system prompt:

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
    """List the AI indices available in this space, with the ES|QL target to query each
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
    """Describe one AI index: the ES|QL target to put after FROM, every field it exposes
    and which are semantic, the knowledge indicator types and tags it holds, and example
    queries. Always call this before writing a query against an index."""
    response = client.get(f"/ai_index/{ai_index_id}/_describe")
    response.raise_for_status()
    return response.json()["response"]


@tool
def query_ai_indices(query: str, params: dict | None = None, limit: int = 20) -> dict:
    """Run an ES|QL query against one or more AI indices and return {columns, values}.
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

Minimal requirements in `pyproject.toml`

```toml
[dependency-groups]
dev = [
    "deepagents>=0.7",
    "langchain>=1.4.0",
    "langchain-mcp-adapters>=0.3.2",
    "langchain-openai>=1.6.2",
]
```

Only the two skill scripts need `deepagents`, and it raises the floor to Python 3.11. Drop that line if you're running the Step 3 scripts alone.
