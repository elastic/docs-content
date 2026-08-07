**Examples**

* Filter by a selected value:

  ```esql
  | WHERE field == ?value
  ```

* Group by a selected field:

  ```esql
  | STATS count = COUNT(*) BY ??field
  ```

* Adjust a function setting, such as a date histogram interval:

  ```esql
  | STATS count = COUNT(*) BY BUCKET(@timestamp, ?interval)
  ```

* Switch the aggregation function:

  ```esql
  | STATS metric = ??function
  ```
