---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-getting-started-removing.html
---

# Remove the add-on [ech-getting-started-removing]

::::{warning} 
This action will destroy all associated data and cannot be undone.
::::


To remove the add-on from MY_APP using the Heroku CLI:

```term
heroku addons:destroy foundelasticsearch --app MY_APP

 ▸    WARNING: Destructive Action
 ▸    This command will affect the app testing-heroku-es
 ▸    To proceed, type MY_APP or re-run this command with
 ▸    --confirm MY_APP

> MY_APP
Destroying foundelasticsearch-trapezoidal-nnnnn on ⬢ MY_APP... done
```

