---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/canvas-tinymath-functions.html
type: reference
description: Look up the TinyMath functions you can use in Canvas expressions, with the parameters, return value, errors, and an example for each.
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
---

# TinyMath functions [canvas-tinymath-functions]

Use TinyMath functions to do math in the [Canvas expression language](canvas-function-reference.md), from rounding and averages to trigonometry and comparisons. The [`EvalMath` lambda](../../alerting/alerts/rule-action-variables.md#_evalmath) in alert action templates accepts the same functions.

Most of the functions accept arrays and apply JavaScript Math methods to each element of that array. For the functions that accept multiple arrays as parameters, the function generally does the calculation index by index.

An expression can't contain an array directly. Arrays come from the data that the expression runs on, such as the columns of a datatable. The examples with arrays show what each function returns for those values.

If you pass a single array to `add`, `max`, `mean`, `median`, `min`, `mode`, or `range`, the function summarizes the whole array instead of working by index. For example, `mean` of a column returns the average of that column.

If a value isn't a number, such as null, most functions return `NaN`. The exceptions, which don't check that values are numbers, are `count`, `defaults`, `first`, `ifelse`, `last`, `size`, and `unique`. To replace null values before you calculate, use [`defaults`](#_defaults_a_b). For example, if `prices` is `[1, null]`, `abs(prices)` returns `NaN`, while `abs(defaults(prices, 0))` returns `[1, 0]`.

You can wrap any function in another function as long as the return type of the inner function matches the parameter type of the outer function.

:::{note}
:applies_to: {"serverless": "ga", "stack": "ga 9.4+"}
A TinyMath expression can contain up to 20 levels of nested parentheses. The expression can be up to 8,192 characters, not counting quoted text, such as a quoted column name or a Kibana Query Language (KQL) or Lucene filter. TinyMath rejects expressions that exceed these limits before it parses them. Typical expressions stay well within these limits.
:::

## Expression syntax

An expression combines numbers, variables, operators, and function calls, such as `round(price * 1.2, 2)`. A variable is a value from the data that the expression runs on, such as a datatable column in Canvas or a field in an alert action template.

| To do this | Write this | Notes |
| --- | --- | --- |
| Calculate | `+`, `-`, `*`, `/`, and parentheses, as in `(2 + 3) * 4` | `*` and `/` run before `+` and `-`. Operators of the same rank run from left to right. `^` and `%` aren't supported, so use [`pow`](#_pow_a_b) and [`mod`](#_mod_a_b). |
| Write a number | `10`, `-10`, `1.5`, or `1e3` | Write `0.5`, not `.5`. Leading zeros and a leading `+` aren't accepted. |
| Subtract or negate a variable | `a - b` or `0 - x` | Put spaces around `-`. TinyMath reads `a-b` as one variable named `a-b`, and `-x` as one variable named `-x`. |
| Use a value from the data | `price` or `context.value` | Names are case-sensitive. A dot reads a nested value, so `context.value` reads `value` inside `context`. A name can contain letters, digits, `_`, `.`, `@`, and `-`, but can't start with a digit. |
| Use a name with spaces or other characters | `"sales total"` or `'sales total'` | Quote a name that contains a space, starts with a digit, or contains a character such as `+`. |
| Call a function | `round(x, 2)` | Put `(` right after the function name, with no space. Separate arguments with commas. An argument can be an expression, as in `add(1 + 2, 3 * 4)`. Function names are case-sensitive and can't contain digits. |
| Compare values | `<`, `<=`, `>`, `>=`, `==` | `!=`, `=`, and `===` aren't supported. A comparison gives `true` or `false`. Use it on its own, in parentheses, or as a function argument, as in `ifelse(x > 1, 10, 20)`. You can't chain comparisons or use the result in arithmetic. |

Each operator gives the same result as the function with the same meaning, including for arrays and when an error occurs. `+` matches [`add`](#_add_args), `-` matches [`subtract`](#_subtract_a_b), `*` matches [`multiply`](#_multiply_a_b), `/` matches [`divide`](#_divide_a_b), `<` matches [`lt`](#_lt_a_b), `<=` matches [`lte`](#_lte_a_b), `>` matches [`gt`](#_gt_a_b), `>=` matches [`gte`](#_gte_a_b), and `==` matches [`eq`](#_eq_a_b).

You can't write `null`, `true`, or `false`. TinyMath reads those words as variable names. To replace null values in your data, use [`defaults`](#_defaults_a_b).

## Functions by task

| Task | Functions |
| --- | --- |
| Arithmetic | [`add`](#_add_args), [`subtract`](#_subtract_a_b), [`multiply`](#_multiply_a_b), [`divide`](#_divide_a_b), [`mod`](#_mod_a_b), [`pow`](#_pow_a_b), [`abs`](#_abs_a), [`exp`](#_exp_a), [`log`](#_log_a_b), [`log10`](#_log10_a) (call it as `log(a, 10)`), [`sqrt`](#_sqrt_a), [`cbrt`](#_cbrt_a), [`square`](#_square_a), [`cube`](#_cube_a) |
| Rounding | [`ceil`](#_ceil_a), [`floor`](#_floor_a), [`fix`](#_fix_a), [`round`](#_round_a_b) |
| Summarize numbers or arrays | [`sum`](#_sum_args), [`mean`](#_mean_args), [`median`](#_median_args), [`mode`](#_mode_args), [`min`](#_min_args), [`max`](#_max_args), [`range`](#_range_args), [`count`](#_count_a), [`size`](#_size_a), [`unique`](#_unique_a), [`first`](#_first_a), [`last`](#_last_a) |
| Limits and random numbers | [`clamp`](#_clamp_a_min_max), [`random`](#_random_a_b) |
| Trigonometry and constants | [`sin`](#_sin_a), [`cos`](#_cos_a), [`tan`](#_tan_a), [`degtorad`](#_degtorad_a), [`radtodeg`](#_radtodeg_a), [`pi`](#_pi) |
| Comparisons and conditions | [`eq`](#_eq_a_b), [`gt`](#_gt_a_b), [`gte`](#_gte_a_b), [`lt`](#_lt_a_b), [`lte`](#_lte_a_b), [`ifelse`](#_ifelse_cond_a_b), [`defaults`](#_defaults_a_b) |


## abs( a ) [_abs_a] 

Calculates the absolute value of a number. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The absolute value of `a`. Returns an array with the absolute values of each element if `a` is an array.

**Example**

```js
abs(-1) // returns 1
abs(2) // returns 2
abs([-1, -2, 3, -4]) // returns [1, 2, 3, 4]
```


## add( …args ) [_add_args] 

Calculates the sum of one or more numbers or arrays. If you pass several arguments and at least one is an array, the function calculates the sum by index.

| Param | Type | Description |
| --- | --- | --- |
| …args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The sum of all numbers in `args` if `args` contains only numbers. Returns an array of sums of the elements at each index, including all scalar numbers in `args` in the calculation at each index if you pass several arguments and at least one is an array. If you pass a single array, the result covers every element.

**Throws**: `'Array length mismatch'` if `args` contains arrays of different lengths

**Example**

```js
add(1, 2, 3) // returns 6
add([10, 20, 30, 40], 10, 20, 30) // returns [70, 80, 90, 100]
add([1, 2], 3, [4, 5], 6) // returns [(1 + 3 + 4 + 6), (2 + 3 + 5 + 6)] = [14, 16]
add([1, 2, 3]) // returns 6
```


## cbrt( a ) [_cbrt_a] 

Calculates the cube root of a number. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The cube root of `a`. Returns an array with the cube roots of each element if `a` is an array.

**Example**

```js
cbrt(-27) // returns -3
cbrt(94) // returns 4.546835943776344
cbrt([27, 64, 125]) // returns [3, 4, 5]
```


## ceil( a ) [_ceil_a] 

Calculates the ceiling of a number, that is, rounds a number toward positive infinity. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The ceiling of `a`. Returns an array with the ceilings of each element if `a` is an array.

**Example**

```js
ceil(1.2) // returns 2
ceil(-1.8) // returns -1
ceil([1.1, 2.2, 3.3]) // returns [2, 3, 4]
```


## clamp( a, min, max ) [_clamp_a_min_max]

Restricts a value to a given range. Returns `min` if the value is below it, `max` if the value is above it, and the value itself otherwise. To limit a value on one side only, use the [`max`](#_max_args) function for a lower limit or the [`min`](#_min_args) function for an upper limit. For example, `max(value, 5)` returns at least 5, and `min(value, 5)` returns at most 5.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| min | number &#124; Array.<number> | the minimum value this function returns |
| max | number &#124; Array.<number> | the maximum value this function returns |

**Returns**: `number` | `Array.<number>`. The closest value between `min` (inclusive) and `max` (inclusive). Returns an array with values greater than or equal to `min` and less than or equal to `max` at each index if `a`, `min`, or `max` is an array. If you leave out `min` or `max`, the result is `NaN`, or an array of `NaN` values if `a` is an array.

**Throws**:

* `'Array length mismatch'` if `a`, `min`, or `max` are arrays of different lengths
* `'Min must be less than max'` if `max` is less than `min`

**Example**

```js
clamp(1, 2, 3) // returns 2
clamp([10, 20, 30, 40], 15, 25) // returns [15, 20, 25, 25]
clamp(10, [15, 2, 4, 20], 25) // returns [15, 10, 10, 20]
clamp(35, 10, [20, 30, 40, 50]) // returns [20, 30, 35, 35]
clamp([1, 9], 3, [4, 5]) // returns [clamp([1, 3, 4]), clamp([9, 3, 5])] = [3, 5]
```


## cos( a ) [_cos_a]

Calculates the cosine of a number. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers in radians |

**Returns**: `number` | `Array.<number>`. The cosine of `a`. Returns an array with the cosine of each element if `a` is an array.

**Example**

```js
cos(0) // returns 1
cos(1.5707963267948966) // returns 6.123233995736766e-17
cos([0, 1.5707963267948966]) // returns [1, 6.123233995736766e-17]
```


## count( a ) [_count_a] 

Returns the length of an array. Alias for [`size`](#_size_a).

| Param | Type | Description |
| --- | --- | --- |
| a | Array.<any> | array of any values |

**Returns**: `number`. The length of the array.

**Throws**: `'Must pass an array'` if `a` is not an array.

**Example**

```js
count([]) // returns 0
count([-1, -2, -3, -4]) // returns 4
```


## cube( a ) [_cube_a] 

Calculates the cube of a number. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The cube of `a`. Returns an array with the cubes of each element if `a` is an array.

**Example**

```js
cube(-3) // returns -27
cube([3, 4, 5]) // returns [27, 64, 125]
```


## defaults( a, b ) [_defaults_a_b]

Replaces null values with a fallback value. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | any &#124; Array.<any> | a value or an array of values that can include null |
| b | any | the value to use in place of null |

**Returns**: `any` | `Array.<any>`. `a` if it isn't null, otherwise `b`. Returns an array with `b` in place of each null element if `a` is an array.

**Example**

```js
defaults(5, 1) // returns 5
defaults(value, 1) // returns 1 if value is null
defaults(prices, 0) // returns [3, 0, 5] if prices is [3, null, 5]
```


## degtorad( a ) [_degtorad_a]

Converts degrees to radians. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers in degrees |

**Returns**: `number` | `Array.<number>`. `a` converted to radians. Returns an array with each element converted to radians if `a` is an array.

**Example**

```js
degtorad(0) // returns 0
degtorad(90) // returns 1.5707963267948966
degtorad([0, 90, 180, 360]) // returns [0, 1.5707963267948966, 3.141592653589793, 6.283185307179586]
```


## divide( a, b ) [_divide_a_b] 

Divides two numbers. If either argument is an array, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | dividend, a number or an array of numbers |
| b | number &#124; Array.<number> | divisor, a number or an array of numbers, b != 0 |

**Returns**: `number` | `Array.<number>`. Returns the quotient of `a` and `b` if both are numbers. Returns an array with the quotients applied index-wise to each element if `a` or `b` is an array.

**Throws**:

* `'Array length mismatch'` if `a` and `b` are arrays with different lengths
* `'Cannot divide by 0'` if `b` equals 0 or contains 0

**Example**

```js
divide(6, 3) // returns 2
divide([10, 20, 30, 40], 10) // returns [1, 2, 3, 4]
divide(10, [1, 2, 5, 10]) // returns [10, 5, 2, 1]
divide([14, 42, 65, 108], [2, 7, 5, 12]) // returns [7, 6, 13, 9]
```


## eq( a, b ) [_eq_a_b]

Checks whether two values are equal. For arrays, the function returns `true` only if every element is equal. You can also write this comparison as `a == b`.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| b | number &#124; Array.<number> | a number, or, if `a` is also an array, an array of numbers with the same length as `a` |

**Returns**: `boolean`. `true` if `a` and `b` are equal, `false` otherwise. If `a` is an array, returns `true` only if every element of `a` equals `b`, or equals the element at the same index of `b` if `b` is an array.

**Throws**:

* `'Missing b value'` if `b` is not provided
* `'Array length mismatch'` if `a` and `b` are arrays of different lengths

**Example**

```js
eq(1, 1) // returns true
eq(1, 2) // returns false
eq([1, 1], 1) // returns true
eq([1, 2], 1) // returns false
eq([1, 2], [1, 2]) // returns true
```


## exp( a ) [_exp_a] 

Calculates *e^x* where *e* is Euler's number. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. Returns an array with the values of `e^x` evaluated where `x` is each element of `a` if `a` is an array.

**Example**

```js
exp(2) // returns e^2 = 7.38905609893065
exp([1, 2, 3]) // returns [e^1, e^2, e^3] = [2.718281828459045, 7.38905609893065, 20.085536923187668]
```


## first( a ) [_first_a] 

Returns the first element of an array. If `a` isn't an array, the function returns `a`.

| Param | Type | Description |
| --- | --- | --- |
| a | any &#124; Array.<any> | a value or an array of values |

**Returns**: `*`. The first element of `a`. Returns `a` if `a` is not an array.

**Example**

```js
first(2) // returns 2
first([1, 2, 3]) // returns 1
```


## fix( a ) [_fix_a] 

Calculates the fix of a number, that is, rounds a number toward 0. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The fix of `a`. Returns an array with the fixes for each element if `a` is an array.

**Example**

```js
fix(1.2) // returns 1
fix(-1.8) // returns -1
fix([1.8, 2.9, -3.7, -4.6]) // returns [1, 2, -3, -4]
```


## floor( a ) [_floor_a] 

Calculates the floor of a number, that is, rounds a number toward negative infinity. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The floor of `a`. Returns an array with the floor of each element if `a` is an array.

**Example**

```js
floor(1.8) // returns 1
floor(-1.2) // returns -2
floor([1.7, 2.8, 3.9]) // returns [1, 2, 3]
```


## gt( a, b ) [_gt_a_b]

Checks whether one value is greater than another. For arrays, the function returns `true` only if every element is greater. You can also write this comparison as `a > b`.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| b | number &#124; Array.<number> | a number, or, if `a` is also an array, an array of numbers with the same length as `a` |

**Returns**: `boolean`. `true` if `a` is greater than `b`, `false` otherwise. If `a` is an array, returns `true` only if every element of `a` is greater than `b`, or greater than the element at the same index of `b` if `b` is an array.

**Throws**:

* `'Missing b value'` if `b` is not provided
* `'Array length mismatch'` if `a` and `b` are arrays of different lengths

**Example**

```js
gt(1, 1) // returns false
gt(2, 1) // returns true
gt([2, 3], 1) // returns true
gt([1, 2], 1) // returns false
gt([1, 2], [0, 1]) // returns true
```


## gte( a, b ) [_gte_a_b]

Checks whether one value is greater than or equal to another. You can also write this comparison as `a >= b`.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| b | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `boolean`. `true` if `a` is greater than or equal to `b`, `false` otherwise.

The result for arrays depends on the version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` If `a` or `b` is an array, returns `true` only if every element satisfies the comparison.
- {applies_to}`stack: ga 9.0-9.4` If `a` is an array, returns `true` only if every element is equal to the other value, or every element is greater.

**Throws**:

* `'Missing b value'` if `b` is not provided
* `'Array length mismatch'` if `a` and `b` are arrays of different lengths

**Example**

```js
gte(1, 1) // returns true
gte(1, 2) // returns false
gte([1, 2], 2) // returns false
```

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` More array comparisons:

```js
gte([1, 2], [1, 1]) // returns true
gte(2, [1, 2]) // returns true
```

{applies_to}`stack: ga 9.0-9.4` More array comparisons:

```js
gte([1, 2], [1, 1]) // returns false
gte(2, [1, 2]) // returns false
```


## ifelse( cond, a, b ) [_ifelse_cond_a_b]

Returns one of two values, depending on a condition.

| Param | Type | Description |
| --- | --- | --- |
| cond | boolean | a condition, such as `5 > 6` or the result of a comparison function |
| a | any &#124; Array.<any> | the value to return if `cond` is true |
| b | any &#124; Array.<any> | the value to return if `cond` is false |

**Returns**: `any` | `Array.<any>`. `a` if `cond` is true, otherwise `b`. TinyMath evaluates both `a` and `b` first, so an error in either one stops the expression. For example, `ifelse(5 < 6, 1, 1 / 0)` throws `'Cannot divide by 0'`. Comparing arrays gives one boolean. `ifelse` therefore picks one value for the whole array, not one per element.

**Throws**:

* `'Condition clause is of the wrong type'` if `cond` is not a boolean
* `'Missing a value'` if `a` is not provided
* `'Missing b value'` if `b` is not provided

**Example**

```js
ifelse(5 > 6, 1, 0) // returns 0
ifelse(1 == 1, 7, 5) // returns 7
ifelse(1 < 2, [1, 2, 3], [2, 3, 4]) // returns [1, 2, 3]
ifelse(gt([0, 3], 1), 10, 20) // returns 20
```


## last( a ) [_last_a] 

Returns the last element of an array. If `a` isn't an array, the function returns `a`.

| Param | Type | Description |
| --- | --- | --- |
| a | any &#124; Array.<any> | a value or an array of values |

**Returns**: `*`. The last element of `a`. Returns `a` if `a` is not an array.

**Example**

```js
last(2) // returns 2
last([1, 2, 3]) // returns 3
```


## log( a, b ) [_log_a_b]

Calculates the logarithm of a number. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers that can't be negative |
| b | number | (optional) the base of the logarithm. If you don't provide a base, the function uses e and calculates the natural logarithm. |

**Returns**: `number` | `Array.<number>`. The logarithm of `a`. Returns an array with the logarithms of each element if `a` is an array.

**Throws**:

* `'Base out of range'` if `b` is less than or equal to 0
* `'Must be greater than 0'` if `a` < 0

**Example**

```js
log(1) // returns 0
log(64, 8) // returns 2
log(42, 5) // returns 2.322344707681546
log([2, 4, 8, 16, 32], 2) // returns [1, 2, 3, 4, 5]
```


## log10( a ) [_log10_a]

Calculates the base 10 logarithm of a number. For arrays, the function applies to each element.

Expressions don't accept the name `log10`, because function names can't contain digits. To calculate a base 10 logarithm, use `log` with a base of 10, as in the examples.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers that can't be negative |

**Returns**: `number` | `Array.<number>`. The base 10 logarithm of `a`. Returns an array with the base 10 logarithms of each element if `a` is an array. The result can differ from the exact value in the last digits, as in `log(1000, 10)`, which returns `2.9999999999999996`.

**Throws**: `'Must be greater than 0'` if `a` < 0

**Example**

```js
log(10, 10) // returns 1
log(100, 10) // returns 2
log(80, 10) // returns 1.9030899869919433
log([10, 100, 10000, 100000], 10) // returns [1, 2, 4, 5]
```


## lt( a, b ) [_lt_a_b]

Checks whether one value is less than another. For arrays, the function returns `true` only if every element is less. You can also write this comparison as `a < b`.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| b | number &#124; Array.<number> | a number, or, if `a` is also an array, an array of numbers with the same length as `a` |

**Returns**: `boolean`. `true` if `a` is less than `b`, `false` otherwise. If `a` is an array, returns `true` only if every element of `a` is less than `b`, or less than the element at the same index of `b` if `b` is an array.

**Throws**:

* `'Missing b value'` if `b` is not provided
* `'Array length mismatch'` if `a` and `b` are arrays of different lengths

**Example**

```js
lt(1, 1) // returns false
lt(1, 2) // returns true
lt([1, 2], 3) // returns true
lt([1, 2], 2) // returns false
lt([1, 2], [2, 3]) // returns true
```


## lte( a, b ) [_lte_a_b]

Checks whether one value is less than or equal to another. You can also write this comparison as `a <= b`.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| b | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `boolean`. `true` if `a` is less than or equal to `b`, `false` otherwise.

The result for arrays depends on the version:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` If `a` or `b` is an array, returns `true` only if every element satisfies the comparison.
- {applies_to}`stack: ga 9.0-9.4` If `a` is an array, returns `true` only if every element is equal to the other value, or every element is less.

**Throws**:

* `'Missing b value'` if `b` is not provided
* `'Array length mismatch'` if `a` and `b` are arrays of different lengths

**Example**

```js
lte(1, 1) // returns true
lte(1, 2) // returns true
lte([1, 2], [1, 1]) // returns false
```

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` More array comparisons:

```js
lte([1, 2], 2) // returns true
lte(1, [1, 2]) // returns true
```

{applies_to}`stack: ga 9.0-9.4` More array comparisons:

```js
lte([1, 2], 2) // returns false
lte(1, [1, 2]) // returns false
```


## max( …args ) [_max_args] 

Finds the maximum value of one or more numbers or arrays of numbers. If you pass several arguments and at least one is an array, the function finds the maximum by index.

| Param | Type | Description |
| --- | --- | --- |
| …args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The maximum value of all numbers if `args` contains only numbers. Returns an array with the maximum values at each index, including all scalar numbers in `args` in the calculation at each index if you pass several arguments and at least one is an array. If you pass a single array, the result covers every element.

**Throws**: `'Array length mismatch'` if `args` contains arrays of different lengths

**Example**

```js
max(1, 2, 3) // returns 3
max([10, 20, 30, 40], 15) // returns [15, 20, 30, 40]
max([1, 9], 4, [3, 5]) // returns [max([1, 4, 3]), max([9, 4, 5])] = [4, 9]
max([3, 1, 4]) // returns 4
```


## mean( …args ) [_mean_args] 

Finds the mean value of one or more numbers or arrays of numbers. If you pass several arguments and at least one is an array, the function finds the mean by index.

| Param | Type | Description |
| --- | --- | --- |
| …args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The mean value of all numbers if `args` contains only numbers. Returns an array with the mean values of each index, including all scalar numbers in `args` in the calculation at each index if you pass several arguments and at least one is an array. If you pass a single array, the result covers every element.

**Throws**: `'Array length mismatch'` if `args` contains arrays of different lengths

**Example**

```js
mean(1, 2, 3) // returns 2
mean([10, 20, 30, 40], 20) // returns [15, 20, 25, 30]
mean([1, 9], 5, [3, 4]) // returns [mean([1, 5, 3]), mean([9, 5, 4])] = [3, 6]
mean([1, 2, 6]) // returns 3
```


## median( …args ) [_median_args] 

Finds the median value(s) of one or more numbers or arrays of numbers. If you pass several arguments and at least one is an array, the function finds the median by index.

| Param | Type | Description |
| --- | --- | --- |
| …args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The median value of all numbers if `args` contains only numbers. Returns an array with the median values of each index, including all scalar numbers in `args` in the calculation at each index if you pass several arguments and at least one is an array. If you pass a single array, the result covers every element.

**Throws**: `'Array length mismatch'` if `args` contains arrays of different lengths

**Example**

```js
median(1, 1, 2, 3) // returns 1.5
median(1, 1, 2, 2, 3) // returns 2
median([10, 20, 30, 40], 10, 20, 30) // returns [15, 20, 25, 25]
median([1, 9], 2, 4, [3, 5]) // returns [median([1, 2, 4, 3]), median([9, 2, 4, 5])] = [2.5, 4.5]
median([3, 1, 4, 1, 5]) // returns 3
```


## min( …args ) [_min_args] 

Finds the minimum value of one or more numbers or arrays of numbers. If you pass several arguments and at least one is an array, the function finds the minimum by index.

| Param | Type | Description |
| --- | --- | --- |
| …args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The minimum value of all numbers if `args` contains only numbers. Returns an array with the minimum values of each index, including all scalar numbers in `args` in the calculation at each index if you pass several arguments and at least one is an array. If you pass a single array, the result covers every element.

**Throws**: `'Array length mismatch'` if `args` contains arrays of different lengths

**Example**

```js
min(1, 2, 3) // returns 1
min([10, 20, 30, 40], 25) // returns [10, 20, 25, 25]
min([1, 9], 4, [3, 5]) // returns [min([1, 4, 3]), min([9, 4, 5])] = [1, 4]
min([3, 1, 4]) // returns 1
```


## mod( a, b ) [_mod_a_b] 

Remainder after dividing two numbers. If either argument is an array, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | dividend, a number or an array of numbers |
| b | number &#124; Array.<number> | divisor, a number or an array of numbers, b != 0 |

**Returns**: `number` | `Array.<number>`. The remainder of `a` divided by `b` if both are numbers. Returns an array with the remainders applied index-wise to each element if `a` or `b` is an array. If `a` is a number and `b` is an array that contains 0, the result for that element is `NaN`.

**Throws**:

* `'Array length mismatch'` if `a` and `b` are arrays with different lengths
* `'Cannot divide by 0'` if `b` is 0, or if `a` and `b` are both arrays and `b` contains 0

**Example**

```js
mod(10, 7) // returns 3
mod([11, 22, 33, 44], 10) // returns [1, 2, 3, 4]
mod(100, [3, 7, 11, 23]) // returns [1, 2, 1, 8]
mod([14, 42, 65, 108], [5, 4, 14, 2]) // returns [4, 2, 9, 0]
```


## mode( …args ) [_mode_args] 

Finds the mode value(s) of one or more numbers or arrays of numbers. If you pass several arguments and at least one is an array, the function finds the mode by index.

| Param | Type | Description |
| --- | --- | --- |
| …args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `Array.<number>` | `Array.<Array.<number>>`. An array of mode value(s) of all numbers if `args` contains only numbers. Returns an array of arrays with mode value(s) of each index, including all scalar numbers in `args` in the calculation at each index if you pass several arguments and at least one is an array. If you pass a single array, the result covers every element.

**Throws**: `'Array length mismatch'` if `args` contains arrays of different lengths

**Example**

```js
mode(1, 1, 2, 3) // returns [1]
mode(1, 1, 2, 2, 3) // returns [1,2]
mode([10, 20, 30, 40], 10, 20, 30) // returns [[10], [20], [30], [10, 20, 30, 40]]
mode([1, 9], 1, 4, [3, 5]) // returns [mode([1, 1, 4, 3]), mode([9, 1, 4, 5])] = [[1], [1, 4, 5, 9]]
mode([1, 1, 2]) // returns [1]
```


## multiply( a, b ) [_multiply_a_b] 

Multiplies two numbers. If either argument is an array, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| b | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The product of `a` and `b` if both are numbers. Returns an array with the products applied index-wise to each element if `a` or `b` is an array.

**Throws**: `'Array length mismatch'` if `a` and `b` are arrays with different lengths

**Example**

```js
multiply(6, 3) // returns 18
multiply([10, 20, 30, 40], 10) // returns [100, 200, 300, 400]
multiply(10, [1, 2, 5, 10]) // returns [10, 20, 50, 100]
multiply([1, 2, 3, 4], [2, 7, 5, 12]) // returns [2, 14, 15, 48]
```


## pi() [_pi]

Returns the mathematical constant pi.

**Returns**: `number`. The mathematical constant pi, `3.141592653589793`.

**Example**

```js
pi() // returns 3.141592653589793
```


## pow( a, b ) [_pow_a_b] 

Raises a number to a given exponent. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| b | number | the power that `a` is raised to |

**Returns**: `number` | `Array.<number>`. `a` raised to the power of `b`. Returns an array with each element raised to the power of `b` if `a` is an array.

**Throws**: `'Missing exponent'` if `b` is not provided

**Example**

```js
pow(2, 3) // returns 8
pow([1, 2, 3], 4) // returns [1, 16, 81]
```


## radtodeg( a ) [_radtodeg_a]

Converts radians to degrees. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers in radians |

**Returns**: `number` | `Array.<number>`. `a` converted to degrees. Returns an array with each element converted to degrees if `a` is an array.

**Example**

```js
radtodeg(0) // returns 0
radtodeg(1.5707963267948966) // returns 90
radtodeg([0, 1.5707963267948966, 3.141592653589793, 6.283185307179586]) // returns [0, 90, 180, 360]
```


## random( a, b ) [_random_a_b]

Generates a random number within the given range where the lower bound is inclusive and the upper bound is exclusive. If you pass no numbers, it returns a number between 0 and 1. If you pass one number, it returns a number between 0 and that number.

| Param | Type | Description |
| --- | --- | --- |
| a | number | (optional) must be 0 or greater if `b` is not provided |
| b | number | (optional) must be greater than or equal to `a` |

**Returns**: `number`. A random number between 0 and 1 if you pass no numbers. Returns a random number between 0 and `a` if you pass one number. Returns a random number between `a` and `b` if you pass two numbers.

**Throws**: `'Min is greater than max'` if `a` < 0 when you pass only `a`, or if `a` > `b` when you pass both `a` and `b`

**Example**

```js
random() // returns a random number between 0 (inclusive) and 1 (exclusive)
random(10) // returns a random number between 0 (inclusive) and 10 (exclusive)
random(-10, 10) // returns a random number between -10 (inclusive) and 10 (exclusive)
```


## range( …args ) [_range_args] 

Finds the range of one or more numbers or arrays of numbers. If you pass several arguments and at least one is an array, the function finds the range by index.

| Param | Type | Description |
| --- | --- | --- |
| …args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The range value of all numbers if `args` contains only numbers. Returns an array with the range values at each index, including all scalar numbers in `args` in the calculation at each index if you pass several arguments and at least one is an array. If you pass a single array, the result covers every element.

**Throws**: `'Array length mismatch'` if `args` contains arrays of different lengths

**Example**

```js
range(1, 2, 3) // returns 2
range([10, 20, 30, 40], 15) // returns [5, 5, 15, 25]
range([1, 9], 4, [3, 5]) // returns [range([1, 4, 3]), range([9, 4, 5])] = [3, 5]
range([1, 9, 4]) // returns 8
```


## round( a, b ) [_round_a_b] 

Rounds a number to the nearest integer by default, or to a number of decimal places if you pass `b`. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| b | number | (optional) number of decimal places, default value: 0 |

**Returns**: `number` | `Array.<number>`. The rounded value of `a`. Returns an array with the rounded values of each element if `a` is an array.

**Example**

```js
round(1.2) // returns 1
round(-10.51) // returns -11
round(-10.1, 2) // returns -10.1
round(10.93745987, 4) // returns 10.9375
round([2.9234, 5.1234, 3.5234, 4.49234324], 2) // returns [2.92, 5.12, 3.52, 4.49]
```


## sin( a ) [_sin_a]

Calculates the sine of a number. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers in radians |

**Returns**: `number` | `Array.<number>`. The sine of `a`. Returns an array with the sine of each element if `a` is an array.

**Example**

```js
sin(0) // returns 0
sin(1.5707963267948966) // returns 1
sin([0, 1.5707963267948966]) // returns [0, 1]
```


## size( a ) [_size_a] 

Returns the length of an array. Alias for [`count`](#_count_a).

| Param | Type | Description |
| --- | --- | --- |
| a | Array.<any> | array of any values |

**Returns**: `number`. The length of the array.

**Throws**: `'Must pass an array'` if `a` is not an array

**Example**

```js
size([]) // returns 0
size([-1, -2, -3, -4]) // returns 4
```


## sqrt( a ) [_sqrt_a] 

Calculates the square root of a number. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The square root of `a`. Returns an array with the square roots of each element if `a` is an array.

**Throws**: `'Unable find the square root of a negative number'` if `a` < 0

**Example**

```js
sqrt(9) // returns 3
sqrt(30) // returns 5.477225575051661
sqrt([9, 16, 25]) // returns [3, 4, 5]
```


## square( a ) [_square_a] 

Calculates the square of a number. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The square of `a`. Returns an array with the squares of each element if `a` is an array.

**Example**

```js
square(-3) // returns 9
square([3, 4, 5]) // returns [9, 16, 25]
```


## subtract( a, b ) [_subtract_a_b] 

Subtracts two numbers. If either argument is an array, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| b | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The difference of `a` and `b` if both are numbers, or an array of differences applied index-wise to each element.

**Throws**: `'Array length mismatch'` if `a` and `b` are arrays with different lengths

**Example**

```js
subtract(6, 3) // returns 3
subtract([10, 20, 30, 40], 10) // returns [0, 10, 20, 30]
subtract(10, [1, 2, 5, 10]) // returns [9, 8, 5, 0]
subtract([14, 42, 65, 108], [2, 7, 5, 12]) // returns [12, 35, 60, 96]
```


## sum( …args ) [_sum_args]

Calculates the sum of one or more numbers or arrays. If an argument is an array, the function adds its elements. The arrays can have different lengths.

| Param | Type | Description |
| --- | --- | --- |
| …args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number`. The sum of all numbers and all elements of any arrays in `args`.

**Example**

```js
sum(1, 2, 3) // returns 6
sum([10, 20, 30, 40], 10, 20, 30) // returns 160
sum([1, 2], 3, [4, 5], 6) // returns sum(1, 2, 3, 4, 5, 6) = 21
sum([10, 20, 30, 40], 10, [1, 2, 3], 22) // returns sum(10, 20, 30, 40, 10, 1, 2, 3, 22) = 138
```


## tan( a ) [_tan_a]

Calculates the tangent of a number. For arrays, the function applies to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers in radians |

**Returns**: `number` | `Array.<number>`. The tangent of `a`. Returns an array with the tangent of each element if `a` is an array.

**Example**

```js
tan(0) // returns 0
tan(1) // returns 1.5574077246549023
tan([0, 1, -1]) // returns [0, 1.5574077246549023, -1.5574077246549023]
```


## unique( a ) [_unique_a]

Counts the number of unique values in an array.

| Param | Type | Description |
| --- | --- | --- |
| a | Array.<any> | array of any values |

**Returns**: `number`. The number of unique values in the array. Returns 1 if `a` is not an array.

**Example**

```js
unique(100) // returns 1
unique([]) // returns 0
unique([1, 2, 3, 4]) // returns 4
unique([1, 2, 3, 4, 2, 2, 2, 3, 4, 2, 4, 5, 2, 1, 4, 2]) // returns 5
```
