---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/xpack-security-access-agreement.html
applies_to:
  stack: all
products:
  - id: kibana
---

# {{kib}} access agreement [xpack-security-access-agreement]

Access agreement is a [subscription feature](https://www.elastic.co/subscriptions) that requires users to acknowledge and accept an agreement before accessing {{kib}}. The agreement text supports Markdown format and can be specified using the `xpack.security.authc.providers.<provider-type>.<provider-name>.accessAgreement.message` setting.

You can specify a default access agreement  using the `xpack.security.accessAgreement.message` setting. This message will be used for each provider who doesn’t specify an access agreement.

::::{note}
You need to acknowledge the access agreement only once per session, and {{kib}} reports the acknowledgement in the audit logs.

::::


Here is an example of defining an access agreement in [`kibana.yml`](/deploy-manage/stack-settings.md):

```yaml
xpack.security.authc.providers:
  basic.basic1:
    order: 0
    accessAgreement:
      message: |
        **You are accessing a system with sensitive information**

        By logging in, you acknowledge that information system usage
        ...(shortened)
```

When you authenticate using `basic.basic1`, you’ll see the following agreement that you must acknowledge before you can access {{kib}}:

:::{image} /deploy-manage/images/kibana-access-agreement.png
:alt: Access Agreement UI
:screenshot:
:::

