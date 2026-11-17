When you cancel a running query in **Discover**, what you see afterward depends on your version.

:::::{applies-switch}

::::{applies-item} { serverless: ga, stack: ga 9.3+ }
Select the **Cancel** button that appears while the query runs. **Discover** stops the search and displays the partial results collected up to that point.
::::

::::{applies-item} stack: ga 9.0-9.2
Select the **Cancel** button that appears while the query runs. **Discover** stops the search and shows an empty results table.
::::

:::::

:::{tip}
For long-running queries, you can also [send the query to the background](/explore-analyze/discover/background-search.md) instead of canceling it, allowing it to complete while you continue working.
:::
