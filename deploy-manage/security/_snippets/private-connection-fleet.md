If you are using {{service-name}} together with Fleet, and enrolling the Elastic Agent with a private connection URL, you need to configure Fleet Server to use and propagate the {{service-name}} URL by updating the **Fleet Server hosts** field in the **Fleet settings** section of {{kib}}. Otherwise, Elastic Agent will reset to use a default address instead of the {{service-name}} URL. 

The URL needs to follow this pattern: 

```text
https://{{fleet_component_ID_or_deployment_alias}}.fleet.{{private_hosted_zone_domain_name}}:443`
```

Similarly, the {{es}} host needs to be updated to propagate the private connection URL. The {{es}} URL needs to follow this pattern: 

```text
https://{{elasticsearch_cluster_ID_or_deployment_alias}}.es.{{private_hosted_zone_domain_name}}:443
```

The settings `xpack.fleet.agents.fleet_server.hosts` and `xpack.fleet.outputs` that are needed to enable this configuration in {{kib}} are not available in the {{kib}} settings in {{ecloud}}.