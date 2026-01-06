---
description: "Guidelines for writing effective tutorials in the Elastic documentation."
---

# Tutorials

This page provides guidelines for writing effective tutorials in the Elastic docs. This page and its associated template can be used by humans and LLMs to draft new tutorials, or to evaluate existing pages.

Use this page to:

- Draft a new tutorial by copying and pasting the [template](https://github.com/elastic/docs-content/blob/main/contribute-docs/content-types/_snippets/templates/tutorial-template.md)
- Understand the structure and best practices for tutorials before you write one
- Evaluate existing tutorials or drafts against the standards outlined here

Whether you're a regular contributor or reviewing someone else's work, these guidelines help ensure consistency, completeness, and quality across the Elastic documentation.

## What is a tutorial

A tutorial is a comprehensive, hands-on learning experience that guides users through completing a meaningful task from start to finish. You can think of a tutorial as a chain of related [how-to guides](/contribute-docs/content-types/how-tos.md), with additional explanatory context to help users learn as they work.

Ideally, users can complete a tutorial without needing to jump to other guides. Of course, this is more of an art than a science, and it's important to balance the need for background context with overall readability. If you find yourself needing to write a lot of background context, consider writing multiple, more focused tutorials.

Tutorials include three essential components:

- Clear **learning objectives** that describe what users will be able to do by the end
- **Prerequisites and setup** needed before starting
- A sequence of **instructional steps** that build on each other to accomplish a larger goal

::::{include} /contribute-docs/content-types/_snippets/how-to-tutorial-disambiguation-note.md
::::

## Structure of a tutorial

To help users successfully complete the learning experience, tutorials use a consistent structure. A predictable format helps users understand what they'll learn, what's required, and what they'll achieve.

### Required elements

Every tutorial must include the following elements:

1. A consistent **filename:** Use descriptive patterns like `*-tutorial.md`.
   - For example: `ingest-pipeline-tutorial.md`

2. Appropriate **[frontmatter](https://elastic.github.io/docs-builder/syntax/frontmatter/):**
   - `applies_to:` [Tags](https://elastic.github.io/docs-builder/syntax/applies) for versioning/availability info per the [cumulative docs guidelines](/contribute-docs/how-to/cumulative-docs/index.md)
   - `description`: A brief summary of what users will learn
   - `product`: The relevant Elastic product(s) used in the tutorial
% TODO once we have structured types     - The `type` field set to `tutorial`

3. A clear **title:** A descriptive title that indicates what users will learn or accomplish
   - For example, "Build an ingest pipeline with processors"

4. An **overview:** Explain what the tutorial teaches, who it's for, and what users will be able to do by the end. Include:
   - A brief description of what users will learn
   - The intended audience and their expected skill level
   - Learning objectives as a bulleted list

5. A **before you begin** section: List all prerequisites including:
   - Required prior knowledge or skills
   - Software, hardware, or access requirements
   - Data sets or environments to set up
   - Estimated time to complete (optional but helpful)

6. **Instructional steps:** Organize the tutorial into logical sections, each with a descriptive heading. Use numbered steps that begin with imperative verbs.
   :::{tip}
   Use the [stepper component](https://elastic.github.io/docs-builder/syntax/stepper/) for visual flow, or add subheadings to break complex steps into subsections.
   :::

7. **Checkpoints and results:** After significant steps, show users what they should see or what state their system should be in.

8. **[Code annotations](https://elastic.github.io/docs-builder/syntax/code/#code-callouts):** Explain important lines within code blocks to help users understand the code. Annotations can help reduce the need for extra text in the body of the tutorial, keeping the tutorial concise and focused. This makes it easier for a reader to simply run through the steps in a hurry.

9. **Next steps:** Suggest follow-up tutorials, related features to explore, or ways to expand on what they built.

10. **Related pages:** Links to related documentation such as conceptual topics, reference material, how-to guides, or troubleshooting resources.

### Optional elements

Include the following when they add value:

- **[Screenshots](https://elastic.github.io/docs-builder/syntax/images/#screenshots):** Add visual aids for UI-based steps when they improve clarity. Use screenshots sparingly as they require maintenance.
- **Explanatory callouts:** Use [admonitions](https://elastic.github.io/docs-builder/syntax/admonitions/) to provide extra context, troubleshooting tips, or explanations without interrupting the main flow.
- **Time estimates:** Indicate how long each major section or the overall tutorial takes to complete.
- A **summary:** Recap what users learned and accomplished in the tutorial. Reinforce the key learning objectives.
% TODO: reviewer I've made the summary optional, because if the overview already lists learning objectives clearly, a summary that just repeats them feels redundant. The tutorial's value is in the journey, not bookending it with the repetive information. 🤺

## Best practices

When you create tutorials, follow these best practices:

- **Focus on learning outcomes:** State what users will be able to do and the value they'll gain. Learning objectives should be clear, achievable, and relevant to real-world tasks.
- **Choose your tutorial approach:** Tutorials can be feature-focused or scenario-driven. Both are valid. Refer to [examples](#examples) for inspiration.
  - **Feature-focused:** Explore features or functionality (useful for deep dives into specific feature sets)
  - **Scenario-driven:** Work through a real-world use case (useful for demonstrating end-to-end solutions)
- **Gradually introduce complexity:** Start with simple concepts and use progressive disclosure. Each step should build on the previous steps.
- **Provide context when needed:** Unlike how-to guides, tutorials benefit from explanations of *why* something works or why a particular approach is recommended. That said, it's important to keep the tutorial as concise and focused as possible. Err on the side of brevity.
- **Use realistic examples:** Create examples that mirror real-world scenarios users will meet where possible.
- **Guide the learner:** Assume users are new to the feature or workflow. Provide encouragement and explain what they're accomplishing at key milestones.
- **Include checkpoints:** Add verification steps throughout so users can confirm they're on the right track before continuing.
- **Test your tutorial:** Authors and reviewers should complete the entire tutorial from scratch to identify gaps, errors, or unclear instructions.
  :::{tip}
  Have someone unfamiliar with the feature try your tutorial. They'll find every gap and unclear step!
  :::

## Template

To get started writing a new tutorial, use the [template](https://github.com/elastic/docs-content/blob/main/contribute-docs/content-types/_snippets/templates/tutorial-template.md).

## Examples

Here are some examples of well-structured tutorials in the Elastic documentation:

- [Tutorial: Threat hunting with {{esql}}](/solutions/security/esql-for-security/esql-threat-hunting-tutorial.md): A **scenario-driven** tutorial that teaches {{esql}} through a realistic cybersecurity scenario, with extensive code annotations.
- [{{esql}} for search tutorial](elasticsearch://reference/query-languages/esql/esql-search-tutorial.md): A **feature-focused** tutorial that systematically teaches search concepts using {{esql}}, from basic text matching to AI-powered semantic search, with subsections breaking down complex topics.

% TODO: Add links to 2-3 exemplary tutorials in the docs
