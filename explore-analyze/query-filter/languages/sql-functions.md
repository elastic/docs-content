---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions.html
---

# Functions and Operators [sql-functions]

Elasticsearch SQL provides a comprehensive set of built-in operators and functions:

* [Operators](sql-operators.md)

    * [`Equality (=)`](sql-operators.md#sql-operators-equality)
    * [`Null safe Equality (<=>)`](sql-operators.md#sql-operators-null-safe-equality)
    * [`Inequality (<> or !=)`](sql-operators.md#sql-operators-inequality)
    * [`Comparison (<, <=, >, >=)`](sql-operators.md#sql-operators-comparison)
    * [`BETWEEN`](sql-operators.md#sql-operators-between)
    * [`IS NULL/IS NOT NULL`](sql-operators.md#sql-operators-is-null)
    * [`IN (<value1>, <value2>, ...)`](sql-operators.md#sql-operators-in)
    * [`AND`](sql-operators-logical.md#sql-operators-and)
    * [`OR`](sql-operators-logical.md#sql-operators-or)
    * [`NOT`](sql-operators-logical.md#sql-operators-not)
    * [`Add (+)`](sql-operators-math.md#sql-operators-plus)
    * [`Subtract (infix -)`](sql-operators-math.md#sql-operators-subtract)
    * [`Negate (unary -)`](sql-operators-math.md#sql-operators-negate)
    * [`Multiply (*)`](sql-operators-math.md#sql-operators-multiply)
    * [`Divide (/)`](sql-operators-math.md#sql-operators-divide)
    * [`Modulo or Remainder(%)`](sql-operators-math.md#sql-operators-remainder)
    * [`Cast (::)`](sql-operators-cast.md#sql-operators-cast-cast)

* [LIKE and RLIKE Operators](sql-like-rlike-operators.md)

    * [`LIKE`](sql-like-rlike-operators.md#sql-like-operator)
    * [`RLIKE`](sql-like-rlike-operators.md#sql-rlike-operator)

* [Aggregate Functions](sql-functions-aggs.md)

    * [`AVG`](sql-functions-aggs.md#sql-functions-aggs-avg)
    * [`COUNT`](sql-functions-aggs.md#sql-functions-aggs-count)
    * [`COUNT(ALL)`](sql-functions-aggs.md#sql-functions-aggs-count-all)
    * [`COUNT(DISTINCT)`](sql-functions-aggs.md#sql-functions-aggs-count-distinct)
    * [`FIRST/FIRST_VALUE`](sql-functions-aggs.md#sql-functions-aggs-first)
    * [`LAST/LAST_VALUE`](sql-functions-aggs.md#sql-functions-aggs-last)
    * [`MAX`](sql-functions-aggs.md#sql-functions-aggs-max)
    * [`MIN`](sql-functions-aggs.md#sql-functions-aggs-min)
    * [`SUM`](sql-functions-aggs.md#sql-functions-aggs-sum)
    * [`KURTOSIS`](sql-functions-aggs.md#sql-functions-aggs-kurtosis)
    * [`MAD`](sql-functions-aggs.md#sql-functions-aggs-mad)
    * [`PERCENTILE`](sql-functions-aggs.md#sql-functions-aggs-percentile)
    * [`PERCENTILE_RANK`](sql-functions-aggs.md#sql-functions-aggs-percentile-rank)
    * [`SKEWNESS`](sql-functions-aggs.md#sql-functions-aggs-skewness)
    * [`STDDEV_POP`](sql-functions-aggs.md#sql-functions-aggs-stddev-pop)
    * [`STDDEV_SAMP`](sql-functions-aggs.md#sql-functions-aggs-stddev-samp)
    * [`SUM_OF_SQUARES`](sql-functions-aggs.md#sql-functions-aggs-sum-squares)
    * [`VAR_POP`](sql-functions-aggs.md#sql-functions-aggs-var-pop)
    * [`VAR_SAMP`](sql-functions-aggs.md#sql-functions-aggs-var-samp)

* [Grouping Functions](sql-functions-grouping.md)

    * [`HISTOGRAM`](sql-functions-grouping.md#sql-functions-grouping-histogram)

* [Date-Time Operators](sql-functions-datetime.md#sql-functions-datetime-interval)
* [Date-Time Functions](sql-functions-datetime.md#sql-functions-current-date)

    * [`CURRENT_DATE/CURDATE`](sql-functions-datetime.md#sql-functions-current-date)
    * [`CURRENT_TIME/CURTIME`](sql-functions-datetime.md#sql-functions-current-time)
    * [`CURRENT_TIMESTAMP`](sql-functions-datetime.md#sql-functions-current-timestamp)
    * [`DATE_ADD/DATEADD/TIMESTAMP_ADD/TIMESTAMPADD`](sql-functions-datetime.md#sql-functions-datetime-add)
    * [`DATE_DIFF/DATEDIFF/TIMESTAMP_DIFF/TIMESTAMPDIFF`](sql-functions-datetime.md#sql-functions-datetime-diff)
    * [`DATE_FORMAT`](sql-functions-datetime.md#sql-functions-datetime-dateformat)
    * [`DATE_PARSE`](sql-functions-datetime.md#sql-functions-datetime-dateparse)
    * [`DATETIME_FORMAT`](sql-functions-datetime.md#sql-functions-datetime-datetimeformat)
    * [`DATETIME_PARSE`](sql-functions-datetime.md#sql-functions-datetime-datetimeparse)
    * [`FORMAT`](sql-functions-datetime.md#sql-functions-datetime-format)
    * [`DATE_PART/DATEPART`](sql-functions-datetime.md#sql-functions-datetime-part)
    * [`DATE_TRUNC/DATETRUNC`](sql-functions-datetime.md#sql-functions-datetime-trunc)
    * [`DAY_OF_MONTH/DOM/DAY`](sql-functions-datetime.md#sql-functions-datetime-day)
    * [`DAY_OF_WEEK/DAYOFWEEK/DOW`](sql-functions-datetime.md#sql-functions-datetime-dow)
    * [`DAY_OF_YEAR/DOY`](sql-functions-datetime.md#sql-functions-datetime-doy)
    * [`DAY_NAME/DAYNAME`](sql-functions-datetime.md#sql-functions-datetime-dayname)
    * [`EXTRACT`](sql-functions-datetime.md#sql-functions-datetime-extract)
    * [`HOUR_OF_DAY/HOUR`](sql-functions-datetime.md#sql-functions-datetime-hour)
    * [`ISO_DAY_OF_WEEK/ISODAYOFWEEK/ISODOW/IDOW`](sql-functions-datetime.md#sql-functions-datetime-isodow)
    * [`ISO_WEEK_OF_YEAR/ISOWEEKOFYEAR/ISOWEEK/IWOY/IW`](sql-functions-datetime.md#sql-functions-datetime-isoweek)
    * [`MINUTE_OF_DAY`](sql-functions-datetime.md#sql-functions-datetime-minuteofday)
    * [`MINUTE_OF_HOUR/MINUTE`](sql-functions-datetime.md#sql-functions-datetime-minute)
    * [`MONTH_OF_YEAR/MONTH`](sql-functions-datetime.md#sql-functions-datetime-month)
    * [`MONTH_NAME/MONTHNAME`](sql-functions-datetime.md#sql-functions-datetime-monthname)
    * [`NOW`](sql-functions-datetime.md#sql-functions-now)
    * [`SECOND_OF_MINUTE/SECOND`](sql-functions-datetime.md#sql-functions-datetime-second)
    * [`QUARTER`](sql-functions-datetime.md#sql-functions-datetime-quarter)
    * [`TIME_PARSE`](sql-functions-datetime.md#sql-functions-datetime-timeparse)
    * [`TO_CHAR`](sql-functions-datetime.md#sql-functions-datetime-to_char)
    * [`TODAY`](sql-functions-datetime.md#sql-functions-today)
    * [`WEEK_OF_YEAR/WEEK`](sql-functions-datetime.md#sql-functions-datetime-week)
    * [`YEAR`](sql-functions-datetime.md#sql-functions-datetime-year)

* [Full-Text Search Functions](sql-functions-search.md)

    * [`MATCH`](sql-functions-search.md#sql-functions-search-match)
    * [`QUERY`](sql-functions-search.md#sql-functions-search-query)
    * [`SCORE`](sql-functions-search.md#sql-functions-search-score)

* [Mathematical Functions](sql-functions-math.md)

    * [`ABS`](sql-functions-math.md#sql-functions-math-abs)
    * [`CBRT`](sql-functions-math.md#sql-functions-math-cbrt)
    * [`CEIL/CEILING`](sql-functions-math.md#sql-functions-math-ceil)
    * [`E`](sql-functions-math.md#sql-functions-math-e)
    * [`EXP`](sql-functions-math.md#sql-functions-math-exp)
    * [`EXPM1`](sql-functions-math.md#sql-functions-math-expm1)
    * [`FLOOR`](sql-functions-math.md#sql-functions-math-floor)
    * [`LOG`](sql-functions-math.md#sql-functions-math-log)
    * [`LOG10`](sql-functions-math.md#sql-functions-math-log10)
    * [`PI`](sql-functions-math.md#sql-functions-math-pi)
    * [`POWER`](sql-functions-math.md#sql-functions-math-power)
    * [`RANDOM/RAND`](sql-functions-math.md#sql-functions-math-random)
    * [`ROUND`](sql-functions-math.md#sql-functions-math-round)
    * [`SIGN/SIGNUM`](sql-functions-math.md#sql-functions-math-sign)
    * [`SQRT`](sql-functions-math.md#sql-functions-math-sqrt)
    * [`TRUNCATE/TRUNC`](sql-functions-math.md#sql-functions-math-truncate)
    * [`ACOS`](sql-functions-math.md#sql-functions-math-acos)
    * [`ASIN`](sql-functions-math.md#sql-functions-math-asin)
    * [`ATAN`](sql-functions-math.md#sql-functions-math-atan)
    * [`ATAN2`](sql-functions-math.md#sql-functions-math-atan2)
    * [`COS`](sql-functions-math.md#sql-functions-math-cos)
    * [`COSH`](sql-functions-math.md#sql-functions-math-cosh)
    * [`COT`](sql-functions-math.md#sql-functions-math-cot)
    * [`DEGREES`](sql-functions-math.md#sql-functions-math-degrees)
    * [`RADIANS`](sql-functions-math.md#sql-functions-math-radians)
    * [`SIN`](sql-functions-math.md#sql-functions-math-sin)
    * [`SINH`](sql-functions-math.md#sql-functions-math-sinh)
    * [`TAN`](sql-functions-math.md#sql-functions-math-tan)

* [String Functions](sql-functions-string.md)

    * [`ASCII`](sql-functions-string.md#sql-functions-string-ascii)
    * [`BIT_LENGTH`](sql-functions-string.md#sql-functions-string-bit-length)
    * [`CHAR`](sql-functions-string.md#sql-functions-string-char)
    * [`CHAR_LENGTH`](sql-functions-string.md#sql-functions-string-char-length)
    * [`CONCAT`](sql-functions-string.md#sql-functions-string-concat)
    * [`INSERT`](sql-functions-string.md#sql-functions-string-insert)
    * [`LCASE`](sql-functions-string.md#sql-functions-string-lcase)
    * [`LEFT`](sql-functions-string.md#sql-functions-string-left)
    * [`LENGTH`](sql-functions-string.md#sql-functions-string-length)
    * [`LOCATE`](sql-functions-string.md#sql-functions-string-locate)
    * [`LTRIM`](sql-functions-string.md#sql-functions-string-ltrim)
    * [`OCTET_LENGTH`](sql-functions-string.md#sql-functions-string-octet-length)
    * [`POSITION`](sql-functions-string.md#sql-functions-string-position)
    * [`REPEAT`](sql-functions-string.md#sql-functions-string-repeat)
    * [`REPLACE`](sql-functions-string.md#sql-functions-string-replace)
    * [`RIGHT`](sql-functions-string.md#sql-functions-string-right)
    * [`RTRIM`](sql-functions-string.md#sql-functions-string-rtrim)
    * [`SPACE`](sql-functions-string.md#sql-functions-string-space)
    * [`SUBSTRING`](sql-functions-string.md#sql-functions-string-substring)
    * [`TRIM`](sql-functions-string.md#sql-functions-string-trim)
    * [`UCASE`](sql-functions-string.md#sql-functions-string-ucase)

* [Type Conversion Functions](sql-functions-type-conversion.md)

    * [`CAST`](sql-functions-type-conversion.md#sql-functions-type-conversion-cast)
    * [`CONVERT`](sql-functions-type-conversion.md#sql-functions-type-conversion-convert)

* [Conditional Functions And Expressions](sql-functions-conditional.md)

    * [`CASE`](sql-functions-conditional.md#sql-functions-conditional-case)
    * [`COALESCE`](sql-functions-conditional.md#sql-functions-conditional-coalesce)
    * [`GREATEST`](sql-functions-conditional.md#sql-functions-conditional-greatest)
    * [`IFNULL`](sql-functions-conditional.md#sql-functions-conditional-ifnull)
    * [`IIF`](sql-functions-conditional.md#sql-functions-conditional-iif)
    * [`ISNULL`](sql-functions-conditional.md#sql-functions-conditional-isnull)
    * [`LEAST`](sql-functions-conditional.md#sql-functions-conditional-least)
    * [`NULLIF`](sql-functions-conditional.md#sql-functions-conditional-nullif)
    * [`NVL`](sql-functions-conditional.md#sql-functions-conditional-nvl)

* [Geo Functions](sql-functions-geo.md)

    * [`ST_AsWKT`](sql-functions-geo.md#sql-functions-geo-st-as-wkt)
    * [`ST_Distance`](sql-functions-geo.md#sql-functions-geo-st-distance)
    * [`ST_GeometryType`](sql-functions-geo.md#sql-functions-geo-st-geometrytype)
    * [`ST_WKTToSQL`](sql-functions-geo.md#sql-functions-geo-st-wkt-to-sql)
    * [`ST_X`](sql-functions-geo.md#sql-functions-geo-st-x)
    * [`ST_Y`](sql-functions-geo.md#sql-functions-geo-st-y)
    * [`ST_Z`](sql-functions-geo.md#sql-functions-geo-st-z)

* [System Functions](sql-functions-system.md)

    * [`DATABASE`](sql-functions-system.md#sql-functions-system-database)
    * [`USER`](sql-functions-system.md#sql-functions-system-user)

















