---
navigation_title: Set up redirects
---

# Manage redirects across doc sets

When you [move](move.md) or delete pages, other [documentation sets](../configure/content-set/index.md) might still link to them. This can lead to a chicken-and-egg problem: you can't publish your changes without breaking links elsewhere.

Redirects let you map old links to new targets across documentation sets, so you can publish changes while updating other doc sets.

## Limitations

Redirects only work within Elastic Docs V3 content sets. You cannot use this method to redirect to external destinations like [API docs](https://www.elastic.co/docs/api/).

For API redirects, consult with the documentation engineering team on Slack (#elastic-docs-v3).

For elastic.co/guide redirects, open a [web team request](http://ela.st/web-request).

## Add a redirect

To successfully implement a redirect:

1. Locate and open the `redirects.yml` file to edit.
   - Each docs repository powered by Docs V3 can have its own `redirects.yml` file. You must only edit the one in the repository that you're moving or removing files from.
   - It is at the same location as the `docset.yml` file. Depending on the repository, this is generally at the root or within the `/docs` folder of the repository.

   :::{note}
   Some repositories might not yet have a `redirects.yml` file. In this case, create one next to the repo's `docset.yml` file. Refer to [](#file-location).
   :::

2. Edit the file. Refer to [](#syntax) to get details on the expected syntax.
   - All paths must be relative to the `redirects.yml` file.
   - You may need to adjust the syntax based on how you'd like to treat anchors within redirected files. Find examples in [](#syntax).

3. Fix all existing links to the moved or removed file within the repository where you're adding the redirect, by updating them to the new correct target, or by removing them if necessary. This is a best practice to keep our content healthy, and mandatory for your PR to pass CI checks.

4. Create a PR with all of the changes made through the previous steps. 

CI checks run to validate the newly added redirect and the docs build. 
If you get validation errors about the redirect, double check that your changes follow all the steps in this procedure. If the errors persist after a writer reviewed the PR, ask @elastic/docs-engineering for assistance.

## Validation

Running `docs-builder diff validate` will give you feedback on whether all necessary redirect rules are in place after your changes. It will also run on pull requests.

## File location

Redirects are configured at the content set-level.
The configuration file should be located next to your `docset.yml` file:

* `redirects.yml` if you use `docset.yml`
* `_redirects.yml` if you use `_docset.yml`

## Syntax

Example syntax:

```yaml
redirects:
  'testing/redirects/4th-page.md': 'testing/redirects/5th-page.md'
  'testing/redirects/9th-page.md': '!testing/redirects/5th-page.md'
  'testing/redirects/6th-page.md':
  'testing/redirects/7th-page.md':
    to: 'testing/redirects/5th-page.md'
    anchors: '!'
  'testing/redirects/first-page-old.md':
    to: 'testing/redirects/second-page.md'
    anchors:
      'old-anchor': 'active-anchor'
      'removed-anchor':
  'testing/redirects/second-page-old.md':
    many:
      - to: "testing/redirects/second-page.md"
        anchors:
          "aa": "zz"
          "removed-anchor":
      - to: "testing/redirects/third-page.md"
        anchors:
          "bb": "yy"
  'testing/redirects/third-page.md':
    anchors:
      'removed-anchor':
  'testing/redirects/cross-repo-page.md': 'other-repo://reference/section/new-cross-repo-page.md'
  'testing/redirects/8th-page.md':
    to: 'other-repo://reference/section/new-cross-repo-page.md'
    anchors: '!'
    many:
      - to: 'testing/redirects/second-page.md'
        anchors:
          'item-a': 'yy'
      - to: 'testing/redirects/third-page.md'
        anchors:
          'item-b': 
            
  
```

### Redirect preserving all anchors

This example redirects `4th-page.md#anchor` to `5th-page.md#anchor`:

```yaml
redirects:
  'testing/redirects/4th-page.md': 'testing/redirects/5th-page.md'
```
### Redirect stripping all anchors

This example strips all anchors from the source page.
Any remaining links resolving to anchors on `7th-page.md` will fail link validation.

```yaml
redirects:
  'testing/redirects/7th-page.md':
    to: 'testing/redirects/5th-page.md'
    anchors: '!'
```

Alternate syntax:

```yaml
redirects:
  'testing/redirects/7th-page.md': '!testing/redirects/5th-page.md'
```

To handle removed anchors on a page that still exists, omit the `to:` field:

```yaml
  'testing/redirects/third-page.md':
    anchors:
      'removed-anchor':
```

### Redirect with renamed anchors

This example redirects:

- `first-page-old.md#old-anchor` → `second-page.md#active-anchor`
- `first-page-old.md#removed-anchor` → `second-page.md`
- Any other anchor is passed through and validated normally.

```yaml
redirects:
  'testing/redirects/first-page-old.md':
    to: 'testing/redirects/second-page.md'
    anchors:
      'old-anchor': 'active-anchor'
      'removed-anchor':
```

### Redirecting to other repositories

Use the `repo://path/to/page.md` syntax to redirect across repositories.

```yaml
redirects:
  'testing/redirects/cross-repo-page.md': 'other-repo://reference/section/new-cross-repo-page.md'
```

### Managing complex scenarios with anchors

* `to`, `anchor` and `many` can be used together to support more complex scenarios.
* Setting `to` at the top level determines the default case, which can be used for partial redirects.
* Cross-repository links are supported, with the same syntax as in the previous example.
* The existing rules for `anchors` also apply here. To define a catch-all redirect, use `{}`.

```yaml
redirects:
  # In this first scenario, the default redirection target remains the same page, with anchors being preserved. 
  # Omitting the ``anchors`` tag or explicitly setting it as empty are both supported.
  'testing/redirects/8th-page.md':
    to: 'testing/redirects/8th-page.md'
    many:
      - to: 'testing/redirects/second-page.md'
        anchors:
          'item-a': 'yy'
      - to: 'testing/redirects/third-page.md'
        anchors:
          'item-b':

  # In this scenario, the default redirection target is a different page, and anchors are dropped.
  'testing/redirects/deleted-page.md':
    to: 'testing/redirects/5th-page.md'
    anchors: '!'
    many:
      - to: "testing/redirects/second-page.md"
        anchors:
          "aa": "zz"
          "removed-anchor":
      - to: "other-repo://reference/section/partial-content.md"
        anchors:
          "bb": "yy"
```
