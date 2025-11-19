```js
const response = await client.indices.delete({
  index: "books",
});
console.log(response);

const response1 = await client.indices.delete({
  index: "my-explicit-mappings-books",
});
console.log(response1);
```

% WARNING: This snippet is auto-generated. Do not edit directly.
% See https://github.com/leemthompo/python-console-converter/blob/main/README.md
