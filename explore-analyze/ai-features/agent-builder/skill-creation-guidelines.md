---
navigation_title: "Skill creation guidelines"
description: "Guidelines for creating effective custom skills in Elastic Agent Builder."
applies_to:
  stack: ga 9.4+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Write effective custom skills in {{agent-builder}}

[Custom skills](custom-skills.md) give your agents consistent, reusable expertise for specific task domains. The quality of a skill depends almost entirely on how well its instructions are written. This guide covers how to write instructions that help the agent select the right skill, follow the right steps, and handle edge cases gracefully.

## Skill authoring checklist

Use this checklist when creating or updating a skill:

- [Decide where to put your instructions](#decide-where-to-put-your-instructions)
- [Write a clear description](#write-a-clear-description)
  - [Make descriptions semantically distinct](#make-descriptions-semantically-distinct)
- [Structure the instructions](#structure-the-instructions)
  - [Start with trigger conditions](#start-with-trigger-conditions)
  - [Write detailed core instructions](#write-detailed-core-instructions)
  - [Add realistic examples](#add-realistic-examples)
  - [Document edge cases](#document-edge-cases)
- [Use referenced content](#use-referenced-content)
- [Scope each skill to one task](#scope-each-skill-to-one-task)
- [Assign only relevant tools](#assign-only-relevant-tools)
- [Test your skill](#test-your-skill)

## Decide where to put your instructions

The agent's system prompt is always in context. Skill instructions are only loaded when the agent decides the skill is relevant. This distinction should guide what you put where.

### Use a skill

Use a skill when instructions are task-specific or complex enough to warrant their own context:

- Instructions only apply to certain tasks, not all tasks the agent handles.
- Instructions are too detailed or domain-specific to include in the system prompt without cluttering it.
- You want the same expertise reused across multiple agents.
- The task complexity justifies its own documentation, for example when there are ten or more specific considerations.
- You need tools that should only be available for a particular task type.

### Use the system prompt

Keep instructions in the system prompt when they are general and should always apply:

- The behavior is core to the agent's identity or should apply to every response.
- Instructions are short, general, and always relevant.

For one-off requirements specific to a single interaction, use direct instructions in the conversation instead. There is no need to encode them in a skill or system prompt.

:::{tip}
For broader guidance on writing custom instructions, tool descriptions, and chat prompts, refer to [Best practices for prompt engineering](prompt-engineering.md).
:::

## Write a clear description

The description is the primary signal the agent uses to decide whether to load a skill. It is always included in context, whereas the skill's full instructions are only read once the skill is selected. A vague description means the agent might load the wrong skill, or none.

A good description explains what the skill does and explicitly states when to use it. Keep it concise: the description has a 1024-character limit, and every word should be useful for routing.

✅ **Good**

```markdown
Find security alerts related to an original alert by analyzing common IOCs,
affected assets, attack patterns, and temporal proximity.  # <1>
Use when investigating an alert to understand the broader attack context.  # <2>
```
1. Describes what the skill does with enough specificity to distinguish it from similar skills.
2. States an explicit trigger condition so the agent knows when to load it.

❌ **Too vague**

```markdown
"How to find alerts"  # <1>
"Security"            # <2>
```
1. No explanation of what the skill does or when to use it.
2. Gives the agent no actionable guidance on when or how to use the skill.

### Make descriptions semantically distinct

If you have multiple skills that cover related areas, make sure their descriptions are semantically distinct. If two descriptions are similar, the agent will struggle to choose between them. Merge overlapping skills or sharpen the language until the difference is clear.

## Structure the instructions

The instructions field contains the full skill content, written in Markdown. The agent reads this content only after deciding the skill is relevant, so you have room to be thorough. Structure matters: a well-organized skill helps the agent confirm it loaded the right one and follow your intent precisely.

### Start with trigger conditions

Open the instructions with an explicit section that tells the agent when this skill applies. Even though the description already handled routing, restating trigger conditions inside the content helps the agent confirm it is in the right place and makes the skill self-documenting.

```markdown
## When to Use This Skill  # <1>

Use this skill when:
- A user asks to investigate a security alert  # <2>
- A user wants to understand if an alert is isolated or part of a broader attack
- A user asks "are there related alerts" or "what else happened around this time"
- You need to correlate multiple security events
```
1. Name the section clearly so the skill is self-documenting.
2. Phrase trigger conditions as specific user queries or task types, not abstract categories.

:::{tip}
Avoid vague openings like "This skill helps with alerts." Be specific about the exact situations this skill should handle.
:::

### Write detailed core instructions

The core instructions are where you control how the agent behaves. Be precise. Vague or short instructions produce inconsistent results: the agent will fill in the gaps where you have not given explicit guidance.

Step-by-step format works well for procedural tasks:

```markdown
## Finding Related Alerts

1. **Extract key indicators from the original alert:**  # <1>
   - IP addresses involved
   - User accounts affected
   - Timestamps (a window of ±2 hours is a good starting point)
   - Attack signatures or IOCs
   - Affected assets and hostnames

2. **Query for related alerts using these criteria:**  # <2>
   - Same source or destination IP within 24 hours
   - Same user account across different alert types
   - Same malware hash or signature
   - Alerts on the same asset within a short timeframe

3. **Present findings with context:**  # <3>
   - Group related alerts by common indicators
   - Explain the relationship between alerts
   - Highlight the timeline of events
   - Note if the pattern suggests a coordinated attack
```
1. Gather data before querying so the agent has concrete values to search with.
2. Use specific, measurable criteria rather than vague descriptions.
3. Tell the agent what format to present results in, not only what to find.

:::{tip}
If you find yourself writing instructions for two distinct workflows, that is a signal to [split the skill](#scope-each-skill-to-one-task).
:::

### Add realistic examples

Concrete examples improve the agent's ability to apply instructions correctly. Show realistic inputs and the expected output or reasoning process, with enough detail to be unambiguous.

```markdown
## Example: IP-based Correlation  # <1>

User query: "Investigate alert ALT-2024-001 for related activity"  # <2>

Original alert: Failed login from IP 192.0.2.45 to server WEB-01

Steps taken:
1. Search for other alerts involving 192.0.2.45
2. Search for other alerts on WEB-01
3. Check for alerts within ±2 hours of the original timestamp

Found related alerts:  # <3>
- ALT-2024-002: Port scan from 192.0.2.45 (10 minutes earlier)
- ALT-2024-003: SQL injection attempt on WEB-01 (15 minutes later)
```
1. Name examples descriptively so the agent can reference the right one.
2. Include a realistic user query to anchor the example in context.
3. Show the expected output format alongside the steps.

Add examples when the task involves nuanced logic or when the expected output format matters.

### Document edge cases

Tell the agent what to do when things go wrong. Without explicit guidance, the agent will improvise and might produce confusing or unhelpful responses.

```markdown
## Edge Cases

- **No related alerts found:** Inform the user that the alert appears isolated, and explain what was searched.  # <1>
- **Too many related alerts:** Group by type and show summary statistics rather than listing all results.  # <2>
- **Partial data available:** Work with available indicators and note which data points are missing.
- **Ambiguous relationships:** Present possible connections with confidence levels rather than asserting a definitive link.  # <3>
```
1. Tell the agent what to say, not only what to avoid doing.
2. Define fallback behavior for overwhelming result sets.
3. Instruct the agent to signal uncertainty rather than assert conclusions.

## Use referenced content

The `referenced_content` API field lets you attach named content blocks to a skill. The agent can choose which blocks to read based on what the task requires, rather than loading everything at once. This is useful when parts of your skill instructions only apply under specific conditions.

Good candidates for referenced content include:
- API specifications that are lengthy or change frequently.
- Large sets of example queries that would clutter the main instructions.
- Lookup tables, error codes, or reference data the agent might need to consult.
- Condition-specific guidance, such as separate blocks for Linux, macOS, and Windows behavior within the same skill.

Reference the content blocks by name inside your main instructions so the agent knows they exist and when to read them:

```markdown
## Log Triage Process

For example ES|QL queries, see `./queries`.  # <1>
For OS-specific behavior, see `./linux`, `./macos`, or `./windows`.  # <2>
```
1. Point to named content blocks by relative path so the agent knows where to find them.
2. Use topic-based names so the agent can select the most relevant block for the task.

Keep the depth of referenced content shallow. Nesting blocks more than two levels deep makes the structure harder to follow.

For an example of creating a skill with `referenced_content`, refer to [Skills APIs](kibana-api.md#skills-apis).

## Scope each skill to one task

Each skill should do one thing well. A focused skill is easier for the agent to apply correctly and easier for you to maintain. If you find yourself writing instructions that cover two distinct workflows, split them into two skills with separate descriptions.

## Assign only relevant tools

Each skill can specify which tools it has access to. Assign only the tools that are directly relevant to the skill's task. Providing unnecessary tools increases the risk that the agent calls the wrong one.

Apply the same principle to tools: prefer a tool that does one thing well over a wrapper that combines multiple operations.

Describe how to use the available tools within your instructions so the agent knows when to reach for each one.

## Test your skill

After saving, assign the skill to an agent and test it with realistic queries. Check that the agent selects the skill when expected, follows the steps correctly, and handles the edge cases you documented. Revise the description or instructions based on what you observe.

## Next steps

- [Create a custom skill](custom-skills.md) and add it to your skill library.
- Review the [built-in skills](builtin-skills-reference.md) for examples of how Elastic structures skill descriptions and instructions.
- Explore [prompt engineering best practices](prompt-engineering.md) for broader guidance on writing custom instructions, tool descriptions, and chat prompts.

## Related pages

- [Skills in {{agent-builder}}](skills.md)
- [Skills APIs](kibana-api.md#skills-apis)
