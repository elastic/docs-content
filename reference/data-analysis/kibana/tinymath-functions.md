---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/canvas-tinymath-functions.html
---

# TinyMath functions [canvas-tinymath-functions]

TinyMath provides a set of functions that can be used with the Canvas expression language to perform complex math calculations. Read on for detailed information about the functions available in TinyMath, including what parameters each function accepts, the return value of that function, and examples of how each function behaves.

Most of the functions accept arrays and apply JavaScript Math methods to each element of that array. For the functions that accept multiple arrays as parameters, the function generally does the calculation index by index.

Any function can be wrapped by another function as long as the return type of the inner function matches the acceptable parameter type of the outer function.


## abs( a ) [_abs_a]

Calculates the absolute value of a number. For arrays, the function will be applied index-wise to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The absolute value of `a`. Returns an array with the absolute values of each element if `a` is an array.

**Example**

```js
abs(-1) // returns 1
abs(2) // returns 2
abs([-1 , -2, 3, -4]) // returns [1, 2, 3, 4]
```


## add( …​args ) [_add_args]

Calculates the sum of one or more numbers/arrays passed into the function. If at least one array of numbers is passed into the function, the function will calculate the sum by index.

| Param | Type | Description |
| --- | --- | --- |
| …​args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The sum of all numbers in `args` if `args` contains only numbers. Returns an array of sums of the elements at each index, including all scalar numbers in `args` in the calculation at each index if `args` contains at least one array.

**Throws**: `'Array length mismatch'` if `args` contains arrays of different lengths

**Example**

```js
add(1, 2, 3) // returns 6
add([10, 20, 30, 40], 10, 20, 30) // returns [70, 80, 90, 100]
add([1, 2], 3, [4, 5], 6) // returns [(1 + 3 + 4 + 6), (2 + 3 + 5 + 6)] = [14, 16]
```


## cbrt( a ) [_cbrt_a]

Calculates the cube root of a number. For arrays, the function will be applied index-wise to each element.

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

Calculates the ceiling of a number, i.e., rounds a number towards positive infinity. For arrays, the function will be applied index-wise to each element.

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


## clamp( …​a, min, max ) [_clamp_a_min_max]

Restricts value to a given range and returns closed available value. If only `min` is provided, values are restricted to only a lower bound.

| Param | Type | Description |
| --- | --- | --- |
| …​a | number &#124; Array.<number> | one or more numbers or arrays of numbers |
| min | number &#124; Array.<number> | (optional) The minimum value this function will return. |
| max | number &#124; Array.<number> | (optional) The maximum value this function will return. |

**Returns**: `number` | `Array.<number>`. The closest value between `min` (inclusive) and `max` (inclusive). Returns an array with values greater than or equal to `min` and less than or equal to `max` (if provided) at each index.

**Throws**:

* `'Array length mismatch'` if a `min` and/or `max` are arrays of different lengths
* `'Min must be less than max'` if `max` is less than `min`

**Example**

```js
clamp(1, 2, 3) // returns 2
clamp([10, 20, 30, 40], 15, 25) // returns [15, 20, 25, 25]
clamp(10, [15, 2, 4, 20], 25) // returns [15, 10, 10, 20]
clamp(35, 10, [20, 30, 40, 50]) // returns [20, 30, 35, 35]
clamp([1, 9], 3, [4, 5]) // returns [clamp([1, 3, 4]), clamp([9, 3, 5])] = [3, 5]
```


## count( a ) [_count_a]

Returns the length of an array. Alias for size.

| Param | Type | Description |
| --- | --- | --- |
| a | Array.<any> | array of any values |

**Returns**: `number`. The length of the array.

**Throws**: `'Must pass an array'` if `a` is not an array.

**Example**

```js
count([]) // returns 0
count([-1, -2, -3, -4]) // returns 4
count(100) // returns 1
```


## cube( a ) [_cube_a]

Calculates the cube of a number. For arrays, the function will be applied index-wise to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The cube of `a`. Returns an array with the cubes of each element if `a` is an array.

**Example**

```js
cube(-3) // returns -27
cube([3, 4, 5]) // returns [27, 64, 125]
```


## divide( a, b ) [_divide_a_b]

Divides two numbers. If at least one array of numbers is passed into the function, the function will be applied index-wise to each element.

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


## exp( a ) [_exp_a]

Calculates *e^x* where *e* is Euler’s number. For arrays, the function will be applied index-wise to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. Returns an array with the values of `e^x` evaluated where `x` is each element of `a` if `a` is an array.

**Example**

```js
exp(2) // returns e^2 = 7.3890560989306495
exp([1, 2, 3]) // returns [e^1, e^2, e^3] = [2.718281828459045, 7.3890560989306495, 20.085536923187668]
```


## first( a ) [_first_a]

Returns the first element of an array. If anything other than an array is passed in, the input is returned.

| Param | Type | Description |
| --- | --- | --- |
| a | Array.<any> | array of any values |

**Returns**: `*`. The first element of `a`. Returns `a` if `a` is not an array.

**Example**

```js
first(2) // returns 2
first([1, 2, 3]) // returns 1
```


## fix( a ) [_fix_a]

Calculates the fix of a number, i.e., rounds a number towards 0. For arrays, the function will be applied index-wise to each element.

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

Calculates the floor of a number, i.e., rounds a number towards negative infinity. For arrays, the function will be applied index-wise to each element.

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


## last( a ) [_last_a]

Returns the last element of an array. If anything other than an array is passed in, the input is returned.

| Param | Type | Description |
| --- | --- | --- |
| a | Array.<any> | array of any values |

**Returns**: `*`. The last element of `a`. Returns `a` if `a` is not an array.

**Example**

```js
last(2) // returns 2
last([1, 2, 3]) // returns 3
```


## log( a, b ) [_log_a_b]

Calculates the logarithm of a number. For arrays, the function will be applied index-wise to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers, `a` must be greater than 0 |
| b | Object | (optional) base for the logarithm. If not provided a value, the default base is e, and the natural log is calculated. |

**Returns**: `number` | `Array.<number>`.  The logarithm of `a`. Returns an array with the the logarithms of each element if `a` is an array.

**Throws**:

* `'Base out of range'` if `b` ⇐ 0
* `'Must be greater than 0'` if `a` > 0

**Example**

```js
log(1) // returns 0
log(64, 8) // returns 2
log(42, 5) // returns 2.322344707681546
log([2, 4, 8, 16, 32], 2) // returns [1, 2, 3, 4, 5]
```


## log10( a ) [_log10_a]

Calculates the logarithm base 10 of a number. For arrays, the function will be applied index-wise to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers, `a` must be greater than 0 |

**Returns**: `number` | `Array.<number>`. The logarithm of `a`. Returns an array with the the logarithms base 10 of each element if `a` is an array.

**Throws**: `'Must be greater than 0'` if `a` < 0

**Example**

```js
log(10) // returns 1
log(100) // returns 2
log(80) // returns 1.9030899869919433
log([10, 100, 1000, 10000, 100000]) // returns [1, 2, 3, 4, 5]
```


## max( …​args ) [_max_args]

Finds the maximum value of one of more numbers/arrays of numbers passed into the function. If at least one array of numbers is passed into the function, the function will find the maximum by index.

| Param | Type | Description |
| --- | --- | --- |
| …​args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The maximum value of all numbers if `args` contains only numbers. Returns an array with the the maximum values at each index, including all scalar numbers in `args` in the calculation at each index if `args` contains at least one array.

**Throws**: `'Array length mismatch'` if `args` contains arrays of different lengths

**Example**

```js
max(1, 2, 3) // returns 3
max([10, 20, 30, 40], 15) // returns [15, 20, 30, 40]
max([1, 9], 4, [3, 5]) // returns [max([1, 4, 3]), max([9, 4, 5])] = [4, 9]
```


## mean( …​args ) [_mean_args]

Finds the mean value of one of more numbers/arrays of numbers passed into the function. If at least one array of numbers is passed into the function, the function will find the mean by index.

| Param | Type | Description |
| --- | --- | --- |
| …​args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The mean value of all numbers if `args` contains only numbers. Returns an array with the the mean values of each index, including all scalar numbers in `args` in the calculation at each index if `args` contains at least one array.

**Example**

```js
mean(1, 2, 3) // returns 2
mean([10, 20, 30, 40], 20) // returns [15, 20, 25, 30]
mean([1, 9], 5, [3, 4]) // returns [mean([1, 5, 3]), mean([9, 5, 4])] = [3, 6]
```


## median( …​args ) [_median_args]

Finds the median value(s) of one of more numbers/arrays of numbers passed into the function. If at least one array of numbers is passed into the function, the function will find the median by index.

| Param | Type | Description |
| --- | --- | --- |
| …​args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The median value of all numbers if `args` contains only numbers. Returns an array with the the median values of each index, including all scalar numbers in `args` in the calculation at each index if `args` contains at least one array.

**Example**

```js
median(1, 1, 2, 3) // returns 1.5
median(1, 1, 2, 2, 3) // returns 2
median([10, 20, 30, 40], 10, 20, 30) // returns [15, 20, 25, 25]
median([1, 9], 2, 4, [3, 5]) // returns [median([1, 2, 4, 3]), median([9, 2, 4, 5])] = [2.5, 4.5]
```


## min( …​args ) [_min_args]

Finds the minimum value of one of more numbers/arrays of numbers passed into the function. If at least one array of numbers is passed into the function, the function will find the minimum by index.

| Param | Type | Description |
| --- | --- | --- |
| …​args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The minimum value of all numbers if `args` contains only numbers. Returns an array with the the minimum values of each index, including all scalar numbers in `args` in the calculation at each index if `a` is an array.

**Throws**: `'Array length mismatch'` if `args` contains arrays of different lengths.

**Example**

```js
min(1, 2, 3) // returns 1
min([10, 20, 30, 40], 25) // returns [10, 20, 25, 25]
min([1, 9], 4, [3, 5]) // returns [min([1, 4, 3]), min([9, 4, 5])] = [1, 4]
```


## mod( a, b ) [_mod_a_b]

Remainder after dividing two numbers. If at least one array of numbers is passed into the function, the function will be applied index-wise to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | dividend, a number or an array of numbers |
| b | number &#124; Array.<number> | divisor, a number or an array of numbers, b != 0 |

**Returns**: `number` | `Array.<number>`. The remainder of `a` divided by `b` if both are numbers. Returns an array with the the remainders applied index-wise to each element if `a` or `b` is an array.

**Throws**:

* `'Array length mismatch'` if `a` and `b` are arrays with different lengths
* `'Cannot divide by 0'` if `b` equals 0 or contains 0

**Example**

```js
mod(10, 7) // returns 3
mod([11, 22, 33, 44], 10) // returns [1, 2, 3, 4]
mod(100, [3, 7, 11, 23]) // returns [1, 2, 1, 8]
mod([14, 42, 65, 108], [5, 4, 14, 2]) // returns [5, 2, 9, 0]
```


## mode( …​args ) [_mode_args]

Finds the mode value(s) of one of more numbers/arrays of numbers passed into the function. If at least one array of numbers is passed into the function, the function will find the mode by index.

| Param | Type | Description |
| --- | --- | --- |
| …​args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<Array.<number>>`. An array of mode value(s) of all numbers if `args` contains only numbers. Returns an array of arrays with mode value(s) of each index, including all scalar numbers in `args` in the calculation at each index if `args` contains at least one array.

**Example**

```js
mode(1, 1, 2, 3) // returns [1]
mode(1, 1, 2, 2, 3) // returns [1,2]
mode([10, 20, 30, 40], 10, 20, 30) // returns [[10], [20], [30], [10, 20, 30, 40]]
mode([1, 9], 1, 4, [3, 5]) // returns [mode([1, 1, 4, 3]), mode([9, 1, 4, 5])] = [[1], [4, 5, 9]]
```


## multiply( a, b ) [_multiply_a_b]

Multiplies two numbers. If at least one array of numbers is passed into the function, the function will be applied index-wise to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| b | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The product of `a` and `b` if both are numbers. Returns an array with the the products applied index-wise to each element if `a` or `b` is an array.

**Throws**: `'Array length mismatch'` if `a` and `b` are arrays with different lengths

**Example**

```js
multiply(6, 3) // returns 18
multiply([10, 20, 30, 40], 10) // returns [100, 200, 300, 400]
multiply(10, [1, 2, 5, 10]) // returns [10, 20, 50, 100]
multiply([1, 2, 3, 4], [2, 7, 5, 12]) // returns [2, 14, 15, 48]
```


## pow( a, b ) [_pow_a_b]

Calculates the cube root of a number. For arrays, the function will be applied index-wise to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| b | number | the power that `a` is raised to |

**Returns**: `number` | `Array.<number>`. `a` raised to the power of `b`. Returns an array with the each element raised to the power of `b` if `a` is an array.

**Throws**: `'Missing exponent'` if `b` is not provided

**Example**

```js
pow(2,3) // returns 8
pow([1, 2, 3], 4) // returns [1, 16, 81]
```


## random( a, b ) [_random_a_b]

Generates a random number within the given range where the lower bound is inclusive and the upper bound is exclusive. If no numbers are passed in, it will return a number between 0 and 1. If only one number is passed in, it will return a number between 0 and the number passed in.

| Param | Type | Description |
| --- | --- | --- |
| a | number | (optional) must be greater than 0 if `b` is not provided |
| b | number | (optional) must be greater than `a` |

**Returns**: `number`. A random number between 0 and 1 if no numbers are passed in. Returns a random number between 0 and `a` if only one number is passed in. Returns a random number between `a` and `b` if two numbers are passed in.

**Throws**: `'Min must be greater than max'` if `a` < 0 when only `a` is passed in or if `a` > `b` when both `a` and `b` are passed in

**Example**

```js
random() // returns a random number between 0 (inclusive) and 1 (exclusive)
random(10) // returns a random number between 0 (inclusive) and 10 (exclusive)
random(-10,10) // returns a random number between -10 (inclusive) and 10 (exclusive)
```


## range( …​args ) [_range_args]

Finds the range of one of more numbers/arrays of numbers passed into the function. If at least one array of numbers is passed into the function, the function will find the range by index.

| Param | Type | Description |
| --- | --- | --- |
| …​args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The range value of all numbers if `args` contains only numbers. Returns an array with the range values at each index, including all scalar numbers in `args` in the calculation at each index if `args` contains at least one array.

**Example**

```js
range(1, 2, 3) // returns 2
range([10, 20, 30, 40], 15) // returns [5, 5, 15, 25]
range([1, 9], 4, [3, 5]) // returns [range([1, 4, 3]), range([9, 4, 5])] = [3, 5]
```


## range( …​args ) [_range_args_2]

Finds the range of one of more numbers/arrays of numbers into the function. If at least one array of numbers is passed into the function, the function will find the range by index.

| Param | Type | Description |
| --- | --- | --- |
| …​args | number &#124; Array.<number> | one or more numbers or arrays of numbers |

**Returns**: `number` | `Array.<number>`. The range value of all numbers if `args` contains only numbers. Returns an array with the the range values at each index, including all scalar numbers in `args` in the calculation at each index if `args` contains at least one array.

**Example**

```js
range(1, 2, 3) // returns 2
range([10, 20, 30, 40], 15) // returns [5, 5, 15, 25]
range([1, 9], 4, [3, 5]) // returns [range([1, 4, 3]), range([9, 4, 5])] = [3, 5]
```


## round( a, b ) [_round_a_b]

Rounds a number towards the nearest integer by default, or decimal place (if passed in as `b`). For arrays, the function will be applied index-wise to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |
| b | number | (optional) number of decimal places, default value: 0 |

**Returns**: `number` | `Array.<number>`. The rounded value of `a`. Returns an array with the the rounded values of each element if `a` is an array.

**Example**

```js
round(1.2) // returns 2
round(-10.51) // returns -11
round(-10.1, 2) // returns -10.1
round(10.93745987, 4) // returns 10.9375
round([2.9234, 5.1234, 3.5234, 4.49234324], 2) // returns [2.92, 5.12, 3.52, 4.49]
```


## size( a ) [_size_a]

Returns the length of an array. Alias for count.

| Param | Type | Description |
| --- | --- | --- |
| a | Array.<any> | array of any values |

**Returns**: `number`. The length of the array.

**Throws**: `'Must pass an array'` if `a` is not an array

**Example**

```js
size([]) // returns 0
size([-1, -2, -3, -4]) // returns 4
size(100) // returns 1
```


## sqrt( a ) [_sqrt_a]

Calculates the square root of a number. For arrays, the function will be applied index-wise to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The square root of `a`. Returns an array with the the square roots of each element if `a` is an array.

**Throws**: `'Unable find the square root of a negative number'` if `a` < 0

**Example**

```js
sqrt(9) // returns 3
sqrt(30) //5.477225575051661
sqrt([9, 16, 25]) // returns [3, 4, 5]
```


## square( a ) [_square_a]

Calculates the square of a number. For arrays, the function will be applied index-wise to each element.

| Param | Type | Description |
| --- | --- | --- |
| a | number &#124; Array.<number> | a number or an array of numbers |

**Returns**: `number` | `Array.<number>`. The square of `a`. Returns an array with the the squares of each element if `a` is an array.

**Example**

```js
square(-3) // returns 9
square([3, 4, 5]) // returns [9, 16, 25]
```


## subtract( a, b ) [_subtract_a_b]

Subtracts two numbers. If at least one array of numbers is passed into the function, the function will be applied index-wise to each element.

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
subtract([14, 42, 65, 108], [2, 7, 5, 12]) // returns [12, 35, 52, 96]
```


## sum( …​args ) [_sum_args]

Calculates the sum of one or more numbers/arrays passed into the function. If at least one array is passed, the function will sum up one or more numbers/arrays of numbers and distinct values of an array. Sum accepts arrays of different lengths.

**Returns**: `number`. The sum of one or more numbers/arrays of numbers including distinct values in arrays

**Example**

```js
sum(1, 2, 3) // returns 6
sum([10, 20, 30, 40], 10, 20, 30) // returns 160
sum([1, 2], 3, [4, 5], 6) // returns sum(1, 2, 3, 4, 5, 6) = 21
sum([10, 20, 30, 40], 10, [1, 2, 3], 22) // returns sum(10, 20, 30, 40, 10, 1, 2, 3, 22) = 138
```


## unique( a ) [_unique_a]

Counts the number of unique values in an array.

**Returns**: `number`. The number of unique values in the array. Returns 1 if `a` is not an array.

**Example**

```js
unique(100) // returns 1
unique([]) // returns 0
unique([1, 2, 3, 4]) // returns 4
unique([1, 2, 3, 4, 2, 2, 2, 3, 4, 2, 4, 5, 2, 1, 4, 2]) // returns 5
```

