---
applies_to:
  serverless:
products:
  - id: cloud-serverless
navigation_title: Serverless FAQ
---

# Frequently asked questions (FAQ) about {{serverless-full}} projects [general-what-is-serverless-elastic-answers-to-common-serverless-questions]

The following FAQ addresses common questions about using {{serverless-full}} projects.

For information about upcoming features, refer to our [roadmap](https://github.com/orgs/elastic/projects/2066/views/2?filterQuery=&sliceBy%5Bvalue%5D=Serverless).

## Pricing and availability

**Q: Where can I learn about pricing for {{serverless-short}}?**  
A: See pricing information for [{{es-serverless}}](https://www.elastic.co/pricing/serverless-search), [{{es}} {{vectordb}}](https://cloud.elastic.co/pricing/serverless?s=vectordb), [{{observability}}](https://www.elastic.co/pricing/serverless-observability), and [{{sec-serverless}}](https://www.elastic.co/pricing/serverless-security).

**Q: What Cloud regions does {{serverless-full}} support?**  
A: {{serverless-full}} is available in select AWS, GCP, and Azure regions, with plans to expand to more regions. For more information, refer to [](/deploy-manage/deploy/elastic-cloud/regions.md).

## Data management

**Q: How can I move data to or from {{serverless-short}} projects?**  
A: You can [use Reindex from remote](/manage-data/migrate/migrate-data-using-reindex-api.md) as the preferred
option. You can also [use Logstash](logstash://reference/index.md) with {{es}} input and output plugins to move data to and from {{serverless-short}} projects.

**Q: Can I request backups or restores for my serverless projects?**  
A: On-demand project backups or restores are currently unavailable. 
User-initiated data recovery is anticipated in a future release. You can follow its progress by referring to the [public roadmap](https://github.com/elastic/roadmap/issues/228).

## Security, compliance, and access

**Q: How can I create {{serverless-full}} service accounts?**  
A: Create API keys for service accounts in your {{serverless-short}} projects. You can create them in {{kib}}, with the {{es}} API, or as code with Terraform. Refer to [](/deploy-manage/api-keys/serverless-project-api-keys.md) for details.

**Q: Can I configure {{es}} authentication realms (for example, native realm) in {{serverless-short}} projects?**  
A: No. {{serverless-short}} uses a different authentication model and does not support [{{es}} authentication realms](/deploy-manage/users-roles/cluster-or-deployment-auth/authentication-realms.md). Project-level access is handled through [Serverless project API keys](/deploy-manage/api-keys/serverless-project-api-keys.md), and user authentication is managed at the [{{ecloud}} organization level](/deploy-manage/users-roles/cloud-organization.md) (including SAML SSO).

**Q: What compliance and privacy standards does {{serverless-full}} adhere to?**  
A: Alongside the entire Elastic platform, {{serverless-full}} is independently audited and certified to meet industry-leading compliance and privacy standards. Refer to the [Elastic Trust Center](https://www.elastic.co/trust) for more information. Further details about specific standards are available on our [roadmap](https://www.elastic.co/cloud/serverless/roadmap).

**Q: What domains do I need to allow for browser access to {{kib}} in {{serverless-short}} projects?**  
A: In addition to the standard {{ecloud}} endpoints, ensure users can access `kibana.estccdn.com`, which is required to load {{kib}}. If this domain is blocked, {{kib}} might appear as a blank page. Refer to [Browser access requirements](/deploy-manage/deploy/elastic-cloud.md#browser-access) for more information.

## Project lifecycle and support

**Q: How does {{serverless-full}} ensure compatibility between software versions?**  
A: Connections and configurations are unaffected by upgrades. To ensure compatibility between software versions, quality testing and API versioning are used.

**Q: Can I convert a {{serverless-full}} project into an {{ech}} deployment, or a hosted deployment into a {{serverless-short}} project?**  
A: No, you cannot convert, because projects and deployments are based on different architectures.

**Q: Can I convert a {{serverless-short}} project into a project of a different type?**  
A: No, you cannot convert your project to a different project type, but you can create as many projects as you’d like.

**Q: How do I raise a support case for {{serverless-full}}?**  
A: Raise a case for your subscription as you do today. In the body of the case, mention you are working with a {{serverless-short}} project to ensure appropriate support.

**Q: Why does the `GET /` root API return a version number that differs from the current Elasticsearch release?**

:::{include} /deploy-manage/deploy/_snippets/serverless-version-reporting.md
:::
