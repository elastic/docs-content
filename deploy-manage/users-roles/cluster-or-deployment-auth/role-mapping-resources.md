---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/role-mapping-resources.html
navigation_title: "Role mapping properties"
applies_to:
  deployment:
    ece:
    eck:
    ess:
    self:
---

# Role mapping resource properties [role-mapping-resources]

A role mapping resource has the following properties:

`enabled`
:   (Boolean)  Mappings that have `enabled` set to `false` are ignored when role mapping is performed.

`metadata`
:   (object) Additional metadata that helps define which roles are assigned to each user. Within the `metadata` object, keys beginning with `_` are reserved for system usage.

`roles`
:   (list) A list of roles that are granted to the users that match the role mapping rules.

`rules`
:   (object) The rules that determine which users should be matched by the mapping. A rule is a logical condition that is expressed by using a JSON DSL. The DSL supports the following rule types:

    `any`
    :   (array of rules) If **any** of its children are true, it evaluates to `true`.

    `all`
    :   (array of rules) If **all** of its children are true, it evaluates to `true`.

    `field`
    :   (object) See [Field rules](#mapping-roles-rule-field).

    `except`
    :   (object) A single rule as an object. Only valid as a child of an `all` rule. If its child is `false`, the `except` is `true`.



## Field rules [mapping-roles-rule-field]

The `field` rule is the primary building block for a role mapping expression. It takes a single object as its value and that object must contain a single member with key *F* and value *V*. The field rule looks up the value of *F* within the user object and then tests whether the user value *matches* the provided value *V*.

The value specified in the field rule can be one of the following types:

| Type | Description | Example |
| --- | --- | --- |
| Simple String | Exactly matches the provided value. | `"esadmin"` |
| Wildcard String | Matches the provided value using a wildcard. | `"*,dc=example,dc=com"` |
| Regular Expression | Matches the provided value using a                       [Lucene regexp](elasticsearch://reference/query-languages/regexp-syntax.md). | `"/.*-admin[0-9]*/"` |
| Number | Matches an equivalent numerical value. | `7` |
| Null | Matches a null or missing value. | `null` |
| Array | Tests each element in the array in                      accordance with the above definitions.                      If *any* of elements match, the match is successful. | `["admin", "operator"]` |


### User fields [_user_fields]

The *user object* against which rules are evaluated has the following fields:

`username`
:   (string) The username by which the {{es}} {{security-features}} knows this user. For example, `"username": "jsmith"`.

`dn`
:   (string) The *Distinguished Name* of the user. For example, `"dn": "cn=jsmith,ou=users,dc=example,dc=com",`.

`groups`
:   (array of strings) The groups to which the user belongs. For example, `"groups" : [ "cn=admin,ou=groups,dc=example,dc=com","cn=esusers,ou=groups,dc=example,dc=com ]`.

`metadata`
:   (object) Additional metadata for the user. This can include a variety of key-value pairs. When referencing metadata fields in role mapping rules, use the dot notation to specify the key within the metadata object. If the key contains special characters such as parentheses, dots, or spaces, you must escape these characters using backslashes (`\`). For example, `"metadata": { "cn": "John Smith" }`.

`realm`
:   (object) The realm that authenticated the user. The only field in this object is the realm name. For example, `"realm": { "name": "ldap1" }`.

The `groups` field is multi-valued; a user can belong to many groups. When a `field` rule is applied against a multi-valued field, it is considered to match if *at least one* of the member values matches. For example, the following rule matches any user who is a member of the `admin` group, regardless of any other groups they belong to:

```js
{ "field" : { "groups" : "admin" } }
```
%  NOTCONSOLE

For additional realm-specific details, see [Active Directory and LDAP realms](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#ldap-role-mapping).

