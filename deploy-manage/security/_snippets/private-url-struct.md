Use the following URL structure. This URL is built from endpoint information retrieved from your Elastic deployment and the private hosted zone domain name that you registered.

  ```
  https://{{alias}}.{{product}}.{{private_hosted_zone_domain_name}}
  ```

  For example:

  ```text subs=true
  https://my-deployment-d53192.es.{{example-phz-dn}}
  ```


:::{tip}
You can use either 443 or 9243 as a port.

You can also connect to the cluster using the {{es}} cluster ID, for example, https://6b111580caaa4a9e84b18ec7c600155e.{{example-phz-dn}}
:::