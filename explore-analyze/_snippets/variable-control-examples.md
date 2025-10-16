**Examples**

* Integrate filtering into your {{esql}} experience

  ```esql
  | WHERE field == ?value
  ```

* Fields in controls for dynamic group by

  ```esql
  | STATS count=COUNT(*) BY ??field
  ```

* Variable time ranges? Bind function configuration settings to a control

  ```esql
  | BUCKET(@timestamp, ?interval),
  ```

* Make the function itself dynamic

  ```esql
  | STATS metric = ??function
  ```