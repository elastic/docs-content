---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-generate-roles-token.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-revoke-roles-token.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Manage roles tokens

At the end of the {{ece}} installation process on the first host, you are provided with a roles token. This token can be used to install {{ece}} on additional hosts, but it does not include any role permissions.

You can [assign roles](./assign-roles-to-hosts.md) to the additional hosts through the Cloud UI later on, but this role assignment is a manual process.

For automation purposes, you need to generate a new *ephemeral* or *persistent* token with the right role permissions, so that you can install {{ece}} on hosts and add the right roles at the same time.

This section covers the different types of tokens and the following tasks:

* [Generate roles tokens](#ece-generate-roles-token)
* [Revoke roles tokens](#ece-revoke-roles-token)

## Ephemeral and persistent roles tokens

Ephemeral and persistent tokens differ as follows:

Ephemeral token
:   Available for use during {{ece}} installation on additional hosts for one hour before the token is revoked automatically. Cannot be revoked manually.

Persistent token
:   Available for use during {{ece}} installation on additional hosts indefinitely. Can be revoked at any time.

The permitted roles are the same as those you can [assign in the Cloud UI](./assign-roles-to-hosts.md):

`allocator`
:   Allocates the available computing resources to {{es}} nodes or {{kib}} instances. In larger installations, a majority of the machines will be allocators.

`coordinator`
:   Serves as a distributed coordination system and resource scheduler.

`proxy`
:   Manages communication between a user and an {{es}} or {{kib}} instance.

`director`
:   Manages the ZooKeeper datastore. This role is typically shared with the coordinator role. In production deployments it can be separated from a coordinator.

## Generate roles tokens [ece-generate-roles-token]

To generate an ephemeral token for additional allocators:

```sh
curl -H 'Content-Type: application/json' -u USER:PASSWORD https://$COORDINATOR_HOST:12443/api/v1/platform/configuration/security/enrollment-tokens -d '{ "persistent": false, "roles": [ "allocator"] }'
```
```sh
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0Njk3N2I3ZC1hM2U2LTQ2MDUtYjcwZC0xNzIzMTI5YWY4ZTQiLCJyb2xlcyI6WyJwcm94eSIsImFsbG9jYXRvciJdLCJpc3MiOiJib290c3RyYXAtaW5pdGlhbCIsImV4cCI6MTQ5MzY0NjIxM30.xsaRb72CsNMuXKy6Y-PJgqLc0qmjCljlB4Smcx_MRxg"
}
```

To generate a persistent token for additional allocators:

```sh
curl -H 'Content-Type: application/json' -u USER:PASSWORD https://$COORDINATOR_HOST:12443/api/v1/platform/configuration/security/enrollment-tokens -d '{ "persistent": true, "roles": [ "allocator"] }'
```
```sh
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0Yzg5OTBkZi0xZmI3LTQ4MjAtYjg2OC02YmM5ZTg4NjA4MTQiLCJyb2xlcyI6WyJwcm94eSIsImFsbG9jYXRvciJdLCJpc3MiOiJib290c3RyYXAtaW5pdGlhbCJ9.mfTkO4j8uZJ-qwB2jmBuMScyYfLmcJpvKgSTLx2WV24",
  "token_id": "4c8990df-1fb7-4820-b868-6bc9e8860814"
}
```

## Revoke roles tokens [ece-revoke-roles-token]

At the end of the {{ece}} installation process on the first host, you are provided with a roles token. You can also generate new roles tokens yourself, either as ephemeral tokens that get deleted after 24 hours or as persistent tokens that get stored by {{ece}}. These tokens enable additional hosts to join an {{ece}} installation and should be kept secure or deleted if they are no longer needed.

If you delete all tokens and need to add more hosts to your installation, you should generate a new token first.

::::{important}
During installation, an emergency token gets generated that enables you to install {{ece}} on additional hosts with all roles already assigned, except the allocator role. The emergency token can save your installation if all coordinators fail or are removed and you can no longer use the Cloud UI or the RESTful API. You should not delete this token. To learn more, check [Using the Emergency Roles Token](/troubleshoot/deployments/cloud-enterprise/use-emergency-roles-token.md).
::::

To delete a token:

1. Retrieve the list of available tokens through the RESTful API :

    ```sh
    curl -u USER:PASSWORD https://localhost:12443/api/v1/platform/configuration/security/enrollment-tokens
    ```
    ```sh
    {
      "tokens": [{
        "token_id": "5f9cad2f-c6e7-4ee2-8f6e-53225df45be5",
        "roles": []
      }, {
        "token_id": "4c8990df-1fb7-4820-b868-6bc9e8860814",
        "roles": ["proxy", "allocator"]
      }]
    }
    ```

2. Use the token ID to delete the tokens you no longer need: `4c8990df-1fb7-4820-b868-6bc9e8860814`:

    ```sh
    curl -XDELETE -u USER:PASSWORD  'https://localhost:12443/api/v1/platform/configuration/security/enrollment-tokens/4c8990df-1fb7-4820-b868-6bc9e8860814'
    ```
    ```sh
    {
    }
    ```

3. Optional: To check that the token has been deleted, repeat Step 1 and make sure that the token is no longer listed.
