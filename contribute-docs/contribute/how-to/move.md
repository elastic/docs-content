# Move files and folders

When you move a source file or folder, you must also update all inbound and outbound links to reflect the new file location. `docs-builder` provides tooling to handle this step for you.

## `docs-builder mv`

Move a file or folder from one location to another and update all links in the documentation. For example:

```bash
docs-builder mv ./old-location/ia.md ./new-location/ia.md
```

:::{important}
The `docset.yml` and `toc.yml` files are not automatically updated when using this tool. You must update these references manually.
:::

## `docs-builder mv --help`

```bash
Usage: mv [arguments...] [options...] [-h|--help] [--version]

Move a file or folder from one location to another and update all links in the documentation

Arguments:
  [0] <string?>    The source file or folder path to move from
  [1] <string?>    The target file or folder path to move to

Options:
  --dry-run <bool?>      Dry run the move operation (Default: null)
  -p|--path <string?>    Defaults to the`{pwd}` folder (Default: null)
```
