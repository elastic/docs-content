---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/testing-connectors.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Instructions for testing connectors to verify they work correctly before using them in rules.
---

# Test connectors [testing-connectors]

You can test connectors to verify they work correctly before using them in rules. In **{{stack-manage-app}}** > **{{connectors-ui}}**, navigate to the **Test** tab of the connector edit flyout or click **Save & test** when creating a new connector:

:::{image} /explore-analyze/images/kibana-connector-save-and-test.png
:alt: Rule management page with the errors banner
:screenshot:
:::

or by directly opening the proper connector edit flyout:

:::{image} /explore-analyze/images/kibana-email-connector-test.png
:alt: Rule management page with the errors banner
:screenshot:
:::

:::{image} /explore-analyze/images/kibana-teams-connector-test.png
:alt: Five clauses define the condition to detect
:screenshot:
:::

## Troubleshooting connectors with the `kbn-action` tool [_troubleshooting_connectors_with_the_kbn_action_tool]
```{applies_to}
stack: preview
serverless: preview
```

You can run an email action via [kbn-action](https://github.com/pmuellr/kbn-action). In this example, it is a Cloud hosted deployment of the {{stack}}:

```txt
$ npm -g install pmuellr/kbn-action

$ export KBN_URLBASE=https://elastic:<password>@<cloud-host>.us-east-1.aws.found.io:9243

$ kbn-action ls
[
    {
        "id": "a692dc89-15b9-4a3c-9e47-9fb6872e49ce",
        "actionTypeId": ".email",
        "name": "gmail",
        "config": {
            "from": "test@gmail.com",
            "host": "smtp.gmail.com",
            "port": 465,
            "secure": true,
            "service": null
        },
        "isPreconfigured": false,
        "isDeprecated": false,
        "referencedByCount": 0
    }
]
```

You can then run the following test:

```txt
$ kbn-action execute a692dc89-15b9-4a3c-9e47-9fb6872e49ce '{subject: "hallo", message: "hallo!", to:["test@yahoo.com"]}'
{
    "status": "ok",
    "data": {
        "accepted": [
            "test@yahoo.com"
        ],
        "rejected": [],
        "envelopeTime": 100,
        "messageTime": 955,
        "messageSize": 521,
        "response": "250 2.0.0 OK  1593144408 r5sm8625873qtc.20 - gsmtp",
        "envelope": {
            "from": "test@gmail.com",
            "to": [
                "test@yahoo.com"
            ]
        },
        "messageId": "<cf9fec58-600f-64fb-5f66-6e55985b935d@gmail.com>"
    },
    "actionId": "a692dc89-15b9-4a3c-9e47-9fb6872e49ce"
}
```
