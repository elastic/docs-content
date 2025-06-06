---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/create-defend-policy-api.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
---

# Create an Elastic Defend policy using API [create-defend-policy-api]

In addition to [configuring an {{elastic-defend}} policy](configure-an-integration-policy-for-elastic-defend.md) through the {{elastic-sec}} UI, you can create and customize an {{elastic-defend}} policy through the API. This is a three-step process involving the [{{fleet}} API](/reference/fleet/fleet-api-docs.md). You can repeat steps 2 and 3 to make more modifications to the {{elastic-defend}} policy.

::::{admonition} Requirements
You must have the **{{elastic-defend}} Policy Management: All** [privilege](elastic-defend-feature-privileges.md) to configure an integration policy.

::::



## Step 1: Create an agent policy [create-agent-policy]

Make the following API call to create a new agent policy where you will add your {{elastic-defend}} integration. Replace `<KIBANA-VERSION>` with your version of {{kib}}.

```console
curl --user <username>:<password> --request POST \
  --url 'https://<kibana-url>:5601/api/fleet/agent_policies' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'kbn-version: <KIBANA-VERSION>' \ <1>
  -d \
'
{
  "name": "My Policy Name",
  "description": "",
  "namespace": "default",
  "inactivity_timeout": 1209600
}'
```

1. `<KIBANA-VERSION>` to be replaced


Make a note of the `<POLICY-ID>` you receive in the response. You will use this in step 2 to add {{elastic-defend}}.

::::{dropdown} Click to display example response
```json
{
  "item": {
    "id": "<POLICY-ID>", <1>
    "name": "My Policy Name",
    "description": "",
    "namespace": "default",
    "inactivity_timeout": 1209600,
    "is_protected": false,
    "status": "active",
    "is_managed": false,
    "revision": 1,
    "updated_at": "2023-07-24T18:35:00.233Z",
    "updated_by": "elastic",
    "schema_version": "1.1.1"
  }
}
```

1. `<POLICY-ID>` needed in step 2


::::



## Step 2: Add the {{elastic-defend}} integration [add-defend-integration]

Next, make the following call to add the {{elastic-defend}} integration to the policy that you created in step 1.

Replace these values:

1. `<KIBANA-VERSION>` with your version of {{kib}}.
2. `<POLICY-ID>` with the agent policy ID you received in step 1.
3. `<LATEST-ELASTIC-DEFEND-PACKAGE-VERSION>` with the latest {{elastic-defend}} package version (for example, `8.9.1`). To find it, navigate to **Integrations** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and select **{{elastic-defend}}**.

This adds the {{elastic-defend}} integration to your agent policy with the default settings.

```console
curl --user <username>:<password> --request POST \
  --url 'https://<kibana-url>:5601/api/fleet/package_policies' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'kbn-version: <KIBANA-VERSION>' \ <1>
  -d \
'
{
  "name": "Protect",
  "description": "",
  "namespace": "default",
  "policy_id": "<POLICY-ID>", <2>
  "enabled": true,
  "inputs": [
    {
      "enabled": true,
      "streams": [],
      "type": "ENDPOINT_INTEGRATION_CONFIG",
      "config": {
        "_config": {
          "value": {
            "type": "endpoint",
            "endpointConfig": {
              "preset": "EDRComplete"
            }
          }
        }
      }
    }
  ],
  "package": {
    "name": "endpoint",
    "title": "Elastic Defend",
    "version": "<LATEST-ELASTIC-DEFEND-PACKAGE-VERSION>" <3>
  }
}'
```

1. `<KIBANA-VERSION>` to be replaced
2. `<POLICY-ID>` to be replaced
3. `<LATEST-ELASTIC-DEFEND-PACKAGE-VERSION>` to be replaced


Make a note of the `<PACKAGE-POLICY-ID>` you receive in the response. This refers to the {{elastic-defend}} policy and you will use it in step 3.

::::{dropdown} Click to display example response
```json
{
  "item": {
    "id": "<PACKAGE-POLICY-ID>", <1>
    "version": "WzMwOTcsMV0=",
    "name": "Protect",
    "namespace": "default",
    "description": "",
    "package": {
      "name": "endpoint",
      "title": "Elastic Defend",
      "version": "8.5.0"
    },
    "enabled": true,
    "policy_id": "b4be0860-d492-11ed-a59c-3ffbbd16325a",
    "inputs": [
      {
        "type": "endpoint",
        "enabled": true,
        "streams": [],
        "config": {
          "integration_config": {
            "value": {
              "type": "endpoint",
              "endpointConfig": {
                "preset": "EDRComplete"
              }
            }
          },
          "artifact_manifest": {
            "value": {
              "manifest_version": "1.0.2",
              "schema_version": "v1",
              "artifacts": {
                "endpoint-exceptionlist-macos-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-exceptionlist-macos-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-exceptionlist-windows-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-exceptionlist-windows-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-exceptionlist-linux-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-exceptionlist-linux-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-trustlist-macos-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-trustlist-macos-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-trustlist-windows-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-trustlist-windows-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-trustlist-linux-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-trustlist-linux-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-eventfilterlist-macos-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-eventfilterlist-macos-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-eventfilterlist-windows-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-eventfilterlist-windows-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-eventfilterlist-linux-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-eventfilterlist-linux-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-hostisolationexceptionlist-macos-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-hostisolationexceptionlist-macos-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-hostisolationexceptionlist-windows-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-hostisolationexceptionlist-windows-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-hostisolationexceptionlist-linux-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-hostisolationexceptionlist-linux-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-blocklist-macos-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-blocklist-macos-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-blocklist-windows-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-blocklist-windows-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                },
                "endpoint-blocklist-linux-v1": {
                  "encryption_algorithm": "none",
                  "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "decoded_size": 14,
                  "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                  "encoded_size": 22,
                  "relative_url": "/api/fleet/artifacts/endpoint-blocklist-linux-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                  "compression_algorithm": "zlib"
                }
              }
            }
          },
          "policy": {
            "value": {
              "windows": {
                "events": {
                  "dll_and_driver_load": true,
                  "dns": true,
                  "file": true,
                  "network": true,
                  "process": true,
                  "registry": true,
                  "security": true
                },
                "malware": {
                  "mode": "prevent",
                  "blocklist": true
                },
                "ransomware": {
                  "mode": "prevent",
                  "supported": true
                },
                "memory_protection": {
                  "mode": "prevent",
                  "supported": true
                },
                "behavior_protection": {
                  "mode": "prevent",
                  "supported": true
                },
                "popup": {
                  "malware": {
                    "message": "",
                    "enabled": true
                  },
                  "ransomware": {
                    "message": "",
                    "enabled": true
                  },
                  "memory_protection": {
                    "message": "",
                    "enabled": true
                  },
                  "behavior_protection": {
                    "message": "",
                    "enabled": true
                  }
                },
                "logging": {
                  "file": "info"
                },
                "antivirus_registration": {
                  "enabled": false
                },
                "attack_surface_reduction": {
                  "credential_hardening": {
                    "enabled": true
                  }
                }
              },
              "mac": {
                "events": {
                  "process": true,
                  "file": true,
                  "network": true
                },
                "malware": {
                  "mode": "prevent",
                  "blocklist": true
                },
                "behavior_protection": {
                  "mode": "prevent",
                  "supported": true
                },
                "memory_protection": {
                  "mode": "prevent",
                  "supported": true
                },
                "popup": {
                  "malware": {
                    "message": "",
                    "enabled": true
                  },
                  "behavior_protection": {
                    "message": "",
                    "enabled": true
                  },
                  "memory_protection": {
                    "message": "",
                    "enabled": true
                  }
                },
                "logging": {
                  "file": "info"
                }
              },
              "linux": {
                "events": {
                  "process": true,
                  "file": true,
                  "network": true,
                  "session_data": false,
                  "tty_io": false
                },
                "malware": {
                  "mode": "prevent",
                  "blocklist": true
                },
                "behavior_protection": {
                  "mode": "prevent",
                  "supported": true
                },
                "memory_protection": {
                  "mode": "prevent",
                  "supported": true
                },
                "popup": {
                  "malware": {
                    "message": "",
                    "enabled": true
                  },
                  "behavior_protection": {
                    "message": "",
                    "enabled": true
                  },
                  "memory_protection": {
                    "message": "",
                    "enabled": true
                  }
                },
                "logging": {
                  "file": "info"
                }
              }
            }
          }
        }
      }
    ],
    "revision": 1,
    "created_at": "2023-04-06T15:53:14.020Z",
    "created_by": "elastic",
    "updated_at": "2023-04-06T15:53:14.020Z",
    "updated_by": "elastic"
  }
}
```

1. `<PACKAGE-POLICY-ID>` needed in step 3


::::



## Step 3: Customize and save the {{elastic-defend}} policy settings [customize-policy-settings]

The response you received in step 2 represents the default configuration of your new {{elastic-defend}} integration. You’ll need to modify the default configuration, then make another API call to save your customized policy settings.


### Modify the configuration [modify-configuration]

1. From the response you received in step 2, copy the content within the top level `item` object.
2. From that content, remove the following fields:

    ```json
    "id": "<PACKAGE-POLICY-ID>",
    "revision": 1,
    "created_at": "2023-04-06T15:53:14.020Z",
    "created_by": "elastic",
    "updated_at": "2023-04-06T15:53:14.020Z",
    "updated_by": "elastic"
    ```

3. Make any changes to the `policy` object to customize the {{elastic-defend}} configuration.


### Save your customized policy settings [save-customized-policy]

Include the resulting JSON object in the following call to save your customized {{elastic-defend}} policy. Replace these values:

1. `<PACKAGE-POLICY-ID>` with the {{elastic-defend}} policy ID you received in step 2.
2. `<KIBANA-VERSION>` with your version of {{kib}}.
3. `<LATEST-ELASTIC-DEFEND-PACKAGE-VERSION>` with the latest {{elastic-defend}} package version (for example, `8.9.1`). To find it, navigate to **Integrations** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and select **{{elastic-defend}}**.

```console
curl --user <username>:<password> --request PUT \
  --url 'https://<kibana-url>:5601/api/fleet/package_policies/<PACKAGE-POLICY-ID>' \ <1>
  -H 'Accept: */*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'kbn-version: <KIBANA-VERSION>' \ <2>
  -d \
'
{
  "version": "WzMwOTcsMV0=",
  "name": "Protect",
  "namespace": "default",
  "description": "",
  "package": {
    "name": "endpoint",
    "title": "Elastic Defend",
    "version": "<LATEST-ELASTIC-DEFEND-PACKAGE-VERSION>" <3>
  },
  "enabled": true,
  "policy_id": "b4be0860-d492-11ed-a59c-3ffbbd16325a",
  "inputs": [
    {
      "type": "endpoint",
      "enabled": true,
      "streams": [],
      "config": {
        "integration_config": {
          "value": {
            "type": "endpoint",
            "endpointConfig": {
              "preset": "EDRComplete"
            }
          }
        },
        "artifact_manifest": {
          "value": {
            "manifest_version": "1.0.2",
            "schema_version": "v1",
            "artifacts": {
              "endpoint-exceptionlist-macos-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-exceptionlist-macos-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-exceptionlist-windows-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-exceptionlist-windows-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-exceptionlist-linux-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-exceptionlist-linux-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-trustlist-macos-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-trustlist-macos-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-trustlist-windows-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-trustlist-windows-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-trustlist-linux-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-trustlist-linux-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-eventfilterlist-macos-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-eventfilterlist-macos-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-eventfilterlist-windows-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-eventfilterlist-windows-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-eventfilterlist-linux-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-eventfilterlist-linux-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-hostisolationexceptionlist-macos-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-hostisolationexceptionlist-macos-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-hostisolationexceptionlist-windows-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-hostisolationexceptionlist-windows-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-hostisolationexceptionlist-linux-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-hostisolationexceptionlist-linux-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-blocklist-macos-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-blocklist-macos-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-blocklist-windows-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-blocklist-windows-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              },
              "endpoint-blocklist-linux-v1": {
                "encryption_algorithm": "none",
                "decoded_sha256": "d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "decoded_size": 14,
                "encoded_sha256": "f8e6afa1d5662f5b37f83337af774b5785b5b7f1daee08b7b00c2d6813874cda",
                "encoded_size": 22,
                "relative_url": "/api/fleet/artifacts/endpoint-blocklist-linux-v1/d801aa1fb7ddcc330a5e3173372ea6af4a3d08ec58074478e85aa5603e926658",
                "compression_algorithm": "zlib"
              }
            }
          }
        },
        "policy": {
          "value": {
            "windows": {
              "events": {
                "dll_and_driver_load": true,
                "dns": true,
                "file": true,
                "network": true,
                "process": true,
                "registry": true,
                "security": true
              },
              "malware": {
                "mode": "prevent",
                "blocklist": true
              },
              "ransomware": {
                "mode": "prevent",
                "supported": true
              },
              "memory_protection": {
                "mode": "prevent",
                "supported": true
              },
              "behavior_protection": {
                "mode": "prevent",
                "supported": true
              },
              "popup": {
                "malware": {
                  "message": "",
                  "enabled": true
                },
                "ransomware": {
                  "message": "",
                  "enabled": true
                },
                "memory_protection": {
                  "message": "",
                  "enabled": true
                },
                "behavior_protection": {
                  "message": "",
                  "enabled": true
                }
              },
              "logging": {
                "file": "info"
              },
              "antivirus_registration": {
                "enabled": false
              },
              "attack_surface_reduction": {
                "credential_hardening": {
                  "enabled": true
                }
              }
            },
            "mac": {
              "events": {
                "process": true,
                "file": true,
                "network": true
              },
              "malware": {
                "mode": "prevent",
                "blocklist": true
              },
              "behavior_protection": {
                "mode": "prevent",
                "supported": true
              },
              "memory_protection": {
                "mode": "prevent",
                "supported": true
              },
              "popup": {
                "malware": {
                  "message": "",
                  "enabled": true
                },
                "behavior_protection": {
                  "message": "",
                  "enabled": true
                },
                "memory_protection": {
                  "message": "",
                  "enabled": true
                }
              },
              "logging": {
                "file": "info"
              }
            },
            "linux": {
              "events": {
                "process": true,
                "file": true,
                "network": true,
                "session_data": false,
                "tty_io": false
              },
              "malware": {
                "mode": "prevent",
                "blocklist": true
              },
              "behavior_protection": {
                "mode": "prevent",
                "supported": true
              },
              "memory_protection": {
                "mode": "prevent",
                "supported": true
              },
              "popup": {
                "malware": {
                  "message": "",
                  "enabled": true
                },
                "behavior_protection": {
                  "message": "",
                  "enabled": true
                },
                "memory_protection": {
                  "message": "",
                  "enabled": true
                }
              },
              "logging": {
                "file": "info"
              }
            }
          }
        }
      }
    }
  ]
}'
```

1. `<PACKAGE-POLICY-ID>` to be replaced
2. `<KIBANA-VERSION>` to be replaced
3. `<LATEST-ELASTIC-DEFEND-PACKAGE-VERSION>` to be replaced
