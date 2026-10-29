:::{note}
:applies_to: {"serverless": "ga", "stack": "ga 9.5+"}
For an email connector, {{kib}} replaces the `subject` and `message` you send with the fixed text `This is a test email from Kibana`. The `to`, `cc`, and `bcc` recipients still apply. To send custom content, use the connector in a rule action. For details, refer to [Email connector and action](kibana://reference/connectors-kibana/email-action-type.md#email-action-configuration).
:::
