---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/canvas-function-reference.html
---

# Canvas function reference [canvas-function-reference]

Behind the scenes, Canvas is driven by a powerful expression language, with dozens of functions and other capabilities, including table transforms, type casting, and sub-expressions.

The Canvas expression language also supports [TinyMath functions](/reference/data-analysis/kibana/tinymath-functions.md), which perform complex math calculations.

A * denotes a required argument.

A † denotes an argument can be passed multiple times.

[A](#a_fns) | B | [C](#c_fns) | [D](#d_fns) | [E](#e_fns) | [F](#f_fns) | [G](#g_fns) | [H](#h_fns) | [I](#i_fns) | [J](#j_fns) | [K](#k_fns) | [L](#l_fns) | [M](#m_fns) | [N](#n_fns) | O | [P](#p_fns) | Q | [R](#r_fns) | [S](#s_fns) | [T](#t_fns) | [U](#u_fns) | [V](#v_fns) | W | X | Y | Z


## A [a_fns]


### `all` [all_fn]

Returns `true` if all of the conditions are met. See also [`any`](#any_fn).

**Expression syntax**

```js
all {neq "foo"} {neq "bar"} {neq "fizz"}
all condition={gt 10} condition={lt 20}
```

**Code example**

```text
kibana
| selectFilter
| demodata
| math "mean(percent_uptime)"
| formatnumber "0.0%"
| metric "Average uptime"
  metricFont={
    font size=48 family="'Open Sans', Helvetica, Arial, sans-serif"
      color={
        if {all {gte 0} {lt 0.8}} then="red" else="green"
      }
      align="center" lHeight=48
  }
| render
```

This sets the color of the metric text to `"red"` if the context passed into `metric` is greater than or equal to 0 and less than 0.8. Otherwise, the color is set to `"green"`.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* * †<br>Alias: `condition` | `boolean` | The conditions to check. |

**Returns:** `boolean`


### `alterColumn` [alterColumn_fn]

Converts between core types, including `string`, `number`, `null`, `boolean`, and `date`, and renames columns. See also [`mapColumn`](#mapColumn_fn), [`mathColumn`](#mathColumn_fn), and [`staticColumn`](#staticColumn_fn).

**Expression syntax**

```js
alterColumn "cost" type="string"
alterColumn column="@timestamp" name="foo"
```

**Code example**

```text
kibana
| selectFilter
| demodata
| alterColumn "time" name="time_in_ms" type="number"
| table
| render
```

This renames the `time` column to `time_in_ms` and converts the type of the column’s values from `date` to `number`.

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `column` | `string` | The name of the column to alter. |
| `name` | `string` | The resultant column name. Leave blank to not rename. |
| `type` | `string` | The type to convert the column to. Leave blank to not change the type. |

**Returns:** `datatable`


### `any` [any_fn]

Returns `true` if at least one of the conditions is met. See also [`all`](#all_fn).

**Expression syntax**

```js
any {eq "foo"} {eq "bar"} {eq "fizz"}
any condition={lte 10} condition={gt 30}
```

**Code example**

```text
kibana
| selectFilter
| demodata
| filterrows {
    getCell "project" | any {eq "elasticsearch"} {eq "kibana"} {eq "x-pack"}
  }
| pointseries color="project" size="max(price)"
| pie
| render
```

This filters out any rows that don’t contain `"elasticsearch"`, `"kibana"` or `"x-pack"` in the `project` field.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* * †<br>Alias: `condition` | `boolean` | The conditions to check. |

**Returns:** `boolean`


### `as` [as_fn]

Creates a `datatable` with a single value. See also [`getCell`](#getCell_fn).

**Expression syntax**

```js
as
as "foo"
as name="bar"
```

**Code example**

```text
kibana
| selectFilter
| demodata
| ply by="project" fn={math "count(username)" | as "num_users"} fn={math "mean(price)" | as "price"}
| pointseries x="project" y="num_users" size="price" color="project"
| plot
| render
```

`as` casts any primitive value (`string`, `number`, `date`, `null`) into a `datatable` with a single row and a single column with the given name (or defaults to `"value"` if no name is provided). This is useful when piping a primitive value into a function that only takes `datatable` as an input.

In the example, `ply` expects each `fn` subexpression to return a `datatable` in order to merge the results of each `fn` back into a `datatable`, but using a `math` aggregation in the subexpressions returns a single `math` value, which is then cast into a `datatable` using `as`.

**Accepts:** `string`, `boolean`, `number`, `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `name` | `string` | The name to give the column.<br>Default: `"value"` |

**Returns:** `datatable`


### `asset` [asset_fn]

Retrieves Canvas workpad asset objects to provide as argument values. Usually images.

**Expression syntax**

```js
asset "asset-52f14f2b-fee6-4072-92e8-cd2642665d02"
asset id="asset-498f7429-4d56-42a2-a7e4-8bf08d98d114"
```

**Code example**

```text
image dataurl={asset "asset-c661a7cc-11be-45a1-a401-d7592ea7917a"} mode="contain"
| render
```

The image asset stored with the ID `"asset-c661a7cc-11be-45a1-a401-d7592ea7917a"` is passed into the `dataurl` argument of the `image` function to display the stored asset.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `id` | `string` | The ID of the asset to retrieve. |

**Returns:** `string`


### `axisConfig` [axisConfig_fn]

Configures the axis of a visualization. Only used with [`plot`](#plot_fn).

**Expression syntax**

```js
axisConfig show=false
axisConfig position="right" min=0 max=10 tickSize=1
```

**Code example**

```text
kibana
| selectFilter
| demodata
| pointseries x="size(cost)" y="project" color="project"
| plot defaultStyle={seriesStyle bars=0.75 horizontalBars=true}
  legend=false
  xaxis={axisConfig position="top" min=0 max=400 tickSize=100}
  yaxis={axisConfig position="right"}
| render
```

This sets the `x-axis` to display on the top of the chart and sets the range of values to `0-400` with ticks displayed at `100` intervals. The `y-axis` is configured to display on the `right`.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| `max` | `number`, `string`, `null` | The maximum value displayed in the axis. Must be a number, a date in milliseconds since epoch, or an ISO8601 string. |
| `min` | `number`, `string`, `null` | The minimum value displayed in the axis. Must be a number, a date in milliseconds since epoch, or an ISO8601 string. |
| `position` | `string` | The position of the axis labels. For example, `"top"`, `"bottom"`, `"left"`, or `"right"`.<br>Default: `"left"` |
| `show` | `boolean` | Show the axis labels?<br>Default: `true` |
| `tickSize` | `number`, `null` | The increment size between each tick. Use for `number` axes only. |

**Returns:** `axisConfig`


## C [c_fns]


### `case` [case_fn]

Builds a [`case`](#case_fn), including a condition and a result, to pass to the [`switch`](#switch_fn) function.

**Expression syntax**

```js
case 0 then="red"
case when=5 then="yellow"
case if={lte 50} then="green"
```

**Code example**

```text
math "random()"
| progress shape="gauge" label={formatnumber "0%"}
  font={
    font size=24 family="'Open Sans', Helvetica, Arial, sans-serif" align="center"
      color={
        switch {case if={lte 0.5} then="green"}
          {case if={all {gt 0.5} {lte 0.75}} then="orange"}
          default="red"
      }
  }
  valueColor={
    switch {case if={lte 0.5} then="green"}
      {case if={all {gt 0.5} {lte 0.75}} then="orange"}
      default="red"
  }
| render
```

This sets the color of the progress indicator and the color of the label to `"green"` if the value is less than or equal to `0.5`, `"orange"` if the value is greater than `0.5` and less than or equal to `0.75`, and `"red"` if `none` of the case conditions are met.

**Accepts:** `any`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `when` | `any` | The value compared to the *context* to see if they are equal. The `when` argument is ignored when the `if` argument is also specified. |
| `if` | `boolean` | This value indicates whether the condition is met. The `if` argument overrides the `when` argument when both are provided. |
| `then` * | `any` | The value returned if the condition is met. |

**Returns:** `case`


### `clear` [clear_fn]

Clears the *context*, and returns `null`.

**Accepts:** `null`

**Returns:** `null`


### `clog` [clog_fn]

Outputs the *input* in the console. This function is for debug purposes

**Expression syntax**

```js
clog
```

**Code example**

```text
kibana
| demodata
| clog
| filterrows fn={getCell "age" | gt 70}
| clog
| pointseries x="time" y="mean(price)"
| plot defaultStyle={seriesStyle lines=1 fill=1}
| render
```

This prints the `datatable` objects in the browser console before and after the `filterrows` function.

**Accepts:** `any`

**Returns:** Depends on your input and arguments


### `columns` [columns_fn]

Includes or excludes columns from a `datatable`. When both arguments are specified, the excluded columns will be removed first.

**Expression syntax**

```js
columns include="@timestamp, projects, cost"
columns exclude="username, country, age"
```

**Code example**

```text
kibana
| selectFilter
| demodata
| columns include="price, cost, state, project"
| table
| render
```

This only keeps the `price`, `cost`, `state`, and `project` columns from the `demodata` data source and removes all other columns.

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `include` | `string` | A comma-separated list of column names to keep in the `datatable`. |
| `exclude` | `string` | A comma-separated list of column names to remove from the `datatable`. |

**Returns:** `datatable`


### `compare` [compare_fn]

Compares the *context* to specified value to determine `true` or `false`. Usually used in combination with `<<if_fn>>` or [`case`](#case_fn). This only works with primitive types, such as `number`, `string`, `boolean`, `null`. See also [`eq`](#eq_fn), [`gt`](#gt_fn), [`gte`](#gte_fn), [`lt`](#lt_fn), [`lte`](#lte_fn), [`neq`](#neq_fn)

**Expression syntax**

```js
compare "neq" to="elasticsearch"
compare op="lte" to=100
```

**Code example**

```text
kibana
| selectFilter
| demodata
| mapColumn project
  fn={getCell project |
    switch
      {case if={compare eq to=kibana} then=kibana}
      {case if={compare eq to=elasticsearch} then=elasticsearch}
      default="other"
  }
| pointseries size="size(cost)" color="project"
| pie
| render
```

This maps all `project` values that aren’t `"kibana"` and `"elasticsearch"` to `"other"`. Alternatively, you can use the individual comparator functions instead of compare.

**Accepts:** `string`, `number`, `boolean`, `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `op` | `string` | The operator to use in the comparison: `"eq"` (equal to), `"gt"` (greater than), `"gte"` (greater than or equal to), `"lt"` (less than), `"lte"` (less than or equal to), `"ne"` or `"neq"` (not equal to).<br>Default: `"eq"` |
| `to`<br>Aliases: `b`, `this` | `any` | The value compared to the *context*. |

**Returns:** `boolean`


### `containerStyle` [containerStyle_fn]

Creates an object used for styling an element’s container, including background, border, and opacity.

**Expression syntax**

```js
containerStyle backgroundColor="red"’
containerStyle borderRadius="50px"
containerStyle border="1px solid black"
containerStyle padding="5px"
containerStyle opacity="0.5"
containerStyle overflow="hidden"
containerStyle backgroundImage={asset id=asset-f40d2292-cf9e-4f2c-8c6f-a504a25e949c}
  backgroundRepeat="no-repeat"
  backgroundSize="cover"
```

**Code example**

```text
shape "star" fill="#E61D35" maintainAspect=true
| render containerStyle={
    containerStyle backgroundColor="#F8D546"
      borderRadius="200px"
      border="4px solid #05509F"
      padding="0px"
      opacity="0.9"
      overflow="hidden"
  }
```

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| `backgroundColor` | `string` | A valid CSS background color. |
| `backgroundImage` | `string` | A valid CSS background image. |
| `backgroundRepeat` | `string` | A valid CSS background repeat.<br>Default: `"no-repeat"` |
| `backgroundSize` | `string` | A valid CSS background size.<br>Default: `"contain"` |
| `border` | `string` | A valid CSS border. |
| `borderRadius` | `string` | The number of pixels to use when rounding the corners. |
| `opacity` | `number` | A number between 0 and 1 that represents the degree of transparency of the element. |
| `overflow` | `string` | A valid CSS overflow.<br>Default: `"hidden"` |
| `padding` | `string` | The distance of the content, in pixels, from the border. |

**Returns:** `containerStyle`


### `context` [context_fn]

Returns whatever you pass into it. This can be useful when you need to use *context* as argument to a function as a sub-expression.

**Expression syntax**

```js
context
```

**Code example**

```text
date
| formatdate "LLLL"
| markdown "Last updated: " {context}
| render
```

Using the `context` function allows us to pass the output, or *context*, of the previous function as a value to an argument in the next function. Here we get the formatted date string from the previous function and pass it as `content` for the markdown element.

**Accepts:** `any`

**Returns:** Depends on your input and arguments


### `createTable` [createTable_fn]

Creates a datatable with a list of columns, and 1 or more empty rows. To populate the rows, use [`mapColumn`](#mapColumn_fn) or [`mathColumn`](#mathColumn_fn).

**Expression syntax**

```js
createTable id="a" id="b"
createTable id="a" name="A" id="b" name="B" rowCount=5
```

**Code example**

```text
var_set
name="logs" value={essql "select count(*) as a from kibana_sample_data_logs"}
name="commerce" value={essql "select count(*) as b from kibana_sample_data_ecommerce"}
| createTable ids="totalA" ids="totalB"
| staticColumn name="totalA" value={var "logs" | getCell "a"}
| alterColumn column="totalA" type="number"
| staticColumn name="totalB" value={var "commerce" | getCell "b"}
| alterColumn column="totalB" type="number"
| mathColumn id="percent" name="percent" expression="totalA / totalB"
| render
```

This creates a table based on the results of two `essql` queries, joined into one table.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| `ids` † | `string` | Column ids to generate in positional order. ID represents the key in the row. |
| `names` † | `string` | Column names to generate in positional order. Names are not required to be unique, and default to the ID if not provided. |
| `rowCount` | `number` | The number of empty rows to add to the table, to be assigned a value later<br>Default: `1` |

**Returns:** `datatable`


### `csv` [csv_fn]

Creates a `datatable` from CSV input.

**Expression syntax**

```js
csv "fruit, stock
  kiwi, 10
  Banana, 5"
```

**Code example**

```text
csv "fruit,stock
  kiwi,10
  banana,5"
| pointseries color=fruit size=stock
| pie
| render
```

This creates a `datatable` with `fruit` and `stock` columns with two rows. This is useful for quickly mocking data.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `data` | `string` | The CSV data to use. |
| `delimiter` | `string` | The data separation character. |
| `newline` | `string` | The row separation character. |

**Returns:** `datatable`


## D [d_fns]


### `date` [date_fn]

Returns the current time, or a time parsed from a specified string, as milliseconds since epoch.

**Expression syntax**

```js
date
date value=1558735195
date "2019-05-24T21:59:55+0000"
date "01/31/2019" format="MM/DD/YYYY"
```

**Code example**

```text
date
| formatdate "LLL"
| markdown {context}
  font={font family="Arial, sans-serif" size=30 align="left"
    color="#000000"
    weight="normal"
    underline=false
    italic=false}
| render
```

Using `date` without passing any arguments will return the current date and time.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `value` | `string` | An optional date string that is parsed into milliseconds since epoch. The date string can be either a valid JavaScript `Date` input or a string to parse using the `format` argument. Must be an ISO8601 string, or you must provide the format. |
| `format` | `string` | The MomentJS format used to parse the specified date string. For more information, see [https://momentjs.com/docs/#/displaying/](https://momentjs.com/docs/#/displaying/). |

**Returns:** `number`


### `demodata` [demodata_fn]

A sample data set that includes project CI times with usernames, countries, and run phases.

**Expression syntax**

```js
demodata
demodata "ci"
demodata type="shirts"
```

**Code example**

```text
kibana
| selectFilter
| demodata
| table
| render
```

`demodata` is a mock data set that you can use to start playing around in Canvas.

**Accepts:** `filter`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `type` | `string` | The name of the demo data set to use.<br>Default: `"ci"` |

**Returns:** `datatable`


### `do` [do_fn]

Executes multiple sub-expressions, then returns the original *context*. Use for running functions that produce an action or a side effect without changing the original *context*.

**Accepts:** `any`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* †<br>Aliases: `exp`, `expression`, `fn`, `function` | `any` | The sub-expressions to execute. The return values of these sub-expressions are not available in the root pipeline as this function simply returns the original *context*. |

**Returns:** Depends on your input and arguments


### `dropdownControl` [dropdownControl_fn]

Configures a dropdown filter control element.

**Expression syntax**

```js
dropdownControl valueColumn=project filterColumn=project
dropdownControl valueColumn=agent filterColumn=agent.keyword filterGroup=group1
```

**Code example**

```text
demodata
| dropdownControl valueColumn=project filterColumn=project
| render
```

This creates a dropdown filter element. It requires a data source and uses the unique values from the given `valueColumn` (i.e. `project`) and applies the filter to the `project` column. Note: `filterColumn` should point to a keyword type field for Elasticsearch data sources.

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| `filterColumn` * | `string` | The column or field that you want to filter. |
| `filterGroup` | `string` | The group name for the filter. |
| `labelColumn` | `string` | The column or field to use as the label in the dropdown control |
| `valueColumn` * | `string` | The column or field from which to extract the unique values for the dropdown control. |

**Returns:** `render`


## E [e_fns]


### `embeddable` [embeddable_fn]

Returns an embeddable with the provided configuration

**Accepts:** `filter`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `config` | `string` | The base64 encoded embeddable input object |
| `type` * | `string` | The embeddable type |

**Returns:** `embeddable`


### `eq` [eq_fn]

Returns whether the *context* is equal to the argument.

**Expression syntax**

```js
eq true
eq null
eq 10
eq "foo"
```

**Code example**

```text
kibana
| selectFilter
| demodata
| mapColumn project
  fn={getCell project |
    switch
      {case if={eq kibana} then=kibana}
      {case if={eq elasticsearch} then=elasticsearch}
      default="other"
  }
| pointseries size="size(cost)" color="project"
| pie
| render
```

This changes all values in the project column that don’t equal `"kibana"` or `"elasticsearch"` to `"other"`.

**Accepts:** `boolean`, `number`, `string`, `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `value` | `boolean`, `number`, `string`, `null` | The value compared to the *context*. |

**Returns:** `boolean`


### `escount` [escount_fn]

Query Elasticsearch for the number of hits matching the specified query.

**Expression syntax**

```js
escount index="logstash-*"
escount "currency:"EUR"" index="kibana_sample_data_ecommerce"
escount query="response:404" index="kibana_sample_data_logs"
```

**Code example**

```text
kibana
| selectFilter
| escount "Cancelled:true" index="kibana_sample_data_flights"
| math "value"
| progress shape="semicircle"
  label={formatnumber 0,0}
  font={font size=24 family="'Open Sans', Helvetica, Arial, sans-serif" color="#000000" align=center}
  max={filters | escount index="kibana_sample_data_flights"}
| render
```

The first `escount` expression retrieves the number of flights that were cancelled. The second `escount` expression retrieves the total number of flights.

**Accepts:** `filter`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Aliases: `q`, `query` | `string` | A Lucene query string.<br>Default: `"-_index:.kibana"` |
| `index`<br>Alias: `dataView` | `string` | An index or data view. For example, `"logstash-*"`.<br>Default: `"_all"` |

**Returns:** `number`


### `esdocs` [esdocs_fn]

Query Elasticsearch for raw documents. Specify the fields you want to retrieve, especially if you are asking for a lot of rows.

**Expression syntax**

```js
esdocs index="logstash-*"
esdocs "currency:"EUR"" index="kibana_sample_data_ecommerce"
esdocs query="response:404" index="kibana_sample_data_logs"
esdocs index="kibana_sample_data_flights" count=100
esdocs index="kibana_sample_data_flights" sort="AvgTicketPrice, asc"
```

**Code example**

```text
kibana
| selectFilter
| esdocs index="kibana_sample_data_ecommerce"
  fields="customer_gender, taxful_total_price, order_date"
  sort="order_date, asc"
  count=10000
| mapColumn "order_date"
  fn={getCell "order_date" | date {context} | rounddate "YYYY-MM-DD"}
| alterColumn "order_date" type="date"
| pointseries x="order_date" y="sum(taxful_total_price)" color="customer_gender"
| plot defaultStyle={seriesStyle lines=3}
  palette={palette "#7ECAE3" "#003A4D" gradient=true}
| render
```

This retrieves the first 10000 documents data from the `kibana_sample_data_ecommerce` index sorted by `order_date` in ascending order, and only requests the `customer_gender`, `taxful_total_price`, and `order_date` fields.

**Accepts:** `filter`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Aliases: `q`, `query` | `string` | A Lucene query string.<br>Default: `"-_index:.kibana"` |
| `count` | `number` | The number of documents to retrieve. For better performance, use a smaller data set.<br>Default: `1000` |
| `fields` | `string` | A comma-separated list of fields. For better performance, use fewer fields. |
| `index`<br>Alias: `dataView` | `string` | An index or data view. For example, `"logstash-*"`.<br>Default: `"_all"` |
| `metaFields` | `string` | Comma separated list of meta fields. For example, `"_index,_type"`. |
| `sort` | `string` | The sort direction formatted as `"field, direction"`. For example, `"@timestamp, desc"` or `"bytes, asc"`. |

**Returns:** `datatable`


### `essql` [essql_fn]

Queries Elasticsearch using Elasticsearch SQL.

**Expression syntax**

```js
essql query="SELECT * FROM "logstash*""
essql "SELECT * FROM "apm*"" count=10000
```

**Code example**

```text
kibana
| selectFilter
| essql query="SELECT Carrier, FlightDelayMin, AvgTicketPrice FROM   "kibana_sample_data_flights""
| table
| render
```

This retrieves the `Carrier`, `FlightDelayMin`, and `AvgTicketPrice` fields from the "kibana_sample_data_flights" index.

**Accepts:** `kibana_context`, `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Aliases: `q`, `query` | `string` | An Elasticsearch SQL query. |
| `count` | `number` | The number of documents to retrieve. For better performance, use a smaller data set.<br>Default: `1000` |
| `parameter` †<br>Alias: `param` | `string`, `number`, `boolean` | A parameter to be passed to the SQL query. |
| `timeField`<br>Alias: `timeField` | `string` | The time field to use in the time range filter, which is set in the context. |
| `timezone`<br>Alias: `tz` | `string` | The timezone to use for date operations. Valid ISO8601 formats and UTC offsets both work.<br>Default: `"UTC"` |

**Returns:** `datatable`


### `exactly` [exactly_fn]

Creates a filter that matches a given column to an exact value.

**Expression syntax**

```js
exactly "state" value="running"
exactly "age" value=50 filterGroup="group2"
exactly column="project" value="beats"
```

**Accepts:** `filter`

| Argument | Type | Description |
| --- | --- | --- |
| `column` *<br>Aliases: `c`, `field` | `string` | The column or field that you want to filter. |
| `filterGroup` | `string` | The group name for the filter. |
| `value` *<br>Aliases: `v`, `val` | `string` | The value to match exactly, including white space and capitalization. |

**Returns:** `filter`


## F [f_fns]


### `filterrows` [filterrows_fn]

Filters rows in a `datatable` based on the return value of a sub-expression.

**Expression syntax**

```js
filterrows {getCell "project" | eq "kibana"}
filterrows fn={getCell "age" | gt 50}
```

**Code example**

```text
kibana
| selectFilter
| demodata
| filterrows {getCell "country" | any {eq "IN"} {eq "US"} {eq "CN"}}
| mapColumn "@timestamp"
  fn={getCell "@timestamp" | rounddate "YYYY-MM"}
| alterColumn "@timestamp" type="date"
| pointseries x="@timestamp" y="mean(cost)" color="country"
| plot defaultStyle={seriesStyle points="2" lines="1"}
  palette={palette "#01A4A4" "#CC6666" "#D0D102" "#616161" "#00A1CB" "#32742C" "#F18D05" "#113F8C" "#61AE24" "#D70060" gradient=false}
| render
```

This uses `filterrows` to only keep data from India (`IN`), the United States (`US`), and China (`CN`).

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Aliases: `exp`, `expression`, `fn`, `function` | `boolean` | An expression to pass into each row in the `datatable`. The expression should return a `boolean`. A `true` value preserves the row, and a `false` value removes it. |

**Returns:** `datatable`


### `filters` [filters_fn]

Aggregates element filters from the workpad for use elsewhere, usually a data source. [`filters`](#filters_fn) is deprecated and will be removed in a future release. Use `kibana | selectFilter` instead.

**Expression syntax**

```js
filters
filters group="timefilter1"
filters group="timefilter2" group="dropdownfilter1" ungrouped=true
```

**Code example**

```text
filters group=group2 ungrouped=true
| demodata
| pointseries x="project" y="size(cost)" color="project"
| plot defaultStyle={seriesStyle bars=0.75} legend=false
  font={
    font size=14
    family="'Open Sans', Helvetica, Arial, sans-serif"
    align="left"
    color="#FFFFFF"
    weight="lighter"
    underline=true
    italic=true
  }
| render
```

`filters` sets the existing filters as context and accepts a `group` parameter to opt into specific filter groups. Setting `ungrouped` to `true` opts out of using global filters.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* †<br>Alias: `group` | `string` | The name of the filter group to use. |
| `ungrouped`<br>Aliases: `nogroup`, `nogroups` | `boolean` | Exclude filters that belong to a filter group?<br>Default: `false` |

**Returns:** `filter`


### `font` [font_fn]

Create a font style.

**Expression syntax**

```js
font size=12
font family=Arial
font align=middle
font color=pink
font weight=lighter
font underline=true
font italic=false
font lHeight=32
```

**Code example**

```text
kibana
| selectFilter
| demodata
| pointseries x="project" y="size(cost)" color="project"
| plot defaultStyle={seriesStyle bars=0.75} legend=false
  font={
    font size=14
    family="'Open Sans', Helvetica, Arial, sans-serif"
    align="left"
    color="#FFFFFF"
    weight="lighter"
    underline=true
    italic=true
  }
| render
```

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| `align` | `string` | The horizontal text alignment.<br>Default: `${ theme "font.align" default="left" }` |
| `color` | `string` | The text color.<br>Default: `${ theme "font.color" }` |
| `family` | `string` | An acceptable CSS web font string<br>Default: `${ theme "font.family" default="'Open Sans', Helvetica, Arial, sans-serif" }` |
| `italic` | `boolean` | Italicize the text?<br>Default: `${ theme "font.italic" default=false }` |
| `lHeight`<br>Alias: `lineHeight` | `number`, `null` | The line height in pixels<br>Default: `${ theme "font.lHeight" }` |
| `size` | `number` | The font size<br>Default: `${ theme "font.size" default=14 }` |
| `sizeUnit` | `string` | The font size unit<br>Default: `"px"` |
| `underline` | `boolean` | Underline the text?<br>Default: `${ theme "font.underline" default=false }` |
| `weight` | `string` | The font weight. For example, `"normal"`, `"bold"`, `"bolder"`, `"lighter"`, `"100"`, `"200"`, `"300"`, `"400"`, `"500"`, `"600"`, `"700"`, `"800"`, or `"900"`.<br>Default: `${ theme "font.weight" default="normal" }` |

**Returns:** `style`


### `formatdate` [formatdate_fn]

Formats an ISO8601 date string or a date in milliseconds since epoch using MomentJS. See [https://momentjs.com/docs/#/displaying/](https://momentjs.com/docs/#/displaying/).

**Expression syntax**

```js
formatdate format="YYYY-MM-DD"
formatdate "MM/DD/YYYY"
```

**Code example**

```text
kibana
| selectFilter
| demodata
| mapColumn "time" fn={getCell time | formatdate "MMM 'YY"}
| pointseries x="time" y="sum(price)" color="state"
| plot defaultStyle={seriesStyle points=5}
| render
```

This transforms the dates in the `time` field into strings that look like `"Jan ‘19"`, `"Feb ‘19"`, etc. using a MomentJS format.

**Accepts:** `number`, `string`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `format` | `string` | A MomentJS format. For example, `"MM/DD/YYYY"`. See [https://momentjs.com/docs/#/displaying/](https://momentjs.com/docs/#/displaying/). |

**Returns:** `string`


### `formatnumber` [formatnumber_fn]

Formats a number into a formatted number string using the Numeral pattern.

**Expression syntax**

```js
formatnumber format="$0,0.00"
formatnumber "0.0a"
```

**Code example**

```text
kibana
| selectFilter
| demodata
| math "mean(percent_uptime)"
| progress shape="gauge"
  label={formatnumber "0%"}
  font={font size=24 family="'Open Sans', Helvetica, Arial, sans-serif" color="#000000" align="center"}
| render
```

The `formatnumber` subexpression receives the same `context` as the `progress` function, which is the output of the `math` function. It formats the value into a percentage.

**Accepts:** `number`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `format` | `string` | A Numeral pattern format string. For example, `"0.0a"` or `"0%"`. |

**Returns:** `string`


## G [g_fns]


### `getCell` [getCell_fn]

Fetches a single cell from a `datatable`.

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Aliases: `c`, `column` | `string` | The name of the column to fetch the value from. If not provided, the value is retrieved from the first column. |
| `row`<br>Alias: `r` | `number` | The row number, starting at 0.<br>Default: `0` |

**Returns:** Depends on your input and arguments


### `gt` [gt_fn]

Returns whether the *context* is greater than the argument.

**Accepts:** `number`, `string`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `value` | `number`, `string` | The value compared to the *context*. |

**Returns:** `boolean`


### `gte` [gte_fn]

Returns whether the *context* is greater or equal to the argument.

**Accepts:** `number`, `string`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `value` | `number`, `string` | The value compared to the *context*. |

**Returns:** `boolean`


## H [h_fns]


### `head` [head_fn]

Retrieves the first N rows from the `datatable`. See also [`tail`](#tail_fn).

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `count` | `number` | The number of rows to retrieve from the beginning of the `datatable`.<br>Default: `1` |

**Returns:** `datatable`


## I [i_fns]


### `if` [if_fn]

Performs conditional logic.

**Accepts:** `any`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `condition` | `boolean` | A `true` or `false` indicating whether a condition is met, usually returned by a sub-expression. When unspecified, the original *context* is returned. |
| `else` | `any` | The return value when the condition is `false`. When unspecified and the condition is not met, the original *context* is returned. |
| `then` | `any` | The return value when the condition is `true`. When unspecified and the condition is met, the original *context* is returned. |

**Returns:** Depends on your input and arguments


### `image` [image_fn]

Displays an image. Provide an image asset as a `base64` data URL, or pass in a sub-expression.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Aliases: `dataurl`, `url` | `string`, `null` | The HTTP(S) URL or `base64` data URL of an image.<br>Default: `null` |
| `mode` | `string` | `"contain"` shows the entire image, scaled to fit. `"cover"` fills the container with the image, cropping from the sides or bottom as needed. `"stretch"` resizes the height and width of the image to 100% of the container.<br>Default: `"contain"` |

**Returns:** `image`


## J [j_fns]


### `joinRows` [joinRows_fn]

Concatenates values from rows in a `datatable` into a single string.

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `column` | `string` | The column or field from which to extract the values. |
| `distinct` | `boolean` | Extract only unique values?<br>Default: `true` |
| `quote` | `string` | The quote character to wrap around each extracted value.<br>Default: `"'"` |
| `separator`<br>Aliases: `delimiter`, `sep` | `string` | The delimiter to insert between each extracted value.<br>Default: `","` |

**Returns:** `string`


## K [k_fns]


### `kibana` [kibana_fn]

Gets kibana global context

**Accepts:** `kibana_context`, `null`

**Returns:** `kibana_context`


## L [l_fns]


### `location` [location_fn]

Find your current location using the Geolocation API of the browser. Performance can vary, but is fairly accurate. See [https://developer.mozilla.org/en-US/docs/Web/API/Navigator/geolocation](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/geolocation). Don’t use [`location`](#location_fn) if you plan to generate PDFs as this function requires user input.

**Accepts:** `null`

**Returns:** `datatable`


### `lt` [lt_fn]

Returns whether the *context* is less than the argument.

**Accepts:** `number`, `string`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `value` | `number`, `string` | The value compared to the *context*. |

**Returns:** `boolean`


### `lte` [lte_fn]

Returns whether the *context* is less than or equal to the argument.

**Accepts:** `number`, `string`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `value` | `number`, `string` | The value compared to the *context*. |

**Returns:** `boolean`


## M [m_fns]


### `mapCenter` [mapCenter_fn]

Returns an object with the center coordinates and zoom level of the map.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| `lat` * | `number` | Latitude for the center of the map |
| `lon` * | `number` | Longitude for the center of the map |
| `zoom` * | `number` | Zoom level of the map |

**Returns:** `mapCenter`


### `mapColumn` [mapColumn_fn]

Adds a column calculated as the result of other columns. Changes are made only when you provide arguments.See also [`alterColumn`](#alterColumn_fn) and [`staticColumn`](#staticColumn_fn).

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Aliases: `column`, `name` | `string` | The name of the resulting column. Names are not required to be unique. |
| `copyMetaFrom` | `string`, `null` | If set, the meta object from the specified column id is copied over to the specified target column. If the column doesn’t exist it silently fails.<br>Default: `null` |
| `expression` *<br>Aliases: `exp`, `fn`, `function` | `boolean`, `number`, `string`, `null` | An expression that is executed on every row, provided with a single-row `datatable` context and returning the cell value. |
| `id` | `string`, `null` | An optional id of the resulting column. When no id is provided, the id will be looked up from the existing column by the provided name argument. If no column with this name exists yet, a new column with this name and an identical id will be added to the table.<br>Default: `null` |

**Returns:** `datatable`


### `markdown` [markdown_fn]

Adds an element that renders Markdown text. TIP: Use the [`markdown`](#markdown_fn) function for single numbers, metrics, and paragraphs of text.

**Accepts:** `datatable`, `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* †<br>Aliases: `content`, `expression` | `string` | A string of text that contains Markdown. To concatenate, pass the `string` function multiple times.<br>Default: `""` |
| `font` | `style` | The CSS font properties for the content. For example, "font-family" or "font-weight".<br>Default: `${font}` |
| `openLinksInNewTab` | `boolean` | A true or false value for opening links in a new tab. The default value is `false`. Setting to `true` opens all links in a new tab.<br>Default: `false` |

**Returns:** `render`


### `math` [math_fn]

Interprets a `TinyMath` math expression using a `number` or `datatable` as *context*. The `datatable` columns are available by their column name. If the *context* is a number it is available as `value`.

**Accepts:** `number`, `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `expression` | `string` | An evaluated `TinyMath` expression. See [/reference/data-analysis/kibana/tinymath-functions.md](/reference/data-analysis/kibana/tinymath-functions.md). |
| `onError` | `string` | In case the `TinyMath` evaluation fails or returns NaN, the return value is specified by onError. When `'throw'`, it will throw an exception, terminating expression execution (default). |

**Returns:** Depends on your input and arguments


### `mathColumn` [mathColumn_fn]

Adds a column by evaluating `TinyMath` on each row. This function is optimized for math and performs better than using a math expression in [`mapColumn`](#mapColumn_fn).

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Aliases: `column`, `name` | `string` | The name of the resulting column. Names are not required to be unique. |
| *Unnamed*<br>Alias: `expression` | `string` | An evaluated `TinyMath` expression. See [/reference/data-analysis/kibana/tinymath-functions.md](/reference/data-analysis/kibana/tinymath-functions.md). |
| `castColumns` † | `string` | The column ids that are cast to numbers before the formula is applied. |
| `copyMetaFrom` | `string`, `null` | If set, the meta object from the specified column id is copied over to the specified target column. If the column doesn’t exist it silently fails.<br>Default: `null` |
| `id` * | `string` | id of the resulting column. Must be unique. |
| `onError` | `string` | In case the `TinyMath` evaluation fails or returns NaN, the return value is specified by onError. When `'throw'`, it will throw an exception, terminating expression execution (default). |

**Returns:** `datatable`


### `metric` [metric_fn]

Displays a number over a label.

**Accepts:** `number`, `string`, `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Aliases: `description`, `label`, `text` | `string` | The text describing the metric.<br>Default: `""` |
| `labelFont` | `style` | The CSS font properties for the label. For example, `font-family` or `font-weight`.<br>Default: `${font size=14 family="'Open Sans', Helvetica, Arial, sans-serif" color="#000000" align=center}` |
| `metricFont` | `style` | The CSS font properties for the metric. For example, `font-family` or `font-weight`.<br>Default: `${font size=48 family="'Open Sans', Helvetica, Arial, sans-serif" color="#000000" align=center lHeight=48}` |
| `metricFormat`<br>Alias: `format` | `string` | A Numeral pattern format string. For example, `"0.0a"` or `"0%"`. |

**Returns:** `render`


## N [n_fns]


### `neq` [neq_fn]

Returns whether the *context* is not equal to the argument.

**Accepts:** `boolean`, `number`, `string`, `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `value` | `boolean`, `number`, `string`, `null` | The value compared to the *context*. |

**Returns:** `boolean`


## P [p_fns]


### `palette` [palette_fn]

Creates a color palette.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* †<br>Alias: `color` | `string` | The palette colors. Accepts an HTML color name, HEX, HSL, HSLA, RGB, or RGBA. |
| `continuity` | `string` | Default: `"above"` |
| `gradient` | `boolean` | Make a gradient palette where supported?<br>Default: `false` |
| `range` | `string` | Default: `"percent"` |
| `rangeMax` | `number` |  |
| `rangeMin` | `number` |  |
| `reverse` | `boolean` | Reverse the palette?<br>Default: `false` |
| `stop` † | `number` | The palette color stops. When used, it must be associated with each color. |

**Returns:** `palette`


### `pie` [pie_fn]

Configures a pie chart element.

**Accepts:** `pointseries`

| Argument | Type | Description |
| --- | --- | --- |
| `font` | `style` | The CSS font properties for the labels. For example, `font-family` or `font-weight`.<br>Default: `${font}` |
| `hole` | `number` | Draws a hole in the pie, between `0` and `100`, as a percentage of the pie radius.<br>Default: `0` |
| `labelRadius` | `number` | The percentage of the container area to use as a radius for the label circle.<br>Default: `100` |
| `labels` | `boolean` | Display the pie labels?<br>Default: `true` |
| `legend` | `string`, `boolean` | The legend position. For example, `"nw"`, `"sw"`, `"ne"`, `"se"`, or `false`. When `false`, the legend is hidden.<br>Default: `false` |
| `palette` | `palette` | A `palette` object for describing the colors to use in this pie chart.<br>Default: `${palette}` |
| `radius` | `string`, `number` | The radius of the pie as a percentage, between `0` and `1`, of the available space. To automatically set the radius, use `"auto"`.<br>Default: `"auto"` |
| `seriesStyle` † | `seriesStyle` | A style of a specific series |
| `tilt` | `number` | The percentage of tilt where `1` is fully vertical, and `0` is completely flat.<br>Default: `1` |

**Returns:** `render`


### `plot` [plot_fn]

Configures a chart element.

**Accepts:** `pointseries`

| Argument | Type | Description |
| --- | --- | --- |
| `defaultStyle` | `seriesStyle` | The default style to use for every series.<br>Default: `${seriesStyle points=5}` |
| `font` | `style` | The CSS font properties for the labels. For example, `font-family` or `font-weight`.<br>Default: `${font}` |
| `legend` | `string`, `boolean` | The legend position. For example, `"nw"`, `"sw"`, `"ne"`, `"se"`, or `false`. When `false`, the legend is hidden.<br>Default: `"ne"` |
| `palette` | `palette` | A `palette` object for describing the colors to use in this chart.<br>Default: `${palette}` |
| `seriesStyle` † | `seriesStyle` | A style of a specific series |
| `xaxis` | `boolean`, `axisConfig` | The axis configuration. When `false`, the axis is hidden.<br>Default: `true` |
| `yaxis` | `boolean`, `axisConfig` | The axis configuration. When `false`, the axis is hidden.<br>Default: `true` |

**Returns:** `render`


### `ply` [ply_fn]

Subdivides a `datatable` by the unique values of the specified columns, and passes the resulting tables into an expression, then merges the outputs of each expression.

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| `by` † | `string` | The column to subdivide the `datatable`. |
| `expression` †<br>Aliases: `exp`, `fn`, `function` | `datatable` | An expression to pass each resulting `datatable` into. Tips: Expressions must return a `datatable`. Use [`as`](#as_fn) to turn literals into `datatable`s. Multiple expressions must return the same number of rows.If you need to return a different row count, pipe into another instance of [`ply`](#ply_fn). If multiple expressions returns the columns with the same name, the last one wins. |

**Returns:** `datatable`


### `pointseries` [pointseries_fn]

Turn a `datatable` into a point series model. Currently we differentiate measure from dimensions by looking for a `TinyMath` expression. See [/reference/data-analysis/kibana/tinymath-functions.md](/reference/data-analysis/kibana/tinymath-functions.md). If you enter a `TinyMath` expression in your argument, we treat that argument as a measure, otherwise it is a dimension. Dimensions are combined to create unique keys. Measures are then deduplicated by those keys using the specified `TinyMath` function

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| `color` | `string` | An expression to use in determining the mark’s color. |
| `size` | `string` | The size of the marks. Only applicable to supported elements. |
| `text` | `string` | The text to show on the mark. Only applicable to supported elements. |
| `x` | `string` | The values along the X-axis. |
| `y` | `string` | The values along the Y-axis. |

**Returns:** `pointseries`


### `progress` [progress_fn]

Configures a progress element.

**Accepts:** `number`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `shape` | `string` | Select `"gauge"`, `"horizontalBar"`, `"horizontalPill"`, `"semicircle"`, `"unicorn"`, `"verticalBar"`, `"verticalPill"`, or `"wheel"`.<br>Default: `"gauge"` |
| `barColor` | `string` | The color of the background bar.<br>Default: `"#f0f0f0"` |
| `barWeight` | `number` | The thickness of the background bar.<br>Default: `20` |
| `font` | `style` | The CSS font properties for the label. For example, `font-family` or `font-weight`.<br>Default: `${font size=24 family="'Open Sans', Helvetica, Arial, sans-serif" color="#000000" align=center}` |
| `label` | `boolean`, `string` | To show or hide the label, use `true` or `false`. Alternatively, provide a string to display as a label.<br>Default: `true` |
| `max` | `number` | The maximum value of the progress element.<br>Default: `1` |
| `valueColor` | `string` | The color of the progress bar.<br>Default: `"#1785b0"` |
| `valueWeight` | `number` | The thickness of the progress bar.<br>Default: `20` |

**Returns:** `render`


## R [r_fns]


### `removeFilter` [removeFilter_fn]

Removes filters from context

**Accepts:** `kibana_context`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `group` | `string` | Removes only filters belonging to the provided group |
| `from` | `string` | Removes only filters owned by the provided id |
| `ungrouped`<br>Aliases: `nogroup`, `nogroups` | `boolean` | Should filters without group be removed<br>Default: `false` |

**Returns:** `kibana_context`


### `render` [render_fn]

Renders the *context* as a specific element and sets element level options, such as background and border styling.

**Accepts:** `render`

| Argument | Type | Description |
| --- | --- | --- |
| `as` | `string` | The element type to render. You probably want a specialized function instead, such as [`plot`](#plot_fn) or [`shape`](#shape_fn). |
| `containerStyle` | `containerStyle` | The style for the container, including background, border, and opacity.<br>Default: `${containerStyle}` |
| `css` | `string` | Any block of custom CSS to be scoped to the element.<br>Default: `".canvasRenderEl${}"` |

**Returns:** `render`


### `repeatImage` [repeatImage_fn]

Configures a repeating image element.

**Accepts:** `number`

| Argument | Type | Description |
| --- | --- | --- |
| `emptyImage` | `string`, `null` | Fills the difference between the *context* and `max` parameter for the element with this image. Provide an image asset as a `base64` data URL, or pass in a sub-expression.<br>Default: `null` |
| `image` | `string`, `null` | The image to repeat. Provide an image asset as a `base64` data URL, or pass in a sub-expression.<br>Default: `null` |
| `max` | `number`, `null` | The maximum number of times the image can repeat.<br>Default: `1000` |
| `size` | `number` | The maximum height or width of the image, in pixels. When the image is taller than it is wide, this function limits the height.<br>Default: `100` |

**Returns:** `render`


### `replace` [replace_fn]

Uses a regular expression to replace parts of a string.

**Accepts:** `string`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Aliases: `pattern`, `regex` | `string` | The text or pattern of a JavaScript regular expression. For example, `"[aeiou]"`. You can use capturing groups here. |
| `flags`<br>Alias: `modifiers` | `string` | Specify flags. See [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp).<br>Default: `"g"` |
| `replacement` | `string` | The replacement for the matching parts of string. Capturing groups can be accessed by their index. For example, `"$1"`.<br>Default: `""` |

**Returns:** `string`


### `revealImage` [revealImage_fn]

Configures an image reveal element.

**Accepts:** `number`

| Argument | Type | Description |
| --- | --- | --- |
| `emptyImage` | `string`, `null` | An optional background image to reveal over. Provide an image asset as a ``base64`` data URL, or pass in a sub-expression.<br>Default: `null` |
| `image` | `string`, `null` | The image to reveal. Provide an image asset as a `base64` data URL, or pass in a sub-expression.<br>Default: `null` |
| `origin` | `string` | The position to start the image fill. For example, `"top"`, `"bottom"`, `"left"`, or right.<br>Default: `"bottom"` |

**Returns:** `render`


### `rounddate` [rounddate_fn]

Uses a MomentJS formatting string to round milliseconds since epoch, and returns milliseconds since epoch.

**Accepts:** `number`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `format` | `string` | The MomentJS format to use for bucketing. For example, `"YYYY-MM"` rounds to months. See [https://momentjs.com/docs/#/displaying/](https://momentjs.com/docs/#/displaying/). |

**Returns:** `number`


### `rowCount` [rowCount_fn]

Returns the number of rows. Pairs with [`ply`](#ply_fn) to get the count of unique column values, or combinations of unique column values.

**Accepts:** `datatable`

**Returns:** `number`


## S [s_fns]


### `selectFilter` [selectFilter_fn]

Selects filters from context

**Accepts:** `kibana_context`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* †<br>Alias: `group` | `string` | Select only filters belonging to the provided group |
| `from` | `string` | Select only filters owned by the provided id |
| `ungrouped`<br>Aliases: `nogroup`, `nogroups` | `boolean` | Should filters without group be included<br>Default: `false` |

**Returns:** `kibana_context`


### `seriesStyle` [seriesStyle_fn]

Creates an object used for describing the properties of a series on a chart. Use [`seriesStyle`](#seriesStyle_fn) inside of a charting function, like [`plot`](#plot_fn) or [`pie`](#pie_fn).

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| `bars` | `number` | The width of bars. |
| `color` | `string` | The line color. |
| `fill` | `number`, `boolean` | Should we fill in the points?<br>Default: `false` |
| `horizontalBars` | `boolean` | Sets the orientation of the bars in the chart to horizontal. |
| `label` | `string` | The name of the series to style. |
| `lines` | `number` | The width of the line. |
| `points` | `number` | The size of points on line. |
| `stack` | `number`, `null` | Specifies if the series should be stacked. The number is the stack ID. Series with the same stack ID are stacked together. |

**Returns:** `seriesStyle`


### `shape` [shape_fn]

Creates a shape.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `shape` | `string` | Pick a shape.<br>Default: `"square"` |
| `border`<br>Alias: `stroke` | `string` | An SVG color for the border outlining the shape. |
| `borderWidth`<br>Alias: `strokeWidth` | `number` | The thickness of the border.<br>Default: `0` |
| `fill` | `string` | An SVG color to fill the shape.<br>Default: `"black"` |
| `maintainAspect` | `boolean` | Maintain the shape’s original aspect ratio?<br>Default: `false` |

**Returns:** Depends on your input and arguments


### `sort` [sort_fn]

Sorts a `datatable` by the specified column.

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Aliases: `by`, `column` | `string` | The column to sort by. When unspecified, the `datatable` is sorted by the first column. |
| `reverse` | `boolean` | Reverses the sorting order. When unspecified, the `datatable` is sorted in ascending order.<br>Default: `false` |

**Returns:** `datatable`


### `staticColumn` [staticColumn_fn]

Adds a column with the same static value in every row. See also [`alterColumn`](#alterColumn_fn), [`mapColumn`](#mapColumn_fn), and [`mathColumn`](#mathColumn_fn)

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Aliases: `column`, `name` | `string` | The name of the new column. |
| `value` | `string`, `number`, `boolean`, `null` | The value to insert in each row in the new column. TIP: use a sub-expression to rollup other columns into a static value.<br>Default: `null` |

**Returns:** `datatable`


### `string` [string_fn]

Concatenates all of the arguments into a single string.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* †<br>Alias: `value` | `string`, `number`, `boolean` | The values to join together into one string. Include spaces where needed. |

**Returns:** `string`


### `switch` [switch_fn]

Performs conditional logic with multiple conditions. See also [`case`](#case_fn), which builds a `case` to pass to the [`switch`](#switch_fn) function.

**Accepts:** `any`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* * †<br>Alias: `case` | `case` | The conditions to check. |
| `default`<br>Alias: `finally` | `any` | The value returned when no conditions are met. When unspecified and no conditions are met, the original *context* is returned. |

**Returns:** Depends on your input and arguments


## T [t_fns]


### `table` [table_fn]

Configures a table element.

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| `font` | `style` | The CSS font properties for the contents of the table. For example, `font-family` or `font-weight`.<br>Default: `${font}` |
| `paginate` | `boolean` | Show pagination controls? When `false`, only the first page is displayed.<br>Default: `true` |
| `perPage` | `number` | The number of rows to display on each page.<br>Default: `10` |
| `showHeader` | `boolean` | Show or hide the header row with titles for each column.<br>Default: `true` |

**Returns:** `render`


### `tail` [tail_fn]

Retrieves the last N rows from the end of a `datatable`. See also [`head`](#head_fn).

**Accepts:** `datatable`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Alias: `count` | `number` | The number of rows to retrieve from the end of the `datatable`.<br>Default: `1` |

**Returns:** `datatable`


### `timefilter` [timefilter_fn]

Creates a time filter for querying a source.

**Accepts:** `filter`

| Argument | Type | Description |
| --- | --- | --- |
| `column`<br>Aliases: `c`, `field` | `string` | The column or field that you want to filter.<br>Default: `"@timestamp"` |
| `filterGroup` | `string` | The group name for the filter |
| `from`<br>Aliases: `f`, `start` | `string` | The beginning of the range, in ISO8601 or Elasticsearch `datemath` format |
| `to`<br>Aliases: `end`, `t` | `string` | The end of the range, in ISO8601 or Elasticsearch `datemath` format |

**Returns:** `filter`


### `timefilterControl` [timefilterControl_fn]

Configures a time filter control element.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| `column`<br>Aliases: `c`, `field` | `string` | The column or field that you want to filter.<br>Default: `"@timestamp"` |
| `compact` | `boolean` | Shows the time filter as a button, which triggers a popover.<br>Default: `true` |
| `filterGroup` | `string` | The group name for the filter. |

**Returns:** `render`


### `timelion` [timelion_fn]

Uses Timelion to extract one or more time series from many sources.

**Accepts:** `filter`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed*<br>Aliases: `q`, `query` | `string` | A Timelion query<br>Default: `".es(*)"` |
| `from` | `string` | The Elasticsearch `datemath` string for the beginning of the time range.<br>Default: `"now-1y"` |
| `interval` | `string` | The bucket interval for the time series.<br>Default: `"auto"` |
| `timezone` | `string` | The timezone for the time range. See [https://momentjs.com/timezone/](https://momentjs.com/timezone/).<br>Default: `"UTC"` |
| `to` | `string` | The Elasticsearch `datemath` string for the end of the time range.<br>Default: `"now"` |

**Returns:** `datatable`


### `timerange` [timerange_fn]

An object that represents a span of time.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| `from` * | `string` | The start of the time range |
| `to` * | `string` | The end of the time range |

**Returns:** `timerange`


### `to` [to_fn]

Explicitly casts the type of the *context* from one type to the specified type.

**Accepts:** `any`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* †<br>Alias: `type` | `string` | A known data type in the expression language. |

**Returns:** Depends on your input and arguments


## U [u_fns]


### `uiSetting` [uiSetting_fn]

Returns a UI settings parameter value.

**Accepts:** `any`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `parameter` | `string` | The parameter name. |
| `default` | `any` | A default value in case of the parameter is not set. |

**Returns:** Depends on your input and arguments


### `urlparam` [urlparam_fn]

Retrieves a URL parameter to use in an expression. The [`urlparam`](#urlparam_fn) function always returns a `string`. For example, you can retrieve the value `"20"` from the parameter `myVar` from the URL `https://localhost:5601/app/canvas?myVar=20`.

**Accepts:** `null`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Aliases: `param`, `var`, `variable` | `string` | The URL hash parameter to retrieve. |
| `default` | `string` | The string returned when the URL parameter is unspecified.<br>Default: `""` |

**Returns:** `string`


## V [v_fns]


### `var` [var_fn]

Updates the Kibana global context.

**Accepts:** `any`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* *<br>Alias: `name` | `string` | Specify the name of the variable. |

**Returns:** Depends on your input and arguments


### `var_set` [var_set_fn]

Updates the Kibana global context.

**Accepts:** `any`

| Argument | Type | Description |
| --- | --- | --- |
| *Unnamed* * †<br>Alias: `name` | `string` | Specify the name of the variable. |
| `value` †<br>Alias: `val` | `any` | Specify the value for the variable. When unspecified, the input context is used. |

**Returns:** Depends on your input and arguments


