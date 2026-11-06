Create an API key with the required privileges:

1. In {{kib}}, open **Stack Management** → **API Keys**, then select **Create API key**.
2. Leave **Control security privileges** off and define a role with the following privileges:

    - **Index privileges**: `read` and `view_index_metadata` on `ai-index-*`.
    - **{{kib}} privileges**: **{{context-engine}}** at **Read** in the space you want to query.

    ::::{dropdown} Example role definition for the default space
    ```json
    {
      "contextEngineRole": {
        "cluster": [],
        "indices": [
          {
            "names": [
              "ai-index-*"
            ],
            "privileges": [
              "read",
              "view_index_metadata"
            ],
            "field_security": {
              "grant": [
                "*"
              ],
              "except": []
            },
            "allow_restricted_indices": false
          }
        ],
        "applications": [
          {
            "application": "kibana-.kibana",
            "privileges": [
              "feature_contextEngine.read"
            ],
            "resources": [
              "space:default"
            ]
          }
        ],
        "run_as": [],
        "metadata": {},
        "transient_metadata": {
          "enabled": true
        }
      }
    }
    ```
    ::::

3. Create the API key and copy its `encoded` value.
