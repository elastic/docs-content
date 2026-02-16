---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/security-spaces.html
  - https://www.elastic.co/guide/en/serverless/current/security-spaces.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Spaces and {{elastic-sec}} [security-spaces]

{{elastic-sec}} supports the organization of your security operations into logical instances with the [spaces](../../../deploy-manage/manage-spaces.md) feature. Each space in {{kib}} represents a separate logical instance of {{elastic-sec}} in which detection rules, rule exceptions, value lists, alerts, Timelines, cases, and {{kib}} advanced settings are private to the space and accessible only by users that have role privileges to access the space. 

For example, if you create a `SOC_prod` space in which you load and activate all the {{elastic-sec}} prebuilt detection rules, these rules and any detection alerts they generate will be accessible only when visiting the {{security-app}} in the `SOC_prod` space. If you then create a new `SOC_dev` space, you’ll notice that no detection rules or alerts are present. Any rules subsequently loaded or created here will be private to the `SOC_dev` space, and they will run independently of those in the `SOC_prod` space.

::::{note}
{applies_to}`stack: ga 9.1` You can fine-tune which {{elastic-defend}} policies and artifacts are accessible from particular spaces. For example, you can control which of your hosts running {{elastic-defend}} appear in a particular space by using {{fleet}} to assign {{agent}} policies to specific spaces. {{elastic-defend}} artifacts associated with those policies will also appear in the designated spaces. To learn more, refer to [Spaces and {{elastic-sec}}](spaces-defend-faq.md).
::::

::::{note}
By default, alerts created by detection rules are stored in {{es}} indices under the `.alerts-security.alerts-<space-name>` index pattern, and they may be accessed by any user with role privileges to access those {{es}} indices. In our example above, any user with {{es}} privileges to access `.alerts-security.alerts-SOC_prod` will be able to view `SOC_prod` alerts from within {{es}} and other {{kib}} apps such as Discover.

To ensure that detection alert data remains private to the space in which it was created, ensure that the roles assigned to your {{elastic-sec}} users include {{es}} privileges that limit their access to alerts within their space’s alerts index.

::::
