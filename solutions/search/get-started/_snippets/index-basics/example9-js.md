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
