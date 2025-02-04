# Organization operations [ec-api-organizations]


## Get information about your organization [ec_get_information_about_your_organization] 

Get information about your Elasticsearch Service organization.

```sh
curl -XGET \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations"
```


## Invite members to your organization [ec_invite_members_to_your_organization] 

Invite members to your Elasticsearch Service organization.

```sh
curl -XPOST \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations/$ORGANIZATION_ID/invitations" \
-d '
{
  "emails": [
    "test@test.com" <1>
  ]
}'
```

1. One or more email addresses to invite to the organization



## View pending invitations to your organization [ec_view_pending_invitations_to_your_organization] 

View pending invitations to your Elasticsearch Service organization.

```sh
curl -XGET \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations/$ORGANIZATION_ID/invitations"
```


## View members in your organization [ec_view_members_in_your_organization] 

View members in your Elasticsearch Service organization.

```sh
curl -XGET \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations/$ORGANIZATION_ID/members"
```


## Remove members from your organization [ec_remove_members_from_your_organization] 

Remove members from your Elasticsearch Service organization.

```sh
curl -XDELETE \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations/$ORGANIZATION_ID/members/$USER_IDS"
```

`USER_IDS`  One or more comma-delimited user ids to remove from the organization

