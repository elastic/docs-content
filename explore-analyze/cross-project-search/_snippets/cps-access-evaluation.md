Access control operates in two stages:

* Authentication verifies the identity associated with a request (for example, a Cloud user or API key) and retrieves that identity's role assignments in each project.
* Authorization evaluates those roles to determine which actions and resources the request can access within each project.

For example, if you have a viewer role in project 1, an admin role in project 2, and a custom role in project 3, you can access all three projects through {{cps}}. Each project enforces the permissions associated with the role you have in that project.

When a {{cps}} query targets a linked project that you have access to, authorization checks are performed locally in that project to determine whether you have the required privileges to access the requested resources.