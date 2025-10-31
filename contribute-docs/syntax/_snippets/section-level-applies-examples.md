:::::{dropdown} Applicable to Stack and Serverless, minus a section

````markdown
--- 
applies_to:
stack: ga
serverless: ga
---

# Spaces

[...]

#### Configure a space-level landing page [space-landing-page]
```{applies_to}
serverless: unavailable
```
````
:::::

:::::{dropdown} Applicable to all deployment types, but some paragraphs are specific to other deployment types

````markdown
#### Cloud organization level security [cloud-organization-level]
```{applies_to}
serverless: ga
deployment:
  ess: ga
```

[...]

#### Orchestrator level security [orchestrator-level]
```{applies_to}
deployment:
  ece: ga
```

[...]
````
:::::