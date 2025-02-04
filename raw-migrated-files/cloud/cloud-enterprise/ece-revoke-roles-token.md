# Revoke roles tokens [ece-revoke-roles-token]

At the end of the Elastic Cloud Enterprise installation process on the first host, you are provided with a roles token. You can also generate new roles tokens yourself, either as ephemeral tokens that get deleted after 24 hours or as persistent tokens that get stored by Elastic Cloud Enterprise. These tokens enable additional hosts to join an Elastic Cloud Enterprise installation and should be kept secure or deleted if they are no longer needed.

If you delete all tokens and need to add further hosts to your installation later on, you can  [generate a new token](../../../deploy-manage/deploy/cloud-enterprise/generate-roles-tokens.md) first.

::::{important} 
During installation, an emergency token gets generated that enables you to install Elastic Cloud Enterprise on additional hosts with all roles already assigned, except the allocator role. The emergency token can save your installation if all coordinators fail or are removed and you can no longer use the Cloud UI or the RESTful API. You should not delete this token. To learn more, check [Using the Emergency Roles Token](../../../troubleshoot/deployments/cloud-enterprise/use-emergency-roles-token.md).
::::


To delete a token:

1. Retrieve the list of available tokens through the RESTful API :

    ```sh
    curl -u USER:PASSWORD https://localhost:12443/api/v1/platform/configuration/security/enrollment-tokens
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

2. Use the token ID to delete the tokens you no longer need, here `4c8990df-1fb7-4820-b868-6bc9e8860814`:

    ```sh
    curl -XDELETE -u USER:PASSWORD  'https://localhost:12443/api/v1/platform/configuration/security/enrollment-tokens/4c8990df-1fb7-4820-b868-6bc9e8860814'
    {
    }
    ```

3. Optional: To check that the token has been deleted, repeat Step 1 and make sure that the token is no longer listed.

