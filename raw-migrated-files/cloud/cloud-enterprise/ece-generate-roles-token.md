# Generate roles tokens [ece-generate-roles-token]

At the end of the Elastic Cloud Enterprise installation process on the first host, you are provided with a roles token. This token can be used to install Elastic Cloud Enterprise on additional hosts, but it does not include any role permissions. [Roles can be assigned](../../../deploy-manage/deploy/cloud-enterprise/assign-roles-to-hosts.md) to the additional hosts through the Cloud UI later on, but this role assignment is a manual process. For automation purposes, you need to generate a new ephemeral or persistent token with the right role permissions, so that you can install Elastic Cloud Enterprise on hosts and add the right roles at the same time.

Ephemeral and persistent tokens differ as follows:

Ephemeral token
:   Available for use during Elastic Cloud Enterprise installation on additional hosts for one hour before the token is revoked automatically. Cannot be revoked manually.

Persistent token
:   Available for use during Elastic Cloud Enterprise installation on additional hosts indefinitely. [Can be revoked](../../../deploy-manage/deploy/cloud-enterprise/generate-roles-tokens.md) at any time.

The permitted roles are the same as those you can [assign in the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/assign-roles-to-hosts.md):

`allocator`
:   Allocates the available computing resources to Elasticsearch nodes or Kibana instances. In larger installations, a majority of the machines will be allocators.

`coordinator`
:   Serves as a distributed coordination system and resource scheduler.

`proxy`
:   Manages communication between a user and an Elasticsearch or Kibana instance.

`director`
:   Manages the ZooKeeper datastore. This role is typically shared with the coordinator role. In production deployments it can be separated from a coordinator.

To generate an ephemeral token for additional allocators:

```sh
curl -H 'Content-Type: application/json' -u USER:PASSWORD https://COORDINATOR_HOST_IP:12443/api/v1/platform/configuration/security/enrollment-tokens -d '{ "persistent": false, "roles": [ "allocator"] }'
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0Njk3N2I3ZC1hM2U2LTQ2MDUtYjcwZC0xNzIzMTI5YWY4ZTQiLCJyb2xlcyI6WyJwcm94eSIsImFsbG9jYXRvciJdLCJpc3MiOiJib290c3RyYXAtaW5pdGlhbCIsImV4cCI6MTQ5MzY0NjIxM30.xsaRb72CsNMuXKy6Y-PJgqLc0qmjCljlB4Smcx_MRxg"
}
```

To generate a persistent token for additional allocators:

```sh
curl -H 'Content-Type: application/json' -u USER:PASSWORD https://COORDINATOR_HOST_IP:12443/api/v1/platform/configuration/security/enrollment-tokens -d '{ "persistent": true, "roles": [ "allocator"] }'
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0Yzg5OTBkZi0xZmI3LTQ4MjAtYjg2OC02YmM5ZTg4NjA4MTQiLCJyb2xlcyI6WyJwcm94eSIsImFsbG9jYXRvciJdLCJpc3MiOiJib290c3RyYXAtaW5pdGlhbCJ9.mfTkO4j8uZJ-qwB2jmBuMScyYfLmcJpvKgSTLx2WV24",
  "token_id": "4c8990df-1fb7-4820-b868-6bc9e8860814"
}
```

