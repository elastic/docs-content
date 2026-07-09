---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/security-project-settings.html
applies_to:
  serverless: ga
navigation_title: Manage projects with API
---

# Manage serverless projects using the API [serverless-api]

On this page, you can find examples of how to create and manage serverless projects using the [{{serverless-full}} API]({{cloud-serverless-apis}}), covering common operations such as:

- [Creating a project](#general-manage-project-with-api-create-a-serverless-elasticsearch-project)
- [Retrieving project details](#general-manage-project-with-api-get-project)
- [Retrieving the project's status](#general-manage-project-with-api-get-project-status)
- [Deleting a project](#general-manage-project-with-api-delete-project)
- [Updating a project](#general-manage-project-with-api-update-project)
- [Listing regions where projects can be created](#general-manage-project-with-api-list-available-regions)

To try the examples in this section, start by [setting up an API key](#general-manage-project-with-api-set-up-api-key).

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/cloud/manage-project
:::

## API resources

To learn about API principles, authentication, and how to use the OpenAPI specification, refer to the [{{serverless-full}} API]({{cloud-serverless-apis}}) documentation.

The available APIs are grouped by project type:

- APIs for [Search projects]({{cloud-serverless-apis}}group/endpoint-elasticsearch-projects)
- APIs for [Observability projects]({{cloud-serverless-apis}}group/endpoint-observability-projects)
- APIs for [Security projects]({{cloud-serverless-apis}}group/endpoint-security-projects)

## Set up an API key [general-manage-project-with-api-set-up-api-key]

To use the {{serverless-full}} API, you must authenticate your requests with an {{ecloud}} API key.

1. As an **Organization owner**, [create an {{ecloud}} API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) with one of the following roles, so that it can create and manage projects:

   - **Organization owner**
   - **Cloud resource access** with the **Admin** role assigned to **all projects** of the relevant type ({{es}}, {{observability}}, or Security)

   Select the key's **API access** level based on what you need it to do: **Cloud API** access is enough to manage projects, while **Cloud, {{es}}, and {{kib}} API** access also grants access to the project's {{es}} and {{kib}} endpoints. For more details, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).

2. Store the generated API key as an environment variable so that you don’t need to specify it again for each request:

   ```console
   export API_KEY="YOUR_GENERATED_API_KEY"
   ```

## Create an {{serverless-full}} project [general-manage-project-with-api-create-a-serverless-elasticsearch-project]

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/cloud/create-project
:::

```bash
curl -H "Authorization: ApiKey $API_KEY" \
     -H "Content-Type: application/json" \
     "https://api.elastic-cloud.com/api/v1/serverless/projects/elasticsearch" \
     -XPOST --data '{
        "name": "My project",  <1>
        "region_id": "aws-us-east-1"  <2>
     }'
```
1. Replace `My project` with a more descriptive name in this call.
2. You can obtain a [list of available regions](#general-manage-project-with-api-list-available-regions). 

The response from the create project request will include the created project details, including the project ID, the endpoints to access different apps such as {{es}} and {{kib}}, and a set of built-in `admin` credentials.

Example of `Create project` response:

```console-response
{
    "id": "cace8e65457043698ed3d99da2f053f6",
    "endpoints": {
        "elasticsearch": "https://sample-project-c990cb.es.us-east-1.aws.elastic.cloud",
        "kibana": "https://sample-project-c990cb-c990cb.kb.us-east-1.aws.elastic.cloud"
    },
    "credentials": {
        "username": "admin",
        "password": "abcd12345"
    }
    (...)
}
```

:::{note}
For programmatic access to the project's {{es}} and {{kib}} APIs, we recommend creating an [{{ecloud}} API key with access to the {{es}} and {{kib}} APIs](/deploy-manage/api-keys/elastic-cloud-api-keys.md#project-access) rather than using the built-in `admin` credentials.

The `admin` credentials returned in the `credentials` field serve as a fallback mechanism to access the project when no API key is available. Store them in a secure location, and use the [reset credentials API]({{cloud-serverless-apis}}operation/operation-resetelasticsearchprojectcredentials) if you need to recover or rotate them.
:::

You can store the project ID as an environment variable for the next requests:

```console
export PROJECT_ID=cace8e65457043698ed3d99da2f053f6
```

## Get project details [general-manage-project-with-api-get-project]

You can retrieve your project details through an API call:

```bash
curl -H "Authorization: ApiKey $API_KEY" \
    "https://api.elastic-cloud.com/api/v1/serverless/projects/elasticsearch/${PROJECT_ID}"
```

## Get the project status [general-manage-project-with-api-get-project-status]

The 'status' endpoint indicates whether the project is initialized and ready to be used. In the response, the project's `phase` will change from "initializing" to "initialized" when it is ready:

```bash
curl -H "Authorization: ApiKey $API_KEY" \
    "https://api.elastic-cloud.com/api/v1/serverless/projects/elasticsearch/${PROJECT_ID}/status"
```

Example response:

```console-response
{
    "phase":"initializing"
}
```

## Delete a project [general-manage-project-with-api-delete-project]

You can delete your project via the API:

```bash
curl -XDELETE -H "Authorization: ApiKey $API_KEY" \
    "https://api.elastic-cloud.com/api/v1/serverless/projects/elasticsearch/${PROJECT_ID}"
```

## Update a project [general-manage-project-with-api-update-project]

You can update your project using a PATCH request. Only the fields included in the body of the request will be updated.

```bash
curl -H "Authorization: ApiKey $API_KEY" \
    -H "Content-Type: application/json" \
    "https://api.elastic-cloud.com/api/v1/serverless/projects/elasticsearch/${PROJECT_ID}" \
    -XPATCH --data '{
        "name": "new name",
        "alias": "new-project-alias"
     }'
```

## List available regions [general-manage-project-with-api-list-available-regions]

You can obtain the list of regions where projects can be created using the API:

```bash
curl -H "Authorization: ApiKey $API_KEY" \
    "https://api.elastic-cloud.com/api/v1/serverless/regions"
```
