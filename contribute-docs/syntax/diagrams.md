# Diagrams

The `diagram` directive allows you to render various types of diagrams using the [Kroki](https://kroki.io/) service. Kroki supports many diagram types including Mermaid, D2, Graphviz, PlantUML, and more.

## Basic usage

The basic syntax for the diagram directive is:

```markdown
::::{diagram} [diagram-type]
<diagram content>
::::
```

If no diagram type is specified, it defaults to `mermaid`.

## Supported diagram types

The diagram directive supports the following diagram types:

- `mermaid` - Mermaid diagrams (default)
- `d2` - D2 diagrams
- `graphviz` - Graphviz/DOT diagrams
- `plantuml` - PlantUML diagrams
- `ditaa` - Ditaa diagrams
- `erd` - Entity Relationship diagrams
- `excalidraw` - Excalidraw diagrams
- `nomnoml` - Nomnoml diagrams
- `pikchr` - Pikchr diagrams
- `structurizr` - Structurizr diagrams
- `svgbob` - Svgbob diagrams
- `vega` - Vega diagrams
- `vegalite` - Vega-Lite diagrams
- `wavedrom` - WaveDrom diagrams

## Examples

### Mermaid flowchart (default)

::::::{tab-set}

:::::{tab-item} Source
```markdown
::::{diagram}
flowchart LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
::::
```
:::::

:::::{tab-item} Rendered
::::{diagram}
flowchart LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
::::
:::::

::::::

### Mermaid sequence diagram

::::::{tab-set}

:::::{tab-item} Source
```markdown
::::{diagram} mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello Bob, how are you?
    B-->>A: Great!
::::
```
:::::

:::::{tab-item} Rendered
::::{diagram} mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello Bob, how are you?
    B-->>A: Great!
::::
:::::

::::::

### D2 diagram

::::::{tab-set}

:::::{tab-item} Source
```markdown
::::{diagram} d2
x -> y: hello world
y -> z: nice to meet you
::::
```
:::::

:::::{tab-item} Rendered
::::{diagram} d2
x -> y: hello world
y -> z: nice to meet you
::::
:::::

::::::

### Graphviz diagram

::::::{tab-set}

:::::{tab-item} Source
```markdown
::::{diagram} graphviz
digraph G {
    rankdir=LR;
    A -> B -> C;
    A -> C;
}
::::
```
:::::

:::::{tab-item} Rendered
::::{diagram} graphviz
digraph G {
    rankdir=LR;
    A -> B -> C;
    A -> C;
}
::::
:::::

::::::

## Error handling

If the diagram content is empty or the encoding fails, an error message will be displayed instead of the diagram.
