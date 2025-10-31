# Code

Code blocks can be used to display multiple lines of code. They preserve formatting and provide syntax highlighting when possible.

## Code block

Start and end a code block with a code fence. A code fence is a sequence of at least three consecutive backtick characters `` ``` ``. You can optionally add a language identifier to enable syntax highlighting.


::::{tab-set}

:::{tab-item} Output

```yaml
project:
  title: MyST Markdown
  github: https://github.com/jupyter-book/mystmd
```

:::

:::{tab-item} Markdown

````markdown
```yaml
project:
  title: MyST Markdown
  github: https://github.com/jupyter-book/mystmd
```
````

:::

::::

### Code callouts

There are two ways to add callouts to a code block. When using callouts, you must use one callout format. You cannot combine explicit and magic callouts.

#### Explicit callouts

Add `<\d+>` to the end of a line to explicitly create a code callout.

An ordered list with the same number of items as callouts must follow the code block. If the number of list items doesn’t match the callouts, docs-builder will throw an error.


::::{tab-set}

:::{tab-item} Output

```yaml
project:
  license:
    content: CC-BY-4.0 <1>
```

1. The license

:::

:::{tab-item} Markdown

````markdown
```yaml
project:
  license:
    content: CC-BY-4.0 <1>
```

1. The license
````

:::

::::

You can also have one block element in between the code block and the callout list:

::::{tab-set}

:::{tab-item} Output

```javascript
var input1 = "World"; // <1>
var input2 = "Elastic"; // <2>

function render(input) {
    return `Hello, ${input}!`;
}

render(input1);
render(input2);
```

**Inputs:**

1. `World`
2. `Elastic`

**Outputs**:

1. `Hello, World!`
2. `Hello, Elastic!`

:::


:::{tab-item} Markdown

````markdown
```javascript
var input1 = "World"; // <1>
var input2 = "Elastic"; // <2>

function render(input) {
    return `Hello, ${input}!`;
}

render(input1);
render(input2);
```

**Inputs:**

1. `World`
2. `Elastic`

**Outputs**:

1. `Hello, World!`
2. `Hello, Elastic!`
````

:::

::::

#### Automatic callouts

If a code block contains code comments in the form of `//` or `#`, callouts are automatically created.


::::{tab-set}

:::{tab-item} Output

```csharp
var apiKey = new ApiKey("<API_KEY>"); // Set up the api key
var client = new ElasticsearchClient("<CLOUD_ID>", apiKey);
```

:::

:::{tab-item} Markdown

````markdown
```csharp
var apiKey = new ApiKey("<API_KEY>"); // Set up the api key
var client = new ElasticsearchClient("<CLOUD_ID>", apiKey);
```
````
:::


::::

Code comments must follow code to be hoisted as a callout. For example:

::::{tab-set}

:::{tab-item} Output

```csharp
// THIS IS NOT A CALLOUT
var apiKey = new ApiKey("<API_KEY>"); // This is a callout
var client = new ElasticsearchClient("<CLOUD_ID>", apiKey);
```

:::

:::{tab-item} Markdown

````markdown
```csharp
// THIS IS NOT A CALLOUT
var apiKey = new ApiKey("<API_KEY>"); // This is a callout
var client = new ElasticsearchClient("<CLOUD_ID>", apiKey);
```
````

:::

::::

#### Align callouts

You can align callouts with spaces.

::::{tab-set}

:::{tab-item} Output

```yaml
foo: 1       <1>
barbar: 2    <2>
bazbazbaz: 3 <3>
```

1. Foo
2. Bar
3. Baz

:::

:::{tab-item} Markdown
````markdown
```yaml
foo: 1       <1>
barbar: 2    <2>
bazbazbaz: 3 <3>
```

1. Foo
2. Bar
3. Baz
````
:::

::::

#### Turn off callouts

You can turn off callouts by adding a code block argument `callouts=false`.

::::{tab-set}

:::{tab-item} Output

```yaml callouts=false
project:
  license:
    content: CC-BY-4.0 <1>
```

1. The license

:::

:::{tab-item} Markdown

````markdown
```yaml callouts=false
project:
  license:
    content: CC-BY-4.0 <1>
```

1. The license
````

:::

::::

### Console code blocks

We document a lot of API endpoints at Elastic. For these endpoints, we support `console` as a language. The term console relates to the dev console in kibana which users can link to directly from these code snippets.

In a console code block, the first line is highlighted as a dev console string and the remainder as json:

::::{tab-set}

:::{tab-item} Output

```console
POST _reindex
{
  "source": {
    "remote": {
      "host": "<OTHER_HOST_URL>",
      "username": "user",
      "password": "pass"
    },
    "index": "my-index-000001",
    "query": {
      "match": {
        "test": "data"
      }
    }
  },
  "dest": {
    "index": "my-new-index-000001"
  }
}
```


:::

:::{tab-item} Markdown

````markdown
```console
POST _reindex
{
  "source": {
    "remote": {
      "host": "<OTHER_HOST_URL>",
      "username": "user",
      "password": "pass"
    },
    "index": "my-index-000001",
    "query": {
      "match": {
        "test": "data"
      }
    }
  },
  "dest": {
    "index": "my-new-index-000001"
  }
}
```
````

:::

::::

Console code blocks now support multiple API calls within a single code block. When you have multiple console commands, they are displayed as separate sections within the same block with proper visual separation:

::::{tab-set}

:::{tab-item} Output

```console
GET /mydocuments/_search
{
    "from": 1,
    "query": {
        "match_all" {}
    }
}

POST /mydocuments/_doc
{
    "title": "New Document",
    "content": "This is a sample document"
}
```

:::

:::{tab-item} Markdown

````markdown
```console
GET /mydocuments/_search
{
    "from": 1,
    "query": {
        "match_all" {}
    }
}

POST /mydocuments/_doc
{
    "title": "New Document",
    "content": "This is a sample document"
}
```
````

:::

::::

### Code block substitutions

You can use substitutions to insert reusable values into your code block examples.
Check the [code blocks substitutions syntax](./substitutions.md#code-blocks) for more information.

## Inline code

Use backticks to create an inline code span.
Inline code spans are useful for short code snippets or variable names.


### Inline code in a paragraph

::::{tab-set}

:::{tab-item} Output

This `code` is inline.

:::

:::{tab-item} Markdown

````markdown
This `code` is inline.
````
:::

::::

### Inline code in a heading

::::{tab-set}

:::{tab-item} Output

## This `code` is in a heading.

:::

:::{tab-item} Markdown

````markdown
## This `code` is in a heading.
````
:::

::::

## Supported languages

Refer to [hljs.ts](https://github.com/elastic/docs-builder/blob/main/src/Elastic.Documentation.Site/Assets/hljs.ts)
for a complete list of supported languages.
