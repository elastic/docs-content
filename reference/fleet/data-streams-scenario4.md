---
navigation_title: Scenario 4
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/data-streams-scenario4.html
products:
  - id: fleet
  - id: elastic-agent
applies_to:
  stack: ga 9.1
  serverless: ga
---

# Scenario 4: Apply an ILM policy to all data streams in a custom integration [data-streams-scenario4]

If you’ve created a custom integration package, you can apply a single ILM policy to all its data streams using a shared `@custom` component template. This eliminates the need to configure each data stream individually.

## Step 1: Define the ILM policy [data-streams-scenario4-step1]

1. In {{kib}}, go to the **Index Lifecycle Policies** management page. You can also use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create policy**.
3. Name the policy, configure it as needed, and click **Save policy**.

## Step 2: Create a custom component template [data-streams-scenario4-step2]

Create a custom component template named `<integration>@custom`, replacing `<integration>` with your package name.

For example, for a Docker integration, use:

```json
PUT _component_template/docker@custom
{
  "template": {
    "settings": {
      "index": {
        "lifecycle": {
          "name": "docker-ilm-policy"
        }
      }
    },
    "mappings": {
      "properties":
      }
    }
  }
}
```

## Step 3: Deploy or update the integration [data-streams-scenario4-step3]

The `@custom` component template is automatically included when the package is installed or updated.

To apply the ILM policy:

- Bump the version of your custom package.

- Reinstall or upgrade the package using the {{fleet}} UI or Developer Console.

After the ILM policy from `docker` has been deployed, it applies to all data streams in the package.