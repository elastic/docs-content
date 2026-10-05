---
navigation_title: "LangChain"
description: Wrap the Context Engine APIs as LangChain tools, so a LangChain agent can retrieve Knowledge Indicators from your AI Indices.
type: how-to
applies_to:
  stack: experimental 9.6
  serverless: experimental
products:
  - id: kibana
---

# Query AI Indices from LangChain

:::{include} _snippets/hidden-docs-notice.md
:::

A LangChain agent can retrieve Knowledge Indicators (KIs) from {{context-engine}} using read-only tools.

For the integration model and the built-in {{agent-builder}} route, refer to [Use {{context-engine}} with agents and applications](use-context-engine-with-agents.md).

To connect a LangChain agent to {{context-engine}}, use the {{context-engine}} APIs to wrap the available retrieval operations as LangChain tools in your application.

Examples on this page use Python, but the same approach works in [LangChain.js](https://reference.langchain.com/javascript/langchain).

## Requirements

Before you begin, make sure you have:

* An {{stack}} deployment with an Enterprise license, or an {{serverless-full}} project.
* The `contextEngine:enabled` advanced setting turned on in the space you want to query. This setting is per space, and the APIs return `404` in any space where it's off.
* At least one AI Index containing Knowledge Indicators (KIs). See [Create an AI Index](quickstart.md#context-engine-create-ai-index) if you don't have one yet.
* An API key whose privileges cover both Kibana and Elasticsearch. [Step 1](#step-1-create-credentials) walks through this.
* Python 3.10 or later, with `langchain` installed. The skill option in [Step 3](#step-3-create-the-agent) adds `deepagents`, which needs 3.11 or later.

## How retrieval works

{{context-engine}} uses a discovery-first retrieval flow:

1. List the AI Indices available to the agent.
2. Describe the relevant AI Index to identify its query target, fields, and available Knowledge Indicators.
3. Query the AI Index using the information returned by the describe operation.

Describing the AI Index before querying it prevents the agent from guessing the query target or field names.

All three operations run against one {{kib}} space, as the owner of the API key. An agent only ever sees the AI Indices that key is allowed to read.

## Step 1: Create credentials

Your credential needs privileges in both Kibana and Elasticsearch.

Create the credential as follows:

1. In Kibana, go to **Stack Management → API Keys** and click `Create API key`
2. Leave **Control security privileges** off and define a role with the following privileges:

    * **Index privileges**: `read` and `view_index_metadata` on `ai-index-*`.
    * **Kibana privileges**, in the space you want to query: **{{context-engine}}** at **Read**.

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

3. Copy the `encoded` value and export it, along with your Kibana URL:

    ```shell
    export KIBANA_URL="https://my-deployment.kb.us-east-1.aws.elastic.cloud"
    export KIBANA_API_KEY="VnVhQ2ZHY0JDZGJrU..."
    ```

This example also uses an OpenRouter key to reach the model:

```shell
export OPENROUTER_API_KEY="sk-..."
```

## Step 2: Wrap the retrieval operations as tools

Each tool wraps one endpoint. The docstrings are the only instructions the model gets about how and when to call them, so they carry the ordering and the constraints.

The following API references define the request and response schemas used by the tools:

- [List AI indices](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-context-engine-ai-index)
- [Describe an AI index](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-context-engine-ai-index-aiindexid-describe)
- [Query AI indices](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-context-engine-ai-index-query)

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

The annotations explain the following details:

1. Set `KIBANA_SPACE` to target a non-default space. Leave it unset for the default space.
2. Required on all three endpoints. Without it the request fails with `400`.
3. Required for `POST` on self-managed and {{ech}} deployments. Harmless elsewhere.
4. The API response nests the {{esql}} target under `dest.value`. The example surfaces it as `esql_target` for clarity.

Each entry the list operation returns gives the agent:

* `id`, to pass to the describe operation.
* `esql_target`, the exact string to put after `FROM`. Use it verbatim: it differs from the ID (`sales-knowledge` becomes `ai-index-idx-sales-knowledge`) and can be a wildcard or a data stream.
* `description`, to determine whether the AI Index is relevant to the question.
* `managed`, to distinguish a [built-in AI Index supplied by an Elastic integration](concepts.md#managed-ai-indices) from one created by a user.

The list omits an AI Index when your credential can't read its backing index. It does include an AI Index that's registered but still empty.

## Step 3: Create the agent

The agent needs a model, the tools from Step 2, and instructions telling it to follow the list, describe, query flow. You can supply those instructions two ways:

* **System instructions**: a prompt string in your script. Everything stays in one file, which suits a single application.
* **A skill**: a `SKILL.md` file that you write and keep outside your script. One copy serves every agent that loads it, and the agent reads the full instructions only when it judges them relevant.

::::{tab-set}
:group: ce-instructions
:::{tab-item} System instructions
:sync: system-prompt

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
all three. The server applies the space and permissions condition, so never add one to a query.
Answer from the rows you get back and cite the Knowledge Indicator titles.
"""

def main() -> None:
    llm = ChatOpenAI(
        model="anthropic/claude-sonnet-4-6",
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        openai_api_base="https://openrouter.ai/api/v1",   <1>
    )
    agent = create_agent(llm, [list_ai_indices, describe_ai_index, query_ai_indices])
```

The annotation explains the following detail:

1. This example routes through OpenRouter. Replace `openai_api_base` and the corresponding API key to use a different LLM provider.

:::
:::{tab-item} Skill
:sync: skill

`SkillsMiddleware` applies progressive disclosure: at startup it reads each skill's frontmatter and puts only the `name` and `description` into the system prompt. The agent reads the full `SKILL.md` with `read_file` when it decides the skill applies, then pulls in supporting files only as the instructions call for them. The tool-calling rules stay out of the context window until they're needed.

Write the skill yourself, so it names your tools and states the rules your agent has to follow. The frontmatter needs a `name` and a `description`, and the `name` has to match the directory that holds the file. The description is all the agent sees until it opens the file, so write it around the questions the skill helps answer.

The following `SKILL.md` covers the retrieval flow for the tools from [Step 2](#step-2-wrap-the-retrieval-operations-as-tools). Save it as `skills/context-engine-retrieval/SKILL.md`, next to your script:

```markdown
---
name: context-engine-retrieval
description: Retrieve Knowledge Indicators from Elastic Context Engine AI Indices. Use when a question is likely answered by recurring internal knowledge, such as policies, runbooks, or past investigation findings.
---

# Retrieve context from Elastic Context Engine

Elastic Context Engine knowledge is available through three tools: `list_ai_indices`,
`describe_ai_index`, and `query_ai_indices`.

## Retrieval flow

1. Call `list_ai_indices` to see which AI Indices you can read.
2. Pick the AI Index whose description matches the question, then call `describe_ai_index` on it.
3. Call `query_ai_indices` with an ES|QL query built from that description.

## Rules

- Never guess an index ID, an ES|QL target, or a field name. The describe output gives you all three.
- Use the `FROM` target from the describe output verbatim.
- Pass user input as named parameters rather than writing it into the query string.
- The server applies the space and permissions condition, so never add one to a query.
- Answer from the rows you get back and cite the Knowledge Indicator titles.
```

Create the agent with the skills middleware instead of a system prompt. Skills come from the `deepagents` package, which needs Python 3.11 or later.

```py
from pathlib import Path

from deepagents.backends import StateBackend
from deepagents.backends.utils import create_file_data
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware
from langgraph.checkpoint.memory import InMemorySaver

SKILL_PATH = Path(__file__).parent / "skills/context-engine-retrieval/SKILL.md"


def main() -> None:
    # ...llm as in the system instructions example...
    backend = StateBackend()
    skill_files = {
        "/skills/context-engine-retrieval/SKILL.md": create_file_data(
            SKILL_PATH.read_text()
        ),   <1>
    }

    agent = create_agent(
        llm,
        [list_ai_indices, describe_ai_index, query_ai_indices],
        middleware=[
            FilesystemMiddleware(backend=backend),   <2>
            SkillsMiddleware(backend=backend, sources=["/skills/"]),   <3>
        ],
        checkpointer=InMemorySaver(),   <4>
    )
```

The annotations explain the following details:

1. Reads the skill once, at startup, and seeds the agent's virtual filesystem with it. The directory name under `/skills/` has to match the `name` in the skill's frontmatter.
2. Gives the agent the `read_file` tool that the read stage depends on. Without it the agent can see each skill's description but can't open the instructions.
3. Scans `/skills/` and puts every skill it finds into the system prompt, name and description only.
4. `StateBackend` holds the skill files in the graph's state, scoped to a single thread, so skills need a `checkpointer` for that state to be stored against. Swap `InMemorySaver` for a durable `checkpointer` to keep a thread beyond the life of the process.

:::
::::

## Step 4: Ask a question

Invoke the agent with a question that the Knowledge Indicators in your AI Index can answer. The following question is an example.

::::{tab-set}
:group: ce-instructions
:::{tab-item} System instructions
:sync: system-prompt

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

:::
:::{tab-item} Skill
:sync: skill

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

Set `KIBANA_SPACE` to the space ID before creating the client, so requests go to `/s/{space_id}/api/context_engine`. The API key needs the {{context-engine}} feature privilege in that space, and `contextEngine:enabled` has to be on there.

To read from several spaces in one agent, build one client per space and register a separate set of tools for each.

For common access and retrieval failures, refer to [Troubleshoot {{context-engine}} retrieval](use-context-engine-with-agents.md#troubleshoot-context-engine-retrieval).

## Appendix

Here is the full end-to-end Python script using the system prompt option from [Step 3](#step-3-create-the-agent):

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
all three. The server applies the space and permissions condition, so never add one to a query.
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

Additionally, take a look at the same script using the skill option from [Step 3](#step-3-create-the-agent):

:::{dropdown} demo_api_skill.py
```py
import os
from pathlib import Path

import httpx
from deepagents.backends import StateBackend
from deepagents.backends.utils import create_file_data
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

SKILL_PATH = Path(__file__).parent / "skills/context-engine-retrieval/SKILL.md"

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
    backend = StateBackend()
    skill_files = {
        "/skills/context-engine-retrieval/SKILL.md": create_file_data(
            SKILL_PATH.read_text()
        ),
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
    "deepagents>=0.7",  # needed for skills instead of system prompts and requires Python 3.11+
    "langchain>=1.4.0",
    "langchain-openai>=1.6.2",  # only needed for this example or if you want to use OpenAI or OpenRouter LLMs
]
```
