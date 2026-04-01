% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```js
const response = await client.index({
  index: "books",
  document: {
    name: "The Great Gatsby",
    author: "F. Scott Fitzgerald",
    release_date: "1925-04-10",
    page_count: 180,
    language: "EN",
  },
});
console.log(response);
```
