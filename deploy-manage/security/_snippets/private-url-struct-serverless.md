Use the following URL structure. Take the alias and product from your project's endpoint, then combine them with the private hosted zone domain name that you registered.

  ```
  https://{{alias}}.{{product}}.{{private_hosted_zone_domain_name}}
  ```

  For example:

  ```text subs=true
  https://my-project-d53192.es.{{example-serverless-phz-dn}}
  ```

You can also copy the **Private endpoint** URL directly from your project overview in the {{ecloud}} Console.

:::{tip}
{{serverless-full}} supports port 443.

You can also connect using the project ID, for example, https://6b111580caaa4a9e84b18ec7c600155e.{{example-serverless-phz-dn}}.
:::
