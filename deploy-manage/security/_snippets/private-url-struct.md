Use the following URL structure. Take the alias and product from your Elastic endpoint URL, then replace the public domain with the private hosted zone domain name that you registered.

  ```
  https://{{alias}}.{{product}}.{{private_hosted_zone_domain_name}}
  ```

  For example, if the public endpoint is:

  ```text subs=true
  https://my-deployment-d53192.es.{{example-default-dn}}
  ```

  the private connection URL is:

  ```text subs=true
  https://my-deployment-d53192.es.{{example-phz-dn}}
  ```


:::{tip}
{{ech}} supports ports 443 and 9243.

You can also connect to the cluster using the {{es}} cluster ID, for example, https://6b111580caaa4a9e84b18ec7c600155e.{{example-phz-dn}}.
:::
