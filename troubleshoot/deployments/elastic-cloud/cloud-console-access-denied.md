---
navigation_title: Cloud Console access denied
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
---

# Access Denied page in the {{ecloud}} Console

When you open the {{ecloud}} Console, you see an **Access Denied** page instead of the expected content. 

This message might appear when navigating directly to an {{ecloud}} URL, or when following links in {{kib}} that redirect to the {{ecloud}} Console, such as **Manage project**, **View all projects**, and **Organization**.

## Why this happens

Your organization admin set your access level to **{{es}} and {{kib}}** for your project assignments. This access level lets you work in your assigned projects, but restricts access to organization-level pages in the {{ecloud}} Console such as **Members**, **Billing**, and **Network security**.

## What you can do

* **Open your projects directly.** Use the project URL your admin shared with you. Project URLs follow this pattern: `https://<project-alias>.<kb>.<region>.<csp>.elastic-cloud.com`. Bookmark it for easy access.
* **Check your project overview page.** The project overview page in the Console is still accessible for projects you're assigned to.
* **Contact your admin** if you need access to additional Console pages or projects.

To learn more about access levels, refer to [Access options](/deploy-manage/users-roles/cloud-organization/user-roles.md#access).
