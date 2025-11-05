If a change is released in Serverless and will be released in a future version of the {{stack}}, you can add both a `serverless` and `stack` tag, indicating the version of the {{stack}} in which the feature will be released:

```
---
applies_to:
  serverless: ga
  stack: ga 9.2
---
```

Because these changes need to be published as soon as the feature is released in Serverless, you might need to publish your docs before the feature is available in the {{stack}}. To allow for this, Docs V3 [displays badges differently](/contribute-docs/how-to/cumulative-docs/index.md#how-do-these-tags-behave-in-the-output) when the `applies_to` tag specifies a product version that has not yet been released to customers.

* A feature is tagged as available in a current Serverless release and a future {{stack}} version will render the following badges:

    {applies_to}`serverless: ga`
    {applies_to}`stack: ga 99.99`

* After the {{stack}} version is released, the same badges will render with the version number without any changes to the badge value in the source.

    {applies_to}`serverless: ga`
    {applies_to}`stack: ga 9.0`