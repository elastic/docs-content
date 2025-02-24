---
applies_to:
  deployment:
    ess:
    ece:
    eck:
    self:
---

# Built-in users

The {{stack-security-features}} provide built-in user credentials to help you get up and running. This includes the `elastic` user.

In this section, you'll learn the following: 

* [Built-in users for self-managed clusters](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md): Learn about the users that are used to communicate between {{stack}} components, and about managing bootstrap passwords for built-in users. 
* How to manage built-in user passwords:
  * In {{ece}} and {{ech}}, [learn how to reset password for the `elastic` user](/deploy-manage/users-roles/cluster-or-deployment-auth/manage-elastic-user-cloud.md).
  * In {{eck}}, [learn how to manage the `elastic` user, and how to rotate all auto-generated credentials used by ECK](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-eck.md).
  * In self-managed clusters, [learn how to change passwords for built-in users](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-sm.md).