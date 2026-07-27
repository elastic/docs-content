Use the following URL structure. This URL is built from endpoint information retrieved from your Elastic deployment or project and the private hosted zone domain name that you registered.

  ```
  https://{{alias}}.{{product}}.{{private_hosted_zone_domain_name}}
  ```

  For example:

  ```text subs=true
  https://my-deployment-d53192.es.{{example-phz-dn}}
  ```


:::{tip}
{{ech}} supports ports 443 and 9243. {{serverless-full}} supports port 443.

You can also connect to the cluster using the {{es}} cluster or project ID, for example, https://6b111580caaa4a9e84b18ec7c600155e.{{example-phz-dn}}.
:::
