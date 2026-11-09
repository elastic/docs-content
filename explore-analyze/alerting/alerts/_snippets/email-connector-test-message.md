:::{note}
:applies_to: {"serverless": "ga", "stack": "ga 9.5+"}
When you test an email connector, {{kib}} sends the fixed text `This is a test email from Kibana` instead of the `subject` and `message` you provide. The `to`, `cc`, and `bcc` recipients still apply. To send custom content, use the connector in a rule action. For details, refer to [Test connectors](kibana://reference/connectors-kibana/email-action-type.md#email-action-configuration) in the email connector reference.
:::
