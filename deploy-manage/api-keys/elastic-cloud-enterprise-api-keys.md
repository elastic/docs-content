---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-restful-api-authentication.html
applies_to:
  deployment:
    ece: ga
products:
  - id: cloud-enterprise
---

# {{ece}} API keys [ece-restful-api-authentication]

The {{ece}} RESTful APIs support both key-based and token-based authentication. Key-based is generally the preferred method.

{{ece}} API keys allow you to manage your {{ece}} platform and deployments using the [{{ece}}](https://www.elastic.co/docs/api/doc/cloud-enterprise/) API.


## Authenticate using an API key [ece-api-keys]

For key-based API authentication, you can create an API key through the {{ece}} UI. Once created, you can specify the key in the header of your API calls to authenticate.

::::{note}
API keys are not available for the built-in users (`admin` and `readonly`).  Therefore, the **API Keys** settings page on the UI does not appear for these users.
::::


To create an API key:

1. Sign in to the Cloud UI.
2. Go to **Profile**, **Settings**, and then **API Keys**.
3. Select **Generate API key**.
4. Specify a name and expiration for the API key.
5. Copy the generated API key and store it in a safe place. You can also download the key as a CSV file.

    ::::{note}
    By default, the API key will expire three months after its creation date, but you can set the expiration to Never. When you use an API key to authenticate, the API response header `X-Elastic-Api-Key-Expiration` indicates the key’s expiration date. You can log this value to detect API keys that are nearing expiration.
    ::::


The API key has the same permissions as the API key owner. You may have multiple API keys for different purposes and you can revoke them when you no longer need them.

Currently, API keys cannot be generated for the `admin` and `readonly` users that come pre-configured with your {{ece}} installation.

To revoke an API key:

1. Sign in to the Cloud UI.
2. Go to **Profile**, **Settings**, and then **API Keys**.
3. Select the trash icon under the **Revoke** column for any keys that you want to delete.


## Authenticate using a bearer token [ece-restful-api-authentication-token]

For token-based API authentication, you can use the same username and password that you use to log into the Cloud UI. If you want to use the credentials that were provided when you installed {{ece}} on your first host, for example `admin`, you can [retrieve them separately](../users-roles/cloud-enterprise-orchestrator/manage-system-passwords.md#ece-retrieve-passwords).

For operations that only read information, but don’t create, update or delete, you can authenticate with a user that has restricted permissions, such as the `readonly` user.

To create a bearer token:

1. Open a terminal and send your credentials to the login endpoint:

    ```sh
    curl -k -X POST -H 'Content-Type: application/json' https://$COORDINATOR_HOST:12443/api/v1/users/auth/_login --data-binary '
    {
      "username": "USER",
      "password": "PASSWORD"
    }'
    ```

    If your credentials are valid, the response from the login API will contain a JSON Web Token (JWT):

    ```text
    { "token": "eyJ0eXa...<very long string>...MgBmsw4s" }
    ```

2. Specify the bearer token in the Authentication header of your API requests. To learn more, check [accessing the API from the command line](cloud://reference/cloud-enterprise/ece-api-command-line.md).

