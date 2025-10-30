# Automated settings reference

Elastic Docs V3 supports the ability to build a markdown settings reference from a YAML source file.

### Syntax

```markdown
:::{settings} /syntax/kibana-alerting-action-settings.yml
:::
```

### Example

```yaml
groups:
  - group: Group name
    id: Link ID
    settings:
      - setting: Setting name
        default: Default value
        platform: Supported platforms
        description: |
          A multi-line description with markdown support.
          More here.
        example: |
          A multi-line example with markdown support.
```

### Result

_Everything below this line is auto-generated._

:::{settings} /syntax/kibana-alerting-action-settings.yml
:::